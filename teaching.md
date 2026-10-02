---
title: Teaching
layout: page
permalink: /teaching/
eyebrow: In the classroom
description: Courses in legged robot dynamics, learning and control, and mechanical design.
intro: Robot dynamics, learning, control, and mechanical design.
---

{% for course in site.data.teaching %}
## {{ course.number }}
{: #{{ course.number | slugify }} }

{{ course.name }}
{% if course.description %}

{{ course.description }}
{% endif %}
{% if course.link %}

[Course information]({{ course.link }})
{% endif %}
{% endfor %}
