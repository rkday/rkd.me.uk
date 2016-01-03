Title: Notes from the December 2013 Clojure eXchange
Date: 2014-01-07 22:10:07
Category: Code
Tags: clojure
Slug: clojure-xchange-2013
Author: Rob Day

Last month, I went to the Clojure eXchange in London (run by SkillsMatter). I've been meaning since then to write up my notes from the most interesting talks, so here goes. You can see all these talks (and others I've not mentioned) at http://skillsmatter.com/event/java-jee/clojure-exchange-2013.

## Speech Acts (@gigasquid)

This was basically a talk about speech acts and John McCarthy's Elephant 2000 paper , with a Parrot AR drone thrown in for a bit of robotic overlord interest.

The idea is that you have three types of speech acts:
- Assertions, which tell the listener that something is true
- Persuasion, which creates beliefs, which draw inferences from assertions
- Requests, which (if accepted) create a commitment and will be acted upon at a future time

In software terms:
- assertions set program state (in contrast to traditional 'assertions' which make a program fail if it's not true)
- persuasion sets conditional state - the program will believe something is true when something else is true
- requests create deferred actions - the program will do something when something else is true

The example given was something like this:

```
(assert sunny false)
(convince #nice-day "It's a nice day" #(= sunny true)) ; #nice-day is now true when sunny is true
(request *open-window when #nice-day #(println "Opened the window")) ; this commits the program to execute this println function when #nice-day is true
(assert sunny true) ; this sets sunny to true, which causes #nice-day to be true, which causes..
; => "Opened the window"
```

As a concept for structuring programs, I think it's really interesting - I can see it making program logic a lot more explicit. A lot of programs can be conceived of taking some external facts (assertions in this context, but input more generally), deriving state from them, and matching that state against its programmed commitments to decide what to do in a given case - expressing the derived state as "beliefs" in a human-readable framework could be a real aid to debugging.

[The Babar language](https://github.com/gigasquid/babar) is a Clojure-like language based around this concept of speech acts - though I think it's an interesting enough way of structuring programs that I'd use a Clojure/Python/Ruby library implementing these ideas. (That link also contains videos of babar-programmed drones, if you're interested.)

One final note - I like the idea of # and * as sigils to denote different types of variable. Perl was my first language, and the idea of encoding that sort of information in variable names has always stuck with me.

## Scala vs. Clojure (@dpp)

I have to admit that I'm not that interested in Scala - when I want a strongly typed FP language I'm going to learn Haskell - but this was a thought-provoking talk just because it made me think about what makes programming languages (and, by extension, other developer-oriented tools) good or bad.

One idea I liked was about being opinionated - that languages and frameworks become successful by making people follow successful patterns. Ruby on Rails is a good example here (because it forced people to write web apps in an object-oriented MVC style), and Clojure is more opinionated than Scala (in enforcing immutability and making the functional style much more natural than the object-oriented one). To some extent there's a risk there for designers - a language which isn't opinionated is more likely to be successful than one that's opinionated about the wrong things - but it feels like that's a typical tradeoff of risk versus reward.

The other thing to come out of this was a play on [Greenspun's Tenth Law](https://en.wikipedia.org/wiki/Greenspun%27s_tenth_rule) - "any sufficiently complicated Lisp program contains an ad hoc, informally-specified, bug-ridden, slow type system". In the light of libraries like Prismatic/schema (which I use and have contributed to) and core.typed (which I haven't), it's a pretty plausible rule.

Conversely, the fact that the Clojure community are gathering around a couple of core ways to do this (rather than just an ad-hoc implementation in every program) is promising - like how having specific libraries like GNU Guile to implement an embedded Lisp works around the original rule.

## Concurrency (@thattommyhall)

I found this talk really useful because it talked about the core.reducers library, which I'd heard about but not really come to grips with.

The main discussion was of the fold function, which is essentially a parallel reduce - it partitions the collection into 512 pieces, reduces each piece, and then combines the reductions with a combiner function. The combiner function has two rules:
- it must be associative (in the mathematical sense)
- calling it on its own must provide an identity

So + and * are both combiner functions:

```
user=> (+)
0
user=> (*)
1
```

There were two tips given for designing combiner functions. Firstly, you need to check that your combiner is associative. This kind of property-based testing is a good fit for generative testing (QuickCheck-style testing), and so clojure.test.generative is a useful sanity-check here.

The other is that reducers has a monoid function, which simplifies the requirement that your combiner function must provide the identity when called without arguments. monoid takes a function and an identity constructor, and returns a combiner, which returns the given identity when called with no arguments, and the result of the given function otherwise. So if the + function didn't already return 0 when called with no arguments, you'd just need to call (monoid + 0).

## The programming language as a musical instrument (@samaaron)

I found this talk interesting because it asked the question "what if programming was not considered a sub-discipline of engineering"? I'm finding that question particularly interesting at the moment because I'm reading Recoding Gender, about the early computer movement, women's participation in it, and how the different conceptualisations of programming affected that - so I'm going to talk about this train of thought more once I finish the book.
