from datetime import datetime
from slugify import slugify
from sqlalchemy.orm import Session
from . import models, schemas


def make_unique_slug(db: Session, title: str) -> str:
    base = slugify(title)
    slug = base
    i = 2
    while db.query(models.Post).filter(models.Post.slug == slug).first():
        slug = f"{base}-{i}"
        i += 1
    return slug


def calc_read_time(body: str) -> int:
    words = len(body.split())
    return max(1, round(words / 200))


def create_post(db: Session, post: schemas.PostCreate) -> models.Post:
    if post.slug and post.slug.strip():
        slug = slugify(post.slug.strip())
        existing = db.query(models.Post).filter(models.Post.slug == slug).first()
        if existing:
            slug = f"{slug}-2"
    else:
        slug = make_unique_slug(db, post.title)

    db_post = models.Post(
        slug=slug,
        title=post.title,
        category=post.category,
        excerpt=post.excerpt,
        body=post.body,
        cover_image=post.cover_image,
        hero_image_alt=post.hero_image_alt or post.title,
        focus_position=post.focus_position or "center 35%",
        dispatch_id=post.dispatch_id or "ATH-26-01",
        volume=post.volume or "VOL. 04 // ISSUE 08",
        board=post.board or "DIRECT MALE RUNWAY",
        location=post.location or "UDAIPUR / MUMBAI / GLOBAL",
        order=post.order or 1,
        status=post.status,
        scheduled_at=post.scheduled_at,
        meta_title=post.meta_title,
        meta_description=post.meta_description,
        meta_keywords=post.meta_keywords,
        og_image=post.og_image,
        prev_slug=post.prev_slug,
        prev_title=post.prev_title,
        next_slug=post.next_slug,
        next_title=post.next_title,
        read_time_minutes=calc_read_time(post.body),
        published_at=datetime.utcnow() if post.status == "published" else None,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, db_post: models.Post, updates: schemas.PostUpdate) -> models.Post:
    data = updates.model_dump(exclude_unset=True)
    was_draft = db_post.status != "published"

    if "slug" in data:
        raw_slug = data.pop("slug")
        if raw_slug and raw_slug.strip():
            candidate = slugify(raw_slug.strip())
            existing = db.query(models.Post).filter(models.Post.slug == candidate, models.Post.id != db_post.id).first()
            if existing:
                candidate = f"{candidate}-{db_post.id}"
            db_post.slug = candidate

    for field, value in data.items():
        setattr(db_post, field, value)

    if "body" in data:
        db_post.read_time_minutes = calc_read_time(db_post.body)

    if was_draft and db_post.status == "published" and not db_post.published_at:
        db_post.published_at = datetime.utcnow()

    db.commit()
    db.refresh(db_post)
    return db_post


def get_published_posts(db: Session, category: str | None = None):
    query = db.query(models.Post).filter(models.Post.status == "published")
    if category and category.strip() and category.lower() != "all":
        query = query.filter(models.Post.category == category)
    return query.order_by(models.Post.order.asc(), models.Post.published_at.desc()).all()


def get_all_posts(db: Session):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).all()


def get_post_by_slug(db: Session, slug: str):
    return db.query(models.Post).filter(models.Post.slug == slug).first()


def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def publish_due_scheduled_posts(db: Session):
    now = datetime.utcnow()
    due_posts = (
        db.query(models.Post)
        .filter(models.Post.status == "scheduled")
        .filter(models.Post.scheduled_at <= now)
        .all()
    )
    for post in due_posts:
        post.status = "published"
        post.published_at = post.scheduled_at or now
    if due_posts:
        db.commit()
    return due_posts


def delete_post(db: Session, db_post: models.Post):
    db.delete(db_post)
    db.commit()
