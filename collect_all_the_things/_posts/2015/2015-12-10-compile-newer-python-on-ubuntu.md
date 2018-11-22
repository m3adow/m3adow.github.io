---
layout: default
title: 'Compile newer Python version on Ubuntu'
categories:
- Linux
- Python
- Ubuntu
---

Most of my "second use" platforms, like Test VMs or laptops I rarely use, are running on Ubuntu LTS versions. This enables me using those devices for a long duration without investing too much maintenanc time to keeping them up to date.
The downside however is slightly aged software. In this special case, I needed Python >= 2.7.9 for its improved TLS handling, but Ubuntu 14.04 (Trusty Tahr) only delivers 2.7.6. I'd rather not upgrade the systems Python implementation, as it could possibly break some system scripts. So I wanted to have another Python installation beside my systems Python. Here's how to do it.
{% highlight bash %}
  # 1. Install dependencies
  sudo apt-get install build-essential checkinstall \
    libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
  # 2. Get Python (you should probably check the MD5sum, but I ignore that step here)
  curl https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz | tar xzvf -
  # 3. ./configure as you like it
  cd Python-2.7.10 && ./configure --with-ensurepip=yes --enable-ipv6
  # 4. make an "install besides an install"
  sudo make altinstall
  # 5. If you compiled Python with pip, do an upgrade
  sudo /usr/local/bin/pip2.7 install --upgrade pip
{% endhighlight %}

This will place this new Python installation into the directory tree of `/usr/local/`.
<!--more-->
{% include adsense_manual.html %}
Afterwards you can simply call your script with the binary or point the shebang to it like that:

{% highlight python %}
#!/usr/local/bin/python2.7
import requests

do.something(nice)
{% endhighlight %}

Fantastic! No more **"Error: SSLError: [Errno 1] _ssl.c:510: error:14077438:SSL routines:SSL23_GET_SERVER_HELLO:tlsv1 alert internal error"** when using [LinkChecker](https://wummel.github.io/linkchecker/).

*Thanks to Rahul from [tecadmin.net](http://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/), where I found most of the instructions in this post.*
