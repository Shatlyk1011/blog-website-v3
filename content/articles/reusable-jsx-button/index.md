---
title: "Reusable Button component. Build Once, Use Everywhere."
slug: reusable-jsx-button
date: "2025-07-04T15:16:36Z"
description: "The Power of Reusable Buttons. We will create reusable button component written in JSX"
tags: ["react", "javascript", "frontend-development"]
mins: 2
aliases:
  - /blog/reusable-jsx-button/
  - /dev/reusable-jsx-button/
  - /thoughts/reusable-jsx-button/
cover: cover.webp
---
## Building a Reusable Button Component in React

Creating a reusable button component in React is a fundamental task for any developer aiming to streamline UI development. A well-designed button component can be used across multiple projects, saving time and ensuring consistency.

In this blog, we'll build a flexible React button component that supports different variants, sizes, and element types (button or anchor). I'll explain the code, highlight its reusability, and provide ready to use code snippet.

### Why is it important?

Buttons are a core part of any user interface, appearing in forms, navigation bars, links, and more. A reusable button component allows developers to:

- **Reduce repetitive code** by centralizing button logic.

- **Maintain consistent styling** across the application.

- **Easily customize buttons** with props for variants, sizes, and other functionality.

- **Support** both `<button>` and `<a>` elements for flexibility in navigation or actions.

> We use Tailwind version 4

### Key Features + Code Snippet

- **Variants**: Easily switch between primary, secondary, outline, and link stylings.

- **Sizes**: Choose between large (lg) and medium (md) out of the box. Expand easily to support more.

- **Polymorphic**: Render as either a standard `<button>` for actions or an `<a>` for links, with proper external link handling.

- **TypeScript Safety**: All props are type-checked, and required fields (e.g., href for `<a>`) are enforced.

- **Customizable**: Add more variants, sizes, or class overrides as your design system evolves.

#### Code Snippet

```jsx
import type { ButtonHTMLAttributes, AnchorHTMLAttributes, ReactNode, FC } from "react"

import { cn } from "@/shared/utils"

const buttonVariants = {
  primary: "text-gray-50 bg-cyan-700 hover:bg-cyan-800",
  secondary: "text-gray-50 bg-blue-700 hover:bg-blue-800",
  outline: "text-gray-50 border border-current hover:bg-gray-100 hover:text-gray-900",
  // learn more about tailwind groups: https://tailwindcss.com/docs/hover-focus-and-other-states#differentiating-nested-groups
  link: "group/link text-gray-100 ",
}

const buttonSizes = {
  lg: "px-4 py-3 rounded-none text-base ",
  md: "px-3 py-2 rounded-none text-sm ",
}

type CommonProps = {
  variant?: keyof typeof buttonVariants;
  size?: keyof typeof buttonSizes;
  classes?: string;
  children: ReactNode;
};

type ButtonProps = {
  element?: "button";
} & Omit<ButtonHTMLAttributes<HTMLButtonElement>, "className"> & CommonProps;

type AnchorProps = {
  element: "a";
  href: string;                // <-- required when using 'a'
  isExternal?: boolean;
} & Omit<AnchorHTMLAttributes<HTMLAnchorElement>, "className"> & CommonProps;

type Props = ButtonProps | AnchorProps;

const ContentWrapper = ({ children }: { children: ReactNode }) => (
  <span className="relative inline-block group-hover/link:underline group-hover/link:underline-offset-4">
    {children}
  </span>
);

const Button: FC<Props> = ({ variant = "primary", size = "lg", classes, element, children, ...rest }) => {
  const className = cn(
    "relative max-h-max leading-[0] inline-flex items-center font-semibold text-nowrap transition",
    buttonSizes[size],
    buttonVariants[variant],
    classes,
  )

  if (element === "a") {
    const { isExternal, ...anchorProps } = rest as AnchorProps
    return (
      <a
        {...anchorProps}
        className={className}
        target={isExternal ? "_blank" : undefined}
        rel={isExternal ? "noopener noreferrer" : undefined}
      >
        <ContentWrapper>
          {children}
        </ContentWrapper>
      </a>
    )
  }

  // Default: button
  const buttonProps = rest as ButtonProps
  return (
    <button {...buttonProps} type="button" className={className}>
      <ContentWrapper>
        {children}
      </ContentWrapper>
    </button>
  )
}

export default Button
```

**Check out my [YouTube video](https://www.youtube.com/watch?v=_-G7VTWqMfc&t) where I explain its functionality**

### Code Explanation

Let's break down the key parts of the code to understand how it achieves reusability and flexibility.

- The `buttonVariants` object defines three variants (you can add more): `primary`, `secondary`, and `tertiary`, each with specific classes. This object contains styles related to `colors`, `shadow`, `hover/focus` effects.

- The `buttonSizes` object defines two sizes (you can add more): `lg`, `md`. It contains styles related to dimensions and spacing `font-size`, `height`, `width`, `padding`, `border-radius` etc.

- **ContentWrapper** is a helper component designed to wrap the visible content (children) inside reusable `Button`, providing consistent styling for hover underline effects—especially important for the link variant.

## Summary

Here we build a truly reusable Button component using Tailwind. You only need to style once, and then reuse everywhere in your app. The code is type-safe, simple to drop in, and easy to extend when design needs change.
