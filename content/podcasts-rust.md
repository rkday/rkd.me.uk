Title: Podcasts on the command-line, in Rust
Date: 2018-04-08 22:10
Category: None
Author: Rob Day
Slug: rust-podcasts

I've been listening to more podcasts recently on my commute and at the gym, including [New Rustacean](https://newrustacean.com/) and [AB Testing](http://www.angryweasel.com/ABTesting/). I currently use [Clementine](https://www.clementine-player.org/) to manage my podcasts, but it's not perfect - the "Copy to device" menu option was greyed out this morning, so I had to copy podcast episodes on manually.

I've been looking for a small project to work on to practice Rust, and here I have a problem that needs solving - so I've spent some time today hacking together a simple text interface program in Rust to manage podcasts. The code is at <https://github.com/rkday/podcast-manager.rs>.

Here's a screenshot:

![Screenshot](/static/podcasts_screenshot.png)

Currently, it can:

- download and parse an RSS feed
- show all podcast episodes as a list
- allow the user to scroll through that list with Up and Down
- show extra information about an episode in the siebar

Next steps:

- download the MP3 to my MP3 player when I hit 'y'
- allow multiple podcasts (currently, AB Testing is hardcoded)
- fix the unhelpful delay at the start where it downloads the feed URL (a loading screen? caching?)

Longer-term futures:

- support feed formats like Atom
- support deleting podcasts off a device
- maybe even support playback from the console?

Rust turned out to be a pretty reasonable language for this kind of thing - the <https://github.com/fdehau/tui-rs> crate is quite impressive, and the ecosystem is already far enough along for <https://github.com/rust-syndication/rss> to exist.

I did spot one bug in the wider Rust ecosystem when writing this - the AB Testing podcast's descriptions crashed the Rust textwrap library due to https://github.com/mgeisler/textwrap/issues/129 - but that's now fixed.