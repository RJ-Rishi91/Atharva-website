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
]

def build():
    print("=" * 60)
    print("Building Atharva Sharma Portfolio Static Website...")
    print("=" * 60)
    
    generated_files = []
    
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
        print(f"✓ Generated {page['output']:<16} ({file_size:>6} bytes) [{page['page_title']}]")
        generated_files.append(output_path)
        
    print("-" * 60)
    print("Running Automated Integrity Validations...")
    
    # 1. Verify Zero googleusercontent.com references
    errors = 0
    for file_path in generated_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "googleusercontent.com" in content:
                print(f"❌ ERROR: googleusercontent.com found in {os.path.basename(file_path)}")
                errors += 1
                
            # Check for image paths
            img_matches = re.findall(r'src=["\'](assets/images/[^"\']+)["\']', content)
            for img in img_matches:
                full_img_path = os.path.join(ROOT_DIR, img)
                if not os.path.exists(full_img_path):
                    print(f"❌ ERROR: Missing image reference in {os.path.basename(file_path)}: {img}")
                    errors += 1
                    
    if errors == 0:
        print("✓ Zero remote googleusercontent.com references.")
        print("✓ All referenced local images exist on disk.")
        print("✓ Build successful! Site is ready for GitHub Pages deployment.")
        print("=" * 60)
        return 0
    else:
        print(f"❌ Build validation failed with {errors} error(s).")
        return 1

if __name__ == "__main__":
    sys.exit(build())
