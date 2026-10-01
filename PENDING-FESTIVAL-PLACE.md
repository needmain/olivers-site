# PENDING — Festival Place reinstatement

**Status: deliberately removed, to be reinstated.** The second Oliver's site
(Festival Place / "Oliver's Too") is not yet announced, so every reference to it
has been pulled from the mockups. This file is the record of what was removed and
how to put it back.

Last updated: 2026-10-01

---

## 1. Chip-fork location toggles — REMOVED, CSS RETAINED

Removed from the header (top right) of all eight redesign pages:

`_toggle-london-v2.html`, `_about-london-v2.html`, `_restaurant-london-v2.html`, `_takeaway-london-v2.html`, `_restaurant-menu-london-v2.html`, `_takeaway-menu-london-v2.html`, `_kids-london-v2.html`, `_catered-packages-london-v2.html`

**The CSS was deliberately left in place.** Every page still carries the
`.location-switch` / `.loc-fork` rules and the `<svg class="fork-defs">` wood
pattern, so reinstating is a **markup-only** change — paste the block back and
it works.

### Where it goes

Inside `<div class="nav-tier-1">`, **after** the `<button class="nav-toggle">`
line and before the closing `</div>` of `nav-tier-1`.

### The exact block

```html
<div class="location-switch">
                                    <a href="_toggle-london-v2.html" class="loc-fork active" aria-label="London Road — current location">
                                        <svg viewBox="0 0 1122 184" aria-hidden="true">
                                            <path class="f-body" d="M279.0 0.0 L400.0 1.0 L637.0 23.0 L1052.0 10.0 L1087.0 24.0 L1115.0 58.0 L1120.0 99.0 L1104.0 138.0 L1081.0 158.0 L1057.0 166.0 L963.0 178.0 L659.0 163.0 L516.0 167.0 L350.0 183.0 L175.0 179.0 L98.0 169.0 L12.0 152.0 L0.0 144.0 L3.0 134.0 L92.0 112.0 L125.0 101.0 L138.0 89.0 L113.0 73.0 L35.0 51.0 L22.0 41.0 L28.0 32.0 L158.0 10.0 L278.0 1.0 Z"/>
                                            <path class="f-wash" d="M279.0 0.0 L400.0 1.0 L637.0 23.0 L1052.0 10.0 L1087.0 24.0 L1115.0 58.0 L1120.0 99.0 L1104.0 138.0 L1081.0 158.0 L1057.0 166.0 L963.0 178.0 L659.0 163.0 L516.0 167.0 L350.0 183.0 L175.0 179.0 L98.0 169.0 L12.0 152.0 L0.0 144.0 L3.0 134.0 L92.0 112.0 L125.0 101.0 L138.0 89.0 L113.0 73.0 L35.0 51.0 L22.0 41.0 L28.0 32.0 L158.0 10.0 L278.0 1.0 Z"/>
                                            <text class="f-label" x="578" y="115">LONDON ROAD</text>
                                        </svg>
                                    </a>
                                    <a href="_toggle-town-v2.html" class="loc-fork" aria-label="Switch to Festival Place (coming soon)">
                                        <svg viewBox="0 0 1122 184" aria-hidden="true">
                                            <path class="f-body" d="M279.0 0.0 L400.0 1.0 L637.0 23.0 L1052.0 10.0 L1087.0 24.0 L1115.0 58.0 L1120.0 99.0 L1104.0 138.0 L1081.0 158.0 L1057.0 166.0 L963.0 178.0 L659.0 163.0 L516.0 167.0 L350.0 183.0 L175.0 179.0 L98.0 169.0 L12.0 152.0 L0.0 144.0 L3.0 134.0 L92.0 112.0 L125.0 101.0 L138.0 89.0 L113.0 73.0 L35.0 51.0 L22.0 41.0 L28.0 32.0 L158.0 10.0 L278.0 1.0 Z"/>
                                            <path class="f-wash" d="M279.0 0.0 L400.0 1.0 L637.0 23.0 L1052.0 10.0 L1087.0 24.0 L1115.0 58.0 L1120.0 99.0 L1104.0 138.0 L1081.0 158.0 L1057.0 166.0 L963.0 178.0 L659.0 163.0 L516.0 167.0 L350.0 183.0 L175.0 179.0 L98.0 169.0 L12.0 152.0 L0.0 144.0 L3.0 134.0 L92.0 112.0 L125.0 101.0 L138.0 89.0 L113.0 73.0 L35.0 51.0 L22.0 41.0 L28.0 32.0 L158.0 10.0 L278.0 1.0 Z"/>
                                            <text class="f-label" x="578" y="115">FESTIVAL PLACE</text>
                                        </svg>
                                    </a>
                                </div>
```

### To reinstate

1. Paste the block above back into the position described.
2. On each page, the first badge should carry `class="loc-fork active"` for the
   page's own location (currently London Road on all eight).
3. Check `aria-label` values read sensibly — they are what screen readers
   announce, and they still said "Switch to Festival Place".
4. The nav offset (`body.page-toggle-london { padding-top: 102px; }`) assumes a
   ~96px header. **Re-measure the header height after reinstating** — the badges
   sit absolutely positioned and can change it.

---

## 2. Other Festival Place references — current state

| Where | State |
|---|---|
| Nav "Location" dropdown | **Festival Place entry removed.** The dropdown and its `aria-haspopup` trigger are intact, so it is a one-line re-add. |
| Footer address card (all 8 pages) | **Replaced.** Now reads *"Another **Oliver's** is on its way — and that's all we're saying for now!"* (with "Oliver's" in the brand script). The heading, address and the "Oliver's Too" logo were removed. |
| Homepage "Visit Us" card | **Done.** Now shows only the London Road address and the map link. The `.vu-new-inline` / `.vu-eyebrow` / `.vu-name` / `.vu-where` rules are kept so reinstating is markup-only. |
| `_toggle-town-v2.html` | The old Festival Place mockup still exists but is **pre-revamp**; nothing links to it now. |
| Live production pages | **Untouched.** All of the above is mockup-only. |

## 3. When the announcement is cleared

Reinstate in this order:

1. The chip-fork toggles (§1 above).
2. The "Location" dropdown entry — `<li><a href="_toggle-town-v2.html">Festival Place</a></li>`.
3. The footer card heading + address (and the logo, if wanted).
4. The homepage "Visit Us" card.
5. Revamp `_toggle-town-v2.html` to match the London Road design.

**Nothing here is live.** `main` is untouched; the redesign lives on the
`revamp-mockups` branch only.
