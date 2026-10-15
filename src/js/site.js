/* Phan's Custom Tailor — site behaviour. Vanilla JS, no dependencies.
   Everything works without this file; it only adds menus, filters, form handling and tracking. */
(function () {
  'use strict';
  var root = document.body;
  if (!root || root.hasAttribute('data-pct-ready')) return;
  root.setAttribute('data-pct-ready', '');
  root.classList.add('pct-js');
  window.dataLayer = window.dataLayer || [];
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function track(event, data) {
    var o = { event: event };
    for (var k in data) if (data[k]) o[k] = data[k];
    window.dataLayer.push(o);
  }
  function $(sel, ctx) { return (ctx || root).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || root).querySelectorAll(sel)); }

  /* ---------- Tracking on links and buttons ---------- */
  root.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-pct-track]') : null;
    if (!el) return;
    track(el.getAttribute('data-pct-track'), {
      where: el.getAttribute('data-pct-where'),
      product: el.getAttribute('data-pct-product-name'),
      to: el.getAttribute('data-pct-to'),
      page: location.pathname
    });
  });

  /* ---------- Full-screen menu (works without JS through #pct-menu:target) ---------- */
  var menu = $('[data-pct-menu]');
  var menuBtn = $('[data-pct-menu-open]');
  var lastFocus = null;
  function menuOpen() { return !!menu && menu.classList.contains('pct-is-open'); }
  function setMenu(open) {
    if (!menu || open === menuOpen()) return;
    if (open) {
      lastFocus = document.activeElement;
      $$('img[data-src]', menu).forEach(function (im) { im.src = im.getAttribute('data-src'); im.removeAttribute('data-src'); });
    }
    menu.classList.toggle('pct-is-open', open);
    root.classList.toggle('pct-menu-open', open);
    document.documentElement.classList.toggle('pct-menu-open', open);
    if (menuBtn) menuBtn.setAttribute('aria-expanded', String(open));
    root.dispatchEvent(new CustomEvent('pct:menu', { detail: { open: open } }));
    if (open) {
      var current = $('.pct-menu__list a[aria-current]', menu) || $('.pct-menu__list a', menu);
      setTimeout(function () { if (current) current.focus({ preventScroll: true }); }, 60);
      track('menu_open', { page: location.pathname });
    } else if (lastFocus && lastFocus.focus) {
      lastFocus.focus({ preventScroll: true });
    }
  }
  if (menu) {
    if (location.hash === '#pct-menu') history.replaceState(null, '', location.pathname + location.search);
    if (menuBtn) menuBtn.addEventListener('click', function (e) { e.preventDefault(); setMenu(true); });
    $$('[data-pct-menu-close]', menu).forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); setMenu(false); }); });
    // Hovered item swaps the preview photo
    var previews = $$('[data-pct-menu-img]', menu);
    $$('[data-pct-menu-item]', menu).forEach(function (a) {
      var show = function () {
        var i = a.getAttribute('data-pct-menu-item');
        previews.forEach(function (im) { im.classList.toggle('pct-is-active', im.getAttribute('data-pct-menu-img') === i); });
      };
      a.addEventListener('mouseenter', show);
      a.addEventListener('focus', show);
    });
    // Keep keyboard focus inside the open menu
    menu.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var f = $$('a[href], button', menu).filter(function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    });
  }

  /* ---------- Home hero: hovering a section link shows its photo ---------- */
  var heroEl = $('[data-pct-hero]');
  if (heroEl) {
    var slides = $$('.pct-hero__slide', heroEl);
    var loadSlides = function () { slides.forEach(function (im) { var src = im.getAttribute('data-src'); if (src) { im.src = src; im.removeAttribute('data-src'); } }); };
    if (document.readyState === 'complete') setTimeout(loadSlides, 600); else window.addEventListener('load', function () { setTimeout(loadSlides, 600); });
    var setSlide = function (n) {
      slides.forEach(function (im, i) { im.classList.toggle('pct-is-active', String(i) === String(n)); });
      heroEl.setAttribute('data-pct-active-slide', n);
      root.dispatchEvent(new CustomEvent('pct:hero-slide', { detail: { index: Number(n) } }));
    };
    var resetTimer = null;
    $$('[data-pct-slide-link]', heroEl).forEach(function (a) {
      var go = function () { clearTimeout(resetTimer); loadSlides(); setSlide(a.getAttribute('data-pct-slide-link')); };
      a.addEventListener('mouseenter', go);
      a.addEventListener('focus', go);
    });
    var links = $('.pct-hero__links', heroEl);
    if (links) {
      links.addEventListener('mouseleave', function () { resetTimer = setTimeout(function () { setSlide(0); }, 450); });
      links.addEventListener('focusout', function (e) { if (!links.contains(e.relatedTarget)) setSlide(0); });
    }
  }

  /* ---------- Language menu ---------- */
  var lang = $('[data-pct-lang]');
  if (lang) {
    var langBtn = $('.pct-lang__btn', lang);
    langBtn.addEventListener('click', function () {
      var open = langBtn.getAttribute('aria-expanded') !== 'true';
      langBtn.setAttribute('aria-expanded', String(open));
      lang.classList.toggle('pct-is-open', open);
    });
    document.addEventListener('click', function (e) {
      if (!lang.contains(e.target)) { langBtn.setAttribute('aria-expanded', 'false'); lang.classList.remove('pct-is-open'); }
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (lang && lang.classList.contains('pct-is-open')) { lang.classList.remove('pct-is-open'); $('.pct-lang__btn', lang).setAttribute('aria-expanded', 'false'); $('.pct-lang__btn', lang).focus(); }
    if (menuOpen()) setMenu(false);
    closeFilters();
  });

  /* ---------- Floating buttons hide while a form is on screen ---------- */
  var floats = $$('[data-pct-float]');
  var forms = $$('form[data-pct-form]');
  if (floats.length && forms.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      var visible = entries.some(function (en) { return en.isIntersecting; });
      floats.forEach(function (f) { f.classList.toggle('pct-is-hidden-float', visible); });
    }, { threshold: 0.05 });
    forms.forEach(function (f) { io.observe(f); });
  }

  /* ---------- YouTube: load the player only on click ---------- */
  $$('[data-pct-video]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var id = a.getAttribute('data-pct-video');
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      f.title = 'YouTube video';
      f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen = true;
      var wrap = document.createElement('div');
      wrap.className = 'pct-video';
      wrap.appendChild(f);
      a.replaceWith(wrap);
      f.focus();
      track('video_play', { video: id });
    });
  });

  /* ---------- Add to bag (proposal: checkout not connected yet) ---------- */
  $$('[data-pct-bag]').forEach(function (btn) {
    if (btn.getAttribute('data-pct-live') === 'true') return;
    var msg = btn.parentNode.querySelector('[data-pct-bag-msg]');
    btn.addEventListener('click', function () { if (msg) msg.hidden = false; });
  });

  /* ---------- Shop filters, sort, URL state ---------- */
  var shop = $('[data-pct-shop]');
  var filters = $('[data-pct-filters]');
  var openBtn = $('[data-pct-filters-open]');
  function closeFilters() {
    if (!filters || !filters.classList.contains('pct-is-open')) return;
    filters.classList.remove('pct-is-open');
    if (openBtn) { openBtn.setAttribute('aria-expanded', 'false'); openBtn.focus(); }
  }
  if (shop && filters) {
    var list = $('[data-pct-products]', shop);
    var cards = $$('[data-pct-product]', list);
    var count = $('[data-pct-count]', shop);
    var empty = $('[data-pct-empty]', shop);
    var sort = $('[data-pct-sort]', shop);
    var params = new URLSearchParams(location.search);
    ['cat', 'colour', 'price'].forEach(function (name) {
      var v = params.get(name) || '';
      var input = filters.querySelector('input[name="' + name + '"][value="' + (window.CSS && CSS.escape ? CSS.escape(v) : v) + '"]');
      if (input) input.checked = true;
    });
    if (params.get('sort')) sort.value = params.get('sort');

    var apply = function (push) {
      var fd = new FormData(filters);
      var cat = fd.get('cat') || '', colour = fd.get('colour') || '', price = fd.get('price') || '', s = sort.value;
      var range = price ? price.split('-') : null;
      var shown = 0;
      cards.forEach(function (c) {
        var p = Number(c.getAttribute('data-price')) || 0;
        var ok = (!cat || c.getAttribute('data-cat') === cat) &&
          (!colour || c.getAttribute('data-colour') === colour) &&
          (!range || (p > 0 && p >= Number(range[0] || 0) && (!range[1] || p < Number(range[1]))));
        c.hidden = !ok;
        if (ok) shown++;
      });
      var sorted = cards.slice().sort(function (a, b) {
        if (s === 'price-asc' || s === 'price-desc') {
          var pa = Number(a.getAttribute('data-price')) || Infinity, pb = Number(b.getAttribute('data-price')) || Infinity;
          return s === 'price-asc' ? pa - pb : (pb === Infinity ? -1 : pa === Infinity ? 1 : pb - pa);
        }
        if (s === 'newest') return (b.getAttribute('data-date') || '').localeCompare(a.getAttribute('data-date') || '');
        return Number(a.getAttribute('data-index')) - Number(b.getAttribute('data-index'));
      });
      sorted.forEach(function (c) { list.appendChild(c); });
      count.textContent = count.getAttribute('data-template').replace('{n}', shown);
      empty.hidden = shown > 0;
      if (push !== false) {
        var q = new URLSearchParams();
        if (cat) q.set('cat', cat); if (colour) q.set('colour', colour); if (price) q.set('price', price); if (s && s !== 'featured') q.set('sort', s);
        var qs = q.toString();
        history.replaceState(null, '', location.pathname + (qs ? '?' + qs : ''));
        track('shop_filter', { cat: cat, colour: colour, price: price, sort: s });
      }
    };
    filters.addEventListener('change', function () { apply(); });
    sort.addEventListener('change', function () { apply(); });
    filters.addEventListener('reset', function () { setTimeout(function () { sort.value = 'featured'; apply(); }, 0); });
    filters.addEventListener('submit', function (e) { e.preventDefault(); });
    apply(false);
    if (openBtn) openBtn.addEventListener('click', function () {
      filters.classList.add('pct-is-open');
      openBtn.setAttribute('aria-expanded', 'true');
      var first = filters.querySelector('input:checked') || filters.querySelector('input');
      if (first) first.focus();
    });
    $$('[data-pct-filters-close]', filters).forEach(function (b) { b.addEventListener('click', closeFilters); });
  }

  /* ---------- Enquiry form ---------- */
  forms.forEach(function (form) {
    var status = $('[data-pct-status]', form);
    var submit = form.querySelector('button[type="submit"]');
    function setError(input, msg) {
      var err = document.getElementById(input.id + '-err');
      input.setAttribute('aria-invalid', msg ? 'true' : 'false');
      if (err) { err.textContent = msg || ''; err.hidden = !msg; }
    }
    function check(input) {
      var v = input.value.trim();
      if (input.name === 'name' || input.name === 'message') return v ? '' : input.getAttribute('data-err');
      if (input.name === 'email') return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : input.getAttribute('data-err');
      if (input.name === 'phone') return !v || (/^[+\d\s().-]+$/.test(v) && v.replace(/\D/g, '').length >= 8) ? '' : input.getAttribute('data-err');
      if (input.name === 'leave') {
        var arrive = form.elements.arrive.value;
        return !v || !arrive || v >= arrive ? '' : input.getAttribute('data-err');
      }
      return '';
    }
    var fields = ['name', 'email', 'phone', 'leave', 'message'].map(function (n) { return form.elements[n]; }).filter(Boolean);
    fields.forEach(function (input) {
      input.addEventListener('blur', function () { if (input.value || input.getAttribute('aria-invalid') === 'true') setError(input, check(input)); });
      input.addEventListener('input', function () { if (input.getAttribute('aria-invalid') === 'true') setError(input, check(input)); });
    });
    if (form.elements.arrive) form.elements.arrive.addEventListener('change', function () {
      form.elements.leave.min = form.elements.arrive.value;
      if (form.elements.leave.value) setError(form.elements.leave, check(form.elements.leave));
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstBad = null;
      fields.forEach(function (input) { var m = check(input); setError(input, m); if (m && !firstBad) firstBad = input; });
      if (firstBad) { firstBad.focus(); return; }
      if (form.elements._honey && form.elements._honey.value) return;
      var data = new FormData(form);
      var garments = data.getAll('garments');
      data.delete('garments');
      if (garments.length) data.set('garments', garments.join(', '));
      var label = submit.textContent;
      submit.disabled = true;
      submit.textContent = form.getAttribute('data-sending');
      status.textContent = '';
      fetch(form.getAttribute('data-ajax'), { method: 'POST', headers: { Accept: 'application/json' }, body: data })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (res) {
          if (res && (res.success === false || res.success === 'false')) throw new Error('rejected');
          track('form_submit', { garments: garments.join(', ') || 'none' });
          location.href = form.getAttribute('data-thanks');
        })
        .catch(function () {
          submit.disabled = false;
          submit.textContent = label;
          status.innerHTML = '<p class="pct-error"></p>';
          status.firstChild.textContent = form.getAttribute('data-err-send');
        });
    });
  });

  /* ---------- Smooth scroll for in-page links ---------- */
  root.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a || a.getAttribute('href').length < 2) return;
    var target = document.getElementById(a.getAttribute('href').slice(1));
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    if (target.id === 'pct-main') target.focus({ preventScroll: true });
    history.replaceState(null, '', '#' + target.id);
  });
})();
