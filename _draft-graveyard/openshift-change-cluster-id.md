---
layout: default
title: "Openshift: Change ClusterID"
categories:
- Openshift
---

# Openshift: Change ClusterID

E.g. to move a cluster with a changed Pull Secret to another subscription (may happen in bigger organisations)


```bash
oc edit clusterversion
```

- Edit `spec.clusterID`, use a generated UUID: https://www.uuidgenerator.net/version4
