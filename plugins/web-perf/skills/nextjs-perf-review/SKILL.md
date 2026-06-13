---
name: nextjs-perf-review
description: Review a Next.js App Router app for performance — server vs client components, hydration cost, caching and revalidation, data fetching, image optimization, and font loading. Use when a Next.js app is slow, over-hydrating, or you want a rendering/caching review before shipping.
---

# Next.js Perf Review

Next.js gives you a fast default and a dozen ways to throw it away — a stray
`"use client"`, an uncached fetch, an unoptimized image. This skill reviews an App
Router app for the rendering and caching mistakes that cost the most.

## Process

### 1. Server vs client components

The default is a Server Component (zero JS to the client). Every `"use client"` is a
deliberate cost. Check:

- Components marked client that don't need interactivity — they (and their imports) ship
  and hydrate for nothing. Push the `"use client"` boundary **down** to the leaf that
  actually needs state/effects/handlers.
- A client component high in the tree forcing everything under it to be client too.
- Data fetching or heavy formatting done in a client component that belongs on the
  server.

### 2. Hydration cost

- Large client trees hydrating on load → poor INP/TBT. Move static parts to server
  components; keep interactive islands small.
- Pass server-fetched data as props rather than re-fetching on the client.
- Heavy client-only widgets (editors, charts, maps) → `next/dynamic` with `ssr: false`
  and load on interaction.

### 3. Caching & revalidation

This is where App Router performance is won or lost:

- **`fetch` caching** — is data static (cached), dynamic (`no-store`), or time-based
  (`next: { revalidate: N }`)? An accidental `no-store` makes a cacheable page dynamic
  and slow.
- **Route segment config** — `dynamic`, `revalidate`, `fetchCache` set intentionally?
- **`generateStaticParams`** for known dynamic routes to prerender them.
- Tag-based revalidation (`revalidateTag`) used for targeted invalidation instead of
  blanket dynamic rendering.
- Watch for things that silently opt a route into dynamic rendering (`cookies()`,
  `headers()`, `searchParams`) when it could be static.

### 4. Data fetching

- Parallelize independent fetches (`Promise.all`) instead of awaiting in series
  (request waterfalls).
- Fetch at the layout/page level and stream; use `<Suspense>` boundaries so slow data
  doesn't block the whole page.
- Avoid client-side fetch-on-mount for data that could be server-rendered.

### 5. Images, fonts, scripts

- **`next/image`** for all content images (sizing, lazy-load, modern formats); set
  `priority` on the LCP image and avoid lazy-loading it.
- **`next/font`** to self-host and avoid layout shift + render-blocking font requests.
- **`next/script`** with the right `strategy` (`afterInteractive`/`lazyOnload`) for
  third-party scripts.

## Output shape

```text
## Rendering       (client/server boundary issues, with the component + fix)
## Hydration       (oversized client trees, dynamic-import candidates)
## Caching         (fetch/segment config issues, accidental dynamic rendering)
## Data fetching   (waterfalls, missing Suspense/streaming)
## Assets          (image/font/script issues)
## Priorities      (the changes with the biggest Core Web Vitals impact)
```

Tie findings back to the metric they hurt (LCP, INP, CLS) where you can, and lead with
the ones on the initial render path. For raw measurement, pair with the `web-perf` skill.
