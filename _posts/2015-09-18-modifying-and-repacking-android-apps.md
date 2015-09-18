---
layout: default
categories:
- android
---
# The problem

While installing a SuperHexagon APK which I bought from [Humble Bundle](https://www.humblebundle.com/store/p/superhexagon_storefront) a couple of years ago I encountered an error. The package installer simply stated "*App not installed*", a logcat got me some more information:
{% highlight text %}
D/Finsky  (22452): [1] 1.onResponse: Verification id=7 response=0
D/Finsky  (22452): [1] PackageVerificationReceiver.onReceive: Verification requested, id = 7
E/Vold    (  226): Error creating imagefile (Read-only file system)
E/Vold    (  226): ASEC image file creation failed (Read-only file system)
W/Vold    (  226): Returning OperationFailed - no handler for errno 30
E/PackageHelper(22426): Failed to create secure container smdl1097147630.tmp
{% endhighlight %}

Trying to install it via `adb install` didn't help either:

{% highlight text %}
adb install c:\home\downloads\SuperHexagon-release-v1.0.7-humblebundle.apk
5139 KB/s (27327032 bytes in 5.192s)
    pkg: /data/local/tmp/SuperHexagon-release-v1.0.7-humblebundle.apk
Failure [INSTALL_FAILED_CONTAINER_ERROR]
{% endhighlight %}

I did some research and finally found the problem. The HumbleBundle Android version of SuperHexagon hasn't aged well, the APK is configured to install on SD card. This simply doesn't work on my First Generation Moto G which doesn't even have a SD card slot. So I did some more reasearch and found the solution. Of course this will most likely work for other applications with the same error too.
<!--more-->

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

1. Unpack the APK:

    {% highlight bat %}
    apktool.bat d c:\home\tmp\SuperHexagon-release-v1.0.7-humblebundle.apk -o c:\home\tmp\superhexagon
    {% endhighlight %}

2. Edit the **AndroidManifest.xml** and change *android:installLocation="preferExternal"* to *android:installLocation="auto"*.
3. Repack the APK:

    {% highlight bat %}
    apktool.bat b c:\home\tmp\superhexagon -o c:\home\tmp\SuperHexagon-release-v1.0.7-humblebundle-fixed.apk
    {% endhighlight %}

Now we fixed the error. Sadly, our app will most likely not be able to install as it's not signed anymore. That's what we do now. The [Android developer documentation](https://developer.android.com/tools/publishing/app-signing.html#signing-manually) does a good job explaining it, so I make it short.

1. Generate a private key for signing the application. You'll find the needed keytool.exe in the bin directory of the JDK.

    {% highlight bat %}
    c:\Program Files\Java\jdk1.8.0_60\bin\keytool.exe -genkey -v -keystore c:\home\tmp\signing.keystore -alias signkey -keyalg RSA -keysize 2048 -validity 10000
    {% endhighlight %}

    There's no real need entering any real data here, just press Enter and choose any password.

2. Sign the fixed APK with your newly created key via `jarsigner.exe` which is also located in the JDKs bin directory.

    {% highlight bat %}
    c:\Program Files\Java\jdk1.8.0_60\bin\jarsigner.exe -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore c:\home\tmp\signing.keystore c:\home\tmp\SuperHexagon-release-v1.0.7-humblebundle-fixed.apk signkey
    {% endhighlight %}

3. If you want, you can verify that the APK was signed correctly.

    {% highlight bat %}
    c:\Program Files\Java\jdk1.8.0_60\bin\jarsigner -verify -verbose -certs c:\home\tmp\signing.keystore c:\home\tmp\SuperHexagon-release-v1.0.7-humblebundle-fixed.apk
    {% endhighlight %}

4. Afterwards zipalign the APK to ensure the best performance.

    {% highlight bat %}
    zipalign -v 4 c:\home\tmp\SuperHexagon-release-v1.0.7-humblebundle-fixed.apk c:\home\tmp\SuperHexagon-release-v1.0.7-humblebundle-fixed-aligned.apk
    {% endhighlight %}

That's it, you're done. You can now transfer this APK to your device and install it without hassle.

<img src="../assets/2015-09-18-superhexagon_android_lollipop.png" alt="SuperHexagon on my Lollipop Moto G" width="50%" height="50%">

That was totally worth it!
