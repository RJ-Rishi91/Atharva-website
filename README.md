# Atharva Sharma — Modeling Portfolio Site

A single-purpose visual portfolio site for casting directors and agencies.
Not a personal blog or marketing hub — a comp-card/book, built to be
scanned fast and taken seriously.

## Stack

- Plain static HTML/CSS/vanilla JS (Tailwind via CDN for utility classes)
- No JS framework — kept deliberately simple and lightweight
- Shared header/footer via a lightweight build-time include (not manually
  duplicated per page)
- Deploy target: GitHub Pages, custom domain in Atharva's name

## Folder structure

```
atharva-portfolio/
├── README.md
├── SITEMAP.md
├── DESIGN-TOKENS.md
├── CONTENT-GUIDELINES.md
├── design.md                 ← full page-by-page build spec (source of truth)
├── stitch-export/            ← raw Stitch-generated page exports (reference only)
├── assets/
│   └── images/                ← real photos, referenced by filename in design.md
└── (built site output — index.html, digitals.html, portfolio.html,
     stats.html, about.html, contact.html, etc.)
```

## Related docs

- **design.md** — the authoritative build spec: page-by-page content,
  exact image filenames, hero/about treatment, and the no-fabrication rule.
  If anything here conflicts with it, design.md wins.
- **SITEMAP.md** — page list, routes, and what's on each page.
- **DESIGN-TOKENS.md** — colors, type, spacing, motion/interaction values
  actually used in the generated code, pulled from the Stitch export so
  nothing drifts across pages.
- **CONTENT-GUIDELINES.md** — what can and can't appear as copy on the
  site: real contact info, the placeholder policy, and the rule against
  inventing biographical/physical/contact details.

## Current status

- Design phase (Google Stitch) complete: hero, digitals, portfolio,
  stats, about, and contact pages generated and reviewed.
- Known fix applied: Stitch-invented fabricated stats/bio/contact data
  removed and replaced with real info or explicit `TBD` placeholders —
  see CONTENT-GUIDELINES.md.
- Known fix applied: hero rebuilt as live coded layers (real image +
  real text elements), not a flattened graphic.
- Next: implementation pass (Google Antigravity) — consolidate the
  per-page Stitch exports into one linked static site, replace all
  `lh3.googleusercontent.com` placeholder image URLs with the real local
  files in `assets/images/`, wire up shared header/footer, prep for
  GitHub Pages.
- Outstanding: Digitals page has no real shots yet (raw/unretouched,
  blank wall, natural light) — currently shows a "coming soon" state by
  design. Ethnic/Traditional portfolio category has only one image —
  worth shooting more before launch.
