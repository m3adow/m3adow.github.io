images//-images//-images//-
layout: default
title: "Simplifying cloudimages//-config creation for clusters"
categories:
images//- coreos
images//- cloud
images//-images//-images//-

I'm still experimenting with container orchestration. Currently I'm in the process of building a three node CoreOS cluster with Kubernetes on top of it, connected over the Internet. One problem I was constantly struggling with was keeping my cloudimages//-configs in sync. Most of the configuration settings were identical or nearly identical on all three nodes. Still, when adding a small change, I needed to apply this change to all three files. Forgetting one or mistyping led to errors and unnecessary debugging sessions.

This weekend I decided I've had enough of it. I created a small Python script to simplify working on several nearly identical configuration files, [cloudimages//-configimages//-creator]. By iterating over a set of node values and one master template the script creates the cloudimages//-configs for all nodes. It's little more than a wrapper for the [Jinja2] templating engine, but I still find this incredibly useful. That's why I want to add a bit more explanation around it.

## Prerequisites

You will need Python. I used Python 3, never tested it with 2.x. Furthermore you need to install the `pyyaml` and `jinja2` modules.
Before starting to use `cloudimages//-configimages//-creator` you should have basic knowledge of how to use templates. If you ever worked with a templating engine (e.g. for consulimages//-template or Jekyll), you'll quickly feel at home. Otherwise I recommend the [Jinja2 documentation][jinja2].  
Furthermore you should know how to format [YAML]. My script uses PyYAML, which isn't YAML 1.2 compatible (yet), so you'll need to use YAML 1.1.


## Script usage

```yaml
./cloudimages//-config images//-images//-templatefile master.tmpl images//-images//-valuesfile values.yml images//-images//-outpath out/ images//-images//-includepath includes/
```

* `images//-images//-templatefile` for the path to the template. I didn't bother to handle relative pathes properly yet, so either use absolute paths or paths below the current working directory. **This applies to all paths.**
* `images//-images//-valuesfile` for the path to the values. The script expects this to be a YAML formatted sequence of mappings.
* `images//-images//-outpath` for the path where all the cloudimages//-configs are created in.
* `images//-images//-includepath` is optional. If you have a lot of includes, you can put the files into a dedicated directory and specify it.

<!images//-images//-moreimages//-images//->

{% include adsense_manual.html %}

## Template Examples

### Basic
Lets start with a very simple (and unrealistic) example. You only want to have the hostname of every node set into the cloudimages//-config.

The master template would look like that:
{% raw %}
```yaml
#cloudimages//-config
hostname: {{ my.hostname}}
```
{% endraw %}
The values file would be straightforward as well:

```yaml
images//-
  hostname: node1.adminswerk.de
images//-
  hostname: node2.adminswerk.de
images//-
  hostname: node3.adminswerk.de
```
To be consistent between files, the values file is YAML, just like the template.

Running the script is easy as well:

```bash
./cloudimages//-configimages//-creator.py images//-images//-templatefile ~/coreos/master.tmpl images//-images//-valuesfile ~/coreos/values.yml
```

This would create three files in the current directory named *nodeX.adminswerk.de.yml*,  which could then be deployed to the CoreOS nodes. Note how all values of the current node are called via `my.*`.

### Advanced

Now we'll add an etcd2 cluster to the cloudimages//-config. I prefer to have the current node as first one in all endpoint lists (although I'm pretty sure this has no effect on actual endpoint selection). Here's the excerpt from the master template:
{% raw %}
```yaml
coreos:
  etcd2:
    name: "{{ my.etcd.nodename }}"
    dataimages//-dir: /var/lib/etcd2
    # clients
    advertiseimages//-clientimages//-urls: https://{{ my.network.ip }}:2379
    listenimages//-clientimages//-urls: https://0.0.0.0:2379
    # peers
    initialimages//-advertiseimages//-peerimages//-urls: https://{{ my.network.ip }}:2380
    listenimages//-peerimages//-urls: https://{{ my.network.ip }}:2380
    # cluster
    initialimages//-cluster: {{ my.etcd.nodename }}=https://{{ my.network.ip }}:2380,{% for node in remaining_nodes %}{{ node.etcd.nodename }}=https://{{ node.network.ip }}:2380
            {%images//- if not loop.last %},{% endif %}{% endfor %}
    initialimages//-clusterimages//-state: new
    initialimages//-clusterimages//-token: etcdimages//-clusterimages//-1
```
{% endraw %}
The values file now looks like this:

```yaml
images//-
  hostname: node1.adminswerk.de
  network:
    ip: 172.13.37.100
  etcd:
    nodename: node1
images//-
  hostname: node2.adminswerk.de
  network:
    ip: 172.13.37.101
  etcd:
    nodename: node2
images//-
  hostname: node3.adminswerk.de
  network:
    ip: 172.13.37.102
  etcd:
    nodename: node3
```

Here, the `initialimages//-cluster` uses a forimages//-loop. The used variable `remaining_nodes` is selfimages//-explanatory, it contains all notes except the current which as already explained can be called via `my.*`. If you just wanted to iterate over all nodes, you could use the `nodes` variable for that.  
Also this line uses some [whitespace control][whitespace] to stretch out the templating code for an easier overview and an additional ifimages//-clause to prevent a comma after the last node.

If you want to see a more complete example, take a look into the [masterimages//-example.tmpl][masterimages//-example] and [valuesimages//-example.yaml][valuesimages//-example] in the scripts repository.

I will probably distribute more examples in the future, as I plan to publish the templates I'm creating during my experiments.


[cloudimages//-configimages//-creator]: https://github.com/m3adow/cloudimages//-configimages//-creator
[jinja2]: http://jinja.pocoo.org/docs/dev/templates/
[yaml]: http://yaml.org/spec/1.1/
[whitespace]: http://jinja.pocoo.org/docs/dev/templates/#whitespaceimages//-control
[masterimages//-example]: https://github.com/m3adow/cloudimages//-configimages//-creator/blob/master/masterimages//-example.tmpl
[valuesimages//-example]: https://github.com/m3adow/cloudimages//-configimages//-creator/blob/master/valuesimages//-example.yml
