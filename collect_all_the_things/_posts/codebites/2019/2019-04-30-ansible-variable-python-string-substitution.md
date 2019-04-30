---
layout: default
title: "Ansible: Using Python string substituition in variables"
categories:
- Ansible
- Codebites
hidden: true
---

Scenario: Utilize Pythons string substitution in Ansible variables

{% raw %}

```yaml
- hosts: localhost
  connection: local

  vars:
    foobar: ">>%s<<"
    substitution: "adminswerk.de"


  tasks:
    - debug:
        msg: "{{ foobar % substitution }}"
```

{% endraw %}

Output (slightly truncated):

```bash
$ ansible-playbook string_format.yml
PLAY [localhost] **********************************************************************************************************************************************

TASK [debug] **************************************************************************************************************************************************
ok: [localhost] => {
    "msg": ">>adminswerk.de<<"
}

PLAY RECAP ****************************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0
```
