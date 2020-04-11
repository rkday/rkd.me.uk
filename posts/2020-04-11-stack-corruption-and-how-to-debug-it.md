---
title: Stack corruption and how to debug it
published_date: "2020-04-11 17:45:08 +0000"
layout: default.liquid
is_draft: false
---
I hit some stack corruption bugs recently, and have been looking at tools to debug/prevent them. Here's what I learnt!

First, what is a stack? Here's a program that prints out its own stack:

```cpp
$ cat show_the_stack.cpp 
#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include <stdlib.h>
#include <assert.h>

intptr_t begin = 0;

void never_called() {
  printf("This will never be called\n");
}

int myfunc(uint64_t x) {
  int64_t a[2] = {0xaa, 0xbb};
  uint64_t b = 203;

  printf("a in myfunc: %p / %ld\n", (void*)&a, (intptr_t)&a - begin);
  printf("x in myfunc: %p / %ld\n", (void*)&x, (intptr_t)&x - begin);
  printf("__builtin_frame_address() in myfunc: %p / %ld\n", (void*)__builtin_frame_address(0), (intptr_t)__builtin_frame_address(0) - begin);
  printf("first 64 bits of __builtin_frame_address() in myfunc: %p\n", (void*)*(uint64_t*)__builtin_frame_address(0));

  for (int ii = 0; ii < 60; ++++ii)
  {
    uint64_t* memory_address = (uint64_t*)begin - (ii / 2);
    if ((void*)memory_address == (void*)((uint64_t*)__builtin_frame_address(0)))
    {
      printf("==== myfunc\n");
    }
    if ((void*)memory_address == (void*)((uint64_t*)__builtin_frame_address(1)))
    {
      printf("==== myfunc2\n");
    }
    if ((void*)memory_address == (void*)((uint64_t*)__builtin_frame_address(2)))
    {
      printf("==== main\n");
    }
    printf("#%d: %p: %lu (%p)\n", (ii / 2), (void*)memory_address, *memory_address, reinterpret_cast<void*>(*memory_address));  
  }
  return 0x999;
}

int myfunc2(uint64_t y)
{
  myfunc(406);
  return 0x888;
}

int main() {
  uint32_t a = UINT_MAX;
  uint32_t b = 2;

  uint64_t c = (a*b);

  printf("Address of main(): %p\n", main);
  printf("Address of myfunc(): %p\n", myfunc);
  printf("Address of myfunc2(): %p\n", myfunc2);

  begin = (intptr_t)__builtin_frame_address(0);

  printf("__builtin_frame_address() in main: %p\n", (void*)__builtin_frame_address(0));

  myfunc2(104);

  return 0x777;
}
```

and its output, lightly annotated:

```
$ ./show_the_stack                            
Address of main(): 0x5614d6712350
Address of myfunc(): 0x5614d6712170
Address of myfunc2(): 0x5614d6712320
__builtin_frame_address() in main: 0x7ffd8ff849d0
a in myfunc: 0x7ffd8ff84950 / -128
x in myfunc: 0x7ffd8ff84948 / -136
__builtin_frame_address() in myfunc: 0x7ffd8ff84970 / -96
first 64 bits of __builtin_frame_address() in myfunc: 0x7ffd8ff84990
==== main
#0: 0x7ffd8ff849d0: 0 ((nil))
#1: 0x7ffd8ff849c8: 4294967295 (0xffffffff) // Local variable 'a'
#2: 0x7ffd8ff849c0: 11005348544 (0x28ff84ac0) // Local variable 'b' is the 0x2 at the start.
#3: 0x7ffd8ff849b8: 4294967294 (0xfffffffe) // Local variable 'c'
#4: 0x7ffd8ff849b0: 146028888100 (0x2200000024)
#5: 0x7ffd8ff849a8: 158913790002 (0x2500000032)
#6: 0x7ffd8ff849a0: 0 ((nil))
#7: 0x7ffd8ff84998: 94647497073647 (0x5614d67123ef) // Return address for myfunc2() - a few bytes after the start of main() at 0x5614d6712350
==== myfunc2
#8: 0x7ffd8ff84990: 140727018867152 (0x7ffd8ff849d0) // Frame pointer for calling function (main) - i.e. location of #0
#9: 0x7ffd8ff84988: 104 (0x68) // Local variable/ parameter y
#10: 0x7ffd8ff84980: 94647497073664 (0x5614d6712400)
#11: 0x7ffd8ff84978: 94647497073462 (0x5614d6712336) // Return address for myfunc() - a few bytes after the start of myfunc2() at 0x5614d6712320
==== myfunc
#12: 0x7ffd8ff84970: 140727018867088 (0x7ffd8ff84990) // Frame pointer for calling function (myfunc) - i.e. location of #8
#13: 0x7ffd8ff84968: 16279931531481382912 (0xe1edef791da10000)
#14: 0x7ffd8ff84960: 0 ((nil))
#15: 0x7ffd8ff84958: 187 (0xbb) // Local variable a[1]
#16: 0x7ffd8ff84950: 170 (0xaa) // Local variable a[0]
#17: 0x7ffd8ff84948: 406 (0x196) // Local variable/parameter x
#18: 0x7ffd8ff84940: 203 (0xcb) // Local variable b
#19: 0x7ffd8ff84938: 19 (0x13) // Local variable ii
```

