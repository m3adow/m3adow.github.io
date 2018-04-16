---
layout: default
title: "Understanding multi line strings in YAML and Ansible (Part II - Ansible)"
categories:
- YAML
- Ansible
---

In [Part I][part1] of this series we examined the two block styles
of YAML, literal and folded, as well as the three block chomping methods, strip,
clip and keep. In this post we want to investigate how these styles and methods
interact with different Ansible use cases.

# Multi line strings in Modules
The classic usage of a multi line string in Ansible is in the `command` or `shell`
module. This example is directly taken from the [Ansible docs][commandmodule]:
```yaml
# You can use shell to run other executables to perform actions inline
- name: Run expect to wait for a successful PXE boot via out-of-band CIMC
  shell: |
    set timeout 300
    spawn ssh admin@{{ cimc_host }}

    expect "password:"
    send "{{ cimc_password }}\n"

    expect "\n{{ cimc_name }}"
    send "connect host\n"

    expect "pxeboot.n12"
    send "\n"

    exit 0
  args:
    executable: /usr/bin/expect
  delegate_to: localhost
```

A literal style block with clip chomping is used to send several commands.
Folded style would not make any sense here, except if you wanted to either pipe
the commands or chain them with `&&` or `||`.

<!--more-->

{% include adsense_manual.html %}

One task I use in one of my server playbooks:
```yaml
- name: Get public IP
  shell: >
    bash -c "set -eo pipefail;
      [ -z "${PUBLIC_IP}" ]
      && curl -s https://ipv4.wtfismyip.com/text
      | tr -d '\n'"
  register: node_public_ip
  changed_when: false
  failed_when: node_public_ip.rc > 0
  check_mode: no
```
To ease the readability, I use folded style here. This enables me to do line breaks
whenever I want without using \"\\\".

A similar approach for the `blockinfile` module:
```yaml
- name: insert/update eth0 configuration stanza in /etc/network/interfaces
        (it might be better to copy files into /etc/network/interfaces.d/)
  blockinfile:
    path: /etc/network/interfaces
    block: |
      iface eth0 inet static
          address 192.0.2.23
          netmask 255.255.255.0
```
Once again, literal style with clip chomping. Folded style would not make any
sense at all, as it would reduce the block to one line.
As in the other two examples, the different block folding methods would not
change the functionality at all.

# Multi line strings in variables and loops
Let's start easy with these three example variables with a couple of lines
from the Linux kernel `copyright` file:
```yaml
vars:
  literal: |
    This package is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  folded: >
    This package is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  folded_strip: >-
    This package is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

{% include adsense_manual_link.html %}

## shell
Now let's put these variable in a simple looped `shell` task. Just disregard the fact that
you would probably never use this in a real playbook.

```yaml
- name: Ensure the file does not exist first
  file:
    path: /tmp/mytemp
    state: absent
- shell: "/bin/echo -en '## BEGIN ##\n>>{{ item }}<<\n## END ##\n' >> /tmp/mytemp"
  with_items:
    - "{{ literal }}"
    - "{{ folded }}"
    - "{{ folded_strip }}"
```
Note that we use markers around each string, to ease the detection of the block
end. If we now manually output the file, we can clearly see the differences:
```bash
$ cat /tmp/mytemp
## BEGIN ##
>>This package is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
<<
## END ##
## BEGIN ##
>>This package is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
<<
## END ##
## BEGIN ##
>>This package is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.<<
## END ##


```
It's apparent that the line break behavior we learned about in the last post
also applies to the blocks when looped.

## blockinfile
Now, let's use `blockinfile` with these vars:

```yaml
- name: Ensure the file does not exist first
  file:
    path: /tmp/mytemp
    state: absent
- blockinfile:
    path: /tmp/mytemp
    block: ">>{{ item.content }}<<"
    create: yes
    marker: "## {mark} {{ item.marker }}"
  with_items:
    - {"content": "{{ literal }}", "marker": 1}
    - {"content": "{{ folded }}", "marker": 2}
    - {"content": "{{ folded_strip }}", "marker": 3}
