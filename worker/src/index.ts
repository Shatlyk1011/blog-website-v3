type D1Result<T> = {
  results: T[]
}

type D1Statement = {
  bind: (...values: string[]) => D1Statement
  first: <T>() => Promise<T | null>
  run: <T>() => Promise<D1Result<T>>
}

type D1Database = {
  prepare: (query: string) => D1Statement
}

type WorkerHandler<Environment> = {
  fetch: (request: Request, env: Environment) => Response | Promise<Response>
}

export interface Env {
  DB: D1Database
  ALLOWED_ORIGINS: string
}

type ViewRow = { views: number }
type RateLimitEntry = { requests: number; resetAt: number }

const rateLimits = new Map<string, RateLimitEntry>()
const RATE_LIMIT_WINDOW_MS = 60_000
const RATE_LIMIT_MAX_REQUESTS = 12
const validArticleId = /^[a-z0-9][a-z0-9-]{0,159}$/

function corsHeaders(request: Request, env: Env) {
  const origin = request.headers.get('Origin')
  const allowedOrigins = env.ALLOWED_ORIGINS
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean)

  if (origin && !allowedOrigins.includes(origin)) return null

  return {
    'Access-Control-Allow-Origin': origin ?? allowedOrigins[0],
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    Vary: 'Origin',
  }
}

function json(body: unknown, status: number, headers: Record<string, string>) {
  return Response.json(body, {
    status,
    headers: { ...headers, 'Cache-Control': 'no-store' },
  })
}

function isRateLimited(request: Request, articleId: string) {
  const ip = request.headers.get('CF-Connecting-IP') ?? 'unknown'
  const key = `${ip}:${articleId}`
  const now = Date.now()
  const entry = rateLimits.get(key)

  if (!entry || entry.resetAt <= now) {
    rateLimits.set(key, { requests: 1, resetAt: now + RATE_LIMIT_WINDOW_MS })
    return false
  }

  entry.requests += 1
  return entry.requests > RATE_LIMIT_MAX_REQUESTS
}

export default {
  async fetch(request, env): Promise<Response> {
    const headers = corsHeaders(request, env)
    if (!headers) return new Response('Forbidden', { status: 403 })
    if (request.method === 'OPTIONS') return new Response(null, { headers })

    const url = new URL(request.url)
    const match = url.pathname.match(/^\/v1\/views\/([^/]+)$/)
    if (!match) return json({ error: 'Not found' }, 404, headers)

    const articleId = decodeURIComponent(match[1])
    if (!validArticleId.test(articleId)) {
      return json({ error: 'Invalid article identifier' }, 400, headers)
    }

    if (isRateLimited(request, articleId)) {
      return json({ error: 'Too many requests' }, 429, headers)
    }

    if (request.method === 'GET') {
      const row = await env.DB
        .prepare('SELECT views FROM article_views WHERE article_id = ?')
        .bind(articleId)
        .first<ViewRow>()

      return json({ views: row?.views ?? 0 }, 200, headers)
    }

    if (request.method === 'POST') {
      const result = await env.DB
        .prepare(
          `INSERT INTO article_views (article_id, views, updated_at)
           VALUES (?, 1, CURRENT_TIMESTAMP)
           ON CONFLICT(article_id) DO UPDATE SET
             views = views + 1,
             updated_at = CURRENT_TIMESTAMP
           RETURNING views`,
        )
        .bind(articleId)
        .run<ViewRow>()

      return json({ views: result.results[0].views }, 200, headers)
    }

    return json({ error: 'Method not allowed' }, 405, headers)
  },
} satisfies WorkerHandler<Env>
