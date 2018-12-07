---
layout: default
title: "Technical fundament of /dev/blog/ID10T"
categories:
- Blogging
---
<p>As the technical fundament of ID10T changed completely, it's a good idea to explicate its underlying infrastructure. I really like when other blogs websites or applications are thoroughly explaining their hosting technology, so I want to do it with my blog as well.</p>

### Blog software
I'm using [Jekyll](https://jekyllrb.com) as my blog software of choice. Due to its nature of being a static page generator, all the end user sees, are completely generated pages without PHP or alike (some JScript though) which results in a very good pagespeed. The template I based my blog design on is [Contrast](https://github.com/niklasbuschmann/contrast) from Niklas Buschmann.

### Github pages
Like many other sites, I use [Github pages](https://pages.github.com/) as the hosting provider. It's free, fast and provides a lot of flexibility due to it's connection to git. Sadly, Github pages doesn't provide a way to secure your connection. Https is only possible with the \*.github.io domain, SSL with a custom one isn't supported. To circumvent this, I prepend [cloudflare](https://cloudflare.com) with enabled and forced SSL encryption. This isn't a true end-to-end encryption as the clients connection is only secured up until the cloudflare servers, the connection afterwards, from cloudflare to GH pages, remains unsecured. But at least there's no possibility for an man-in-the-middle attack when using an open W-LAN.

### Uberspace
When using only GH pages, there's no way of previewing drafts. The normal way Github expects you to write up your posts is with a Jekyll instance running locally where you can serve the drafts all you want. But that's not my use case. I'm one of those pesky "generation mobile" members. I want to be able to write posts everywhere, on every device, preview them on the go and publish them afterwards.

To realise that, I'm using an [uberspace](https://uberspace.de). Uberspace is a hybrid between shared hosting and a virtual server. An uberspace is able to run a [plethora of software](https://wiki.uberspace.de/), Ruby with Jekyll is one of those.
Thus, I planned on running a triumvirate of Dropbox, for the syncing from and to every device, Jekyll, for the preview of drafts and git to commit and push the changes to my Github repository belonging to my blog. I'm running a dropbox daemon on my uberspace which only syncs the folder containing the Jekyll source files. To start a build and deployment of the "local" (on uberspace) Jekyll installation or to commit and push the changes to github, I've written a small script which I called [jekyll-file-remote](https://github.com/m3adow/jekyll_file_remote). It's basically an infinite loop checking a watch folder for control files.

Thereby I can write markdown drafts on every device I want, as those are synced via Dropbox. If I want to preview the drafts, I create a control file resulting in compiling them via the jekyll installed on my uberspace and previewing them into another location which is excluded for search engine crawlers. If I'm satisfied with my blog post, I create another control file for jekyll-file-remote, which automatically commits and pushes the changes to my [m3adow.github.io](https://github.com/m3adow/m3adow.github.io) repository.
