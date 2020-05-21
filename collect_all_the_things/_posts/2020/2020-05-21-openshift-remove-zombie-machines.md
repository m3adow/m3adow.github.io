---
layout: default
title: "Openshift: Remove Zombie machines"
categories:
- Openshift
- Kubernetes
---

When an Openshift MachineSet was created with a faulty configuration, Machines created from it may be undeletable by the Controller although the Machines are not existing at all. The status of the Machines will then stay in the “Deleting” state.

```bash
$ oc get machine -n openshift-machine-api
NAME                              PHASE      TYPE              REGION       ZONE   AGE
m3adow-infra-westeurope1-5asrt    Deleting                                         3d2h
m3adow-infra-westeurope1-ioq4z    Running    Standard_D2s_v3   westeurope   1      3d
```

To manually remove the Machine from the API, remove its finalizers via patch:

```bash
oc patch machine -n openshift-machine-api --type=merge -p '{"metadata":{"finalizers":null}}' m3adow-infra-westeurope1-5asrt
```

This will instantly remove it.

