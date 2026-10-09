# thetaylorlab.com

Public website of the Taylor Lab (Department of Pharmacology, Case Western Reserve University).
It is a small static site: content lives in plain text files, and GitHub rebuilds and publishes the site automatically whenever something changes on the `main` branch.

## Editing content (no coding needed)

You can edit everything in the GitHub website: open a file, click the ✏️ pencil, make the change, then **Commit changes**. The live site updates about a minute later (watch the **Actions** tab).

| To change… | Edit this file |
|---|---|
| Add a publication | `data/publications.yml`: copy an existing entry, paste it at the top, and edit it |
| Add, edit or move a lab member to alumni | `data/people.yml` |
| Gallery photos and captions | `data/gallery.yml` |
| Address, menu | `data/site.yml` |
| Research text | `templates/research.html` |
| Home page text | `templates/home.html` |

**Adding an image** (a headshot, paper figure or gallery photo): open the matching folder (`assets/img/people/`, `assets/img/pubs/` or `assets/img/gallery/`), choose **Add file → Upload files**, then point to it from the YAML file, e.g. `photo: assets/img/people/new-person.webp`. Keep images under about 1000 px wide (JPG, PNG or WebP all work).

**Example publication entry**

```yaml
- year: 2026
  title: Title of the paper
  citation: Author, A., Huang, W. and Taylor, D.J., 2026. Journal, 12(3), p.456.
  abstract: Optional abstract text.
  link: https://pubmed.ncbi.nlm.nih.gov/12345678/
  image: assets/img/pubs/2026-short-name.webp
```

YAML is picky about indentation: keep the same spaces as the neighbouring entries. If a change breaks the build, the **Actions** tab shows a red ✗, the previous version stays online, and you can fix or revert the commit.

## Previewing on your computer (optional)

```bash
pip install -r requirements.txt
python build.py --serve      # then open http://localhost:8000
```

## How it is published

`.github/workflows/pages.yml` runs `build.py`, which turns `data/` + `templates/` + `assets/` into the finished site in `_site/`, and deploys it to GitHub Pages.
