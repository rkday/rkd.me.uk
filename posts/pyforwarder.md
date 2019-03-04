---
title: "pyforwarder, a Python message forwarding library"
published_date: "2019-03-04 23:47:30 +0000"
layout: default.liquid
is_draft: false
---
[Preferring composition to inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance) is a nice design pattern, and one which makes it simpler to break functionality into independent classes that can then be brought together (without the complexities of multiple inheritance).

It does have downsides, though, and the main one for me is boilerplate - you have to write lots of short methods which simply forward a method call onto one of your class's members. Ruby has a really nice solution to this in the [Forwarder module](https://github.com/RobertDober/Forwarder), which lets you just write `forward_all :complaints, :problems, :tasks, to: :first_employee` and minimise that boilerplate.

Python3 is my primary scripting language at the moment, though, not Ruby, and as far as I know there isn't a good equivalent in Python - so I wrote one to see if I could. It's at <https://github.com/rkday/pyforwarder> (and <https://pypi.org/project/pyforwarder/>) and can be installed with `pip install pyforwarder`.

Once pyforwarder is installed and imported, you can do this:

```
from pyforwarder import forwarder

class Tail(object):
def wag(self, speed=5):
    """Hello world"""
    if speed > 10:
	print("Wagging tail very happily")
    else:
	print("Wagging tail")

@forwarder('_tail', target_class=Tail)
class Dog(object):
def __init__(self):
    self._tail = Tail()

rover = Dog()
rover.wag(speed=11)
```

The line `@forwarder('_tail', target_class=Tail)` auto-creates forwarding methods on Dog for all methods on Tail, which call the corresponding method on the `tail` attribute. It's also possible to do:

```
@forwarder('_tail', methods=['wag'], target_class=Tail)
```

to restrict the methods created.

In the latter case it's possible to omit `target_class`, i.e. `@forwarder('_tail', methods='wag'])` - but that makes it impossible to copy the docstring from `Tail.wag` to `Dog.wag`, so it's not really recommended. (I spent a reasonable amount of time making sure that docstrings and some function properties were copied, so that `help()` or tools like `pydoc` give useful information for merhods like `Dog.wag`.)

This is something I did just to see if I could - I'm not using it for real right now - but hopefully it's interesting/useful to someone!
