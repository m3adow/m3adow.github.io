---
layout: default
title: "Ansible: Cleanly Adding n-dimensional lists"
categories:
- Ansible
- Codebites
---

# "Ansible: Cleanly Adding n-dimensional lists"

Targets:

- Create lists without defining empty variables beforehand
- Add a list of variables as single element to another list

Playbook:
{% raw %}

```yaml
- hosts: localhost

  vars:
    - my_data:
        -
          - a
          - b
        -
          - 1
          - 2
        -
          - z9
          - y9


  tasks:
    - name: Clean list creations
      set_fact:
        my_new_list: "{{ my_new_list | default([]) }} + [['{{ item.0 }}', '{{ item.1 }}']]"
      loop: "{{ my_data }}"
    - debug:
        var: my_new_list
```

{% endraw %}

Output (truncated):

```bash
$ ansible-playbook -v list_variable_examples.yml
PLAY [localhost] *********************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************
ok: [localhost]

TASK [Clean list creations] **********************************************************************************************************************************
ok: [localhost] => (item=['a', 'b']) => {"ansible_facts": {"my_new_list": [["a", "b"]]}, "changed": false, "item": ["a", "b"]}
ok: [localhost] => (item=[1, 2]) => {"ansible_facts": {"my_new_list": [["a", "b"], ["1", "2"]]}, "changed": false, "item": [1, 2]}
ok: [localhost] => (item=['z9', 'y9']) => {"ansible_facts": {"my_new_list": [["a", "b"], ["1", "2"], ["z9", "y9"]]}, "changed": false, "item": ["z9", "y9"]}

TASK [debug] *************************************************************************************************************************************************
ok: [localhost] => {
    "my_new_list": [
        [
            "a",
            "b"
        ],
        [
            "1",
            "2"
        ],
        [
            "z9",
            "y9"
        ]
    ]
}

PLAY RECAP ***************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0
```
