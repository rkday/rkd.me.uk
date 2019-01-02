---
layout: default.liquid
title: London Clojurians - October 2013 Clojure Dojo
published_date: 2013-10-30 19:50:00 +0100
slug: oct-clojure
---

I was at the London Clojure Dojo last night, and worked on
[4clojure problem #146](http://www.4clojure.com/problem/146). I'm not
going to post my code - that feels like a violation of the spirit of
4clojure - but I am going to talk about a cool feature of the Clojure
'for' macro that I discovered while playing with this.

Let's say - as a different problem that shows off the same feature -
that you have a map where the keys are integers, and the values are
vectors of integers.

    user=> (def example-data-2 {1 [2 3 4 5] 6 [7 8 9 0]})
    #'user/example-data-2

Let's say that you want - for some reason - to turn this into a
sequence of each key multiplied by each element of its value.

    user=> (def target (list (* 1 2) (* 1 3) (* 1 4) (* 1 5) (* 6 7) (* 6 8) (* 6 9) (* 6 0)))
    #'user/target
    user=> target
    (2 3 4 5 42 48 54 0)

My first approach was to do a nested for loop - one to handle the
outer list and one to handle the inner list. This produced a list of
two lists, which between them contained the right values.

    user=> (for [[x subvector] example-data-2] (for [y subvector] (* x y)))
    ((2 3 4 5) (42 48 54 0))

I was able to join these lists with 'mapcat identity', though a fellow
dojoist pointed out that 'apply concat' also works:

    user=> (mapcat identity (for [[x subvector] example-data-2] (for [y subvector] (* x y))))
    (2 3 4 5 42 48 54 0)
    user=> (apply concat (for [[x subvector] example-data-2] (for [y subvector] (* x y))))
    (2 3 4 5 42 48 54 0)

There's a cleaner solution, though. 'for' can take multiple bindings,
and iterates through them together, producing a combinatorial result:

    user=> (for [x [1 2 3 4] y [1 2 3 4]] [x y])
    ([1 1] [1 2] [1 3] [1 4] [2 1] [2 2] [2 3] [2 4] [3 1] [3 2] [3 3] [3 4] [4 1] [4 2] [4 3] [4 4])

You can even use this to loop over something you destructured earlier
within the same 'for':

    user=> (for [[x subvector] example-data-2 y subvector] (* x y))
    (2 3 4 5 42 48 54 0)

In this example, x initially becomes 1 and subvector becomes
`[2 3 4 5]`, then y becomes each element of that in turn, so `(* x y)` is
`(* 1 2)`, `(* 1 3)`, and so on until `(* 6 0)` - matching the original definition of `target`.

This kind of multiple-level iteration is a pretty cool feature - it'll
be interesting to see if it's applicable to real problems, not just
4clojure
