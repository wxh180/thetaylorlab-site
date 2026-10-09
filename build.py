#!/usr/bin/env python3
"""Build the Taylor Lab website into ./_site

    pip install jinja2 pyyaml
    python build.py            # build
    python build.py --serve    # build and preview at http://localhost:8000

Content lives in data/*.yml (people, publications, gallery, site settings)
and templates/*.html (page layouts and the Research / Home text).
"""
import os, shutil, sys, re, datetime
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site")

def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return yaml.safe_load(f)

def paragraphs(text):
    """Split a text block into paragraphs on blank lines."""
    return [p.strip() for p in re.split(r"\n\s*\n", text or "") if p.strip()]

PAGES = [  # (template, output path, page title, nav path)
    ("home.html", "index.html", None, ""),
    ("research.html", "research/index.html", "Research", "research/"),
    ("people.html", "the-lab/index.html", "People", "the-lab/"),
    ("publications.html", "publications/index.html", "Publications", "publications/"),
    ("gallery.html", "lab-events/index.html", "Gallery", "lab-events/"),
    ("contact.html", "contact-us/index.html", "Contact Us", "contact-us/"),
    ("404.html", "404.html", "Page not found", None),
]

def main():
    site = load("site.yml")
    people = load("people.yml")
    pubs = load("publications.yml")
    gallery = load("gallery.yml")

    # group publications by year, preserving file order
    years, by_year = [], {}
    for p in pubs:
        y = str(p["year"])
        if y not in by_year:
            by_year[y] = []
            years.append(y)
        by_year[y].append(p)

    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")),
                      autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
    env.filters["paragraphs"] = paragraphs
    # Highlight lab members in author lists. Each person is matched as "Lastname, F." (plus any
    # extra initials); add `pub_names: ["Other, A."]` in people.yml for maiden names or variants.
    from markupsafe import Markup, escape
    member_patterns = []
    for g in people:
        for m in g["members"]:
            base = re.sub(r",.*$", "", m["name"]).strip()          # drop ", Ph.D." etc.
            parts = base.split()
            names = [f"{parts[-1]}, {parts[0][0]}."] + list(m.get("pub_names", []))
            is_pi = g["status"] == "current" and g is people[0] and m is g["members"][0]
            for n in names:
                last, ini = [x.strip() for x in n.split(",", 1)]
                ini = ini.strip()[0]            # match on the first initial; extra initials are optional
                rx = (r"(?<![\w-])" + re.escape(last) + r",\s?" + re.escape(ini) +
                      r"\.(?:\s?[A-Z]\.)*(?:[A-Z](?![a-z.]))?")
                member_patterns.append((re.compile(rx), base, is_pi))

    for n in site.get("other_lab_authors", []) or []:
        last, ini = [x.strip() for x in n.split(",", 1)]
        rx = (r"(?<![\w-])" + re.escape(last) + r",\s?" + re.escape(ini.strip()[0]) +
              r"\.(?:\s?[A-Z]\.)*(?:[A-Z](?![a-z.]))?")
        member_patterns.append((re.compile(rx), n, False))

    def bold_lab(text):
        t = str(escape(text))
        for rx, full, is_pi in member_patterns:
            cls = "lab-pi" if is_pi else "lab-member"
            t = rx.sub(lambda mt: f'<mark class="{cls}" title="{full} (Taylor Lab)">{mt.group(0)}</mark>', t)
        return Markup(t)
    env.filters["bold_lab"] = bold_lab
    env.filters["slug"] = lambda s: re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")

    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for extra in ("CNAME", "robots.txt"):
        if os.path.exists(os.path.join(ROOT, extra)):
            shutil.copy(os.path.join(ROOT, extra), OUT)
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    ctx = dict(site=site, people=people, pubs=pubs, years=years, by_year=by_year,
               gallery=gallery, year_now=datetime.date.today().year,
               pub_count=len(pubs), latest=[p for p in pubs if p.get("title")][:3])
    for tpl, out, title, nav in PAGES:
        depth = out.count("/")
        root = "../" * depth          # relative links work on github.io previews and the real domain
        if tpl == "404.html":         # 404 is served at any depth, so it needs an absolute base
            root = os.environ.get("BASE_PATH", "/").rstrip("/") + "/"
        html = env.get_template(tpl).render(page_title=title, current=nav, root=root, **ctx)
        dest = os.path.join(OUT, out)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(html)
    # sitemap
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for _, out, _, nav in PAGES:
            if nav is not None:
                f.write(f"  <url><loc>{site['url']}/{nav}</loc></url>\n")
        f.write("</urlset>\n")
    print(f"Built {len(PAGES)} pages into {OUT}")

if __name__ == "__main__":
    main()
    if "--serve" in sys.argv:
        import http.server, functools
        print("Preview: http://localhost:8000  (Ctrl+C to stop)")
        http.server.ThreadingHTTPServer(("", 8000), functools.partial(http.server.SimpleHTTPRequestHandler, directory=OUT)).serve_forever()
