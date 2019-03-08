---
layout: default
title: "Winbind: UID/GID range full"
categories:
- Linux
- Samba
---

We had a problem on a storage server. One user was not able to authenticate with the Samba service using his Active Directory credentials. Furthermore I couldn't find his user via `getent passwd AD\\username`.
After checking several LDAP/Kerberos/PAM configuration files, I had the glorious idea to also check the logs of winbind.

```plain_text
[2019/01/29 14:05:16.726252,  1, pid=4467, effective(0, 0), real(0, 0)]   Fatal Error: UID range full!! (max: 60000)
[2019/01/29 14:05:16.726299,  1, pid=4467, effective(0, 0), real(0, 0)]   Error allocating a new UID
[2019/01/29 14:05:16.726339,  1, pid=4467, effective(0, 0), real(0, 0)]   no backend defined for idmap config BUILTIN
[2019/01/29 14:05:16.726903,  1, pid=4467, effective(0, 0), real(0, 0)]   Fatal Error: GID range full!! (max: 60000)
[2019/01/29 14:05:16.726948,  1, pid=4467, effective(0, 0), real(0, 0)]   Error allocating a new GID
```

Huh, interesting. This wasn't a heavily used server. Neither users nor groups were even in the proximity of 60000. Accordingly increasing the `idmap uid`/`idmap gid` did not help at all.  
Several hours later I found the solution in the [arstechnica forum][arsforum]:

> Long story short, stop winbind, delete winbindd_cache.tdb & winbindd_idmap.tdb from /var/cache/samba, then restart winbind. Mappings now happen right. So I can log in with domain accounts and access shares.

The provided path `/var/cache/samba` did not fit for the Red Hat Enterprise Linux running on this server. But finding out that `winbindd_cache.tdb` and `winbindd_idmap.tdb` are located in `/var/lib/samba` was no big deal after nearly 60 minutes of unnecessary debugging.

[arsforum]: https://arstechnica.com/civis/viewtopic.php?t=46244
