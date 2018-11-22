---
layout: default
title: "Using the Spotify Web player on Android"
categories:
- Android
- Web
---

A friend of mine asked me if it was possible to use the Spotify Web Player on his Android smartphone.  

<a href="{{site.url}}/assets/images/2018/2018-10-15-spotify-app-android.png"><img src="{{site.url}}/assets/images/2018/2018-10-15-spotify-app-android_thumb.png" style="width: 30%; margin: 10px; float: right" alt="Spotify Android App"></a>

If you are like me and don't use Spotify on mobile very often, you might not know that the free version of the Spotify app is heavily castrated. I'm not using it a lot, but if I understood correctly, you can't properly play a playlist or one song, you get force fed "matching" songs. Also you can't constantly skip songs. To push their Premium Account to you, Spotify additionally prevents mobile browsers from using their less limited Web player.

While I understand that Spotify wants to earn money, I heavily dislike the artificial limitations to push people to a paying account. If you can't sell your Premium Account with a feature list, you should probably work on the list instead of artificially limiting the features on different devices. Especially the differentiation between PC and mobile browsers triggered me. Therefore I welcomed the challenge of convincing Spotifys Web player to work on Android.

<!--more-->

{% include adsense_manual.html %}

# Browser

The Spotify Web Player uses [EME][eme](Encrypted Media Extensions), so we'll need a Browser supporting these. I used [Firefox Nightly][ffnightly], as I'm already using Firefox on all my devices anyways and I strongly dislike Chrome.

As Spotify seems to [check the phone resolution][reddit_1], we need to configure Firefox to return an accepted resolution.

1. Enter `about:config` into a tabs URL window
2. Search for `layout.css.devPixelsPerPx`
3. Change it from `-1.0` to a positive value, `1` is a good starter

<a href="{{site.url}}/assets/images/2018/2018-10-15-firefox-devpixelsperpx.png"><img src="{{site.url}}/assets/images/2018/2018-10-15-firefox-devpixelsperpx.png" style="width: 60%; margin: 10px;" alt="Firefox Mobile about:config - layout.css.devPixelsPerPx"></a>

You can experiment with this value, for my OnePlus 3T and my friends Samsung Galaxy S6, setting it to **2** worked well.

This will change how web sites will be scaled, so don't be surprised if everything is very small now.

# Addons

Sadly, using Firefox Nightly with the changed scaling settings is not sufficient. We need to use two additional Firefox Addons: **[User-Agent Switcher and Manager][useragentswitcher]** and **[uBlock Origin][ublock]**.

{% include adsense_manual_link.html %}

## Changing the User-Agent

Spotify Web also checks your [User-Agent string][useragent_wiki]. As your browser "admits" it's running on an Android device, you will still be redirected to the "Download the App, hurr durr!"-site. Therefore we need to change the User-Agent string Firefox sends to Spotify.

1. Install the already mentioned [User-Agent Switcher and Manager][useragentswitcher] Addon in Firefox Nightly
2. Select "User-Agent Switcher and Manager" from the 3-dot menu
3. Select a nice User-Agent from the list. I chose a recent Firefox Version (Firefox 63.0) with Windows 7, just because it's most likely one of the most used User-Agents.
4. Don't forget to press "Apply".

<a href="{{site.url}}/assets/images/2018/2018-10-15-firefox-user-agent-switch-settings.png"><img src="{{site.url}}/assets/images/2018/2018-10-15-firefox-user-agent-switch-settings_thumb.png" style="width: 60%; margin: 10px;" alt="Firefox Mobile: User Agent Switcher and Manager"></a>

## uBlock Origin

In theory this should suffice to let you use Spotifys Web Player. But I had a lot of Firefox crashes while testing, this setup. Adding a block rule to uBlock Origin seemed to fix that.

1. Download the [uBlock Origin][ublock] Addon
2. Go into its configuration (Addons -> uBlock Origin -> Options)
3. Go to "My filters"
4. Add `||www.spotify.com/*$document,domain=www.spotify.com` in the list

<a href="{{site.url}}/assets/images/2018/2018-10-15-firefox-ublock-spotify-rule.png"><img src="{{site.url}}/assets/images/2018/2018-10-15-firefox-ublock-spotify-rule.png" style="width: 60%; margin: 10px;" alt="Firefox Mobile: ublock Origin rule"></a>

After all those configurations, I was able to successfully use the Spotify Web Player from my OnePlus 3T Android device. My friend was able to use it from his Galaxy S6 as well.  
If you don't hear any sound, don't forget to check your current playback device (the PC icon in the lower right corner).

<a href="{{site.url}}/assets/images/2018/2018-10-15-spotify-web-android-devices.png"><img src="{{site.url}}/assets/images/2018/2018-10-15-spotify-web-android-devices_thumb.png" style="width: 30%; margin: 10px;" alt="Firefox Mobile: Spotify Web Player"></a>

This could work on iOS as well, but I have neither tested it nor do I have any interest in doing so.

[eme]: https://en.wikipedia.org/wiki/Encrypted_Media_Extensions
[ffnightly]: https://play.google.com/store/apps/details?id=org.mozilla.fennec_aurora
[reddit_1]: https://www.reddit.com/r/firefox/comments/81nlk6/is_it_possible_to_use_the_spotify_web_player_on/dw1jrhb/
[useragentswitcher]: https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher/?src=search
[ublock]: https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/?src=search
[useragent_wiki]: https://en.wikipedia.org/wiki/User_agent#Use_in_HTTP