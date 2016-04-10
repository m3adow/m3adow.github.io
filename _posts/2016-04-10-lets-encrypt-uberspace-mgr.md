---
layout: default
title: "Simplyfying Let's Encrypt on Uberspace"
categories:
- Uberspace
---

I'm regularly using [Uberspace][1], a provider for Shared Hosting with a lot of special quirks (sadly only available in German). I'm also using [Let's Encrypt][2] to create certificates for most of my websites. The hard working folks at Uberspace have integrated a [very easy way][3] to apply Let's Encrypt certificates for your domains, but it's also very limited:

> Übrigens ist dieses Zertifikat für alle oben angegebenen Domains gültig, du bekommst also nicht ein Zertifikat pro Domain, sondern ein Zertifikat, welches für alle Domains gültig ist:

*"Your certificate is valid for all entered domains. You don't get one certificate per domain, but one certificate which can be used for all domains."*

I don't want this at all. I've got several domains set up which are not logically linked, some are not even linked with my name and shall stay this way.

So I created a small script to allow the creation of Let's Encrypt certificates for several Uberspace domains independently. Introducing [letsencrypt-uberspace-mgr][4].
<!--more-->

{% include adsense_manual.html %}

# Using letsencrypt-uberspace-mgr

## Setup

If you haven't used Let's Encrypt on your Uberspace yet, I recommend reading their [Wiki entry][3] about it. At absolute minimum you need to run `uberspace-letsencrypt` to initialise Let's Encrypt. Don't mind the message about the included domains, **letsencrypt-uberspace-mgr** overrides those.

Afterwards create `~/etc/letsencrypt_domains.conf` on your Uberspace and put all domains you want to have in one certificate into one line, like this:

{% highlight bash %}
1st.domain.tld,2nd.domain.tld
my.single.tld
my.other.tld,and.another.tld
{% endhighlight %}

Afterwards put it in your crontab:

{% highlight bash %}
23 3 * * 5 /home/your-uberspace-user/path/to/script/letsencrypt-uberspace-mgr > ~/tmp/letsencrypt-uberspace-mgr.log
{% endhighlight %}

and you're done.

I recommend adding `keep-until-expiring = True` to your `~/.config/letsencrypt/cli.ini` to avoid running into the [Rate Limits][5] Let's Encrypt enforces.

## New certificates
I focussed **letsencrypt-uberspace-mgr** on easily keeping your Let's Encrypt certificates up to date as a simple "set and forget" maintenance script running via cron. Thus, creating new certs is still a little counter intuitive. There are actually two ways:  
Either add the new domains into your `~/etc/letsencrypt_domains.conf` and run **letsencrypt-uberspace-mgr** or create a new file (e.g. `~/tmp/new_domains.conf`) and point the `DOMAINS_FILE` variable towards it before executing **letsencrypt-uberspace-mgr**:   
`DOMAINS_FILE="~/tmp/new_domains.conf" bash -c "letsencrypt-uberspace-mgr"`.

If you set `keep-until-expiring = True` as recommended, both methods are fine. If you haven't, I'd recommend the second way due to the already mentioned Rate Limits of Let's Encrypt. Of course you still have to also add those domains to your `~/etc/letsencrypt_domains.conf` to include the certificates in the normal checking.

### Advanced usage

If you want to change any pathes in **letsencrypt-uberspace-mgr**, it can be done similarly to the second way of creating new certs. There are only four configuration variables used in the script:

* `LE_CONFIG_DIR`: The configuration directory for the `letsencrypt` client, default: `"${HOME}/.config/letsencrypt/"`
* `LE_CONF`: The configuration file for the `letsencrypt` client, default: `"${LE_CONFIG_DIR}/cli.ini"`
* `LE_ARGS`: The command line arguments the `letsencrypt` client is called with, default: `"--agree-tos --non-interactive"`
* `DOMAINS_FILE`: The aforementioned path to the file containing all domain sets to be checked, default: `"${HOME}/etc/letsencrypt_domains.conf"`

As shown in the example for new certificates, each of these variables can be set before running the script, effectively overwriting the defaults.

That's it! I hope I could help some people with that. If you need additional features hop on to github and create a feature request (or a pull request if you want to). Additionally, if **letsencrypt-uberspace-mgr** doesn't fit your needs, Christian Hawkins encountered a similar issue and created [ULEM, the Uberspace Let's Encrypt Manager][6].


[1]: https://uberspace.de/
[2]: https://letsencrypt.org/
[3]: https://wiki.uberspace.de/webserver:https#let_s-encrypt-zertifikate
[4]: https://github.com/m3adow/letsencrypt-uberspace-mgr
[5]: https://community.letsencrypt.org/t/rate-limits-for-lets-encrypt/6769
[6]: https://metabubble.net/hosting-servers/ulem-uberspace-lets-encrypt-manager/
