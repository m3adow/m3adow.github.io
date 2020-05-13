---
layout: default
title: "Ansible: Loop 'find' with Regexes and exclude list"
categories:
- Ansible
- Codebites
---

Scenario: Utilize Ansibles "find" module to find all directories and files matching a list of regexes but not matching another list of regexes

{% raw %}

```yaml
- hosts: localhost
  connection: local

  vars:
    # Find everything containing either 'o', 'l' or 'a'
    included_dir_regexes:
      - '.*a.*'
      - '.*o.*'
      - '.*l.*'
    # Exclude everything beginning with 'lo' or ending with 'ol'
    excluded_dir_regexes:
      - '.*/lo'
      - 'ol$'

  tasks:
    - name: Find matching dirs
      find:
        patterns: "{{ item }}"
        paths: "/var"
        use_regex: yes
        recurse: false
        file_type: directory
      register: found_dirs
      loop: "{{ included_dir_regexes }}"
    - name: Extract found directory pathes
      set_fact:
        matched_dirs: "{{ found_dirs | json_query('results[*].files[*].path') | flatten | unique }}"
    - name: Create copy of list for easy comparison
      set_fact:
        matched_dirs_bckup: "{{ matched_dirs }}"
    - name: Filter out every directory containing an exclude Regex
      set_fact:
        matched_dirs: "{{ matched_dirs | difference([item.0.path]) }}"
      when: item.0.path is search(item.1)
      loop: "{{ found_dirs | json_query('results[*].files') | flatten | unique | product(excluded_dir_regexes) | list }}"
    - name: Output original and processed list as well as their length
      debug:
        msg: "{{ item }}"
      loop:
        - "{{ matched_dirs_bckup }} <-> {{ matched_dirs }}"
        - "{{ matched_dirs_bckup | length }} <-> {{ matched_dirs | length }}"
```

{% endraw %}

Output (slightly truncated):

