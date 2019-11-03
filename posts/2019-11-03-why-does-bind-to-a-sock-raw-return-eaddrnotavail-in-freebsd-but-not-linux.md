---
title: Why does bind() to a SOCK_RAW return EADDRNOTAVAIL in FreeBSD but not Linux?
published_date: "2019-11-03 10:50:48 +0000"
layout: default.liquid
is_draft: false
---
I tracked down an interesting bug this weekend - a SIPp user [reported](https://github.com/SIPp/sipp/issues/433) getting a "Can't bind media raw socket" error on FreeBSD 11.2, which I was able to repro. This was in the code that replays packet captures of media, by opening a raw socket and sending the media packets through it, with the raw sockets giving it full control (including the UDP headers).

`truss` (which is basically `strace` for FreeBSD) showed the underlying error:

```
socket(PF_INET,SOCK_RAW,IPPROTO_UDP)  = 7 (0x7)
bind(7,{ AF_INET 127.0.0.1:14000 },16)  ERR#49 'Can't assign requested address'
```

127.0.0.1 definitely exists, so what's the problem? Turns out it was the port - when binding a raw socket, you're doing so at the IP level rather than the transport level, so the port is meaningless. It looks like on FreeBSD, as opposed to Linux, supplying a port here is actively forbidden.

The [Linux IP manual page](http://man7.org/linux/man-pages/man7/ip.7.html) comes closest to suggesting this, when it says "Note that the raw IPv4 protocol as such has no concept of a port, they are implemented only by higher protocols like tcp(7) and udp(7)", but the FreeBSD docs on [ip](https://www.freebsd.org/cgi/man.cgi?query=ip&apropos=0&sektion=4&manpath=FreeBSD+11.2-RELEASE&arch=default&format=html), [inet](https://www.freebsd.org/cgi/man.cgi?query=inet&apropos=0&sektion=4&manpath=FreeBSD+11.2-RELEASE&arch=default&format=html) and [bind](https://www.freebsd.org/cgi/man.cgi?query=bind&apropos=0&sektion=2&manpath=FreeBSD+11.2-RELEASE&arch=default&format=html) don't mention this or that `EADDRNOTAVAIL` might be caused by this.

I wrote a test program to verify this, with the port used controlled by a compile-time #define:

```c
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>

int main() {
  int s = socket(AF_INET, SOCK_RAW, IPPROTO_UDP);
  struct sockaddr_storage addr = {0};
  ((struct sockaddr_in*)&addr)->sin_family = AF_INET;
  ((struct sockaddr_in*)&addr)->sin_port = PORT;
  inet_aton("127.0.0.1", &((struct sockaddr_in*)&addr)->sin_addr);
  printf("IP: %s\n", inet_ntoa((((struct sockaddr_in*)&addr)->sin_addr)));
  int rc = 0;
  rc = bind(s, (struct sockaddr*)&addr, sizeof(struct sockaddr_in));
  printf("Bind result on socket %d: %d / %d / %s\n",
         s, rc, errno, strerror(errno));
```

On Linux:

```
[alexander src]# uname -a
Linux alexander 5.4.0-1-MANJARO #1 SMP PREEMPT Mon Oct 21 10:33:33 UTC 2019 x86_64 GNU/Linux
[alexander src]# gcc -o rawbind rawbind.c -DPORT=15000
[alexander src]# ./rawbind 
IP: 127.0.0.1
Bind result on socket 3: 0 / 0 / Success
[alexander src]# gcc -o rawbind rawbind.c -DPORT=0
[alexander src]# ./rawbind 
IP: 127.0.0.1
Bind result on socket 3: 0 / 0 / Success
```

On FreeBSD:

```
root@freebsd:~/sipp # uname -a
FreeBSD freebsd 11.2-RELEASE FreeBSD 11.2-RELEASE #0 r335510: Fri Jun 22 04:32:14 UTC 2018     root@releng2.nyi.freebsd.org:/usr/obj/usr/src/sys/GENERIC  amd64
root@freebsd:~/sipp # gcc -o rawbind rawbind.c -DPORT=15000
root@freebsd:~/sipp # ./rawbind 
IP: 127.0.0.1
Bind result on socket 3: -1 / 49 / Can't assign requested address
root@freebsd:~/sipp # gcc -o rawbind rawbind.c -DPORT=0
root@freebsd:~/sipp # ./rawbind
IP: 127.0.0.1
Bind result on socket 3: 0 / 0 / No error: 0
```

Hopefully this will save someone else some time when they're searching for information about `bind()`, `SOCK_RAW` and FreeBSD!
