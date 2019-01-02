Title: Clang vs. GCC - code coverage checking
Date: 2016-04-02 15:37
Category: None
Author: Rob Day
Slug: clang-vs-gcc-coverage

Recently, I've been compiling some of the codebases I work on under Clang 3.8 instead of GCC 4.8, to take advantage of better compiler warnings and faster compilation speed (I've seen a 33% speedup, though I haven't tested this rigorously). Today, I got to grips with llvm-cov-3.8, and checked the coverage of my Clang-compiled test suite - and saw coverage failures, on a test suite I know has 100% coverage when compiled under GCC. Some of the uncovered lines were very odd - a closing brace, for example. What's going on?

The section of code in question looked something like this (deliberately reduced to form a minimal example):

```c++
int Foo::xyz()
{
  std::string my_ip = "10.0.0.2";
  int index = 0;
  for (std::vector<std::string>::iterator it = replicas.begin();
                                          it != replicas.end();
                                          ++it, ++index) // Clang reports this line as uncovered...
  {
    if (*it == my_ip)
    {
      break;
    }
  } // ...and also this line. ???

  return 0;
}
```

I [foolishly assumed some kind of Clang/llvm-cov bug](http://blog.codinghorror.com/the-first-rule-of-programming-its-always-your-fault/), perhaps something to do with using the comma operator in a for loop (as other for loops without the comma operator didn't have this coverage issue), and started trying to create a minimal example so I could report a bug. I didn't have any luck with this - until I tweaked my minimal example so that `my_ip` matched the first value in the `replicas` list, at which point the problem reproduced.

Aha! There is a genuine coverage bug here, which Clang spotted and GCC didn't:

- my test suite always set up the input so that `my_ip` was the first item in `replicas`
- so we always broke out of the loop - we never exited the loop normally - and I think this is what the uncovered `}` is trying to tell me
- and we always broke out on the first iteration, so the `++it, ++index` code never ran (which is why that line is uncovered)

Good job, Clang!

In GCC's defense, using the C++11 range-based for loops makes you write the code like this:

```c++
int Foo::xyz()
{
  std::string my_ip = "10.0.0.2";
  int index = 0;
  for (std::string& it: replicas)
  {
    if (it == my_ip)
    {
      break;
    }
    ++index;
  }

  return 0;
}
```

and in that case, both GCC and Clang can spot that the `++index;` line is uncovered.

So if you want to make your code coverage checking more robust, switch to Clang or use more C++11 features - or both.

**Update:**

[notanote on Hacker News](https://news.ycombinator.com/item?id=11412653) pointed out that GCC 4.8 is much older than Clang 3.8 (GCC 4.8.0 was released in March 2013, GCC 4.8.4 - my version - in Deceber 2014, and Clang 3.8 in March 2016), so it would be fairer to compare against a recent GCC. The [Ubuntu Toolchain PPA](https://launchpad.net/~ubuntu-toolchain-r/+archive/ubuntu/test) doesn't have the in-progress GCC 6 available for Ubuntu Trusty, just for Xenial - but it does have GCC 5.3. I installed that and checked coverage, and it still doesn't report any uncovered lines on that test. (I've uploaded the .gcov output files for [GCC 4.8.4](/static/clang-minimal-coverage-example1.cpp.gcc4-gcov.txt), [GCC 5.3](/static/clang-minimal-coverage-example1.cpp.gcc5-gcov.txt) and [Clang 3.8](/static/clang-minimal-coverage-example1.cpp.clang-gcov.txt), if you're interested.)

GCC-5 is more of a pain to install than Clang 3.8 - it brings in [an updated libstdc++ which defaults to a new ABI](https://gcc.gnu.org/onlinedocs/libstdc++/manual/using_dual_abi.html), which causes compatibility issues when deploying to other Ubuntu Trusty systems - which is why I don't use a non-default GCC.