```bash
$ ansible-playbook find_exclude.yml
PLAY [localhost] ******************************************************************************************************************************************

TASK [Gathering Facts] ************************************************************************************************************************************ok: [localhost]

TASK [Find matching dirs] *********************************************************************************************************************************ok: [localhost] => (item=.*a.*)
ok: [localhost] => (item=.*o.*)
ok: [localhost] => (item=.*l.*)

TASK [Extract found directory pathes] *********************************************************************************************************************
ok: [localhost]

TASK [Create copy of list for easy comparison] ************************************************************************************************************
ok: [localhost]

TASK [Filter out every directory containing an exclude Regex] *********************************************************************************************
ok: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/local', 'islnk': False, 'isgid': False, 'isuid': False, 'roth': True, 'mti[70/4982]
270381.0, 'dev': 64771, 'ischr': False, 'gid': 0, 'atime': 1549368103.1275654, 'isdir': True, 'mode': '0755', 'wgrp': False, 'gr_name': 'root', 'isblk': Fa
lse, 'uid': 0, 'pw_name': 'root', 'nlink': 2, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr': True, 'ctim
e': 1476894420.511, 'size': 4096, 'inode': 8199, 'xoth': True}, '.*/lo'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/local', 'islnk': False, 'isgid': False, 'isuid': False, 'roth': True, 'mtime'
: 1309270381.0, 'dev': 64771, 'ischr': False, 'gid': 0, 'atime': 1549368103.1275654, 'isdir': True, 'mode': '0755', 'wgrp': False, 'gr_name': 'root', 'isbl
k': False, 'uid': 0, 'pw_name': 'root', 'nlink': 2, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr': True,
 'ctime': 1476894420.511, 'size': 4096, 'inode': 8199, 'xoth': True}, 'ol$'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/account', 'islnk': False, 'isgid': False, 'isuid': False, 'roth': True, 'mtim
e': 1478092643.0, 'dev': 64771, 'ischr': False, 'gid': 0, 'atime': 1549368103.1275654, 'isdir': True, 'mode': '0755', 'wgrp': False, 'gr_name': 'root', 'is
blk': False, 'uid': 0, 'pw_name': 'root', 'nlink': 2, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr': Tru
e, 'ctime': 1545381409.8627524, 'size': 4096, 'inode': 8208, 'xoth': True}, '.*/lo'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/account', 'islnk': False, 'isgid': False, 'isuid': False, 'roth': True, 'mtim
e': 1478092643.0, 'dev': 64771, 'ischr': False, 'gid': 0, 'atime': 1549368103.1275654, 'isdir': True, 'mode': '0755', 'wgrp': False, 'gr_name': 'root', 'is
blk': False, 'uid': 0, 'pw_name': 'root', 'nlink': 2, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr': Tru
e, 'ctime': 1545381409.8627524, 'size': 4096, 'inode': 8208, 'xoth': True}, 'ol$'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/crash', 'islnk': False, 'isgid': False, 'isuid': False, 'roth': True, 'mtime'
: 1545382796.7166486, 'dev': 64771, 'ischr': False, 'gid': 0, 'atime': 1549368103.1585653, 'isdir': True, 'mode': '0755', 'wgrp': False, 'gr_name': 'root',
 'isblk': False, 'uid': 0, 'pw_name': 'root', 'nlink': 2, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr':
 True, 'ctime': 1545382796.7166486, 'size': 4096, 'inode': 8207, 'xoth': True}, '.*/lo'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/crash', 'islnk': False, 'isgid': False, 'isuid': False, 'roth': True, 'mtime'
: 1545382796.7166486, 'dev': 64771, 'ischr': False, 'gid': 0, 'atime': 1549368103.1585653, 'isdir': True, 'mode': '0755', 'wgrp': False, 'gr_name': 'root',
 'isblk': False, 'uid': 0, 'pw_name': 'root', 'nlink': 2, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr':
 True, 'ctime': 1545382796.7166486, 'size': 4096, 'inode': 8207, 'xoth': True}, 'ol$'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/cache', 'islnk': False, 'isgid': False, 'isuid': False, 'roth': True, 'mtime'
: 1506360128.512635, 'dev': 64771, 'ischr': False, 'gid': 0, 'atime': 1549368103.5075643, 'isdir': True, 'mode': '0755', 'wgrp': False, 'gr_name': 'root',
'isblk': False, 'uid': 0, 'pw_name': 'root', 'nlink': 12, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr':
 True, 'ctime': 1506360128.512635, 'size': 4096, 'inode': 8194, 'xoth': True}, '.*/lo'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/cache', 'islnk': False, 'isgid': False, 'isuid': False, 'roth': True, 'mtime'
: 1506360128.512635, 'dev': 64771, 'ischr': False, 'gid': 0, 'atime': 1549368103.5075643, 'isdir': True, 'mode': '0755', 'wgrp': False, 'gr_name': 'root',
'isblk': False, 'uid': 0, 'pw_name': 'root', 'nlink': 12, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr':
 True, 'ctime': 1506360128.512635, 'size': 4096, 'inode': 8194, 'xoth': True}, 'ol$'])
 skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/games', 'islnk': False, 'isgid': False, 'isuid': False, 'roth': True[38/4982]
: 1309270381.0, 'dev': 64771, 'ischr': False, 'gid': 0, 'atime': 1549368103.656564, 'isdir': True, 'mode': '0755', 'wgrp': False, 'gr_name': 'root', 'isblk
': False, 'uid': 0, 'pw_name': 'root', 'nlink': 2, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr': True,
'ctime': 1476894420.5059998, 'size': 4096, 'inode': 8198, 'xoth': True}, '.*/lo'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/games', 'islnk': False, 'isgid': False, 'isuid': False, 'roth': True, 'mtime'
: 1309270381.0, 'dev': 64771, 'ischr': False, 'gid': 0, 'atime': 1549368103.656564, 'isdir': True, 'mode': '0755', 'wgrp': False, 'gr_name': 'root', 'isblk
': False, 'uid': 0, 'pw_name': 'root', 'nlink': 2, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr': True,
'ctime': 1476894420.5059998, 'size': 4096, 'inode': 8198, 'xoth': True}, 'ol$'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/spool', 'islnk': False, 'isgid': False, 'gr_name': 'root', 'roth': True, 'mti
me': 1476968365.2544403, 'dev': 64771, 'ischr': False, 'gid': 0, 'isdir': True, 'mode': '0755', 'wusr': True, 'wgrp': False, 'isuid': False, 'isblk': False
, 'uid': 0, 'pw_name': 'root', 'nlink': 15, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'atime': 1549368103.1
315656, 'ctime': 1476968365.2544403, 'xoth': True, 'inode': 8205, 'size': 4096}, '.*/lo'])
ok: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/spool', 'islnk': False, 'isgid': False, 'gr_name': 'root', 'roth': True, 'mtime': 1
476968365.2544403, 'dev': 64771, 'ischr': False, 'gid': 0, 'isdir': True, 'mode': '0755', 'wusr': True, 'wgrp': False, 'isuid': False, 'isblk': False, 'uid
': 0, 'pw_name': 'root', 'nlink': 15, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'atime': 1549368103.1315656
, 'ctime': 1476968365.2544403, 'xoth': True, 'inode': 8205, 'size': 4096}, 'ol$'])
ok: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/lock', 'islnk': False, 'isgid': False, 'gr_name': 'lock', 'roth': True, 'mtime': 15
49422122.25729, 'dev': 64771, 'ischr': False, 'gid': 54, 'isdir': True, 'mode': '0775', 'wusr': True, 'wgrp': True, 'isuid': False, 'isblk': False, 'uid':
0, 'pw_name': 'root', 'nlink': 6, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'atime': 1549368103.639564, 'ct
ime': 1549422122.25729, 'xoth': True, 'inode': 8200, 'size': 4096}, '.*/lo'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/lock', 'islnk': False, 'isgid': False, 'gr_name': 'lock', 'roth': True, 'mtim
e': 1549422122.25729, 'dev': 64771, 'ischr': False, 'gid': 54, 'isdir': True, 'mode': '0775', 'wusr': True, 'wgrp': True, 'isuid': False, 'isblk': False, '
uid': 0, 'pw_name': 'root', 'nlink': 6, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'atime': 1549368103.63956
4, 'ctime': 1549422122.25729, 'xoth': True, 'inode': 8200, 'size': 4096}, 'ol$'])
ok: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/log', 'islnk': False, 'isgid': False, 'gr_name': 'root', 'roth': True, 'mtime': 154
9422121.492292, 'dev': 64772, 'ischr': False, 'gid': 0, 'isdir': True, 'mode': '0755', 'wusr': True, 'wgrp': False, 'isuid': False, 'isblk': False, 'uid':
0, 'pw_name': 'root', 'nlink': 16, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'atime': 1549368103.639564, 'c
time': 1549422121.492292, 'xoth': True, 'inode': 2, 'size': 12288}, '.*/lo'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/log', 'islnk': False, 'isgid': False, 'gr_name': 'root', 'roth': True, 'mtime
': 1549422121.492292, 'dev': 64772, 'ischr': False, 'gid': 0, 'isdir': True, 'mode': '0755', 'wusr': True, 'wgrp': False, 'isuid': False, 'isblk': False, '
uid': 0, 'pw_name': 'root', 'nlink': 16, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'atime': 1549368103.6395
64, 'ctime': 1549422121.492292, 'xoth': True, 'inode': 2, 'size': 12288}, 'ol$'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/opt', 'islnk': False, 'isgid': False, 'gr_name': 'root', 'roth': True[6/4982]
': 1544201873.361944, 'dev': 64771, 'ischr': False, 'gid': 0, 'isdir': True, 'mode': '0755', 'wusr': True, 'wgrp': False, 'isuid': False, 'isblk': False, '
uid': 0, 'pw_name': 'root', 'nlink': 4, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'atime': 1549368103.64156
41, 'ctime': 1544201873.361944, 'xoth': True, 'inode': 8202, 'size': 4096}, '.*/lo'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/opt', 'islnk': False, 'isgid': False, 'gr_name': 'root', 'roth': True, 'mtime
': 1544201873.361944, 'dev': 64771, 'ischr': False, 'gid': 0, 'isdir': True, 'mode': '0755', 'wusr': True, 'wgrp': False, 'isuid': False, 'isblk': False, '
uid': 0, 'pw_name': 'root', 'nlink': 4, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'atime': 1549368103.64156
41, 'ctime': 1544201873.361944, 'xoth': True, 'inode': 8202, 'size': 4096}, 'ol$'])
ok: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/lost+found', 'islnk': False, 'isgid': False, 'gr_name': 'root', 'roth': False, 'mti
me': 1476894310.0, 'dev': 64771, 'ischr': False, 'gid': 0, 'isdir': True, 'mode': '0700', 'wusr': True, 'wgrp': False, 'isuid': False, 'isblk': False, 'uid
': 0, 'pw_name': 'root', 'nlink': 2, 'isreg': False, 'isfifo': False, 'xgrp': False, 'woth': False, 'rgrp': False, 'rusr': True, 'atime': 1549368148.749437
6, 'ctime': 1476894312.817, 'xoth': False, 'inode': 11, 'size': 16384}, '.*/lo'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/lost+found', 'islnk': False, 'isgid': False, 'gr_name': 'root', 'roth': False
, 'mtime': 1476894310.0, 'dev': 64771, 'ischr': False, 'gid': 0, 'isdir': True, 'mode': '0700', 'wusr': True, 'wgrp': False, 'isuid': False, 'isblk': False
, 'uid': 0, 'pw_name': 'root', 'nlink': 2, 'isreg': False, 'isfifo': False, 'xgrp': False, 'woth': False, 'rgrp': False, 'rusr': True, 'atime': 1549368148.
7494376, 'ctime': 1476894312.817, 'xoth': False, 'inode': 11, 'size': 16384}, 'ol$'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/lib', 'islnk': False, 'pw_name': 'root', 'gr_name': 'root', 'roth': True, 'mt
ime': 1549422121.517292, 'dev': 64771, 'isgid': False, 'ischr': False, 'gid': 0, 'atime': 1549368103.1675653, 'isdir': True, 'mode': '0755', 'wgrp': False,
 'isuid': False, 'isblk': False, 'uid': 0, 'nlink': 42, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr': T
rue, 'ctime': 1549422121.517292, 'xoth': True, 'inode': 8193, 'size': 4096}, '.*/lo'])
skipping: [localhost] => (item=[{'xusr': True, 'issock': False, 'path': '/var/lib', 'islnk': False, 'pw_name': 'root', 'gr_name': 'root', 'roth': True, 'mt
ime': 1549422121.517292, 'dev': 64771, 'isgid': False, 'ischr': False, 'gid': 0, 'atime': 1549368103.1675653, 'isdir': True, 'mode': '0755', 'wgrp': False,
 'isuid': False, 'isblk': False, 'uid': 0, 'nlink': 42, 'isreg': False, 'isfifo': False, 'xgrp': True, 'woth': False, 'rgrp': True, 'rusr': True, 'wusr': T
rue, 'ctime': 1549422121.517292, 'xoth': True, 'inode': 8193, 'size': 4096}, 'ol$'])

TASK [Output original and processed list as well as their length] *****************************************************************************************
ok: [localhost] => (item=['/var/local', '/var/account', '/var/crash', '/var/cache', '/var/games', '/var/spool', '/var/lock', '/var/log', '/var/opt', '/var/
lost+found', '/var/lib'] <-> ['/var/account', '/var/crash', '/var/cache', '/var/games', '/var/opt', '/var/lib']) => {
    "msg": "['/var/local', '/var/account', '/var/crash', '/var/cache', '/var/games', '/var/spool', '/var/lock', '/var/log', '/var/opt', '/var/lost+found',
'/var/lib'] <-> ['/var/account', '/var/crash', '/var/cache', '/var/games', '/var/opt', '/var/lib']"
}
ok: [localhost] => (item=11 <-> 6) => {
    "msg": "11 <-> 6"
}

PLAY RECAP ************************************************************************************************************************************************
localhost                  : ok=6    changed=0    unreachable=0    failed=0
```