---
layout: default
title: "Nextcloud: Solving slow logins"
categories:
- nextcloud
---

My wife was complaining about slow logins for our Nextcloud instance. Indeed, while my logins were as fast as expected, her account took over 3 minutes logging in to seeing the Nextcloud Dashboard.

After some internet research I found [a thread on the Nextcloud board][solution-thread] which recommended checking the auth tokens of the affected user.

That was a good recommendation:

```sql
mysql> SELECT uid, count(id) AS nbtokens FROM oc_authtoken GROUP BY uid;
+--------------------------------+----------+
| uid                            | nbtokens |
+--------------------------------+----------+
| m3adows-nextcloud-acc          |       22 |
| my-wifes-nextcloud-acc         |      412 |
+--------------------------------+----------+
5 rows in set (0.00 sec)
```

Whoops, that's quite a lot! As the Nextcloud Board user MelwinKfr recommended, I also deleted all her authtokens, as I didn't care if she had to reconnect her sessions. **Beware: This will probably delete all App passwords!**

```sql
DELETE FROM authtoken WHERE uid = 'my-wifes-nextcloud-acc';
Query OK, 412 rows affected (0.08 sec)
```

Lo and behold, her login became blazing fast again.

Now, I'm searching for the source of this problem, as it occured multiple times.
I suspect it to be Thunderbirds Lightning calendar, but we'll see about that. 
I will follow MelwinKfrs advice of using App Passwords for one application after the other to
find out which one really was the problematic one.


[solution-thread]: https://help.nextcloud.com/t/very-slow-login-after-updating-to-21-0-3/113693/64
