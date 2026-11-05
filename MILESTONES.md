# Website launch checklist

Build a complete, straightforward static Jekyll site using the layout and page
structure of the [Lighthouse Lab reference](https://thelighthouselab.org/research/),
with a light theme and the lab content already in this repository. Missing
information belongs in this checklist, not in visible placeholder pages.

## Reference-based rebuild

Status: Local implementation and initial verification complete. Standard and
subpath production builds pass. Reviewed in Chrome at 1440, 768, 390, and 320px.

- [x] Apply the reference's restrained layout, typography, spacing, and navigation
  across the site, using a light theme.
- [x] Complete Home, Research, People, Teaching, About, and Join using existing
  repository content.
- [x] Add detail pages for Animal movement, Robotics and learning, and Agriculture;
  describe research themes without implying completed projects or results.
- [x] Keep research-area summaries in `_data/research.yml` and their detail content
  in `_projects/`.
- [x] Store member records in `_people/` and course data in `_data/teaching.yml`.
- [x] Make `/research/` canonical and redirect the legacy `/projects/` address.
- [x] Add a native SVG lamp mark and favicon.
- [x] Keep Publications unpublished and out of navigation until bibliography
  content is supplied.
- [x] Add page descriptions, a 404 page, and a mobile navigation toggle that
  preserves navigation without JavaScript.
- [x] Verify the standard Jekyll build.
- [x] Check page routes, internal links, assets, and fragment anchors across all
  11 generated pages.
- [x] Review the completed site at phone and desktop widths; check for horizontal
  overflow at tablet and narrow phone widths.
- [x] Check mobile menu operation, Escape, keyboard skip link, research detail
  navigation, the legacy redirect, and navigation without JavaScript.
- [x] Check text contrast against the page and card backgrounds (minimum 4.87:1).

## Information still needed

- [ ] Confirm the principal investigator, institution, department, and public
  contact details.
- [ ] Review the current members and alumni, including names, roles, and profile
  links.
- [ ] Supply concrete project records before adding project-specific claims:
  question, description, contributors, status, results, and paper/code/data links.
- [ ] Choose a publication source and provide the initial bibliography.
  A Google Scholar profile is linked from Research; the local Publications page
  remains unpublished until it has content.
- [ ] Supply approved photographs and research figures, with captions, credits,
  and alternative text.
- [ ] Confirm current recruitment guidance and the collaboration contact.
- [ ] Confirm the teaching descriptions and course links.

## Quality and launch

- [ ] Review all public copy for accuracy and remove unfinished material.
- [x] Check page titles and descriptions, favicon, and a useful 404 page.
- [x] Check heading structure, keyboard navigation, focus visibility, color
  contrast, and current image alternative text.
- [ ] Check external links and any newly supplied images.
- [ ] Review the site in the target browsers and optimize any supplied images.
- [x] Prepare GitHub Pages deployment for `LampLighterLab/website`, with production
  defaults at `https://lamplighterlab.github.io/website/` and a workflow that
  builds pull requests and deploys `main`.
- [ ] Enable GitHub Actions as the publishing source in Settings → Pages, push
  the workflow, and verify the first deployment and HTTPS at the final address.
- [x] Establish a Git baseline and document deployment and rollback.
- [ ] Have a lab member follow the README to update a page or research area.
- [ ] Complete the lab's content and design review, then publish.

The repository is prepared for GitHub Pages; publication still requires the
repository setting and first deployment above. See [README.md](README.md) for
local previews, deployment, rollback, and editing instructions.
