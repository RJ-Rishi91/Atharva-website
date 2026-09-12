import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Add current directory to sys.path
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

from app.database import SessionLocal, engine, Base
from app import models, crud

Base.metadata.create_all(bind=engine)


def parse_markdown_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content

    fm_text, body = match.groups()
    metadata = {}
    for line in fm_text.splitlines():
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            metadata[key] = val

    return metadata, body.strip()


def parse_date(date_str: str | None) -> datetime:
    if not date_str:
        return datetime.utcnow()
    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return datetime.utcnow()


def seed_posts():
    db = SessionLocal()
    # If the database already contains posts, skip seeding so user modifications stay intact
    if db.query(models.Post).count() > 0:
        print("Database already contains posts. Skipping auto-seed.")
        db.close()
        return

    journal_dir = current_dir.parent / "src" / "content" / "journal"
    if not journal_dir.exists():
        print(f"No journal directory found at {journal_dir}")
        db.close()
        return

    md_files = sorted(list(journal_dir.glob("*.md")))
    print(f"Found {len(md_files)} markdown files in {journal_dir}")

    seeded_count = 0
    for file_path in md_files:
        slug = file_path.stem
        metadata, body = parse_markdown_file(file_path)
        if not metadata:
            print(f"Skipping {file_path.name} (no frontmatter)")
            continue

        existing = db.query(models.Post).filter(models.Post.slug == slug).first()
        if existing:
            print(f"Post already exists: {slug}")
            continue

        title = metadata.get("title", slug.replace("-", " ").title())
        category = metadata.get("category", "CRAFT & TECHNIQUE")
        excerpt = metadata.get("description", "")
        cover_image = metadata.get("heroImage")
        hero_image_alt = metadata.get("heroImageAlt", title)
        focus_position = metadata.get("focusPosition", "center 35%")
        dispatch_id = metadata.get("dispatchId", "ATH-25-01")
        volume = metadata.get("volume", "VOL. 04 // ISSUE 08")
        board = metadata.get("board", "DIRECT MALE RUNWAY")
        location = metadata.get("location", "UDAIPUR / MUMBAI / GLOBAL")
        order_val = int(metadata.get("order")) if metadata.get("order") and metadata.get("order").isdigit() else 1
        prev_slug = metadata.get("prevSlug")
        prev_title = metadata.get("prevTitle")
        next_slug = metadata.get("nextSlug")
        next_title = metadata.get("nextTitle")
        published_at = parse_date(metadata.get("date"))

        post = models.Post(
            slug=slug,
            title=title,
            category=category,
            excerpt=excerpt,
            body=body,
            cover_image=cover_image,
            hero_image_alt=hero_image_alt,
            focus_position=focus_position,
            dispatch_id=dispatch_id,
            volume=volume,
            board=board,
            location=location,
            order=order_val,
            status="published",
            prev_slug=prev_slug,
            prev_title=prev_title,
            next_slug=next_slug,
            next_title=next_title,
            read_time_minutes=crud.calc_read_time(body),
            published_at=published_at,
        )
        db.add(post)
        seeded_count += 1
        print(f"Seeded: {slug} ({category})")

    db.commit()
    db.close()
    print(f"Successfully seeded {seeded_count} posts into the database.")


if __name__ == "__main__":
    seed_posts()
