# Atharva Sharma Editorial CMS Backend

FastAPI backend and SQLite database for the Editorial Journal — provides CRUD, scheduling, media uploading, and live site webhook triggers.

## Quickstart

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

To run the local server:
```bash
uvicorn app.main:app --reload --port 8000
```

- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health
- **Public Posts API**: http://localhost:8000/api/posts

## Master Password

The default admin master password configured in `.env` is:
`Admin@Atharva2026!`

To generate a new password hash:
```bash
python3 -c "from app.auth import hash_password; print(hash_password('NewSecurePassword!'))"
```
Paste into `ADMIN_PASSWORD_HASH` in `.env`.

## Endpoints

### Public
- `GET /api/health` — API health check
- `GET /api/posts` — List all published dispatches (supports `?category=...`)
- `GET /api/posts/{slug}` — Retrieve a single published dispatch

### Auth
- `POST /api/admin/login` — Exchange password for Bearer JWT token

### Admin (Bearer Token Required)
- `GET /api/admin/posts` — List all posts (including drafts and scheduled)
- `GET /api/admin/posts/{id}` — Retrieve post by ID
- `POST /api/admin/posts` — Create a new dispatch
- `PUT /api/admin/posts/{id}` — Update an existing dispatch
- `DELETE /api/admin/posts/{id}` — Delete a dispatch
- `POST /api/admin/upload` — Multipart image upload (PNG, JPG, WebP, SVG)
- `POST /api/admin/posts/bulk-import` — Batch-import dispatches from CSV

## Continuous Deployment Rebuild Loop

When a dispatch is published, updated, or deleted:
FastAPI automatically executes a background webhook triggering the GitHub Actions `repository_dispatch` event (`cms_post_published`) on `RJ-Rishi91/Atharva-website`. GitHub Actions compiles Astro and deploys the updated static site live to `https://atharvasharma.co.in`.
