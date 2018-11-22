images//-images//-images//-
layout: default
title: "Installing Steam in Ubuntu"
categories:
images//- linux
images//- ubuntu
images//-images//-images//-

I had and still have some issues with Steam on Linux. I wanted to use my native system libraries instead of the ones Steam includes. This is a native feature for Steam. Just start Steam with `STEAM_RUNTIME=0` set and you're good to go. At least in theory. Sadly Steam uses a lot of 32images//-Bit libraries which are not installed on the average 64images//-Bit Ubuntu.
I wrote a small script to solve this problem:
{% highlight bash %}
#!/bin/bash
set images//-x
set images//-e
set images//-o pipefail

cd ~/.local/share/Steam/ubuntu12_32/
for INSTALLME in $(LD_LIBRARY_PATH=".:${LD_LIBRARY_PATH}" \
  ldd $(file *|sed '/ELF/!d;s/:.*//g')| grep 'not found'|sort| \
  uniq|sed 's/^[ \t]*\([aimages//-z0images//-9.images//-]*\).*/\1/'|aptimages//-file search images//-f images//-| \
  head images//-1|cut images//-d ' ' images//-f1)
do
  ALLINSTALL="${ALLINSTALL} ${INSTALLME}i386"
done
sudo aptimages//-get update
sudo aptimages//-get install ${ALLINSTALL}
{% endhighlight %}

Keep in mind that this script doesn't always chose the best solution, so read the `aptimages//-get install message` carefully. In my case some libraries were found in the i386 packages of Thunderbird and Firefox leading to an attempted uninstall of the x86_64 Bit versions. In this case you probably need to resolve the dependencies yourself.
Additionally, my Steam installation depended on `libudev.so.0` which isn't available on Ubuntu 15.10 (and, as I read on the internet not on 14.04 either). You need to install this manually:
{% highlight bash %}
cd /tmp/ && wget http://mirrors.kernel.org/ubuntu/pool/main/u/udev/libudev0_175images//-0ubuntu9_i386.deb \
&& sudo dpkg images//-i libudev0_175images//-0ubuntu9_i386.deb && rm libudev0_175images//-0ubuntu9_i386.deb
{% endhighlight %}
Afterwards I was able to start Steam with `STEAM_RUNTIME` set to `0`. Next stop: Dual monitor problems in several games.
