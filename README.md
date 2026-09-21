# Simulation Toolbox · ROSCon 2026

Landing page for the **Simulation Toolbox – gearing up for robotics** session
(Adam Dąbrowski, Robotec.ai) at ROSCon 2026, Toronto. It is the single page
behind the QR code on the slides: every simulator, standard, talk and resource
mentioned in the session, verified against current releases, plus the practice
notebooks.

Built as a static site with [Hugo](https://gohugo.io/) and deployed to GitHub
Pages by GitHub Actions. No JavaScript is required to read it; a few lines
filter the simulator cards.

## Content and hosting are separate

| You want to…                              | Edit                                   |
| ----------------------------------------- | -------------------------------------- |
| Bump a simulator release, add a link      | `data/simulators.yaml`                 |
| Add or reword a secondary tool            | `data/tools.yaml`                      |
| Change the decision table                 | `data/cheatsheet.yaml`                 |
| Update the standards (SI, REP-158, co-sim)| `data/standards.yaml`                  |
| Publish the notebook links, fix the result| `data/practice.yaml`                   |
| Talks and community links                 | `data/resources.yaml`                  |
| Session metadata, speaker, slides path    | `data/site.yaml`                       |
| Intro paragraph                           | `content/_index.md`                    |
| Replace the slides                        | `static/slides/*.pdf` (+ path in `data/site.yaml`) |
| Look and feel                             | `assets/css/style.css`, `layouts/partials/*.html` |
| Hosting                                   | `.github/workflows/pages.yml`, `hugo.toml` |

Nothing in `layouts/` contains prose; if you find yourself editing HTML to
change words, the words belong in a data file instead.

The **workload spectrum** graphic is generated from the `workload` field
(0 = software-in-the-loop, 100 = robot learning) of each simulator, so it stays
in sync with the cards. Filter chips use the `tags` field.

## Hosting on GitHub Pages

1. Create the empty repository `RobotecAI/simulation-toolbox` on GitHub (the remote is already configured).
2. Push this directory to its `main` branch:

   ```bash
   git push -u origin main
   ```

3. In the repository: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. The `Deploy to GitHub Pages` workflow runs on the push (or trigger it under
   **Actions → Run workflow**). About a minute later the site is live at
   <https://robotecai.github.io/simulation-toolbox/>.

The workflow reads the final URL from GitHub, so the site works unchanged for
a project page, an organisation page or a custom domain (add the domain under
Settings → Pages; no config change needed). It also passes the repository URL
in so the page shows "edit / report a stale link" links.

### QR code for the slides

Already generated for the URL above (`static/img/qr-slides.png`, 2048 px). To regenerate:

```bash
pip install "qrcode[pil]"
python3 tools/make_qr.py https://robotecai.github.io/simulation-toolbox/
```

This writes `static/img/qr-slides.png` (for the deck) and `static/img/qr.png`,
which the page shows automatically in the Q&A box.

## Local preview

```bash
hugo server            # http://localhost:1313/ with live reload
hugo --gc --minify     # production build into public/
tools/check_links.sh   # curl every external link in data/*.yaml
```

Any Hugo ≥ 0.110 (extended) works; CI pins `HUGO_VERSION` in
`.github/workflows/pages.yml`. A weekly `Check links` workflow flags dead
links and runs on pull requests touching `data/`.

## Before the session — needs Adam

- [ ] `data/practice.yaml`: paste the two notebook URLs (rendered as "Link to be published" until then) and confirm the 24 % → 1 % fall-rate result and its metric definition with the exercise team.
- [ ] `data/site.yaml`: official workshop URL, once listed on roscon.ros.org.
- [ ] `static/slides/`: replace the PDF with the final export carrying the QR code; keep the filename or update `data/site.yaml`.
- [ ] Optional hero image: `static/img/humanoids-warehouse.jpg` (from slide 3) is included but not used, pending confirmation it is our own capture.
- [ ] Licence check: code MIT, text/data CC BY 4.0 (see `LICENSE`). Change if Robotec.ai prefers Apache-2.0 for the code.

## Structure

```
.
├── hugo.toml                 site plumbing (baseURL is overridden in CI)
├── content/_index.md         intro paragraph
├── data/                     ← all content
├── layouts/
│   ├── index.html            single-page shell
│   └── partials/             one file per section + spectrum SVG
├── assets/css/style.css      theme (light/dark, print)
├── static/                   slides PDF, images, favicon
├── tools/                    make_qr.py, check_links.sh
└── .github/workflows/        pages.yml (deploy), links.yml (weekly link check)
```

## Contributing

Found a newer release or a stale link? Edit the relevant YAML in `data/` and
open a pull request. Keep the `verified` date honest: set it to the day you
checked the upstream page.
