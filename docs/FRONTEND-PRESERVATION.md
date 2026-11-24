# Frontend preservation and known original issues

## Evidence

The complete pre-integration ZIP includes original working changes, untracked files, `.git`, editor settings and `node_modules`. Its location is in BACKUP-LOCATION.txt. The manifest records 2,675 non-Git files; the archive also contains Git metadata. The original 12 HTML pages and all original CSS are included in that baseline.

`scripts/verify_frontend.py` compares every baseline file's SHA-256 to the parent tree, verifies every copied static asset, then checks all 12 rendered page DOMs against the original after normalizing only technical URL/static/form bindings. It separately compares all inline script bodies. This tests layout structure, text, original classes and unchanged scripts; it is not proof of pixel-identical rendering in a real browser.

## Copy strategy

Only `django_backend/` was created inside the existing repository. Original README, package files, Tailwind configuration, CSS, HTML and assets remain unchanged. Static assets under `static/frontend` are byte-for-byte copies. No CSS override was added to make Django look different. Exact navbar/footer variants are kept in include files, preserving inconsistent original labels rather than silently rewriting company content.

The only pre-existing broken active local link repaired in copied templates is the Quality footer's `./services-details-supply.html`, mapped to the actual Supply Chain named route. The original link is unchanged. Both partnership variants are retained, not merged. Relative image references in commented markup are preserved/documented rather than treated as visible failures.

## Existing issues deliberately retained

- Placeholder Font Awesome `integrity="sha512-..."` on some pages can block that external icon stylesheet in a browser.
- Old footer labels still call the Sourcing page Mineral Trading and the Trading page Gold Export.
- Many social links are `#`; only supplied real URLs remain real URLs.
- Homepage Get Started links to the homepage.
- The Contact page has an unmatched closing main element and differing displayed address variants.
- Some external photographs may be unavailable or depict a subject different from their alt text; no new images or content were substituted.
- CSS contains accumulated global overrides and original animation choices.
- Original counters/company claims were preserved, not independently verified or changed.

These require separate approval if you want them fixed. Fonts, Bootstrap, AOS, icon stylesheets, remote images and Maps remain external dependencies. Their URLs are preserved, but CDN availability and full visual behavior need browser checks. See TESTING.md for what was actually verified.
