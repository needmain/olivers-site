#!/usr/bin/env python3
"""Generate _restaurant-menu-print-london-v2.html — a dedicated, print-optimised menu.

WHY A GENERATOR: the menu body (12 sections, 90 rows, 103 prices) is extracted from
_restaurant-menu-london-v2.html and only the class names are remapped. Nothing is
retyped, so the print page cannot silently disagree with the screen page about a
price. If you edit the menu page, RE-RUN `python _build-print-menu.py` (this file,
which lives in the project root) rather than hand-editing the print page — the two
must not drift.
"""
import re
from pathlib import Path

SITE = Path(r"C:\OLIVERS WEB\olivers-site")
SRC = SITE / "_restaurant-menu-london-v2.html"
OUT = SITE / "_restaurant-menu-print-london-v2.html"
OUT_PROD = SITE / "restaurant-menu-print.html"

src = SRC.read_text(encoding="utf-8")
body = src.split("</style>", 1)[1]

# --- extract the menu sections ---
# Extract the <section class="mn-sec"> blocks DIRECTLY. Slicing "from mn-wrap to the
# next mn-band" swept in everything in between — including the menu page's new
# "Printable menu" button, which then appeared on the print sheet. A mn-sec never
# contains a nested <section>, so matching to </section> is safe.
secs = re.findall(r'<section class="mn-sec.*?</section>', body, re.S)
assert len(secs) == 12, "expected 12 sections, found %d" % len(secs)
menu_html = "\n            ".join(s.strip() for s in secs)

fi = body.index('<div class="mn-fine">') + len('<div class="mn-fine">')
fj = body.index("</section>", fi)
fine_html = body[fi:fj]
fine_html = re.sub(r"</div>\s*</div>\s*$", "", fine_html).rstrip()
assert "<p" in fine_html, "fine print has no paragraphs"

# --- the address block, taken from the page FOOTER (the phrase also appears in the
#     nav's chip-fork label, so search from <footer> onwards, not from the top) ---
foot_start = body.index("<footer")
# case-insensitive: the markup says "London Road" and only LOOKS uppercase because of
# CSS. Matching the rendered case is the bug that produced an empty address.
addr = re.search(r'<h4[^>]*>London Road</h4>(.*?)(?=<h4|</div>)', body[foot_start:], re.S | re.I)
addr_html = addr.group(1) if addr else ""
addr_lines = re.findall(r"<p>(.*?)</p>", addr_html, re.S)
assert addr_lines, "no address lines found in the footer"
addr_html_out = "<br>".join(" ".join(re.sub(r"<[^>]+>", "", l).split()) for l in addr_lines)
addr_text = " / ".join(" ".join(re.sub(r"<[^>]+>", "", l).split()) for l in addr_lines)

# --- remap the screen classes to print classes (nothing else changes) ---
CLASSES = [
    ("mn-sec mn-callout", "pm-sec pm-callout"),
    ("mn-item mn-item--2", "pm-row two"),
    ("mn-item mn-item--3", "pm-row three"),
    ("mn-item", "pm-row"),
    ("mn-list", "pm-list"),
    ("mn-name", "pm-nm"),
    ("mn-desc", "pm-desc"),
    ("mn-dots", "pm-dots"),
    ("mn-price", "pm-pr"),
    ("mn-note", "pm-note"),
    ("mn-cols", "pm-cols"),
    ("mn-sec", "pm-sec"),
    ("mn-callout", "pm-callout"),
]
for a, b in CLASSES:
    menu_html = menu_html.replace(a, b)

# the screen-only column headings ("Btl") carry no print value in a single-price row
menu_html = re.sub(r'<div class="pm-cols">\s*</div>', "", menu_html)

# --- counts, so the run proves the content carried over ---
n_sec = len(re.findall(r'class="pm-sec', menu_html))
n_row = len(re.findall(r'class="pm-row', menu_html))
prices = re.findall(r'class="pm-pr">([\d.]+)<', menu_html)
fine_paras = len(re.findall(r"<p", fine_html))
assert n_sec == 12, f"expected 12 sections, extracted {n_sec}"
assert len(prices) == 103, f"expected 103 prices, extracted {len(prices)}"

