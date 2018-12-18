---
layout: default
title: "Subnautica: Fix 0000000e Access Violation crash"
categories:
- Gaming
- Windows
---

<a href="{{site.url}}/assets/images/2018/2018-12-16-subnautica-banner.pn"><img src="{{site.url}}/assets/images/2018/2018-12-16-subnautica-banner-small.jpg" alt="Subnautica Banner Small"></a>

[Subnautica](https://www.humblebundle.com/store/subnautica?partner=m3adow) is available for free on the [Epic Game Store](https://www.epicgames.com/store/en-US/product/subnautica/home)  until 27th December. It was on my radar for quite some time, so I decided to try it out. Unfortunately on my PC the game crashed before even starting properly. At least it creates crash logs. While most of those were useless to me, one part was constant in all my tries:

```text
Read from location 0000000e caused an access violation
```

This seems to be an error common in many Unity Engine games, not exclusive to Subnautica. Therefore a lot of people experienced this crash issue. Most search results on the Internet recommend disabling overlays. I did that for Steam, Discord, Riva Tuner and f.lux, to no avail.  

{% include adsense_manual.html %}

Finally I found a [forum post](https://forums.unknownworlds.com/discussion/155160/discovered-reason-for-game-crashing-when-launching-access-violation#latest) in the official Subnautica forum which linked this issue to Citrix Workplace, formerly Citrix Connector. I actively use Citrix Workplace for work, so this directly related to my issue. But I didn't want to uninstall the application every time I want to play Subnautica. I tried disabling all of Citrix services (at least I tried, the installation creates a lot of background services), but that didn't help. After some tries I found out that disabling the device "Citrix Virtual Bus Enumerator" in the Device Manager does the trick.

<a href="{{site.url}}/assets/images/2018/2018-12-16-subnautica-device-manager-citrix-virtual-bus.png"><img src="{{site.url}}/assets/images/2018/2018-12-16-subnautica-device-manager-citrix-virtual-bus.png" style="width: 90%; margin: 1em;" alt="Device Manager"></a>

Reenabling the device when I need Citrix or disabling it when I want to play Subnautica is an acceptable burden. For people who want to automate the switch, there are solutions via [batch](https://stackoverflow.com/questions/47530182/enabling-disabling-the-device-in-windows-10-from-command-line) or [Power Shell](https://blog.kulman.sk/enabling-and-disabling-hardware-devices-with-powershell/) available.
