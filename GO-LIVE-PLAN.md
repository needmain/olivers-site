# GO-LIVE PLAN — putting the London Road redesign on the live site

Reconnaissance done 2026-10-01 against `revamp-mockups` @ `6536b1e`.
Safety tag: **`revamp-mockups-approved-20261001`**.

Nothing here has been done. This is the plan, with the facts it rests on.

---

## 1. The thing to understand first

**The redesign is not in the live pages at all.** All nine production pages are
byte-for-byte identical to `main`, and so is `css/style.css`:

```
index.html about.html restaurant.html takeaway.html kids.html
catered-packages.html contact.html giftvouchers.html takeaway-menu.html
   -> all UNCHANGED vs main
```

The entire redesign lives in the `_*-london-v2.html` mockups. **Merging this
branch today would change nothing a customer sees** — it would only publish the
mockups as stray public URLs.

So going live is a real piece of work, not a merge.

---

## 2. Isolation is mostly a non-issue (better path exists)

I had assumed we'd need to strip ~26 preview files before merging. Not so:

**`main` contains only `_redirects` from the preview-pattern files — zero mockups.**

The mockups were only ever added on `revamp-mockups`. So if the production
changes are applied onto a branch cut **from `main`**, the mockups never come
along and there is nothing to strip.

> Only if `revamp-mockups` were merged into `main` wholesale would stripping be
> needed — and that path is not recommended anyway, because it would ship
> `css/_preview-scope.css`.

---

## 3. The actual mechanism: promote `_preview-scope.css` into `style.css`

This is the key. `css/_preview-scope.css` is not merely preview decoration — its
own header records that **its rules previously lived in `css/style.css`** and
were pulled out on 2026-09-12 because nine live pages load that file.

It holds:

| Section | Contents |
|---|---|
| 1 | The **new palette** — `--green`, `--navy`, `--gold`, `--cream`, and the legacy aliases repointed |
| 2 | `.logo-img`, `.brand-logo` |
| 3 | `.logo-sub`, `.nav-menu a` colour overrides |
| 4 | `.info-card .btn-outline` — the green CTA buttons |
| 5 | The **"Menus" nav dropdown**, including the deliberate `(0,3,2)` double-prefix that beats the per-page inline blocks |

**Making the new look live = moving these rules back into `css/style.css`,
deliberately, with approval.** That is what the file's own PROMOTION RULE says.

⚠️ Two cautions carried over from the file's own notes:
- Rules are deliberately **unprefixed** so the cascade order matches the original
  `style.css` edits. Adding a body-class prefix would raise specificity and
  override the per-page inline `<style>` blocks that intentionally win today.
- The dropdown needs `body.page-toggle-london .nav-menu .nav-dropdown a` at
  `(0,3,2)`. Downgrading it to `.nav-dropdown a` `(0,1,1)` silently loses to the
  nav-link padding rule.

⚠️ The file claims it is *"listed in .gitignore, so it cannot be committed or
deployed"* — but it **is tracked** (`git ls-files` lists it; it was force-added).
The .gitignore entry alone is not protection. Worth fixing.

---

## 4. Assets — three problems, all found by checking rather than assuming

Every image the nine mockups reference, and its git status:

| Image | Status |
|---|---|
| `OLIVERS OUTSIDE SIGN.jpg`, `award-hygiene.jpg`, `customer fishchipimage.jpg`, `restaurant-3.jpg`, `restaurant-4.jpg`, `sausage-icon.png`, `takeaway-1.jpg`, `takeaway-2.jpg` | ✅ already on `main` |
| `_preview-interior-light.jpg` | ⚠️ tracked, but **underscore-prefixed** — the preview convention. Used by About + Restaurant galleries. **Needs a production filename.** |
| `chipfork-wood.png` | ⚠️ tracked; referenced by all nine mockups **only** via the vestigial `<svg class="fork-defs">` block that existed for the removed location toggles. **Drop that block and the image is not needed.** |
| `olivers-bigfry-light.jpg` | ❌ **UNTRACKED** — on disk only. Used by About. **Will 404 on the live site unless git-added.** |
| `olivers-mural-light.jpg` | ❌ **UNTRACKED** — same. Used by About. |

The two untracked ones are part of the "15 untracked-and-unignored files" noted
in the handover brief. They work locally, which is exactly why this is easy to
miss.

---

## 5. Page-by-page mapping

Each mockup becomes its production page:

