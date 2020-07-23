---
layout: default
title: "Openshift: Change Pull Secret"
categories:
- Openshift
---

**Warning: This procedure will lead to Node drains, node restarts and - as a result pod restarts! Prepare accordingly!** 

To change the pull secret of an Openshift cluster (e.g. because you switched Red Hat accounts), save your new pull secret you downloaded from [cloud.openshift.com][cloud_openshift] in a file, lets call it `my-pull.secret`. Then execute this oc command:

```bash
oc set data secret/pull-secret -n openshift-config \
  --from-file=.dockerconfigjson=my-pull.secret
```

Of course you'll need the proper permissions, I assume it's Cluster Admin, but I didn't test the exact permission requirements.


[cloud_openshift]: https://cloud.openshift.com