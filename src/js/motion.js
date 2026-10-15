/* Phan's Custom Tailor — motion layer (GSAP + ScrollTrigger + SplitText, three.js loaded on demand).
   Content is fully visible without this file. The inline script in <body> adds .pct-anim only when the visitor
   has not asked for reduced motion; a 4s safety timer reveals everything if this file never runs. */
(function () {
  'use strict';
  var body = document.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !window.gsap || !window.ScrollTrigger || !body.classList.contains('pct-anim')) {
    body.classList.add('pct-anim-done');
    return;
  }
  var gsap = window.gsap;
  gsap.registerPlugin(window.ScrollTrigger);
  var hasSplit = !!window.SplitText;
  if (hasSplit) gsap.registerPlugin(window.SplitText);
  var ScrollTrigger = window.ScrollTrigger;
  var lang = body.getAttribute('data-pct-lang-code');
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var EXPO = 'expo.out';
  gsap.defaults({ ease: 'power3.out', duration: 1 });

  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function onEnter(el, start) { return { trigger: el, start: start || 'top 86%', toggleActions: 'play none none none' }; }

  /* ---------- Text: reveal by lines (falls back to a rise for Chinese) ---------- */
  function revealLines(el, opts) {
    if (!el) return null;
    opts = opts || {};
    if (!hasSplit || lang === 'zh') {
      return gsap.fromTo(el, { autoAlpha: 0, y: 34 }, { autoAlpha: 1, y: 0, duration: opts.duration || 1.2, ease: EXPO, delay: opts.delay || 0, scrollTrigger: opts.trigger });
    }
    var split = window.SplitText.create(el, { type: 'lines', mask: 'lines', linesClass: 'pct-line' });
    gsap.set(el, { autoAlpha: 1 });
    return gsap.fromTo(split.lines, { yPercent: 115 }, {
      yPercent: 0, duration: opts.duration || 1.25, ease: EXPO, stagger: opts.stagger || 0.1, delay: opts.delay || 0, scrollTrigger: opts.trigger,
      onComplete: function () { split.revert(); }
    });
  }
  function rise(els, opts) {
    opts = opts || {};
    if (!els || (els.length === 0)) return null;
    return gsap.fromTo(els, { autoAlpha: 0, y: opts.y == null ? 28 : opts.y }, {
      autoAlpha: 1, y: 0, duration: opts.duration || 1.1, ease: EXPO, stagger: opts.stagger || 0.08, delay: opts.delay || 0, scrollTrigger: opts.trigger
    });
  }

  /* Above-the-fold entrances start at once (they hold the largest paint); splits are reverted when done */
  /* ---------- Header: drop in, hide on scroll down, return on scroll up ---------- */
  var header = $('[data-pct-header]');
  if (header) {
    gsap.fromTo(header.querySelector('.pct-header__bar'), { autoAlpha: 0, y: -18 }, { autoAlpha: 1, y: 0, duration: 1, delay: 0.2, ease: EXPO });
    var shown = true;
    ScrollTrigger.create({
      start: 0, end: 'max',
      onUpdate: function (self) {
        if (body.classList.contains('pct-menu-open')) return;
        var hide = self.direction === 1 && self.scroll() > 320;
        if (hide === !shown) return;
        shown = !hide;
        gsap.to(header, { yPercent: hide ? -100 : 0, duration: 0.5, ease: 'power3.out', overwrite: true });
      }
    });
  }

  /* ---------- Home hero: photo settles, section links rise one by one ---------- */
  var hero = $('.pct-hero');
  if (hero) {
    var media = $('.pct-hero__media', hero);
    var tl = gsap.timeline({ delay: 0.1 });
    tl.fromTo(media, { scale: 1.12, clipPath: 'inset(6% 4% 6% 4%)' }, { scale: 1, clipPath: 'inset(0% 0% 0% 0%)', duration: 1.8, ease: 'expo.inOut' }, 0);
    tl.fromTo($('.pct-hero__label', hero), { autoAlpha: 0, y: 12 }, { autoAlpha: 1, y: 0, duration: 1, ease: EXPO }, 0.9);
    tl.fromTo($$('.pct-hero__links a span', hero), { yPercent: 110, autoAlpha: 1 }, { yPercent: 0, autoAlpha: 1, duration: 1.1, ease: EXPO, stagger: 0.07 }, 1.0);
    tl.fromTo($('.pct-hero__note', hero), { autoAlpha: 0 }, { autoAlpha: 1, duration: 1 }, 1.5);
    // Scroll: links drift up and fade, photo sinks
    gsap.to($('.pct-hero__inner', hero), { yPercent: -18, opacity: 0.1, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to(media, { yPercent: 12, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
  }

  /* ---------- Full-screen menu: panel wipes down, items rise in, rules draw ---------- */
  var menuEl = $('[data-pct-menu]');
  if (menuEl) {
    var menuTl = null;
    body.addEventListener('pct:menu', function (e) {
      if (menuTl) menuTl.kill();
      if (!e.detail.open) { gsap.set(menuEl, { clearProps: 'clipPath' }); return; }
      menuTl = gsap.timeline();
      menuTl.fromTo(menuEl, { clipPath: 'inset(0% 0% 100% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.75, ease: 'expo.inOut' }, 0)
        .fromTo($$('.pct-menu__label', menuEl), { yPercent: 105 }, { yPercent: 0, duration: 0.9, ease: EXPO, stagger: 0.05 }, 0.35)
        .fromTo($$('.pct-menu__num', menuEl), { autoAlpha: 0, x: -10 }, { autoAlpha: 1, x: 0, duration: 0.6, stagger: 0.05 }, 0.45)
        .fromTo($$('.pct-menu__list li', menuEl), { '--pct-rule': 0 }, { '--pct-rule': 1, duration: 0.9, ease: 'power3.inOut', stagger: 0.04 }, 0.3)
        .fromTo($('.pct-menu__preview', menuEl), { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'expo.inOut' }, 0.4)
        .fromTo($$('.pct-menu__foot > *, .pct-menu__top > *', menuEl), { autoAlpha: 0, y: 16 }, { autoAlpha: 1, y: 0, duration: 0.8, stagger: 0.08 }, 0.55);
    });
  }

  /* ---------- Inner page heads and article heads ---------- */
  $$('.pct-page-head, .pct-article__head').forEach(function (head) {
    var t = gsap.timeline({ delay: 0 });
    var crumbs = $('.pct-crumbs', head);
    if (crumbs) t.fromTo(crumbs, { autoAlpha: 0, y: 10 }, { autoAlpha: 1, y: 0, duration: 0.8, ease: EXPO }, 0);
    var k = $('.pct-kicker', head);
    if (k) t.fromTo(k, { autoAlpha: 0, y: 12 }, { autoAlpha: 1, y: 0, duration: 0.9, ease: EXPO }, 0.1);
    var h1 = $('.pct-h1', head);
    if (h1) {
      gsap.set(h1, { autoAlpha: 1 });
      var r = revealLines($('.pct-h1__text', head) || h1, { duration: 0.95, stagger: 0.07 });
      if (r) t.add(r, 0.05);
    }
    var rest = $$('.pct-lead, .pct-page-head__aside, .pct-article__meta', head);
    if (rest.length) t.fromTo(rest, { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 1, ease: EXPO, stagger: 0.08 }, 0.35);
  });

  /* Split text only after the web fonts are in, so lines break where they will finally sit (max 0.7s wait) */
  var fontsReady = document.fonts && document.fonts.ready ? Promise.race([document.fonts.ready, new Promise(function (r) { setTimeout(r, 700); })]) : Promise.resolve();
  fontsReady.then(run);

  function run() {
  /* ---------- Section headings, leads ---------- */
  $$('main .pct-h2').forEach(function (h) {
    if (h.closest('.pct-page-head, .pct-hero, .pct-post-lead, .pct-pdp')) return;
    revealLines(h, { trigger: onEnter(h) });
  });
  $$('main .pct-lead, main .pct-section-head > div, main .pct-steps-foot, main .pct-intro__text .pct-link').forEach(function (el) {
    if (el.closest('.pct-page-head, .pct-hero, .pct-article__head')) return;
    rise(el, { trigger: onEnter(el), delay: 0.15 });
  });

  /* ---------- Images: curtain reveal + gentle zoom, parallax on large ones ---------- */
  var parallaxSel = '.pct-intro__figure, .pct-grid-2 > [class*="pct-col-"] > .pct-figure, .pct-longstep .pct-figure, .pct-article__cover .pct-figure';
  $$('main .pct-figure').forEach(function (fig) {
    if (fig.closest('.pct-post-card, .pct-product-card, .pct-pdp__gallery')) return;
    var img = $('img', fig);
    if (!img) return;
    var para = fig.matches(parallaxSel) || !!fig.closest('.pct-intro__figure');
    gsap.set(fig, { overflow: 'hidden' });
    gsap.fromTo(fig, { clipPath: 'inset(18% 0% 18% 0%)', autoAlpha: 0 }, { clipPath: 'inset(0% 0% 0% 0%)', autoAlpha: 1, duration: 1.5, ease: 'expo.inOut', scrollTrigger: onEnter(fig, 'top 88%') });
    gsap.fromTo(img, { scale: para ? 1.4 : 1.25 }, { scale: para ? 1.14 : 1, duration: 1.9, ease: EXPO, scrollTrigger: onEnter(fig, 'top 88%') });
    if (para) gsap.fromTo(img, { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: fig, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  $$('main .pct-band').forEach(function (band) {
    var img = $('img', band);
    if (!img || band.hasAttribute('data-pct-gl')) return;
    gsap.set(img, { scale: 1.18 });
    gsap.fromTo(img, { yPercent: -7 }, { yPercent: 7, ease: 'none', scrollTrigger: { trigger: band, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* ---------- Rules that draw themselves ---------- */
  $$('.pct-steps, .pct-pricelist, .pct-mills, .pct-trip, .pct-contact-grid, .pct-trio > div, .pct-quote--lead, .pct-pdp__attrs').forEach(function (el) {
    el.classList.add('pct-draw');
    gsap.fromTo(el, { '--pct-rule': 0 }, { '--pct-rule': 1, duration: 1.6, ease: 'power3.inOut', scrollTrigger: onEnter(el, 'top 90%') });
  });

  /* ---------- Lists and grids: staggered rise ---------- */
  var groups = [
    ['.pct-steps', '.pct-step'], ['.pct-longsteps', '.pct-longstep'], ['.pct-values', '.pct-value'], ['.pct-mills', '.pct-mill'],
    ['.pct-trio', '.pct-trio > div'], ['.pct-trip', '.pct-trip > div'], ['.pct-checklist', 'li'], ['.pct-contact-grid', '.pct-contact-grid > div'],
    ['.pct-quotes-side', '.pct-quote'], ['.pct-faq', '.pct-faq-group'], ['.pct-reviews__foot', '.pct-reviews__foot > *'],
    ['.pct-bookband__grid', '.pct-bookband__grid > *'], ['.pct-visit', '.pct-visit dl > div, .pct-map'], ['.pct-form', '.pct-field, .pct-form__foot'],
    ['.pct-footer__grid', '.pct-footer__grid > div']
  ];
  groups.forEach(function (g) {
    $$(g[0]).forEach(function (wrap) {
      var items = $$(g[1], wrap.parentNode).filter(function (i) { return wrap.contains(i); });
      if (items.length) rise(items, { trigger: onEnter(wrap, 'top 85%'), stagger: 0.09, y: 36 });
    });
  });
  $$('.pct-longstep__num').forEach(function (n) {
    gsap.fromTo(n, { xPercent: -30, autoAlpha: 0 }, { xPercent: 0, autoAlpha: 1, duration: 1.2, ease: EXPO, scrollTrigger: onEnter(n) });
  });
  // Cards arrive in batches as they scroll in
  if ($('.pct-post-card, .pct-product-card')) {
  gsap.set('.pct-post-card, .pct-product-card', { autoAlpha: 0, y: 60 });
  ScrollTrigger.batch('.pct-post-card, .pct-product-card', {
    start: 'top 92%',
    onEnter: function (batch) { gsap.to(batch, { autoAlpha: 1, y: 0, duration: 1.2, ease: EXPO, stagger: 0.1, overwrite: true }); }
  });
  }

  /* ---------- Price list: rows slide in, numbers count up ---------- */
  $$('.pct-pricelist').forEach(function (list) {
    var rows = $$('.pct-pricelist__row', list);
    gsap.fromTo(rows, { autoAlpha: 0, x: 40 }, { autoAlpha: 1, x: 0, duration: 1.1, ease: EXPO, stagger: 0.08, scrollTrigger: onEnter(list) });
    $$('.pct-pricelist__price', list).forEach(function (el) {
      var tn = Array.prototype.find.call(el.childNodes, function (n) { return n.nodeType === 3 && /\d/.test(n.nodeValue); });
      if (!tn) return;
      var orig = tn.nodeValue;
      var m = orig.match(/\d[\d.,]*\d/);
      if (!m) return;
      var target = Number(m[0].replace(/[.,]/g, ''));
      var sep = /\d\.\d/.test(m[0]) ? '.' : ',';
      var o = { v: 0 };
      var fmt = function (v) { return String(v).replace(/\B(?=(\d{3})+(?!\d))/g, sep); };
      tn.nodeValue = orig.replace(m[0], '0');
      gsap.to(o, {
        v: target, duration: 1.8, ease: 'power3.out', scrollTrigger: onEnter(list),
        onUpdate: function () { tn.nodeValue = orig.replace(m[0], fmt(Math.round(o.v / 1000) * 1000)); },
        onComplete: function () { tn.nodeValue = orig; }
      });
    });
  });

  /* ---------- Mill names: endless marquee that speeds up with scroll ---------- */
  var mills = $('.pct-millnames');
  if (mills) {
    var inner = mills.innerHTML;
    var copies = '';
    for (var i = 0; i < 6; i++) copies += '<span class="pct-marquee__set"' + (i ? ' aria-hidden="true"' : '') + '>' + inner + '</span>';
    mills.innerHTML = '<span class="pct-marquee__track">' + copies + '</span>';
    mills.classList.add('pct-marquee');
    var loop = gsap.to($('.pct-marquee__track', mills), { xPercent: -50, ease: 'none', duration: 40, repeat: -1 });
    var settle = null;
    ScrollTrigger.create({
      trigger: mills, start: 'top bottom', end: 'bottom top',
      onUpdate: function (self) {
        var v = self.getVelocity();
        var boost = Math.min(Math.abs(v) / 250, 8);
        gsap.to(loop, { timeScale: (v < 0 ? -1 : 1) * (1 + boost), duration: 0.25, overwrite: true });
        if (settle) settle.kill();
        settle = gsap.to(loop, { timeScale: v < 0 ? -1 : 1, duration: 1.4, delay: 0.25, ease: 'power2.out' });
      }
    });
  }

  /* ---------- Reviews: the lead quote lights up word by word as you scroll ---------- */
  var leadQuote = $('.pct-quote--lead blockquote p');
  if (leadQuote && hasSplit) {
    var words = window.SplitText.create(leadQuote, { type: 'words' }).words;
    gsap.fromTo(words, { opacity: 0.14 }, { opacity: 1, ease: 'none', stagger: 0.12, scrollTrigger: { trigger: leadQuote, start: 'top 82%', end: 'bottom 48%', scrub: 0.6 } });
  }

  /* ---------- Journal lead + product page ---------- */
  var postLead = $('.pct-post-lead');
  if (postLead) rise($$(':scope > *', postLead), { stagger: 0.15, delay: 0.5, y: 40 });
  var pdp = $('.pct-pdp');
  if (pdp) {
    gsap.fromTo($$('.pct-pdp__gallery img', pdp), { autoAlpha: 0, scale: 1.08 }, { autoAlpha: 1, scale: 1, duration: 1.6, ease: EXPO, stagger: 0.1 });
    rise($$('.pct-pdp__info > *', pdp), { stagger: 0.07, delay: 0.25 });
  }
  var rte = $('.pct-rte');
  if (rte) $$(':scope > h2, :scope > h3, :scope > ul, :scope > ol, :scope > .pct-table-scroll, :scope > blockquote', rte).forEach(function (el) { rise(el, { trigger: onEnter(el, 'top 90%'), y: 24 }); });

  /* ---------- Footer logo ---------- */
  var flogo = $('.pct-footer .pct-logo');
  if (flogo) gsap.fromTo(flogo, { autoAlpha: 0, y: 30, letterSpacing: 0 }, { autoAlpha: 1, y: 0, duration: 1.4, ease: EXPO, scrollTrigger: onEnter(flogo, 'top 95%') });

  /* ---------- Pointer niceties (mouse only) ---------- */
  if (fine) {
    // Magnetic buttons
    $$('.pct-btn, .pct-wa-float, .pct-footer__social a, .pct-lang__btn').forEach(function (el) {
      if (el.closest('.pct-bottom-bar, .pct-drawer')) return;
      var xTo = gsap.quickTo(el, 'x', { duration: 0.5, ease: 'power3.out' });
      var yTo = gsap.quickTo(el, 'y', { duration: 0.5, ease: 'power3.out' });
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        xTo((e.clientX - r.left - r.width / 2) * 0.28);
        yTo((e.clientY - r.top - r.height / 2) * 0.38);
      });
      el.addEventListener('pointerleave', function () {
        gsap.to(el, { x: 0, y: 0, duration: 0.9, ease: 'elastic.out(1, 0.45)', overwrite: true });
      });
    });

    // Cursor follower with labels over cards and photos
    var cursor = document.createElement('div');
    cursor.className = 'pct-cursor';
    cursor.setAttribute('aria-hidden', 'true');
    cursor.innerHTML = '<span class="pct-cursor__label"></span>';
    body.appendChild(cursor);
    var label = cursor.firstChild;
    var cx = gsap.quickTo(cursor, 'x', { duration: 0.45, ease: 'power3.out' });
    var cy = gsap.quickTo(cursor, 'y', { duration: 0.45, ease: 'power3.out' });
    var labels = { view: body.getAttribute('data-pct-cursor-view') || 'View', read: body.getAttribute('data-pct-cursor-read') || 'Read' };
    window.addEventListener('pointermove', function (e) {
      cx(e.clientX); cy(e.clientY);
      if (!cursor.classList.contains('pct-is-on')) cursor.classList.add('pct-is-on');
    }, { passive: true });
    document.addEventListener('pointerleave', function () { cursor.classList.remove('pct-is-on'); });
    document.addEventListener('pointerover', function (e) {
      var t = e.target.closest ? e.target : null;
      if (!t) return;
      var card = t.closest('[data-pct-cursor]');
      var link = t.closest('a, button, summary, label, select, input, textarea');
      cursor.classList.toggle('pct-is-label', !!card);
      cursor.classList.toggle('pct-is-link', !card && !!link);
      if (card) label.textContent = labels[card.getAttribute('data-pct-cursor')] || '';
    });
  }

  /* ---------- Page transitions between internal pages ---------- */
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || a.target === '_blank' || a.hasAttribute('download')) return;
    var url = new URL(a.href, location.href);
    if (url.origin !== location.origin || (url.pathname === location.pathname && url.hash)) return;
    if (url.pathname === location.pathname && url.search === location.search) return;
    e.preventDefault();
    var curtain = document.createElement('div');
    curtain.className = 'pct-curtain';
    curtain.setAttribute('aria-hidden', 'true');
    body.appendChild(curtain);
    try { sessionStorage.setItem('pct-transition', '1'); } catch (err) { /* private mode */ }
    gsap.fromTo(curtain, { yPercent: 100 }, { yPercent: 0, duration: 0.55, ease: 'power3.inOut', onComplete: function () { location.href = url.href; } });
  });
  window.addEventListener('pageshow', function (e) { if (e.persisted) $$('.pct-curtain').forEach(function (c) { c.remove(); }); });

  /* ---------- WebGL: living cloth on the hero photo and the fabric band ---------- */
  function initGL() {
    var nodes = $$('[data-pct-gl]');
    if (!nodes.length) return;
    if (navigator.connection && navigator.connection.saveData) return;
    var test = document.createElement('canvas');
    if (!(test.getContext('webgl2') || test.getContext('webgl'))) return;
    import(body.getAttribute('data-pct-three')).then(function (THREE) {
      nodes.forEach(function (n) { makeScene(THREE, n); });
    }).catch(function () { /* stay with the photos */ });
  }

  var RIPPLE_V = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }';
  var SWAP_F = [
    'precision highp float;',
    'uniform sampler2D uTex; uniform sampler2D uTex2; uniform vec2 uRes; uniform vec2 uImg; uniform vec2 uImg2; uniform vec2 uMouse;',
    'uniform float uHover; uniform float uTime; uniform float uScroll; uniform float uMix;',
    'varying vec2 vUv;',
    'vec2 cover(vec2 uv, vec2 img){ float rs = uRes.x / uRes.y; float ri = img.x / img.y; vec2 o = uv - 0.5; if (rs > ri) { o.y *= ri / rs; } else { o.x *= rs / ri; } o.y += 0.08 * (1.0 - min(rs / ri, 1.0)); return o + 0.5; }',
    'void main(){',
    '  vec2 uv = vUv;',
    '  uv.x += sin(uv.y * 5.0 + uTime * 0.5) * 0.0025;',
    '  uv.y += sin(uv.x * 4.0 + uTime * 0.4) * 0.002;',
    '  vec2 asp = vec2(uRes.x / uRes.y, 1.0);',
    '  vec2 d = (vUv - uMouse) * asp; float dist = length(d);',
    '  float wave = sin(dist * 30.0 - uTime * 4.0) * exp(-dist * 6.0) * 0.012 * uHover;',
    '  if (dist > 0.0001) uv += normalize(d) / asp * wave;',
    // the transition: a soft diagonal front sweeps across, folding the cloth as it passes
    '  float front = uMix * 1.6 - 0.3;',
    '  float pos = vUv.x * 0.75 + (1.0 - vUv.y) * 0.25 + sin(vUv.y * 9.0 + uTime) * 0.03;',
    '  float t = smoothstep(front - 0.18, front + 0.18, pos);',
    '  float fold = sin(clamp((pos - front) / 0.36 + 0.5, 0.0, 1.0) * 3.14159) * sin(uMix * 3.14159);',
    '  vec2 off = vec2(0.0, fold * 0.06);',
    '  float z = 1.04 + uScroll * 0.12;',
    '  vec2 a = (cover(uv + off, uImg) - 0.5) / (z + fold * 0.05) + 0.5;',
    '  vec2 b = (cover(uv - off, uImg2) - 0.5) / (z + (1.0 - uMix) * 0.08) + 0.5;',
    '  vec3 colA = texture2D(uTex, a).rgb; vec3 colB = texture2D(uTex2, b).rgb;',
    '  vec3 col = mix(colB, colA, t);',
    '  col *= 1.0 - fold * 0.25;',
    '  gl_FragColor = vec4(col, 1.0);',
    '}'
  ].join('\n');
  var RIPPLE_F = [
    'precision highp float;',
    'uniform sampler2D uTex; uniform vec2 uRes; uniform vec2 uImg; uniform vec2 uMouse; uniform float uHover; uniform float uTime; uniform float uScroll;',
    'varying vec2 vUv;',
    'vec2 cover(vec2 uv){ float rs = uRes.x / uRes.y; float ri = uImg.x / uImg.y; vec2 o = uv - 0.5; if (rs > ri) { o.y *= ri / rs; } else { o.x *= rs / ri; } return o + 0.5; }',
    'void main(){',
    '  vec2 uv = vUv;',
    '  uv.x += sin(uv.y * 5.0 + uTime * 0.55) * 0.0035 + sin(uv.y * 11.0 - uTime * 0.8) * 0.0015;',
    '  uv.y += sin(uv.x * 4.0 + uTime * 0.45) * 0.003;',
    '  vec2 asp = vec2(uRes.x / uRes.y, 1.0);',
    '  vec2 d = (vUv - uMouse) * asp; float dist = length(d);',
    '  float wave = sin(dist * 34.0 - uTime * 4.5) * exp(-dist * 5.5) * 0.016 * uHover;',
    '  if (dist > 0.0001) uv += normalize(d) / asp * wave;',
    '  vec2 c = cover(uv); c = (c - 0.5) / (1.06 + uScroll * 0.14) + 0.5;',
    '  vec3 col = texture2D(uTex, c).rgb;',
    '  col += 0.05 * uHover * exp(-dist * 4.0);',
    '  gl_FragColor = vec4(col, 1.0);',
    '}'
  ].join('\n');
  var CLOTH_V = [
    'uniform float uTime; uniform vec2 uMouse; uniform float uHover; uniform float uScroll; uniform vec2 uRes; uniform vec2 uView;',
    'varying vec2 vUv; varying float vShade;',
    'float h(vec2 p){',
    '  float t = uTime;',
    '  float z = sin(p.x * 2.1 + t * 0.85) * 0.085 + sin(p.x * 1.05 - p.y * 1.6 + t * 0.6) * 0.07 + sin(p.x * 5.2 + p.y * 3.0 + t * 1.5) * 0.014;',
    '  z *= 0.75 + uScroll * 0.9;',
    '  vec2 m = (uMouse - 0.5) * uView; float dd = distance(p, m);',
    '  z += exp(-dd * dd * 5.0) * 0.24 * uHover;',
    '  return z;',
    '}',
    'void main(){',
    '  vUv = uv;',
    '  vec2 p = position.xy * uRes;',
    '  float z = h(p); float e = 0.02;',
    '  vec3 n = normalize(vec3(-(h(p + vec2(e, 0.0)) - z) / e, -(h(p + vec2(0.0, e)) - z) / e, 1.0));',
    '  vShade = dot(n, normalize(vec3(-0.45, 0.55, 1.0)));',
    '  gl_Position = projectionMatrix * modelViewMatrix * vec4(p, z, 1.0);',
    '}'
  ].join('\n');
  var CLOTH_F = [
    'precision highp float;',
    'uniform sampler2D uTex; uniform vec2 uRes; uniform vec2 uImg;',
    'varying vec2 vUv; varying float vShade;',
    'void main(){',
    '  float rs = uRes.x / uRes.y; float ri = uImg.x / uImg.y; vec2 o = vUv - 0.5;',
    '  if (rs > ri) { o.y *= ri / rs; } else { o.x *= rs / ri; }',
    '  vec3 c = texture2D(uTex, o + 0.5).rgb;',
    '  float l = 0.5 + vShade * 0.6;',
    '  gl_FragColor = vec4(c * l, 1.0);',
    '}'
  ].join('\n');

  function makeScene(THREE, node) {
    var mode = node.getAttribute('data-pct-gl');
    var big = node.clientWidth * Math.min(window.devicePixelRatio || 1, 2) > 1500;
    var src = (big && node.getAttribute('data-pct-gl-src-lg')) || node.getAttribute('data-pct-gl-src');
    var renderer;
    try { renderer = new THREE.WebGLRenderer({ antialias: mode === 'cloth', alpha: false, powerPreference: 'high-performance' }); } catch (err) { return; }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    var canvas = renderer.domElement;
    canvas.className = 'pct-gl';
    canvas.setAttribute('aria-hidden', 'true');
    var scene = new THREE.Scene();
    var u = {
      uTex: { value: null }, uRes: { value: new THREE.Vector2(1, 1) }, uImg: { value: new THREE.Vector2(1, 1) }, uView: { value: new THREE.Vector2(1, 1) },
      uMouse: { value: new THREE.Vector2(0.5, 0.5) }, uHover: { value: 0 }, uTime: { value: 0 }, uScroll: { value: 0 },
      uTex2: { value: null }, uImg2: { value: new THREE.Vector2(1, 1) }, uMix: { value: 0 }
    };
    var camera, geo, mat;
    if (mode === 'ripple' || mode === 'swap') {
      camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
      geo = new THREE.PlaneGeometry(2, 2);
      mat = new THREE.ShaderMaterial({ uniforms: u, vertexShader: RIPPLE_V, fragmentShader: mode === 'swap' ? SWAP_F : RIPPLE_F });
    } else {
      camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
      camera.position.z = 5;
      geo = new THREE.PlaneGeometry(1, 1, 180, 64);
      mat = new THREE.ShaderMaterial({ uniforms: u, vertexShader: CLOTH_V, fragmentShader: CLOTH_F });
    }
    scene.add(new THREE.Mesh(geo, mat));

    function resize() {
      var w = node.clientWidth, h = node.clientHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false);
      if (mode !== 'cloth') {
        u.uRes.value.set(w, h);
      } else {
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        var vh = 2 * camera.position.z * Math.tan((camera.fov * Math.PI / 180) / 2);
        var vw = vh * camera.aspect;
        u.uView.value.set(vw, vh);
        u.uRes.value.set(vw * 1.08, vh * 1.22);
      }
    }
    var running = false, visible = false, last = 0;
    var mouse = { x: 0.5, y: 0.5, tx: 0.5, ty: 0.5, h: 0, th: 0 };
    function tick(time) {
      var dt = Math.min(0.05, last ? time - last : 0.016);
      last = time;
      u.uTime.value += dt;
      mouse.x += (mouse.tx - mouse.x) * 0.08;
      mouse.y += (mouse.ty - mouse.y) * 0.08;
      mouse.th *= 0.965;
      mouse.h += (mouse.th - mouse.h) * 0.08;
      u.uMouse.value.set(mouse.x, mouse.y);
      u.uHover.value = mouse.h;
      renderer.render(scene, camera);
    }
    function play() { if (!running && visible && u.uTex.value) { running = true; last = 0; gsap.ticker.add(tick); } }
    function pause() { if (running) { running = false; gsap.ticker.remove(tick); } }

    var area = node.closest('section') || node.parentNode;
    area.addEventListener('pointermove', function (e) {
      var r = node.getBoundingClientRect();
      mouse.tx = (e.clientX - r.left) / r.width;
      mouse.ty = 1 - (e.clientY - r.top) / r.height;
      mouse.th = 1;
    }, { passive: true });

    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      if (visible) play(); else pause();
    }, { rootMargin: '100px' }).observe(node);
    if (window.ResizeObserver) new ResizeObserver(resize).observe(node); else window.addEventListener('resize', resize);
    ScrollTrigger.create({
      trigger: node, start: mode === 'cloth' ? 'top bottom' : 'top top', end: 'bottom top',
      onUpdate: function (self) { u.uScroll.value = self.progress; }
    });

    new THREE.TextureLoader().load(src, function (tex) {
      tex.minFilter = THREE.LinearFilter;
      tex.generateMipmaps = false;
      u.uTex.value = tex;
      u.uImg.value.set(tex.image.width, tex.image.height);
      node.appendChild(canvas);
      resize();
      renderer.render(scene, camera);
      u.uTex2.value = tex;
      u.uImg2.value.copy(u.uImg.value);
      gsap.fromTo(canvas, { opacity: 0 }, { opacity: 1, duration: 1.2, ease: 'power2.out', onComplete: function () { node.classList.add('pct-gl-on'); } });
      play();
      if (mode === 'swap') setupSwap(THREE, node, u);
    });
  }

  // Hero: hovering a section link folds the current photo into that section's photo
  function setupSwap(THREE, node, u) {
    var loader = new THREE.TextureLoader();
    var cache = {};
    var base = { tex: u.uTex.value, img: u.uImg.value.clone() };
    var urls = { 0: null };
    $$('[data-pct-slide-link]').forEach(function (a) { urls[a.getAttribute('data-pct-slide-link')] = a.getAttribute('data-pct-gl-img'); });
    var current = 0, tween = null, want = 0;
    function get(i, cb) {
      if (i === 0) return cb(base);
      if (cache[i]) return cb(cache[i]);
      loader.load(urls[i], function (tex) {
        tex.minFilter = THREE.LinearFilter; tex.generateMipmaps = false;
        cache[i] = { tex: tex, img: new THREE.Vector2(tex.image.width, tex.image.height) };
        cb(cache[i]);
      });
    }
    function go(i) {
      want = i;
      if (i === current && !tween) return;
      get(i, function (next) {
        if (want !== i) return;
        if (tween) { tween.kill(); u.uTex.value = u.uTex2.value; u.uImg.value.copy(u.uImg2.value); }
        // uTex = outgoing, uTex2 = incoming; uMix runs 0 -> 1
        u.uTex2.value = next.tex; u.uImg2.value.copy(next.img); u.uMix.value = 0;
        tween = gsap.to(u.uMix, { value: 1, duration: 1.05, ease: 'power2.inOut', onComplete: function () {
          u.uTex.value = next.tex; u.uImg.value.copy(next.img); u.uMix.value = 0; tween = null; current = i;
        } });
        current = i;
      });
    }
    body.addEventListener('pct:hero-slide', function (e) { go(e.detail.index || 0); });
    // preload the section photos once the hero is idle
    setTimeout(function () { Object.keys(urls).forEach(function (k) { if (k !== '0') get(Number(k), function () {}); }); }, 1500);
  }

  if (document.readyState === 'complete') setTimeout(initGL, 200);
  else window.addEventListener('load', function () { setTimeout(initGL, 200); });

  body.classList.add('pct-anim-done');
  if (document.readyState === 'complete') ScrollTrigger.refresh();
  else window.addEventListener('load', function () { ScrollTrigger.refresh(); });
  }
})();
