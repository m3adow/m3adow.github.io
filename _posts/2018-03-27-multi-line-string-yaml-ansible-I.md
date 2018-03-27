---
layout: default
title: "Understanding multi line strings in YAML and Ansible (Part I - YAML)"
categories:
- YAML
- Ansible
---

I had a strange problem with variables spanning multiple lines in Ansible. During
the process of debugging it, I learned a bit about multi line strings which are
called "blocks" in the [official YAML specification][yamldoc]. In this blog post
we'll examine the different YAML block styles and block chomping methods.
In Part II we will then learn the use cases and quirks of each style when
used in Ansible.

We'll run this base playbook for each style via `ansible-playbook -v playbook.yml`
and will only replace the variable with the corresponding style.
```yaml
---
- hosts: localhost
  connection: local
  vars:
    my_pattern: |
      With his own sword,
      Which he did wave against my throat, I have ta’en
      His head from him.
  tasks:
    - debug:
        var: my_pattern
```
# Styles
There are two basic styles of blocks in YAML, **literal** and **folded**. Both have
different advantages and disadvantages, especially when used in Ansible.

## Literal
According to the YAML specification literal is "*is the simplest, most
restricted, and most readable scalar style*". It's denoted by the pipe, `|`:
```yaml
my_pattern: |
  With his own sword,
  Which he did wave against my throat, I have ta’en
  His head from him.
```
Output:
```
ok: [localhost] => {                              
    "my_pattern": "With his own sword,\nWhich he did wave against my throat, I have ta’en\nHis head from him.\n"                                                  
}
```

<!--more-->

{% include adsense_manual.html %}

We can observe the preservation of every line break in the string. This also applies
to multiple sequential line feeds:
```yaml
my_pattern: |
  With his own sword,
  Which he did wave against my throat, I have ta’en


  His head from him.
```
Output:
```
ok: [localhost] => {                              
    "my_pattern": "With his own sword,\nWhich he did wave against my throat, I have ta’en\n\n\nHis head from him.\n"                                                  
}
```
It does not however apply to trailing line breaks at the end of the string:
```yaml
my_pattern: |
  With his own sword,


  Which he did wave against my throat, I have ta’en
  His head from him.



```
Output:
```
ok: [localhost] => {                              
    "my_pattern": "With his own sword,\n\n\nWhich he did wave against my throat, I have ta’en\nHis head from him.\n"                                                                                      
}
```
All trailing line breaks except one are removed. This is called
"[Block chomping][blockchomping]" which we'll come back to shortly.

{% include adsense_manual_link.html %}

## Folded
The YAML specification describes the folded style as "*similar to the literal
style; however, folded scalars are subject to line folding*". Okay, but what is
this supposed to mean? This is also answered by the YAML specification: "*Folding
allows long lines to be broken anywhere a single space character separates two
non-space characters.*"

Lets examine our example. The folded style is denoted by
the greater-than sign (yes, [that's its name][greaterthan]), `>`:
```yaml
my_pattern: >
  With his own sword,
  Which he did wave against my throat, I have ta’en
  His head from him.
```
Output:
```
ok: [localhost] => {
    "my_pattern": "With his own sword, Which he did wave against my throat, I have ta’en His head from him.\n"
}
```
Two observations can be made. For once, line breaks within the string are replaced
by a space. Additionally, there's still a line break at the end, to quote the YAML
specification once again: "*The final line break, and trailing empty lines if any,
are subject to chomping and are never folded*". As I already mentioned, we'll come
to block chomping later on.

For now let's look at a more advanced example:
```yaml
my_pattern: >                                 
  With his own sword,


  Which he did wave against my throat, I have ta’en
  His head from him.


```
Output:
```
ok: [localhost] => {
    "my_pattern": "With his own sword,\n\nWhich he did wave against my throat, I have ta’en His head from him.\n"
}
```
As we can see, two of the three line breaks after the first line have been preserved.
Single line breaks, like the one between line four and five, are still  replaced by
one space while the three trailing line feeds have been reduce to one due to block
chomping.  
I have now mentioned it three times, so lets investigate...

# Block Chomping

Directly from the YAML specification:
> Chomping controls how final line breaks
and trailing empty lines are interpreted. YAML provides three chomping methods:
>
>**Strip**  
    Stripping is specified by the “-” chomping indicator. In this case, the final line break and any trailing empty lines are excluded from the scalar’s content.   
>**Clip**  
    Clipping is the default behavior used if no explicit chomping indicator is specified. In this case, the final line break character is preserved in the scalar’s content. However, any trailing empty lines are excluded from the scalar’s content.  
> **Keep**  
    Keeping is specified by the “+” chomping indicator. In this case, the final line break and any trailing empty lines are considered to be part of the scalar’s content. These additional lines are not subject to folding.

We already observed the default `Clip` behavior. Trailing line breaks were reduced to one,
this one however was always preserved. Therefore, we skip this and directly proceed
to the remaining two methods.

{% include gearbest_bottom.html %}

## Stripping
Here is our beloved Shakespeare citation, in **literal style**, with stripping enabled
and a couple of additional line breaks.  
We are already advanced YAML block style users, so we don't delay ourselves with
basic functionality.
```yaml
my_pattern: |-
  With his own sword,


  Which he did wave against my throat, I have ta’en

  His head from him.


```
Output:
```
ok: [localhost] => {
    "my_pattern": "With his own sword,\n\n\nWhich he did wave against my throat, I have ta’en\n\nHis head from him."
}
```
As expected, all line feeds within the string were preserved while the trailing
line breaks were removed.

Very similar in **folded style**:
```yaml
my_pattern: >-
  With his own sword,


  Which he did wave against my throat, I have ta’en

  His head from him.


```
Output:
```
ok: [localhost] => {
    "my_pattern": "With his own sword,\n\nWhich he did wave against my throat, I have ta’en\nHis head from him."
}
```
While the line breaks within the string are folded as we already observed earlier,
all trailing line feeds have been removed.

## Keeping

Last but not least the keeping method. First with literal style:
```yaml
my_pattern: |-
  With his own sword,


  Which he did wave against my throat, I have ta’en

  His head from him.


```
Output:
```
ok: [localhost] => {
    "my_pattern": "With his own sword,\n\n\nWhich he did wave against my throat, I have ta’en\n\nHis head from him.\n\n\n"
}
```

{% include host1plus_banner.html %}

 Unsurprisingly, all line feeds within the string are preserved. Similarly, as
 described by the block chompings method description, all trailing line breaks
 are preserved.

 No surprises with the folding style:
 ```yaml
 my_pattern: |-
   With his own sword,


   Which he did wave against my throat, I have ta’en

   His head from him.


 ```
 Output:
 ```
 ok: [localhost] => {
     "my_pattern": "With his own sword,\n\nWhich he did wave against my throat, I have ta’en\nHis head from him.\n\n\n"
 }
 ```
Line breaks within the string are folded, trailing line feeds are preserved.

# Summary

In this post we've learned about the two YAML block styles, **literal** and
**folded**. We've also discovered the three block chomping methods responsible for trailing
line break handling, **stripping**, **clipping** and **keeping**. We've observed
the differences between the block styles in combination with different block chomping
methods.

In Part II of this mini series we will examine the interaction between all those
styles and methods in Ansible variables, loops and methods.



[yamldoc]: http://www.yaml.org/spec/1.2/spec.html#Block
[blockchomping]: http://www.yaml.org/spec/1.2/spec.html#id2794534
[greaterthan]: https://en.wikipedia.org/wiki/Greater-than_sign
