#!/usr/bin/env python3
"""Apply the user's three decisions:
  1. Option B colours on the menu page — navy section banners (B's "navy headings"),
     keeping the green frame/rules/dividers and the faded-green kids block that B
     also specifies. A/B/C differed on headings: A = green, B = navy, C = gold rules.
  2. The logo bigger — ~2/3 of the header bar, up from 30px (~1/3).
  3. The same single-part logo ("Oliver's" alone, no "Fish & Chips") on the two pages
     that still carry the old two-part version: the homepage and About Us.

The body's top offset is a magic number (see its comment) and MUST follow the header
height, so it is updated in the same pass rather than left to bite later.
"""
import re
from pathlib import Path

SITE = Path(r"C:\OLIVERS WEB\olivers-site")
LOGO = "62px"     # ~2/3 of the header bar (30px was ~1/3)
OFFSET = "128px"  # must clear the taller fixed header
PAGES = [
    "_toggle-london-v2.html",          # homepage  — has the old two-part logo
    "_about-london-v2.html",           # About Us  — has the old two-part logo
    "_restaurant-london-v2.html",
    "_restaurant-menu-london-v2.html",
]
report = []

for name in PAGES:
    p = SITE / name
    s = p.read_text(encoding="utf-8")
    before = s

    # 1. single-part logo
    s = s.replace(
        '<span class="logo-main">Oliver\'s</span><span class="logo-sub">Fish &amp; Chips</span>',
        '<span class="logo-main">Oliver\'s</span>',
    )

    # 2. logo size override — replace the existing one, or add it next to .logo
    if re.search(r"\.nav-tier-1 \.logo-main\s*\{[^}]*\}", s):
        s = re.sub(r"\.nav-tier-1 \.logo-main\s*\{[^}]*\}",
                   f".nav-tier-1 .logo-main {{ font-size: {LOGO}; }}", s)
    else:
        anchor = "body.page-toggle-london .nav-tier-1 .logo { flex-shrink: 0; }"
        assert anchor in s, f"{name}: no logo anchor to attach the override to"
        s = s.replace(anchor, anchor +
                      f"\n        /* enlarged to ~2/3 of the header bar (was 30px, ~1/3) */\n"
                      f"        body.page-toggle-london .nav-tier-1 .logo-main {{ font-size: {LOGO}; }}")

    # 3. body offset must track the header, or content hides under the fixed bar
    s, n = re.subn(r"body\.page-toggle-london\s*\{\s*padding-top:\s*\d+px;\s*\}",
                   f"body.page-toggle-london {{ padding-top: {OFFSET}; }}", s)
    assert n == 1, f"{name}: expected 1 body-offset rule, found {n}"

    p.write_text(s, encoding="utf-8", newline="")
    report.append(f"  {name:34s} logo={LOGO:5s} offset={OFFSET}"
                  f"  logo-sub removed={('logo-sub' not in s.split('</style>',1)[1])}")

# 4. Option B on the menu page: navy banners instead of green (B = navy headings),
#    leaving B's green frame, green dividers and faded-green kids block in place.
mp = SITE / "_restaurant-menu-london-v2.html"
m = mp.read_text(encoding="utf-8")
old = """.mn-sec h3 {
            background: var(--forest);"""
new = """.mn-sec h3 {
            background: var(--navy);"""
assert old in m, "menu page: could not find the green section banner rule"
m = m.replace(old, new)
assert "background: var(--navy);" in m
mp.write_text(m, encoding="utf-8", newline="")
report.append("  menu page: section banners -> NAVY (option B), green frame/dividers kept")

print("\n".join(report))