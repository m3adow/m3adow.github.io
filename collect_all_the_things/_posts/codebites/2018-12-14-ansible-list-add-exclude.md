---
layout: default
title: "Ansible: Add two lists, then filter with third list"
categories:
- Ansible
- Codebites
hidden: true
---

Playbook:
{% raw %}

```yaml
- Hosts: localhost
  connection: local
  gather_facts: no

  vars:
    - base_list: [1, 2, 3, 4]
    - exclude_list: [2, 4]
    - add_list: [5, 6]

  tasks:
    - debug:
        msg: "{{ base_list | union(add_list) | difference(exclude_list) }}"
```

{% endraw %}
Output:

```bash
$ ansible-playbook list_add_subtract.yml
PLAY [localhost] *******************************************************************************************************************************************

TASK [debug] ***********************************************************************************************************************************************
ok: [localhost] => {
    "msg": [
        1,
        3,
        5,
        6
    ]
}

PLAY RECAP *************************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0
```
