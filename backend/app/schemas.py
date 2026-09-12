from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str
    category: str
    excerpt: str
    body: str
    cover_image: Optional[str] = None
    hero_image_alt: Optional[str] = None
    focus_position: Optional[str] = "center 35%"

    dispatch_id: Optional[str] = "ATH-26-01"
    volume: Optional[str] = "VOL. 04 // ISSUE 08"
    board: Optional[str] = "DIRECT MALE RUNWAY"
    location: Optional[str] = "UDAIPUR / MUMBAI / GLOBAL"
    order: Optional[int] = 1

    status: str = Field(default="draft", pattern="^(draft|scheduled|published)$")
    scheduled_at: Optional[datetime] = None  # required when status == "scheduled"

    # SEO Overrides
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    og_image: Optional[str] = None

    # Next / Prev Navigation
    prev_slug: Optional[str] = None
    prev_title: Optional[str] = None
    next_slug: Optional[str] = None
    next_title: Optional[str] = None


class PostCreate(PostBase):
    slug: Optional[str] = None  # Auto-generated from title if omitted


class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    category: Optional[str] = None
    excerpt: Optional[str] = None
    body: Optional[str] = None
    cover_image: Optional[str] = None
    hero_image_alt: Optional[str] = None
    focus_position: Optional[str] = None

    dispatch_id: Optional[str] = None
    volume: Optional[str] = None
    board: Optional[str] = None
    location: Optional[str] = None
    order: Optional[int] = None

    status: Optional[str] = Field(default=None, pattern="^(draft|scheduled|published)$")
    scheduled_at: Optional[datetime] = None

    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    og_image: Optional[str] = None

    prev_slug: Optional[str] = None
    prev_title: Optional[str] = None
    next_slug: Optional[str] = None
    next_title: Optional[str] = None


class PostOut(PostBase):
    id: int
    slug: str
    read_time_minutes: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    effective_meta_title: str
    effective_meta_description: str
    effective_og_image: Optional[str] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
