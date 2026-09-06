---
name: Editorial Brutalism
colors:
  surface: '#fbf9f6'
  surface-dim: '#dbdad7'
  surface-bright: '#fbf9f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f0'
  surface-container: '#efeeeb'
  surface-container-high: '#eae8e5'
  surface-container-highest: '#e4e2df'
  on-surface: '#1b1c1a'
  on-surface-variant: '#5c403c'
  inverse-surface: '#30312f'
  inverse-on-surface: '#f2f0ed'
  outline: '#916f6b'
  outline-variant: '#e5bdb9'
  surface-tint: '#be0d17'
  primary: '#b20011'
  on-primary: '#ffffff'
  primary-container: '#d72626'
  on-primary-container: '#fff1ef'
  inverse-primary: '#ffb4ab'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e5e2e1'
  on-secondary-container: '#656464'
  tertiary: '#005c8b'
  on-tertiary: '#ffffff'
  tertiary-container: '#0076b0'
  on-tertiary-container: '#eef5ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad6'
  primary-fixed-dim: '#ffb4ab'
  on-primary-fixed: '#410002'
  on-primary-fixed-variant: '#93000c'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c9c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474646'
  tertiary-fixed: '#cbe6ff'
  tertiary-fixed-dim: '#90cdff'
  on-tertiary-fixed: '#001e31'
  on-tertiary-fixed-variant: '#004b72'
  background: '#fbf9f6'
  on-background: '#1b1c1a'
  surface-variant: '#e4e2df'
  editorial-red-deep: '#C92A2A'
  pure-black: '#0D0D0D'
  pure-white: '#FFFFFF'
  warm-canvas: '#F7F5F2'
  grid-line: '#E5E1DA'
typography:
  display-hero:
    fontFamily: Anton
    fontSize: 112px
    fontWeight: '400'
    lineHeight: 96px
    letterSpacing: -0.03em
  display-hero-mobile:
    fontFamily: Anton
    fontSize: 56px
    fontWeight: '400'
    lineHeight: 52px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Anton
    fontSize: 64px
    fontWeight: '400'
    lineHeight: 64px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Anton
    fontSize: 36px
    fontWeight: '400'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Anton
    fontSize: 36px
    fontWeight: '400'
    lineHeight: 40px
    letterSpacing: 0em
  title-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  label-code:
    fontFamily: Space Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.15em
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.2em
spacing:
  unit-2xs: 0.25rem
  unit-xs: 0.5rem
  unit-sm: 0.75rem
  unit-md: 1rem
  unit-lg: 1.5rem
  unit-xl: 2.5rem
  unit-2xl: 4rem
  unit-3xl: 6rem
  unit-4xl: 10rem
  gutter-desktop: 2rem
  gutter-mobile: 1rem
  margin-desktop: 3rem
  margin-mobile: 1.25rem
---

# Atharva Sharma — Modeling Portfolio Website Design System

## Visual Identity & Color Palette
- Background: #F7F5F2 (editorial warm off-white / newsprint tone), Pure Dark #0D0D0D, Clean White #FFFFFF
- Primary Accent: #D72626 / #C92A2A (striking editorial crimson red, matching the bold reference poster)
- Typography & Hierarchy:
  - Display / Hero Headline: Ultra-condensed bold sans-serif (e.g. Impact, Anton, Bebas Neue, Oswald / condensed grotesque), all-caps, tight tracking, massive fluid clamp() sizing.
  - Micro-labels / Monospace details: Clean geometric sans / tracking-widest monospace for editorial coordinates, stats, captions, and micro-labels ("UDAIPUR", "EST. 2026", "MAIN BOOK", "PORTFOLIO N0.01").
  - Body Copy: Clean minimal neutral sans-serif (Inter / Helvetica Neue).

## Photographic Treatment
- Base state: Grayscale / subtle duotone high-contrast editorial treatment.
- Interactive state: Smooth CSS transition on hover / tap to vibrant full natural color with subtle scale transform.
- Layout: Asymmetrical, fluid masonry grid, mixed aspect ratios, generous negative space, no rounded card borders. Live coded typography overlapping imagery with CSS layering and keyframe entrance animations.
