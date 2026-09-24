#!/usr/bin/env python3
"""Move the logo ONTO the nav row, at its far left — beside "Home", not on the strip
above the tabs.

How: the header is two tiers — .nav-tier-1 (logo + location toggles) sits above the
<nav-menu> row. `display: contents` dissolves the tier's own box so its children (the
logo, the toggles) become direct children of .nav-container, which we then lay out as
a single ROW with flex `order`: logo (1st, hard left) -> nav tabs (2nd) -> location
toggles (3rd, pushed right with margin-left:auto).

Scoped to the desktop breakpoint (>860px) so the mobile hamburger layout is untouched.

The header gets SHORTER (one row instead of two), so the body's top offset must come
down with it or a gap appears above the content. Set conservatively here and confirmed
by measurement immediately after.
"""
import re
from pathlib import Path

SITE = Path(r"C:\OLIVERS WEB\olivers-site")
PAGES = ["_toggle-london-v2.html", "_about-london-v2.html",
         "_restaurant-london-v2.html", "_restaurant-menu-london-v2.html"]
OFFSET = "84px"   # one row (~74px) + a small cushion; measured straight after

LOGO_ROW_CSS = """        /* ---- Logo ON the nav row ----
           The logo used to sit on the strip ABOVE the tabs. `display: contents`
           dissolves that tier's box so the logo and the location toggles join the nav
           container directly, which is then laid out as one row: logo hard left, tabs
           next to it, toggles pushed right by margin-left:auto. Desktop only, so the
           mobile hamburger bar keeps its own layout. */
        @media (min-width: 861px) {
            body.page-toggle-london .nav-container {
                flex-direction: row;
                align-items: center;
                justify-content: flex-start;
                gap: 30px;
            }
            body.page-toggle-london .nav-tier-1 { display: contents; }
            body.page-toggle-london .nav-tier-1 .logo { order: 1; margin-left: 0; }
            body.page-toggle-london .nav-menu { order: 2; margin-left: 0; }
            body.page-toggle-london .location-switch { order: 3; margin-left: auto; }
        }

"""

for name in PAGES:
    p = SITE / name
    s = p.read_text(encoding="utf-8")
    css = re.findall(r"<style>(.*?)</style>", s, re.S)[0]

    # the logo no longer needs the -28px pull: display:contents + order puts it left
    s = re.sub(r"\n\s*margin-left: -28px;[^\n]*", "", s)
    assert "margin-left: -28px" not in s, f"{name}: -28px pull not removed"

    anchor = "        body.page-toggle-london .nav-tier-1 .logo-main { font-size: 62px; }"
    assert anchor in s, f"{name}: logo anchor missing"
    s = s.replace(anchor, LOGO_ROW_CSS + anchor)

    s, n = re.subn(r"body\.page-toggle-london\s*\{\s*padding-top:\s*\d+px;\s*\}",
                   f"body.page-toggle-london {{ padding-top: {OFFSET}; }}", s)
    assert n == 1, f"{name}: expected 1 body-offset rule, found {n}"

    p.write_text(s, encoding="utf-8", newline="")
    print(f"  {name:34s} logo -> nav row (desktop), offset {OFFSET}")