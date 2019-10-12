---
title: "50 short programs in Rust, #2"
published_date: "2019-10-12 20:11:29 +0000"
layout: default.liquid
tags: ["50 short programs in Rust"]
is_draft: false
---
I use XFCE4 as my main window manager, and I like its flexibility/customisability. I recently found out about `xfce4-genmon-plugin`, which is a "generic monitor" - it runs any command on a configurable interval and includes the output on the XFCE panel. By having that command return XMl, it can even do quite flexible things with tooltips and images (see <https://goodies.xfce.org/projects/panel-plugins/xfce4-genmon-plugin#usage>).

While most desktops include something that displays total CPU/RAM/etc. usage in the panel, I find it useful to also see what program is the heaviest user of each. Here's a Rust program (using [rust-psutil](https://github.com/borntyping/rust-psutil)) which runs for two seconds and prints out the program which used most CPU over those two seconds and had the highest memory usage at the end, and can then be hooked into `xfce4-genmon-plugin`:

```rust
use std::collections::HashMap;

fn main() {
    let mut original_times = HashMap::new();

    for prog in psutil::process::all().expect("Could not get all processes the first time") {
        original_times.insert(prog.pid, prog.utime + prog.stime);
    }

    std::thread::sleep(std::time::Duration::new(2,0));

    let mut busiest_process = (String::new(), 0.0);
    let mut most_ram = (String::new(), 0);

    for prog in psutil::process::all().expect("Could not get all processes the second time") {
        let rss = prog.memory().expect(&format!("Could not get memory for {}", prog.comm)).resident;
        if rss > most_ram.1 {
            most_ram = (prog.comm.clone(), rss);
        }
        if original_times.contains_key(&prog.pid) {
            let secs_passed = (prog.utime + prog.stime) - original_times[&prog.pid];
            if secs_passed > busiest_process.1 {
                busiest_process = (prog.comm, secs_passed);
            }

        }
        original_times.insert(prog.pid, prog.utime + prog.stime);
    }

    if busiest_process.0 == most_ram.0 {
        println!("{}: {:.1}%, {} MiB", busiest_process.0, (busiest_process.1/2.0)*100.0, most_ram.1/(1024*1024));
    } else {
        println!("{}: {:.1}% / {}: {} MiB", busiest_process.0, (busiest_process.1/2.0)*100.0, most_ram.0, most_ram.1/(1024*1024));
    }
}
```

It would be nice if:

- it also printed out the heaviest user of disk I/O - this information is in `/proc/[pid]/io`, so it's just a matter of enhancing `rust-psutil` to retrieve it.
- `psutil::process::all()` (or some variant) always returned a best-effort list of processes, instead of failing if a process exited in the brief period between it seeing the `/proc/[pid]/` directory and successfully reading all the files in it.

(Code also at <https://github.com/rkday/50-short-programs-in-rust/tree/master/hungriest-program>.)
