# Sitemap

6 pages, shared header + footer on every page (see DESIGN-TOKENS.md for
the nav bar spec). Nav order matches page order below.

| # | Page | File | Route |
|---|------|------|-------|
| 1 | Home | `index.html` | `/` |
| 2 | Digitals | `digitals.html` | `/digitals` |
| 3 | Portfolio | `portfolio.html` | `/portfolio` |
| 4 | Stats | `stats.html` | `/stats` |
| 5 | About | `about.html` | `/about` |
| 6 | Contact | `contact.html` | `/contact` |

---

### 1. Home (`index.html`)
- Hero: live-coded name typography + real hero photo
  (`atharva-studio-bw-stool.png`), poster-style composition
- Curated masonry grid (8 images, grayscale-default/color-on-hover)
- Category preview strip (3 tiles → link into Portfolio sections)
- About teaser (one factual line + "Read more" → About page)
- Instagram banner (static link → real Instagram handle)
- Booking CTA banner → Contact page

### 2. Digitals (`digitals.html`)
- "Coming soon" state — 4 pending shot-type placeholders (full body,
  profile 90°, waist-up, close headshot) with framing/pose notes
- No real digitals shot yet — do not fill with other images

### 3. Portfolio (`portfolio.html`)
- Grouped by look, in this order:
  1. Commercial / Casual (5 images)
  2. Ethnic / Traditional (1 image — flagged as needing more shots)
  3. Editorial / Dramatic (3 images)

### 4. Stats (`stats.html`)
- Physical spec table — fields only until real measurements are
  provided: Height, Chest/Waist/Hips, Shoe size, Hair color, Eye color
- No fabricated numbers (see CONTENT-GUIDELINES.md)

### 5. About (`about.html`)
- Main portrait (`atharva-studio-bw-stool.png`) with overlaid name
- Small thumbnail row (3 images)
- Short factual bio block — no invented career/training claims

### 6. Contact (`contact.html`)
- Real contact info only: email, phone/WhatsApp, Instagram
  (see CONTENT-GUIDELINES.md for exact values)
- Downloadable comp-card PDF (build once Digitals + Stats are real)

---

### Navigation notes
- Header nav links to all 6 pages, persistent/sticky across the site.
- Footer repeats identical contact block on all 6 pages — must pull
  from the same single source so it can't drift out of sync again.
