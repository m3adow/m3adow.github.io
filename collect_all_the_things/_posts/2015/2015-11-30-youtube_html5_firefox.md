---
layout: default
title: "Ubuntu: Full Youtube HTML5 Player support for Firefox"
categories:
- linux
- firefox
---
**Problem:** Firefox on Ubuntu doesn't support the whole spectrum of HTML5 features Youtube provides.

<a href="https://adminswerk.de/assets/2015-11-29-YouTube-HTML5-Firefox.png"><img src="https://adminswerk.de/assets/2015-11-29-YouTube-HTML5-Firefox.png" alt="Youtube HTML5 unsupported Features" width="60%" height="60%"></a>

**Solution:**

Switching the following **about:config** Settings to **true**:

{% highlight python %}
media.mediasource.webm.enabled
media.mediasource.enabled
media.fragmented-mp4.exposed
media.fragmented-mp4.ffmpeg.enabled
media.fragmented-mp4.gmp.enabled
{% endhighlight %}
<!--more-->
{% include adsense_manual.html %}

**Result:**

Youtube is satisfied:

<a href="https://adminswerk.de/assets/2015-11-29-YouTube-HTML5-Firefox-all-enabled.png"><img src="https://adminswerk.de/assets/2015-11-29-YouTube-HTML5-Firefox-all-enabled.png" alt="Youtube HTML5 all supported" width="60%" height="60%"></a>

I found a lot of tipps to install *ubuntu-restricted-extras* or *x264*, but I have yet to run into any errors without having those packages installed. These instructions were tested on a couple of my systems running Firefox 42 and either Ubuntu 14.04 (Trusty Tahr) or Ubuntu 15.10 (Wily Werewolf), so this might not work in earlier versions of Ubuntu or might not be needed in later Firefox versions. I found it also worked in Windows 7, but didn't thoroughly test that.
