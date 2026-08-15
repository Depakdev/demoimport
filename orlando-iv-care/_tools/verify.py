#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sanity checks for the generated site. Run: python3 _tools/verify.py"""

import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

errors, warnings = [], []


def rel(p):
    return os.path.relpath(p, ROOT)


class TagBalance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.problems = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.problems.append("stray </%s> at line %d" % (tag, self.getpos()[0]))
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    unclosed = [t for t, _ in self.stack[i + 1:]]
                    self.problems.append("</%s> at line %d closed over unclosed %s"
                                         % (tag, self.getpos()[0], unclosed))
                    del self.stack[i:]
                    break
            else:
                self.problems.append("unmatched </%s> at line %d" % (tag, self.getpos()[0]))


html_files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in ("_tools", ".git", "_old-delete-me")]
    for fn in sorted(filenames):
        if fn.endswith(".html"):
            html_files.append(os.path.join(dirpath, fn))

print("Checking %d HTML files\n" % len(html_files))

for path in html_files:
    name = rel(path)
    with open(path, encoding="utf-8") as f:
        src = f.read()

    # 1. no unresolved template tokens
    if "{{P}}" in src:
        errors.append("%s: unresolved {{P}} template token" % name)

    # 2. tag balance
    p = TagBalance()
    p.feed(src)
    for prob in p.problems:
        errors.append("%s: %s" % (name, prob))
    if p.stack:
        errors.append("%s: unclosed tags %s" % (name, [t for t, _ in p.stack]))

    # 3. internal links resolve
    base = os.path.dirname(path)
    for href in re.findall(r'href="([^"]+)"', src):
        if href.startswith(("http", "mailto:", "tel:", "#", "data:")):
            continue
        target = href.split("#")[0]
        if not target:
            continue
        if not os.path.exists(os.path.normpath(os.path.join(base, target))):
            errors.append("%s: broken link -> %s" % (name, href))

    # 4. images exist and have alt + dimensions
    for tag in re.findall(r"<img\b[^>]*>", src):
        m = re.search(r'src="([^"]+)"', tag)
        if m and not m.group(1).startswith("http"):
            if not os.path.exists(os.path.normpath(os.path.join(base, m.group(1)))):
                errors.append("%s: missing image -> %s" % (name, m.group(1)))
        if 'alt="' not in tag:
            errors.append("%s: <img> without alt (%s)" % (name, tag[:70]))
        if "width=" not in tag or "height=" not in tag:
            warnings.append("%s: <img> without width/height (CLS risk)" % name)
        if 'data-image-name="' not in tag:
            warnings.append("%s: <img> without data-image-name (not swappable)" % name)

    # 5. css/js referenced exist
    for src_attr in re.findall(r'<script[^>]+src="([^"]+)"', src):
        if not src_attr.startswith("http"):
            if not os.path.exists(os.path.normpath(os.path.join(base, src_attr))):
                errors.append("%s: missing script -> %s" % (name, src_attr))

    # 6. duplicate element IDs
    ids = re.findall(r'\sid="([^"]+)"', src)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        errors.append("%s: duplicate id(s) %s" % (name, sorted(dupes)))

    # 7. SEO essentials
    for pat, label in [(r"<title>[^<]{10,}</title>", "title"),
                       (r'name="description" content="[^"]{50,}"', "meta description"),
                       (r'rel="canonical"', "canonical"),
                       (r'property="og:title"', "og:title"),
                       (r'name="viewport"', "viewport")]:
        if not re.search(pat, src):
            errors.append("%s: missing %s" % (name, label))

    # 8. exactly one h1, and a main landmark
    h1s = len(re.findall(r"<h1[\s>]", src))
    if h1s != 1:
        errors.append("%s: %d <h1> tags (expected 1)" % (name, h1s))
    if '<main id="main"' not in src:
        errors.append("%s: missing <main id=\"main\">" % name)
    if 'class="skip-link"' not in src:
        errors.append("%s: missing skip link" % name)

    # 9. header bar itself must not show "How It Works" or a phone number
    #    (the slide-out mobile drawer may still contain them)
    head = src.split("</header>")[0]
    bar = re.sub(r"<nav\b.*?</nav>", "", head, flags=re.S)
    if "How It Works" in bar:
        errors.append("%s: 'How It Works' still in header bar" % name)
    if "tel:" in bar or "header__call" in bar:
        errors.append("%s: phone number still in header bar" % name)
    if "How It Works" in head:
        errors.append("%s: 'How It Works' still in nav" % name)

    # 10. accessibility spot checks
    for tag in re.findall(r'<button\b[^>]*>', src):
        pass
    if re.search(r'user-scalable=no|maximum-scale=1', src):
        errors.append("%s: viewport disables zoom" % name)

    # 11. no emoji used as UI icons
    if re.search(r"[\U0001F300-\U0001FAFF✀-➿]", src):
        warnings.append("%s: contains emoji-range characters" % name)

# --- content requirements ---------------------------------------------------
with open(os.path.join(ROOT, "services.html"), encoding="utf-8") as f:
    svc = f.read()

REQUIRED = ["Hangover", "Migraine", "Immune Boost", "Dehydration", "Fatigue",
            "Energy Boost", "NAD+", "Vitamin C", "Glutathione", "B12",
            "Amino Acid", "Antioxidant", "Recovery IV Therapy",
            "Athletic Recovery", "Beauty IV Therapy", "Skin Glow", "Weight Loss"]
cards = len(re.findall(r'class="svc-card ', svc))
if cards != 17:
    errors.append("services.html: %d service cards (expected 17)" % cards)
