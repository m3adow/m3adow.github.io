---
layout: default
title: "Solving multi monitor mouse problems in fullscreen applications"
categories:
- Windows
- Gaming
---

I've been an avid gamer for ages. I've also been using two monitors for ages. And I've had my [fair share]({% post_url 2015/2015-12-20-steam-in-ubuntu %}) of [problems]({% post_url 2015/2015-12-29-multi-monitor-wallpaper-ubuntu %}) with this combination already.

Some time ago I broke my arm. Therefore my gaming life was handicapped severely and I was limited to mouse only games. No big deal, there are still a lot of games waiting to be played in my Steam and GoG libraries. As I'm German, I of course decided to start with some economy simulations. Anno 1404 and Tropico 4 were my first choice of games.

Sadly both games had some kind of problem with my second monitor. Tropico 4 didn't capture my cursor, leading to issues with scrolling via cursor movement to the right edge of the screen. As the cursor moved to the second screen then, a click would lead to a minimization of the game, which was pretty annoying after some time.

<a href="{{site.url}}/assets/images/2017/2017-11-11-tropico-4.png"><img src="{{site.url}}/assets/images/2017/2017-11-11-tropico-4-thumb.jpg" style="margin: 10px;" alt="Tropico 4"></a>

<!--more-->

{% include adsense_manual.html %}

While Anno 1404 didn't have this problem in Fullscreen mode, the same issue occured when I switched to Window Mode so I could take advantage of f.lux color correction.  
After a couple of hours I grew tired of these issues and searched for solutions. In a [Steam Community thread](https://steamcommunity.com/app/245620/discussions/0/540742579609970174/) for Tropico 5 I found the key to my solution, [Dual Monitor Tools](http://dualmonitortool.sourceforge.net/) was mentioned (yes, I know about the second "Step 5" in the quote).

> *I found a solution ... Dual Monitor Tools. Nice little programs, FREE!
http://dualmonitortool.sourceforge.net/  
> Before you start a game you will press a key combination (which you will configure below). This will lock the mouse inside the screen; it will not be able to go to any of your other monitors until you press that same key combination again. In doing this it also locks your mouse inside the game.  
> The program comes as a zip file and requires no installation. To use the application simply unzip it to a directory of your choice.  
> Step 1) Open the directory you just extracted the zip to  
> Step 2) Double click “SwapScreen.exe”  
> Step 3) Right click Swap Screen next to your clock  
> Step 4) Left click Options  
> Step 5) Left click on the “Cursor” tab  
> Step 6) Go down under “Lock Cursor onto screen” and click “Change”. Now select a key combination of your choice.  
> Step 5) Click close.*

While this was already quite good, I strived to automate the process. So I wrote a small Batch script.

```powershell
@echo off
rem The path to the Dual Monitor Tools Installtion
set dmt_path="C:\m3adow\apps\dual-monitor-tools"
rem The Path to the game executable
set mygame="C:\m3adow\games\gog\Anno 1404 Gold Edition\Anno4.exe"
rem Get the Game directory from the game exe path
for %%F in (%mygame%) do set gamedir=%%~dpF
echo "DMT path is set to %dmt_path%"
start /MIN "" %dmt_path%\DMT.exe
rem Wait 3 seconds to ensure DMT has started
ping -n 3 127.0.0.1 > nul

start /MIN "" %dmt_path%\DMT.exe DMT:Cursor:CursorToPrimaryScreen DMT:Cursor:LockCursor
start /D "%gamedir%" ""  /WAIT %mygame%
start "" %dmt_path%\DMT.exe DMT:Cursor:FreeCursor
```

This script ensures DMT is started, then sends two internal commands to DMT, `DMT:Cursor:CursorToPrimaryScreen` and `DMT:Cursor:LockCursor`. The first one moves the cursor to the Primary Screen, the second one then locks the cursor to its current screen.  
Afterwards the game itself is started, while the batch script patiently waits in the background. When the game is ended, the `DMT:Cursor:FreeCursor` command is executed, unlocking the cursor again.

<a href="{{site.url}}/assets/images/2017/2017-11-11-anno1404-window-mode.png"><img src="{{site.url}}/assets/images/2017/2017-11-11-anno1404-window-mode-thumb.jpg" style="margin: 10px;" alt="Anno 1404"></a>

This batch script works like a charm for Anno 1404 in window mode, solving my issue completely. Sadly,Tropico 4 uses some obscure launcher solution which somehow impedes functionality of the batch. Thusly I still need to use the manual option for it.  
Still, if you have a need for such a solution either for these games or for others, feel free to try it or even improve it. Any contribution in the comments would be appreciated.
