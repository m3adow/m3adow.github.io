---
layout: default
title: "Redirecting ports with iptables"
categories:
- linux
---

From time to time I need to test the connectivity of applications listening on a port which has not yet been opened in the firewall. Therefore I use iptables to redirect an open port to the port the application is listening on. Lets assume I want to redirect port 80 to 8080 and port 443 to port 8443. Here's how to do it:

First enable IP Forwarding
```
sysctl -w net.ipv4.ip_forward=1
```
Afterwards enable the redirection for said ports
```bash
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8443
```
*Optional:* If you also want to redirect the port on the local machine, you have to set an additional iptables rule
```bash
iptables -t nat -I OUTPUT -p tcp -o lo --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -I OUTPUT -p tcp -o lo --dport 443 -j REDIRECT --to-port 8443
```

This is of course not reboot safe. For reboot safety you need to set `ip_forward` in the `/etc/sysctl.conf` or a respective `/etc/sysctl.d/` file and use the `iptables-restore` functionality of your distribution.

**PS:** This could of course also be used to circumvent firewall restrictions, e.g. to connect to SSH via another port without reconfiguring sshd. Do this at your own risk!