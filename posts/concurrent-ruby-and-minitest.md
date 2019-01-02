---
layout: default.liquid
title: Concurrent-ruby and Minitest
published_date: 2014-12-07 21:22:00 +0100
slug: concurrent-ruby-and-minitest
---

I spent some time earlier today debugging an interesting interaction in Ruby between minitest/autorun and concurrent-ruby, and since none of my searches on it turned up quite the right answer, figured I'd write up my notes.

I'm currently writing a Diameter stack in Ruby, partly because I need a good Diameter test library for testing/fixing FHoSS issues, but also so that I can think about good library/API design. One of the features I've just added is to have the message-sending function return a Concurrent::Promise object that gets fulfilled with the answer - striking a nice middle ground between callbacks (which are hellishly complicated if you have a long scenario where each message depends on what came before it) and just returning the result (which means lots of blocking and inefficiency). But when I came to UT it, [this test](https://github.com/rkday/ruby-diameter/blob/762a53fc74d51c1567e0cbfee756c5371fa272ae/test/test_stack.rb#L91) failed with a deadlock:

```
Stack 2::A client DiameterStack with an established connection to 'bob'#test_0002_fulfils the promise when an answer is delivered:
fatal: No live threads left. Deadlock?
    /usr/share/ruby/thread.rb:72:in `sleep'
    /usr/share/ruby/thread.rb:72:in `block (2 levels) in wait'
    /usr/share/ruby/thread.rb:68:in `handle_interrupt'
    /usr/share/ruby/thread.rb:68:in `block in wait'
    /usr/share/ruby/thread.rb:66:in `handle_interrupt'
    /usr/share/ruby/thread.rb:66:in `wait'
    /home/rkd/.gem/ruby/gems/concurrent-ruby-0.7.1-x86_64-linux/lib/concurrent/atomic/condition.rb:43:in `wait'
    /home/rkd/.gem/ruby/gems/concurrent-ruby-0.7.1-x86_64-linux/lib/concurrent/atomic/event.rb:89:in `wait'
    /home/rkd/.gem/ruby/gems/concurrent-ruby-0.7.1-x86_64-linux/lib/concurrent/obligation.rb:55:in `wait'
    /home/rkd/rb_diameter/test/test_stack.rb:105:in `block (2 levels) in <top (required)c>'
```

Debugging this eventually led me to the conclusion that the code in my Promise wasn't getting run at all. I narrowed it down to this completely minimal testcase that failed:

```
require 'minitest/autorun'
require 'concurrent'

describe 'promises' do
  it 'works' do
    p = Concurrent::Promise.execute{ puts "Hi" }
    p.wait
  end
end
```

and this one, identical but for the minitest infrastructure, that passed:

```
require 'concurrent'

p = Concurrent::Promise.execute{ puts "Hi" }
p.wait
```

How bizarre. I could tell that there was some kind of interaction between concurrent-ruby and minitest, but I had no idea what and all my hypotheses seemed implausible (some code in concurrent-ruby that spots when you're in a test and spawns fewer background threads? some code in minitest that forces everything to happen on a single thread?). I couldn't find the immediate answer on the web (searching "minitest concurrent-ruby" or variations on that tended to come up with "how to make minitest run your tests concurrently"-style tips), but did eventually find the two bits of information I needed.

The first was <http://blog.arkency.com/2013/06/are-we-abusing-at-exit/>, which says:

"But here is the question: How can minitest run our test if the test is defined after we require minitest? You probably already know the answer: it uses at_exit hook to trigger test running"

The other was the concurrent-ruby's API docs, particularly <http://ruby-concurrency.github.io/concurrent-ruby/Concurrent/Configuration.html>:

```
Instance Attribute Summary

    - (Object) auto_terminate
    defines if executors should be auto-terminated in at_exit callback.

```

So that means:

* minitest/autorun works by running an at_exit callback that runs all the tests you've defined
* concurrent-ruby has an option that termminates all the background thread pools at exit (and it turns out that defaults to true)
* ...and I'm requiring minitest/autorun before concurrent-ruby, so minitest/autorun's at_exit callback triggers last
* ...so by the time my tests run and try to execute a Promise, the worker threads that would run that Promise code have been destroyed and it silently fails

One simple line added to my [minitest_helper.rb](https://github.com/rkday/ruby-diameter/blob/762a53fc74d51c1567e0cbfee756c5371fa272ae/test/minitest_helper.rb#L26) fixed that up:

```
# Compatibility with minitest/autorun
Concurrent.configuration.auto_terminate = false
```

Hopefully this is useful to anyone who hits similar issues in the future! I've also spotted <https://github.com/ruby-concurrency/concurrent-ruby/issues/192> (which wouldn't have fixed this, but would have meant I got an exception and thus a head start on debugging), and submitted a pull request to fix that.
