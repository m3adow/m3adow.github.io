---
layout: default
title: "Installing Steam in Ubuntu"
categories:
- linux
- ubuntu
---

I had and still have some issues with Steam on Linux. I wanted to use my native system libraries instead of the ones Steam includes. This is a native feature for Steam. Just start Steam with `STEAM_RUNTIME=0` set and you're good to go. At least in theory. Sadly Steam uses a lot of 32-Bit libraries which are not installed on the average 64-Bit Ubuntu.
I used this command to solve the problem:
