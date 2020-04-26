---
title: An interposer to debug C++ exceptions
published_date: "2020-04-26 15:18:53 +0000"
layout: default.liquid
is_draft: false
---
I've just released <https://github.com/rkday/cpp-exception-interposer>, which solves some problems I've had with tracking down the source of C++ exceptions (especially in environments where using gdb's `catch throw` command is impractical).

The way it works is:

* it's an interposer, loaded with `LD_PRELOAD`, which means that the functions defined there take precedence over other libraries, including the C++ standard libary
* it defines its own version of `__cxa_throw`, which is the function that gets called when an exception is thrown. The function signature is defined at <https://libcxxabi.llvm.org/spec.html>, and the process for throwing a C++ exception (including calling `__cxa_throw`) defined at <http://itanium-cxx-abi.github.io/cxx-abi/abi-eh.html#cxx-throw>.
* this version of `__cxa_throw` does two things:
    * uses `libbacktrace` to retrieve and print the function call stack. Note that we're early enough in exception processing that the stack hasn't been unwound, so the line of code which threw the exception is still available from the call stack.
    * uses `dlsym` and `RTD_NEXT` to call the real `__cxa_throw`, allowing exception processing to continue.

For an example, I'll quote from the README:

This program (compiled with `g++ -g -std=c++17 -o exceptions exceptions.cpp`):

```cpp
#include <stdexcept>
#include <stdio.h>
#include <optional>

void foo()
{
  std::optional<int> x;
  x.value();
}

void bar()
{
  try {
    foo();
  } catch (std::exception& e) {
    printf("Exception caught and ignored\n");
  }
}

int main()
{
  bar();
}
```

normally provides this output:

```
$ ./exceptions 
Exception caught and ignored
```

but running it with the interposer provides much better diagnostics:

```
$ LD_PRELOAD=cpp-exception-interposer/cpp_exception_interposer.so ./exceptions 
*** C++ exception (St19bad_optional_access) thrown ***
0x7fa4646ee451 ???
  ???:0
0x55958f3f12ea _ZSt27__throw_bad_optional_accessv
  /usr/include/c++/9.3.0/optional:99
0x55958f3f132c _ZNRSt8optionalIiE5valueEv
  /usr/include/c++/9.3.0/optional:931
0x55958f3f11e3 _Z3foov
  /home/rkd/src/exceptions.cpp:8
0x55958f3f1208 _Z3barv
  /home/rkd/src/exceptions.cpp:14
0x55958f3f125a main
  /home/rkd/src/exceptions.cpp:22
0x7fa4641ca022 ???
  ???:0
0x55958f3f10ed ???
  ???:0
0xffffffffffffffff ???
  ???:0
*** Proceeding with C++ exception handling ***
Exception caught and ignored
```
