# Website maintenance

For setup, local builds, and member profiles, see [README.md](README.md).
This reference keeps deployment, site structure, and advanced editing details.

The site uses Jekyll and a light layout based on the [Lighthouse Lab reference](https://thelighthouselab.org/research/).


## GitHub Pages deployment

The intended public address is <https://lamplighterlab.mae.cornell.edu/>.
The repository can keep its name, `LampLighterLab/website`: a custom domain serves
this site at `/`, without the repository name in the URL. Until the custom domain
is configured, the default address is <https://lamplighterlab.github.io/website/>.
`.github/workflows/pages.yml` builds the site using Ruby 3.4 and the dependencies in `Gemfile.lock`, then uploads
only `_site/` to GitHub Pages. Pull requests to `main` build without deploying;
pushes to `main` and manual runs on `main` build and deploy.

Before the first deployment:

1. Open the repository's [Settings → Pages](https://github.com/LampLighterLab/website/settings/pages).
   Under **Build and deployment → Source**, select **GitHub Actions**. Use the
   workflow already in this repository; there is no need to create another one.
2. Ensure GitHub Actions is enabled for the repository and the organization
   permits the actions used in the workflow. A public repository works with
   GitHub Free; private repositories require a plan that supports Pages.
3. Commit and push the source changes to `main`. In **Actions**, check that
   **Build and deploy website** finishes successfully. Once the workflow is on
   `main`, **Run workflow** can also deploy it without a new commit.
4. Open the deployed URL from the workflow. Check Home, research detail pages,
   People and portraits, Teaching, Joining, and an unknown URL to test the 404.
   Confirm **Enforce HTTPS** in Pages settings.

### Unstyled site after deployment

Check **Settings → Pages → Build and deployment → Source** is **GitHub Actions**.
The branch-based Pages builder uses Jekyll 3 and an older Sass compiler; it leaves
`@use "base"` in the CSS instead of compiling this site's styles. A successful
`pages build and deployment` run alongside our `Build and deploy website` run
indicates the competing branch builder is still enabled. Select GitHub Actions
and rerun our workflow on `main` after fixing any failed checks. Do not add a
second suggested workflow. Our workflow checks the compiled CSS before upload.

The workflow uses GitHub's automatic token; no personal access token, deployment
key, `gh-pages` branch, or committed `_site/` folder is needed. Pages must be
enabled in Settings before the workflow, including pull request builds, can read
its settings. The workflow reads both the origin and base path from GitHub, so
canonical URLs, links, and assets follow the active hosting address: `/website/`
on the temporary GitHub address, or `/` once the custom domain is configured.
These values override the production defaults only during the workflow build;
the temporary configuration is not committed or included in the public site.

To preview the production configuration locally, stop any existing preview server
and run:

```sh
bundle exec jekyll serve --config _config.yml,_config.production.yml
```

Open <http://127.0.0.1:4000/>. To check the production build alone:

```sh
JEKYLL_ENV=production bundle exec jekyll build --config _config.yml,_config.production.yml --strict_front_matter
```

To connect the Cornell address:

1. In this repository's **Settings → Pages → Custom domain**, enter
   `lamplighterlab.mae.cornell.edu` and save it.
2. Ask the Cornell/MAE DNS administrator to create this DNS record after the
   GitHub setting is saved:

   ```dns
   lamplighterlab.mae.cornell.edu. IN CNAME lamplighterlab.github.io.
   ```

   The target is the GitHub hostname only, with no `/website` suffix.
3. Once DNS validates and the HTTPS certificate is available, enable
   **Enforce HTTPS** and run the deployment workflow again. Check that the home
   page is at `/` and research pages are at `/research/.../` on the Cornell host.

`_config.production.yml` already uses the Cornell origin with an empty `baseurl`.
No repository rename or `CNAME` file is needed for this Actions deployment.
Configure the Cornell hostname as a custom domain pointing to GitHub Pages so
it remains the address visitors see in their browser.

For rollback, revert the offending source commit on `main` and push the revert.
The workflow rebuilds and deploys the restored source. Keep generated files out
of Git during deployment and rollback.

See GitHub's [publishing source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
and [custom subdomain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-a-subdomain).

## What belongs in Git

Commit the Markdown content, YAML data and configuration, templates, Sass,
JavaScript, images and downloadable files, documentation, `.gitignore`,
`Gemfile`, and `Gemfile.lock`. The lockfile is generated by Bundler but belongs
in Git so contributors and deployment use the same dependency versions.
The `.gitkeep` files preserve intentionally empty content and asset folders.

Do not commit `_site/`: Jekyll generates its HTML, compiled CSS, source maps,
and copied assets from the source files. Also leave `.jekyll-cache/`,
`.jekyll-metadata`, `.sass-cache/`, `.bundle/`, `vendor/`, macOS metadata,
and editor temporary files untracked. These are covered by `.gitignore`.

Run `git diff --cached` to review staged source changes before committing.

## Pages and content

| Page | Source | Public URL |
| --- | --- | --- |
| Home | `index.md` | `/` |
| Research | `projects.md` | `/research/` |
| Animal movement | `_projects/animal-movement.md` | `/research/animal-movement/` |
| Robotics and learning | `_projects/robotics-and-learning.md` | `/research/robotics-and-learning/` |
| Agriculture | `_projects/agriculture.md` | `/research/agriculture/` |
| People | `people.md` and `_people/` | `/people/` |
| Teaching | `teaching.md` and `_data/teaching.yml` | `/teaching/` |
| About | `about.md` | `/about/` |
| Join | `join.md` | `/join/` |

The old `/projects/` address redirects to `/research/`. The `_projects/`
collection currently holds research-area pages describing the lab's existing
themes; these pages do not represent individual projects or completed results.

- `_data/research.yml` supplies the three research-area summaries. Each entry
  contains `slug`, `title`, and `summary`.
- `_data/navigation.yml` controls the main navigation.
- `_people/` contains member records rendered by `_layouts/people.html`.
- `_data/teaching.yml` supplies the course listings on Home and Teaching.
- `_layouts/` and `_includes/` contain shared page templates, navigation, and
  footer content.
- `_sass/` and `assets/css/` contain the typography, colors, and responsive
  layouts. `assets/images/lamp.svg` provides both the lamp mark and favicon.
- `assets/js/main.js` adds the mobile menu toggle; navigation remains available
  when JavaScript is disabled.
- `404.html` supplies the page-not-found screen.
- `_publications/` is a reserved collection. `publications.md` has
  `published: false` and is omitted from normal builds until bibliography content
  is supplied. It is also absent from navigation.

## Updating content

Edit the relevant Markdown page while keeping its YAML front matter. Page headers
show only the title; put the main text directly in the Markdown body.
Use `##` for sections beneath the page title supplied by the layout. Keep
`description` concise for search metadata and link to source material when it is
available.

For a paragraph in a slightly smaller font, add `.text-small` on the next line:

```markdown
This paragraph is 10% smaller than the surrounding text.
{: .text-small }
```

For just part of a sentence, use
`<span class="text-small">smaller text</span>`. Adjust `.text-small` in
`_sass/_base.scss` to change the size consistently across the site.

To update a research area, edit both its summary in `_data/research.yml` and the
corresponding Markdown file in `_projects/`. The data entry's `slug` should match
the filename without `.md` and the last segment of the page's `permalink`. Keep
these aligned, and preserve public URLs or add redirects when changing them.

## Portrait tooling

To prepare a photo and inspect the crop before committing:

```sh
.venv/bin/python scripts/prepare_portraits.py assets/images/people/first_last.jpg
```

Then open the resulting file in your usual image viewer. This overwrites the
web copy in place, so keep your original elsewhere. Crop the original yourself
first if the automatic center crop does not frame your face well. With no paths,
the script prepares all portraits in `assets/images/people/`. Already prepared
images are left unchanged, so subsequent commits do not repeatedly degrade them.

No template edit or `image` field is required to add a card. If the portrait is
missing, the site shows your initials. For an unusual filename, an optional
`image: /assets/images/people/custom_portrait.jpg` field overrides the automatic
match; avoid this for new profiles. Supported extensions are checked in the order
`.jpg`, `.jpeg`, `.png`, `.webp`, so remove old copies if you switch formats.

To move someone to the alumni list, change their record to `group: alumni`.
Alumni show names only, with an optional website link. `people.md` controls the
page title and description.

The commit checker can also run without modifying files:

```sh
.venv/bin/python scripts/check_commit.py --check         # staged files
.venv/bin/python scripts/check_commit.py --check --all   # all tracked files
.venv/bin/python -m unittest discover -s tests
```

Portrait preparation uses [Pillow](https://pillow.readthedocs.io/en/stable/).

## Other assets

| Asset | Folder |
| --- | --- |
| Your portrait and current member portraits | `assets/images/people/` |
| Research photos and diagrams | `assets/images/research/` |
| PDFs, CVs, and other downloadable files | `assets/files/` |
| Lamp mark and favicon | `assets/images/lamp.svg` |

Use hyphens in filenames for assets other than portraits. The 1 MiB staged-file
limit also applies to these folders; the automatic portrait script only processes
files in `assets/images/people/`.

Other assets need a link or image in the relevant Markdown page, for example in
`_projects/animal-movement.md`:

```liquid
![Describe what this figure shows]({{ '/assets/images/research/movement.jpg' | relative_url }})

[Download the paper (PDF)]({{ '/assets/files/paper.pdf' | relative_url }})
```

These paths are relative to the site root. The `relative_url` filter also supports
hosting the site under a subpath. Always edit source files, not `_site/`.

To update Teaching, edit `_data/teaching.yml`. Each course has `number` and `name`;
optional `description` and `link` fields add context and a course-information
link. The Home page reads this same course list.

Specific projects, papers, photographs, and contact details can be added when
the lab supplies them. Record missing information in
[MILESTONES.md](MILESTONES.md), rather than adding public placeholder copy.

After changes, build the site and review the affected pages at phone and desktop
widths. Check navigation, links, headings, and any image alternative text.
