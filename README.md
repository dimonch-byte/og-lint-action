# og-lint-action

Catch broken link previews **before** they ship: fails the PR when your built HTML has no `og:image`, a *relative* `og:image` (the #1 reason LinkedIn/Facebook show no picture), no `twitter:card`, or no image dimensions.

```yaml
- uses: actions/checkout@v4
- run: npm run build
- uses: dimonch-byte/og-lint-action@v1
  with:
    targets: "dist/**/*.html"
    # warn-only: "true"
```
Local: `python3 og_lint.py 'dist/**/*.html'` or `python3 og_lint.py https://your-site.com/`

**What it does not do:** it checks markup only. A page can pass and still show no preview if your host, WAF or bot-protection blocks `facebookexternalhit`/`LinkedInBot`.

Browser version (paste your `<head>`): https://dimonch-byte.github.io/og-lint/

*Disclosure: I build [SharePack](https://sharepack.adjudi.com/?utm_source=github&utm_medium=readme&utm_campaign=sharepack-intent-w2&utm_content=og-lint-action), a paid ($29) pack that fetches your live page as each real crawler and gives the exact fix. This action is free and MIT, and works without it.*
