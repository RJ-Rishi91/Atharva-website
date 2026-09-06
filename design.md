# Atharva Sharma — Modeling Portfolio Website
## Design Brief for Google Stitch

---

## ⚠️ CRITICAL RULES — DO NOT VIOLATE

1. **Use ONLY the images listed below by exact filename.** Every image referenced
   in this document comes from one of two uploaded folders:
   - `atharva-images/` — real photos of Atharva, to be used ON the live site
   - `reference-images/` — STYLE REFERENCES ONLY. These
     (`ref-poster-style.jpg`, `ref-about-style.jpg`, and `ref-hero-composition.jpg`)
     tell you the visual
     treatment to apply. Do NOT place any of these three images on the
     live site themselves — rebuild their look using real HTML/CSS
     elements and Atharva's own real photos instead.

2. **Never generate, substitute, or insert AI-generated, synthetic, or stock
   photos of a person anywhere on the site.** Not as placeholders, not to
   "fill" a section that has fewer images than expected. If a section has
   fewer real images than a typical layout wants, leave it visually sparse
   with a "coming soon" note rather than inventing imagery.

3. **Technical note:** the original files had spaces, `+` signs, and inconsistent capitalization
   (`.PNG` vs `.jpeg`), and two HEIC duplicates of the same lake/backpack
   shot. All filenames have been cleaned to simple hyphenated names
   (converted to JPG where needed) — use ONLY the clean names below, and
   ignore any old filenames if you see them referenced elsewhere.

---

## GLOBAL DESIGN LANGUAGE

- **Palette:** black / white / off-white base, single red accent color
  (match the red used in `ref-poster-style.jpg`)
- **Default image treatment:** grayscale / duotone (black-white-red)
- **Interaction rule:** on hover (desktop) or tap (mobile), the interacted
  image transitions smoothly from grayscale to full color
- **Typography:** oversized, bold, condensed sans-serif for headlines/name
  (match the type scale and weight of "ARJUN RAMPAL" in `ref-poster-style.jpg`);
  clean minimal sans-serif for body copy
- **Layout:** full-bleed photography, generous whitespace, mobile-first,
  fast-loading. No rounded template-style cards, no stock design flourishes,
  no gradients beyond the grayscale-to-color interaction itself.

---

## PAGE 1 — HOME

### Hero section (top of page)

**Build this as live coded layers (real HTML/CSS/DOM elements), NOT as one
flattened image with text baked in.** The image and the typography must
remain separate, independently styleable, independently animatable
elements, so the layout can reflow across breakpoints and orientations
and each element can have its own animation timing.

- **Style references (for visual composition only — do not use these files
  directly on the site):**
  - `reference-images/ref-poster-style.jpg` — oversized bleeding
    typography, scattered micro-text labels, red accent block
  - `reference-images/ref-hero-composition.jpg` — exact target
    look for color, type scale, spacing, and grain treatment, built as a
    reference comp. Replicate this composition with live code, using the
    real image + real text elements below — do not use this file as the
    hero graphic itself.
- **Hero image (real photo, used as-is, not edited/flattened):**
  `atharva-images/atharva-studio-bw-stool.png` — displayed as an actual `<img>` /
  background-image element, `object-fit: cover`, positioned so the subject
  stays framed correctly across breakpoints and orientations.
