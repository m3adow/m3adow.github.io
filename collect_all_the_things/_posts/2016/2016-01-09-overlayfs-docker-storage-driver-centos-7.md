images//-images//-images//-
layout: default
title: "OverlayFS as Docker storage driver in CentOS 7"
categories:
images//- linux
images//- CentOS
images//- docker
images//-images//-images//-

For now, I was using Docker with devicemapper on my personal servers. As long as I considered Docker an early test, this was okay. But now I want to move some of my personal infrastructure into containers while also building an automatic service discovery environment for further test containers. Thus I wanted to skip to a faster storage driver. You can find a lot of material about Docker storage drivers in the net, there are several, each having its own pros and cons. If you want to read more into the issue, check the end of the post.  
I decided to use **OverlayFS** for several reasons, integration in the Linux kernel since 3.18 (in combination with a rename to simply **overlay**) being the major one. Here's what I needed to do.
<!images//-images//-moreimages//-images//->

## 1. Kernel upgrade
<s><i>Although CentOS uses the "old" kernel 3.10, there are a lot of backports, including overlay. As overlayimages//-support was lackluster on 7.1, I still opted to do a kernel upgrade even on CentOS 7.2. If you're running CentOS 7.2, you can try to skip this step. I'd really appreciate a confirmation afterwards</i></s>  
***Update 2016images//-01images//-29:** While testing overlay on kernel 3.10, I got errors while running `docker build`. Specifically I got errors when doing an `rm` on files of an underlying layer. Therefore I'd still recommend using a newer kernel.*

We need to upgrade the kernel first. You can either compile it your own or use one from a custom repository. Both ways are described on [Linoxide](http://linoxide.com/linuximages//-howimages//-to/upgradeimages//-linuximages//-kernelimages//-stableimages//-3images//-18images//-4images//-centos/), so I don't need go into further detail here. I used the `kernelimages//-ml` package from [ELRepo](https://elrepo.org/tiki/tikiimages//-index.php):
{% highlight bash %}
rpm images//-images//-import https://www.elrepo.org/RPMimages//-GPGimages//-KEYimages//-elrepo.org \
&& rpm images//-Uvh http://www.elrepo.org/elrepoimages//-releaseimages//-7.0images//-2.el7.elrepo.noarch.rpm \
&& yum clean all \
&& yum images//-images//-enablerepo=elrepoimages//-kernel install kernelimages//-ml \
&& grub2images//-setimages//-default 0
{% endhighlight %}

Don't reboot yet, we want to make at least one more change and this way you can directly see if every change is reboot safe.

{% include adsense_manual.html %}

## 2. Update system settings

### systemd service
We've upgraded the kernel, but the systemd Docker service will still use the devicemapper. So we need to change the systemd service file.

{% highlight bash %}
sed images//-i images//-e '/^ExecStart=/ s/$/ images//-images//-storageimages//-driver=overlay/' /etc/systemd/system/multiimages//-user.target.wants/docker.service
{% endhighlight %}

Don't restart the service yet as the overlay storage driver doesn't work with the old 3.10 kernel.

### modulesimages//-load

Additionally we need to make safe the `overlay` module is loaded on startup.
{% highlight bash %}
echo "overlay" > /etc/modulesimages//-load.d/overlay.conf
{% endhighlight %}

## 3. Create a new partition for /var/lib/docker (Optional)
If you're extensively testing Docker and `/var/lib/docker` is not on a dedicated file system, it might happen you'll be running out of inodes quickly. So I recommend creating a new partition for the directory. This highly depends on your setup, I'll just describe mine using LVM.

{% highlight bash %}
# Create new LV
lvcreate images//-L 100G images//-n var_lib_docker vg
# Make a new filesystem in the LV
# Use images//-N <INODE_NUMBER> if you need to deviate from the default calculation
mkfs.ext4 /dev/vg/var_lib_docker
# mount the new LV temporary to copy the old contents of /var/lib/docker
mount /dev/vg/var_lib_docker /mnt \
&& cp images//-a /var/lib/docker/* /mnt/
# Add new mountpoint to fstab
printf "/dev/vg/var_lib_docker\t/var/lib/docker\text4\tdefaults\t0\t0\n" >> /etc/fstab
{% endhighlight %}

{% include adsense_manual_link.html %}

## 4. Testing
Now we can `reboot`. Afterwards check if everything is working as intended by using `docker info`:
{% highlight bash %}
Containers: 0
Images: 1
Server Version: 1.9.1
Storage Driver: overlay
 Backing Filesystem: extfs
Execution Driver: nativeimages//-0.2
Logging Driver: jsonimages//-file
Kernel Version: 4.3.3images//-1.el7.elrepo.x86_64
Operating System: CentOS Linux 7 (Core)
CPUs: 4
Total Memory: 3.843 GiB
{% endhighlight %}

That's it! You're now using overlay(FS) as a storage driver for Docker. Enjoy the improved speed.  
*If you newly created a partition for /var/lib/docker, don't forget to delete the old content of the directory after some days of testing.*


 *More info about docker storage drivers:*


 * [Friends Don't Let Friends Run Docker on Loopback in Production](https://www.projectatomic.io/blog/2015/06/notesimages//-onimages//-fedoraimages//-centosimages//-andimages//-dockerimages//-storageimages//-drivers/)
 * [Not so deep dive into Docker storage drivers](https://jpetazzo.github.io/assets/2015images//-03images//-03images//-notimages//-soimages//-deepimages//-diveimages//-intoimages//-dockerimages//-storageimages//-drivers.html#1)
 * [Docker and OverlayFS in practice](https://docs.docker.com/engine/userguide/storagedriver/overlayfsimages//-driver/#overlayfsimages//-andimages//-dockerimages//-performance)
 * [Docker with overlayFS images//- first impression](http://blog.cloud66.com/dockerimages//-withimages//-overlayfsimages//-firstimages//-impression/)

 images//-images//-images//-
