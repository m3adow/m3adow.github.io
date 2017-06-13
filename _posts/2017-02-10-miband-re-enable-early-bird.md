---
layout: default
title: "Xiaomi Mi Band: Re-enable Early Bird Alarm"
categories:
- Android
---

I bought a [Xiaomi Mi Band 1S][mibandamazon] one year ago solely for the reason of taking advantage of the "Early Bird Alarm". This feature essentially tells the band to watch your sleep cycles 30 minutes before your set alarm and wake you up if it detects you are in a light sleep some time during this timespan (you probably knew this already, why are you here otherwise? ;-}). Sadly, Xiaomi removed this feature some time in 2016 without ever mentioning why or if it ever returns. As I don't use my band for everything else, I recently decided to recover my "Early Bird". I was successful and want to share all the actions I tried in case others have a similar need for returning their smart alarm. I assume these steps can be applied to other Mi Band versions (Mi Band 1, Mi Band 1S, Mi Band 2) as well.

**Prelude:**
I'm not certain if every action is needed. I tried dry testing my changes but all changes failed the tests, including the (fully working) one I'm using now. So I advise on "live" testing every change for two or three nights if you don't want to pull completely through with everything. If you find out only parts of it are needed, I'd appreciate if you left a comment afterwards.

<!--more-->

{% include adsense_manual.html %}

That said, here are all the steps I took to regain the Early Bird Alarm on my Mi Band:

**1. Disable all Alarms in the Mi Fit App:**  This should be done before fiddling with other apps. Either disable the alarms in the Mi Fit App or straightforwardly delete all of them. Not doing this might result in failure of tests for all other steps.

<a href="{{site.url}}/assets/images/2017/2017-02-09-tools-and-miband.png"><img src="{{site.url}}/assets/images/2017/2017-02-09-tools-and-miband.png" style="width: 30%; float: right; margin: 10px;"></a>**2. Use alternative Apps:** There are three Apps I know of which could still be able to set Early Bird Alarms, [Notify& Fitness for Mi Band][notifyfitnessmi] (free version available), [Tools & Mi Band][toolsmi] (2,99€) and the Open Source App [Gadgetbride][gadgetbride]. Although I suspect all three Apps use the same mechanism to set an Early Bird Alarm, I'd still recommend trying all three after every step, just to be sure. I might eventually do this myself, so perhaps I'll write an update in a few weeks or months. Please note that there are some Apps out there which advertise similar features but need to be connected to the band as soon as the "Early Bird" phase starts. My phone is either off or in Airplane mode at night, so this was no alternative for me. Still, this implementation is an easy way out.

***3. Uninstall the Mi Fit App:*** If you don't use your Mi Band for anything else except Alarms (like me), uninstall it. It's possible that a future Firmware Update to the Mi Band (which is distributed via the Mi Fit App) completely purges the possibility of Early Bird making all your experimenting futile, so I'd get rid of this risk. Additionally depending on your nightly test results, you might install a different version of the App and need to uninstall your current version anyways.

<a href="{{site.url}}/assets/images/2017/2017-02-09-miband-fw-downgrade.png"><img src="{{site.url}}/assets/images/2017/2017-02-09-miband-fw-downgrade.png" style="width: 30%; float: right; margin: 10px;"></a>**4. Downgrade the Mi Band Firmware:** Using [Gadgetbride][gadgetbride] you can downgrade the firmware of the Mi Band. There's a [good article][mifwdowngrade] regarding this process in the [Github wiki of the Gadgetbride repo][mifwdowngrade], so I suggest you stick to this for a firmware downgrade. You need to get the `*.fw` file first which needs to be extracted from an older APK of the App. I use [APKMirror.com][apkmirror] for this. Early Bird Alarm was removed with version 2 of the Mi Fit App, so look for 1.x versions of the App. I personally tried the Mi Fit version [1.5.912 (1539)][mifit15912] which contains the Firmware version 05.15.7.14 and [1.8.711 (1610)][mifit18711] which contains Firmware version 05.15.12.10. According to the [Gadgetbride wiki][mifwinfo] version 05.15.7.14 is the best fit for my Mi Band 1A. I still settled with v05.15.12.10, but that's more coincidence than intent. You will need to either use an alternative App for setting your alarms or the old version of Mi Fit containing this firmware. I wasn't able to get the old versions of Mi Fit connecting to my band, but it might work for you. You can also try to combine an older firmware with a newer App version via injecting the old firmware file into the new App. You can use my blog post on [how to modify and repackage Android Apps][modrepackageandroid] as a starting point for that.
Afterwards I advise to do nightly tests again.

**For now, the combination I use are the Firmware version 05.15.12.10 and the "Tools & Mi Band"-App to set the alarms**. This is pure chance, I already gave up on restoring the Early Bird functionality when it suddenly worked the night I used this combo. But as I already mentioned, my dry testing didn't properly work for this combination either, so it's very possible that other solution mixtures work as well and I might restart testing some time in the future.

If you find a different working solution, please comment with your Mi Band version and the solution so others can be helped as well.


[mibandamazon]: http://a-fwd.com/asin-de=B00Q5P79TO&asin-uk=B00RCOYD50&asin-com=B01A8NRAP6&fb=com
[notifyfitnessmi]: https://play.google.com/store/apps/details?id=com.mc.miband1
[toolsmi]: https://play.google.com/store/apps/details?id=cz.zdenekhorak.mibandtools
[gadgetbride]: https://f-droid.org/repository/browse/?fdfilter=Gadget&fdid=nodomain.freeyourgadget.gadgetbridge
[mifwdowngrade]:https://github.com/Freeyourgadget/Gadgetbridge/wiki/Mi-Band-Firmware-Update
[apkmirror]: https://www.apkmirror.com/?s=Mi+fit&post_type=app_release&searchtype=apk
[mifit18711]:https://www.apkmirror.com/apk/xiaomi-technology/mi-fit/mi-fit-1-8-711-release/mi-fit-1-8-711-android-apk-download/
[mifit15912]: https://www.apkmirror.com/apk/xiaomi-technology/mi-fit/mi-fit-1-5-912-release/mi-fit-1-5-912-android-apk-download/
[mifwinfo]: https://github.com/Freeyourgadget/Gadgetbridge/wiki/Mi-Band-Firmware-Information
[modrepackageandroid]: https://adminswerk.de/modifying-and-repacking-android-apps/