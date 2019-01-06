---
layout: default.liquid
title: Four cool things from KamailioWorld 2014
published_date: 2014-04-15 20:50:00 +0100
slug: kamailio2014
---

A week ago I got back from KamailioWorld in Berlin, where I was giving a talk on performance testing. I really enjoyed myself - it's a nicely-run conference, and it's useful to talk to the broader open-source community and find out about new trends (WebRTC, stronger cryptography) and tools.

I've decided to write up (partly for my own reference) four cool tools I learnt about at KamailioWorld and hope to get some use out of in the near future.

# The Twinkle softphone

I'd been vaguely aware of the Twinkle softphone, but because it's Linux-only and I use Windows 7 at work, hadn't paid much attention to it - I mostly use cross-platform phones like Jitsi or Blink. However, I noticed the Twinkle configuration window during another presentation, and noticed that it has support for IMS-AKA authentication - this is something hardly any phones have, but which is really imnportant if you'redoing any IMS development or testing. I'll definitely check Twinkle out next time I'm working on AKA.

# sipgrep v2

This is an updated rewrite of the old sipgrep tool, moving from Perl to C. I've never used the new or old version, but it has a lot of features that make checking SIP traffic easy compared to just tcpdump - such as coloured output and the ability to match on specific headers. (It may be that it's not much more useful than taking a capture file and opening it in Wireshark - but it's worth a look, and if nothing else it'll be quicker on remote systems.)

# mts-project

I was discussing Seagull, the Diameter test tool, and someone pointed me at MTS as an alternative. I'd never heard of it before - and it doesn't obviously come up in search results for a Diameter test tool - but it looks reasonably fully-featured and usable. I'll give it a try next time I need to reproduce a FHoSS bug - I had been building a test suite in JRuby that wrapped the jDiameter stack, but maybe MTS will be a good alternative.

# Jitsi Videobridge

This is basically a free-software version of Google Hangouts (which I use a lot for team meetings) - video conferencing over WebRTC. The live demos were pretty impressive, and I'm hoping to set it up one evening and have a play with it for myself. (Unfortunately Firefox's WebRTC support isn't good enough for it yet, which is sad.)

There was a lot of other cool stuff on display - sip:provider ce, CGRateS and OpenEPC, just to name a few - but I've tried to limit this post to just the ones I expect to use myself in the near future. AS you can tell, I learnt a lot from KamailioWorld - here's to next year!
