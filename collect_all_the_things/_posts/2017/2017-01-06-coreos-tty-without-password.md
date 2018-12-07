---
layout: default
title: "Container Linux: Get a TTY without password"
categories:
- Coreos
---

I've been experimenting a lot with CoreOS Container Linux (formerly simply CoreOS). One of the issues I've had regularly was getting my cloud-config to the server after an initial install. There's no meta data drive or something similar on bare metal servers or normal VPS.

Easy solution: [Bypass the authentication][1]. If you have access to a VNC or something similar, you can add `coreos.autologin=tty0` (or just omit the `=tty0`) kernel option to get to a login shell directly.
If you don't know where to put that, it needs to be put in the Grub command line. Here's an image of it.

<a href="{{site.url}}/assets/images/2017/2017-01-06-container-linux-grub-cmd.png"><img src="{{site.url}}/assets/images/2017/2017-01-06-container-linux-grub-cmd.png" alt="Container Linux Grub" style="width: 60%;"></a>

So you need to press `e` in the Grub menu, enter the option behind the original options (in my case I put it behind `$linux_cmdline`) and press Ctrl+x or F10 afterwards to boot with it.

That's it, your window will now put you into a login shell of the coreos user and you'll be able to `curl` cloud-config.


[1]: https://coreos.com/os/docs/latest/booting-with-iso.html#bypass-authentication
