---
layout: default
title: "Ubuntu: How to fix the No Wi-Fi password dialogue error"
categories:
- linux
- Ubuntu
---

I recently stumbled over a problem on my notebook running Ubuntu 16.04 "Xenial Xerus". When trying to connect to a new, protected Wi-Fi network no password dialogue appeared, making a quick GUI connection impossible. Creating the connection manually, entering the Wi-Fi password in the "Wi-Fi-Security"  setting in the process worked like a charm. Using `nmtui` from the terminal also worked flawlessly.

As I didn't connect the notebook to new Wi-Fi networks in months, I didn't encounter this error for a long time. Therefore I had a lot of problems debugging it as I installed bazillions of updates and new packages in the meantime.

I narrowed the problem down to NetworkManager not having a way of saving the Wi-Fi password, which is normally done via `gnome-keyring`, specifically via `gnome-keyring-daemon`. The daemon didn't seem to start properly, but even starting it manually still didn't make a difference. The logs still complained:

```
Okt 17 06:58:53 XPS13 NetworkManager[1064]: <info>  [1508216333.3058] device (wlan0): Activation: (wifi) access point 'MyTest' has security, but secrets are required.
Okt 17 06:58:53 XPS13 NetworkManager[1064]: <info>  [1508216333.3062] device (wlan0): state change: config -> need-auth (reason 'none') [50 60 0]
Okt 17 06:58:53 XPS13 NetworkManager[1064]: <warn>  [1508216333.3062] device (wlan0): No agents were available for this request.
```

Finally I found the solution in an [askubuntu question](https://askubuntu.com/a/936051). Nearly half a year ago I installed [Flatpak](http://flatpak.org/) so I could install [FeedReader](https://jangernert.github.io/FeedReader/). One of the dependencies was `dbus-user-session`. This package seems to have problems with the `gnome-keyring-daemon` in 16.04 rendering it defective. Purging the `dbus-user-session` package and its dependencies solved my problem and the Wi-Fi password dialogue appeared once again.

```bash
apt purge dbus-user-session xdg-desktop-portal xdg-desktop-portal-gtk
```

<a href="{{site.url}}/assets/images/2017/2017-10-17-ubuntu-wifi-security-dialogue.png"><img src="{{site.url}}/assets/images/2017/2017-10-17-ubuntu-wifi-security-dialogue.png" style="width: 80%; margin: 10px;" alt="Wi-Fi dialogue"></a>

I still had a problem with the NetworkManager applet in the tray, but this could be fixed with an `apt install --reinstall network-manager-gnome` and a reboot afterwards.
