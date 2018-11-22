---
layout: default
title: "Tidy up your Docker lab "
categories:
- Docker
---

Short tip for people like me experimenting with Docker: Cleaning up after you can be time-consuming and annoying. This also applies to keeping 3rd party images up-to-date. Luckily there's Spotify's [docker-gc](https://github.com/spotify/docker-gc) for housekeeping which - although very basic - does the job exceptional well. Just create one file with containing the names or IDs of all images you want to keep and one file with all the container names or IDs you want to keep and run `docker-gc` afterwards. Thereafter you can simply do a `docker pull` on the remaining images.  
Here's how I do the whole process, first cleaning up, afterwards refreshing the images which remain. As I do not conserve any containers, there is no EXCLUDE_CONTAINERS_FROM_GC:
{% highlight bash %}
#!/bin/sh
set -e
set -u
set -o pipefail
/bin/docker run -e "EXCLUDE_FROM_GC=/mnt/docker-gc-exclude" \
  -v "/docker-gc/:/mnt/" -v "/var/run/docker.sock:/var/run/docker.sock" \
  spotify/docker-gc
for IMAGE in $(docker images|tail -n +2 |awk '{print $1 ":" $2}')
do
  docker pull "${IMAGE}"
done
{% endhighlight %}
