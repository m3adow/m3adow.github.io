---
layout: default
title: "Steam: Fix Software install on every Startup"
categories:
- steam
---

While enjoying first playthrough of [Borderlands 2][hb_bl2], I encountered an annoyance. Every time I started the game, Steam tried a first-time setup by installing the Visual C++ 2010 Redistributable Package (vcredist). Additionally it also required me to confirm the install process every time, due to Windows UAC. I encountered similar annoyances a couple of weeks later when playing [Dishonored][hb_dh].

Some research revealed that this is a very common issue with Steam games, especially older(ish) ones. For some reason the required program installations are not recognised which leads to this installation dialogue before each game start.

<a href="{{site.url}}/assets/images/2021/2021-01-07-steam-first-time-setup.png"><img src="{{site.url}}/assets/images/2021/2021-01-07-steam-first-time-setup.png" style="margin: 10px;" alt="League of Legends Steam properties"></a>

I did some more digging and found out, that the source often times lies in a missing Windows Registry key. Therefore I created a Github Gist which contains all registry entries I could find: [https://gist.github.com/m3adow/721947cf076a0eec5bc2b194e16853d9][gist]
Here's a short instruction how to use the Registry Gist:

1. Get the Steam ID of the game which bugs you with the installation on every start. The easiest ways are by checking the desktop shortcut. Right-Click it, choose "Properties" and note down the number in the `URL` entry after `steam://rungameid/`. In the picture below that would be `20590`.  
<a href="{{site.url}}/assets/images/2021/2021-01-07-steam-league-of-legends.png"><img src="{{site.url}}/assets/images/2021/2021-01-07-steam-league-of-legends.png" style="margin: 10px;" alt="League of Legends Steam properties"></a>
2. Copy the Code from my [Gist](gist) into a new text file. Save the text file with a `.reg` file extension, `steamfix.reg` for example.
3. Change the `{% raw %}{{ INSERTYOURAPPIDHERE }}{% endraw %}` part to the Steam ID of your game and save the file. In my example the replacement would result in `[HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Valve\Steam\Apps\20590]`.
4. Double click the file and confirm you really want to apply these changes.

BAM! You're done. The installation of programs at each start of the game should be history.  
If this is not the case please add a comment containing the game, its Steam ID and the software it tries to install every time, so others or I are able to invest more research into it.

[hb_bl2]: https://www.humblebundle.com/store/borderlands-2-game-of-the-year?partner=m3adow
[hb_dh]: https://www.humblebundle.com/store/dishonored?partner=m3adow
[gist]: https://gist.github.com/m3adow/721947cf076a0eec5bc2b194e16853d9
