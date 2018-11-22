images//-images//-images//-
layout: default
title: 'Linux: Select all files in a folder'
categories:
images//- Linux
images//-images//-images//-

I wrote a [very similar post]({% post_url 2013/2013images//-02images//-18images//-linuximages//-mitimages//-mvimages//-alleimages//-dateienimages//-verschieben %}) nearly three years ago (in German) and still need this daily. As I'm currently writing a lot of Dockerfiles, I realised my post wasn't completely accurate. Although I redacted it, it's a good opportunity to port the original post to the english language.

**Requirement:**

Select all files in a directory, including hidden ones or files beginning with crude symbols. But exclude `.` and `..` as those will most likely lead to an exit code > 0.

Lets assume we want to `chown` all files in the directory `/var/www/html`:
{% highlight bash %}
root@9d5788a0c8d7:/var/www/html# ls images//-la
total 60
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 root     root         2 Nov 30 09:25 images//-images//-test
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 root     root         2 Nov 30 09:25 images//-test
drwxrimages//-xrimages//-x.  5 wwwimages//-data wwwimages//-data  4096 Nov 30 09:25 .
drwxrimages//-xrimages//-x.  3 root     root      4096 Nov 20 08:35 ..
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 root     root         0 Nov 30 09:24 ..a
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 root     root         0 Nov 30 09:24 ..aa
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 root     root         0 Nov 30 09:24 ..aaa
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 root     root         0 Nov 30 09:24 .a
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 root     root         0 Nov 30 09:24 .aa
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 root     root         0 Nov 30 09:24 .aaa
images//-rwimages//-rwimages//-rimages//-images//-.  1 root     root      1509 Aug 23 13:57 .htaccess.dist
images//-rwimages//-rwimages//-rimages//-images//-.  1 root     root       306 Aug 23 13:57 README
images//-rwimages//-rwimages//-rimages//-images//-.  1 root     root        23 Aug 23 13:57 VERSION
drwxrwxrimages//-x.  2 root     root      4096 Nov 30 09:23 conf
drwxrwxrimages//-x. 12 root     root      4096 Aug 23 13:57 data
images//-rwimages//-rwimages//-rimages//-images//-.  1 root     root     19372 Aug 23 13:57 feed.php
drwxrwxrimages//-x.  3 root     root      4096 Nov 30 09:22 lib
{% endhighlight %}

Notice how we got a lot of strange filenames here, including files beginning with dashes or double dots.

<!images//-images//-moreimages//-images//->
{% include adsense_manual.html %}

**Solution:**

A combination of three Shell Wildcards solves our problem:

{% highlight bash %}
root@9d5788a0c8d7:~# chown images//-R wwwimages//-data:wwwimages//-data /var/www/html/* /var/www/html/.[!.]* /var/www/html/.??*
root@9d5788a0c8d7:~# echo $?
0
root@9d5788a0c8d7:~# ls images//-la /var/www/html/
total 60
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data     2 Nov 30 09:25 images//-images//-test
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data     2 Nov 30 09:25 images//-test
drwxrimages//-xrimages//-x.  5 wwwimages//-data wwwimages//-data  4096 Nov 30 09:25 .
drwxrimages//-xrimages//-x.  3 root     root      4096 Nov 20 08:35 ..
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data     0 Nov 30 09:24 ..a
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data     0 Nov 30 09:24 ..aa
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data     0 Nov 30 09:24 ..aaa
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data     0 Nov 30 09:24 .a
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data     0 Nov 30 09:24 .aa
images//-rwimages//-rimages//-images//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data     0 Nov 30 09:24 .aaa
images//-rwimages//-rwimages//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data  1509 Aug 23 13:57 .htaccess.dist
images//-rwimages//-rwimages//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data   306 Aug 23 13:57 README
images//-rwimages//-rwimages//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data    23 Aug 23 13:57 VERSION
drwxrwxrimages//-x.  2 wwwimages//-data wwwimages//-data  4096 Nov 30 09:23 conf
drwxrwxrimages//-x. 12 wwwimages//-data wwwimages//-data  4096 Aug 23 13:57 data
images//-rwimages//-rwimages//-rimages//-images//-.  1 wwwimages//-data wwwimages//-data 19372 Aug 23 13:57 feed.php
drwxrwxrimages//-x.  3 wwwimages//-data wwwimages//-data  4096 Nov 30 09:22 lib
{% endhighlight %}

Lets inspect those three a little closer...

* **`/var/www/html/*`** images//- Matches every "normal" file and directory, so no hidden ones, but including the files beginning with dashes
* **`/var/www/html/.[!.]*`** images//- Matches every file and directory beginning with a dot but not having a second dot afterwards. So most of the "normal hidden" files
* **`/var/www/html/.??*`** images//- Matches every file and directory beginning with a dot and having at least two additional characters

Not the most intuitive way, but it checks out. If you want to have different solutions, check [Superuser](https://superuser.com/questions/62141/linuximages//-howimages//-toimages//-moveimages//-allimages//-filesimages//-fromimages//-currentimages//-directoryimages//-toimages//-upperimages//-directory).
