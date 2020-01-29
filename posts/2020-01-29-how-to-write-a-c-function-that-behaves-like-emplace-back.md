---
title: How to write a C++ function that behaves like emplace_back?
published_date: "2020-01-29 23:16:18 +0000"
layout: default.liquid
is_draft: false
---
Recently I was working on some C++ code where I had one class (Foo), and another class (FooDoer) that took ownership of Foo objects and did stuff with them.

Rather than dealing with move constructors or pointers to Foo so that I could pass them around, I wanted to be able to tell FooDoer "construct a Foo object that looks like this and then own it". Foo had quite a complicated constructor, though, and I didn't want to give FooDoer lots of methods matching the Foo constructor and keep them in sync - I just wanted stuff passed straight through.

I knew that this must be possible, because this is how the `emplace_back` method on `std::vector` behaves - if Foo has a constructor that takes an int and a std::string, I can do `std::vector<Foo> v; v.emplace_back(9, "hello world");` and it will do in-place construction in the vector. So how does that work, and can I replicate that in my own code?

Yes, it turns out, pretty straightforwardly - the trick is the `...` syntax in C++11, wich gives "template parameter packs" and "function parameter packs". (More detail at <https://eli.thegreenplace.net/2014/variadic-templates-in-c/>).

The code ends up looking like:

```c++
#include <string>
#include <iostream>

class Foo {
  public:
    Foo(int a, std::string b) {
      std::cout << "Foo created with " << a << " and " << b << std::endl;
    };

    Foo(float a) {
      std::cout << "Foo created with " << a << std::endl;
    };
};

class FooDoer {
  public:
    template<typename... Args> void function_like_emplace_back(Args... args) {
      Foo(args...);
    };
};

int main() {
  FooDoer f;
  f.function_like_emplace_back(9, "hello world");
  f.function_like_emplace_back(0.5);
}
```

C++ templates can give notoriously bad error messages, but if I add something that doesn't compile, e.g. `f.function_like_emplace_back("hello world");`, then the error messages are actually decent:

```
$ g++ like_emplace_back.cpp
like_emplace_back.cpp: In instantiation of ‘void FooDoer::function_like_emplace_back(Args ...) [with Args = {const char*}]’:
like_emplace_back.cpp:26:45:   required from here
like_emplace_back.cpp:18:7: error: no matching function for call to ‘Foo::Foo(const char*&)’
   18 |       Foo(args...);
      |       ^~~~~~~~~~~~
like_emplace_back.cpp:10:5: note: candidate: ‘Foo::Foo(float)’
   10 |     Foo(float a) {
      |     ^~~
like_emplace_back.cpp:10:15: note:   no known conversion for argument 1 from ‘const char*’ to ‘float’
   10 |     Foo(float a) {
      |         ~~~~~~^
like_emplace_back.cpp:6:5: note: candidate: ‘Foo::Foo(int, std::string)’
    6 |     Foo(int a, std::string b) {
      |     ^~~
like_emplace_back.cpp:6:5: note:   candidate expects 2 arguments, 1 provided
like_emplace_back.cpp:4:7: note: candidate: ‘constexpr Foo::Foo(const Foo&)’
    4 | class Foo {
      |       ^~~
like_emplace_back.cpp:4:7: note:   no known conversion for argument 1 from ‘const char*’ to ‘const Foo&’
like_emplace_back.cpp:4:7: note: candidate: ‘constexpr Foo::Foo(Foo&&)’
like_emplace_back.cpp:4:7: note:   no known conversion for argument 1 from ‘const char*’ to ‘Foo&&’
```

Okay, perhaps what I really mean is "decent for C++" - certainly no worse than if I try and do `Foo foo("hello world")` directly:

```
like_emplace_back.cpp: In function ‘int main()’:
like_emplace_back.cpp:27:24: error: no matching function for call to ‘Foo::Foo(const char [12])’
   27 |   Foo foo("hello world");
      |                        ^
like_emplace_back.cpp:10:5: note: candidate: ‘Foo::Foo(float)’
   10 |     Foo(float a) {
      |     ^~~
like_emplace_back.cpp:10:15: note:   no known conversion for argument 1 from ‘const char [12]’ to ‘float’
   10 |     Foo(float a) {
      |         ~~~~~~^
like_emplace_back.cpp:6:5: note: candidate: ‘Foo::Foo(int, std::string)’
    6 |     Foo(int a, std::string b) {
      |     ^~~
like_emplace_back.cpp:6:5: note:   candidate expects 2 arguments, 1 provided
like_emplace_back.cpp:4:7: note: candidate: ‘constexpr Foo::Foo(const Foo&)’
    4 | class Foo {
      |       ^~~
like_emplace_back.cpp:4:7: note:   no known conversion for argument 1 from ‘const char [12]’ to ‘const Foo&’
like_emplace_back.cpp:4:7: note: candidate: ‘constexpr Foo::Foo(Foo&&)’
like_emplace_back.cpp:4:7: note:   no known conversion for argument 1 from ‘const char [12]’ to ‘Foo&&’
```
