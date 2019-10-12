---
title: "50 short programs in Rust, #1"
published_date: "2019-10-07 20:49:00 +0000"
layout: default.liquid
tags: ["50 short programs in Rust"]
is_draft: false
---
I'm at the point where I can read and write Rust (well, with a fair bit of help from the compiler), but I don't yet feel fluent in it and it doesn't feel completely natural. For example, I still reach for Python when I want to implement short programs to try out an idea.

I'd like to build my fluency in Rust by writing a lot of those programs - I've set a target of 50 - so that I improve my ability to write Rust quickly, and am aware of techniques and approaches for doing the sort of thing I want to do quickly. (Often these will be ports or reimplementations of programs I've previously written in Python.)

The one I'm going to start with is a program for accepting TCP connections and closing them immediately, and printing out a count of how many times it's done so. This can be quite useful for ferreting out bugs in TCP clients - if they have logic to reconnect when the connection drops, but don't have rate-limiting or delays on those connection attempts, this can trigger them to spin around connecting very fast and use a lot of CPU.

```rust
use std::net::TcpListener;
use std::time::SystemTime;

fn main() {
    let listener =
        TcpListener::bind("0.0.0.0:8006").expect("Could not bind to socket");
    let mut conncount = 0;
    let mut start = None;

    // Loop over incoming connections so that we accept them, but don't assign
    // them to a variable so that they immediately drop and are closed.
    for _ in listener.incoming() {
        conncount += 1;

        // It's more useful to know the time since our first connection, not
        // the time since the program started.
        if start.is_none() {
            start = Some(SystemTime::now());
        }

        let elapsed = start
            .unwrap()
            .elapsed()
            .expect("Could not get elapsed time!");
        println!(
            "{} connections in {}.{} seconds",
            conncount,
            elapsed.as_secs(),
            elapsed.subsec_millis()
        );
    }
}
```

This project is also on Github, at <https://github.com/rkday/50-short-programs-in-rust>.
