---
layout: default
title: "Compile Blackcoin headless on Raspbian"
categories:
- Crypto currency
- Raspberry Pi
---

As I'm working with my Raspberry Pis again, I wanted to reactivate the wallets of crypto currencies I used to mine some time ago. The Pi is not very potent, so only Proof-of-stake coins qualify. For me those are [Blackcoin](http://blackcoin.co/), [Mintcoin](http://www.mintcoinofficial.com/) and [Reddcoin](https://www.reddcoin.com/) all of which I wanted to run on the Pi. Of course I needed the headless version, I'm not using X11, not even speaking of QT.
So here is the TL;DR for compiling the blackcoind, mintcoind and reddcoind on Raspbian. It is probably the same for every other Debian derivate and most altcoins, independent of architecture or name. I'm taking Blackcoin for my example:

{% highlight bash %}
sudo apt-get install build-essential libssl-dev libdb-dev libdb++-dev libboost-all-dev git
sudo apt-get install libminiupnpc-dev # For UPNP support. You can also set USE_UPNP=0
sudo apt-get install libqrencode-dev # Or set USE_QRCODE=0
git clone https://github.com/rat4/blackcoin/
cd blackcoin/src/
make -f makefile.unix
{% endhighlight %}

That's it. Now drink a coffee or - in my case with the original Raspberry Pi Model B, take a long nap (5 hours compile time). Afterwards you are free to enjoy your own brand new blackcoind.
