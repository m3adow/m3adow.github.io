---
layout: default
title: "OpenWRT: Upgrade all packages with opkg"
categories:
- Codebites
- OpenWRT
hidden: true
---
I'm using OpenWRT on my [Linksys WRT3200ACM][wrt_amazon]. As the integrated package manager `opkg` does not have a pendant to `apt-get dist-upgrade`, this is the command I regularly execute, to upgrade the system:

```bash
opkg update && opkg list-upgradable| awk '{print $1}'| tr '\n' ' '| xargs -r opkg upgrade
```

I recommend running this command in a session detached from SSH. This way you're safe in case your machine or the router get network problems. I've ran into that problem once which cost me a couple of hours for debuggin. Therefor I run the command in a detached tmux session:

```bash
tmux new -d "opkg update && opkg list-upgradable| awk '{print $1}'| tr '\n' ' '| xargs -r opkg upgrade"
```

If you are brave, you can automate this via cron. I prefer doing supervised updates regularly, as my router is a rather critical part of my infrastructure.

[wrt_amazon]: https://www.amazon.com/Linksys-Dual-Band-Wireless-Tri-Stream-WRT3200ACM/dp/B01JOXW3YE/ref=as_li_ss_tl?ie=UTF8&qid=1548752349&sr=8-3&keywords=linksys+wrt3200acm&linkCode=ll1&tag=admwer-20&linkId=c3e0a952da7522ba7ac2630c7fce2c8f