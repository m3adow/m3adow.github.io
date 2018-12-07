---
layout: default
title: "Simplifying cloud-config creation for clusters"
categories:
- Coreos
- Cloud
---

I'm still experimenting with container orchestration. Currently I'm in the process of building a three node CoreOS cluster with Kubernetes on top of it, connected over the Internet. One problem I was constantly struggling with was keeping my cloud-configs in sync. Most of the configuration settings were identical or nearly identical on all three nodes. Still, when adding a small change, I needed to apply this change to all three files. Forgetting one or mistyping led to errors and unnecessary debugging sessions.

This weekend I decided I've had enough of it. I created a small Python script to simplify working on several nearly identical configuration files, [cloud-config-creator]. By iterating over a set of node values and one master template the script creates the cloud-configs for all nodes. It's little more than a wrapper for the [Jinja2] templating engine, but I still find this incredibly useful. That's why I want to add a bit more explanation around it.

## Prerequisites

You will need Python. I used Python 3, never tested it with 2.x. Furthermore you need to install the `pyyaml` and `jinja2` modules.
Before starting to use `cloud-config-creator` you should have basic knowledge of how to use templates. If you ever worked with a templating engine (e.g. for consul-template or Jekyll), you'll quickly feel at home. Otherwise I recommend the [Jinja2 documentation][jinja2].  
Furthermore you should know how to format [YAML]. My script uses PyYAML, which isn't YAML 1.2 compatible (yet), so you'll need to use YAML 1.1.


## Script usage

```yaml
./cloud-config --templatefile master.tmpl --valuesfile values.yml --outpath out/ --includepath includes/
```

* `--templatefile` for the path to the template. I didn't bother to handle relative pathes properly yet, so either use absolute paths or paths below the current working directory. **This applies to all paths.**
* `--valuesfile` for the path to the values. The script expects this to be a YAML formatted sequence of mappings.
* `--outpath` for the path where all the cloud-configs are created in.
* `--includepath` is optional. If you have a lot of includes, you can put the files into a dedicated directory and specify it.

<!--more-->

{% include adsense_manual.html %}

## Template Examples

### Basic
Lets start with a very simple (and unrealistic) example. You only want to have the hostname of every node set into the cloud-config.

The master template would look like that:
{% raw %}
```yaml
#cloud-config
hostname: {{ my.hostname}}
```
{% endraw %}
The values file would be straightforward as well:

```yaml
-
  hostname: node1.adminswerk.de
-
  hostname: node2.adminswerk.de
-
  hostname: node3.adminswerk.de
```
To be consistent between files, the values file is YAML, just like the template.

Running the script is easy as well:

```bash
./cloud-config-creator.py --templatefile ~/coreos/master.tmpl --valuesfile ~/coreos/values.yml
```

This would create three files in the current directory named *nodeX.adminswerk.de.yml*,  which could then be deployed to the CoreOS nodes. Note how all values of the current node are called via `my.*`.

### Advanced

Now we'll add an etcd2 cluster to the cloud-config. I prefer to have the current node as first one in all endpoint lists (although I'm pretty sure this has no effect on actual endpoint selection). Here's the excerpt from the master template:
{% raw %}
```yaml
coreos:
  etcd2:
    name: "{{ my.etcd.nodename }}"
    data-dir: /var/lib/etcd2
    # clients
    advertise-client-urls: https://{{ my.network.ip }}:2379
    listen-client-urls: https://0.0.0.0:2379
    # peers
    initial-advertise-peer-urls: https://{{ my.network.ip }}:2380
    listen-peer-urls: https://{{ my.network.ip }}:2380
    # cluster
    initial-cluster: {{ my.etcd.nodename }}=https://{{ my.network.ip }}:2380,{% for node in remaining_nodes %}{{ node.etcd.nodename }}=https://{{ node.network.ip }}:2380
            {%- if not loop.last %},{% endif %}{% endfor %}
    initial-cluster-state: new
    initial-cluster-token: etcd-cluster-1
```
{% endraw %}
The values file now looks like this:

```yaml
-
  hostname: node1.adminswerk.de
  network:
    ip: 172.13.37.100
  etcd:
    nodename: node1
-
  hostname: node2.adminswerk.de
  network:
    ip: 172.13.37.101
  etcd:
    nodename: node2
-
  hostname: node3.adminswerk.de
  network:
    ip: 172.13.37.102
  etcd:
    nodename: node3
```

Here, the `initial-cluster` uses a for-loop. The used variable `remaining_nodes` is self-explanatory, it contains all notes except the current which as already explained can be called via `my.*`. If you just wanted to iterate over all nodes, you could use the `nodes` variable for that.  
Also this line uses some [whitespace control][whitespace] to stretch out the templating code for an easier overview and an additional if-clause to prevent a comma after the last node.

If you want to see a more complete example, take a look into the [master-example.tmpl][master-example] and [values-example.yaml][values-example] in the scripts repository.

I will probably distribute more examples in the future, as I plan to publish the templates I'm creating during my experiments.


[cloud-config-creator]: https://github.com/m3adow/cloud-config-creator
[jinja2]: http://jinja.pocoo.org/docs/dev/templates/
[yaml]: http://yaml.org/spec/1.1/
[whitespace]: http://jinja.pocoo.org/docs/dev/templates/#whitespace-control
[master-example]: https://github.com/m3adow/cloud-config-creator/blob/master/master-example.tmpl
[values-example]: https://github.com/m3adow/cloud-config-creator/blob/master/values-example.yml
