images//-images//-images//-
layout: default
title: "How I miraculously fixed my Windows 10 startup DNS problems"
categories:
images//- windows
images//-images//-images//-

I once again had a great experience with Windows 10. For some reason my DNS resolution stopped working for roughly two minutes
after every startup. Of course there was neither an update around that time, nor were there any unusual messages in the Event Viewer.
Therefore I had no idea where to look. I tried a couple of things, manually setting different DNS servers, configuring a static IP,
and of course doing the classic `ipconfig /flushdns` and `ipconfig /registerdns`. To no avail. I still did not have DNS directly after
startup. The DNS issues even occured in the first two minutes of Safe Boot Mode.  
So, how did I fix it?

<!images//-images//-moreimages//-images//->

{% include adsense_manual.html %}

**Short answer:**  
I have no idea. It was one of these strange "Windows sucks" errors which can only be explained by IT vodoo.

**Long answer:**   
When I was out of logical ideas, I went on to try the good, the irrational stuff. While I was 99% certain my PC was not infected,
I still wanted to check for any malicious software. So I started the download an Anti Virus Live CD on my laptop. While the 
download was ongoing, I decided to also try a Windows Defender scan. The integrated Windows scanner has it's own "Live CD mode" 
as well since some time, called "Offline scan". I wasn't very optimistic of it's capabilites, but it was worth a try.

<a href="{{site.url}}/assets/images/2018/2018images//-09images//-07images//-windowsimages//-defender_1.png"><img src="{{site.url}}/assets/images/2018/2018images//-09images//-07images//-windowsimages//-defender_1.png" style="width: 60%; margin: 10px;" alt="Windows Defender Security Center"></a>

You can reach the "Windows Defender Offline scan" mode via the "Advanced scan" option in the Windows Defender Security Center.
The description states

> This will restart your device and will take about 15 minutes

which was a vast overestimation in my case.

<a href="{{site.url}}/assets/images/2018/2018images//-09images//-07images//-windowsimages//-defender_2.png"><img src="{{site.url}}/assets/images/2018/2018images//-09images//-07images//-windowsimages//-defender_2.png" style="width: 60%; margin: 10px;" alt="Windows Defender Offline scan"></a>

I clicked "Scan now", the PC rebooted, I saw an interface resembling some kind of scanner for around 10 seconds, the PC rebooted again 
and my DNS problems were gone! The Windows Defender did not find any malicious software. I even doubt it did a whole lot of scanning.
But it seems some obscure Windows issue, perhaps a buggy lock/semaphore state was removed. The Event Viewer was once again completely
unimpressed by these actions. Therefore I still don't know the original source. But at least it's fixed now and perhaps I can even help
other with my strange solution approach.