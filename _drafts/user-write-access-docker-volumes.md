---
layout: default
title: "Solving permission problems in Docker host volumes"
categories:
- docker
---

One of the pitfalls I constantly run into while using docker is user access, especially write access to host volumes.

I'll use an example to visualise the problem as well as the possible solutions. Lets assume we have the following PHP website:

{% highlight php %}
<?php
$file = fopen('visitors.html', 'a') or die ("Could not access file.");
$time = date('c');
fwrite( $file, '<b>$time:</b> $REMOTE_ADDR<br/>');
fclose( $file );
?>
{% endhighlight %}

It's just a very simple application to log the IP of your visitors. Lets try running this in a container.

{% highlight bash %}
docker run --rm -ti -v /var/www/php-test/:/var/www/html -p 80:80 php:apache
{% endhighlight %}

Starting the container works of course. But accessing the website doesn't work so well.

<a href="https://adminswerk.de/assets/2016-01-05-php-permission-denied-docker.jpg"><img src="https://adminswerk.de/assets/2016-01-05-php-permission-denied-docker.jpg" alt="PHP: Permission denied" width="80%" height="80%"></a>

Why? Lets inspect this a little more thorough

{% highlight bash %}
docker run -ti -p 80:80 -v /var/www/php-test/:/var/www/html/ php:apache bash
root@7d71eccace2d:/var/www/html# ls -ld /var/www/html/
drwxr-xr-x. 2 1337 1337 4096 Jan  5 09:49 /var/www/html/
root@7d71eccace2d:/var/www/html# ls -l /var/www/html/
ls -l /var/www/html/
total 4
-rw-r--r--. 1 1337 1337 167 Jan  5 09:49 index.php
{% endhighlight %}

Of course it's a permissions problem, that's what this post is about. But why?  
The problem lies within Dockers mapping of host UIDs (and GIDs) into containers. Docker simply maps UIDs 1:1, even when there's no such user in the container. This isn't a problem as long as the application in the container is running with root privileges. But our web server doesn't (and shouldn't) run as root but as `www-data` leading to our permission problem.


<!-- OLD TEXT
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
-->
