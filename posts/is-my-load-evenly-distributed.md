---
layout: default.liquid
title: Is my load evenly distributed?
published_date: 2016-04-16 10:59:00 +0100
slug: is-my-load-evenly-distributed
---

I recently had a log file full of timestamped data, and I needed to analyse it to see how evenly distributed it was. Turns out this is surprisingly easy with standard GNU command-line tools.

The data looked like this:

```
15-04-2016 11:01:02.897 UTC 200 GET /foobar 0.000048 seconds
15-04-2016 11:01:02.905 UTC 200 GET /foobar 0.000492 seconds
15-04-2016 11:01:03.031 UTC 200 GET /foobar 0.000032 seconds
15-04-2016 11:01:03.034 UTC 200 PUT /foobar 0.001252 seconds
15-04-2016 11:01:03.340 UTC 200 GET /foobar 0.000041 seconds
15-04-2016 11:01:03.344 UTC 200 GET /foobar 0.000668 seconds
15-04-2016 11:01:03.441 UTC 200 GET /foobar 0.000030 seconds
15-04-2016 11:01:03.446 UTC 200 PUT /foobar 0.002239 seconds
15-04-2016 11:01:03.750 UTC 200 PUT /foobar 0.005282 seconds
15-04-2016 11:01:04.657 UTC 200 GET /foobar 0.000056 seconds
...
```

So first, I piped it through `cut` to extract just the timestamp field:

```
$ cat ~/logfile.txt | cut -f2 -d " " 
11:01:02.897
11:01:02.905
11:01:03.031
11:01:03.034
11:01:03.340
11:01:03.344
11:01:03.441
11:01:03.446
11:01:03.750
11:01:04.657
...
```

And then through sed to delete the last two characters, grouping the data into 100ms windows:

```
$ cat ~/logfile.txt | cut -f2 -d " " | sed "s/..$//"
11:01:02.8
11:01:02.9
11:01:03.0
11:01:03.0
11:01:03.3
11:01:03.3
11:01:03.4
11:01:03.4
11:01:03.7
11:01:04.6
...
```

I then piped that into `uniq -c`, which removes duplicate lines and gives a count of how many duplicates there were:

```
$ cat ~/logfile.txt | cut -f2 -d " " | sed "s/..$//" | uniq -c
      1 11:01:02.8
      1 11:01:02.9
      2 11:01:03.0
      2 11:01:03.3
      2 11:01:03.4
      1 11:01:03.7
     16 11:01:04.6
      2 11:01:05.2
      2 11:01:05.4
      4 11:01:05.7
      1 11:01:06.0
      6 11:01:06.6
      2 11:01:07.0
      2 11:01:07.1
      2 11:01:07.4
      2 11:01:07.5
      1 11:01:07.8
      3 11:01:08.1
      3 11:01:08.3
      2 11:01:08.6
      2 11:01:08.9
```

and finally into `sort -nr`, which showed me the time windows with the highest number of requests:

```
$ cat ~/logfile.txt | cut -f2 -d " " | sed "s/..$//" | uniq -c | sort -nr
     16 11:01:04.6
      6 11:01:06.6
      4 11:01:05.7
      3 11:01:08.3
      3 11:01:08.1
      2 11:01:08.9
      2 11:01:08.6
      2 11:01:07.5
      2 11:01:07.4
      2 11:01:07.1
      2 11:01:07.0
      2 11:01:05.4
      2 11:01:05.2
      2 11:01:03.4
      2 11:01:03.3
      2 11:01:03.0
      1 11:01:07.8
      1 11:01:06.0
      1 11:01:03.7
      1 11:01:02.9
      1 11:01:02.8

```

Picking out this data helped me prove that the incoming data wasn't evenly distributed - there were some short bursts of traffic - and so I was able to start figuring out where the load spikes were coming from, rather than debugging my (working) overload control algorithm. Hurrah!
