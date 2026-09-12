import os
import shutil
import uuid
from dotenv import load_dotenv
from slugify import slugify

load_dotenv()

from fastapi import BackgroundTasks, Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import auth, bulk_import, crud, models, schemas
from .database import Base, engine, get_db
from .scheduler import start_scheduler
from .webhook import trigger_github_rebuild

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = os.getenv("UPLOAD_DIR")
if not UPLOAD_DIR:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_DIR = os.path.join(base_dir, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Atharva Sharma Editorial CMS API", version="1.0.0")

# Mount uploads directory for serving uploaded images
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_anti_crawler_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Robots-Tag"] = "noindex, nofollow, noarchive"
    return response


@app.get("/robots.txt", response_class=PlainTextResponse)
def backend_robots():
    return "User-agent: *\nDisallow: /\n"


_scheduler = None


@app.on_event("startup")
def startup_init():
    global _scheduler
    try:
        import sys
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        from seed_posts import seed_posts
        seed_posts()
    except Exception as err:
        print(f"Auto-seed note: {err}")

    try:
        _scheduler = start_scheduler()
    except Exception as err:
        print(f"Scheduler startup note: {err}")


# ---------- Public routes (Journal index & detail pages call these) ----------

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "atharva-cms-backend"}


@app.get("/api/posts", response_model=list[schemas.PostOut])
def list_published_posts(category: str | None = None, db: Session = Depends(get_db)):
    return crud.get_published_posts(db, category)


@app.get("/api/posts/{slug}", response_model=schemas.PostOut)
def get_published_post(slug: str, db: Session = Depends(get_db)):
    post = crud.get_post_by_slug(db, slug)
    if not post or post.status != "published":
        raise HTTPException(status_code=404, detail="Dispatch not found")
    return post


# ---------- Auth ----------

@app.post("/api/admin/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest):
    if not auth.verify_admin_password(payload.password):
        raise HTTPException(status_code=401, detail="Incorrect master password")
    return schemas.TokenResponse(access_token=auth.create_access_token())


# ---------- Admin routes (Require Bearer JWT Token) ----------

@app.get("/api/admin/posts", response_model=list[schemas.PostOut])
def list_all_posts(db: Session = Depends(get_db), _: bool = Depends(auth.get_current_admin)):
    return crud.get_all_posts(db)


@app.get("/api/admin/posts/{post_id}", response_model=schemas.PostOut)
def get_admin_post(
    post_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(auth.get_current_admin),
):
    db_post = crud.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Dispatch not found")
    return db_post


@app.post("/api/admin/posts", response_model=schemas.PostOut)
def create_post(
    post: schemas.PostCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: bool = Depends(auth.get_current_admin),
):
    if post.status == "scheduled" and not post.scheduled_at:
        raise HTTPException(status_code=400, detail="scheduled_at is required when status is 'scheduled'")
    created = crud.create_post(db, post)
    if created.status == "published":
        background_tasks.add_task(trigger_github_rebuild, "cms_post_published", {"post_id": created.id, "action": "created"})
    return created


@app.put("/api/admin/posts/{post_id}", response_model=schemas.PostOut)
def update_post(
    post_id: int,
    updates: schemas.PostUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: bool = Depends(auth.get_current_admin),
):
    db_post = crud.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Dispatch not found")
    effective_status = updates.status or db_post.status
    effective_scheduled_at = updates.scheduled_at or db_post.scheduled_at
    if effective_status == "scheduled" and not effective_scheduled_at:
        raise HTTPException(status_code=400, detail="scheduled_at is required when status is 'scheduled'")
    was_published = db_post.status == "published"
    updated = crud.update_post(db, db_post, updates)
    if was_published or updated.status == "published":
        background_tasks.add_task(trigger_github_rebuild, "cms_post_published", {"post_id": updated.id, "action": "updated"})
    return updated


@app.delete("/api/admin/posts/{post_id}")
def delete_post(
    post_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: bool = Depends(auth.get_current_admin),
):
    db_post = crud.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Dispatch not found")
    was_published = db_post.status == "published"
    crud.delete_post(db, db_post)
    if was_published:
        background_tasks.add_task(trigger_github_rebuild, "cms_post_published", {"post_id": post_id, "action": "deleted"})
    return {"deleted": True}


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}


@app.post("/api/admin/upload")
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    _: bool = Depends(auth.get_current_admin),
):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}"
        )

    clean_stem = slugify(os.path.splitext(file.filename or "image")[0]) or "asset"
    unique_name = f"{uuid.uuid4().hex[:10]}_{clean_stem}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    base = os.getenv("API_BASE_URL") or str(request.base_url).rstrip('/')
    full_url = f"{base}/uploads/{unique_name}"

    return {
        "url": full_url,
        "filename": unique_name
    }


@app.post("/api/admin/posts/bulk-import")
async def bulk_import_posts(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: bool = Depends(auth.get_current_admin),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")
    contents = await file.read()
    result = bulk_import.import_posts_from_csv(db, contents)
    if result["published_count"] > 0:
        background_tasks.add_task(trigger_github_rebuild, "bulk_import_published", {"count": result["published_count"]})
    return result
