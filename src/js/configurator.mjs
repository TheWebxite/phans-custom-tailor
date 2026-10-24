// Phan's suit configurator: tabs, options, live preview, summary, WhatsApp hand-off and a shareable link.
import { suitSVG, DEFAULTS } from './suit-svg.mjs';

const root = document.querySelector('[data-pct-cfg]');
const dataEl = document.getElementById('pct-cfg-data');
if (root && dataEl) {
  const data = JSON.parse(dataEl.textContent);
  const { lang, D } = data;
  const lbl = (o) => (o && (o[lang] || o.en)) || '';
  const FAB = Object.fromEntries(data.fabrics.map((f) => [f.id, { tile: `/assets/img/cfg/${f.id}.jpg`, tone: f.tone, scale: f.scale }]));
  const fabById = Object.fromEntries(data.fabrics.map((f) => [f.id, f]));
  const groups = Object.fromEntries(data.groups.map((g) => [g.key, g]));

  const fromURL = () => {
    const q = new URLSearchParams(location.search), o = {};
    for (const k of Object.keys(DEFAULTS)) {
      if (!q.has(k) || k === 'view') continue;
      const v = q.get(k);
      if (k === 'monogram') o[k] = clean(v);
      else if (k === 'fabric' ? fabById[v] : groups[k]?.options.some((x) => x.v === v)) o[k] = v;
    }
    return o;
  };
  const clean = (v) => (v || '').toUpperCase().replace(/[^A-Z]/g, '').slice(0, 3);
  const s = { ...DEFAULTS, ...fromURL() };
  const shareURL = () => {
    const q = new URLSearchParams();
    for (const [k, v] of Object.entries(s)) if (k !== 'view' && v !== DEFAULTS[k]) q.set(k, v);
    const qs = q.toString();
    return location.origin + location.pathname + (qs ? `?${qs}` : '');
  };

  const stage = root.querySelector('[data-cfg-stage]');
  const caption = root.querySelector('[data-cfg-caption]');
  const summary = root.querySelector('[data-cfg-summary]');
  const priceEl = root.querySelector('[data-cfg-price]');
  const waBtn = root.querySelector('[data-cfg-wa]');
  const mono = root.querySelector('input[data-k="monogram"]');
  if (mono) mono.value = s.monogram;
  const nf = new Intl.NumberFormat(lang === 'vi' ? 'vi-VN' : 'en-US');

  function rows() {
    const r = [[D.labels.fabric, lbl(fabById[s.fabric].name)]];
    for (const g of data.groups) r.push([lbl(g.label), lbl(g.options.find((o) => o.v === s[g.key])?.label)]);
    r.push([D.labels.monogram, s.monogram || D.monogramNone]);
    return r;
  }
  function render(changed) {
    stage.innerHTML = suitSVG(s, FAB, { label: D.title });
    caption.textContent = lbl(fabById[s.fabric].name);
    root.querySelectorAll('[data-k][data-v]').forEach((b) => {
      const on = s[b.dataset.k] === b.dataset.v;
      b.classList.toggle('is-on', on); b.setAttribute('aria-checked', String(on));
    });
    root.querySelectorAll('[data-view]').forEach((b) => {
      const on = b.dataset.view === s.view; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', String(on));
    });
    if (changed === 'fabric' || changed === 'buttons' || changed === 'init') {
      root.querySelectorAll('[data-thumb]').forEach((b) => {
        b.querySelector('.pct-cfg__thumb').innerHTML = suitSVG({ ...s, [b.dataset.k]: b.dataset.v, view: b.dataset.back ? 'back' : 'front' }, FAB, { viewBox: b.dataset.thumb, id: `t-${b.dataset.k}-${b.dataset.v}` });
      });
    }
    const r = rows();
    summary.innerHTML = r.map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('');
    const piece = s.waistcoat === 'yes' ? 'suit3' : 'suit2';
    priceEl.textContent = `${nf.format(data.prices[piece])} ${data.currency}`;
    const text = [D.waIntro, `- ${s.waistcoat === 'yes' ? D.threePiece : D.twoPiece}`, ...r.map(([k, v]) => `- ${k}: ${v}`), `${D.waLink}: ${shareURL()}`].join('\n');
    waBtn.href = `https://wa.me/${data.wa}?text=${encodeURIComponent(text)}`;
    try { history.replaceState(null, '', shareURL().replace(location.origin, '')); } catch (e) { /* file:// or sandboxed */ }
    const tryImg = root.querySelector('[data-cfg-tryimg]');
    if (tryImg && !tryImg.closest('[data-pane]').hidden) {
      const q = new URLSearchParams(); for (const k of ['fabric', 'fit', 'closure', 'lapel', 'pockets', 'breast', 'waistcoat', 'pleats', 'hem', 'buttons']) q.set(k, s[k]);
      const src = `/api/suit?${q}`;
      if (tryImg.getAttribute('src') !== src) { clearTimeout(tryImg._t); tryImg._t = setTimeout(() => tryImg.setAttribute('src', src), 400); }
    }
  }
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function go(step) {
    root.querySelectorAll('[data-step]').forEach((t) => t.setAttribute('aria-selected', String(t.dataset.step === step)));
    root.querySelectorAll('[data-pane]').forEach((p) => { p.hidden = p.dataset.pane !== step; });
    if (step === 'review') render('review');
    if (window.matchMedia('(max-width: 899px)').matches) root.querySelector('.pct-cfg__panel').scrollIntoView({ block: 'start', behavior: 'smooth' });
  }

  root.addEventListener('click', (e) => {
    const opt = e.target.closest('[data-k][data-v]');
    if (opt) {
      s[opt.dataset.k] = opt.dataset.v;
      if (opt.dataset.k === 'vents') s.view = 'back';
      else if (opt.dataset.k !== 'fabric' && opt.dataset.k !== 'lining') s.view = 'front';
      render(opt.dataset.k); return;
    }
    const v = e.target.closest('[data-view]'); if (v) { s.view = v.dataset.view; render('view'); return; }
    const t = e.target.closest('[data-step]'); if (t) { go(t.dataset.step); return; }
    const n = e.target.closest('[data-go]'); if (n) { go(n.dataset.go); return; }
    const c = e.target.closest('[data-cfg-copy]');
    if (c) {
      const done = () => { const o = c.textContent; c.textContent = c.dataset.done; setTimeout(() => { c.textContent = o; }, 1800); };
      (navigator.clipboard ? navigator.clipboard.writeText(shareURL()) : Promise.reject()).then(done, () => { prompt('', shareURL()); });
    }
  });
  root.querySelector('[role="tablist"]').addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const tabs = [...root.querySelectorAll('[data-step]')];
    const i = tabs.findIndex((x) => x.getAttribute('aria-selected') === 'true');
    const n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
    go(n.dataset.step); n.focus();
  });
  if (mono) mono.addEventListener('input', () => { const v = clean(mono.value); if (mono.value !== v) mono.value = v; s.monogram = v; render('monogram'); });
  render('init');
}