```
The content is as expected:

```bash
$ cat /tmp/mytemp                     
## BEGIN 1
>>This package is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
<<
## END 1
## BEGIN 2
>>This package is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
<<
## END 2
## BEGIN 3
>>This package is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.<<
## END 3
```
No problems here, block styles as well as block chomping methods are respected.

{% include gearbest_bottom.html %}

## lineinfile
So far, so good! Now let's get to the hairy stuff. `lineinfile` for starters.
While it's not intuitive to use blocks in combination with `lineinfile` (that's what
`blockinfile` is for, duh!), [Ansible's documentation][ansible-yaml] implies that
the folded style can be used to break long lines:
> Values can span multiple lines using `|` or `>`. Spanning multiple lines using
a `|` will include the newlines. Using a `>` will ignore newlines; **it’s used to
make what would otherwise be a very long line easier to read and edit.** In either
case the indentation will be ignored.

Okay, let's see! Here is our playbook:
```yaml
- hosts: localhost
  gather_facts: no
  connection: local
  vars:
    literal_line: |                               
      I am a literal line                         
    folded_line: >                                
      I am a folded line                          
    folded_strip_line: >-                         
      I am a folded stripped line                 
tasks:                     
- lineinfile:
    path: /tmp/mylinetemp                        
    line: "{{ item }}"                        
    create: yes                               
  with_items:                                 
    - "{{literal_line}}"                      
    - "{{folded_line}}"                       
    - "{{folded_strip_line}}"
```
And here is the content of `mylinetemp` after the first run:
```bash
$ cat /tmp/mytemp
I am a literal line

I am a folded line

I am a folded stripped line

```
The first run didn't cause any problems at all. How about a second run? This should
not pose a problem due to idempotency, right? Here is the file content after run #2:
```bash
$ cat /tmp/mytemp
I am a literal line

I am a folded line

I am a folded stripped line
I am a literal line

I am a folded line
```
The only line which is correctly detected is the folded stripped line. The other
two lines will be added on every run. Why is that? The verbose output of Ansible
gives the probable answer:
```
TASK [lineinfile] ****************************************************************************************************************************************************************************************
changed: [localhost] => (item=I am a literal line
) => {"backup": "", "changed": true, "item": "I am a literal line\n", "msg": "line added"}
changed: [localhost] => (item=I am a folded line
) => {"backup": "", "changed": true, "item": "I am a folded line\n", "msg": "line added"}
ok: [localhost] => (item=I am a folded stripped line) => {"backup": "", "changed": false, "item": "I am a folded stripped line", "msg": ""}
```
The line feed `\n` is still in the search string the `lineinfile` module searches
for. If I am not mistaken, this poses a problem, as the line break is not part of the line itself but the delimiter due to Regex single line mode.


## user
That's already annoying at best, problematic at worst. But let's not stop here. What about
modules which "build" one line from various parameters, like `cron`, `mount` or -
even more important - `user` or `group`?

It's...unintuitive. We'll only use folded style here, as it's safe to use
according to the Ansible documentation. Literal style could expectedly break
stuff.

First of all the good news, my tests with the `user` module were unsuccessful.
I always got an error:
```yaml
- hosts: localhost
  connection: local
  vars:
    users:                                        
      - name: user1                               
        comment: >                                
          A very long comment, just because the user is so very important                            
      - name: user2                               
        comment: A moderately long comment     
    tasks:              
      - user:
          name: "{{ item.name }}"
          comment: "{{ item.comment }}"
          createhome: no
        with_items: "{{ users }}"
```
Output:
```
TASK [user] **********************************************************************************************************************************************************************************************
failed: [localhost] (item={u'comment': u'A very long comment, just because the user is so very important\n', u'name': u'user1'}) => {"changed": false, "item": {"comment": "A very long comment, just because the user is so very important\n", "name": "user1"}, "msg": "useradd: invalid comment 'A very long comment, just because the user is so very important\n'\n", "name": "user1", "rc": 3}
ok: [localhost] => (item={u'comment': u'A moderately long comment', u'name': u'user2'}) => {"append": false, "changed": false, "comment": "A moderately long comment", "group": 1001, "home": "/home/user2", "item": {"comment": "A moderately long comment", "name": "user2"}, "move_home": false, "name": "user2", "shell": "", "state": "present", "uid": 1001}

