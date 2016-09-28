---
layout: default
title: "Docker: Exploring Automatic Service Configuration with Consul, Registrator and consul-template (Part I)"
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
  * Shortcoming and Solution
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
### <a name="introduction"></a>Introduction

#### <a name="whatisasd"></a>What is Automatic Service Discovery?
When handling Micro Services the knowledge of "how many instances of a service are running where" gradually vanishes. To still let services keep track of their dependencies, e.g. a database dependency for an application server, we can make use of Automatic Service Discovery.  
A lot of good articles about that subject already exist, so I don't want to reinvent the wheel. If you're not familiar with the concept as a whole, I suggest you read the blog posts of Jeff Lindsay about [Modern Service Discovery with Docker][1] and [Consul Service Discovery with Docker][2] as well as [the series about it][3] from Jose Luis Ordiales, at least [his post about][4] consul.

#### <a name="whatisasc"></a>What is Automatic Service Configuration?
Although Automatic Service Discovery can be used to do basic service configuration as well, that's only true for dependency services. But what about application specific configuration? While new applications would probably just expect a Key/Value store as a dependency for configuration, Legacy applications can't be changed in that way. Those don't know about Key/Value stores or Automatic Service Discovery.  

So the basic duty of Automatic Service Configuration is enabling a fully automatic configuration of auto discovered Micro Services.

### <a name="scenario"></a>Scenario

I encountered this problem when deciding I wanted to be able to quickly boot up a couple of different web applications in my test lab without reconfiguring my **Consul Template** for the nginx reverse proxy for every specific application. I wanted to be able to provide configuration values in my web application containers which could be taken by my nginx reverse template to configure values like `server_name` on the fly.

Of course there's the [nginx-proxy][5] container for that specific scenario. But I wanted to have a solution which could universally satisfy this requirement, without being limited to reverse proxying. Although all of this happened in my test lab, I can imagine similar requirements when handling legacy software. A couple of identical containers using an API with different rate limitings for example. Or using a Tomcat container with per-application settings for JVM memory values. I see this as a very plausible requirement, especially in testing and development environments.

That's why I wanted universal a solution for Automatic Service Configuration.

So lets start!
<!--more-->

{% include adsense_manual.html %}

### <a name="preparation"></a>Preparation

To make our exploration an easier one, we will use a separated virtual network where all our containers will reside. For this we'll need a Docker version of at least 1.9.

```bash
docker network create --subnet="172.31.255.0/24" -o "com.docker.network.bridge.enable_icc"="true" -d bridge asc_test
```

This way we don't have to struggle with different Docker bridge configurations and can fix the IP addresses of our containers.

### <a name="consul"></a>consul

Now lets set up our first container for the Key/Value store [Consul][6]. If you're familiar with Automatic Service Discovery or you read the posts I recommended, you're probably familiar with Consul. In contrast to Registrator and Consul Template we won't be changing anything on Consul, so we can just use the popular container from Jeff Lindsays Gliderlabs. But first lets create a file with some minor tweaks to Consuls configuration. We'll call it `xtended_config.json` which leads to it being loaded after the default `config.json` file of the containers configuration:

```json
{
  "ports": {
    "dns": "53"
  },
  "recursors": [
    "8.8.8.8"
  ]
}
```

Now we can start our container.

```bash
docker run -d \
  --net=asc_test -p 8500:8500 \
  --expose=8300-8302 --expose=8301-8302/udp --expose=8400 \
  --expose=8500 --expose 8600 --expose=53/udp \
  --name=consul-server -h node1 \
  -v /asc_test/xtended_config.json:/config/xtended_config.json:ro \
  gliderlabs/consul-server -bootstrap-expect 1
```

That's it, we're done with the Consul configuration. You should be able to connect to the web interface via port 8500, although there's little to be seen there yet.

<a href="{{site.url}}/assets/images/2016/2016-03-16-consul-web-default.png"><img src="{{site.url}}/assets/images/2016/2016-03-16-consul-web-default.png" alt="Default Consul Web Interface View" style="width: 60%;"></a>

This concludes Part I of our Automatic Service Configuration journey.








[1]: http://progrium.com/blog/2014/07/29/understanding-modern-service-discovery-with-docker/
[2]: http://progrium.com/blog/2014/08/20/consul-service-discovery-with-docker/
[3]: http://jlordiales.me/2014/12/07/aws-docker/
[4]: http://jlordiales.me/2015/01/23/docker-consul/
[5]: https://hub.docker.com/r/jwilder/nginx-proxy/
[6]: https://www.consul.io/
