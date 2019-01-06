---
layout: default.liquid
title: C++ static analysis
published_date: 2016-04-10 11:54:00 +0100
slug: cpp-static-analysis
---

Recently, I've been looking at static analysis for some of my C++ codebases - tools that will warn about possible errors in my code without needing to run the code. I've been looking, in particular, for things that I can add as a build step - that is, cases where I can trust the static analyser to be right and fail the build if it fails, rather than fuzzier checks where you need human judgement to double-check that the analysis makes sense.

I've now got a reasonably good feel for what the available tools are and how to run them - so I'm writing the blog post I'd have liked to read when I started looking at this stuff.

## Compiler warnings

If you're interested in static analysis, the first thing you should do is make sure you're making full use of your compiler warnings - with the -Wall flagat least, and maybe -Wextra. On Clang, my preferred compiler, -Wextra includes warnings about signed/unsigned integer comparisons and warnings about unused function parameters.

Switching between Clang and GCC is a good idea to ensure higher quality, as different compilers warn on different things  - when compiling some of my codebases with Clang 3.8 (after previously using GCC 4.8), I got new warnings about unused private member variables and using ::abs instead of std::abs. In the other direction, GCC includes -Wsign-compare in -Wall, whereas Clang only has it in -Wextra.

## cppcheck

<http://cppcheck.sourceforge.net/>

cppcheck was the first static analysis tool I tried, and it's relatively easy to get started with - it's in most GNU/Linux distributions' packaging systems, for example.

Running it over my codebase gave me:

- a warning about using `vector.empty()` where I meant `vector.clear()`
- performance suggestions, like passing const arguments by reference and using `++x` not `x++`
- warnings about using C-style casts, which are less safe than the C++ `static_cast`, `const_cast` and `reinterpret_cast`
- warnings about unused local variables
- warnings about unused functions
- warnings about classes that included pointers but didn't have copy constructors

I did see instances where it failed to parse modern C++ correctly - for example, I saw it get confused by C++ map initialization syntax - it parsed:

`std::map<std::string, uint32_t> \{\{"FOO" + std::to_string(x), 1\}\};`

and reported "(warning) Redundant code: Found a statement that begins with string constant."

This seems to have been fixed between 1.61 (the version on Ubuntu Trusty) and 1.70 (the version on Fedora), though.

The plugin architecture looks quite friendly - you can add new rules just by writing an XML file with a regular expression, whereas adding checks to Clang-based tools requires writing code. 

## clang-tidy

<http://clang.llvm.org/extra/clang-tidy/>

clang-tidy is based on Clang, and uses the Clang library to parse code before analysis - this makes it less prone to parsing errors like I saw with cppcheck, because it can correctly parse anything which Clang can correctly compile.

I found it a bit hard to get started with - just running `clang-tidy file.cpp` complained about being unable to find a compilation database. Fortunately I found <http://eli.thegreenplace.net/2014/05/21/compilation-databases-for-clang-based-tools>, which explained how this worked and the fix (appending `--` and then any compiler arguments I needed).

Running it over my codebase pointed out:

- suggestions of better ways to do things in C++11 (the clang-modernize tool has been integrated into clang-tidy) like:
  - nullptr (which can avoid bugs where the type system treats NULL as an int)
  - the 'override' annotation (which can avoid bugs where you think you've overriden a virtual function, but have made a typo and so declared a new function)
  - range-based for loops (which are unlikely to avoid bugs, but which make code more readable, as you're not dealing directly with iterators)
- differences between parameter names in the header file and the source file (a great feature - this is annoying and difficult to spot manually)

(I'd already run cppcheck over this codebase, and fixed those warnings, so clang-tidy almost certainly detects some or all of the things that cppcheck does.)

## oclint

<http://oclint.org/>

Like clang-tidy, this is based on Clang, and needs the same `--` argument when invoking it.

I found its checks and warnings to need a bit too much human judgement for my taste - it checks things like variable name length, function complexity and so on. But whereas it's difficult to say "ah, it doesn't make sense to use nullptr here because...", it is possible to have code where having a long variable name, or a long function, is actually the best way to write it (e.g. because of the inherent complexity of what you're trying to do).

That said, it might be worth integrating a limited set of checks into a build - for example, it's reasonable to say 'you should never have 1-character variable names - even loop indexes should be `ii` or `jj` for easy searching", and oclint can enforce that.

## Copy-Paste Detector

<http://pmd.sourceforge.net/pmd-4.2.5/cpd.html>

CPD finds duplicated sections of code. It worked pretty well, but like oclint this didn't feel like a hard-and-fast check - duplicated code can sometimes be the best option, perhaps because two cases differ in subtle ways that can't be nicely factored out. (As an example, I think I tried too hard to limit duplication [when porting epoll support to SIPp](https://github.com/SIPp/sipp/commit/9fd813edaebb9d75866a9eecc162a2707e07e6f9) - the resulting set of #ifdefs is probably less maintainable than having two separate-but-similar functions would have been.)

This might still be a useful tool to regularly run over a codebase, though - both to maintain awareness of what code is duplicated 9so if you make a change, you make it in both places) and to check that the number of duplicated sections isn't growing sharply.

## Clang Thread Safety Analysis

<http://clang.llvm.org/docs/ThreadSafetyAnalysis.html>

I didn't actually test this, but it looks so cool I couldn't leave it out of a static analysis blog post.

This adds a series of annotations to Clang that let you express "this variable is guarded by this mutex", "this mutex must be acquired after that mutex", and so on (although ACQUIRED_BEFORE and ACQUIRED_AFTER aren't implemented yet). Clang can then statically check this at compile'time, to verify that your locks really are all taken in the right order, that nothing is accessed without the proper lock, and so on.

This was a bit more involved than what I was trying to do, though - I wanted to just analyse my existing codebases cheaply, without hving to modify the code to help the analysis. But if I'm writing some complex threaded code from scratch in the future, I might take another look at this tool to help verify its correctness.



(Overall disclaimer on static analysis: obviously you should also be looking for software defects by running the code - for example, through a test suite - but

- [as Dijkstra said](https://www.cs.utexas.edu/~EWD/transcriptions/EWD03xx/EWD340.html), testing can only confirm the presence of bugs, not their absence, and static analysis can help spot issues in cases that your test suite doesn't cover
- some of the issues static analysis picks up are not just bugs you can find in unit testing - these tools also give performance and readability guidance
- the earlier you find an issue, the cheaper it is to fix - this is the logic usually used to justify designs and unit tests, but it also applies here, since it's cheaper to fix an issue if you spot it as soon as you write the code, rather than after you also write the unit test that hits the error case)


