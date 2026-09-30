---
title: "JavaScript Fundamentals for Frontend Development"
slug: javascript-fundamentals-for-frontend-development
date: "2025-05-03T15:16:36Z"
description: "A practical introduction to the JavaScript fundamentals every frontend developer should understand."
tags: ["javascript", "frontend-development"]
mins: 3
aliases:
  - /blog/javascript-fundamentals-for-frontend-development/
  - /dev/javascript-fundamentals-for-frontend-development/
  - /thoughts/javascript-fundamentals-for-frontend-development/
cover: cover.webp
---
Javascript uses concepts that can feel confusing. Let’s break down some of the most essential ideas.


### Type Coercion

**Coercion** - is when JavaScript automatically changes one type to another during operations—like mixing apples and oranges, but the code tries to make them work together. It can be helpful but sneaky, leading to surprises if you're not careful.

```js
let result = 'Price: ' + 100 // Number 100 becomes a string, output: "Price: 100"

let sum = '5' - 2 // String "5" becomes a number, output: 3
```

> But: "5" + 2 gives "52," not 7. Learn more about it [here](https://javascript.info/type-conversions)

### Scope

Scope is like a fence around your variables—it decides where they can be seen and used in your code. Without it, everything would be chaotic. There are **three** types of scope: global scope (available anywhere in the code - `window` object), function scope (inside a function only), and block scope (inside curly braces {} like in `if` statements, using `let` or `const`). This keeps your code organized and secure.

```js
function calculateTax(price) {
  let tax = price * 0.1 // This 'tax' is visible only inside this function
  return tax
}
console.log(tax) // Error! Can't see 'tax' out here—it's scoped to the function
```

### Closures

A closure is like a backpack 🎒 that a **function carries**, holding onto variables from its "home" (outer function) even after the home is gone. It's great for keeping data private, like a secret pocket.

```js
function makeCounter() {
  let count = 0 // The 'secret' in the backpack 🎒
  return function () {
    // Inner function with access to count
    count++ // Changes the outer variable
    return count
  }
}
let counter = makeCounter()
console.log(counter()) // 1
console.log(counter()) // 2  (Remembers the last count!)
```

### `this` keyword

`this` is like a pointer saying, "Me!"—it refers to the object that's currently running the code. It changes depending on how you call the function, which can be tricky at first, like a chameleon.

**Example**: In an object, `this` means the object itself.

The value of `this` depends on how the function is called.

- If this is used in the global object, the value of this is `window` object (but if strict mode is used, the value is undefined).
- In most cases, the value of `this` is the object to **the left of the dot** (the left rule of `this`).
- If a function is an arrow function, it ignores all the above rules and obtains the value of `this` from the lexical environment during its creation.
- If `call`, `apply`, or `bind` are used to create or call a function, `this` inside the function is the object passed as an argument.

**Example 1**

```js
let User = {
  name: 'Alice',
  greet: function () {
    console.log('Hello, ' + this.name) // 'this' is User object
  },
}
User.greet() // "Hello, Alice"
```

**Example 2**

```js
const Person1 = {
  name: 'Alice',
  greet: function () {
    console.log('Hello, ' + this.name)
  },
}

const Person2 = {
  name: 'Bob',
}

// change the context of `this` by binding the Person2 object
const greetPerson2 = Person1.greet.bind(Person2)

greetPerson2() // Output: Hello, Bob
```

**Explanation:**

- `Person1` has a method `greet` that uses `this.name`.
- `bind(Person2)` **creates a new function** `greetPerson2` where `this` is permanently set to Person2.
- Calling `greetPerson2()` uses `Person2`'s context, printing "Hello, Bob".

### Object-Oriented Programming in JavaScript

OOP is like building with Lego blocks: you create blueprints - **classes or prototypes** for objects that can inherit traits, making code reusable. It's for organizing bigger projects.

####  Prototypes

Prototypes are like family trees—objects inherit methods (actions) from a parent prototype, saving space by sharing.

```js
function Person(name) {
  this.name = name // Unique to each person
}
Person.prototype.greet = function () {
  // Shared action
  return 'Hi, ' + this.name
}
let Nick = new Person('Nick')
console.log(Nick.greet()) // "Hi, Nick"
```

### Arrow Functions vs Normal Functions

Arrow functions are shorthand versions of normal functions, like quick notes vs full letters. The big difference: arrows **don't have their own** `this` — they borrow from surroundings, which is handy in some spots but not others.

```js
let obj = {
  value: 10,
  normal: function () {
    setTimeout(function () {
      console.log(this.value)
    }, 100)
  },
  arrow: function () {
    setTimeout(() => {
      console.log(this.value)
    }, 100)
  },
}

console.log(obj.normal()) // Undefined — wrong 'this' context
console.log(obj.arrow()) // 10—borrows obj's 'this'
```

### Promises

Promises are like "I Owe You" for code that takes time (async) — they promise a result later, either success (resolve) or fail (reject). Chain them with `.then()` for the next steps.

```js
let promise = new Promise((resolve, reject) => {
  console.log('thinking...')
  setTimeout(() => {
    return resolve('Done!')
  }, 2000) // Wait 2 seconds
})
promise.then((result) => console.log(result)) // "Done!"
```

## Summary

- Scope: Fences variables; global everywhere, function/local hidden; prevents messes.
- Closures: Functions remember outer stuff; like private backpacks; useful for states.
- `this` Keyword: Points to current object; changes with call; watch in events.
- OOP: Blueprints with prototypes/classes; inherit to reuse; methods are actions.
- Arrow vs Normal: Arrows short, share `this`; good for quick anon funcs.
- Promises: Handle waits; resolve/reject; chain for steps.
