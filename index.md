---
layout: default.liquid
---
## Blog!

{% for post in collections.posts.pages %}
[{{ post.title }} ({{post.published_date}})]({{ post.permalink }})

{{ post.excerpt }}

{% endfor %}
