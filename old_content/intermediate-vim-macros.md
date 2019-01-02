Title: Intermediate Vim: Macros
Date: 2016-04-24 09:58
Category: None
Author: Rob Day
Slug: intermediate-vim-macros

_(I previously posted on another Vim feature, sessions, which you can find [here](/intermediate-vim-sessions.html))._

Macros have been the bane of my life in Vim for a little while. I didn't really know what they did, so I never used them, but sometimes I'd mistype `:q` as `q` and Vim would print 'recording' at the bottom and I'd panic slightly. (If you didn't know that that 'recording' message was part of the macro feature, well, now you do!). 

So, when I decided to learn some more advanced features of Vim, macros were one of the things I picked. As it turns out, they're actually pretty easy:

- hit `q` and another character to start recording to a buffer identified by that character (I normally use `qq` for ease, but if I wanted multiple macros, I could store one with `qq`, one with `qw`, etc.)
- type the sequence of commands you want to record - starting or finishing it with commands like 0 or j (start of line/move down a line) is good, so that after your macro runs, you're ready to run it again on the next line
- type `q` again to stop recording
- now type `@` and the name of your macro buffer (e.g. `@q` if you started with `qq`, `@w` if you started with `qw`) to replay your macro
- if you want to re-run the last-used macro, `@@` does that

I recently wanted to add C++ const specifiers to a lot of function definitions, which was more fun to automate with a macro than do by hand - `qqA const<Esc>q` defined a macro that appended ' const' to the end of the current line, and I could just hit `@@` on any line where I wanted that to happen.
