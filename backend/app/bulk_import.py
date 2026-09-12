import csv
import io
from datetime import datetime
from sqlalchemy.orm import Session
from . import crud, models
from .models import CATEGORIES

REQUIRED_COLUMNS = {"title", "category", "excerpt", "body"}
VALID_STATUSES = {"draft", "scheduled", "published"}
SCHEDULE_FORMAT = "%Y-%m-%d %H:%M"


def _parse_scheduled_at(value: str) -> datetime:
    return datetime.strptime(value.strip(), SCHEDULE_FORMAT)


def _unique_slug(db: Session, requested_slug: str) -> str:
    slug = requested_slug
    n = 2
    while db.query(models.Post).filter(models.Post.slug == slug).first():
        slug = f"{requested_slug}-{n}"
        n += 1
    return slug


def import_posts_from_csv(db: Session, file_bytes: bytes) -> dict:
    text = file_bytes.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    if reader.fieldnames is None:
        return {
            "created_count": 0,
            "published_count": 0,
            "created": [],
            "error_count": 1,
            "errors": [{"row": 0, "title": "", "reason": "CSV appears to be empty or unreadable"}],
        }

    headers = {h.strip() for h in reader.fieldnames}
    missing = REQUIRED_COLUMNS - headers
    if missing:
        return {
            "created_count": 0,
            "published_count": 0,
            "created": [],
            "error_count": 1,
            "errors": [{
                "row": 0,
                "title": "",
                "reason": f"Missing required column(s): {', '.join(sorted(missing))}",
            }],
        }

    created = []
    errors = []
    published_count = 0

    for i, raw_row in enumerate(reader, start=2):
        row = {k.strip(): (v.strip() if v else "") for k, v in raw_row.items() if k}
        title = row.get("title", "")
        try:
            if not title:
                raise ValueError("Title is required")
            if not row.get("excerpt"):
                raise ValueError("Excerpt is required")
            if not row.get("body"):
                raise ValueError("Body is required")

            category = row.get("category", "")
            if category not in CATEGORIES:
                raise ValueError(f"Category must be exactly one of: {', '.join(CATEGORIES)}")

            status = row.get("status") or "draft"
            if status not in VALID_STATUSES:
                raise ValueError("Status must be draft, scheduled, or published")

            scheduled_at = None
            if status == "scheduled":
                raw_schedule = row.get("scheduled_at")
                if not raw_schedule:
                    raise ValueError("scheduled_at is required when status is 'scheduled'")
                try:
                    scheduled_at = _parse_scheduled_at(raw_schedule)
                except ValueError:
                    raise ValueError(
                        "scheduled_at must be in format YYYY-MM-DD HH:MM (e.g. 2026-03-15 09:00)"
                    )

            requested_slug = row.get("slug") or None
            slug = _unique_slug(db, requested_slug) if requested_slug else crud.make_unique_slug(db, title)

            db_post = models.Post(
                slug=slug,
                title=title,
                category=category,
                excerpt=row.get("excerpt"),
                body=row.get("body"),
                cover_image=row.get("cover_image") or None,
                hero_image_alt=row.get("hero_image_alt") or title,
                focus_position=row.get("focus_position") or "center 35%",
                dispatch_id=row.get("dispatch_id") or "ATH-26-01",
                volume=row.get("volume") or "VOL. 04 // ISSUE 08",
                board=row.get("board") or "DIRECT MALE RUNWAY",
                location=row.get("location") or "UDAIPUR / MUMBAI / GLOBAL",
                order=int(row.get("order")) if row.get("order") and row.get("order").isdigit() else 1,
                status=status,
                scheduled_at=scheduled_at,
                meta_title=row.get("meta_title") or None,
                meta_description=row.get("meta_description") or None,
                meta_keywords=row.get("meta_keywords") or None,
                og_image=row.get("og_image") or None,
                read_time_minutes=crud.calc_read_time(row.get("body")),
                published_at=datetime.utcnow() if status == "published" else None,
            )
            db.add(db_post)
            db.commit()
            db.refresh(db_post)

            if status == "published":
                published_count += 1
            created.append({"row": i, "title": title, "slug": db_post.slug, "status": status})

        except ValueError as e:
            db.rollback()
            errors.append({"row": i, "title": title or "(missing)", "reason": str(e)})
        except Exception as e:
            db.rollback()
            errors.append({"row": i, "title": title or "(missing)", "reason": f"Unexpected error: {e}"})

    return {
        "created_count": len(created),
        "published_count": published_count,
        "created": created,
        "error_count": len(errors),
        "errors": errors,
    }