You can see that if I started writing to a[2] and later, I'd start overwriting important bits of the stack - e.g. a[4] would overwite the parent frame pointer, a[5] would overwrite the return address, and a[7] would start overwriting local variables in the parent function.

This might also occur if I saved off a pointer to a variable on the stack, then wrote to it later once the function had returned and the stack layout had changed. (This was my actual problem; it wasn't quite as obvious as it sounds, because I was passing that pointer into a third-party library which wasn't clear that it saved the pointer off.)

This can be particularly painful because corrupting the parent frame pointer and/or return address makes gdb struggle to give useful backtraces:

```
Program received signal SIGSEGV, Segmentation fault.
0x0000000000000000 in ?? ()
(gdb) bt
#0  0x0000000000000000 in ?? ()
#1  0x0000000000000068 in ?? ()
#2  0x00007fffffffdb20 in ?? ()
#3  0x0000555555555229 in main () at corruption3.cpp:28
Backtrace stopped: frame did not save the PC
(gdb) 
```

My other usual go-to for debugging memory issues, valgrind, also doesn't work very well for stack issues - it's much better at tracking heap allocations and writes than stack problems. So what tools are available?

## __stack_chk_fail

Clang and GCC have the ability to check canary values on the stack, and complain if they've been overwritten. This is enabled with `-fstack-protector`, or `-fstack-protector-all` to apply it to more functions.

```cpp
$ cat corruption1.cpp                                      
#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include <stdlib.h>
#include <assert.h>

int myfunc(uint64_t x) {
  int64_t a[2] = {0xaa, 0xbb};
  uint64_t b = 203;

  uint64_t* forbidden_stack_address = (uint64_t*)__builtin_frame_address(0) - 1;
  *forbidden_stack_address = 4;

  return 0x999;
}

int myfunc2(uint64_t y)
{
  myfunc(406);
  return 0x888;
}

int main() {
  myfunc2(104);

  return 0x777;
}
```

Here I corrupt the 64 bits just before the frame pointer (i.e. the '#13: 0x7ffd8ff84968: 16279931531481382912 (0xe1edef791da10000)') from the above stack.

This is detected at runtime:

```
$ ./corruption1                                                      
*** stack smashing detected ***: terminated
[1]    107717 abort (core dumped)  ./corruption1
                                                                                                                                                                       $ gdb ./corruption1                                                  
GNU gdb (GDB) 9.1
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-pc-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./corruption1...
(gdb) run
Starting program: /home/rkd/src/stack_corruption/corruption1 
*** stack smashing detected ***: terminated

Program received signal SIGABRT, Aborted.
0x00007ffff7abace5 in raise () from /usr/lib/libc.so.6
(gdb) bt
#0  0x00007ffff7abace5 in raise () from /usr/lib/libc.so.6
#1  0x00007ffff7aa4857 in abort () from /usr/lib/libc.so.6
#2  0x00007ffff7afe2b0 in __libc_message () from /usr/lib/libc.so.6
#3  0x00007ffff7b8e06a in __fortify_fail () from /usr/lib/libc.so.6
#4  0x00007ffff7b8e034 in __stack_chk_fail () from /usr/lib/libc.so.6
#5  0x00005555555551a8 in myfunc (x=406) at corruption1.cpp:14
#6  0x00005555555551d3 in myfunc2 (y=104) at corruption1.cpp:19
#7  0x0000555555555226 in main () at corruption1.cpp:24
```

## AddressSanitizer

The stack protector can catch invalid writes, but not reads. This program reads off the end of an array, including things it's not meant to:

```cpp
$ cat corruption2.cpp 
#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include <stdlib.h>
#include <assert.h>

int myfunc(uint64_t x) {
  int64_t a[2] = {0xaa, 0xbb};
  uint64_t b = 203;

  printf("%ld\n", a[2]);
  printf("%ld\n", a[3]);
  printf("%ld\n", a[4]);
  printf("%ld\n", a[5]);

  return 0x999;
}

int myfunc2(uint64_t y)
{
  myfunc(406);
  return 0x888;
}

int main() {
  myfunc2(104);

  return 0x777;
}
```

AddressSanitizer (enabled with `-fsanitize=address` can catch this):

```
$ ./corruption2                                                   
=================================================================
==108199==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffdc23eb1f0 at pc 0x55e4140a07e7 bp 0x7ffdc23eb1b0 sp 0x7ffdc23eb1a8
READ of size 8 at 0x7ffdc23eb1f0 thread T0
    #0 0x55e4140a07e6  (/home/rkd/src/stack_corruption/corruption2+0xf87e6)
    #1 0x55e4140a0955  (/home/rkd/src/stack_corruption/corruption2+0xf8955)
    #2 0x55e4140a0988  (/home/rkd/src/stack_corruption/corruption2+0xf8988)
    #3 0x7f95be950022  (/usr/lib/libc.so.6+0x27022)
    #4 0x55e413fc70ad  (/home/rkd/src/stack_corruption/corruption2+0x1f0ad)

Address 0x7ffdc23eb1f0 is located in stack of thread T0 at offset 48 in frame
    #0 0x55e4140a06bf  (/home/rkd/src/stack_corruption/corruption2+0xf86bf)

  This frame has 1 object(s):
    [32, 48) 'a' (line 8) <== Memory access at offset 48 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow (/home/rkd/src/stack_corruption/corruption2+0xf87e6) 
Shadow bytes around the buggy address:
  0x1000384755e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000384755f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100038475600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100038475610: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100038475620: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x100038475630: 00 00 00 00 00 00 00 00 f1 f1 f1 f1 00 00[f3]f3
  0x100038475640: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100038475650: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100038475660: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100038475670: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100038475680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==108199==ABORTING
```

and, paired with gdb, it can pinpoint the line where corruption occurs:

```
$ gdb ./corruption2                                               
GNU gdb (GDB) 9.1
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-pc-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./corruption2...
(gdb) break __sanitizer::Die
Breakpoint 1 at 0xdf1b0
(gdb) run
Starting program: /home/rkd/src/stack_corruption/corruption2 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
=================================================================
==108263==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffffffda10 at pc 0x55555564c7e7 bp 0x7fffffffd9d0 sp 0x7fffffffd9c8
READ of size 8 at 0x7fffffffda10 thread T0
    #0 0x55555564c7e6  (/home/rkd/src/stack_corruption/corruption2+0xf87e6)
    #1 0x55555564c955  (/home/rkd/src/stack_corruption/corruption2+0xf8955)
    #2 0x55555564c988  (/home/rkd/src/stack_corruption/corruption2+0xf8988)
    #3 0x7ffff7a72022  (/usr/lib/libc.so.6+0x27022)
    #4 0x5555555730ad  (/home/rkd/src/stack_corruption/corruption2+0x1f0ad)

Address 0x7fffffffda10 is located in stack of thread T0 at offset 48 in frame
    #0 0x55555564c6bf  (/home/rkd/src/stack_corruption/corruption2+0xf86bf)

  This frame has 1 object(s):
    [32, 48) 'a' (line 8) <== Memory access at offset 48 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow (/home/rkd/src/stack_corruption/corruption2+0xf87e6) 
Shadow bytes around the buggy address:
  0x10007fff7af0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fff7b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fff7b10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fff7b20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fff7b30: 00 00 00 00 00 00 00 00 00 00 00 00 f1 f1 f1 f1
=>0x10007fff7b40: 00 00[f3]f3 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fff7b50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fff7b60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fff7b70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fff7b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007fff7b90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==108263==ABORTING

Breakpoint 1, 0x00005555556331b0 in __sanitizer::Die() ()
(gdb) bt
#0  0x00005555556331b0 in __sanitizer::Die() ()
#1  0x000055555561b5be in __asan::ScopedInErrorReport::~ScopedInErrorReport() ()
#2  0x000055555561b06f in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) ()
#3  0x000055555561bc49 in __asan_report_load8 ()
#4  0x000055555564c7e7 in myfunc (x=406) at corruption2.cpp:11
#5  0x000055555564c956 in myfunc2 (y=104) at corruption2.cpp:21
#6  0x000055555564c989 in main () at corruption2.cpp:26
(gdb) 
```