for r in REQUIRED:
    if r not in svc:
        errors.append("services.html: missing service '%s'" % r)

# location pages: no address / map / directions / coordinates
BANNED = [r"\bdirections\b", r"google\s*maps?", r"\biframe\b", r"latitude",
          r"longitude", r"\bcoordinates\b", r"\bstreet\b", r"\bsuite\b",
          r"\bzip\s*code\b", r"\bFL\s+3\d{4}\b", r"postalCode", r"streetAddress"]
loc_dir = os.path.join(ROOT, "locations")
loc_files = sorted(os.listdir(loc_dir))
if len([f for f in loc_files if f.endswith(".html")]) != 5:
    errors.append("locations/: expected 5 pages, found %d" % len(loc_files))
for fn in loc_files:
    with open(os.path.join(loc_dir, fn), encoding="utf-8") as f:
        s = f.read()
    for pat in BANNED:
        if re.search(pat, s, re.I):
            errors.append("locations/%s: contains banned term matching /%s/" % (fn, pat))

# no individual service pages
for fn in os.listdir(ROOT):
    if fn.endswith(".html") and fn not in {"index.html", "services.html",
                                           "locations.html", "about.html", "contact.html"}:
        errors.append("unexpected top-level page: %s" % fn)

# assets present
for asset in ["css/style.css", "js/main.js", "sitemap.xml", "robots.txt",
              "images/SOURCES.md", "images/favicon.svg", "README.md",
              "_tools/use-local-images.py"]:
    if not os.path.exists(os.path.join(ROOT, asset)):
        errors.append("missing asset: %s" % asset)


# --- mobile drawer regression checks ----------------------------------------
# The drawer (.nav) is a child of <header>. If any ancestor gains a property
# that creates a containing block for position:fixed, the drawer gets clipped
# to the header's height instead of filling the viewport. This bit us once.
with open(os.path.join(ROOT, "css/style.css"), encoding="utf-8") as f:
    css = f.read()


def css_block(selector):
    i = css.find(selector + " {")
    if i == -1:
        return ""
    return css[i:css.index("}", i)]


CB_PROPS = ["backdrop-filter", "-webkit-backdrop-filter", "filter:",
            "transform:", "perspective:", "will-change", "contain:"]
for sel in [".site-header", ".site-header__inner", "body"]:
    block = css_block(sel)
    for prop in CB_PROPS:
        if prop in block:
            errors.append("css: %s sets %s — this makes it the containing block "
                          "for the fixed-position mobile drawer and clips it"
                          % (sel, prop.rstrip(":")))

nav_block = css[css.find("  .nav {"):css.find("  .nav {") + 900] if "  .nav {" in css else ""
if "height: 100dvh" not in nav_block and "height: 100vh" not in nav_block:
    errors.append("css: mobile .nav drawer has no viewport-based height")
if "body.nav-open .site-header" not in css:
    errors.append("css: header does not outrank the mobile bar while the drawer is open")

# The scrim must sit inside <header>, in the same stacking context as .nav,
# otherwise the header's own z-index traps the drawer underneath it.
for path in html_files:
    with open(path, encoding="utf-8") as f:
        h = f.read()
    hdr = h[h.find("<header"):h.find("</header>")]
    if 'class="nav-scrim"' not in hdr:
        errors.append("%s: .nav-scrim must be inside <header> (same stacking "
                      "context as the drawer)" % rel(path))
    if hdr.find('class="nav-scrim"') > hdr.find('<nav class="nav"'):
        errors.append("%s: .nav-scrim must come before <nav> in the header" % rel(path))

# Hamburger bars must stack vertically
tog = css_block(".nav-toggle")
if "flex-direction: column" not in tog:
    errors.append("css: .nav-toggle is missing flex-direction:column "
                  "(hamburger bars render side by side)")



# --- dark-surface text contrast ---------------------------------------------
# Headings carry an explicit dark colour, so any section with a dark background
# must be listed in the :is(...) dark-text rule or its headings render
# near-black on near-black. .why was missing from that list once.
DARK_BG_TOKENS = ("--ink-900", "--ink-800", "--ink-700", "#080C0D", "#0E1416", "#162022")
# These set their own per-element colours instead of using the shared list.
EXEMPT = {".hero", ".page-hero", ".cta-band", ".site-header", ".site-footer",
          ".nav", ".mobile-bar", ".loc-card", ".nav__head", ".nav-scrim"}

dark_list = ""
for line in css.splitlines():
    if line.startswith(":is(") and "color: var(--color-text-invert)" in line and "h1" in line:
        dark_list = line
if not dark_list:
    errors.append("css: could not find the shared dark-text heading rule")

for m in re.finditer(r"^(\.[\w-]+)\s*\{([^}]*)\}", css, re.M):
    sel, block = m.group(1), m.group(2)
    if sel in EXEMPT:
        continue
    bg = re.search(r"background(-color)?:\s*([^;]+);", block)
    if not bg:
        continue
    if any(tok in bg.group(2) for tok in DARK_BG_TOKENS):
        if sel not in dark_list:
            errors.append("css: %s has a dark background but is not in the shared "
                          "dark-text rule — its headings will be near-black on "
                          "near-black" % sel)


# --- report -----------------------------------------------------------------
if warnings:
    print("WARNINGS (%d):" % len(warnings))
    for w in sorted(set(warnings)):
        print("  ⚠  " + w)
    print()

if errors:
    print("ERRORS (%d):" % len(errors))
    for e in errors:
        print("  ✗  " + e)
    sys.exit(1)

print("✓ All checks passed — %d pages, 17 services, 5 location pages." % len(html_files))
