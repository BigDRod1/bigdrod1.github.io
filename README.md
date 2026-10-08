# NotAFinanceBro (bigdrod1.github.io)

Static research blog for [NotAFinanceBro](https://bigdrod1.github.io), built with Jekyll for GitHub Pages (user site: serve from `main` root).

## Local build

```bash
bundle install
bundle exec jekyll serve
```

Open http://127.0.0.1:4000

## Publishing the first article

The article `_posts/2026-10-12-the-tyranny-of-the-bell-curve.md` ships with:

```yaml
published: false
```

On Monday, October 12, 2026, change that one line to:

```yaml
published: true
```

Commit and push to `main`. Charts are already public at `/assets/charts/`.

## Chart URL pattern

`https://bigdrod1.github.io/assets/charts/<filename>.png`

Example: https://bigdrod1.github.io/assets/charts/01_spy_hist_vs_normal.png
