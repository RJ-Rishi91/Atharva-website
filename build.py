#!/usr/bin/env python3
"""
Lightweight Static Site Generator for Atharva Sharma Modeling Portfolio.
Strictly adheres to:
- README.md
- SITEMAP.md
- DESIGN-TOKENS.md
- CONTENT-GUIDELINES.md
- design.md
"""

import os
import re
import sys
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, "src", "templates")
PAGES_DIR = os.path.join(ROOT_DIR, "src", "pages")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets", "images")

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
        "page_title": "ATHARVA SHARMA — Modeling Portfolio & Editorial Book",
    },
    {
        "template": "digitals.html",
        "output": "digitals.html",
        "active_page": "digitals",
        "page_title": "DIGITALS.RAW — Atharva Sharma",
    },
    {
        "template": "portfolio.html",
        "output": "portfolio.html",
        "active_page": "portfolio",
        "page_title": "PORTFOLIO ARCHIVE — Atharva Sharma",
    },
    {
        "template": "stats.html",
        "output": "stats.html",
        "active_page": "stats",
        "page_title": "TECHNICAL METRICS & STATS — Atharva Sharma",
    },
    {
        "template": "about.html",
        "output": "about.html",
        "active_page": "about",
        "page_title": "ABOUT // BIOGRAPHY — Atharva Sharma",
    },
    {
        "template": "journal.html",
        "output": "journal.html",
        "active_page": "journal",
        "page_title": "EDITORIAL JOURNAL & DISPATCHES — Atharva Sharma",
    },
    {
        "template": "contact.html",
        "output": "contact.html",
        "active_page": "contact",
        "page_title": "CONNECT & DIRECT BOOKINGS — Atharva Sharma",
    },
    # 7 Editorial Journal Article Detail Pages
    {
        "template": "journal-runway-poise.html",
        "output": "journal-runway-poise.html",
        "active_page": "journal",
        "page_title": "DISPATCH 01: The Anatomy of Runway Poise — Atharva Sharma",
    },
    {
        "template": "journal-heritage-couture.html",
        "output": "journal-heritage-couture.html",
        "active_page": "journal",
        "page_title": "DISPATCH 02: Between Heritage & Haute Couture — Atharva Sharma",
    },
    {
        "template": "journal-thar-monoliths.html",
        "output": "journal-thar-monoliths.html",
        "active_page": "journal",
        "page_title": "DISPATCH 03: The Thar Monoliths — Atharva Sharma",
    },
    {
        "template": "journal-untouched-digital.html",
        "output": "journal-untouched-digital.html",
        "active_page": "journal",
        "page_title": "DISPATCH 04: The Untouched Digital — Atharva Sharma",
    },
    {
        "template": "journal-equine-motion.html",
        "output": "journal-equine-motion.html",
        "active_page": "journal",
        "page_title": "DISPATCH 05: Equine Motion & Coastal Textures — Atharva Sharma",
    },
    {
        "template": "journal-architecture-dialogue.html",
        "output": "journal-architecture-dialogue.html",
        "active_page": "journal",
        "page_title": "DISPATCH 06: Architecture as Dialogue — Atharva Sharma",
    },
    {
        "template": "journal-unstructured-blazer.html",
        "output": "journal-unstructured-blazer.html",
        "active_page": "journal",
        "page_title": "DISPATCH 07: The Return of the Unstructured Blazer — Atharva Sharma",
    },
    # Essential Tools & Fallback Pages
    {
        "template": "comp-card.html",
        "output": "comp-card.html",
        "active_page": "comp-card",
        "page_title": "MODEL COMPOSITE CARD // ATHARVA SHARMA — Official Casting Book",
    },
    {
        "template": "404.html",
        "output": "404.html",
        "active_page": "404",
        "page_title": "404 // DISPATCH NOT FOUND — Atharva Sharma",
    },
]

def build():
    print("=" * 60)
    print("Building Atharva Sharma Portfolio Static Website...")
    print(f"Total Pages to compile: {len(PAGES)}")
    print("=" * 60)
    
    generated_files = []
    output_basenames = set(page["output"] for page in PAGES)
    
    for page in PAGES:
        tmpl = env.get_template(page["template"])
        rendered = tmpl.render(
            active_page=page["active_page"],
            page_title=page["page_title"]
        )
        
        output_path = os.path.join(ROOT_DIR, page["output"])
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
            
        file_size = os.path.getsize(output_path)
        print(f"✓ Generated {page['output']:<36} ({file_size:>6} bytes)")
        generated_files.append(output_path)
        
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
