---
title: "50 short programs in Rust, #3 - simulating a hash collision attack"
published_date: "2019-10-16 22:17:40 +0000"
layout: default.liquid
is_draft: false
---

_(I'm writing 50 short programs in Rust, often ones I would normally write in Python, to improve my fluency - starting [here](http://rkd.me.uk/posts/2019-10-07-50-short-programs-in-rust-1.html))._

One of my team asked me why Python sets don't have a stable ordering over different runs (but do within the same run):

```
$ python3 -V                                                                  
Python 3.7.4
$ python3 -c 'print(set("hello world")); print(set("hello world"));'
{'o', ' ', 'l', 'd', 'e', 'r', 'h', 'w'}
{'o', ' ', 'l', 'd', 'e', 'r', 'h', 'w'}
$ python3 -c 'print(set("hello world")); print(set("hello world"));'
{'e', 'd', 'o', 'r', ' ', 'w', 'h', 'l'}
{'e', 'd', 'o', 'r', ' ', 'w', 'h', 'l'}
```

The answer is in the [Python Language Reference](https://docs.python.org/3.8/reference/datamodel.html?highlight=data#object.__hash__):

```
By default, the __hash__() values of str and bytes objects are “salted” with an
unpredictable random value. Although they remain constant within an individual
Python process, they are not predictable between repeated invocations of Python.

This is intended to provide protection against a denial-of-service caused by
carefully-chosen inputs that exploit the worst case performance of a dict
insertion, O(n^2) complexity.
See http://www.ocert.org/advisories/ocert-2011-003.html for details.
```

I wanted to illustrate the kind of attack they describe (which has a lot more detail at <https://www.cs.auckland.ac.nz/~mcw/Teaching/refs/misc/denial-of-service.pdf>), so I wrote a short program - initially in Python, but per the theme of these blog posts, I then ported it to Rust.

```rust
use bencher::Bencher;
use bencher::{benchmark_group, benchmark_main};
use std::collections::HashSet;
use std::hash::{Hash, Hasher};

#[derive(Eq, PartialEq)]
struct BadHashable {
    x: u32,
}

impl BadHashable {
    fn new(x: u32) -> BadHashable {
        BadHashable { x }
    }
}

impl Hash for BadHashable {
    fn hash<H: Hasher>(&self, state: &mut H) {
        state.write_u32(8);
    }
}

#[derive(Eq, PartialEq)]
struct GoodHashable {
    x: u32,
}

impl GoodHashable {
    fn new(x: u32) -> GoodHashable {
        GoodHashable { x }
    }
}

impl Hash for GoodHashable {
    fn hash<H: Hasher>(&self, state: &mut H) {
        state.write_u32(self.x);
    }
}

fn insert_good_hashables_1k(bench: &mut Bencher) {
    bench.iter(|| {
        let mut myset = HashSet::new();
        for x in 0..1000 {
            myset.insert(GoodHashable::new(x));
        }
    })
}

fn insert_bad_hashables_1k(bench: &mut Bencher) {
    bench.iter(|| {
        let mut myset = HashSet::new();
        for x in 0..1000 {
            myset.insert(BadHashable::new(x));
        }
    })
}

fn insert_good_hashables_4k(bench: &mut Bencher) {
    bench.iter(|| {
        let mut myset = HashSet::new();
        for x in 0..4000 {
            myset.insert(GoodHashable::new(x));
        }
    })
}

fn insert_bad_hashables_4k(bench: &mut Bencher) {
    bench.iter(|| {
        let mut myset = HashSet::new();
        for x in 0..4001 {
            myset.insert(BadHashable::new(x));
        }
    })
}

benchmark_group!(
    benches,
    insert_good_hashables_1k,
    insert_bad_hashables_1k,
    insert_good_hashables_4k,
    insert_bad_hashables_4k,
);
benchmark_main!(benches);
```

It defines two structs - GoodHashable, where every value hashes differently, and BadHashable, where every instance hashes to the same value (to simulate the oCERT-2011-003 problem of picking a lot of strings which all hash to the same value). It then compares the performance of creating a set with 1,000 and 4,000 elements of each type:

```
Running target/release/deps/hashing-560306a13e73a6c4

running 4 tests
test insert_bad_hashables_1k  ... bench:   1,249,581 ns/iter (+/- 214,227)
test insert_bad_hashables_4k  ... bench:  19,094,799 ns/iter (+/- 1,839,946)
test insert_good_hashables_1k ... bench:      62,894 ns/iter (+/- 25,982)
test insert_good_hashables_4k ... bench:     247,982 ns/iter (+/- 68,617)

test result: ok. 0 passed; 0 failed; 0 ignored; 4 measured
```

Not only is BadHashable much slower, but it scales worse - inserting 4,000 items in a set is 16x slower than inserting 1,000 (i.e. O(n^2) complexity) whereas the difference is only 4x for GoodHashable (i.e. O(n) complexity).

For comparison, my Python version:

```python
import time

class GoodHashable:
    def __init__(self, x):
        self.x = x

    def __hash__(self):
        return self.x

    def __eq__(self, other):
        return other.x == self.x

class BadHashable:
    def __init__(self, x):
        self.x = x

    def __hash__(self):
        return 8

    def __eq__(self, other):
        return other.x == self.x

def time_it(cls, entries):

    start = time.time()

    myset = set()

    for x in range(entries):
        myset.add(cls(x))

    return time.time() - start

good = time_it(GoodHashable, 1000)
bad = time_it(BadHashable, 1000)
bad2 = time_it(BadHashable, 4000)

good2 = time_it(GoodHashable, 4000)
print("Normal case took {} ms, worst case {} ms, {}x difference".format(
          good * 1000, bad * 1000, bad/good))
print("Bad case took {}x longer with 4x more input".format(bad2/bad))
print("Normal case took {}x longer with 4x more input".format(good2/good))
```

P.S. I also wrote a short program to check that Rust protects against this attack in the same way as Python, and it does:

```rust
use std::collections::HashSet;

fn main() {
    let mut hs = HashSet::new();
    hs.insert("shinji");
    hs.insert("asuka");
    hs.insert("rei");
    hs.insert("misato");
    hs.insert("ritsuko");
    println!("{:?}", hs);
}
```

```
$ ./target/debug/hash_speed_demo                                                  
{"rei", "ritsuko", "shinji", "asuka", "misato"}
$ ./target/debug/hash_speed_demo
{"shinji", "misato", "asuka", "rei", "ritsuko"}
$ ./target/debug/hash_speed_demo
{"misato", "shinji", "ritsuko", "rei", "asuka"}
```
