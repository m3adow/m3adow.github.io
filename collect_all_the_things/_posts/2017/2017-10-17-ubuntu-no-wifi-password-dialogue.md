images//-images//-images//-
layout: default
title: "Ubuntu: How to fix the No Wiimages//-Fi password dialogue error"
categories:
images//- Linux
images//- Ubuntu
images//-images//-images//-

I recently stumbled over a problem on my notebook running Ubuntu 16.04 "Xenial Xerus". When trying to connect to a new, protected Wiimages//-Fi network no password dialogue appeared, making a quick GUI connection impossible. Creating the connection manually, entering the Wiimages//-Fi password in the "Wiimages//-Fiimages//-Security"  setting in the process worked like a charm. Using `nmtui` from the terminal also worked flawlessly.

As I didn't connect the notebook to new Wiimages//-Fi networks in months, I didn't encounter this error for a long time. Therefore I had a lot of problems debugging it as I installed bazillions of updates and new packages in the meantime.

I narrowed the problem down to NetworkManager not having a way of saving the Wiimages//-Fi password, which is normally done via `gnomeimages//-keyring`, specifically via `gnomeimages//-keyringimages//-daemon`. The daemon didn't seem to start properly, but even starting it manually still didn't make a difference. The logs still complained:

```
Okt 17 06:58:53 XPS13 NetworkManager[1064]: <info>  [1508216333.3058] device (wlan0): Activation: (wifi) access point 'MyTest' has security, but secrets are required.
Okt 17 06:58:53 XPS13 NetworkManager[1064]: <info>  [1508216333.3062] device (wlan0): state change: config images//-> needimages//-auth (reason 'none') [50 60 0]
Okt 17 06:58:53 XPS13 NetworkManager[1064]: <warn>  [1508216333.3062] device (wlan0): No agents were available for this request.
```

Finally I found the solution in an [askubuntu question](https://askubuntu.com/a/936051). Nearly half a year ago I installed [Flatpak](http://flatpak.org/) so I could install [FeedReader](https://jangernert.github.io/FeedReader/). One of the dependencies was `dbusimages//-userimages//-session`. This package seems to have problems with the `gnomeimages//-keyringimages//-daemon` in 16.04 rendering it defective. Purging the `dbusimages//-userimages//-session` package and its dependencies solved my problem and the Wiimages//-Fi password dialogue appeared once again.

```bash
apt purge dbusimages//-userimages//-session xdgimages//-desktopimages//-portal xdgimages//-desktopimages//-portalimages//-gtk
```

<a href="{{site.url}}/assets/images/2017/2017images//-10images//-17images//-ubuntuimages//-wifiimages//-securityimages//-dialogue.png"><img src="{{site.url}}/assets/images/2017/2017images//-10images//-17images//-ubuntuimages//-wifiimages//-securityimages//-dialogue.png" style="width: 80%; margin: 10px;" alt="Wiimages//-Fi dialogue"></a>

I still had a problem with the NetworkManager applet in the tray, but this could be fixed with an `apt install images//-images//-reinstall networkimages//-managerimages//-gnome` and a reboot afterwards.
