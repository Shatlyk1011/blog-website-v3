---
title: "Web Storage - Cookies vs. Local Storage vs. Session Storage vs. IndexedDB"
slug: web-storage
date: "2025-09-20T12:29:44Z"
description: "A comparison of cookies, Local Storage, Session Storage, and IndexedDB, with guidance on when to use each browser storage option."
tags: ["browser", "web-development"]
mins: 7
aliases:
  - /blog/web-storage/
  - /dev/web-storage/
  - /thoughts/web-storage/
cover: cover.webp
---
## Overview

Storing data on the client side is essential for creating seamless user experiences. Whether it's remembering a user's login session, saving preferences, or handling large datasets for offline functionality, choosing the right storage mechanism can make or break your application's performance and security.

In this blog post, we'll dive into four popular web storage options: `Cookies`, `Local Storage`, `Session Storage`, and `IndexedDB`. We'll explore how each works, their pros and cons, key differences, and real-world examples. By the end, you'll have a clear understanding of when to use each one.

### Cookies

Cookies are one of the oldest ways to store data in the browser. The browser can store cookies, create new cookies, modify existing ones, and send them back to the server with later requests. Let’s break down what they are, how they function, and why they’re still important in an era of JWTs, localStorage, and sophisticated APIs.

#### What Are Cookies?

Cookies are small pieces of data stored in the browser and exchanged between client and server. They help websites keep track of data between page loads across multiple requests — something HTTP itself doesn’t provide. For users, this means not having to log in again every time. For developers, it’s an easy way to persist identifiers, preferences, and sessions.

#### How Cookies Work

- Server to Client – When the server wants to store some data in the browser, it uses the `Set-Cookie` header in an HTTP response.

- Client to Server – On the later requests, the browser automatically includes the cookie in the Cookie header.

- JavaScript Access (Optional) – On the client-side, cookies are accessible via `document.cookie[key]`, unless flagged as HttpOnly.

Cookies are best suited for small, essential data (like tokens, IDs, and preferences), rather than large chunks of data. Browsers usually allow a few hundred cookies with ~4KB of maximum size for per cookie.

Cookies can expire with the session - deleted once the browser closes or persist long-term - Controlled via `Expires` or `Max-Age` attributes.

Here is an example with date expire. When the date passes, the browser deletes it automatically.

```js
let date = new Date()
// Set cookie for 7 days
date.setDate(date.getDate() + 7)
document.cookie = `rememberMe=true; expires=${date.toUTCString()}`
```

Think of cookies as small sticky notes in the browser. They’re reliable for remembering sessions and preferences but not made for storing big chunks of data. If you want to store large data, use `localStorage` or `indexedDB`.

#### Security

While JavaScript can create cookies, the most secure ones (HttpOnly, Secure, SameSite) must be set from the server — you can’t add those flags via `document.cookie`.

```js
res.cookie('sessionId', 'qwerty123', {
  httpOnly: true,
  secure: true,
  sameSite: 'Strict',
})
```

