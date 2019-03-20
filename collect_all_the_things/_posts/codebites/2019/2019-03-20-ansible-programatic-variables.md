---
layout: default
title: "Ansible: Using programatically constructed variables"
categories:
- Ansible
- Codebites
hidden: true
---

Scenario:

Use specific variables, depending on the environment a playbook is run in. In this example either a low load or high load environment

Playbook:
{% raw %}

```yaml
- hosts:
    - localhost
  gather_facts: no

  vars:
    - lowload_app_java_opts: "-Xms512m -Xmx2G"
    - highload_app_java_opts: "-Xms4G -Xmx8G"
    - services:
        - lowload_app
        - highload_app

  tasks:
    - debug:
       msg: "fixed_var: {{ lookup('vars', service_name + '_java_opts') }}"
      loop: "{{ services }}"
      loop_control:
        loop_var: service_name
```

{% endraw %}
Output (truncated):

```bash
$ ansible-playbook -v programatic_variable_lookup.yml
PLAY [localhost] *******************************************************************

TASK [debug] ***********************************************************************
ok: [localhost] => (item=lowload_app) => {
    "msg": "fixed_var: -Xms512m -Xmx2G"
}
ok: [localhost] => (item=highload_app) => {
    "msg": "fixed_var: -Xms 4G -Xmx8G"
}

PLAY RECAP *************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0
```