---
title: "50 short programs in Rust, #6 - xscreensaver"
published_date: "2020-04-13 11:02:18 +0000"
layout: default.liquid
is_draft: false
---
In Coders at Work, jwz talks about writing screensavers for fun ("They make this neat result and you don't have to think about them too much. They don't haunt you."). I've wanted to try writing one since I read that, and I finally got around to it this weekend.

I drew on examples at <http://www.dis.uniroma1.it/~liberato/screensaver/> and <https://rosettacode.org/wiki/Window_creation/X11#C>, and ported it to Rust. For generating the actual graphics, I write a Game of Life implementation.

The code is at <https://github.com/rkday/50-short-programs-in-rust/tree/master/xscreensaver-game-of-life>.

Here's a screenshot:

![Game of Life screensaver](/static/images/game_of_life.png)

The main lessons here were:

- writing a screensaver is actually pretty straightforward - you get a window ID from the $XSCREENSAVER_WINDOW environment variable and draw on that, instead of drawing on a window you create yourself, but otherwise it's a normal X11 program.
- interfacing with C libraries from Rust is a bit fiddlier but also fairly straightforward - most of the difficulty is in finding things like `std::mem::MaybeUninitialized` which reproduce normal C behaviour.
- watching a Life simulation unfold is surprisingly interesting!
