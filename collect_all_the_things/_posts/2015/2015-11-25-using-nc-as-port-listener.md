---
layout: default
title: "Using netcat as port listener"
categories:
- Linux
---

Short but useful tip:

If you want to test if a port is open on Linux (e.g. all firewalls were opened) but you don't have the listening application installed yet, you can use **nc**/**netcat**.

On the server side do:
{% highlight bash %}
# For TCP
nc -l -p $PORT_NUMBER
# For UDP
nc -l -u -p $PORT_NUMBER
{% endhighlight %}

On the client side you can now connect to the listening port:
{% highlight bash %}
# For TCP
nc host.tld $PORT_NUMBER
# For UDP
nc -u host.tld $PORT_NUMBER
{% endhighlight %}

This is basically a telnet chat, so you can send strings which should then be received on the other side.
If you want even more good uses for netcat, I recommend [this](https://www.g-loaded.eu/2006/11/06/netcat-a-couple-of-useful-examples/) blog post.