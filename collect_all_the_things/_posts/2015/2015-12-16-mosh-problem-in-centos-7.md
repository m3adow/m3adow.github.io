---
layout: default
title: "Mosh problem in CentOS 7"
categories:
- Linux
---
While setting up a new server, I encountered a problem with [mosh](https://mosh.mit.edu/). If you don't know mosh, it's an extension to SSH which (among other features) enables instant reconnections after an internet shortage. This is especially useful if you're frequently connecting via mobile network and constantly lose your mobile Internet connection.

However, the problem I encountered was a simple one: Mosh didn't work. Despite opening (and testing) the needed UDP ports in IPtables the server didn't spawn properly. After a bit of debugging I found the error while running the mosh server in verbose mode:

{% highlight bash %}
[m3adow@batman ~]$ mosh-server new -v

MOSH CONNECT 60002 kEK45q7SdtGfP00Op+9Nmw

mosh-server (mosh 1.2.5) [build mosh 1.2.5]
Copyright 2012 Keith Winstein <mosh-devel@mit.edu>
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

[mosh-server detached, pid = 17023]
[m3adow@batman ~]$ forkpty: Operation not permitted
{% endhighlight %}

The "**forkpty: Operation not permitted**" message is the problem indicator. I have yet to find why this happens, but the [solution is simple](http://www.sourcediver.org/blog/2013/12/28/fixing-mosh-on-arch-linux/). Just add the user on the server you want to use mosh with to the `tty` group, e.g. usermod:
{% highlight bash %}
usermod -aG tty my_mosh_user
{% endhighlight %}
Afterwards you should have no more issues `mosh`ing into the server.
