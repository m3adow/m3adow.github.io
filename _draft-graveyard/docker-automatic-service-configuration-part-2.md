---
layout: default
title: "Docker: Exploring Automatic Service Configuration with Consul, Registrator and consul-template (Part II)"
categories:
- Docker
---

## Overview
#### Part I
* [Introduction](#introduction)
  * [What is Automatic Service Discovery?](#whatisasd)
  * [What is Automatic Service Configuration?](#whatisasc)
* [Scenario](#scenario)
* [Preparation](#preparation)
* [Consul](#consul)

#### Part II
* Registrator
  * Limitations
  * Solution
  * Installation and Configuration
  * Summary

#### Part III
* consul-template
  * Shortcoming and Solution
  * Installation and Configuration
  * Summary
* Final infrastructure
* Conclusion

---

In [Part I][1] we learned about the initial motivation for Automatic Service Discovery. Additionally we set up our first container running [Consul][2]. In this Part we will learn about Registrator, its limitations and how to solve them so we can use it for our Automatic Service Configuration infrastructure.

### Registrator

Registrator is intended as an "Automatic Service Announcement" tool. It is maintained by Gliderlabs. Via the help of environment variables you can configure a lot of basic attributes for services running in containers, like service names, service tags, and even additional attributes. Registrator then registers those in the underlying KV-store. It supports many of the popular backends in Automatic Service discovery including our choice, Consul. But sadly Registrator has some...

#### Limitations
 In theory Registrator fully satisfies our needs for Automatic Service Configuration. If only it wasn't for this line in the official documentation:
> Tags and attributes are extra metadata fields for services. Not all backends support them. In fact, currently Consul supports tags and none support attributes.

This means that without changes Registrator is not able to register additional attributes to Consul. There is no easy way to extend it with that functionality either.  
*(In my first tries I abused the tags system of Consul for it (Registrator is able to pass tags to Consul). But apart from having ugly tags like `%%key1=value1%key2=value2%etc=etc%%` in Consul, I ran into additional problems when processing those in Consul Template. Still, this seems to be the easiest and less obtrusive solution. If you're interested, look into [my Github Repo][3].)*

#### Solution
While searching for a solution of my problem I stumbled over [issue #175][4] as well as [pull request #261][5] in the Registrator Repo. While issue #175 describes the problem, pull request #261 seems to provide a solution. Upon closer investigation I realized the pull request needed some additional work as it started into the wrong direction, but took a wrong turn shortly afterwards.




[1]: ./docker-automatic-service-configuration-part-1
[2]: https://www.consul.io/
[3]: https://github.com/m3adow/consul-template-plugins/blob/master/extract_tag_kv.sh
[4]: https://github.com/gliderlabs/registrator/issues/175
[5]: https://github.com/gliderlabs/registrator/pull/261
