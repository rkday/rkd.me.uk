Title: Technical projects

I'm involved in a wide variety of open-source projects, either personal ones, through work, or contributions to larger projects. This page lists a selection of them by language.

## C/C++
*  I'm the maintainer of [the SIPp test tool](http:sipp.sf.net), which implements an XML DSL for writing high-performance telecoms tests.
*  I work for Metaswitch Networks on [the open-source Project Clearwater](http://github.com/Metaswitch). A large part of this ([the core SIP routing component](http://github.com/Metaswitch/sprout)) is written in C++.
*  I've [contributed](http://lists.gnu.org/archive/html/bug-coreutils/2012-08/msg00104.html) to GNU coreutils.

## Python
*  The cluster management and configuration sharing tools for [Project Clearwater](https://github.com/Metaswitch/clearwater-etcd) are written in Python - I designed and implemented [the core state machine](https://github.com/Metaswitch/clearwater-etcd/commits/dev/src/metaswitch/clearwater/cluster_manager/synchronization_fsm.py?page=1).
*  [nose2dep](https://pypi.python.org/pypi/nose2dep), a nose2 plugin for expressing a preferred running order for unit tests
*  [mpinfo](https://pypi.python.org/pypi/MPInfo), a Python package for retrieving information about UK Members of Parliament.
*  I've contributed bug fixes to [ostn2python](https://github.com/TimSC/ostn02python/pull/1) (a GIS helper package for Python) and [robin](https://bitbucket.org/reima/robin/pull-request/3/dont-fail-if-some-info-lacks-a-description/diff) (a Doxygen helper tool).

## Ruby
*  I've written [a Diameter stack in Ruby](https://github.com/rkday/ruby-diameter), which is robust enough for me to base a test suite on it (<https://github.com/rkday/fhoss-testcases>).
*  While writing that stack, I also contributed [various fixes](https://github.com/ruby-concurrency/concurrent-ruby/pulls?q=is%3Apr+author%3Arkday+is%3Aclosed) to the ruby-concurrency library it uses.
*  I'm the maintainer of [quaff](https://rubygems.org/gems/quaff), a Ruby gem for writing telecoms test scenarios. It is inspired by SIPp (see C++ above) but with a focus on ease of use, and integration with other tools, rather than performance.
*  The orchestration and test layers of [Project Clearwater](http://github.com/Metaswitch/chef) are written in Ruby.

## Java
*  I'm a [committer](https://sourceforge.net/p/openimscore/code/HEAD/tree/) to the [OpenIMSCore HSS](http://openimscore.sourceforge.net/), including both bugfixes and new features (such as the IMS Release 9 IncludeRegisterRequest/IncludeRegisterResponse options).
*  I've [contributed](https://github.com/Kunagi/kunagi/pull/3) to the Kunagi agile project management tool.

## Clojure
*  The [overload-middleware](https://clojars.org/overload-middleware) library, an implementation of the ["Adaptive Overload Control For Busy Internet Servers"](http://www.eecs.harvard.edu/%7Emdw/papers/control-usits03.pdf) algorithm in Clojure.
* I've [contributed](https://github.com/Prismatic/schema/pull/53) to the Prismatic/schema library for validating data structures.
