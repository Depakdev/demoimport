#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Switch the site from hot-linked Unsplash photos to your own local files.

The site currently loads its photography from Unsplash's CDN so it looks
finished out of the box. When you have your own photos:

  1. Put them in /images using the filenames listed in images/SOURCES.md
     (e.g. images/hero-iv-therapy.jpg)
  2. Run:   python3 _tools/use-local-images.py

Every <img> is rewritten to point at images/<filename>. Images you haven't
supplied yet keep their Unsplash URL, so the site never breaks mid-swap.

Run with --revert to put the Unsplash URLs back.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, "images")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import PHOTOS  # noqa: E402  (filename -> unsplash photo id)


def pages():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ("_tools", ".git")]
        out += [os.path.join(dirpath, f) for f in filenames if f.endswith(".html")]
    return sorted(out)


def unsplash_url(name, w, h):
    return ("https://images.unsplash.com/%s?auto=format&fit=crop&w=%s&h=%s&q=80"
            % (PHOTOS[name], w, h))


def run(revert=False):
    changed_files = 0
    swapped = 0
    skipped = set()

    for path in pages():
        with open(path, encoding="utf-8") as f:
            src = f.read()
        original = src
        depth = os.path.relpath(path, ROOT).count(os.sep)
        prefix = "../" * depth

        for tag in re.findall(r"<img\b[^>]*>", src):
            m = re.search(r'data-image-name="([^"]+)"', tag)
            if not m:
                continue
            name = m.group(1)
            local = prefix + "images/" + name
            has_local = os.path.exists(os.path.join(IMAGES, name))
            w = re.search(r'width="(\d+)"', tag)
            h = re.search(r'height="(\d+)"', tag)

            if revert:
                if name not in PHOTOS:
                    continue
                new_src = unsplash_url(name, w.group(1) if w else 1600, h.group(1) if h else 900)
            else:
                if not has_local:
                    skipped.add(name)
                    continue
                new_src = local

            new_tag = re.sub(r'src="[^"]*"', 'src="%s"' % new_src, tag, count=1)
            if new_tag != tag:
                src = src.replace(tag, new_tag)
                swapped += 1

        if src != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(src)
            changed_files += 1

    verb = "reverted to Unsplash" if revert else "switched to /images"
    print("%d <img> tags %s across %d files." % (swapped, verb, changed_files))
    if skipped:
        print("\nStill using Unsplash (no local file found in /images):")
        for n in sorted(skipped):
            print("   " + n)
        print("\nAdd those files to /images and run this again.")


if __name__ == "__main__":
    run(revert="--revert" in sys.argv)
