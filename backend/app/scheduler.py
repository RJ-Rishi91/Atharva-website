from apscheduler.schedulers.background import BackgroundScheduler
from . import crud
from .database import SessionLocal
from .webhook import trigger_github_rebuild

CHECK_INTERVAL_MINUTES = 5


def check_and_publish_scheduled() -> None:
    db = SessionLocal()
    try:
        published = crud.publish_due_scheduled_posts(db)
        if published:
            trigger_github_rebuild("scheduled_post_published")
    finally:
        db.close()


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_and_publish_scheduled,
        "interval",
        minutes=CHECK_INTERVAL_MINUTES,
    )
    scheduler.start()
    return scheduler
