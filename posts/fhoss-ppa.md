---
layout: default.liquid
title: New PPA for OpenIMSCore FHoSS
published_date: 2014-07-06 16:10:07 +0100
slug: fhoss-ppa
---

A while back, I got in touch with the Fraunhofer FOKUS team behind OpenIMSCore, with some fixes I wanted to make to their HSS, and ended up being granted commit access to their repository. I've now made those fixes and wanted to distribute them more widely, so I've set up a PPA and made the Fraunhofer Home Subscriber Server (FHoSS) available as a Ubuntu 12.04 LTS package. (It should be trivial to build and install it for other Ubuntu systems, too, but 12.04 seemed like the best one to start with).

The PPA is at [https://launchpad.net/~rkd-u/+archive/fhoss](https://launchpad.net/~rkd-u/+archive/fhoss) - ` sudo add-apt-repository ppa:rkd-u/fhoss && sudo apt-get update && sudo apt-get install openimscore-fhoss` should install the package.

By default, it asks a series of configuration questions during the install, such as the MySQL database password. I'll be writing a post on debconf automation shortly, for anyone who wants unattended install of FHoSS servers with non-default settings.

I'm now subscribed to [the openimscore-hssdev mailing list](https://lists.sourceforge.net/lists/listinfo/openimscore-hssdev), so should be able to answer questions there or in the comments.
