---
title: "Speed Up Your Website. Tips for Better Web Performance"
slug: tips-for-better-performance
date: "2025-07-18T11:11:36Z"
description: "Learn how to make your website faster with easy-to-understand tips on Core Web Vitals, lazy loading, code splitting and rendering strategies."
tags: ["performance", "frontend-development"]
mins: 4
aliases:
  - /blog/tips-for-better-performance/
  - /dev/tips-for-better-performance/
  - /thoughts/tips-for-better-performance/
cover: cover.webp
---
## Tips for Better Web Experience

In this post, we’ll break down four key areas to improve your site’s speed: Core Web Vitals, lazy loading, code splitting, rendering strategies. Let’s dive in with simple explanations.

### Core Web Vitals metrics

Core Web Vitals are metrics that measure how fast a webpage loads, how quickly users can interact with it, and how visually stable it is. Optimizing these metrics will lead for better search rankings and a great user experience.

### Largest Contentful Paint (LCP): How Fast Your Page Loads

LCP measures how long it takes for the main content (like a big image or text block) to appear on the screen. A good LCP is under 1.2 seconds for desktop and 2.5 seconds for mobile.

#### How to Improve LCP

- **Optimize images**: Compress images to reduce file size. Tools like [Squoosh](https://squoosh.app/?ref=blog.shatlykabdullayev.com) can shrink images without losing quality.

- **Use a fast server**: Choose a reliable hosting provider with quick response times.

- **Reduce server delays**: Use a Content Delivery Network (CDN) to serve content from servers closer to your users.

### Cumulative Layout Shift (CLS): Keeping Your Page Stable

CLS measures how much your page’s layout shifts unexpectedly, like when an image loads up and moves content. A good CLS score is under 0.1.

### First Input Delay (FID)

FID checks how long it takes for your site to respond when a user clicks a button or link. A good FID is under 100 milliseconds

#### How to Improve CLS and FID

- **Set image sizes**: Always define `width` and `height` for images so the browser reserves space for them.

- **Avoid sudden content changes**: Don’t insert ads or pop-ups that shift the page after it loads.

- **Use [event delegation](https://javascript.info/event-delegation?ref=blog.shatlykabdullayev.com)**: Instead of adding event listeners to many elements, use a single listener on a parent element to handle interactions efficiently.

### Interaction to Next Paint (INP): How Fast Your Site Responds to Actions

INP measures how quickly your site responds to user interactions, (clicking, tapping, typing). It looks at the time from when a user interacts to when the page visually updates. A good INP is under 200 milliseconds.

#### How to Improve FID and INP

- **Minimize JavaScript**: Remove unused scripts or break them into smaller pieces.

- **Use browser optimizations**: Techniques like `defer` or `async` ([link](https://javascript.info/script-async-defer?ref=blog.shatlykabdullayev.com)) for JavaScript files. Let the browser load them without blocking user actions.

> Check out Google’s [PageSpeed Insights](https://pagespeed.web.dev/?ref=blog.shatlykabdullayev.com) to test your site’s Core Web Vitals


### Lazy Loading and Code Splitting

Load only the content users need **right away**. Two great techniques for this are **lazy loading** and **code splitting**.

**Lazy loading** delays loading images, videos, or other heavy content until they’re needed (like when a user scrolls down).

**Code splitting** breaks your JavaScript into smaller pieces so the browser only loads what’s needed for the current page.


#### How to implement

- **Use priority hints**: Add `fetchpriority` attribute to tell the browser which resources to load first.

- **HTML attribute**: Add `loading="lazy"` to images in your HTML. Most modern browsers support this.

- **Dynamic imports**: Use tools like Vite or Webpack to split code. For example, load a heavy charting library only when a user visits a data-heavy page. Frameworks like `React` or `Vue` have built-in code-splitting features.

### Rendering Strategies: Picking the Right Approach

Loading contents right affects page speed. Here is common strategies, explained simply, with examples from real projects.

#### Client-Side Rendering (CSR)

In CSR, the browser loads a basic page and uses JavaScript to fetch and display content (in client side). It’s great for **dynamic apps** but can be slow initially.

#### Server-Side Rendering (SSR)

SSR sends a fully built page from the server, making the first load faster. It’s good for SEO and speed but this can put a load on the servers.

#### Static Site Generation (SSG)

SSG creates pre-built pages at build time, making them super fast to load. It’s perfect for blogs or marketing sites.

#### Incremental Static Regeneration (ISR)

ISR combines SSG’s speed with the ability to update pages without rebuilding the whole site. It’s great for sites with frequent updates.

## Summary

- Focus on Core Web Vitals (LCP, FID, CLS, INP) to make your site fast, responsive, and stable.

- Use lazy loading, priority hints, and code splitting to load only what’s needed.

- Pick the right rendering strategy (CSR, SSR, SSG, or ISR) for your project.
