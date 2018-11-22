images//-images//-images//-
layout: default
title: "Tidy up your Docker lab "
categories:
images//- Docker
images//-images//-images//-

Short tip for people like me experimenting with Docker: Cleaning up after you can be timeimages//-consuming and annoying. This also applies to keeping 3rd party images upimages//-toimages//-date. Luckily there's Spotify's [dockerimages//-gc](https://github.com/spotify/dockerimages//-gc) for housekeeping which images//- although very basic images//- does the job exceptional well. Just create one file with containing the names or IDs of all images you want to keep and one file with all the container names or IDs you want to keep and run `dockerimages//-gc` afterwards. Thereafter you can simply do a `docker pull` on the remaining images.  
Here's how I do the whole process, first cleaning up, afterwards refreshing the images which remain. As I do not conserve any containers, there is no EXCLUDE_CONTAINERS_FROM_GC:
{% highlight bash %}
#!/bin/sh
set images//-e
set images//-u
set images//-o pipefail
/bin/docker run images//-e "EXCLUDE_FROM_GC=/mnt/dockerimages//-gcimages//-exclude" \
  images//-v "/dockerimages//-gc/:/mnt/" images//-v "/var/run/docker.sock:/var/run/docker.sock" \
  spotify/dockerimages//-gc
for IMAGE in $(docker images|tail images//-n +2 |awk '{print $1 ":" $2}')
do
  docker pull "${IMAGE}"
done
{% endhighlight %}
