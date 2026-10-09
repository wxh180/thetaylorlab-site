// The Taylor Lab — small progressive enhancements (site works without JS)
(function () {
  // Mobile navigation
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Lightbox for any .zoom button
  var zooms = document.querySelectorAll('.zoom');
  if (zooms.length && 'HTMLDialogElement' in window) {
    var dlg = document.createElement('dialog');
    dlg.className = 'lightbox';
    dlg.innerHTML = '<button type="button" aria-label="Close">&times;</button><img alt=""><p></p>';
    document.body.appendChild(dlg);
    var img = dlg.querySelector('img'), cap = dlg.querySelector('p');
    dlg.querySelector('button').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    zooms.forEach(function (b) {
      b.addEventListener('click', function () {
        img.src = b.getAttribute('data-full');
        img.alt = b.getAttribute('data-caption') || '';
        cap.textContent = b.getAttribute('data-caption') || '';
        dlg.showModal();
      });
    });
  }

  // Alumni tabs
  var tabs = document.querySelectorAll('.tabs [role="tab"]');
  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () { select(tab); });
    tab.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (d) { var t = tabs[(i + d + tabs.length) % tabs.length]; select(t); t.focus(); }
    });
  });
  function select(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  }

  // Gallery filter
  var chips = document.querySelectorAll('.filters .chip');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-filter');
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
      document.querySelectorAll('.shot').forEach(function (s) {
        s.hidden = !(f === 'all' || s.getAttribute('data-cat') === f);
      });
    });
  });

  // Publication search
  var q = document.getElementById('pub-search');
  if (q) {
    var items = document.querySelectorAll('.pub');
    var blocks = document.querySelectorAll('.year-block');
    var empty = document.getElementById('pub-empty');
    q.addEventListener('input', function () {
      var terms = q.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      var shown = 0;
      items.forEach(function (it) {
        var hay = it.getAttribute('data-search');
        var ok = terms.every(function (t) { return hay.indexOf(t) !== -1; });
        it.hidden = !ok; if (ok) shown++;
      });
      blocks.forEach(function (b) { b.hidden = !b.querySelector('.pub:not([hidden])'); });
      empty.hidden = shown !== 0;
    });
  }
})();
