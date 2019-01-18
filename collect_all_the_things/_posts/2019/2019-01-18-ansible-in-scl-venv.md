---
layout: default
title: "Using Python Virtual Environments for Ansible Nodes"
categories:
- Ansible
- Linux
---

Did you ever need a different Python version on an Ansible Node? Or a different Python module version? I did.

The Ansible modules *openssl_certificate* and *openssl_csr* require pyOpenSSL >= 0.15. This is not the case for Red Hat Enterprise Linux 6 servers. The Python installation I wanted to use with Ansible needed to have an enabled Python [SCL](https://www.softwarecollections.org/en/) and an activated Python Virtual Environment (because I didn't want to fiddle with the original SCL modules) before running its commands.

Therefore I created the small shell script `python36-starter.sh`:

```bash
#!/bin/bash
. /opt/rh/rh-python36/enable
. /opt/python-venv/bin/activate
exec python "$@"
```

It's pretty much self-explanatory. By sourcing the `enable` and `activate` files of SCL and Virtual Environment, the correct pathes for Python binaries and libraries are set. Then the "new" Python binary is executed with all arguments the script was called with.

By adding the `ansible_python_interpreter` configuration parameter to the according host in the inventory this script will be used by Ansible in future runs.

```text
[webservers]
prodweb
simuweb
testweb
webcert ansible_python_interpreter=/usr/local/bin/python36-starter.sh
xweb
```

This small hack could be extended even further. You could `export` environment variables in it or do some logging or auditing stuff. But keep in mind this is a dirty hack. Do not give up the freedom and clarity Ansible provides by overextending "quick and dirty" hacks.