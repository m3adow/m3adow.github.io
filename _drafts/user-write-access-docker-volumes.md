---
layout: default
title: "Write access for normal users on docker volumes"
categories:
- docker
---

One of the pitfalls I constantly run into while using docker is user access, especially write access to host volumes.

## The problem

When mounting a volume, all permissions remain the same in the container. If the user the file belong to on the host uses an ID (UID or GID) not existing in the container, it belongs to an unknown user. While this is normal behaviour for \*NIX systems, this is a problem when using containers. As long as your application in the container runs as root, this doesn't matter at all. But when having processes not running under root, e.g. a web server like Apache2 or Nginx or an application server like Tomcat this problem unveils itself. You can't just `chown -R user:user *` within the container as the file won't belong to the correct user on the host then.

When I encountered this error first, I naturally searched the web for solutions. I just couldn't find one which sounded like a sustainable approach. Most people who encountered this issue created users on the host who utilized the same IDs as the container user. While this is no big deal, it conflicts with one of the intentions I have with my containers: portability. When not having a user on the host with the same UID like the container user, the container won't run out of the box.

## The solution

My approach rolls up the problem from the other side. Why not change the UID/GID of the user *within* the container? This way you don't have to adapt your host to anything and you won't run into problems when the original container user ID utilizes an ID alreasy used on your host. Of course this needs to happen automatically. Thus I wrote a script intended for that functionality, **[wannabe-user.sh](https://github.com/m3adow/wannabe-user.sh)**.

### Functionality

Basically wannabe-user.sh is just a standard UID/GID changing script. Changing passwd/group, running `find` to change the old UID/GID to the new one, no magic here. To control it you can either use commandline arguments or - specifically tailored for containers, environment variables.
{% highlight bash %}
/wannabe-user.sh -u SOURCE_UID -g SOURCE_GID [-x- NEW_UID -y NEW_GID] [-f OWNERSHIP_PATH] [-r ROOT_FORCE]
{% endhighlight %}
wannabe-user.sh can be run either in ENV mode or in OWNERSHIP mode. While ENV mode simply expects all the variables like `UID` and `NEW_UID` (or the respective `GID` and `NEW_GID`) to be available by the mentioned envvar or commandline arg way, OWNERSHIP mode is the mode I really intended for container operations. Instead of expecting a `NEW_UID`/`NEW_GID`, you now just have to pass a file or a folder to the script via `OWNERSHIP_PATH`. Its UID/GID will be taken as blueprint and applied to the container user or group passed to the script via `SOURCE_UID`/`SOURCE_GID`.
If you want to change the UID of a user to 0 for some reason, you have to additionally set `ROOT_FORCE`.

If you want to know more about *wannabe-user.sh*, feel free to ask me in the comments or on [Github](https://github.com/m3adow/wannabe-user.sh).
