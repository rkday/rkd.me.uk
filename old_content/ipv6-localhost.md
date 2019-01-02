Title: Figuring out IPv6 localhost
Date: 2018-09-30 17:32
Category: Containers
Author: Rob Day
Slug: ipv6-localhost

Recently, I've been trying to make to easier to deploy the microservices I develop locally for testing - it's much more convenient (and faster) to do this (whether under Docker or just running the binaries directly) than it is to deploy them as EC2 virtual machines.

When I do this, I tend to use localhost addresses.

- they're fairly portable - I can hardcode them in tests and still expect the tests to run anywhere
- there's a broad range - all of 127.0.0.0/8 is localhost, so if I have two services that listen on the same port (and would be on different machines in production) I can give them 127.0.0.1 and 127.0.0.2 - or if I'm on a shared machine, I can have 127.1.0.0/16, someone else can have 127.2.0.0/16, etc.

(Docker is often a solution to these sort of portability and isolation problems, but not always - for example, cases where I'm already in a container and want to avoid multiple layers of Docker-in-Docker nesting, or where a Python test suite finds it easier to create and control multiple fake HTTP services directly as Python objects rather than as containers.)

When I tried to do the same thing with IPv6, though, I hit an issue - `::1` is the only defined IPv6 localhost address. `::2` isn't localhost, so I can't deploy services with clashing ports.

A bit of searching led me to [this draft RFC from 2013](https://tools.ietf.org/id/draft-smith-v6ops-larger-ipv6-loopback-prefix-04.html), proposing `1::/64` as a larger loopback prefix. Although it's only a draft, this seemed like a reasonable approach. Rolling it out requires one command to set up the routing:
