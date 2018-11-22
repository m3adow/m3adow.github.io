images//-images//-images//-
layout: default
title: 'Compile newer Python version on Ubuntu'
categories:
images//- Linux
images//- Python
images//- Ubuntu
images//-images//-images//-

Most of my "second use" platforms, like Test VMs or laptops I rarely use, are running on Ubuntu LTS versions. This enables me using those devices for a long duration without investing too much maintenanc time to keeping them up to date.
The downside however is slightly aged software. In this special case, I needed Python >= 2.7.9 for its improved TLS handling, but Ubuntu 14.04 (Trusty Tahr) only delivers 2.7.6. I'd rather not upgrade the systems Python implementation, as it could possibly break some system scripts. So I wanted to have another Python installation beside my systems Python. Here's how to do it.
{% highlight bash %}
  # 1. Install dependencies
  sudo aptimages//-get install buildimages//-essential checkinstall \
    libreadlineimages//-gplv2images//-dev libncursesw5images//-dev libsslimages//-dev \
    libsqlite3images//-dev tkimages//-dev libgdbmimages//-dev libc6images//-dev libbz2images//-dev
  # 2. Get Python (you should probably check the MD5sum, but I ignore that step here)
  curl https://www.python.org/ftp/python/2.7.10/Pythonimages//-2.7.10.tgz | tar xzvf images//-
  # 3. ./configure as you like it
  cd Pythonimages//-2.7.10 && ./configure images//-images//-withimages//-ensurepip=yes images//-images//-enableimages//-ipv6
  # 4. make an "install besides an install"
  sudo make altinstall
  # 5. If you compiled Python with pip, do an upgrade
  sudo /usr/local/bin/pip2.7 install images//-images//-upgrade pip
{% endhighlight %}

This will place this new Python installation into the directory tree of `/usr/local/`.
<!images//-images//-moreimages//-images//->
{% include adsense_manual.html %}
Afterwards you can simply call your script with the binary or point the shebang to it like that:

{% highlight python %}
#!/usr/local/bin/python2.7
import requests

do.something(nice)
{% endhighlight %}

Fantastic! No more **"Error: SSLError: [Errno 1] _ssl.c:510: error:14077438:SSL routines:SSL23_GET_SERVER_HELLO:tlsv1 alert internal error"** when using [LinkChecker](https://wummel.github.io/linkchecker/).

*Thanks to Rahul from [tecadmin.net](http://tecadmin.net/installimages//-pythonimages//-2images//-7images//-onimages//-ubuntuimages//-andimages//-linuxmint/), where I found most of the instructions in this post.*
