# Design Tokens

Pulled directly from the generated Stitch code so every page (and the
Antigravity rebuild) uses the same values — nothing re-guessed or
re-invented per page.

## Colors

| Token | Value | Use |
|---|---|---|
| `canvas-warm` | `#FBF9F6` | primary background |
| `canvas-alt` | `#F5F3F0` | secondary background / section alt |
| `canvas-sheet` | `#EFECE6` | card/sheet background |
| `editorial-red` | `#D72626` | accent — headlines, CTAs, highlights |
| `editorial-red-deep` | `#B20011` | accent hover/active state |
| `editorial-ink` | `#0D0D0D` | primary text / dark surfaces |
| `editorial-gray` | `#656464` | secondary/muted text |
| `grid-border` | `rgba(13,13,13,0.16)` | hairline borders/dividers |

Base palette stays black / white / off-white with `editorial-red` as the
single accent — no other colors introduced anywhere on the site.

## Typography

| Token | Stack | Use |
|---|---|---|
| `font-display` | Anton, Impact, sans-serif | oversized headlines (hero name, section titles) |
| `font-mono` | "Space Mono", monospace | labels, meta text, nav, captions |
| `font-sans` | Inter, sans-serif | body copy |

**Hero type scale** (`.hero-type-bleed`):
```css
font-size: clamp(3.8rem, 12vw, 12.5rem);
line-height: 0.85;
letter-spacing: -0.025em;
```
Fluid by design — must bleed past the container edge on all breakpoints,
not just shrink to fit.

## Motion

| Name | Behavior | Timing |
|---|---|---|
| `heroFadeUp` | opacity 0→1, translateY 24px→0 | 0.9s, `cubic-bezier(0.16,1,0.3,1)` |
| `heroScaleIn` | opacity 0→1, scale 1.03→1 | 1.2s, same easing, 0.2s delay |
| ticker scroll | continuous horizontal loop | 28s linear infinite, pauses on hover |

Hero load sequence: text layers (`anim-fade-up`) first, image layer
(`anim-hero-frame`) settles in after a slight delay — layers animate
independently, never as one baked unit.

`prefers-reduced-motion: reduce` must disable all of the above and show
final states immediately — this is already implemented, keep it.

## Image interaction (applies to every photo, everywhere)

```css
.curated-photo {
  filter: grayscale(100%) contrast(108%);
  transition: filter 0.6s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.group:hover .curated-photo,
.group.is-active .curated-photo {
  filter: grayscale(0%) contrast(102%);
  transform: scale(1.025);
}
```
Grayscale/duotone by default, full color + slight scale on hover
(desktop) or tap (mobile). No exceptions — including any newly added
homepage sections.

## Texture

Subtle grain overlay on hero/image treatments:
```css
.bg-grain {
  background-image: radial-gradient(rgba(13,13,13,0.075) 1px, transparent 0);
  background-size: 3px 3px;
}
```

## Layout

- Full-bleed photography, generous whitespace
- No rounded "template" cards, no gradients beyond the grayscale→color
  interaction itself
- Mobile-first, fast-loading
- Max content width: `1780px` (from the generated header/hero containers)
