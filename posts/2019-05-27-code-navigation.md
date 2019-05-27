---
title: Code navigation
published_date: "2019-05-27 20:25:23 +0000"
layout: default.liquid
is_draft: false
---
I've recently been trying to improve my skills at navigating code. I've used Vim's `ctags` support and the `ctrlp` package, but they've never really stuck - possibly I just find it tricky to remember new Vim keybindings or commands - so my normal approach to "find this function in this codebase" is still to grep it from the command line.

I find it easier to remember command-line tools, though - I switched from grep to ripgrep a while ago and typing 'rg' instead of 'grep' was a fairly painless move to make. Given that, I've been trying to optimise my workflow with better command-line tools as well as vim shortcuts.

## ripgrep -> vim

Quite often, I find some code I want to view/edit by running ripgrep, then copying and pasting the filename back into my terminal. That's obviously inefficient - I'd like to just jump straight from the ripgrep results to a vim session.

I've set ripgrep as the grep command vim uses (in `~/.vimrc`

```
set grepprg=rg\ --vimgrep
```

and I've defined an rgv (ripgrep -> vim) command in my shell:

```
function rgv() { vim -c "silent grep $1" -c "copen"; }
```

This runs a ripgrep search, then launches Vim with the results in a quickfix window I can navigate:

![Demo of the rgv command](/static/rgv.gif)

I also have a slightly less good alternative where I run:

```
rg -n Python | vim -
```

which opens the ripgrep output in vim, and I can then hit gF to jump to the filename/line under the cursor. This lacks the colourcoding and convenience of the quickfix list, though.


## Command-line tag search

In addition to being able to use ripgrep from the command line, and being able to use `Ctrl-]` in vim to jump to a tag, I thought it would be useful to navigate to a particular tag from the command-line.

I set up this Bash alias:

```
alias t='vim -t "$(cut -f1 tags | tail +7 | uniq | fzf)"'
```

where `cut -f1 tags | tail +7 | uniq` extracts the tag names from the `tags` file, `fzf` is a fuzzy-finder that lets me search them, and `vim -t TAG` opens vim at a particular tag. 

![Demo of the t command](/static/t.gif)

## Keeping tag files up-to-date

One aspect I haven't completely cracked is how to keep tag files up-to-date.

* My best current idea (which I still need to set up) is a script in /etc/cron.hourly with the directories I want to tag and the commands I want to run in each directory (which may differ depending on language, source/include layout, submodules etc.)
    * It might be possible to make this easier to use by using `find` to discover all `tags` files, and regenerating those with a standard command, unless an override command is configured for that particular directory.
* I've also seen suggestions about setting up Git hooks, so that tags are regenerated on each commit.

## Links

Some good resources on this topic:

* <https://vim.fandom.com/wiki/Single_tags_file_for_a_source_tree>
* <https://andrew.stwrt.ca/posts/vim-ctags/>
* <https://medium.com/@sidneyliebrand/how-fzf-and-ripgrep-improved-my-workflow-61c7ca212861>
* <https://thoughtbot.com/blog/faster-grepping-in-vim>
