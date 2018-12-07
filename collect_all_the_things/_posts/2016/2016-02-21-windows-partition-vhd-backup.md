---
layout: default
title: "Backup Windows partitions as virtual hard disk (VHD)"
categories:
- Windows
- Virtualization
---

Although I prefer Linux as Desktop OS, Gaming on it is still very hard to realize. That's why I need a Windows installation on my system. Said installation didn't age well, so I decided to rejuvenate my six year old Windows installation and install Windows 10.

I wanted to have a fresh start and didn't want to keep anything, but I still wanted to retain my old system and data partition as backup. I decided to use a Virtual Hard Disk (VHD) file as backup format. The advantage of this is that I can easily boot up a VM to compare my old system with my new one. Additionally Windows 7 [natively supports mounting VHD][1], enabling easy access to the files. Thus, I created a step-by-step instruction for later reference.

### Prerequisite

* For this process you will need about twice the size of your partition as disk space. The resulting image will be roughly the same size as the original.  
* Of course I used Linux to do all of those steps. If you don't have a Linux installation, use a Live USB stick with a distribution of your choice.

<!--more-->

{% include adsense_manual.html %}
### Backup

* unmount the partition you want to backup if it's mounted

{% highlight bash %}
umount /dev/sda2
{% endhighlight %}

* use <code>ntfsclone</code> to create an image excluding unused partition space

{% highlight bash %}
ntfsclone -o /mnt/20160220-win_c_drive_ntfsclone.img /dev/sda2
{% endhighlight %}

*Update 2016-03-18: I removed usage of the `-s` switch because it makes the resulting VHDs unreadable.*

* Install VirtualBox if not already installed, we need VBoxManage

{% highlight bash %}
apt-get update && apt-get install --yes virtualbox
{% endhighlight %}

* Use VBoxManage to convert the ntfsclone image to a VHD

{% highlight bash %}
VBoxManage convertfromraw /mnt/20160220-win_c_drive_ntfsclone.img \
  /mnt/20160220-win_c_drive_ntfsclone.vhd --format VHD
{% endhighlight %}

This process may take some time, but afterwards you have your VHD backup ready to go.

[1]: http://blogs.technet.com/b/danstolts/archive/2012/11/09/how_2d00_to_2d00_mount_2d00_vhd_2d00_image_2d00_from_2d00_windows_2d00_7_2d00_step_2d00_by_2d00_step_2d00_without_2d00_any_2d00_third_2d00_party_2d00_toolsthe_2d00_easy_2d00_way.aspx
