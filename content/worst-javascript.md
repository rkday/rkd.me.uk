Title: The most terrifying Javascript I've seen yet...
Date: 2013-10-11 10:50
Category: Code
Tags: javascript, languages
Slug: batman-js
Author: Rob Day
Summary: What happens in the land of extreme type coercion.

There was a recent discussion on the Clojure mailing list about
dynamically and statically typed languages. Someone posted [this
terrifying example](https://groups.google.com/d/msg/clojure/0I7u5yn01qU/heNJVkeDXoUJ) of Javascript to show what happens at the extremes
of type coercion:

    js> Array(16).join("wat" - 1) + " Batman!"
    "NaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaN Batman!"
    js>
