---
title: "50 short programs in Rust, #4 - raw sockets"
published_date: "2019-11-03 22:16:08 +0000"
layout: default.liquid
is_draft: false
---
In my last post, I showed a short C program I'd written to test `bind()` behaviour with `SOCK_RAW` sockets. I thought I'd try porting it into Rust:

```
use nix::sys::socket::*;

fn main() {
    let s = socket(
        AddressFamily::Inet,
        SockType::Raw,
        SockFlag::empty(),
        Some(SockProtocol::Udp),
    )
    .expect("Failed to get socket");
    let addr =
        SockAddr::new_inet(InetAddr::new(IpAddr::new_v4(127, 0, 0, 1), 15000));
    bind(s, &addr).expect("Failed to bind");
    println!("Bound successfully!");
}
```

It's nice that this is shorter and clearer than the C equivalent (no casting between the myriad `struct sockaddr` variants), but the tradeoff is that it takes longer to compile, especially when pulling the `nix` library in.

One potential other downside is that it's harder to repro and debug issues in a C/C++ program with a Rust repro - but in this case the issues are really about system call behaviour, and truss/strace can trace them in the same way across languages:

```
[root@freebsd ~/50-short-programs-in-rust/raw-bind]# PORT=15000 ./target/debug/raw-bind                                      
thread 'main' panicked at 'Failed to bind: Sys(EADDRNOTAVAIL)', src/libcore/result.rs:1084:5
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace.
[root@freebsd ~/50-short-programs-in-rust/raw-bind]# PORT=15000 truss ./target/debug/raw-bind 2> >(egrep "^(bind|socket)")
socket(PF_INET,SOCK_RAW,IPPROTO_UDP)             = 3 (0x3)
bind(3,{ AF_INET 127.0.0.1:15000 },16)           ERR#49 'Can't assign requested address'
[root@freebsd ~/50-short-programs-in-rust/raw-bind]# PORT=0 truss ./target/debug/raw-bind 2> >(egrep "^(bind|socket)")
socket(PF_INET,SOCK_RAW,IPPROTO_UDP)             = 3 (0x3)
bind(3,{ AF_INET 127.0.0.1:0 },16)               = 0 (0x0)
Bound successfully!
```
