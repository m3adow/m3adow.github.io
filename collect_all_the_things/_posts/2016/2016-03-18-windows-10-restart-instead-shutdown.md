---
layout: default
title: "Windows 10: Fix Reboot instead of Shutdown"
categories:
- Windows
---

Short tip because I had to spend more time onto it than I wanted. If your Windows 10 often denies a shutdown and reboot instead, check the **Power Management** setting of your network cards.

* `Win + X` --> Device Manager --> Network adapters

<a href="{{site.url}}/assets/images/2016/2016-03-18-win-10-device-manager.png"><img src="{{site.url}}/assets/images/2016/2016-03-18-win-10-device-manager.png" alt="Windows 10 Device Manager" style="width: 60%;"></a>

* Check the properties for each of your Network adapters. If there's a tab **Power Management**, see if "Allow this device to wake the computer" is checked. If you're using Wake-on-LAN, check "Only allow a magic packet to wake the computer" as well, otherwise just disable both settings.

<a href="{{site.url}}/assets/images/2016/2016-03-18-win-10-network-device-power-management.png"><img src="{{site.url}}/assets/images/2016/2016-03-18-win-10-network-device-power-management.png" alt="Network adapter Power Management" style="width: 60%;"></a>

That's it, your PC should now stay off if you shut it down. It's possible this setting is reset after updates, so check if the problem resurfaces.

I have no idea why this feature was introduced. From my understanding that's what the magic packet is for. So if one of my readers knows something about it, feel free to comment.

(via [superuser][1])

[1]: https://superuser.com/questions/969936/windows-10-keeps-restarting-my-pc-after-shutdown/971370
