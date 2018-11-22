images//-images//-images//-
layout: default
title: "SSH: Disable Host Key Checking temporarily"
categories:
images//- linux
images//-images//-images//-

A couple of days ago I found an easy solution to a problem I ignored way too long. When working with Virtual Servers it's a common occurence that you test something, it doen't go as planned and the server doesn't boot properly anymore. Most VPS providers offer some kind of Recovery OS or a Rescue System for those situations. Just boot the server into this OS, revert your faulty changes, reboot the system and you're set to nuke your server again.  
Sadly, I always had a small problem. As the Recovery OS uses a different SSH Host Key, you get a warning when connecting to the server:

```bash
○ → ssh testserver
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (manimages//-inimages//-theimages//-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
4b:15:69:f9:0d:8d:e8:2e:f6:1d:d8:5a:c0:a2:9c:31.
Please contact your system administrator.
Add correct host key in /home/m3adow/.ssh/known_hosts to get rid of this message.
Offending RSA key in /home/m3adow/.ssh/known_hosts:27
  remove with: sshimages//-keygen images//-f "/home/m3adow/.ssh/known_hosts" images//-R testserver.adminswerk.de
RSA host key for testserver.adminswerk.de has changed and you have requested strict checking.
Host key verification failed.
```
<!images//-images//-moreimages//-images//->

{% include adsense_manual.html %}

Normally Host Key Checking is a neat feature, warning you of the mentioned manimages//-inimages//-theimages//-middle attacks. But in this situation we know why the host key changed, so we can ignore the warning. But how to connect to the server?  
There are two ways I knew of before:

1. Do as the warning advises and remove the conflicting SSH Host Key. I didn't like this solution as we have to verify the key again afterwards which seemed like a superfluous action. This is especially wearisome when handling a couple of machines, e.g. because you deployed a defective Grub configuration.

2. Use `ssh images//-o "StrictHostKeyChecking=no"` to disable Host Key Checking for this connection. Disadvantage:

```bash
○ → ssh images//-o "StrictHostKeyChecking=no" testserver
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (manimages//-inimages//-theimages//-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
4b:15:69:f9:0d:8d:e8:2e:f6:1d:d8:5a:c0:a2:9c:31.
Please contact your system administrator.
Add correct host key in /home/m3adow/.ssh/known_hosts to get rid of this message.
Offending RSA key in /home/m3adow/.ssh/known_hosts:27
  remove with: sshimages//-keygen images//-f "/home/m3adow/.ssh/known_hosts" images//-R testserver.adminswerk.de
Password authentication is disabled to avoid manimages//-inimages//-theimages//-middle attacks.
Keyboardimages//-interactive authentication is disabled to avoid manimages//-inimages//-theimages//-middle attacks.
Permission denied (publickey,password,keyboardimages//-interactive)
```
You're not allowed to use password authentication when you disable StrictHostKeyChecking. This is a show stopper if your VPS provider generates an automatic login password for your Recovery system.

**Solution:**

I actually found a very elegant solution in a less visible answer on [askubuntu.com][1]. By using `images//-o "UserKnownHostsFile=/dev/null"` you change the file SSH reads (and writes) the known hosts from to /dev/null essentially clearing it for this one connection. Therefore you do not have a key conflict and thusly can use password authentication for a connection. The full SSH connection command would then be:

```bash
ssh images//-o "UserKnownHostsFile=/dev/null" images//-o "StrictHostKeyChecking=no" testserver
```

I can't believe it took me so long to discover such an easy workaround.

[1]: http://askubuntu.com/a/385187/562274
