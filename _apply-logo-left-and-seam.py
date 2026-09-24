#!/usr/bin/env python3
"""1. Pull the logo toward the bar's left corner (user: "further to left corner").
   The nav container is centred with max-width 1160px, so at ~1249px wide its own left
   edge sits ~45px in. A negative margin on the logo (kept in flex flow, so the
   location toggles stay pinned right via space-between) lands it near the corner.

2. THE SEAM FIX, STRUCTURAL. Two rounds of margin games on .rst-wave did not work:
   the rects kept reporting the band's navy edge coincident with the wave's fill edge,
   so a partial device-pixel row could still blend navy into white.
   Instead, make the section BELOW the wave paint OPAQUE WHITE and overlap the band's
   last few pixels. An opaque white neighbour means that boundary row can only ever
   blend white with white — the navy has nothing left to leak through. The band's own
   trailing pixels are already covered by the wave's white fill, so nothing visible
   changes.
"""
import re
from pathlib import Path

SITE = Path(r"C:\OLIVERS WEB\olivers-site")
PAGES = ["_toggle-london-v2.html", "_about-london-v2.html",
         "_restaurant-london-v2.html", "_restaurant-menu-london-v2.html"]
PULL = "-28px"

# --- 1. logo toward the left corner, on all four pages ---
for name in PAGES:
    p = SITE / name
    s = p.read_text(encoding="utf-8")
    old = "body.page-toggle-london .nav-tier-1 .logo { flex-shrink: 0; }"
    new = ("body.page-toggle-london .nav-tier-1 .logo {\n"
           "            flex-shrink: 0;\n"
           f"            margin-left: {PULL};   /* hug the bar's left corner (container is centred) */\n"
           "        }")
    assert old in s, f"{name}: logo rule not found"
    s = s.replace(old, new)
    assert f"margin-left: {PULL};" in s
    p.write_text(s, encoding="utf-8", newline="")
    print(f"  {name:34s} logo pulled {PULL} toward the left corner")

# --- 2. the seam fix, on the restaurant page (where the wave lives) ---
rp = SITE / "_restaurant-london-v2.html"
r = rp.read_text(encoding="utf-8")
anchor = "        /* the fine-print block matches the framed look */"
assert anchor in r, "restaurant page: no anchor for the seam rules"
seam = """        /* ---- Seam fix (structural) ----
           Margins alone did not fix the hairline: the band's navy edge stayed coincident
           with the wave's fill edge, so a partial device-pixel row could blend navy into
           white. This makes the NEXT section paint OPAQUE WHITE and overlap the band's
           last 4px, so that boundary row can only blend white with white. The band's
           trailing pixels are already hidden under the wave's white fill, so nothing
           visible moves — the navy simply has nowhere left to show through. */
        section.rst-section#menu {
            position: relative;
            z-index: 1;
            background: #ffffff;
            margin-top: -4px;
        }

"""
r = r.replace(anchor, seam + anchor)
assert "section.rst-section#menu" in r
rp.write_text(r, encoding="utf-8", newline="")
print(f"  {'_restaurant-london-v2.html':34s} seam fix applied (opaque white neighbour overlaps the band)")