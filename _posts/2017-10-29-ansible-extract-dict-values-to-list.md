---
layout: default
title: "Ansible: Extracting dictionary values into a list"
categories:
- Ansible
---

**Scenario:**

In Ansible you have a list of dictionaries containing some values, e.g. a list of mount points:

```yaml
mymounts:
  basedir: /srv/mymounts
  mounts:
    -
      name: first_mount
      opts: defaults
    -
      name: second_mount
      opts: noauto,x-systemd.automount,_netdev,reconnect
    -
      name: third_mount
      opts: defaults
```

And you want to extract a list of mount pathes combined from `basedir` and `name`
for further usage, so the result looks like this:

```yaml
['/srv/mymounts/first_mount', '/srv/mymounts/second_mount', '/srv/mymounts/third_mount']
```

<!--more-->

{% include adsense_manual.html %}

Sadly, I could not find an easy or intuitive way to do this. You can neither use
Jinja2 {% raw %}`{% for %}`{% endraw %} loops in Playbooks or variable files, nor Python loops.  
But I found a way using `set_fact`:

{% raw %}
```yaml
- name: Expand mount dirs for later use
  set_fact:
    # Sets a list of mount directories
    expanded_mounts: "\
      {{ expanded_mounts | default([]) }} + \
      [ '{{ mymounts['basedir'] }}/{{ item['name'] }}' ]"
  with_items: "{{ mymounts['mounts'] }}"
```
{% endraw %}

As `expanded_mounts` is not defined in the first run, it is created as an empty list via the `default([])` filter. Afterwards the expanded string is created and appended to the empty list via list addition. As we use `with_items`, this is done for every dictionary in the `mounts` list.

What do I need this for? I have a similar list of mountpoints I map SSHFS mounts to. I want to reuse those mountdirs during the creation of a Jinja2 template for [Borg Backup](https://www.borgbackup.org/). As I have other sources as well, I only needed a list of pathes to back up.

{% raw %}
```yaml
- name: Add files for backups and enable them
  include_tasks: borgmatic.yml
  with_items:
    -
      job_name: "{{ borg['borgmatic']['local_backup']['name'] }}"
      job_time: "{{ borg['borgmatic']['local_backup']['time'] }}"
      backup_dirs: "{{ borg['borgmatic']['local_backup']['dirs'] }}"
      exclude_list: "{{ borg['borgmatic']['local_backup']['exclude_list'] }}"
      target_repos: "{{ uberspace_mounts['backup']['repositories'] }}"
    -
      job_name: "{{ uberspace_mounts['backup']['name'] }}"
      job_time: "{{ uberspace_mounts['backup']['time'] }}"
      backup_dirs: ""{{ expanded_mounts }}""
      exclude_list: "{{ uberspace_mounts['backup']['exclude_list'] }}"
      target_repos: ""{{ borg['borgmatic']['local_backup']['repositories'] }}"
```
{% endraw %}

Perhaps a bit complicated, but works like a charm. If you found this article helpful but just not the exact solution, I can recommend you the "[How to append to lists in Ansible](http://blog.crisp.se/2016/10/20/maxwenzin/how-to-append-to-lists-in-ansible)" post from the Crisp blog which also helped me find my solution.
