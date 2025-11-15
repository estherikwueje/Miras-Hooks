# Mira's Hooks — Frontend improvements and hosting

This repo contains a small static site. I made front-end refinements (hero layout, responsive fixes, nav improvements) and added a simple GitHub Pages workflow.

How to preview locally

1. From the repo root run a simple server:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

2. Open the pages in a browser (e.g. `index.html`, `men.html`, `women.html`, `kids.html`).

Deploy to GitHub Pages

- There's a GitHub Actions workflow at `.github/workflows/gh-pages.yml` that will publish the repository root to GitHub Pages on every push to `main` using the default `GITHUB_TOKEN`.
- After pushing, enable GitHub Pages in repository Settings → Pages and select the `gh-pages` branch (the workflow will create/update it).

Next steps I can take (choose any):
- Tidy layout of product cards and add consistent spacing and captions.
- Replace inline image width/position styles with CSS classes.
- Optimize and add alt text for all images.
- Commit and push changes, or open a PR.
