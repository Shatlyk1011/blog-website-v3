# Blog view counter Worker

This Cloudflare Worker is the server-side view counter for the Next.js blog. It uses D1 so visitors cannot write directly to the database.

## Deploy

From this directory:

```bash
npx wrangler login
npx wrangler d1 create blog-view-counter
```

Copy the returned database ID into `wrangler.jsonc`, then apply the schema and deploy:

```bash
npx wrangler d1 migrations apply blog-view-counter --remote
npx wrangler deploy
```

Set the Worker URL in the Hugo site's `hugo.toml`, for example:

```toml
[params.viewCounter]
url = "https://blog-view-counter.<account-subdomain>.workers.dev"
```

`ALLOWED_ORIGINS` is a comma-separated allowlist. It includes both the production
site and the local Hugo server at `http://localhost:1313` by default. Add any
other development origin there before deploying the Worker.

## API

- `POST /v1/views/:articleId` increments and returns the view total.
- `GET /v1/views/:articleId` returns the current total without incrementing it.

The Worker accepts only the configured blog origin, validates article identifiers, and applies a basic per-IP, per-article rate limit. The Hugo site adds one view per browser session per article.
