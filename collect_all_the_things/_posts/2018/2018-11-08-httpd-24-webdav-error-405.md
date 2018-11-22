---
layout: default
title: "Fixing HTTP 405 errors with httpd 2.4 WebDAV"
categories:
 - httpd
 - webdav
---

While updating an Apache httpd from 2.2 to 2.4 we encountered a strange problem. The web server is used as a reverse proxy for a WebDAV application.
Therefore the original httpd 2.2 directive allowed a couple of WebDAV methods. It looked similarly to this:

```apache
<Location "/dav">
  <LimitExcept HEAD GET POST CONNECT PUT DELETE OPTIONS PROPFIND PROPPATCH MKCOL COPY MOVE LOCK UNLOCK TRACE>
    Order       deny,allow
    Allow       from all
  </LimitExcept>
</Location>
```

Adapting this to httpd 2.4 was not a big deal:

```apache
<Location "/dav">
  AllowMethods HEAD GET POST CONNECT PUT DELETE OPTIONS PROPFIND PROPPATCH MKCOL COPY MOVE LOCK UNLOCK TRACE
  Require all granted
</Location>
```

But this didn't work as expected. While `OPTIONS` did work, `PROPFIND`, `PROPPATCH`, etc. were not. My tests with curl always returned HTTP 405.

```bash
curl -X PROPFIND https://example.org/dav
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>405 Method Not Allowed</title>
</head><body>
<h1>Method Not Allowed</h1>
<p>The requested method PROPFIND is not allowed for the URL /.</p>
</body></html>
```

As it turns out, there's a [bug report from 2013][br] in the Apache bug tracker for a similar issue. For whatever reason an enabled `DirectoryIndex` directive blocks the WebDAV methods.
This bug has been fixed in the httpd 2.5 trunk, but not in http 2.4 (and probably never will). Therefore disabling `DirectoryIndex` is the mandatory workaround:

```apache
<Location "/dav">
  DirectoryIndex disabled
  AllowMethods HEAD GET POST CONNECT PUT DELETE OPTIONS PROPFIND PROPPATCH MKCOL COPY MOVE LOCK UNLOCK TRACE
  Require all granted
</Location>
```

As this issue didn't arise until production hours and a quick fix was needed, I've yet to confirm if `mod_dav` and `mod_dav_fs` are even needed. I suspect they are not.

[br]: https://bz.apache.org/bugzilla/show_bug.cgi?id=54914
