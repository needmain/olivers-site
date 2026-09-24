/* ============================================================================
   _preview-hub.js — PREVIEW-ONLY "back to hub" button.

   Injects a fixed button that returns to _preview-index.html from any mockup
   page. Loaded by the local preview pages ONLY; no production page references
   it and it is listed in .gitignore.

   Why a script rather than markup: the alternative is pasting the same anchor
   (plus its styles) into every mockup page. This keeps it in ONE place, so the
   label/look can change without touching 22 files.

   Self-guarding: idempotent (won't double-inject), and does nothing on the hub
   itself or if the document has no <body>.
   ============================================================================ */
(function () {
    'use strict';

    if (window.__previewHubBtn) { return; }          // already injected
    window.__previewHubBtn = true;

    if (!document.body) { return; }                   // nothing to append to
    if (/_preview-index\.html/.test(location.pathname)) { return; }  // don't show it on the hub

    var style = document.createElement('style');
    style.textContent = [
        '#preview-hub-btn{',
        'position:fixed;right:20px;bottom:20px;z-index:9999;',
        "font-family:'Montserrat',system-ui,-apple-system,'Segoe UI',sans-serif;",
        'font-weight:700;font-size:0.78rem;letter-spacing:0.05em;text-transform:uppercase;',
        'color:#fff;background:#0B1B2B;text-decoration:none;',
        'padding:12px 18px;border-radius:999px;',
        'border:2px solid #E0A96D;',
        'box-shadow:0 6px 22px rgba(11,27,43,0.32);',
        'transition:background .2s ease,transform .2s ease,box-shadow .2s ease;',
        'white-space:nowrap;line-height:1;',
        '}',
        '#preview-hub-btn:hover,#preview-hub-btn:focus-visible{',
        'background:#2F8C4A;transform:translateY(-2px);',
        'box-shadow:0 10px 26px rgba(11,27,43,0.4);outline:none;',
        '}',
        '#preview-hub-btn .arrow{margin-right:7px;}',
        '@media print{#preview-hub-btn{display:none;}}',
        '@media (max-width:640px){#preview-hub-btn{right:12px;bottom:12px;padding:10px 14px;font-size:0.72rem;}}'
    ].join('');
    document.head.appendChild(style);

    var a = document.createElement('a');
    a.id = 'preview-hub-btn';
    a.href = '_preview-index.html';
    a.title = 'Back to all mockup pages';
    a.setAttribute('aria-label', 'Back to all mockup preview pages');

    var arrow = document.createElement('span');
    arrow.className = 'arrow';
    arrow.textContent = '\u2190';
    a.appendChild(arrow);
    a.appendChild(document.createTextNode('All mockups'));

    document.body.appendChild(a);
})();
