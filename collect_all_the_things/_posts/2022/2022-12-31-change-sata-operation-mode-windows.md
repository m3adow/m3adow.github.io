---
layout: default
title: "Change SATA operation mode without Windows reinstallation"
categories:
- windows
---

As I recently encountered this problem while exchaning the NVMe of a notebook, here's a quick rundown on how to change the SATA operation 
mode for a Windows system without the requirement for a reinstallation or an OS repair:

1. Boot up Windows as normal
2. Start CMD as admin and run `bcdedit /set safeboot minimal` to enable safe mode on next boot
3. Restart the PC and enter UEFI
4. Now change the SATA Operation mode, in my case from RAID to AHCI
5. Save the UEFI changes and let Windows boot to Safe mode
6. Once again open CMD as admin  and run `bcdedit /deletevalue safeboot` to disable safe mode
7. After another reboot Windows will automatically start with the new drivers enabled
