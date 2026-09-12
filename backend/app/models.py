from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from .database import Base

CATEGORIES = [
    "CRAFT & TECHNIQUE",
    "EDITORIAL DISPATCH",
    "ON LOCATION",
    "INDUSTRY INSIGHTS",
    "CAMPAIGN NOTES",
    "TRAVEL LOG",
    "STYLE COMMENTARY",
]


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    excerpt = Column(String, nullable=False)
    body = Column(Text, nullable=False)  # Markdown content

    # Media & Visual Specification
    cover_image = Column(String, nullable=True)
    hero_image_alt = Column(String, nullable=True)
    focus_position = Column(String, nullable=True, default="center 35%")

    # Editorial Metadata
    dispatch_id = Column(String, nullable=True, default="ATH-26-01")
    volume = Column(String, nullable=True, default="VOL. 04 // ISSUE 08")
    board = Column(String, nullable=True, default="DIRECT MALE RUNWAY")
    location = Column(String, nullable=True, default="UDAIPUR / MUMBAI / GLOBAL")
    order = Column(Integer, nullable=False, default=1)
    read_time_minutes = Column(Integer, nullable=False, default=5)

    # Status & Scheduling
    status = Column(String, nullable=False, default="draft")  # draft | scheduled | published
    scheduled_at = Column(DateTime, nullable=True)  # required when status == "scheduled"

    # SEO Overrides
    meta_title = Column(String, nullable=True)
    meta_description = Column(String, nullable=True)
    meta_keywords = Column(String, nullable=True)
    og_image = Column(String, nullable=True)

    # Next / Previous Link Overrides
    prev_slug = Column(String, nullable=True)
    prev_title = Column(String, nullable=True)
    next_slug = Column(String, nullable=True)
    next_title = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)

    # Resolved SEO properties — frontend consumes these directly
    @property
    def effective_meta_title(self) -> str:
        return self.meta_title or f"{self.title} — ATHARVA SHARMA"

    @property
    def effective_meta_description(self) -> str:
        return self.meta_description or self.excerpt

    @property
    def effective_og_image(self) -> str | None:
        return self.og_image or self.cover_image
