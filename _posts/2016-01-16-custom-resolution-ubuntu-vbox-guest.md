---
layout: default
title: "Custom resolution for an Ubuntu Virtual Box guest"
categories:
- Ubuntu
- virtualization
---

I've encountered this problem more often than I like to admit: I got an Ubuntu or Debian based Virtual Box guest and I'd like to change the resolution of the Desktop to one not being enabled by default.
Changing the resolution temporary is easy with `cvt` and `xrandr`.

{% highlight bash %}
export XRES=1152 \
&& export YRES=864 \
xrandr --newmode $(cvt ${XRES} ${YRES}|tail -1| perl -pe 's/^Modeline\ //') \
&& xrandr --addmode $(cvt ${XRES} ${YRES}|tail -1| cut -d ' ' -f2)
{% endhighlight %}

But making the change reboot persistent without using those commands in a startup script took me hours of searching the web several times as I have little knowledge with X11, [only](https://wiki.archlinux.org/index.php/Xrandr) [find](https://wiki.archlinux.org/index.php/Xorg) [parts](http://community.linuxmint.com/tutorial/view/877) of the solution and never documented the steps needed on my own... yet:
<!--more-->
{% include adsense_manual.html %}

Lets roll it up from behind. Here's the end result:  
`/usr/share/X11/xorg.conf.d/10-monitor.conf`
{% highlight kconfig %}
Section "Device"
    Identifier "Device0"
    Driver     "vboxvideo"
EndSection

Section "Monitor"
    Identifier "VGA-0"
  	Modeline "1152x864_60.00"   81.75  1152 1216 1336 1520  864 867 871 897 -hsync +vsync
    Option "PreferredMode" "1152x864_60.00"
EndSection

Section "Screen"
    Identifier "Screen 0"
    Device     "Device0"
    Monitor    "VGA-0"
    DefaultDepth 24
    SubSection "Display"
  		Modes "1152x864_60.00"
    EndSubSection
EndSection
{% endhighlight %}

Most of this is static and can just be copy 'n pasted. There are some parts which are dynamic and some parts which might change, I'd document both so I (hopefully) never want to search the web for a solution again.

**Dynamic parts:**

* The **Modeline** parts can be achieved via `cvt ${XRES} ${YRES}|tail -1|` as I already mentioned before.
* The **Modes** lines were already mentioned as well: `cvt ${XRES} ${YRES}|tail -1| cut -d ' ' -f2`
* You don't need to set **Option "PreferredMode"**, but it's more comfortable.

**Parts that might change:**

* The **Identifier** of the **Section "Monitor"** changed some time in the past. If it does again, it can be achieved via `xrandr |grep 'primary' | cut -d' ' -f1` (as long as there's only one display)
* The **Device** section might change as well. It's unlikely and depending on the change the way to obtain the needed values might differ as well, so I'll update this if I ever encounter a change.

Afterwards restart the Display manager (depends on which flavor of Debian/Ubuntu you are) or just `reboot`.
