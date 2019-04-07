---
title: Automating Arch Linux setup on an RPi
layout: default.liquid
---

```
#!/bin/bash
set -xe
mkfs.vfat /dev/disk/by-id/mmc-SD16G_0x0000040b-part1
mkfs.ext4 /dev/disk/by-id/mmc-SD16G_0x0000040b-part2
mount /dev/disk/by-id/mmc-SD16G_0x0000040b-part1 boot
mount /dev/disk/by-id/mmc-SD16G_0x0000040b-part2 root
pushd root
tar -xpf /home/rkd/Downloads/ArchLinuxARM-rpi-3-latest.tar.gz
mv boot/* ../boot
popd
umount root boot
```

```
yay -S qemu-user-static
sudo systemctl restart systemd-binfmt.service
systemctl status systemd-binfmt.service
```

```
#!/bin/bash -xe

mount /dev/disk/by-id/mmc-SD16G_0x0000040b-part2 root
mount /dev/disk/by-id/mmc-SD16G_0x0000040b-part1 root/boot
cd root

cp -p ../installer-inside.sh usr/bin
systemd-nspawn -D $PWD usr/bin/installer-inside.sh
cd ..

umount root/boot
umount root
```


```
#!/bin/bash

mv /etc/resolv.conf /etc/resolv.conf.tmp
echo 'nameserver 8.8.8.8' > /etc/resolv.conf

pacman-key --init
pacman-key --populate archlinuxarm

pacman -Syu --noconfirm

pacman -S --noconfirm vim sudo

wpa_passphrase MYSSID PASSPHRASE > /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
systemctl enable wpa_supplicant@wlan0.service
systemctl enable dhcpcd@wlan0


mv /etc/resolv.conf.tmp /etc/resolv.conf
```

```
#!/bin/bash -xe

mount /dev/disk/by-id/mmc-SD16G_0x0000040b-part2 root
mount /dev/disk/by-id/mmc-SD16G_0x0000040b-part1 root/boot
cd root

systemd-nspawn -D $PWD bin/bash
cd ..

umount root/boot
umount root
```

https://en.wikipedia.org/wiki/Binfmt_misc
https://aur.archlinux.org/packages/qemu-user-static/
