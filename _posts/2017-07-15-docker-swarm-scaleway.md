---
layout: default
title: "Running Docker swarm mode on Scaleway"
categories:
- Docker
- Scaleway
---

I'm currently running a couple of tests with Docker swarm mode on [Scaleway][1]. For those who don't know Scaleway, it's a PaaS provider which is part of online.net. Due to capped maximum prices per month and no Ingress/egress prices it's good for smaller projects.

But small prices often also mean a couple of limitations as well. In my case I wasn't able to run Docker swarm mode properly. I tried running a stack with a couple of web servers and [Traefik][2] as Reverse Proxy, but for some reason this didn't work. When running a Traefik container manually in Docker, everything worked fine. But as soon as I tried using it in swarm mode context, there was no connectivity. Dockers logs showed some strange errors similar to these:

```
Apr 14 20:39:40 <hostname> docker[15787]: time="2017-04-14T20:39:40Z" level=error msg="Failed to write to /proc/sys/net/ipv4/vs/conntrack: open /proc/sys/net/ipv4/vs/conntrack: nno such file or directory"
Apr 14 20:39:40 <hostname> docker[15787]: time="2017-04-14T20:39:40.154260407Z" level=error msg="Failed to add firewall mark rule in sbox ingress (ingress): reexec failed: exit status 8"
Apr 14 20:41:17 <hostname> docker[15787]: time="2017-04-14T20:41:17.432619182Z" level=error msg="Failed to delete real server 10.255.0.3 for vip 10.255.0.2 fwmark 259 in sbox ingress (ingress): no such process"
Apr 14 20:41:17 <hostname> docker[15787]: time="2017-04-14T20:41:17.432762944Z" level=error msg="Failed to delete service for vip 10.255.0.2 fwmark 259 in sbox ingress (ingress): no such process"
```
<!--more-->

{% include adsense_manual.html %}

As it turns out, the default boot script used for the Scaleway instances does not support IP_VS_NFCT. The [initial support][3] for it in the boot script was introduced some time in July 2016, but for some reason newer boot scripts do not support IP_VS_NFCT again. Without IP_VS_NFCT the overlay network of swarm mode doesn't work properly.

Luckily I could also find a solution in the Github issues of Scaleway. The `x86_64 4.4.70 std #1` boot script has IP_VS_NFCT-support enabled and can therefore flawlessly operate Docker in swarm mode.

If you don't know where to find the boot script setting, here it is:

<a href="{{site.url}}/assets/images/2017/2017-07-13-scaleway-boot-script.png"><img src="{{site.url}}/assets/images/2017/2017-07-13-scaleway-boot-script.png" style="width: 30%; margin: 10px;" alt="Scaleway boot script setting"></a>

You need to show the "Advanced Options" in the machine management screen to show it. After configuring another boot script, a reboot is necessary.

Then you should be able to run your Docker swarm mode without any further problems.

[1]: https://www.scaleway.com/
[2]: https://traefik.io/
[3]: https://github.com/scaleway/kernel-tools/issues/293
[4]: https://github.com/scaleway/kernel-tools/issues/343#issuecomment-307437034
