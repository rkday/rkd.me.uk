---
title: "50 short programs in Rust, #5 - symlinks"
published_date: "2020-03-14 17:52:26 +0000"
layout: default.liquid
is_draft: false
---
I can almost never remember how to create symlinks - that is, which way round the arguments to 'ln' go. So I wrote a Rust equivalent, called `symlink`, which you invoke as `symlink file-a --pointing-to file-b` - more characters, but if I don't have to look it up every time, quicker overall.

Here's the code:

```rust
use clap::{App, Arg};
use std::io::{Error, ErrorKind};
use std::os::unix::fs;
use std::path::Path;

fn main() -> std::io::Result<()> {
    let matches = App::new("symlink")
        .version("1.0")
        .author("rkd@rkd.me.uk")
        .about("'ln' replacement that's more intuitive")
        .arg(
            Arg::with_name("pointing-to")
                .short("p")
                .long("pointing-to")
                .value_name("FILE")
                .required(true)
                .help("Existing file for symlink to point to")
                .takes_value(true),
        )
        .arg(
            Arg::with_name("LINK")
                .help("Symlink file to create")
                .required(true)
                .index(1),
        )
        .get_matches();

    let symlink = Path::new(matches.value_of("LINK").unwrap());
    let pointing_to = Path::new(matches.value_of("pointing-to").unwrap());

    // Convert the source file from a relative to absolute path if necessary.
    let mut path = std::env::current_dir()?;
    let src_file = if pointing_to.is_absolute() {
        &pointing_to
    } else {
        path.push(pointing_to);
        path.as_path()
    };

    if symlink.exists() {
        Err(Error::new(
            ErrorKind::AlreadyExists,
            format!("{} already exists", symlink.display()),
        ))
    } else if !src_file.exists() {
        Err(Error::new(
            ErrorKind::NotFound,
            format!("{} does not exist", src_file.display()),
        ))
    } else {
        fs::symlink(src_file, symlink)
    }
}
```

and here it is in action:

```
$ symlink ~/.local/bin/code --pointing-to ~/.local/VSCode-linux-x64/bin/code

$ file ~/.local/bin/code
/home/rkd/.local/bin/code: symbolic link to /home/rkd/.local/VSCode-linux-x64/bin/code

$ symlink ~/.local/bin/code --pointing-to ~/.local/VSCode-linux-x64/bin/code 
Error: Custom { kind: AlreadyExists, error: "/home/rkd/.local/bin/code already exists" }

$ symlink ~/.local/bin/code3 --pointing-to /nowhere                         
Error: Custom { kind: NotFound, error: "/nowhere does not exist" }
```
