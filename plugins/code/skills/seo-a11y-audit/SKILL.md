---
name: seo-a11y-audit
description: Audit a web page for SEO and accessibility fundamentals — metadata, heading structure, semantic HTML, links, Open Graph/Twitter cards, alt text, keyboard navigation, focus, contrast, and ARIA. Use when reviewing a page for search visibility and accessibility before launch.
---

# SEO & A11y Audit

SEO and accessibility overlap more than people think — both reward semantic, well-
structured HTML that machines (crawlers, screen readers) can understand. This skill
audits both in one pass over the markup.

## Process

### 1. Document metadata (SEO)

- **`<title>`** — unique, descriptive, ~50–60 chars, keyword near the front.
- **Meta description** — present, compelling, ~150–160 chars (it's the search snippet).
- **Canonical URL** — set, to avoid duplicate-content splits.
- **`lang`** on `<html>`, correct `charset` and `viewport`.
- **Robots** — confirm the page isn't accidentally `noindex`; check `robots.txt`/sitemap
  if relevant.

### 2. Heading structure (SEO + a11y)

- Exactly **one `<h1>`** describing the page.
- Headings nest without skipping levels (no `<h2>` jumping to `<h4>`) — screen-reader
  users navigate by this outline, and crawlers weight it.
- Headings describe content, not styled for size. Don't use a heading tag just for big
  text.

### 3. Semantic structure (a11y)

- Landmark elements — `<header>`, `<nav>`, `<main>` (one), `<footer>` — not a soup of
  `<div>`s. Screen readers jump between landmarks.
- Lists are `<ul>/<ol>`, buttons are `<button>`, links are `<a href>`. A clickable
  `<div>` is invisible to keyboard and assistive tech.

### 4. Links & images

- **Links** — descriptive text, not "click here"/"read more" (both SEO and screen-reader
  context). `<a href>` for navigation, `<button>` for actions. External links safe
  (`rel="noopener"`).
- **Images** — meaningful images have descriptive `alt`; decorative ones have `alt=""`
  (not missing). The LCP image isn't lazy-loaded.

### 5. Social / sharing

- **Open Graph** (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`) and
  **Twitter Card** tags for rich link previews.
- `og:image` exists, is the right size (~1200×630), and is an absolute URL.
- **Structured data** (JSON-LD) where it fits (Article, Product, Breadcrumb) for rich
  results.

### 6. Keyboard & visual a11y

- **Keyboard** — every interactive element reachable and operable by Tab/Enter/Space;
  logical tab order; visible focus indicator (don't `outline: none` without a
  replacement); a skip-to-content link.
- **Forms** — every input has an associated `<label>`; errors are announced, not just
  colored red.
- **Contrast** — text meets WCAG AA (4.5:1 normal, 3:1 large). Don't convey meaning by
  color alone.
- **ARIA** — used only where native HTML can't do it, and correctly (bad ARIA is worse
  than none).

## Output shape

```text
## SEO            (metadata, headings, structured data — issue → fix)
## Accessibility  (semantics, keyboard, contrast, alt, forms, ARIA — issue → fix)
## Both           (heading/semantic issues that hurt SEO and a11y together)
## Priorities     (blockers first: noindex, missing h1, keyboard traps, no alt on key images)
```

Where possible, point at the element/selector. Lead with anything that blocks indexing
or makes the page unusable by keyboard/screen-reader — those are not "nice to haves".