| Mockup | Becomes |
|---|---|
| `_toggle-london-v2.html` | `index.html` |
| `_about-london-v2.html` | `about.html` |
| `_restaurant-london-v2.html` | `restaurant.html` |
| `_takeaway-london-v2.html` | `takeaway.html` |
| `_restaurant-menu-london-v2.html` | **`restaurant-menu.html`** (new page) |
| `_takeaway-menu-london-v2.html` | `takeaway-menu.html` |
| `_kids-london-v2.html` | `kids.html` |
| `_catered-packages-london-v2.html` | `catered-packages.html` |
| `_contact-london-v2.html` | `contact.html` |

For each, the mechanical edits:

1. Rewrite internal links `_x-london-v2.html` → the production filenames.
2. **Remove the `css/_preview-scope.css` `<link>`** — its rules will now be in `style.css`.
3. **Remove the `js/_preview-hub.js` script tag** — preview-only, must not ship.
4. Drop the vestigial `<svg class="fork-defs">` block (see §4).
5. Keep the per-page inline `<style>` blocks as-is. They're proven and
   page-scoped; consolidating them into `style.css` is a bigger change and buys
   nothing at this stage.

---

## 6. Order of work

1. **Finish or revert `about.html`** — it is modified and uncommitted, with images
   pointing outside the repo (`../olivers construction.jpg`). Blocks everything.
2. **Pilot one page** on `revamp-mockups`, so the approach is proven before
   rolling to nine. Contact Us is the smallest and exercises the whole pattern.
3. **Roll the other eight.**
4. **Promote `_preview-scope.css` into `css/style.css`.**
5. **Git-add the two untracked images; rename the `_preview-` one.**
6. **Verify all nine** against the approved mockups.
7. **Joel's sign-off → merge to `main` → push.** Push to `main` is the deploy.

---

## 7. What "done" looks like

- Nine production pages render the new design.
- No page references `_preview-scope.css`, `_preview-hub.js`, or any `_*` file.
- No broken images.
- `main` fast-forwards cleanly with no preview file in the diff.
- `revamp-mockups` and the tag remain untouched as the design archive.

---

## 8. Mobile — was NOT optimised; now tested and fixed

The mockups were reviewed at desktop width only. A real sweep found three defects.

### 8.1 The mobile menu was dead (fixed)
**No mockup loaded `js/nav.js`.** The live pages do. So the hamburger was
decorative in all nine — the mockups had never actually been usable on a phone.
Added to all nine; clicking it now opens a 293px menu with 12 links.

### 8.2 Nav unreachable from 861px to ~1060px (fixed)
The desktop nav needs the pinned 130px logo *plus* nine items, and did not fit:

| Width | Before |
|---|---|
| 861px | 3 items off-screen |
| 1024px | last item off-screen |
| 1100px | fitted, 16px spare |

The header is `position: fixed`, so the overflow produced **no scrollbar** — the
items were simply unreachable. Fix: raised the desktop-nav breakpoint
861px → **1100px**, so tablets get the hamburger.

### 8.3 style.css and the pages disagreed between 769px and 1099px (fixed)
`css/style.css` switches to the hamburger at **768px**. Raising the page
breakpoint to 1100px left a gap: the page stacked the header while style.css
still laid the nav out as a desktop row. Each page now mirrors style.css's own
mobile nav rules across `769px–1099px`, at the **same specificity**
(`.nav-menu` `(0,1,0)` / `.nav-menu.active` `(0,2,0)`) so the open state still
beats the hidden one. No change to the frozen stylesheet.

> **At go-live**, the clean fix is to align `style.css`'s 768px breakpoint to
> 1100px as part of the step-4 promotion, and drop the per-page mirror.

### 8.4 Homepage hero overflowed 6px on phones (fixed)
`.hero-brand`'s 80px side padding plus the wordmark's 96px `clamp()` minimum (in
`style.css`) = 416px in a 390px viewport. Reduced to 20px on mobile. The live
homepage never had this — a redesign regression.

### 8.5 Contact email forced a 15px scroll at 320px (fixed)
`info@olivers4fish.co.uk` is one unbreakable string; it pushed the card's
min-content to 315px inside a 265px column. Added `overflow-wrap: anywhere`.

### Verified widths (all 9 pages, no horizontal overflow, nav reachable)

| Range | Nav | Result |
|---|---|---|
| 320 / 390 / 768px | hamburger | clean |
| 769 / 900 / 1099px | hamburger | clean, opens correctly |
| 1100 / 1150 / 1280 / 1440 / 1920px | desktop | fits, clears the logo |

**Not yet tested:** 480px, 600px, and real-device checks (iOS Safari, Android
Chrome) — viewport testing is not the same as a real device.