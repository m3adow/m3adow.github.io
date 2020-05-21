---
layout: default
title: "Ansible: Global defaults with local overwrites via conditional chaining"
categories:
- Ansible
- Codebites
---

Playbook:

```yaml
- hosts: localhost
  connection: local
  gather_facts: no

  vars:
    global_bool: "Global fallback"

  tasks:
    - debug:
        msg: "This uses the global value."
      when: (local_bool is defined and local_bool) or
            (global_bool and local_bool is not defined)
    - set_fact:
        local_bool: True
        global_bool: False
    - debug:
        msg: "This uses the local value."
      when: (local_bool is defined and local_bool) or
            (global_bool and local_bool is not defined)
```

Output:

```bash
$ ansible-playbook conditional_chaining.yml
 [WARNING]: Unable to parse /etc/ansible/hosts as an inventory source

 [WARNING]: No inventory was parsed, only implicit localhost is available

 [WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'


PLAY [localhost] *******************************************************************************************************************************************

TASK [debug] ***********************************************************************************************************************************************
ok: [localhost] => {
    "msg": "This uses the global value."
}

TASK [set_fact] ********************************************************************************************************************************************
ok: [localhost]

TASK [debug] ***********************************************************************************************************************************************
ok: [localhost] => {
    "msg": "This uses the local value."
}

PLAY RECAP *************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0
```
