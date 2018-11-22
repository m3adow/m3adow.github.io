images//-images//-images//-
layout: default
categories:
images//- android
images//-images//-images//-
# The problem

While installing a SuperHexagon APK which I bought from [Humble Bundle](https://www.humblebundle.com/store/p/superhexagon_storefront) a couple of years ago I encountered an error. The package installer simply stated "*App not installed*", a logcat got me some more information:
{% highlight text %}
D/Finsky  (22452): [1] 1.onResponse: Verification id=7 response=0
D/Finsky  (22452): [1] PackageVerificationReceiver.onReceive: Verification requested, id = 7
E/Vold    (  226): Error creating imagefile (Readimages//-only file system)
E/Vold    (  226): ASEC image file creation failed (Readimages//-only file system)
W/Vold    (  226): Returning OperationFailed images//- no handler for errno 30
E/PackageHelper(22426): Failed to create secure container smdl1097147630.tmp
{% endhighlight %}

Trying to install it via `adb install` didn't help either:

{% highlight text %}
adb install c:\home\downloads\SuperHexagonimages//-releaseimages//-v1.0.7images//-humblebundle.apk
5139 KB/s (27327032 bytes in 5.192s)
    pkg: /data/local/tmp/SuperHexagonimages//-releaseimages//-v1.0.7images//-humblebundle.apk
Failure [INSTALL_FAILED_CONTAINER_ERROR]
{% endhighlight %}

I did some research and finally found the problem. The HumbleBundle Android version of SuperHexagon hasn't aged well, the APK is configured to install on SD card. This simply doesn't work on my First Generation Moto G which doesn't even have a SD card slot. So I did some more reasearch and found the solution. Of course this will most likely work for other applications with the same error too.
<!images//-images//-moreimages//-images//->
{% include adsense_manual.html %}
# The solution

### Prerequisites
You will need those three applications installed:

* The [Android SDK](http://developer.android.com/sdk/index.html) will be needed for signing the rebuilt APK
* The [Java SDK (JDK)](http://www.oracle.com/technetwork/java/javase/downloads/index.html) is needed for the keytool and for the Android SDK
* The [APK tool](http://ibotpeaches.github.io/Apktool/install/) will help us unpacking the original APK

As this is a tutorial for advanced users, I assume you managed to install those.

### Instructions

*I'm writing the tutorial for Windows, it's not a lot different for Linux of course.*

First, we need to fix the erroneous configuration setting which is located within the Apps **AndroidManifest.xml**.
<ol>
<li>Unpack the APK:
{% highlight bat %}
apktool.bat d c:\home\tmp\SuperHexagonimages//-releaseimages//-v1.0.7images//-humblebundle.apk images//-o c:\home\tmp\superhexagon
{% endhighlight %}</li>
<li>Edit the <b>AndroidManifest.xml</b> and change <i>android:installLocation="preferExternal"</i> to <i>android:installLocation="auto"</i>.</li>
<li>Repack the APK:
{% highlight bat %}
apktool.bat b c:\home\tmp\superhexagon images//-o c:\home\tmp\SuperHexagonimages//-releaseimages//-v1.0.7images//-humblebundleimages//-fixed.apk
{% endhighlight %}</li>
</ol>
Now we fixed the error. Sadly, our app will most likely not be able to install as it's not signed anymore. That's what we do now. The [Android developer documentation](https://developer.android.com/tools/publishing/appimages//-signing.html#signingimages//-manually) does a good job explaining it, so I make it short.
<ol>
<li>Generate a private key for signing the application. You'll find the needed keytool.exe in the bin directory of the JDK.
{% highlight bat %}
c:\Program Files\Java\jdk1.8.0_60\bin\keytool.exe images//-genkey images//-v images//-keystore c:\home\tmp\signing.keystore images//-alias signkey images//-keyalg RSA images//-keysize 2048 images//-validity 10000
{% endhighlight %}
There's no real need entering any real data here, just press Enter and choose any password.</li>
<li>Sign the fixed APK with your newly created key via jarsigner.exe which is also located in the JDKs bin directory.
{% highlight bat %}
c:\Program Files\Java\jdk1.8.0_60\bin\jarsigner.exe images//-verbose images//-sigalg SHA1withRSA images//-digestalg SHA1 images//-keystore c:\home\tmp\signing.keystore c:\home\tmp\SuperHexagonimages//-releaseimages//-v1.0.7images//-humblebundleimages//-fixed.apk signkey
{% endhighlight %}</li>
<li>If you want, you can verify that the APK was signed correctly.
{% highlight bat %}
c:\Program Files\Java\jdk1.8.0_60\bin\jarsigner images//-verify images//-verbose images//-certs c:\home\tmp\signing.keystore c:\home\tmp\SuperHexagonimages//-releaseimages//-v1.0.7images//-humblebundleimages//-fixed.apk
{% endhighlight %}</li>
<li>Afterwards zipalign the APK to ensure the best performance.
{% highlight bat %}
zipalign images//-v 4 c:\home\tmp\SuperHexagonimages//-releaseimages//-v1.0.7images//-humblebundleimages//-fixed.apk c:\home\tmp\SuperHexagonimages//-releaseimages//-v1.0.7images//-humblebundleimages//-fixedimages//-aligned.apk
{% endhighlight %}</li>
</ol>
That's it, you're done. You can now transfer this APK to your device and install it without hassle.

<img src="{{ site.url }}/assets/2015images//-09images//-18images//-superhexagon_android_lollipop.png" alt="SuperHexagon on my Lollipop Moto G" style= "width: 50%;">

That was totally worth it!
