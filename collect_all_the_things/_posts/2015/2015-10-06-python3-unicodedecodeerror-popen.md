---
layout: default
title: "Python3: UnicodeDecodeError when using subprocess.Popen"
categories:
- Python
---

While writing a Python script which handles an applications STDOUT on Windows, I encountered an error:
{% highlight py3tb %}
Traceback (most recent call last):
  File "C:/Users/m3adow/PycharmProjects/proj1/script.py", line 355, in <module>
    main()
  File "C:/Users/m3adow/PycharmProjects/proj1/script.py", line 347, in main
    openme(bin_args)
  File "C:/Users/m3adow/PycharmProjects/proj1/script.py", line 307, in spectate
    for line in iter(p.stdout.readline, ''):
  File "C:\tools\python\lib\encodings\cp1252.py", line 23, in decode
    return codecs.charmap_decode(input,self.errors,decoding_table)[0]
UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 1478: character maps to <undefined>
{% endhighlight %}

The lines in question looked like this:
{% highlight python3 %}
def openme(bin_args):
  with subprocess.Popen(args=bin_args, stdout=subprocess.PIPE, stderr= subprocess.STDOUT, universal_newlines=True) as p:
        for line in iter(p.stdout.readline, ''):
          process_stdout(line)
{% endhighlight %}
<!--more-->
After hours of investigation, I found my answer [at Stack Overflow](https://stackoverflow.com/questions/29546311/popen-communicate-throws-unicodedecodeerror).

{% include adwrap_top.html %}
<script type="text/javascript">
amzn_assoc_tracking_id = "admwer-20";
amzn_assoc_ad_mode = "manual";
amzn_assoc_ad_type = "smart";
amzn_assoc_marketplace = "amazon";
amzn_assoc_region = "US";
amzn_assoc_design = "enhanced_links";
amzn_assoc_asins = "B0785Q7GSY";
amzn_assoc_placement = "adunit";
amzn_assoc_linkid = "e7e09f69f432bb5e1749c833de063957";
</script>
<script src="//z-na.amazon-adsystem.com/widgets/onejs?MarketPlace=US"></script>
{% include adwrap_bottom.html %}

The applications STDOUT includes a lot of Asian symbols which don't go well with the formatting Python wants to use when setting **universal_newlines=True**. When setting this attribute, text mode is enabled and Python tries to automatically decode the byte output of STDOUT to the systems locale. Windows uses a very limited encoding page which lacks the needed Asian symbols.

To circumvent the problem, I wrote my own small decoder:
{% highlight python3 %}
def openme(bin_args):
  with subprocess.Popen(args=bin_args, stdout=subprocess.PIPE, stderr= subprocess.STDOUT) as p:
        for byte_line in iter(p.stdout.readline, ''):
          line = byte_line.decode('utf8', errors='backslashreplace').replace('\r', '')
          process_stdout(line)
{% endhighlight %}

The **replace** probably needs modification, in my case the application STDOUT lines ended with *\n\r* so it was really easy.
