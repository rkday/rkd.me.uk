Title: Learning Rust
Date: 2017-11-04 22:28:00
Category: Code
Tags: rust
Slug: learning-rust
Author: Rob Day

I've been learning [Rust](https://www.rust-lang.org) recently, and it's the first new language (with new concepts, like borrowing) I've learnt for a while - probably the first since Clojure in 2013. I thought it was worth writing up exactly what I'm doing to learn it, in the hopes that it's useful for others learning Rust and new programming languages in general.

## Code koans

https://github.com/crazymykl/rust-koans are a good, simple (but gradually increasing in complexity) introduction to Rust. I started learning Rust just by checking them out and working through them, looking up any topics I was unclear on in the Rust book (https://doc.rust-lang.org/book/second-edition/).

They start off with the basics, just dealing with true/false and integers, but cover borrowing and traits by the end. They're also all written as unit tests, which was useful in building up good unit testing habits in Rust - when I moved on to other projects I was alreadly familiar with the test syntax.

These aren't specific to Rust - see http://rubykoans.com/ or https://github.com/torbjoernk/CppKoans for examples in other languages.

## Code katas

The next thing I did after finishing the koans was to start working through http://codekata.com/. I really like this:

- I think writing decent amounts of actual code in a language is the best way to learn it.
- With the code katas, I don't have to choose a project, worry about picking the right one, etc. - they're all just laid out for me
- I don't run the risk of picking a project that's too large - they're pretty likely to be doable in an hour or so
- They're clearly just practice for educating myself, so I can focus on learning (including, for example, refactoring to get the best style) rather than just accomplishing a project I want to do.

I'm tracking the katas I'm doing at https://github.com/rkday/rust-katas.

As well as http://codekata.com/, useful things to do here include:

- https://www.codewars.com/
- https://github.com/gamontalvo/awesome-katas
- exercises from other programming introductory books - for example, [Clojure Programming](http://shop.oreilly.com/product/0636920013754.do) had an exercise about implementing the [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), which I think would be interesting to redo in Rust
- more generally, reimplementing small previous projects in Rust

## awesome-rust

https://github.com/rust-unofficial/awesome-rust is a curated list of rust projects and libraries.

This provides:

- a set of code to read and learn good practices from - for example, I'd like to read and understand all of https://github.com/alexcrichton/tar-rs at some point
- useful libraries, which might inspire further projects (or mean you feel able to do a project in rust which you'd otherwise have done in Python or C++, because there's a Rust library for it)
- awareness of the common libraries for the language (e.g. https://github.com/kbknapp/clap-rs for command-line argument parsing)

As with the koans, this isn't Rust-specific - see e.g. https://github.com/vinta/awesome-python.

## Other

- http://rustup.rs is worth mentioning here - it's the standard Rust installer
- clippy - this is a tool installable with `cargo install clippy`, and is a linter for Rust - it helps spot things which are valid but bad style (like an explicit `return x` instead of just having `x` be the last expression in a function).
- the Rust style guide at https://aturon.github.io/ is also useful for understanding idiomatic code
- StackOverflow questions - sorting the Rust questions by number of votes (https://stackoverflow.com/questions/tagged/rust?sort=votes&pageSize=15) lets me read answers about the topics most people find the most confusing, and reading lots of alternative explanations of things like borrowing and ownership gives me a better picture of how this works.
