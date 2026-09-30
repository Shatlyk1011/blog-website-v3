# Shatlyk Abdullayev’s blog

An English-only Hugo site using the [Taiga](https://github.com/justskiv/taiga) theme. All articles live in one chronological feed and are organized by tags.

## Requirements

- Hugo 0.146 or newer
- Pagefind 1.5.2 or newer

The Taiga theme is pinned as a Git submodule. Clone with submodules enabled:

```sh
git clone --recurse-submodules <repository-url>
```

If the repository was cloned without submodules, initialize the theme with:

```sh
git submodule update --init --recursive
```

## Development

```sh
hugo server --buildDrafts
```

## Production build

```sh
hugo --gc --minify --panicOnWarning
pagefind --site public
python3 themes/taiga/scripts/check-links.py public
```

## Analytics

Analytics are disabled when their values are empty. Configure them in `hugo.toml` or through Hugo configuration environment variables:

- `HUGO_PARAMS_ANALYTICS_CLARITYID`
- `HUGO_PARAMS_ANALYTICS_GOOGLEANALYTICSID`
- `HUGO_PARAMS_ANALYTICS_GOOGLETAGMANAGERID`

## Content model

Every article is a Hugo leaf bundle:

```text
content/articles/article-slug/
├── index.md
└── cover.webp
```

The old `/dev/`, `/thoughts/`, and `/blog/` article URLs are emitted as redirect aliases.
