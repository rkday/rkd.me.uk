---
title: Automating Arch Linux setup on an RPi
published_date: "2019-04-07 17:31:19 +0000"
layout: default.liquid
is_draft: false
---
I bought a Raspberry Pi 3 recently, and installed Arch Linux, in order to have a small, cheap, home server. For various reasons (e.g. plugging in USB devices with too much power draw, causing corrupted SD card writes) I keep having to reinstall it, so I've put together some scripts to make it simple.

Installing the base system, by putting together a script from <https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3>, is fairly straightforward. I jus plug the microSD card into my laptop and run:

```
#!/bin/bash
set -xe

# Format ad moun the boot and root partitions
mkfs.vfat /dev/disk/by-id/mmc-SD16G_0x0000040b-part1
mkfs.ext4 /dev/disk/by-id/mmc-SD16G_0x0000040b-part2
mount /dev/disk/by-id/mmc-SD16G_0x0000040b-part1 boot
mount /dev/disk/by-id/mmc-SD16G_0x0000040b-part2 root

# Extract the base system tarball into it
pushd root
tar -xpf /home/rkd/Downloads/ArchLinuxARM-rpi-3-latest.tar.gz
mv boot/* ../boot

# Clean up
popd
umount root boot
```

Once the base system is in place, though, there are more setup commands I want to run. Because my laptop is x86_64 and the Pi is ARM, the Pi binaries won't run on my laptop, so I can't just chroot into the install. However, the Linux kernel has a concept of 'binfmt support', effectively 'use this program to run this sort of binary'. This means that I can install qemu-user-static, and it will seamlessly emulate an ARM system when running ARM binaries.

On Arch, using `yay` to access AUR packages, that's done like this:

```
yay -S qemu-user-static
sudo systemctl restart systemd-binfmt.service
systemctl status systemd-binfmt.service
```

So I can then run this script (using systemd-nspawn to do my chrooting, which also sets up things like /dev):

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

where `usr/bin/installer-inside.sh` looks something like this:

```
#!/bin/bash

# resolv.conf is a broken symlink in the chroot, so fix it
mv /etc/resolv.conf /etc/resolv.conf.tmp
echo 'nameserver 8.8.8.8' > /etc/resolv.conf

# Set up Pacman keys as recommended by https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3
pacman-key --init
pacman-key --populate archlinuxarm

# Get any updates
pacman -Syu --noconfirm

# Install useful packages
pacman -S --noconfirm vim sudo

# Set up wifi
wpa_passphrase MYSSID PASSPHRASE > /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
systemctl enable wpa_supplicant@wlan0.service
systemctl enable dhcpcd@wlan0

# Restore resolv.conf
mv /etc/resolv.conf.tmp /etc/resolv.conf
```

And if I break network access to my Pi or want to do other one-off fixing/debugging, I just plug the microSD card back into my laptop and run this to get shell access:

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

Some references:

[The Wikipedia page on binfmt_misc](https://en.wikipedia.org/wiki/Binfmt_misc)
[The Arch Linux RPi instructions](https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3)
The AUR pages for [qemu-user-static](https://aur.archlinux.org/packages/qemu-user-static/) and [binfmt-support](https://aur-dev.archlinux.org/packages/binfmt-support/?comments=all)
The [Stack Exchange answer](https://unix.stackexchange.com/questions/41889/how-can-i-chroot-into-a-filesystem-with-a-different-architechture) that pointed me towards qemu-user-static