CSS = """        /* Print-first stylesheet. This page's ONLY job is to come out well on paper
           (and via Save as PDF), so it is black on white with no brand chrome.
           Everything screen-only is stripped in @media print. */
        @page { size: A4; margin: 14mm 12mm; }
        * { box-sizing: border-box; }
        html, body { background: #ffffff; color: #000000; }
        body { font-family: 'Inter', sans-serif; margin: 0; padding: 24px 20px 40px; }
        .pm-wrap { max-width: 900px; margin: 0 auto; }

        .pm-bar { display: flex; align-items: flex-end; justify-content: space-between; gap: 18px;
                  padding-bottom: 12px; border-bottom: 3px solid #000000; margin-bottom: 20px; }
        .pm-bar h1 { font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 1.35rem;
                     margin: 2px 0 0; letter-spacing: 0.01em; }
        .pm-bar address { font-style: normal; font-size: 0.78rem; line-height: 1.5; text-align: right; }

        .pm-actions { text-align: center; margin: 16px 0 24px; }
        .pm-script { font-family: 'Dancing Script', cursive; font-weight: 800; font-size: 1.32em; line-height: 1; }
        .pm-btn { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 0.95rem;
                  color: #ffffff; background: #2F8C4A; border: 0; border-radius: 999px;
                  padding: 13px 32px; cursor: pointer; }
        .pm-btn:hover { background: #26713C; }
        .pm-hint { display: block; margin-top: 8px; font-size: 0.76rem; color: #555555; }

        /* the menu: two columns, as on screen.
           MULTI-COLUMN, not a grid. A grid makes every row as tall as its tallest
           block, so a short block (Early Bird) left a large gap beneath/beside it even
           after the stretch was stopped. Multi-column packs the blocks tightly down one
           column and then the next, with break-inside: avoid keeping each section whole.
           This is the same approach the screen menu page uses. */
        .pm-menu { columns: 2; column-gap: 38px; }
        .pm-sec { break-inside: avoid; page-break-inside: avoid; margin: 0 0 16px; }
        .pm-sec h3 { font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 0.8rem;
                     letter-spacing: 0.14em; text-transform: uppercase; margin: 0 0 8px;
                     padding-top: 9px; border-top: 2px solid #000000; }
        .pm-sec h4 { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 0.72rem;
                     letter-spacing: 0.12em; text-transform: uppercase; margin: 13px 0 6px;
                     padding-top: 7px; border-top: 1px solid #B8BFC6; }
        .pm-note { font-size: 0.78rem; color: #333333; margin: 0 0 8px; }
        .pm-list { display: grid; grid-template-columns: minmax(0, 1fr); }
        .pm-row { display: grid; grid-template-columns: auto 1fr auto; align-items: baseline;
                  gap: 8px; padding: 3px 0; }
        .pm-row.two { grid-template-columns: auto 1fr auto auto; }
        .pm-row.three { grid-template-columns: auto 1fr auto auto auto; }
        .pm-nm { font-size: 0.9rem; }
        .pm-desc { display: block; font-size: 0.74rem; color: #555555; }
        .pm-dots { border-bottom: 1.5px dotted #A9B0B8; transform: translateY(-3px); }
        .pm-pr { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 0.88rem;
                 min-width: 46px; text-align: right; font-variant-numeric: tabular-nums; }
        .pm-cols { display: grid; grid-auto-flow: column; justify-content: end; gap: 8px;
                   font-family: 'Montserrat', sans-serif; font-size: 0.62rem; font-weight: 700;
                   letter-spacing: 0.08em; text-transform: uppercase; color: #666666; margin-bottom: 4px; }
        .pm-cols span { width: 46px; text-align: right; }
        .pm-callout { background: #F2F7F3; border: 1px solid #BFDCC6; border-radius: 10px;
                      padding: 12px 14px; }

        .pm-fine { margin-top: 24px; border-top: 3px solid #000000; padding-top: 12px; }
        .pm-fine h3 { font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 0.78rem;
                      letter-spacing: 0.14em; text-transform: uppercase; margin: 0 0 6px; }
        .pm-fine p { font-size: 0.74rem; color: #333333; margin: 0 0 4px; line-height: 1.5; }
        .pm-foot { margin-top: 18px; font-size: 0.74rem; color: #333333; text-align: center; }

        @media print {
            body { padding: 0; }
            .pm-actions { display: none !important; }   /* the button must never print */
            .pm-menu { gap: 18px 28px; }
            .pm-callout { background: #F2F7F3 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
            a { color: #000000 !important; text-decoration: none !important; }
        }
        @media (max-width: 700px) {
            .pm-menu { grid-template-columns: 1fr; }
            .pm-bar { flex-direction: column; align-items: flex-start; }
            .pm-bar address { text-align: left; }
        }"""

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oliver's Restaurant Menu (printable) — Oliver's Fish &amp; Chips</title>
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@800&family=Montserrat:wght@700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
<!--
    Printable menu. Content is GENERATED from _restaurant-menu-london-v2.html by
    remapping class names — do not hand-edit the menu here or the two pages will
    drift apart. Edit _restaurant-menu-london-v2.html, then re-run
    `python _build-print-menu.py` (project root) to regenerate this file.
-->
<div class="pm-wrap">

    <div class="pm-bar">
        <div>
            <h1><span class="pm-script">Oliver&#39;s</span> Restaurant Menu</h1>
        </div>
        <address>{addr_html_out}</address>
    </div>

    <div class="pm-actions">
        <button type="button" class="pm-btn" onclick="window.print()">Print this menu</button>
        <span class="pm-hint">Or press Ctrl+P / Cmd+P. Save as PDF to email or download it.</span>
    </div>

    <div class="pm-menu">{menu_html}</div>

    <!-- fine_html already carries its own "Please note" heading — do not add a second -->
    <div class="pm-fine">{fine_html}</div>

    <p class="pm-foot">Oliver's Fish &amp; Chips — London Road — prices include VAT</p>
</div>
</body>
</html>
"""

OUT.write_text(PAGE, encoding="utf-8", newline="")
OUT_PROD.write_text(PAGE, encoding="utf-8", newline="")
print(f"wrote {OUT.name} and {OUT_PROD.name}: {len(PAGE)} chars")
print(f"  sections: {n_sec}   rows: {n_row}   prices: {len(prices)}   fine-print paragraphs: {fine_paras}")
print(f"  address carried from the footer: {' '.join(addr_html.split())[:120]}")
print(f"  first price extracted: {prices[0]}   last: {prices[-1]}")