PLAY RECAP ***********************************************************************************************************************************************************************************************
```
The `user` module uses the shell user management commands, `useradd` in this case.
As we can see in the `msg` field, it's `useradd` which complains about an invalid
comment. Therefore it's very unlikely you could bork your `/etc/passwd` when using
a block with a line feed at the end.

{% include host1plus_banner.html %}

## cron
The `cron` module is where the problems start:

```yaml
- hosts: localhost
  connection: local
  vars:
   cronjobs:                                     
     - command: >                                
         /bin/echo "Will all of this long stuff
         be on one line? Hm... I wonder."
       name: >
         A long line job with a very long line description.
         It is very important to document your cron jobs.
     - command: /bin/echo "This is on one line 4 sure"                                              
       name: A short line job                     
  tasks:
    - cron:                                       
        name: "{{ item.name }}"                   
        cron_file: /tmp/mytempcron                
        job: "{{ item.command }}"                 
        user: "{{ ansible_user_id }}"             
      with_items: "{{ cronjobs }}"
```
The output of the first run is only mildly annoying:
```bash
$ cat /tmp/mytempcron
#Ansible: A long line job with a very long line description. It is very important to document your cron jobs.                                                                                             

* * * * * m3adow /bin/echo "Will all of this long stuff be on one line? Hm... I wonder."             
#Ansible: A short line job                        
* * * * * m3adow /bin/echo "This is on one line 4 sure"
```
Apart from the empty line (due to the `\n` in the name variable) between the
Ansible marker and the command, everything seems to be okay. The second run however
reveals the problem:
```bash
$ cat /tmp/mytempcron
#Ansible: A long line job with a very long line description. It is very important to document your cron jobs.                                                                                             

#Ansible: A long line job with a very long line description. It is very important to document your cron jobs.                                                                                             

* * * * * m3adow /bin/echo "Will all of this long stuff be on one line? Hm... I wonder."             
#Ansible: A short line job                        
* * * * * m3adow /bin/echo "This is on one line 4 sure"
```
While the command is still luckily only used once, an additional marker comment was added.
Of course every playbook run will add a new marker comment. So no idempotency,
a bit of file growth per run, but no functional errors. I'd call this an annoyance,
perhaps a small problem but nothing more.

## mount

Talking about functional errors, let's look into the `mount` module of Ansible:
```yaml
- hosts: localhost
  connection: local
  vars:
    mounts:
      - src: m3adow@sshfs_server:/home/m3adow/
        path: /tmp/tempmnt1
        fstype: fuse.sshfs
        mount_options: >
          noauto,x-systemd.automount,x-systemd.idle-timeout=60,_netdev,users,
          idmap=user,transform_symlinks,follow_symlinks,default_permissions,
          allow_root,IdentityFile=/root/.ssh/ssh_key,reconnect,gid=0
      - src: /dev/sda1
        path: /tmp/tempmnt2
        fstype: ext4
        mount_options: defaults
  tasks:
    - mount:
        fstab: /tmp/mytempfstab
        src: "{{ item.src }}"
        path: "{{ item.path }}"
        opts: "{{ item.mount_options }}"
        fstype: "{{ item.fstype }}"
        state: present
      with_items: "{{ mounts }}"
```
And here is the content of the `/tmp/mytempfstab`:

```bash
$ cat /tmp/mytempfstab
m3adow@sshfs_server:/home/m3adow/ /tmp/tempmnt1 fuse.sshfs noauto,x-systemd.automount,x-systemd.idle-timeout=60,_netdev,users,\040idmap=user,transform_symlinks,follow_symlinks,default_permissions,\040allow_root,IdentityFile=/root/.ssh/ssh_key,reconnect,gid=0
 0 0
/dev/sda1 /tmp/tempmnt2 ext4 defaults 0 0
```

Whoopsie! That's not how a fstab entry is supposed to look! This was my initial
problem, that's why I even started to look into block styles and chomping methods.
Of course we already know why this happens. The folded style still contains a line
feed at the end, resulting in the line break after the mount options / before the
dump setting. Additionally, there are also spaces (`\040`) where the line breaks in
the block were rendering.
Rerunning the playbook has similar effects to `cron`:
```bash
$ cat /tmp/mytempfstab
m3adow@sshfs_server:/home/m3adow/ /tmp/tempmnt1 fuse.sshfs noauto,x-systemd.automount,x-systemd.idle-timeout=60,_netdev,users,\040idmap=user,transform_symlinks,follow_symlinks,default_permissions,\040allow_root,IdentityFile=/root/.ssh/ssh_key,reconnect,gid=0
 0 0
