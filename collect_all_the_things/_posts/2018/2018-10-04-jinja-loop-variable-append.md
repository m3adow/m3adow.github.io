---
layout: default
title: "Ansible: Extend variable values in Jinja 2 templates"
categories:
- ansible
---

In a Jinja 2 Template for one of my Ansible playbooks I wanted to construct a string containing several potentially filled variables to eventually append it to a command execution.

I tried this:
{% raw %}
```jinja
{% set additional_opts = '' %}
{% for opt_arg, opt_name in [
  (item.exclusive_labels|default(''), '--exclusive_labels'),
  (item.ignore_labels|default(''), '--ignore_labels'),
  (item.exclusive_prefixes|default(''), '--exclusive_prefixes'),
  (item.ignore_prefixes|default(''), '--ignore_prefixes')
] %}
{% if opt_arg %}
{% set additional_opts %}{{ additional_opts }} {{ opt_name }}="{{ opt_arg }}"
{%- endset %}
{% endif %}
{% endfor %}

runme.py {{ additional_opts }}
```
{% endraw %}

But that didn't work. The `additional_opts` variable never contained any value outside of the loop.
After some research, I found out, that this is working as intended. This is even mentioned in Jinjas (excellent) [Template Designer Documentation][tdd]:

> *Please keep in mind that it is not possible to set variables inside a block and have them show up outside of it. This also applies to loops.*

And there's even a proposal how to achieve this use case properly:

> *As of version 2.10 more complex use cases can be handled using namespace objects which allow propagating of changes across scopes*

After reading that, correcting my template didn't take long. It ended up looking like this:

{% raw %}
```jinja
{% set ns=namespace(additional_opts='') %}
{% for opt_arg, opt_name in [
  (item.exclusive_labels|default(''), '--exclusive_labels'),
  (item.ignore_labels|default(''), '--ignore_labels'),
  (item.exclusive_prefixes|default(''), '--exclusive_prefixes'),
  (item.ignore_prefixes|default(''), '--ignore_prefixes')
] %}
{% if opt_arg %}
{% set ns.additional_opts %}{{ ns.additional_opts }} {{ opt_name }}="{{ opt_arg }}"
{%- endset %}
{% endif %}
{% endfor %}

runme.py {{ ns.additional_opts }}
```
{% endraw %}

While this way is a bit less intuitive, it works like a charm.

[tdd]: http://jinja.pocoo.org/docs/2.10/templates/#assignments
