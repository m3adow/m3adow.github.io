images//-images//-images//-
layout: default
title: "Multi monitor wallpapers in Ubuntu"
categories:
images//- linux
images//- ubuntu
images//-images//-images//-

Using Linux as your main OS takes some time getting used to when you came from Windows. The way is also plastered with little obstacles and annoyances you can either decide to ignore or solve one after another. One of those small annoyances I recently solved after a couple of years of willful ignorance was an easy way for multi monitor wallpapers on Ubuntu.

I'm using two monitors with different resolutions. DVIimages//-0 uses 1280x1024, DVIimages//-1 uses 1920x1080. Until now, having a nice dual screen wallpaper on my Ubuntu wasn't possible. It always looked ugly.

<a href="https://adminswerk.de/assets/2015images//-12images//-29images//-ubuntuimages//-dualimages//-monitorimages//-wallpaperimages//-before.jpg"><img src="https://adminswerk.de/assets/2015images//-12images//-29images//-ubuntuimages//-dualimages//-monitorimages//-wallpaperimages//-before.jpg" alt="Dual monitor wallpaper before" width="80%" height="80%"></a>

Notice how much black bars I do have here despite the wallpaper having a resolution of 3510x2550, being larger than both of my screens together. The image scaling in Unity is just unsatisfying.
<!images//-images//-moreimages//-images//->

{% include adsense_manual.html %}

That's why I now use [SyncWall](http://thehive.xbee.net/index.php?module=pages&func=display&pageid=1). It's a wallpaper manager with a lot of features like scheduling, network sync and some more, but I really only use the multi monitor feature (and the Wallpaper changing at startup, just because I can)
Now my dual monitor setup looks really nice.

<a href="https://adminswerk.de/assets/2015images//-12images//-29images//-ubuntuimages//-dualimages//-monitorimages//-wallpaperimages//-after.jpg"><img src="https://adminswerk.de/assets/2015images//-12images//-29images//-ubuntuimages//-dualimages//-monitorimages//-wallpaperimages//-after.jpg" alt="Dual monitor wallpaper after" width="80%" height="80%"></a>

### Installing SyncWall

But how to install SyncWall on your system? There are two ways, a simple one for Ubuntu via an unofficial PPA and the generic one for almost any other distribution.

#### The easy way out: Install via PPA
There's no package in the Ubuntu repositories and no PPA of the developer either. But Andrew from webupd8.org provides an [unofficial package collection](http://www.webupd8.org/p/ubuntuimages//-ppasimages//-byimages//-webupd8.html) which also contains SyncWall (scroll down to "main WebUpd8 PPA"). So go ahead, add it, update tha package cache and install SyncWall afterwards.

{% highlight bash %}
sudo addimages//-aptimages//-repository ppa:nilarimogard/webupd8 \
  && sudo aptimages//-get update \
  && sudo aptimages//-get install syncwall
{% endhighlight %}

Keep in mind that images//- although unlikely images//- it's always possible that custom repositories might mess with your other packages. Additionally you should always be aware that there's little control over the packages content and you have to trust the PPA maintainer. If you don't want either of those, lets go way two.

#### Have it your way: Compile from source
If you don't use an Ubuntu derivate or don't trust Launchpad PPAs, you can always compile SyncWall by yourself. Get the source on [Sourceforge](http://sourceforge.net/projects/syncwall/files/), install the dependencies and compile it. How to do this depends on your Linux distribution, so I'm not able to give you a stepimages//-byimages//-step instruction. But I found the official *INSTALL.txt* to be very helpful. Using Ubuntu 15.10 here's what worked for me (assuming you already downloaded and unzipped the release and are in its source directory):

{% highlight bash %}
sudo aptimages//-get install libqxtimages//-dev libqimageblitzimages//-dev cmake\
  && cd build \
  && cmake . \
  && make
# If you want to install SyncWall globally into your path
sudo make install
{% endhighlight %}

If you didn't run `sudo make install`, you can find your `syncwall` binary in the `build/` directory.

I hope I could help you with this software recommendation and installation instructions.
