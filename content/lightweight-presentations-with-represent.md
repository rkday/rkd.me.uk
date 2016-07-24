Title: Lightweight presentations with represent
Date: 2016-07-09 16:15
Category: None
Author: Rob Day
Slug: lightweight-presentations-with-represent

I've been trying to find a good, lightweight way to write technical presentations for a while now. Specifically, I'm looking for one that avoids some of the common problems with Powerpoint:

* no need to mess around endlessly with styles, fonts etc. - it should look good out of the box
* easy to represent code snippets
* possible to create, edit and run anywhere - I use a Linux laptop, but often transfer presentations to Windows laptops, so this is important

In the last week, I've discovered present and represent, the tools used for presentations about the Go programming language, and these are now my go-to presentation tools. (For an example presentation, look at [Powered by Go](https://talks.golang.org/2013/oscon-dl.slide).)

These tools work with `.slide` files describing a presentation - you can get the full description at <https://godoc.org/golang.org/x/tools/present>, but here's an example file:

```
Title of document
15:04 2 Jan 2006
<blank line>
Author Name

* Slide 1

Text goes here

- bullets
- more bullets

* Slide 2

   def fn():
       print("Here is some code")
```

After creating a .slide file, if you [install Go](https://golang.org/doc/install), run `go get golang.org/x/tools/cmd/present` and then run `present` (or `$GOPATH/bin/present` if `$GOPATH/bin` isn't in your path), it will run a local web server listing the .slide files and rendering them as HTML.

Often, though, I want to have presentations for offline viewing (being able to copy them onto the conference organiser's laptop, for example), in which case I use [represent](http://cmars.github.io/represent/#1) (`go get github.com/cmars/represent`). With this, you can just run `represent` and it'll convert all the .slide files in the current directory into HTML presentations in a subdirectory called `publish`.

### UltiSnips

In order to help me remember the format of .slide files (both heading and slide format), I've created a [UltiSnips snippet](https://github.com/SirVer/ultisnips#ultisnips) for it, which means I can just type `hhh<Tab>` in a new .slide file and get a template:

`~/.vim/UltiSnips/slide.snippets`:

```
snippet hhh "Slide headings" b
${1:title}
${2:subtitle}
`date "+%e %b, %Y"`

Rob Day
rkd@rkd.me.uk
http://rkd.me.uk
@day_rk

* ${3:First slide title}

endsnippet
```

(I needed `au BufNewFile,BufRead *.slide set filetype=slide` in my .vimrc to make .slide a recognised file type).

### Alternatives

I've also tried a couple of other lightweight slide formats in the past, but I preefer repesent. I've tried:

* cleaver, which is NodeJS-based - I'm more of a systems programmer than a web app programmer, so I'm more comfortable having Go installed on my system than Node
* remark, which involves embedding Markdown into a HTML file, which I find looks cluttered (I just want a file describing my slide, and to have the infrrastructure take care of surrounding stuff!)

The present/represent toolchain give me nice-looking slides, with a simple markup format, and don't require me to install much that I wouldn't have installed anyway - I suspect I'll use this as my preferred presentation tool for a while.
