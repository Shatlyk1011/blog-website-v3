---
title: "The Art of Image Optimization"
slug: image-optimization
date: "2025-10-05T15:16:36Z"
description: "Discover expert techniques to compress and optimize images, slashing load times and boosting user experience without sacrificing quality."
tags: ["performance", "images", "frontend-development"]
mins: 5
aliases:
  - /blog/image-optimization/
  - /dev/image-optimization/
  - /thoughts/image-optimization/
cover: cover.jpg
---
Did you know that 70% of download resources on average websites are **images** and **videos**? (mdn)

Web performance is critical for user satisfaction and engagement. One of the most effective ways to enhance website speed is through **image optimization** .

We’ll explore several key technique for image optimization.

### Using `srcset` and `loading` attributes

The `srcset` attribute is a powerful tool that allows developers to provide multiple image sources tailored to different screen pixel ratios or device resolutions. By serving the most appropriate image size based on the user’s device, `srcset` reduces unnecessary data transfer, leading to faster page loads and a better user experience.

```html
<img 
  src="/bg-1.png" 
  srcset="/bg-2x.png 2x" 
  loading="lazy" 
  alt="background image"
/>
```

#### Code breakdown

- The `src` attribute specifies the **default** image source - `/bg-1.png`. This is the fallback image used by browsers that don’t support `srcset` or when no other conditions match.
- The `srcset` attribute provides a comma-separated list of image sources along with their respective [pixel density](https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio).
- `/bg-2x.png 2x` is served for devices with higher pixel ratios. Here is `2x` indicates using this image source for higher pixel density screens, e.g., for Retina displays.
- `loading="lazy"` attribute enables lazy loading, a technique that defers the loading of images until they are about to enter the viewport. This reduces initial page load time by prioritizing content that is immediately visible to the user.

#### Why this important?

By offering different image resolutions, the browser selects the **most appropriate** image based on the device’s pixel density, reducing the loading of unnecessarily large files on lower-resolution screens.

### Using picture and source elements

The `<picture>` element is a modern HTML feature that allows developers to provide multiple image sources for different scenarios, enabling browsers to choose the most appropriate image based on factors like screen size, resolution, or device density. This flexibility is key to delivering optimized images that balance quality and performance.

```html
<picture>
  <source 
    media="(max-width: 1440px)"
    srcset="large-bg-1x.png 1x,
    large-bg-2x.png 2x" 
  />
  <source 
    media="(max-width: 600px)"
    srcset="small-bg-1x.png 1x,
    small-bg-2x.png 2x" 
  />
  <!-- fallback image -->
  <img 
    src="large-bg.png" 
    alt="background image" 
  />
</picture>
```

#### Code breakdown

- The `<picture>` element acts as a wrapper that contains one or more `<source>` elements and optional fallback `<img>` element.

- It gives the browser options to choose the best image source based on defined criteria, such as the viewport size or device characteristics.

- The first `<source>` provides `large-bg-1x.png 1x` and `large-bg-2x.png 2x` for viewports less than 1440 pixels `media="(max-width: 1440px)"`. Here are the sources with large images. Additionally, we're using `srcset` for various pixel densities.

- The second `<source>` provides `small-bg-1x.png 1x` and `small-bg-2x.png 2x` for viewports 600 pixels or less (media="(max-width: 600px)"). Here are the sources with small images. Additionally, we're using `srcset` for various pixel densities.

- The browser reads (from top to bottom) the source element conditions and selects the first matching `<source>` element to load the appropriate image. If no condition satisfies, the fallback `<img/>` will be used.

#### Why this important?

- By serving smaller images to devices with smaller viewports, we reduce the amount of data transferred. Smaller images mean faster load times, especially on mobile devices with limited bandwidth.

- Delivering appropriately sized images ensures that users see visuals tailored to their device’s screen size and resolution.

- Faster-loading pages improve key web performance metrics like Largest Contentful Paint (LCP) and First Contentful Paint (FCP), which are part of Google’s Core Web Vitals. Better scores can boost your site’s search engine rankings.

- The `<picture>` element supports art direction, allowing you to serve different image compositions (e.g., a close-up portrait for mobile vs. a wider shot for desktop). This ensures the image is visually optimized for each context, enhancing both aesthetics and performance.

> Why should I use the `<picture>` element for image optimization when built-in components like **Next Image** already provide image optimization features?

Next.js’s `<Image>` component, are tightly integrated with specific hosting platforms like Vercel. This convenience comes at a cost:

- Platforms like Vercel impose limits on image optimization usage, especially on free or hobby tiers. For example, Vercel’s free tier caps optimized images at 1,000 per month, which can be quickly exhausted for image-heavy sites, leading to broken images or the need to upgrade to a paid plan.

- Relying on a platform’s image optimization service can make it harder to migrate to another hosting provider without losing the benefits of automated optimization or needing to reconfigure your setup.

- Potential for Over-Optimization: Automated tools may overly compress images, leading to a noticeable loss in quality that can harm the visual appeal of your site, especially for high-resolution displays. Similarly, [Astro’s](https://docs.astro.build/en/guides/images/#default-image-service) default image optimization with Sharp may not allow for the same level of customization as manual optimization pipelines

_See browser supports for [picture](https://caniuse.com/picture) element._

### Use Modern Image Formats

New image formats like `.webp` make images smaller without losing quality. Smaller images mean faster loading and less data used by your users.

_See browser supports for [.webp](https://caniuse.com/webp) format._

### Always Add `alt` Text to Images

Alt text is a short description of the image. It helps people who can't see the image and also helps search engines understand your content. Big platforms like Instagram even use AI to automatically generate descriptions based on what's shown in the image.

### Tips for `<picture/>` element

To maximize the benefits of the `<picture>` element, use these tips:

- Use tools like TinyPNG, or Squoosh to compress images without losing quality. Here you can find good [resources](/articles/my-best-resources/#other-useful-sources)

- Test Responsiveness: Use browser developer tools to simulate different screen sizes and ensure the correct image is loaded.

## Summary

- **Image Optimization:** Use `srcset` to show the right image size for different devices and loading to delay loading off-screen images. The `<picture>` element helps pick the best image for the screen size to speed up page loads.

- **Tips:** Use tools like **TinyPNG** or **Squoosh** to shrink images, test how images look on different screens, and check browser support for better performance.
