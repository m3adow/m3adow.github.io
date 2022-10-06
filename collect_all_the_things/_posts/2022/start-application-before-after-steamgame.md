---
layout: default
title: "Starting applications before and after running a Steam game"
categories:
- Steam
- Gaming
- Windows
---

Once in a while I'm rediscovering [Stardew Valley][stvhumble]*\**, a very relaxing and charming Farming game. Occasionally, I decide to also play it on Android at the time. Sadly, there's no inbuilt way of syncing the saves between my (Windows) PC and my Android device, although the file saves are compatible.

There are a lot of tutorials online how to achieve that, so I won't cover this. I more or less followed [this tutorial][svsynctutorial] on Reddit ([archive.is link][svstutarchive]). In short: I symlinked my saves directory on the PC into my Dropbox folder and  then use an App, [FolderSync][foldersync], to sync these saves to Android.

<a href="{{site.url}}/assets/images/2020/2020-11-05-stardew-valley.jpg"><img src="{{site.url}}/assets/images/2020/2020-11-05-stardew-valley.jpg" style="margin: 10px; max-width: 60%; max-height: auto; border-radius: 5%;" alt="Stardew Valley"></a>

This worked niceley 90% of the time. Sadly, Stardew Valley on PC crashed every once in a while while saving. The error logs in the `ErrorLogs` directory made the problem very clear:

```
Message: The process cannot access the file because it is being used by another process.
InnerException: 
Stack Trace:    at StardewValley.SaveGame.<Save>d__63.MoveNext() in C:\GitlabRunner\builds\Gq5qA5P4\0\ConcernedApe\stardewvalley\Farmer\Farmer\SaveGame.cs:line 344
   at StardewValley.Menus.SaveGameMenu.update(GameTime time) in C:\GitlabRunner\builds\Gq5qA5P4\0\ConcernedApe\stardewvalley\Farmer\Farmer\Menus\SaveGameMenu.cs:line 109
   at StardewValley.Menus.ShippingMenu.update(GameTime time) in C:\GitlabRunner\builds\Gq5qA5P4\0\ConcernedApe\stardewvalley\Farmer\Farmer\Menus\ShippingMenu.cs:line 333
   at StardewValley.Game1._update(GameTime gameTime) in C:\GitlabRunner\builds\Gq5qA5P4\0\ConcernedApe\stardewvalley\Farmer\Farmer\Game1.cs:line 3032
   at StardewValley.Game1.Update(GameTime gameTime) in C:\GitlabRunner\builds\Gq5qA5P4\0\ConcernedApe\stardewvalley\Farmer\Farmer\Game1.cs:line 2913
   at Microsoft.Xna.Framework.Game.Tick()
   at Microsoft.Xna.Framework.Game.HostIdle(Object sender, EventArgs e)
   at Microsoft.Xna.Framework.GameHost.OnIdle()
   at Microsoft.Xna.Framework.WindowsGameHost.RunOneFrame()
   at Microsoft.Xna.Framework.WindowsGameHost.ApplicationIdle(Object sender, EventArgs e)
   at System.Windows.Forms.Application.ThreadContext.System.Windows.Forms.UnsafeNativeMethods.IMsoComponent.FDoIdle(Int32 grfidlef)
   at System.Windows.Forms.Application.ComponentManager.System.Windows.Forms.UnsafeNativeMethods.IMsoComponentManager.FPushMessageLoop(IntPtr dwComponentID, Int32 reason, Int32 pvLoopData)
   at System.Windows.Forms.Application.ThreadContext.RunMessageLoopInner(Int32 reason, ApplicationContext context)
   at System.Windows.Forms.Application.ThreadContext.RunMessageLoop(Int32 reason, ApplicationContext context)
   at System.Windows.Forms.Application.Run(Form mainForm)
   at Microsoft.Xna.Framework.WindowsGameHost.Run()
   at Microsoft.Xna.Framework.Game.RunGame(Boolean useBlockingRun)
   at StardewValley.Program.Main(String[] args) in C:\GitlabRunner\builds\Gq5qA5P4\0\ConcernedApe\stardewvalley\Farmer\Farmer\Program.cs:line 152
```

Another process was accessing the save file, presumably Dropbox which wanted to sync the changed file. Therefore I searched for a solution to automatically stop Dropbox before starting Stardew Valley via Steam and resuming it after I was done playing. While this is pretty easy in Linux, due to Dropbox offering proper command line access, there's no such CLI access on Windows.

<!--more-->

Thusly, I had find another solution. I found it in the `pssuspend` command from Microsofts Sysinternals [PsTools][pstools]. It suspends an application using Windows internal tools. When I exit Stardew Valley, `pssuspend` resumes Dropbox. This is the Batch I'm using, already prepared to being reused. ;-)

```batch
rem @echo off

set PssuspendPath="C:\m3adow\apps\pstools\pssuspend.exe"
set SyncExe="Dropbox.exe"
set GamePath="C:\m3adow\games\steam\steamapps\common\Stardew Valley"
set SteamId=413150
rem Don't use ticks for the variable or the 'tasklist' line will not work properly
set GameExe=Stardew Valley.exe
rem The estimated additional time (to the LoopTime) the game needs to start up
set /A StartupTimeAddition=15
rem The time to sleep between game checks
set /A LoopTime=10

%PssuspendPath% -nobanner "%SyncExe%"

cd %GamePath%
start steam://rungameid/%SteamId%
@ping -n %StartupTimeAddition% localhost> nul

:GAMELOOP
@ping -n %LoopTime% localhost> nul
tasklist /FI "IMAGENAME eq %GameExe%" 2>NUL | find /I /N "%GameExe%">NUL
rem if ERRORLEVEL is 0, the game is still running
if "%ERRORLEVEL%"=="0" GOTO GAMELOOP

rem Do a double resume because Dropbox sometimes doesn't resume properly
%PssuspendPath% -r -nobanner %SyncExe%
@ping -n 1 localhost> nul
%PssuspendPath% -r -nobanner %SyncExe%
```

What does it do exactly?

1. The application `%SyncExe%` is suspended, `Dropbox.exe` in my case.
2. The game with the Steam ID `%SteamId%` is started, Stardew Valley does have the `413150`.
3. Before entering the `GAMELOOP` and waiting `%LoopTime%` seconds the batch waits an additional `%StartupTimeAdditional%` seconds to
ensure a proper game startup
4. In the `GAMELOOP` the batch wait `%LoopTime%` seconds, then checks if the `%GameExe%` exe file - `Stardew Valley.exe` in my case - is in the tasklist of Windows. If so, the
loop is started anew.
5. Otherwise the `%SyncExe%` is resumed twice. Dropbox oftentimes didn't resume the first time, so I lazily added the resume twice which did the job for me.

I hope this helps other people trying something similarly.

*\* = Affiliate Link*

[stvhumble]: https://www.humblebundle.com/store/stardew-valley?partner=m3adow
[svsynctutorial]: https://www.reddit.com/r/StardewValley/comments/b5fb4d/tutorial_sync_saved_games_between_android_and_pc/
[svstutarchive]: https://archive.is/yiLE0
[foldersync]: https://play.google.com/store/apps/details?id=dk.tacit.android.foldersync.lite
[pstools]: https://docs.microsoft.com/en-us/sysinternals/downloads/pstools
