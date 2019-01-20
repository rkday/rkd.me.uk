---
title: Theming Cobalt
published_date: "2019-01-20 18:26:18 +0000"
layout: default.liquid
is_draft: false
---
When I switched from Pelican to Cobalt as my static site generator this year, one of the trickiest things was theming the site. Cobalt doesn't (yet) have anything like <https://github.com/getpelican/pelican-themes>, so you need to roll your own theme, and I thought I'd write up some notes on how.

First, find a base HTML page. <https://templated.co/> has hundreds, all under a Creative Commons license - I hunted for one that looked nice and had a two-column layout (with a thin sidebar and some main content).

Once you've chosen a page, copy that into `_layouts/default.liquid` in your Cobalt folder.

Then, tweak it so that it's a template:

{% raw %}
- the title of your page is `{{ page.title }}` - I have this as the HTML page title and as a `<h1>` on each page
- the content is `{{ page.content }}`
- I want a date on the pages where it makes sense (like blog posts), but not other pages (like the homepage), which I achieve with:

```
{% if page contains "published_date" %}
<h3>{{ page.published_date | date: "%B %e, %Y" }}</h3>
{% endif %}
```

- in the sidebar, I want to list my 10 most recent posts, with:

```
{% for post in collections.posts.pages limit:10 %}
<li><a href="/{{post.permalink}}">{{post.title}}</a> ({{ post.published_date | date: "%B %e, %Y" }})</li>
{% endfor %}
```
{% endraw %}

Useful references:

- the [Variables documentation](http://cobalt-org.github.io/docs/variables/) for Cobalt
- the [Liquid template documentation](https://shopify.github.io/liquid/tags/iteration/), which is where I got the right syntax for 'only the first 10 from this list'
