---
layout: default.liquid
title: Blog posts
---

{% for post in collections.posts.pages %}
[{{ post.title }} ({{post.published_date}})]({{ post.permalink }})

{{ post.excerpt }}

{% endfor %}