This means [malicious scripts](https://en.wikipedia.org/wiki/Cross-site_scripting) touching `document.cookie` won’t see your session token.

#### Local Storage

Modern web apps need ways to store data in the browser. One of the simplest and most widely used APIs for this is LocalStorage. Unlike cookies, it’s not automatically sent with every request to the server, making it ideal for client-side persistence.

LocalStorage is part of the [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage). It stores data as strings and ties that data to the origin (protocol + domain + port). It’s `synchronous`, meaning each read/write blocks execution until it’s done, but it’s fast enough for small to medium data.

```js
// Store a value (key, value)
localStorage.setItem('theme', 'dark')

// Get a value (key)
console.log(localStorage.getItem('theme')) // 👉 "dark"
```

> LocalStorage can hold 5MB of data for per site origin.

Unlike cookies, LocalStorage items don’t expire automatically — they stay saved until you remove them in code, the user clears their browser data, or the session ends in incognito/private mode.

```js
// Save a value
localStorage.setItem('username', 'Alice')

// Remove just one key
localStorage.removeItem('username')
console.log(localStorage.getItem('username')) // 👉 null

// Remove all keys at once
localStorage.clear()
```

You can think of LocalStorage as a personal locker in the browser — it’s big enough for app data and preferences, stays around for long periods, and is quick and easy to use. LocalStorage works best for storing app state, user preferences, and cached data

#### Security

LocalStorage follows the [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) - only the same domain can access the data.

> Do NOT store sensitive data (auth tokens, passwords) in LocalStorage — **it’s fully accessible to JavaScript and any XSS vulnerability.**

#### Pros

LocalStorage is easy to use with its simple setItem/getItem API. It provides much larger space (about 5–10MB compared to cookies’ 4KB), performs better since data isn’t sent to the server, and works well for caching.

#### Cons

However, it has downsides — operations are `synchronous` and can slow things down if used heavily, it only stores `strings` so objects need **JSON conversion**, it has no built-in expiration system, and because it’s accessible to JavaScript, it isn’t safe for storing sensitive information.

#### Session Storage

Session Storage is similar to Local Storage but with a shorter lifespan, making it ideal for **temporary data**. It lives only as long as the browser tab or window is open. It’s great for cases where you want to keep state within a tab but don’t need it after the user closes it.

Session Storage works almost the same way as LocalStorage: it stores key-value pairs (as strings) that can be set and retrieved with `setItem` and `getItem`.

The Difference is "The data stays there after reload, but disappears when the tab or window closes."

```js
// Save data for the session (key, value)
sessionStorage.setItem("tabId", "12345");

// Read it back (key)
console.log(sessionStorage.getItem("tabId")); // 👉 "12345"

// Remove it
sessionStorage.removeItem("tabId");

```

> `SessionStorage` and `LocalStorage` share the same 5MB of data for per site origin.

#### Security

SessionStorage follows the [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) - only the same domain can access the data.

#### Pros

Session Storage is separate for each tab, so data doesn’t conflict across tabs. It also `clears automatically` when the tab closes, making it great for temporary state like form inputs or filters.

#### Cons

The drawback is that data is lost when the tab closes, so it’s not for long-term use. It also has the same limits as LocalStorage — `synchronous` and string-only.

### IndexedDB

When you need to store large or complex data in the browser — `IndexedDB` is the way to go. It’s a full-fledged database inside the browser, designed for handling structured data efficiently.

IndexedDB allows much larger storage than cookies or LocalStorage: 10GB+ for IndesxedDB ( varies 10–60% of available disk space).

Just like LocalStorage, IndexedDB data is persistent — it survives page reloads and browser restarts, follows the [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) so each site has its own database, and remains stored until the user manually clears it through settings or a cache wipe.

YouTube Premium demonstrates IndexedDB in action, storing downloaded videos as binary blobs for **offline** viewing in the browser.

```js
// Open (or create) a database
let request = indexedDB.open('MyDB', 1)

// Run when DB is created or version changes
request.onupgradeneeded = function (e) {
  let db = e.target.result
  let store = db.createObjectStore('users', { keyPath: 'id' })
  store.createIndex('name', 'name', { unique: false })
}

// On success event
request.onsuccess = function (e) {
  let db = e.target.result

  // Add a record
  let tx = db.transaction('users', 'readwrite')
  let store = tx.objectStore('users')
  store.add({ id: 1, name: 'Alice', age: 25 })

  tx.oncomplete = () => console.log('User added ✅')
}
```

### Comparison table

| Feature | Cookies | Local Storage | Session Storage | IndexedDB |
|--------|---------|---------------|-----------------|-----------|
| **Size Limit** | ~4KB per cookie | 5–10 MiB per origin | 5–10 MiB per origin | Up to 10–60% of disk |
| **Persistence** | Session or set expiration | Across sessions | Tab/session only | Across sessions |
| **Access** | Client & Server | Client only | Client only | Client only |
| **Data Type** | Strings | Strings (JSON for objects) | Strings (JSON for objects) | Structured objects/blobs |
| **Sent with Requests** | Yes | No | No | No |
| **Async/Sync** | Sync | Sync | Sync | Async |
| **Use Case** | Sessions, tracking | Persistent preferences | Temporary tab data | Large/offline data |


## Summary

#### Cookies

- Oldest storage mechanism; exchanged between client & server with each request.
- Ideal for small data (sessions, tokens, preferences).
- ~4KB per cookie limit, automatically sent to server.
- Support secure flags: HttpOnly, Secure, SameSite.
- Best for: authentication sessions, persistent login, user tracking.

#### Local Storage

- Part of Web Storage API, stores up to 5–10MB per origin.
- Data persists until manually removed (or browser cleared).
- Stores strings only; requires JSON for objects.
- Not secure for sensitive info (accessible to JavaScript, XSS risk).
- Best for: user preferences, cached app data, UI state.

#### Session Storage

- Works like LocalStorage, but tied to a single browser tab/session.
- Data clears automatically when the tab/window closes.
- 5MB limit and string-only, synchronous API.
- Best for: temporary data like form inputs, filters, or in-progress state.

#### IndexedDB

- A full client-side database for structured or large data.
- Storage quota in gigabytes (10GB+ depending on disk space).
- Asynchronous API, supports objects, files, and binary data.
- Persistent data, survives reloads and restarts.
- Best for: offline apps, large datasets, media storage (e.g., downloaded videos).
