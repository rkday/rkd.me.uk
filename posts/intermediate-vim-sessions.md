---
layout: default.liquid
title: Intermediate Vim - Sessions
published_date: 2016-03-27 11:00:00 +0100
slug: intermediate-vim-sessions
---

I've been trying to improve my skill with Vim recently - I'm definitely nowhere near an expert, but I've been trying to move beyond just the basic "read files/write files/use regexps/install plugins" to understand and use more of Vim's built-in features. I'm planning to write blog posts on a couple of things, including macros, folding and ctags, but the first thing I've dug into and found useful are sessions.

I often have the experience where I'll be deep inside a set of files, then quit vim (perhaps to compile/test some code - which probably indicates that I'm not using `:make` as much as I should, but that's something for another day). Often, I'll want to get back to where I was - e.g. because my fix didn't work and I want to make a further tweak. Until now, my strategy has been "try to remember that I was at line 113, then run `vim +113 file.cpp`", but this doesn't always work well (especially if I've split my window or changed to a new file within Vim, so that my command-line history doesn't reflect what files I was working on). Sessions offer a much better way to do this!

The `:mksession` command creates a Vim session file - a file which preserves the entire state of your editing session (open windows, exact window split, positions within files, etc.). The only thing it doesn't do is save unsaved files, so you need to do that separately. This file defaults to being Session.vim in the current directory, but you can pass an argument to `:mksession` to change that (and use `:mksession!` to overwrite an existing file.)

I now have the following set up in my `.vimrc`:

`cabbrev Q mksession! ~/default_session.vim \| xa`

(which means that typing :Q saves my current session to ~/default_session.vim, then saves all windows and quits - this is using the pipe character `|` to [join multiple commands together](http://vim.wikia.com/wiki/Multiple_commands_at_once))

and the following Bash alias set up:

`alias vims="vim -S ~/default_session.vim"`

(which means that running `vims` restores the last session I saved with :Q)

Hopefully this is useful to others - I think I've covered the main information about Vim sessions, but the full documentation is [here](http://vimdoc.sourceforge.net/htmldoc/usr_21.html#21.4).
