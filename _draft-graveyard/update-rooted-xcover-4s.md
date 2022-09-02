# Update rooted XCover 4s

1. Do Backup!!!
2. Download new Firmware with Frija:
   Model: SM-G398FN
   CSC: DBT
3. Extract Zip file, untar AP file
4. Extract `boot.img.lz4`, on Windows this might be possible with [7-ZIP ZS](https://www.majorgeeks.com/files/details/7_zip_zs.html)
5. Rename `magisk_patched.img` to `boot.img`
6. Tar `boot.img`
7. Change to Download Mode via `adb reboot download`
8. "AP" Flash with Odin v3.13.1
9. Start Magisk Manager after Reboot which will trigger another rebbot