- **Text layer (separate DOM elements, layered over/around the image):**
  - Name "ATHARVA" / "SHARMA" — oversized bold condensed sans-serif, red
    accent, sized with `clamp()`/viewport units so it scales fluidly and
    can bleed past the container edges on any screen size, portrait or
    landscape
  - Small red accent block (top-right corner)
  - Scattered micro-text labels (e.g. "UDAIPUR", "MODEL", "AVAILABLE
    2026", "PORTFOLIO N0.01") — real text elements positioned via
    CSS grid/flex, not part of the image
  - Thin horizontal rule line + caption row ("MAIN BOOK" / "EST. 2026")
- **Responsive behavior:** on narrow/portrait viewports the name stacks
  and scales down proportionally; on wide/landscape viewports the layout
  may shift proportionally (e.g. text beside image rather than only above
  it) — every element must reflow gracefully, not just shrink uniformly.
- **Animation on load (~1-2 sec), each layer independent:** text layer
  slides/fades in first → micro-labels fade in with a slight stagger →
  image layer scales/fades in last. Implement with CSS transitions/
  keyframes (or a lightweight animation library) so timing/easing per
  element can be adjusted independently later.

### Curated grid (below hero)
Dynamic masonry grid, mixed aspect ratios (not uniform squares), grayscale-
to-color on hover. Use in this order:

(Note: `atharva-studio-bw-stool.png` is used in the hero above — do not
repeat it immediately below; it can still appear later on the Portfolio page.)

1. `atharva-images/atharva-horse-beach.jpg` — white outfit, white horse, beach
2. `atharva-images/atharva-kurta-palace-night.jpg` — black embroidered kurta, palace,
   night
3. `atharva-images/atharva-desert-jeep-bw.jpg` — B&W, jeep, desert
4. `atharva-images/atharva-cafe-beanie.jpg` — sweater vest, beanie, cafe
5. `atharva-images/atharva-lake-backpack.jpg` — backpacker, Udaipur lake
6. `atharva-images/atharva-beach-night-linen.jpg` — white linen, night beach
7. `atharva-images/atharva-citynight-scarf.jpg` — city night, scarf
8. `atharva-images/atharva-bedroom-blazer.jpg` — bedroom, brown blazer

---

## PAGE 2 — DIGITALS
No raw/unretouched digitals have been shot yet (full body, waist-up,
profile, headshot against a blank wall, natural light, no filter).
Show a minimal **"Digitals coming soon"** placeholder. Do not fill this
page with any other image from the folder.

---

## PAGE 3 — PORTFOLIO (grouped by look)

**Commercial / Casual**
- `atharva-images/atharva-cafe-beanie.jpg`
- `atharva-images/atharva-bedroom-blazer.jpg`
- `atharva-images/atharva-citynight-scarf.jpg`
- `atharva-images/atharva-lake-backpack.jpg`
- `atharva-images/atharva-beach-night-linen.jpg`

**Ethnic / Traditional**
- `atharva-images/atharva-kurta-palace-night.jpg`
- *(Note: only one image in this category right now — worth shooting more
  before launch to make this group feel complete.)*

**Editorial / Dramatic**
- `atharva-images/atharva-studio-bw-stool.png`
- `atharva-images/atharva-horse-beach.jpg`
- `atharva-images/atharva-desert-jeep-bw.jpg`

---

## PAGE 4 — STATS
Clean spec table, no imagery. Fields only (values filled in later):
- Height
- Chest / Waist / Hips
- Shoe size
- Hair color
- Eye color

---

## PAGE 5 — ABOUT
- **Style reference:** `reference-images/ref-about-style.jpg`
  (large B&W portrait, bold name overlaid directly on image, row of small
  circular thumbnails, justified bio text block below)
- **Main portrait:** `atharva-images/atharva-studio-bw-stool.png`
- Bold name/heading overlaid directly on the portrait, in red accent
- **Thumbnail row** (small circular crops), pulled from:
  - `atharva-images/atharva-desert-jeep-bw.jpg`
  - `atharva-images/atharva-kurta-palace-night.jpg`
  - `atharva-images/atharva-horse-beach.jpg`
- Justified bio text block below the portrait (2-3 sentences — copy TBD)

---

## PAGE 6 — CONTACT
- Email, WhatsApp/phone, Instagram link
- Downloadable comp-card PDF (build later, once Digitals + Stats exist)
- Minimal imagery — reuse the hero or about portrait crop if a visual is
  needed; no new images required