## SafeStack

SafeStack defends against stack corruption by creating a separate 'safe' and 'unsafe' stack. If I compile my `show_the_stack` program with `-fsanitize=safe-stack`, I get:

```
$ clang++ -o show_the_stack -fsanitize=safe-stack -ggdb3 show_the_stack.cpp
$ ./show_the_stack 
Address of main(): 0x55597c85dc30
Address of myfunc(): 0x55597c85d9a0
Address of myfunc2(): 0x55597c85dc00
__builtin_frame_address() in main: 0x7fff2cc0f7f0
a in myfunc: 0x7f27f6f19fe0 / -924320749584
x in myfunc: 0x7f27f6f19ff0 / -924320749568
__builtin_frame_address() in myfunc: 0x7fff2cc0f750 / -160
first 64 bits of __builtin_frame_address() in myfunc: 0x7fff2cc0f780
```

That is, my frame pointers are now in different locations (memory addresses beginning 0x7fff) to my local variables (memory addresses beginning 0x7f27). That makes it much harder to corrupt function return addresses by writing off the end of the array.

However, this just mitigates the effect of stack corruption - it doesn't help me track down stack corruption bugs (and maybe makes it harder to track them down, by making their effects more subtle).

## Manual instrumentation

The following program resists all those techniques:

```cpp
$ cat corruption3.cpp 
#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include <stdlib.h>
#include <assert.h>

void never_called() {
  printf("This will never be called\n");
}

int myfunc(uint64_t x) {
  int64_t a[2] = {0xaa, 0xbb};
  uint64_t b = 203;

  uint64_t* return_address = (uint64_t*)__builtin_frame_address(0) + 1;
  *return_address = (uint64_t)&never_called;

  return 0x999;
}

int myfunc2(uint64_t y)
{
  myfunc(406);
  return 0x888;
}

int main() {
  myfunc2(104);

  return 0x777;
}
```

```
$ gdb ./corruption3
(gdb) run
Starting program: /home/rkd/src/stack_corruption/corruption3 
This will never be called

Program received signal SIGSEGV, Segmentation fault.
0x0000000000000000 in ?? ()
(gdb) bt
#0  0x0000000000000000 in ?? ()
#1  0x0000000000000068 in ?? ()
#2  0x00007fffffffdb20 in ?? ()
#3  0x0000555555555229 in main () at corruption3.cpp:28
Backtrace stopped: frame did not save the PC
(gdb) 
```

It corrupts the return address (causing the `never_called` function to be called), but this isn't spotted by the stack protector or ASan.

In this case I had to write my own guard macros, saving off the return address at the start of the function and checking it later (and therefore catching corruption before we attempt to jump to that address and get a broken backtrace):

```cpp
$ cat corruption_guard.cpp                            
#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include <stdlib.h>
#include <assert.h>

#define STACK_RA_CHECK_SETUP void* ra_start = __builtin_return_address(0);
#define STACK_RA_CHECK assert(ra_start == __builtin_return_address(0)); assert(((intptr_t)ra_start & 0xffffffff00000000) == ((intptr_t)main & 0xffffffff00000000));

int main();

void never_called() {
  printf("This will never be called\n");
}

int myfunc(uint64_t x) {
  STACK_RA_CHECK_SETUP;

  int64_t a[2] = {0xaa, 0xbb};
  uint64_t b = 203;

  STACK_RA_CHECK;
  uint64_t* return_address = (uint64_t*)__builtin_frame_address(0) + 1;
  *return_address = (uint64_t)&never_called;

  STACK_RA_CHECK;
  return 0x999;
}

int myfunc2(uint64_t y)
{
  myfunc(406);
  return 0x888;
}

int main() {
  myfunc2(104);

  return 0x777;
}
```

```
$ ./corruption_guard      
corruption_guard: corruption_guard.cpp:26: int myfunc(uint64_t): Assertion `ra_start == __builtin_return_address(0)' failed.
[1]    109310 abort (core dumped)  ./corruption_guard
```

By putting `STACK_RA_CHECK` throughout the function, it's possible to bisect it and narrow down the problematic lines of code.

As an extra guard (in case something overwrites both the stack return address and my cross-check to the same thing), this assertion checks that the return address looks like a function (i.e. is in sort of the same memory location as main()).

I haven't yet used these in real-world code - but I'm hoping that having researched stack corruption, and the tools for debugging it, will speed things up when I next hit a bug like this.