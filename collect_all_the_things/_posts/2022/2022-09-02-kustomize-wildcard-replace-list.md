---
layout: default
title: "Kustomize: Wildcard replace all items of a list"
categories:
- Kubernetes
- Openshift
---

Most users of Kustomize know this problem: You have some kind of list and want to replace the same key in every item of the list in an overlay. Let's say you have a list of `ClusterRules`:

```yaml
---
apiVersion: monitoring.googleapis.com/v1
kind: ClusterRules
metadata:
  name: pods
spec:
  groups:
    - name: main
      interval: 30s
      rules:
        - alert: PodCrashLooping
          expr:  max_over_time(kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff", job="kube-state-metrics"}[5m]) >= 1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Pod '{{ $labels.exported_pod }}' CrashLoopingPod"
        - alert: PodNotHealthy
          expr: max_over_time(kube_pod_status_phase{phase!~"Running|Succeeded"}[5m]) > 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Pod '{{ $labels.exported_pod }}' not healthy"
```

But you want to have a more lenient alerting time in the development environment, as the stuff there tends to break and isn't as important as production. Thusly, we want to patch the `spec.groups[].rules[].for` path. Should be easy, targeting list items with Kustomize `patchesJson6902` method is simple. Sadly, wildcard replacement for list items are not implemented in the JSON Patch standard. To replace each value of the list above, we would need to use a dedicated JSON Patch for each list item:

```yaml
patchesJson6902:
- target:
    version: v1
    group: monitoring.googleapis.com
    kind: ClusterRules
    name: pods
  patch: |-
    - op: replace
      path: /spec/groups/0/rules/0/for
      value: 15m
    - op: replace
      path:/spec/groups/0/rules/1/for
      value: 15m
```

That's okay for two list items like in this example, but becomes tedious if you have a list with many. You could use a Helm template, but depending on the rest of your code, that may be overkill.  
That's why I searched for a better way to programmatically patch all items in a list with Kustomize. And I found an - admittedly very hacky - solution. Entering Kustomize [`replacements`][replacements]. Replacements are the destined successor of Kustomize deprecated `vars` feature which weren't powerful enough in any scenario I wanted to use them for anyways. According to the documentation,

> Replacements are used to copy fields from one source into any number of specified targets.

That's not exactly what we want, we don't have a field...yet. But that's not a problem, right? The simplest solution is to create a `ConfigMap` which contains the wanted key:


```yaml
--- # This CM is only used for Kustomize replacements
apiVersion: v1
kind: ConfigMap
metadata:
  name: alerting-time-replacement-dummy
data:
  for: 15m
```

Refering to that value in the `kustomization.yaml` is not difficult:

```yaml
replacements:
  - source:
      kind: ConfigMap
      name: alerting-time-replacement-dummy
      fieldPath: data.for
    targets:
      - select:
          kind: ClusterRules
          name: pods
        fieldPaths:
        - spec.groups.*.rules.*.for
```

That properly replaces the values as we wanted:

```yaml
---
apiVersion: monitoring.googleapis.com/v1
kind: ClusterRules
metadata:
  name: pods
spec:
  groups:
    - name: main
      interval: 30s
      rules:
        - alert: PodCrashLooping
          expr:  max_over_time(kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff", job="kube-state-metrics"}[5m]) >= 1
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "Pod '{{ $labels.exported_pod }}' CrashLoopingPod"
        - alert: PodNotHealthy
          expr: max_over_time(kube_pod_status_phase{phase!~"Running|Succeeded"}[5m]) > 0
          for: 15m
          labels:
            severity: critical
          annotations:
            summary: "Pod '{{ $labels.exported_pod }}' not healthy"
```

If you dislike the need to have a permanent useless `ConfigMap` in your cluster, I have slightly bad news for you: Using `patchesJson6902` to delete the `ConfigMap` is not possible. Therefore, I recommend coupling this dirty hack with another small hack and using a "no-op" Job with a low `  ttlSecondsAfterFinished` value (available since Kubernetes 1.23) using an annotation as a replacement:

```yaml
---
apiVersion: batch/v1
kind: Job
metadata:
  name: no-op
  annotations:
    # Refer to it via `fieldPath: metadata.annotations.my-replacement-value`
    my-replacement-value: 15m 
spec:
  ttlSecondsAfterFinished: 1
  template:
    spec:
      containers:
      - name: no-op
        # Don't use dynamic tags in production kids, mkay!
        image: busybox:stable 
        command: [":"]
      restartPolicy: Never
```

The job will be deleted nearly instantly, not leaving any trace in your cluster (although churning away some of your resources for a couple of seconds).

[replacements]: https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/replacements/
