#!/usr/bin/env python3
import sys

oldfile = sys.argv[1]
newfile = sys.argv[2]

inheaders = True

conversions = {
        'Title:': 'title:',
        'Summary:': 'excerpt:',
        'Slug:': 'slug:',
        }

with open(oldfile) as oldf:
    with open(newfile, "w") as newf:
        newf.write("---\n")
        newf.write("layout: default.liquid\n")
        for l in oldf.readlines():
            if inheaders:
                newversion = None
                for old, new in conversions.items():
                    if l.startswith(old):
                        newversion = l.replace(old, new)
                if newversion:
                    l = newversion
                elif l.startswith("Date:"):
                    l = l.replace("Date:", "published_date:")
                    l = l[:-1] + ":00 +0100\n"
                elif l == "\n":
                    l = "---\n\n"
                    inheaders = False
                else:
                    continue
            newf.write(l)
