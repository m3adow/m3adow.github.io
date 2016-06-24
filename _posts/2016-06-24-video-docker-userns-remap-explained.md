---
layout: default
title: "Video: Dockers '--userns-remap' feature explained"
categories:
- docker
---

I have been up to the ears in work and in projects, that's why I haven't been posting a lot. I initially wanted to create a series about automatic service discovery and configuration with Consul, Registrator and consul-template, but decided to switch to [Rancher][1] in the process as I encountered too much hassle and had to make too much workarounds.

But that's not the topic of this post. I recently created a short video on asciinema to further explain dockers `--userns-remap` feature which significantly improves security.

What is it you ask? The original description from the `docker-daemon` manpage:

> \-\-userns-remap=default\|uid:gid\|user:group\|user\|uid Enable user namespaces for containers on the daemon. Specifying "default" will cause a new user and group to be created to handle UID and GID range remapping for the user namespace mappings used for contained processes. Specifying a user (or uid) and optionally a group (or gid) will cause the daemon to lookup the user and group's subordinate ID ranges for use as the user namespace mappings for contained processes.

Here's my video explaining it:

<script type="text/javascript" src="https://asciinema.org/a/49994.js" id="asciicast-49994" async></script>


[1]: http://rancher.com/
