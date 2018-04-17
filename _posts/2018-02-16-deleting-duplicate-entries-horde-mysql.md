---
layout: default
title: "Horde: Deleting Duplicates from MySQL Database"
categories:
- MySQL
- Horde
---

I recently encountered a problem with my [Horde][horde] installation. Due to an
app misconfiguration, my wife created hundreds of calendar entries for the same
event. It is tedious to delete every event by hand, so I wanted to drop the entries
from the database. As this is something other people might profit from, I'm
documenting it. Of course part of this procedure can be done with other MySQL
databases as well.

## Get listing of double entries
   I wanted to see all duplicate entries first, to make safe I'm not deleting important
   stuff. This can be done with a `SELECT COUNT` command:
   ```sql
   SELECT event_title,event_start,COUNT(*) c FROM kronolith_events
     GROUP BY event_title,event_start HAVING c > 1 ORDER BY c ASC;
   ```
This is the result:

<a href="{{site.url}}/assets/images/2018/2018-02-15-mysql-count-duplicates-table.png"><img src="{{site.url}}/assets/images/2018/2018-02-15-mysql-count-duplicates-table.png" style="width: 60%; margin: 10px;" alt="MySQL count duplicates table"></a>

Ouch! That are a lot of duplicate entries. Let's delete them!

<!--more-->

{% include adsense_manual.html %}

We will need the IDs of the entries for that. For Hordes Kronolith this is the
`event_uid`. While we won't use this as single command in this scenario, it's
interesting to know it:

```sql
SELECT GROUP_CONCAT(event_uid) FROM kronolith_events
  GROUP by event_title, event_start HAVING (
    COUNT(event_title) > 1 AND COUNT(event_start) > 1);
```

## Get the affected tables
I had no idea in which tables I would find the affected entries. I am also not
good enough in MySQL to find that out in the CLI (if it is even possible).
So I used bash:

```bash
mysqldump --extended-insert=FALSE horde_db > /tmp/horde_db.sql \
  && for ID in $(mysql -B horde_db <<< "SELECT GROUP_CONCAT(event_uid) FROM kronolith_events
     GROUP by event_title, event_start HAVING (COUNT(event_title) > 1 AND COUNT(event_start) > 1);" \
  | tr ',' ' ' | tr '\n' ' '); \
  do grep "${ID}" tmp/horde_db.sql| awk '{print $3}'| tr -d '`'; \
  done | sort -u
# OUTPUT
horde_dav_objects
horde_histories
kronolith_events
nag_tasks
rampage_objects
```

This might differ for other users, so don't rely on my results.

Now that we got all the affected tables and all the `event_uid`s. We still need
the column names the uids are in. As I have not worked thoroughly with MySQL in
ages, I couldn't find a quick way to get this, therefore I created a mapping
manually. In my case it is this:

* horde_dav_objects -> id_external (with .ics suffix)
* horde_histories -> object_uid (this is a concatenated string)
* kronolith_events -> event_uid
* nag_tasks -> task_uid
* rampage_objects -> object_name

## Delete the rows

Now I could have done some `JOIN`s to get all the entries into one row, but
again, due to my rusted skills it was too complicated for me and I could not
find a quick way. So I just wrote a small bash script. It is very inefficient - my
run took around 90s - because it iterates over every ID, but it gets the job done:

```bash
#!/bin/bash
set -euo pipefail
#set -x

for ID in $(mysql -B --skip-column-names horde_db <<< "
  SET @@group_concat_max_len = 10000000;
  SELECT GROUP_CONCAT(event_uid) FROM kronolith_events GROUP by event_title, event_start HAVING (COUNT(event_title)
  > 1 AND COUNT(event_start) > 1);" | tr ',' ' ' | tr '\n' ' ')
  do  
    echo "$ID"
    mysql --skip-column-names -B horde_db <<< "
    SET @@group_concat_max_len = 10000000;
    DELETE FROM horde_dav_objects WHERE id_external LIKE '${ID}.ics';
    DELETE FROM horde_histories WHERE object_uid LIKE '%${ID}%';
    DELETE FROM kronolith_events WHERE event_uid = '${ID}';
    DELETE FROM nag_tasks WHERE task_uid = '${ID}';
    DELETE FROM rampage_objects WHERE object_name = '${ID}';"
  done
```

This deletes every occurence of these entries, so you will need to recreate those
you need.

If you have ideas how to improve this, because you are better in SQL than I am,
feel free to comment. Other comments are of course welcome as well.

[horde]: https://www.horde.org/
