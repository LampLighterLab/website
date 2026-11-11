# LampLighter Lab website

## Setup

Install **Ruby 3.2+**, **Bundler**, and **Python 3.11+**, then:

```sh
git clone https://github.com/LampLighterLab/website.git
cd website
bundle install
sh scripts/setup-hooks.sh
```

Run setup once per clone. It installs the photo tools and enables the commit hook.

## Preview and build locally

```sh
bundle exec jekyll serve --livereload
```

Open <http://127.0.0.1:4000>. Stop the server with **Ctrl+C**.
To compile without starting a server:

```sh
bundle exec jekyll build
```

Edit source files; `_site/` is generated and should not be committed.
Restart the server after changing `_config.yml`.

## Add or update your profile

Create `_people/first_last.md`, using your name in lowercase with underscores.
For example, Steve Heim uses `_people/steve_heim.md`.

```yaml
---
name: First Last
role: [UG, MEng, MS, PhD, Postdoc, PI]
group: current
initials: FL
order: 1
website: ""
---
```

- Replace the name and initials. Use `UG`, `MS`, `MEng`, `PhD`, or `PI` for the role.
- Keep `order: 1`
- Set `website` to your full personal URL, or leave it blank.
- To update your card, edit your existing file. To move to alumni, set `group: alumni`.

Place your portrait at **`assets/images/people/first_last.jpg`**, matching the
profile filename exactly. JPG, JPEG, PNG, and WebP are supported; use lowercase
extensions and only one photo per person. Convert HEIC to JPG first.
Without a photo, your initials appear instead.

Keep the original photo outside the repo. Choose a centered face with room around
it: the commit hook automatically fixes rotation, crops to a square, resizes to
at most **800×800**, and compresses to **200 KiB**. It rejects any staged file
over **1 MiB**. To prepare the photo before previewing it:

```sh
.venv/bin/python scripts/prepare_portraits.py assets/images/people/first_last.jpg
```

Check your card at <http://127.0.0.1:4000/people/>, then commit and push your branch:

```sh
git add _people/first_last.md assets/images/people/first_last.jpg
git commit -m "Update First Last profile"
git push
```

The hook stages the compressed photo automatically. If it reports unstaged photo
changes, stage the whole photo and retry. If you have no photo, omit its path
from `git add`.

Deployment and other editing details are in [MAINTAINING.md](MAINTAINING.md).
