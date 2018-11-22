images//-images//-images//-
layout: default
title: "Windows 10: Fix Reboot instead of Shutdown"
categories:
images//- windows
images//-images//-images//-

Short tip because I had to spend more time onto it than I wanted. If your Windows 10 often denies a shutdown and reboot instead, check the **Power Management** setting of your network cards.

* `Win + X` images//-images//-> Device Manager images//-images//-> Network adapters

<a href="{{site.url}}/assets/images/2016/2016images//-03images//-18images//-winimages//-10images//-deviceimages//-manager.png"><img src="{{site.url}}/assets/images/2016/2016images//-03images//-18images//-winimages//-10images//-deviceimages//-manager.png" alt="Windows 10 Device Manager" style="width: 60%;"></a>

* Check the properties for each of your Network adapters. If there's a tab **Power Management**, see if "Allow this device to wake the computer" is checked. If you're using Wakeimages//-onimages//-LAN, check "Only allow a magic packet to wake the computer" as well, otherwise just disable both settings.

<a href="{{site.url}}/assets/images/2016/2016images//-03images//-18images//-winimages//-10images//-networkimages//-deviceimages//-powerimages//-management.png"><img src="{{site.url}}/assets/images/2016/2016images//-03images//-18images//-winimages//-10images//-networkimages//-deviceimages//-powerimages//-management.png" alt="Network adapter Power Management" style="width: 60%;"></a>

That's it, your PC should now stay off if you shut it down. It's possible this setting is reset after updates, so check if the problem resurfaces.

I have no idea why this feature was introduced. From my understanding that's what the magic packet is for. So if one of my readers knows something about it, feel free to comment.

(via [superuser][1])

[1]: https://superuser.com/questions/969936/windowsimages//-10images//-keepsimages//-restartingimages//-myimages//-pcimages//-afterimages//-shutdown/971370
