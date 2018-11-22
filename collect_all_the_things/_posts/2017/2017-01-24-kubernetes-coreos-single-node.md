---
layout: default
title: "Kubernetes Single Node installation on CoreOS Container Linux"
categories:
- docker
- Linux
- coreos
---

I've been playing with Kubernetes on CoreOS Container Linux for a couple of months now. As I prefer to implement real world workloads instead of examples, I planned on containerising a couple of applications my family and I rely on. Beforehand I wanted to create an easy way for installing a Kubernetes cluster spread across multiple VPS providers, securely connected over the internet via VPN or something similar. I did a [speed test][1] for initial evaluation of different methods and began working on a proof of concept [CoreOS Kubernetes cluster secured via tinc][2]. This prove more difficult than initially planned, taking me months for a simple setup and setting me back multiple times.  

Therefore I settled with a Kubernetes installation residing on a single node. The clustering was a bit overkill for family applications anyways and this step just took to much time. For the Single Node installation I found a [blog entry][3] from Victor Palau who also created a GitHub repository for an automated Kubernetes installation to an existing Container Linux server. I tested his script on my server from [Chicago VPS][cvpsaffi] and although it largely worked, I was dissatisfied. As the script was initially intended to be run on Microsofts Azure, the requirements a bare metal installation has were not taken into account:  
A couple of ports meant for internal use only were publicy accessible, insecure etcd2 being the worst one. Furthermore I didn't like the apiserver listening on port 443. While on Azure you'd normaly prepend a Load balancer in front of the Single node, this doesn't apply to a Bare Metal installation. Thusly HTTPS was effectively blocked on the node and there was no easy way for integrating a containerised load balancer like [Træfɪk][4]. Addtionally there were some smaller problems or additions I had in mind and wanted to integrate into the automation to ease installations for others and a possible reinstallation for myself.

<!--more-->

{% include adsense_manual.html %}

So I took Victors script and expanded it to be more "Individual Production Ready" by:

* changing the published port of the API server to 6443
* enabling IPtables for port 2379 and 10250-10255 only permitting access from the own IP
* properly integrating kube-dns (not sure about that, didn't work properly in my setup with Victors script)
* enabling Basic Authentication for the API server via random username and password
* integrating an automatic deployment of Kubernetes Dashboard which is accessible via said Basic Authentication

If you want to check it out, you'll obviously need a running CoreOS Container Linux installation. The steps you have to do on the server are quite simple:

```bash
git clone https://github.com/m3adow/k8single
cd k8single
./kubeform.sh [myip-address] [DNS entry for K8s apiserver (optional)]
```

You can use the second argument on `kubeform.sh` to add an additional FQDN to your API server if you want to use a FQDN for connection instead of an IP.  
Afterwards you should be able to access the dashboard via `https://fqdn-of-your-server.com:6443/ui` authenticating with the credentials the script displayed at the end.

I still hope I can revisit my project to get a secured Baremetal Kubernetes cluster running one day, but for now this Single Node installation satisfies my needs. If you have any questions or remarks, feel free to comment.

[cvpsaffi]: https://billing.chicagovps.net/aff.php?aff=632
[1]: https://github.com/m3adow/coreos-secure-node-to-node
[2]: https://github.com/m3adow/coreos-kubernetes-tinc-cluster
[3]: https://victorpalau.net/2016/09/04/single-node-kubernetes-deployment/
[4]: https://traefik.io/
