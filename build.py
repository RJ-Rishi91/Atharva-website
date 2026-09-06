#!/usr/bin/env python3
"""
Lightweight Static Site Generator for Atharva Sharma Modeling Portfolio.
Strictly adheres to:
- README.md
- SITEMAP.md
- DESIGN-TOKENS.md
- CONTENT-GUIDELINES.md
- design.md

Features:
- Complete multi-page Jinja2 compilation
- Full SEO metadata injection (Meta, OG, Twitter, Schema JSON-LD, Geo/Local)
- Automated sitemap.xml generation
- Automated robots.txt generation
- Automated post-build integrity validations
"""

import os
import re
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, "src", "templates")
PAGES_DIR = os.path.join(ROOT_DIR, "src", "pages")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets", "images")

BASE_URL = "https://rj-rishi91.github.io/Atharva-website"

# Setup Jinja2 loader for both templates and pages
env = Environment(
    loader=FileSystemLoader([PAGES_DIR, TEMPLATES_DIR]),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

PAGES = [
    # 7 Primary Canonical Sections
    {
        "template": "home.html",
        "output": "index.html",
        "active_page": "home",
        "page_title": "ATHARVA SHARMA — Male Fashion & Editorial Runway Model Portfolio",
        "meta_description": "Official portfolio of Atharva Sharma, Indian male editorial and runway fashion model based in Udaipur, India. 6'1\" (186cm), high luxury couture, runway poise, and commercial campaign bookings.",
        "meta_keywords": "Atharva Sharma, male model India, Indian runway model, fashion model Udaipur, high fashion editorial, menswear model, male modeling portfolio, 6'1 model, Indian fashion model, couture model",
        "og_image": "assets/images/atharva-studio-bw-stool.png",
        "page_type": "profile",
        "priority": "1.0",
        "changefreq": "weekly",
    },
    {
        "template": "digitals.html",
        "output": "digitals.html",
        "active_page": "digitals",
        "page_title": "DIGITALS.RAW — Atharva Sharma // Casting Polaroids & Clean Specs",
        "meta_description": "Raw, unretouched daylight polaroids and digitals for international modeling agency casting boards in Paris, Milan, New York, London, and Mumbai.",
        "meta_keywords": "model digitals, casting polaroids, Atharva Sharma digitals, unretouched model photos, male model agency polaroids, Paris casting board, Milan fashion week digitals",
        "og_image": "assets/images/atharva-studio-bw-stool.png",
        "page_type": "website",
        "priority": "0.8",
        "changefreq": "monthly",
    },
    {
        "template": "portfolio.html",
        "output": "portfolio.html",
        "active_page": "portfolio",
        "page_title": "PORTFOLIO ARCHIVE — Atharva Sharma // Commercial, Ethnic & Editorial Looks",
        "meta_description": "Comprehensive portfolio archive of Atharva Sharma categorized by look: Commercial & Casual, Ethnic & Traditional Rajasthani Couture, and High-Fashion Dramatic Editorial.",
        "meta_keywords": "Atharva Sharma portfolio, menswear looks, commercial model, traditional kurta photoshoot, high fashion editorial menswear, Rajasthani royal couture model",
        "og_image": "assets/images/atharva-kurta-palace-night.jpg",
        "page_type": "website",
        "priority": "0.9",
        "changefreq": "weekly",
    },
    {
        "template": "stats.html",
        "output": "stats.html",
        "active_page": "stats",
        "page_title": "TECHNICAL METRICS & STATS — Atharva Sharma // 6'1\" Model Specifications",
        "meta_description": "Official industry measurements for Atharva Sharma: Height 6'1\" (186cm), Chest 38\", Waist 30\", Shoes 43 EU / 9.5 UK, Hair Dark Brown, Eyes Hazel, Collar 15.5\", Suit 38R.",
        "meta_keywords": "Atharva Sharma height, model measurements, 6'1 male model specs, shoe size 43 EU, chest 38 waist 30, casting dimensions, agency spec sheet",
        "og_image": "assets/images/atharva-studio-bw-stool.png",
        "page_type": "website",
        "priority": "0.8",
        "changefreq": "monthly",
    },
    {
        "template": "about.html",
        "output": "about.html",
        "active_page": "about",
        "page_title": "ABOUT // BIOGRAPHY — Atharva Sharma // Runway & Editorial Background",
        "meta_description": "Biography and discipline statement of Atharva Sharma, bridging heritage Mewar aesthetics with contemporary international menswear and equestrian movement.",
        "meta_keywords": "Atharva Sharma bio, male model biography, Udaipur model, fashion career, editorial model story, Indian runway model",
        "og_image": "assets/images/atharva-studio-bw-stool.png",
        "page_type": "profile",
        "priority": "0.8",
        "changefreq": "monthly",
    },
    {
        "template": "journal.html",
        "output": "journal.html",
        "active_page": "journal",
        "page_title": "EDITORIAL JOURNAL & ESSAYS — Atharva Sharma // Field Dispatches",
        "meta_description": "Personal dispatches and technical essays by Atharva Sharma documenting runway mechanics, high-fashion lighting, desert expeditions, raw digitals, and tailoring.",
        "meta_keywords": "fashion journal, modeling essays, runway poise, Atharva Sharma blog, fashion dispatches, menswear commentary, haute couture reflections",
        "og_image": "assets/images/atharva-studio-bw-stool.png",
        "page_type": "website",
        "priority": "0.9",
        "changefreq": "weekly",
    },
    {
        "template": "contact.html",
        "output": "contact.html",
        "active_page": "contact",
        "page_title": "CONNECT & DIRECT BOOKINGS — Atharva Sharma // Casting Inquiries",
        "meta_description": "Direct booking inquiries, lookbook commissions, runway requests, and agency contact for Atharva Sharma. Email: atharva@atharvasharma.co.in | WhatsApp: +91 8209225998.",
        "meta_keywords": "book Atharva Sharma, hire male model, casting agency contact, fashion model bookings, commercial shoot inquiries, Udaipur Delhi Mumbai model",
        "og_image": "assets/images/atharva-studio-bw-stool.png",
        "page_type": "website",
        "priority": "0.8",
        "changefreq": "monthly",
    },
    # 7 Editorial Journal Article Detail Pages
    {
        "template": "journal-runway-poise.html",
        "output": "journal-runway-poise.html",
        "active_page": "journal",
        "page_title": "The Anatomy of Runway Poise — Atharva Sharma // Dispatch #01",
        "meta_description": "Technical analysis on runway mechanics, pelvic stability, and transferring equestrian kinetic alignment into contemporary minimalist menswear walks.",
        "meta_keywords": "runway poise, runway walk mechanics, male model runway technique, physical discipline in menswear, Atharva Sharma dispatch",
        "og_image": "assets/images/atharva-studio-bw-stool.png",
        "page_type": "article",
        "category": "Craft & Technique",
        "date_published": "2025-10-15",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    {
        "template": "journal-heritage-couture.html",
        "output": "journal-heritage-couture.html",
        "active_page": "journal",
        "page_title": "Between Heritage & Haute Couture — Atharva Sharma // Dispatch #02",
        "meta_description": "Draping royal Mewar silhouettes and embroidered black velvet kurtas for the global camera lens under nocturnal palace lighting in Udaipur.",
        "meta_keywords": "heritage couture, royal Mewar silhouettes, traditional Indian menswear, velvet kurta photoshoot, Udaipur City Palace editorial",
        "og_image": "assets/images/atharva-kurta-palace-night.jpg",
        "page_type": "article",
        "category": "Editorial Dispatch",
        "date_published": "2025-08-20",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    {
        "template": "journal-thar-monoliths.html",
        "output": "journal-thar-monoliths.html",
        "active_page": "journal",
        "page_title": "The Thar Monoliths: Desert Expedition — Atharva Sharma // Dispatch #03",
        "meta_description": "Staging high fashion and tactical outerwear against harsh midday glare, sand resistance, and rugged vehicle expedition in India's Thar desert.",
        "meta_keywords": "Thar desert photoshoot, expedition menswear, high fashion desert lighting, rugged tactical outerwear model, Atharva Sharma Thar",
        "og_image": "assets/images/atharva-desert-jeep-bw.jpg",
        "page_type": "article",
        "category": "On Location",
        "date_published": "2025-06-10",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    {
        "template": "journal-untouched-digital.html",
        "output": "journal-untouched-digital.html",
        "active_page": "journal",
        "page_title": "The Untouched Digital: Pure Daylight Polaroids — Atharva Sharma // Dispatch #04",
        "meta_description": "Why international casting directors in Paris and Milan demand unretouched, zero-distortion daylight snapshots without makeup or artificial lighting.",
        "meta_keywords": "untouched digitals, casting polaroids honesty, Paris Milan model casting, raw model polaroids, daylight casting photos",
        "og_image": "assets/images/atharva-cafe-beanie.jpg",
        "page_type": "article",
        "category": "Industry Insights",
        "date_published": "2025-05-18",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    {
        "template": "journal-equine-motion.html",
        "output": "journal-equine-motion.html",
        "active_page": "journal",
        "page_title": "Equine Motion & Coastal Textures — Atharva Sharma // Dispatch #05",
        "meta_description": "Exploring fluidity and windblown linen in resort menswear while harmonizing posture alongside unscripted animal movement along coastal tides.",
        "meta_keywords": "equine fashion photoshoot, coastal resort menswear, horse beach modeling, white linen menswear, animal movement fashion",
        "og_image": "assets/images/atharva-horse-beach.jpg",
        "page_type": "article",
        "category": "Campaign Notes",
        "date_published": "2025-03-24",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    {
        "template": "journal-architecture-dialogue.html",
        "output": "journal-architecture-dialogue.html",
        "active_page": "journal",
        "page_title": "Architecture as Dialogue in Central Europe — Atharva Sharma // Dispatch #06",
        "meta_description": "Nocturnal tailoring campaigns against brutalist concrete and neo-classical facades across Budapest, treating the wool scarf as a kinetic styling tool.",
        "meta_keywords": "architectural fashion photography, Budapest night photoshoot, European tailoring menswear, wool scarf kinetic styling, urban noir model",
        "og_image": "assets/images/atharva-citynight-scarf.jpg",
        "page_type": "article",
        "category": "Travel Log",
        "date_published": "2025-01-28",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    {
        "template": "journal-unstructured-blazer.html",
        "output": "journal-unstructured-blazer.html",
        "active_page": "journal",
        "page_title": "The Return of the Unstructured Blazer — Atharva Sharma // Dispatch #07",
        "meta_description": "Deconstructed Italian and Japanese tailoring: how physical posture and candid studio energy compensate when lapels fall naturally without stiff canvassing.",
        "meta_keywords": "unstructured blazer, deconstructed tailoring, candid studio photography, relaxed menswear, Italian tailoring nuances",
        "og_image": "assets/images/atharva-bedroom-blazer.jpg",
        "page_type": "article",
        "category": "Style Commentary",
        "date_published": "2024-11-12",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    # Essential Tools & Fallback Pages
    {
        "template": "comp-card.html",
        "output": "comp-card.html",
        "active_page": "comp-card",
        "page_title": "MODEL COMPOSITE CARD // ATHARVA SHARMA — Official Casting Zed Card",
        "meta_description": "Official printable and digital Comp-Card / Zed Card for Atharva Sharma. Standard A5 layout with key specimen portraits, full measurements, and casting contact.",
        "meta_keywords": "Atharva Sharma comp card, model zed card, printable composite card, male model comp card PDF, 6'1 casting card",
        "og_image": "assets/images/atharva-studio-bw-stool.png",
        "page_type": "website",
        "priority": "0.9",
        "changefreq": "monthly",
    },
    {
        "template": "404.html",
        "output": "404.html",
        "active_page": "404",
        "page_title": "404 // DISPATCH NOT FOUND — Atharva Sharma",
        "meta_description": "The requested editorial specimen or dispatch could not be located in the archive. Return to Atharva Sharma's modeling portfolio directory.",
        "meta_keywords": "404, not found, Atharva Sharma",
        "og_image": "assets/images/atharva-studio-bw-stool.png",
        "page_type": "website",
        "priority": "0.1",
        "changefreq": "yearly",
    },
]

def generate_sitemap():
    """Generates standard sitemap.xml for all pages."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    lines.append('        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')
    
    for page in PAGES:
        canonical = f"{BASE_URL}/{page['output']}"
        img_url = f"{BASE_URL}/{page.get('og_image', 'assets/images/atharva-studio-bw-stool.png')}"
        title = page.get("page_title", "Atharva Sharma")
        
        lines.append("  <url>")
        lines.append(f"    <loc>{canonical}</loc>")
        lines.append(f"    <lastmod>{page.get('date_published', today)}</lastmod>")
        lines.append(f"    <changefreq>{page.get('changefreq', 'monthly')}</changefreq>")
        lines.append(f"    <priority>{page.get('priority', '0.7')}</priority>")
        lines.append("    <image:image>")
        lines.append(f"      <image:loc>{img_url}</image:loc>")
        lines.append(f"      <image:title>{title}</image:title>")
        lines.append("    </image:image>")
        lines.append("  </url>")
        
    lines.append("</urlset>")
    sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("✓ Generated sitemap.xml")

def generate_robots():
    """Generates standard robots.txt."""
    content = f"""# Robots Exclusion Standard for Atharva Sharma Modeling Portfolio
User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    robots_path = os.path.join(ROOT_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Generated robots.txt")

def build():
    print("=" * 60)
    print("Building Atharva Sharma Portfolio Static Website...")
    print(f"Total Pages to compile: {len(PAGES)}")
    print("=" * 60)
    
    generated_files = []
    output_basenames = set(page["output"] for page in PAGES)
    
    for page in PAGES:
        tmpl = env.get_template(page["template"])
        canonical_url = f"{BASE_URL}/{page['output']}"
        
        rendered = tmpl.render(
            active_page=page["active_page"],
            page_title=page["page_title"],
            meta_description=page.get("meta_description", ""),
            meta_keywords=page.get("meta_keywords", ""),
            canonical_url=canonical_url,
            og_image=page.get("og_image", "assets/images/atharva-studio-bw-stool.png"),
            page_type=page.get("page_type", "website"),
            category=page.get("category", ""),
            date_published=page.get("date_published", ""),
            base_url=BASE_URL,
            output_filename=page["output"],
        )
        
        output_path = os.path.join(ROOT_DIR, page["output"])
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
            
        file_size = os.path.getsize(output_path)
        print(f"✓ Generated {page['output']:<36} ({file_size:>6} bytes)")
        generated_files.append(output_path)
        
    generate_sitemap()
    generate_robots()
        
    print("-" * 60)
    print("Running Automated Integrity Validations...")
    
    errors = 0
    for file_path in generated_files:
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 1. Verify Zero googleusercontent.com references
        if "googleusercontent.com" in content:
            print(f"❌ ERROR: googleusercontent.com found in {filename}")
            errors += 1
            
        # 2. Check for image paths
        img_matches = re.findall(r'src=["\'](assets/images/[^"\']+)["\']', content)
        for img in img_matches:
            full_img_path = os.path.join(ROOT_DIR, img)
            if not os.path.exists(full_img_path):
                print(f"❌ ERROR: Missing image reference in {filename}: {img}")
                errors += 1

        # 3. Check for internal html links
        soup = BeautifulSoup(content, "html.parser")
        for a in soup.find_all("a"):
            href = a.get("href", "")
            if href.endswith(".html") or ".html#" in href:
                target_html = href.split("#")[0]
                if target_html not in output_basenames:
                    print(f"❌ ERROR: Broken internal link in {filename} -> {href}")
                    errors += 1
                    
    if errors == 0:
        print("✓ Zero remote googleusercontent.com references.")
        print("✓ All referenced local images exist on disk.")
        print("✓ All internal .html navigation links resolve to valid pages.")
        print("✓ Build successful! All 16 pages are ready for GitHub Pages deployment.")
        print("=" * 60)
        return 0
    else:
        print(f"❌ Build validation failed with {errors} error(s).")
        return 1

if __name__ == "__main__":
    sys.exit(build())
