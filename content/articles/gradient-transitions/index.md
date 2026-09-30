---
title: "Creating Gradients with Transitions"
slug: gradient-transitions
date: "2025-05-14T15:16:36Z"
description: "Creating Smooth Gradient Transitions on :hover using CSS @property rule"
tags: ["css", "frontend-development"]
mins: 2
aliases:
  - /blog/gradient-transitions/
  - /dev/gradient-transitions/
  - /thoughts/gradient-transitions/
cover: cover.jpg
---
## Gradient Transitions with CSS `@property` Rule

Gradients are a powerful way to add visual flair to web elements, but transitioning them smoothly has always been tricky. CSS gradients are treated as images, so direct transitions between gradient states often result in abrupt changes rather than smooth animations.

Enter the CSS `@property` rule—a game-changer that lets us define custom, animatable properties to achieve gradient transitions.

In this blog, we’ll explore how to use `@property` to animate gradient colors on a button, complete with a real-world example.

<video
  className="w-full"
  src="/static/videos/gradient-buttons.mp4"
  muted
  autoPlay
  playsInline
  controls
/>

Let’s create a simple webpage with two buttons: one using a standard gradient transition (which won’t work as expected) and another using the `@property` rule for a smooth transition.

```html
<div class="box">
  <h2>Changing background gradient styles on hover</h2>
  <button class="btn btn-1">Hover Me</button>
</div>

<div class="box">
  <h2>Changing @property rule on hover</h2>
  <button class="btn btn-2">Hover Me</button>
</div>
```

### Styling the Buttons

Next, we style the buttons with a shared gradient background and define their hover behaviors in 2 different ways:

```css
@property --color-primary-one {
  syntax: '<color>';
  inherits: false;
  initial-value: #ff3d3e;
}

@property --color-primary-two {
  syntax: '<color>';
  inherits: false;
  initial-value: #ff6f00;
}

/* common styles with initial gradient color */
.btn {
  padding: 15px 30px;
  color: #ffffff;
  border-radius: 5px;
  background: linear-gradient(to right, var(--color-primary-one) 0%, var(--color-primary-two) 100%);

  cursor: pointer;
}

.btn-1:hover {
  /* this will not work as expected */
  background: linear-gradient(to right, #d63e76 0%, #b90041 100%);

  transition: all 0.3s ease-in-out;
}

.btn-2:hover {
  /* this will work */
  transition:
    --color-primary-one 0.3s ease-in-out,
    --color-primary-two 0.3s ease-in-out;

  --color-primary-one: #d63e76;
  --color-primary-two: #b90041;
}
```

- Base `.btn` class: Applies a gradient background using the custom variables `--color-primary-one` and `--color-primary-two`.

- `.btn-1:hover:` Attempts to transition the entire background property to a new gradient. This **won’t animate** smoothly because gradients are **treated as images**.

- `.btn-2:hover:` Transitions the custom variables `--color-primary-one` and `--color-primary-two` to new color values. Since these are animatable color properties, the gradient updates smoothly.

> The `@property` rule is supported in modern browsers like Chrome, Edge, and Safari. <br /> <br /> Visit [CanIUse](https://caniuse.com/?search=%40property) to check compatibility
> details for all features.

## Summary

Using the `@property` rule, you can create stunning gradient transitions that elevate your web designs. Try it out and make your buttons pop!
