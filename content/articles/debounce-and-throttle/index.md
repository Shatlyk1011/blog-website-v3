---
title: "Debounce and Throttle. Step-by-Step Guide"
slug: debounce-and-throttle
date: "2025-06-07T15:16:36Z"
description: "Learn how debouncing and throttling work in JavaScript, with a detailed implementation and line-by-line explanation."
tags: ["javascript", "performance", "frontend-development"]
mins: 4
aliases:
  - /blog/debounce-and-throttle/
  - /dev/debounce-and-throttle/
  - /thoughts/debounce-and-throttle/
cover: cover.webp
---
## What is Debouncing?

Debouncing is a technique that ensures a function is only **executed after a certain period of inactivity**.

### Debounce implementation (snippet)

Let's implement our reusable debounce function.

```js
function debounce(func, delay) {
  let timeoutId

  return function (...args) {
    clearTimeout(timeoutId)

    timeoutId = setTimeout(() => {
      func.apply(this, args)
    }, delay)
  }
}
```

### Code Explanation

- The `debounce()` function takes two parameters:

  - `func`: The function to debounce (e.g., a function that makes an API call or logs a message).

  - `delay`: The delay (in milliseconds) to wait before executing `func`.

- Closure: The `timeoutId` variable is declared in the outer scope of debounce to persist across multiple calls to the returned function.

  - `timeoutId` stores the ID of the `setTimeout` timer, which can be used to **cancel** the timer if the debounced function is called again before the delay expires.

- The debounce function returns a new function that wraps `func` argument. This wrapper handles the debouncing logic.

- The returned function uses the spread operator to capture any arguments passed to it. These arguments will be forwarded to `func` when it’s executed.

- clearTimeout(timeoutId): If the debounced function is called multiple times within the `wait` period, the `clearTimeout()` function will be called to cancel upcoming execution, and the new `timeoutId` will be settled.

- The `apply` method in a `debounced` function ensures that the `this` context inside the original function `func` matches the current context of the debounced function when it executes.

### Real-World example

Imagine typing in a search bar on a website. As we type, the website might send API requests to fetch search results. Without debouncing, every keystroke could trigger a request, overwhelming the server. With debouncing, the request is sent only after we stop typing for, say, 300 milliseconds. This reduces the number of function calls and improves performance.

<div className="h-[1px] w-full bg-neutral-300 dark:bg-neutral-700"></div>

## What is Throttling?

Throttling is a powerful technique which **limits** how often a function can be called within a time frame. It’s like putting a speed limit on a function to prevent it from running too frequently, which is especially useful for optimizing web performance and ensuring smooth user experiences.

### How Throttling Works

Throttling works by wrapping a function with a mechanism that tracks the **last time it was executed**. If the function is called again before a specified delay has passed, the call is **ignored**. Once the delay expires, the function can run again

### Throttle implementation (snippet)

```js
function throttle(func, delay) {
  let isThrottle = false

  return function (...args) {
    if (!isThrottle) {
      func.apply(this, args)
      isThrottle = true
    }

    setTimeout(() => {
      isThrottle = false
    }, delay)
  }
}
```

### Code Explanation

- The throttle function takes two parameters:
  - `func`: the function to be throttled.
  - `delay`: The minimum time (in milliseconds) that **must pass** before `func` can be called again.
- It returns a new function that controls the execution of `func`.

- isThrottle: A `boolean` flag that tracks whether it’s in a "cooldown" period where further calls are ignored

- The returned function uses the rest parameter (...args) to accept any number of arguments, which will be passed to `func`.

  - It checks if `isThrottle` is false, and if so, it calls `func.apply(this, args)` to execute the original function with the provided arguments.

  - Sets `isThrottle = true` to indicate that the function is now throttled.

- Then, it sets a `setTimeout` that resets `isThrottle` to `false` after the specified `delay`. This allows the function to be called again once the `delay` period is over.

### Real-World Example

Imagine a webpage that fetches data from an API every time a user scrolls. Without throttling, scrolling could trigger hundreds of API requests in seconds, overloading the server and slowing down the site. By applying throttling, you can limit the function to execute, say, once every second, significantly reducing server load and improving performance.

## Summary

- **Debouncing**: Ensures a function executes only after a period of inactivity, reducing unnecessary calls.

- **Throttling**: Limits how often a function runs within a time frame, ensuring controlled execution.

- **Key Difference**: Debouncing waits for a pause; throttling ensures a fixed rate of execution.

- **Use Cases**: Debouncing for search inputs or form validation; throttling for scroll or resize events.

Both optimize performance by reducing function calls, enhancing user experience and server efficiency.