/dev/sda1 /tmp/tempmnt2 ext4 defaults 0 0
m3adow@sshfs_server:/home/m3adow/ /tmp/tempmnt1 fuse.sshfs noauto,x-systemd.automount,x-systemd.idle-timeout=60,_netdev,users,\040idmap=user,transform_symlinks,follow_symlinks,default_permissions,\040allow_root,IdentityFile=/root/.ssh/ssh_key,reconnect,gid=0
 0 0
```

We now have two non functional fstab entries. This will lead to errors when mounting
and booting. Of course one misformatted entry is added every time you run the
playbook.

{% include namesilo_banner.html %}

# Solution

We have examined the behavior of blocks in Ansible exhaustively and we have also
found out the quirks and problems we could encounter. Now let's see how we could
circumvent said problems.

## trim
If you only need to get rid of the trailing white spaces, use the Jinja2 `trim()`
filter. This would solve our problem with the `cron` module in the playbook above:
{% raw %}
```yaml
tasks:
  - cron:                                       
      name: "{{ item.name | trim()}}"                   
      cron_file: /tmp/mytempcron                
      job: "{{ item.command | trim() }}"                 
      user: "{{ ansible_user_id }}"             
    with_items: "{{ cronjobs }}"
```
{% endraw %}
Output:
```bash
$ cat /tmp/mytempcron
#Ansible: A long line job with a very long line description. It is very important to document your cron jobs.
* * * * * m3adow /bin/echo "Will all of this long stuff be on one line? Hm... I wonder."
#Ansible: A short line job
* * * * * m3adow /bin/echo "This is on one line 4 sure"
```
No line feeds in the name or in the command, also full idempotency, following runs
of the playbook will properly detect the existing cron entries and therefore not
change anything.

## regex_replace
Using `trim` does not solve our problem with `mount`. While the trailing line break
would be removed, the spaces in the `mount_options` variable would remain. It
seems we need stronger weapons for this to work. The only reliable solution I
could find is the Jinja2 `regex_replace` filter available since Ansible 2.2.
{% raw %}
```yaml
tasks:
  - mount:
      fstab: /tmp/mytempfstab
      src: "{{ item.src }}"
      path: "{{ item.path }}"
      opts: "{{ item.mount_options | regex_replace('\\s','')}}"
      fstype: "{{ item.fstype }}"
      state: present
    with_items: "{{ mounts }}"
```
{% endraw %}
This does the job:
```bash
$ cat /tmp/mytempfstab
m3adow@sshfs_server:/home/m3adow/ /tmp/tempmnt1 fuse.sshfs noauto,x-systemd.automount,x-systemd.idle-timeout=60,_netdev,users,idmap=user,transform_symlinks,follow_symlinks,default_permissions,allow_root,IdentityFile=/root/.ssh/ssh_key,reconnect,gid=0 0 0
/dev/sda1 /tmp/tempmnt2 ext4 defaults 0 0
```
No line feed before the setting, no `\040` within the mount options. Future
runs of the task will find this line to be `ok` and will not change anything.
Mission accomplished! It is not very intuitive, but it gets the job done.

# Summary

In this post we have learned about the behavior of blocks when used in modules
and - more importantly - when used in variables. We have seen that the Ansible
documentation is misleading at best, plainly wrong at worst. We have also learned
that using blocks in variables doesn't play nicely with some modules, `cron`, `lineinfile`
and especially `mount` in our case studies here. I also presented two solutions
to some problematic use cases.  
For me, it is obvious this property of YAML needs more documentation in Ansible,
as of now it is handled sloppily. I would not recommend using block styles in variables
to ease readability as it could have unforseen consequences.

I hope I could teach you something and would be glad to hear your experiences. Of
course, feel also free to criticise this blog post in the comments.



[part1]: {% post_url 2018-03-27-multi-line-string-yaml-ansible-I %}
[commandmodule]: https://docs.ansible.com/ansible/latest/shell_module.html
[ansible-yaml]: https://docs.ansible.com/ansible/latest/YAMLSyntax.html#yaml-basics
[lineinfile_source]: https://github.com/ansible/ansible-modules-core/blob/devel/files/lineinfile.py
