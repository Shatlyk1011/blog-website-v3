---
title: "The Art of Video Optimization + Snippet"
slug: video-optimization
date: "2025-12-11T16:59:36Z"
description: "Discover expert techniques optimize Video files, slashing load times and boosting user experience without sacrificing quality."
tags: ["performance", "video", "frontend-development"]
mins: 3
aliases:
  - /blog/video-optimization/
  - /dev/video-optimization/
  - /thoughts/video-optimization/
cover: cover.webp
---
Video content has become essential for modern web applications — from product demos and tutorials to background animations and user-generated content. However, videos consume massive amounts of network bandwidth, often accounting for 60-80% of a page's total data transfer (mdn).

Optimizing video delivery - enhances web performance by reducing **load times** and **bandwidth** usage. Let's see how we can achieve these optimization


### Using `<video/>` and `<source/>` elements

The `<video>` element with `<source>` tags allows browsers to select the first compatible video format. Make sure to list `<source>` elements from **smallest** to **largest** file size so the browser could prioritize the most efficient version. 

```html
<video muted autoplay loop playsinline>
  <!-- Mobile -->
  <source media="(max-width: 480px)" src="videos/mobile.webm" />
  <source media="(max-width: 480px)" src="videos/mobile.mp4" />

  <!-- Tablet -->
  <source media="(min-width: 481px)" src="videos/tablet.webm" />
  <source media="(min-width: 481px)" src="videos/tablet.mp4" />

  <!-- Desktop -->
  <source media="(min-width: 1200px)" src="videos/desktop.webm" />
  <source media="(min-width: 1200px)" src="videos/desktop.mp4" />

  <!-- Fallback content -->
  <p>Your browser does not support video playback.</p>
</video>
```

### Code breakdown

* `muted` attribute ensures the video plays without sound.
* `loop` attribute repeats the video continuously.
* `playsinline` attribute allows inline playback on mobile devices.
* `autoplay` attribute enables automatic playback of media content.
* The browser selects the first `<source>` supports that matches the media query, ensuring smaller files are **prioritized** for smaller screens.
* `media` attribute control which video is loaded based on viewport size.

In the example above, we prioritize `.webm` over `.mp4` because the `.webm` format is generally smaller and more efficient.

To enable *automatic video playback* in browsers, ensure the video is **muted**. Otherwise, playback will start **only after user interaction** with the site. See chrome [autoplay policy](https://developer.chrome.com/articles/autoplay/#new_behaviors?ref=blog.shatlykabdullayev.com) for more info.

### Video Resizing with matchMedia API (code snippet)

The following code snippet allows you to dynamically load the appropriate video source based on viewport size using HTML `<source>` elements and JavaScript media query listeners for optimal performance and responsiveness..

```js
function handleVideoResize(videoElement) {
  const sources = Array.from(videoElement.getElementsByTagName('source'))

  const updateVideo = () => {
    videoElement.load()
  }

  updateVideo()

  const mqls = sources
    .filter((source) => source.media)
    .map((source) => {
      const mql = window.matchMedia(source.media)
      mql.addEventListener('change', updateVideo)
      return mql
    })

  return () => {
    mqls.forEach((mql) => mql.removeEventListener('change', updateVideo))
  }
} 
```

#### How it works?

* Retrieves all `<source>` elements from the `<video>` element.
* Triggers `video.load()` to select the appropriate source based on current **media query** matches.
* Sets up `matchMedia` listeners for each source’s media attribute to reload the video when the viewport size changes.


### Using Mux for Video Delivery

For my [personal website](https://shatlykabdullayev.com/?ref=blog.shatlykabdullayev.com), I chose Mux to handle video optimization. It automatically converts uploads to **HLS** format and creates multiple quality variants for adaptive streaming

Videos only start loading when they appear on screen as users scroll down. This makes pages load faster and saves data. While videos load, I show blurred preview images so users don't see empty spaces

**The Result:** fast page loads, smooth playback, and a hands-off pipeline where Mux handles transcoding and CDN distribumatchMedia ion automatically.

### General Advices for video Optimization

* Replace decorative videos (eg: background videos) with animated **WebP** or **GIF** (70-90% smaller)
* Lower framerate where appropriate (30fps → 24fps)
* Use **FFmpeg** or similar tools for video compression
* Set `preload="none"` attribute for videos that not immediately visible on screen

## Summary

* **Using `<video/>` and `<source/>`**: Order sources smallest to largest with media queries. Prioritize WebM over MP4 and use muted for autoplay.
* **Dynamic Video Resizing**: matchMedia API automatically switches video sources on viewport changes for responsive playback.
* **Real-World Implementation**: Mux handles HLS conversion and adaptive streaming. Videos load on scroll with blurred placeholders.
* **General Tips**: Use WebP/GIF for backgrounds, reduce to 24fps, compress with FFmpeg, set preload="none", and use adaptive streaming.