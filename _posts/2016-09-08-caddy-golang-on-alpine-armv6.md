---
layout: default
title: "Running Caddy and Go on ARMv6 Alpine Linux"
categories:
- docker
- go
- raspberry pi
- linux
---

My goal was compiling [Caddy][1] for my old Raspberry Pi 1 Model B. Caddy only provides an ARMv7 binary which isn't compatible to the original Pis ARMv6. My Raspi is running on [Hypriot][2], the Docker distribution for the Pi, therefore I wanted Caddy to run in a container as well. I chose my own [Alpine Linux][3] base image as its foundation.

As Caddy is written in Go, compiling it from source should be [very easy][4]:

> 1.  go get github.com/mholt/caddy/caddy
> 2.  cd into your website's directory
> 3.  Run caddy (assuming $GOPATH/bin is in your $PATH)

While trying to get Go running in my Alpine container I encountered a small problem.  
Go officialy provides an [ARMv6 binary package][5], which is able to natively run on the Pi. But when trying to run this package in  my Alpine container, a rather nondescriptive error blocked me:

```bash
/bin/sh: go: not found
```
I admit I needed longer than expected to solve this problem. After `strace`ing, debugging and a lot of Internet research without result, using a simple `file` gave me the deciding hint:

```bash
/go # file $(which go)
/usr/local/go/bin/go: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-armhf.so.3, not stripped
```

Go is looking for `/lib/ld-linux-armhf.so.3` which isn't available on a minimal Alpine Linux installation. Running `apk add libc6-compat` finally solved this problem.

<!--more-->

{% include adsense_manual.html %}

Now compiling Caddy was easy:

1. Set the GOPATH. For me, that dir is simply /go: export GOPATH=/go
2. Run the previously mentioned `go get github.com/mholt/caddy/caddy`. This took ~15 minutes on my Raspberry Pi 1 Model B.

If you want to add additional plugins to caddy, you need to add their sources to the `caddy/caddymain/run.go` file and run `go install github.com/mholt/caddy/caddy` afterwards. Adding the **realip** plugin would look like that:

```
[...]
// plug in the HTTP server type
_ "github.com/mholt/caddy/caddyhttp"

"github.com/mholt/caddy/caddytls"
// This is where other plugins get plugged in (imported)
_ "github.com/captncraig/caddy-realip"

[...]
```

I've created a couple of Dockerfiles and scripts in my [dockerfiles-arm][6] repo which should ease this process for others. Furthermore I've created a couple of containers for the impatient ([Go][7], [Caddy][8]), although I'd recommend the Dockerfiles.

For more info about configuration of Caddy, see the [documentation][97] and the [Github source][10]. I'll try to distribute an automatically compiled binary of Caddy for ARMv6, but I can't promise anything.


[1]: https://caddyserver.com/
[2]: http://blog.hypriot.com/
[3]: https://hub.docker.com/r/container4armhf/armhf-alpine/
[4]: https://github.com/mholt/caddy/blob/master/README.md#running-from-source
[5]: https://golang.org/dl/
[6]:https://github.com/m3adow/dockerfiles-arm
[7]: https://hub.docker.com/r/container4armhf/armhf-golang-bin/
[8]: https://hub.docker.com/r/container4armhf/armhf-caddy/
[9]: https://caddyserver.com/docs
[10]: https://github.com/mholt/caddy
