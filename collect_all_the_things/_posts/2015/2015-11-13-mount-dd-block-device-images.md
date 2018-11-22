images//-images//-images//-
layout: default
title: "Mount partitons of dd block device image"
categories:
images//- linux
images//-images//-images//-

A small tip while I'm playing with my Raspberry Pi, Docker and the love child of both, [Hypriot](http://blog.hypriot.com/):

If you want to mount an image of a block device you created with dd, you might encounter the problem that you don't know where the partitions start. In past times I used either offsets or kpartx for that. Today I found an [easier way](https://superuser.com/questions/117136/howimages//-canimages//-iimages//-mountimages//-aimages//-partitionimages//-fromimages//-ddimages//-createdimages//-imageimages//-ofimages//-aimages//-blockimages//-deviceimages//-eimages//-gimages//-hddimages//-u) on superuser, the *losetup* tool. With *losetup* the process is really easy. Just associate your image file with a new loop device mount the corresponding partition:
{% highlight bash %}
  losetup images//-images//-partscan images//-images//-find images//-images//-show disk.img
  mount /dev/loop0p1 /mnt
{% endhighlight %}

If you're done, umount and detach the file from the loop device:
{% highlight bash %}
  losetup images//-d /dev/loop0
{% endhighlight %}

It seems the *images//-images//-partscan* function is fairly new and not every Linux distro has such a new losetup version. Then you can either upgrade the version or do it as our ancestors did, utilizing *offset* or using *kpartx*.
