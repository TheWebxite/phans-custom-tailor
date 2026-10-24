// Phan's Custom Tailor — static site builder.
// Usage: node build.mjs            (proposal build, noindex)
//        INDEXABLE=true node build.mjs   (launch build: indexable, robots.txt and sitemap.xml)
// Reads src/, writes dist/. No dependencies beyond Node 18.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { suitSVG, DEFAULTS as CFG_DEFAULTS } from './src/js/suit-svg.mjs';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.join(ROOT, 'src');
const DIST = path.join(ROOT, 'dist');
const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(SRC, p), 'utf8'));

const config = readJSON('config.json');
if (process.env.INDEXABLE) config.indexable = process.env.INDEXABLE === 'true';
const LANGS = config.languages;
const I18N = Object.fromEntries(LANGS.map((l) => [l, readJSON(`i18n/${l}.json`)]));
const IMAGES = readJSON('data/images.json');
const PRICES = readJSON('data/prices.json');
const REVIEWS = readJSON('data/reviews.json');
const CFG = readJSON('data/configurator.json');
const CFG_FAB = Object.fromEntries(CFG.fabrics.map((f) => [f.id, { tile: `/assets/img/cfg/${f.id}.jpg`, tone: f.tone, scale: f.scale }]));
const LOGO_SVG = fs.readFileSync(path.join(SRC, 'brand/logo.svg'), 'utf8')
  .replace('<svg ', '<svg aria-hidden="true" focusable="false" fill="currentColor" ');
const JOURNAL = fs.readdirSync(path.join(SRC, 'data/journal')).filter((f) => f.endsWith('.json'))
  .map((f) => readJSON(`data/journal/${f}`)).sort((a, b) => b.date.localeCompare(a.date));

// ---------------------------------------------------------------------------
// Shop data: WooCommerce Store API when configured, sample JSON otherwise.
// ---------------------------------------------------------------------------
const SAMPLE = readJSON('data/products.sample.json');
async function loadProducts() {
  if (!config.shop.storeApiBase) return SAMPLE.products;
  const url = `${config.shop.storeApiBase.replace(/\/$/, '')}/wp-json/wc/store/v1/products?per_page=100`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Store API ${res.status} at ${url}`);
  return (await res.json()).map((p) => ({ ...p, date_created: p.date_created || '', sample: false }));
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const seoTitle = (t) => (`${t} | Phan's Custom Tailor`.length <= 60 ? `${t} | Phan's Custom Tailor` : `${t} | Phan's`.length <= 60 ? `${t} | Phan's` : t);
const esc = (s = '') => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const get = (obj, key) => key.split('.').reduce((o, k) => (o == null ? o : o[k]), obj);
const fill = (s, vars) => String(s).replace(/\{(\w+)\}/g, (_, k) => (vars[k] ?? `{${k}}`));
const SLUGS = I18N.en.pages; // slugs are shared by every language

function pathFor(lang, slug = '') {
  const prefix = lang === 'en' ? '' : `/${lang}`;
  return `${prefix}/${slug ? slug.replace(/^\/|\/$/g, '') + '/' : ''}`;
}
const pagePath = (lang, key) => pathFor(lang, SLUGS[key].slug);
const abs = (p) => config.siteUrl.replace(/\/$/, '') + p;

function fmtPrice(n, lang) {
  const num = Number(n);
  if (lang === 'vi') return num.toLocaleString('de-DE') + ' ₫';
  if (lang === 'zh') return num.toLocaleString('en-US') + ' 越南盾';
  return num.toLocaleString('en-US') + ' VND';
}
const MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
function fmtDate(iso, lang) {
  const [y, m, d] = iso.split('-').map(Number);
  if (lang === 'vi') return `${String(d).padStart(2, '0')}/${String(m).padStart(2, '0')}/${y}`;
  if (lang === 'zh') return `${y}年${m}月${d}日`;
  return `${d} ${MONTHS_EN[m - 1]} ${y}`;
}
function fmtMonth(ym, lang) {
  const [y, m] = ym.split('-').map(Number);
  if (lang === 'vi') return `Tháng ${m}/${y}`;
  if (lang === 'zh') return `${y}年${m}月`;
  return `${MONTHS_EN[m - 1]} ${y}`;
}
const AUTHORS = {
  thinh: { en: 'Thinh Phan', vi: 'Phan Thịnh', zh: 'Thinh Phan' },
  thuong: { en: 'Thuong Phan', vi: 'Phan Thương', zh: 'Thuong Phan' },
  team: { en: "Phan's Custom Tailor", vi: "Phan's Custom Tailor", zh: "Phan's Custom Tailor" },
};
const wa = (text) => `https://wa.me/${config.contact.whatsapp}?text=${encodeURIComponent(text)}`;

// Responsive image. key = file stem in assets/img.
function img(key, alt, { sizes = '100vw', eager = false, cls = '' } = {}) {
  const meta = IMAGES[key];
  if (!meta) throw new Error(`Missing image: ${key}`);
  const src = `/assets/img/${key}.webp`;
  const set = [meta.small && `/assets/img/${key}-900.webp 900w`, meta.mid && `/assets/img/${key}-1400.webp 1400w`, `${src} ${meta.w}w`].filter(Boolean).join(', ');
  const srcset = meta.small ? ` srcset="${set}" sizes="${sizes}"` : '';
  const loading = eager ? 'loading="eager" fetchpriority="high"' : 'loading="lazy"';
  return `<img src="${src}"${srcset} width="${meta.w}" height="${meta.h}" alt="${esc(alt)}" ${loading} decoding="async"${cls ? ` class="${cls}"` : ''}>`;
}
function productImg(image, opts) {
  if (image.src.startsWith('img:')) return img(image.src.slice(4), image.alt, opts);
  return `<img src="${esc(image.src)}" alt="${esc(image.alt || '')}" loading="${opts?.eager ? 'eager' : 'lazy'}" decoding="async">`;
}
const figure = (key, alt, caption, ratio = '', opts = {}) =>
  `<figure class="pct-figure ${ratio}">${img(key, alt, opts)}${caption ? `<figcaption>${esc(caption)}</figcaption>` : ''}</figure>`;

// Inline SVG icons, one line set with one stroke weight.
const ICON = {
  whatsapp: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.6-.3Z"/></svg>',
  zalo: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v9a2.5 2.5 0 0 1-2.5 2.5H11l-4.5 4v-4h0A2.5 2.5 0 0 1 4 14.5Z"/><path d="M8 8h4l-4 4.5h4M14.5 8v4.5M17 10.2a1.3 1.3 0 1 1 0 .1"/></svg>',
  phone: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 3.5h3l1.5 4-2 1.3a11 11 0 0 0 5.7 5.7l1.3-2 4 1.5v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 3 5.7a2 2 0 0 1 2-2.2Z"/></svg>',
  mail: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3.5 6 8.5 7 8.5-7"/></svg>',
  pin: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 21s-7-6.2-7-11.5a7 7 0 1 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
  calendar: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3.5" y="5" width="17" height="15" rx="1"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
  instagram: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".6" fill="currentColor"/></svg>',
  facebook: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4a21 21 0 0 0-2.3-.1c-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21Z"/></svg>',
  messenger: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3c-5 0-9 3.7-9 8.4 0 2.6 1.3 5 3.3 6.5V21l3-1.6c.9.2 1.8.4 2.7.4 5 0 9-3.7 9-8.4S17 3 12 3Z"/><path d="m7.5 13.5 3-3.2 2.2 2.1 3.8-2.1-3 3.2-2.2-2.1Z" fill="currentColor"/></svg>',
  tripadvisor: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="7" cy="13" r="3.5"/><circle cx="17" cy="13" r="3.5"/><circle cx="7" cy="13" r=".8" fill="currentColor"/><circle cx="17" cy="13" r=".8" fill="currentColor"/><path d="M3.5 9.5C6 7.5 9 6.5 12 6.5s6 1 8.5 3M12 9.5l-1.5 3.5L12 15l1.5-2L12 9.5"/></svg>',
  chevron: '<svg viewBox="0 0 10 6" aria-hidden="true" fill="none" stroke="currentColor"><path d="M1 1l4 4 4-4"/></svg>',
  plus: '<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M8 1v14M1 8h14"/></svg>',
  check: '<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4"><path d="m2.5 8.5 3.5 3.5 7.5-8"/></svg>',
  play: '<svg viewBox="0 0 64 64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="32" cy="32" r="30"/><path d="M26 21v22l18-11Z" fill="currentColor"/></svg>',
  stars: '<svg viewBox="0 0 92 16" aria-hidden="true" fill="currentColor">' + [0, 1, 2, 3, 4].map((i) => `<circle cx="${8 + i * 19}" cy="8" r="${i === 4 ? 6.5 : 7}" ${i === 4 ? 'fill="none" stroke="currentColor" stroke-width="1.2"' : ''}/>`).join('') + '<path d="M83 1.5a6.5 6.5 0 0 1 0 13Z" transform="translate(-6.2 0) scale(1.08 1)"/></svg>',
};

// ---------------------------------------------------------------------------
// Shared parts
// ---------------------------------------------------------------------------
const NAV = ['process', 'pricing', 'design', 'fabrics', 'shop', 'journal', 'about', 'contact'];

const MENU = [
  ['home', 'campaign-group'], ['process', 'stock-fitting-1'], ['pricing', 'stock-man-suit-1'], ['design', 'stock-man-suit-2'], ['fabrics', 'stock-fabric-swatches-1'],
  ['shop', 'cavani-blazer'], ['journal', 'stock-man-suit-2'], ['about', 'showroom'], ['faq', 'stock-fitting-2'], ['contact', 'villa-lounge'],
];
const MONOGRAM = '<svg viewBox="0 0 40 40" aria-hidden="true" focusable="false"><circle cx="20" cy="20" r="20" fill="currentColor"/><text x="20" y="28.5" text-anchor="middle" font-family="Prata, Georgia, serif" font-size="23" fill="#fff">P</text></svg>';
const imgSmall = (key) => `/assets/img/${key}${IMAGES[key]?.small ? '-900' : ''}.webp`;
const imgLarge = (key) => `/assets/img/${key}${IMAGES[key]?.mid ? '-1400' : ''}.webp`;

function header(ctx) {
  const { lang, T, alt } = ctx;
  const langLinks = LANGS.map((l) => `<a href="${alt[l]}" hreflang="${I18N[l].htmlLang}" lang="${I18N[l].htmlLang}"${l === lang ? ' aria-current="true"' : ''} data-pct-track="language_switch" data-pct-to="${l}">${esc(I18N[l].label)}</a>`).join('');
  return `
<!-- PCT HEADER START -->
<header class="pct-header" data-pct-header>
  <div class="pct-wrap pct-header__bar">
    <a class="pct-menu-btn" href="#pct-menu" aria-controls="pct-menu" aria-expanded="false" data-pct-menu-open>
      <span class="pct-menu-btn__icon" aria-hidden="true"></span><span>${esc(T.ui.menu)}</span>
    </a>
    <a class="pct-logo" href="${pathFor(lang)}" aria-label="Phan's Custom Tailor, ${esc(T.nav.home)}">${LOGO_SVG}</a>
    <div class="pct-header__tools">
      <div class="pct-lang" data-pct-lang>
        <button class="pct-lang__btn" type="button" aria-expanded="false" aria-controls="pct-lang-list" aria-label="${esc(T.ui.language)}: ${esc(T.label)}">${esc(T.short)} ${ICON.chevron}</button>
        <div class="pct-lang__list" id="pct-lang-list">${langLinks}</div>
      </div>
      <a class="pct-btn pct-header__book" href="${config.contact.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="header">${esc(T.ui.book)}<span class="pct-sr"> (${esc(T.ui.opensNewTab)})</span></a>
    </div>
  </div>
</header>
<!-- PCT HEADER END -->
${menuOverlay(ctx)}`;
}

function menuOverlay(ctx) {
  const { lang, T, current, alt } = ctx;
  const s = config.social;
  const items = MENU.map(([k, key], i) => {
    const href = k === 'home' ? pathFor(lang) : pagePath(lang, k);
    return `<li><a href="${href}" data-pct-menu-item="${i}"${current === k ? ' aria-current="page"' : ''}>
        <span class="pct-menu__num" aria-hidden="true">${String(i + 1).padStart(2, '0')}</span>
        <span class="pct-menu__label">${esc(T.nav[k])}</span>
        <span class="pct-menu__mark">${MONOGRAM}</span>
      </a></li>`;
  }).join('');
  const activeIndex = Math.max(0, MENU.findIndex(([k]) => k === current));
  const previews = MENU.map(([, key], i) => `<img data-src="${imgSmall(key)}" alt="" decoding="async" width="${IMAGES[key].w}" height="${IMAGES[key].h}" data-pct-menu-img="${i}"${i === activeIndex ? ' class="pct-is-active"' : ''}>`).join('');
  return `
<!-- PCT MENU START -->
<div class="pct-menu" id="pct-menu" role="dialog" aria-modal="true" aria-label="${esc(T.ui.menu)}" data-pct-menu>
  <div class="pct-menu__top">
    <div class="pct-menu__brand"><a class="pct-logo" href="${pathFor(lang)}" aria-label="Phan's Custom Tailor">${LOGO_SVG}</a><span class="pct-menu__tag">${esc(T.ui.menu)}</span></div>
    <a class="pct-menu__close" href="#" role="button" aria-label="${esc(T.ui.close)}" data-pct-menu-close><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 5l14 14M19 5L5 19"/></svg></a>
  </div>
  <div class="pct-menu__body">
    <nav aria-label="Main"><ol class="pct-menu__list">${items}</ol></nav>
    <div class="pct-menu__preview" aria-hidden="true">${previews}</div>
  </div>
  <div class="pct-menu__foot">
    <div>
      <p class="pct-menu__sign">${esc(T.home.title)}</p>
      <div class="pct-menu__social">
        <a href="${s.instagram}" target="_blank" rel="noopener" aria-label="Instagram">${ICON.instagram}</a>
        <a href="${s.facebook}" target="_blank" rel="noopener" aria-label="Facebook">${ICON.facebook}</a>
        <a href="${wa(T.ui.waGeneral)}" target="_blank" rel="noopener" aria-label="WhatsApp" data-pct-track="whatsapp_click" data-pct-where="menu">${ICON.whatsapp}</a>
        <a href="${config.contact.messenger}" target="_blank" rel="noopener" aria-label="Messenger">${ICON.messenger}</a>
        <a href="${s.tripadvisor}" target="_blank" rel="noopener" aria-label="Tripadvisor">${ICON.tripadvisor}</a>
      </div>
    </div>
    <div class="pct-menu__meta">
      <p>${esc(T.footer.address[0])}<br>${esc(T.footer.hours)}</p>
      <div class="pct-menu__langs">${LANGS.map((l) => `<a href="${alt[l]}" hreflang="${I18N[l].htmlLang}" lang="${I18N[l].htmlLang}"${l === lang ? ' aria-current="true"' : ''}>${esc(I18N[l].label)}</a>`).join('')}</div>
      <a class="pct-btn" href="${config.contact.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="menu">${esc(T.ui.book)}</a>
    </div>
  </div>
</div>
<!-- PCT MENU END -->`;
}

function footer(ctx) {
  const { lang, T, alt } = ctx;
  const c = config.contact;
  const s = config.social;
  const year = new Date().getFullYear();
  return `
<!-- PCT FOOTER START -->
<footer class="pct-footer">
  <div class="pct-wrap">
    <a class="pct-logo" href="${pathFor(lang)}" aria-label="Phan's Custom Tailor">${LOGO_SVG}</a>
    <div class="pct-footer__grid">
      <div>
        <h2>${esc(T.footer.visit)}</h2>
        <address>${T.footer.address.map(esc).join('<br>')}</address>
        <p style="margin-top:14px">${esc(T.footer.hours)}<br>${esc(T.footer.hoursNote)}</p>
        <a href="${c.maps}" target="_blank" rel="noopener" class="pct-text-link">${esc(T.ui.getDirections)}</a>
        <div><a class="pct-btn pct-btn--light" href="${c.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="footer">${esc(T.ui.book)}</a></div>
      </div>
      <div>
        <h2>${esc(T.footer.contact)}</h2>
        <ul>
          <li><a href="${c.phoneHref}" data-pct-track="call_click">${esc(c.phoneDisplay)}</a></li>
          <li><a href="${wa(T.ui.waGeneral)}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="footer">WhatsApp</a></li>
          <li><a href="${c.zalo}" target="_blank" rel="noopener" data-pct-track="zalo_click">Zalo</a></li>
          <li><a href="mailto:${c.email}" data-pct-track="email_click">${esc(c.email)}</a></li>
        </ul>
      </div>
      <div>
        <h2>${esc(T.footer.explore)}</h2>
        <ul>${[...NAV.filter((k) => k !== 'contact'), 'faq', 'contact'].map((k) => `<li><a href="${pagePath(lang, k)}">${esc(T.nav[k])}</a></li>`).join('')}</ul>
      </div>
      <div>
        <h2>${esc(T.footer.follow)}</h2>
        <div class="pct-footer__social">
          <a href="${s.instagram}" target="_blank" rel="noopener" aria-label="Instagram">${ICON.instagram}</a>
          <a href="${s.facebook}" target="_blank" rel="noopener" aria-label="Facebook">${ICON.facebook}</a>
          <a href="${c.messenger}" target="_blank" rel="noopener" aria-label="Messenger">${ICON.messenger}</a>
          <a href="${s.tripadvisor}" target="_blank" rel="noopener" aria-label="Tripadvisor">${ICON.tripadvisor}</a>
        </div>
      </div>
    </div>
    <div class="pct-footer__bottom">
      <p>&copy; ${year} ${esc(T.footer.rights)}${config.indexable ? '' : `. ${esc(T.footer.proposal)}`}</p>
      <div class="pct-footer__langs">${LANGS.map((l) => `<a href="${alt[l]}" hreflang="${I18N[l].htmlLang}" lang="${I18N[l].htmlLang}"${l === lang ? ' aria-current="true"' : ''}>${esc(I18N[l].label)}</a>`).join('')}</div>
    </div>
  </div>
</footer>
<!-- PCT FOOTER END -->
<!-- PCT FLOATING START -->
<a class="pct-wa-float" href="${wa(T.ui.waGeneral)}" target="_blank" rel="noopener" aria-label="${esc(T.ui.whatsapp)}" data-pct-float data-pct-track="whatsapp_click" data-pct-where="float">${ICON.whatsapp}</a>
<div class="pct-bottom-bar" data-pct-float>
  <a class="pct-btn" href="${c.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="bottom_bar">${esc(T.ui.bookShort)}</a>
  <a class="pct-btn pct-btn--ghost" href="${wa(T.ui.waGeneral)}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="bottom_bar">${ICON.whatsapp}${esc(T.ui.whatsappShort)}</a>
</div>
<!-- PCT FLOATING END -->`;
}

function bookBand(ctx) {
  const { T } = ctx;
  return `
<section class="pct-bookband pct-section" aria-labelledby="pct-bookband-title">
  <div class="pct-wrap pct-bookband__grid">
    <div>
      <h2 class="pct-h2" id="pct-bookband-title">${esc(T.bookBand.title)}</h2>
      <p class="pct-lead" style="margin-top:20px">${esc(T.bookBand.body)}</p>
      <div class="pct-btns">
        <a class="pct-btn" href="${config.contact.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="book_band">${esc(T.ui.book)}</a>
        <a class="pct-btn pct-btn--ghost" href="${wa(T.ui.waGeneral)}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="book_band">${ICON.whatsapp}${esc(T.ui.whatsapp)}</a>
      </div>
    </div>
    <dl>
      <dt>${esc(T.bookBand.addressLabel)}</dt>
      <dd>${T.footer.address.slice(0, 2).map(esc).join('<br>')}<br><a class="pct-text-link" href="${config.contact.maps}" target="_blank" rel="noopener">${esc(T.ui.getDirections)}</a></dd>
    </dl>
    <dl>
      <dt>${esc(T.bookBand.hoursLabel)}</dt>
      <dd>${esc(T.footer.hours)}<br><span class="pct-small">${esc(T.footer.hoursNote)}</span></dd>
    </dl>
  </div>
</section>`;
}

function crumbs(ctx, items) {
  const { lang, T } = ctx;
  const all = [{ name: T.ui.breadcrumbHome, href: pathFor(lang) }, ...items];
  return `<nav class="pct-crumbs" aria-label="Breadcrumb"><ol>${all.map((c, i) => `<li>${i === all.length - 1 ? `<span aria-current="page">${esc(c.name)}</span>` : `<a href="${c.href}">${esc(c.name)}</a>`}</li>`).join('')}</ol></nav>`;
}
function breadcrumbLD(ctx, items) {
  const all = [{ name: ctx.T.ui.breadcrumbHome, href: pathFor(ctx.lang) }, ...items];
  return { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: all.map((c, i) => ({ '@type': 'ListItem', position: i + 1, name: c.name, item: abs(c.href) })) };
}

function pageHead(ctx, key, { kicker, title, sub, aside = '', crumbItems }) {
  return `
<section class="pct-page-head">
  <div class="pct-wrap">
    ${crumbs(ctx, crumbItems || [{ name: ctx.T.nav[key], href: pagePath(ctx.lang, key) }])}
    <div class="pct-page-head__grid">
      <div>
        <h1 class="pct-h1"><span class="pct-kicker">${esc(kicker)}</span><span class="pct-h1__text">${esc(title)}</span></h1>
        ${sub ? `<p class="pct-lead">${esc(sub)}</p>` : ''}
      </div>
      ${aside ? `<div class="pct-page-head__aside">${aside}</div>` : ''}
    </div>
  </div>
</section>`;
}
const visitAside = (T) => `<p><strong>${esc(T.bookBand.hoursLabel)}</strong>${esc(T.footer.hours)}</p><p><strong>${esc(T.bookBand.addressLabel)}</strong>${esc(T.footer.address[0])}, ${esc(T.footer.address[1])}</p>`;

function priceList(ctx, { compact = false, keys = null } = {}) {
  const { lang, T } = ctx;
  const items = PRICES.items.filter((p) => !keys || keys.includes(p.key));
  return `<div class="pct-pricelist${compact ? ' pct-pricelist--compact' : ''}">${items.map((p) => `
    <div class="pct-pricelist__row">
      <div class="pct-pricelist__name">${esc(T.prices[p.key].name)}</div>
      <div class="pct-pricelist__price">${p.from ? `<small>${esc(T.ui.from)}</small>${fmtPrice(p.from, lang)}` : `${esc(T.ui.priceOnConsultation)}<!-- CONFIRM: ${esc(p.confirm)} -->`}</div>
      ${compact ? '' : `<p class="pct-pricelist__desc">${esc(T.prices[p.key].desc)}</p>`}
    </div>`).join('')}
  </div>`;
}

function reviewsBlock(ctx, { count = 4 } = {}) {
  const { lang, T } = ctx;
  const items = REVIEWS.items.slice(0, count);
  const q = (r, lead = false) => `<figure class="pct-quote${lead ? ' pct-quote--lead' : ''}" lang="en"><blockquote><p>&ldquo;${esc(r.quote)}&rdquo;</p></blockquote><figcaption>${esc(r.name)}${r.place ? `, ${esc(r.place)}` : ''}, ${esc(fmtMonth(r.date, lang))}</figcaption></figure>`;
  return `
  <div class="pct-reviews">
    <div>${q(items[0], true)}</div>
    <div class="pct-quotes-side">${items.slice(1).map((r) => q(r)).join('')}</div>
  </div>
  <div class="pct-reviews__foot">
    <span class="pct-rating">${ICON.stars}<span>${esc(REVIEWS.rating)} / 5, Tripadvisor</span></span><!-- CONFIRM: ${esc(REVIEWS.confirm)} -->
    <a class="pct-link" href="${REVIEWS.url}" target="_blank" rel="noopener">${esc(T.ui.tripadvisorAll)}</a>
    <span class="pct-small">${esc(T.ui.quotedFrom)}</span>
  </div>`;
}

const COVERS = {
  'the-wardrobe-workhorse-a-guide-to-the-versatile-blazer': ['stock-man-suit-2', 'Light grey jacket with a patterned pocket square'],
  'what-is-a-suit-jacket-anatomy-fabrics-the-orphaning-rule': ['stock-fitting-1', 'Hands adjusting the lapel of a grey suit jacket'],
  'suit-jacket-vs-blazer-vs-sport-coat-a-gentleman-s-guide-phan-s-cu': ['stock-hero-workroom-3', 'Choosing buttons on a suiting swatch card'],
  'the-story-of-nobility-weaving-heritage-technology-and-timeless-styl': ['nobility-books', 'Nobility swatch books laid out on a table'],
  'summer-suiting-2025': ['stock-linen-1', 'Three men in linen shirts and suits on a sunny balcony'],
  '5-classic-suit-mistakes-how-to-fix-them-like-an-expert': ['stock-trousers-1', 'Cuffed hem of grey check trousers above tan shoes'],
  'the-art-of-bespoke-crafting-your-perfect-2-piece-suit': ['stock-chalk-scissors-1', 'Tailor marking tweed cloth on a wooden workbench'],
};
function postCard(ctx, post, { sizes = '(max-width: 767px) 100vw, 33vw' } = {}) {
  const { lang, T } = ctx;
  const [key, alt] = COVERS[post.slug];
  return `<a class="pct-post-card" data-pct-cursor="read" href="${pathFor(lang, `journal/${post.slug}`)}">
    ${figure(key, alt, '', '', { sizes })}
    <p class="pct-post-card__meta">${fmtDate(post.date, lang)}, ${esc(fill(T.ui.minRead, { n: post.minutes[lang] || post.minutes.en }))}</p>
    <h3>${esc(post.title[lang] || post.title.en)}</h3>
    <p>${esc(post.excerpt[lang] || post.excerpt.en)}</p>
  </a>`;
}

// ---------------------------------------------------------------------------
// Pages
// ---------------------------------------------------------------------------
function pageHome(ctx) {
  const { lang, T } = ctx;
  const H = T.home;
  const body = `
<section class="pct-hero" aria-labelledby="pct-home-title" data-pct-hero>
  <div class="pct-hero__media" data-pct-gl="swap" data-pct-gl-src="/assets/img/campaign-group-1400.webp" data-pct-gl-src-lg="/assets/img/campaign-group.webp">
    ${img('campaign-group', 'Four men in navy, grey and black suits made by Phan\'s Custom Tailor', { eager: true, cls: 'pct-hero__slide pct-is-active' })}
    ${H.heroLinks.map((l, i) => `<img data-src="${imgLarge(l.img)}" alt="" class="pct-hero__slide" width="${IMAGES[l.img].w}" height="${IMAGES[l.img].h}" data-pct-slide="${i + 1}">`).join('')}
  </div>
  <div class="pct-wrap pct-hero__inner">
    <h1 class="pct-hero__label" id="pct-home-title">${esc(H.kicker)}</h1>
    <ul class="pct-hero__links">
      ${H.heroLinks.map((l, i) => {
        const href = l.to === 'booking' ? config.contact.booking : `${pagePath(lang, l.to)}${l.hash ? '#' + l.hash : ''}`;
        const ext = l.to === 'booking' ? ' target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="hero"' : '';
        return `<li><a href="${href}" data-pct-slide-link="${i + 1}" data-pct-gl-img="${imgLarge(l.img)}"${ext}><span>${esc(l.label)}</span></a></li>`;
      }).join('')}
    </ul>
    <p class="pct-hero__note">${esc(H.heroMeta[1])}<br>${esc(H.heroMeta[0])}</p>
  </div>
</section>

<section class="pct-section" aria-labelledby="pct-intro-title">
  <div class="pct-wrap pct-grid-2">
    <div class="pct-col-5 pct-intro__text">
      <h2 class="pct-h2" id="pct-intro-title">${esc(H.introTitle)}</h2>
      <p class="pct-lead">${esc(H.introBody)}</p>
      <a class="pct-link" href="${pagePath(lang, 'about')}">${esc(H.introLink)}</a>
    </div>
    <div class="pct-col-7 pct-intro__figure">
      ${figure('villa-lounge', 'Fitting lounge at the Phan\'s Custom Tailor villa with armchairs and the PHAN\'S sign', H.introCaption, 'pct-ratio-3x2', { sizes: '(max-width: 767px) 100vw, 58vw' })}
    </div>
  </div>
</section>

<section class="pct-section pct-section--white" aria-labelledby="pct-process-title">
  <div class="pct-wrap">
    <div class="pct-section-head">
      <h2 class="pct-h2" id="pct-process-title">${esc(H.processTitle)}</h2>
      <p class="pct-lead">${esc(H.processIntro)}</p>
    </div>
    <ol class="pct-steps">
      ${T.steps.map((s, i) => `<li class="pct-step"><p class="pct-step__num" aria-hidden="true">${String(i + 1).padStart(2, '0')}</p><h3>${esc(s.title)}</h3><p>${esc(s.short)}</p></li>`).join('')}
    </ol>
    <div class="pct-steps-foot"><a class="pct-link" href="${pagePath(lang, 'process')}">${esc(H.processLink)}</a></div>
  </div>
</section>

<section class="pct-section" aria-labelledby="pct-prices-title">
  <div class="pct-wrap pct-grid-2">
    <div class="pct-col-5">
      ${figure('stock-man-suit-1', 'Man buttoning a light grey tailored suit outdoors', '', 'pct-ratio-4x5', { sizes: '(max-width: 767px) 100vw, 40vw' })}
    </div>
    <div class="pct-col-7">
      <h2 class="pct-h2" id="pct-prices-title">${esc(H.pricesTitle)}</h2>
      <p class="pct-lead" style="margin:20px 0 36px">${esc(H.pricesIntro)}</p>
      ${priceList(ctx, { compact: true, keys: ['suit2', 'suit3', 'trousers', 'shirt'] })}
      <div class="pct-btns" style="margin-top:32px">
        <a class="pct-link" href="${pagePath(lang, 'pricing')}">${esc(H.pricesLink)}</a>
      </div>
    </div>
  </div>
</section>

<section aria-labelledby="pct-fabrics-title">
  <div class="pct-band" data-pct-gl="cloth" data-pct-gl-src="/assets/img/hs-cloth-navy-gl.webp">${img('hs-cloth-navy', 'Navy windowpane suiting cloth', { sizes: '100vw' })}</div>
  <div class="pct-section--white pct-section--tight">
    <div class="pct-wrap">
      <h2 class="pct-h2" id="pct-fabrics-title">${esc(H.fabricsTitle)}</h2>
      <p class="pct-millnames" aria-label="Vitale Barberis Canonico, Holland &amp; Sherry, Nobility"><span>Vitale Barberis Canonico</span><span>Holland &amp; Sherry</span><span>Nobility</span></p>
      <p class="pct-lead">${esc(H.fabricsIntro)}</p>
      <div style="margin-top:28px"><a class="pct-link" href="${pagePath(lang, 'fabrics')}">${esc(H.fabricsLink)}</a></div>
    </div>
  </div>
</section>

<section class="pct-section" id="reviews" aria-labelledby="pct-reviews-title">
  <div class="pct-wrap">
    <div class="pct-section-head">
      <h2 class="pct-h2" id="pct-reviews-title">${esc(H.reviewsTitle)}</h2>
      <p class="pct-lead">${esc(H.reviewsIntro)}</p>
    </div>
    ${reviewsBlock(ctx, { count: 4 })}
  </div>
</section>

<section class="pct-section pct-section--white" aria-labelledby="pct-journal-title">
  <div class="pct-wrap">
    <div class="pct-section-head">
      <h2 class="pct-h2" id="pct-journal-title">${esc(H.journalTitle)}</h2>
      <div><a class="pct-link" href="${pagePath(lang, 'journal')}">${esc(H.journalLink)}</a></div>
    </div>
    <div class="pct-postlist">${JOURNAL.slice(0, 3).map((p) => postCard(ctx, p)).join('')}</div>
  </div>
</section>`;
  const ld = {
    '@context': 'https://schema.org', '@type': 'ClothingStore', '@id': abs('/#business'),
    name: "Phan's Custom Tailor", alternateName: ["Phan's", 'Phan Custom Tailor'],
    description: T.pages.home.description, url: abs(pathFor(lang)), logo: abs('/assets/brand/logo.png'), image: abs('/assets/img/villa-lounge.webp'),
    telephone: '+84826977888', email: config.contact.email,
    address: { '@type': 'PostalAddress', streetAddress: 'Villa, 08 D9 Street, Saigon Pearl', addressLocality: 'Bình Thạnh', addressRegion: 'Ho Chi Minh City', addressCountry: 'VN' },
    openingHoursSpecification: [{ '@type': 'OpeningHoursSpecification', dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], opens: '09:00', closes: '19:00' }, { '@type': 'OpeningHoursSpecification', dayOfWeek: ['Sunday'], opens: '11:00', closes: '15:00' }],
    priceRange: '1,300,000–8,400,000 VND', currenciesAccepted: 'VND',
    founder: [{ '@type': 'Person', name: 'Thinh Phan' }, { '@type': 'Person', name: 'Thuong Phan' }],
    sameAs: [config.social.instagram, config.social.facebook, config.social.tripadvisor],
    inLanguage: T.htmlLang,
  };
  const hero = IMAGES['campaign-group'];
  const preload = `<link rel="preload" as="image" href="/assets/img/campaign-group.webp" imagesrcset="/assets/img/campaign-group-900.webp 900w, /assets/img/campaign-group-1400.webp 1400w, /assets/img/campaign-group.webp ${hero.w}w" imagesizes="100vw" fetchpriority="high">`;
  return { body, overlay: false, jsonld: [ld], noBand: false, preload };
}

function pageAbout(ctx) {
  const { lang, T } = ctx;
  const A = T.about;
  const body = `
${pageHead(ctx, 'about', { kicker: A.kicker, title: A.title, sub: A.sub })}
<div class="pct-band">${img('showroom', 'Inside the Phan\'s villa: cloth shelves, a long cutting table and suits on display', { sizes: '100vw', eager: true })}</div>
<section class="pct-section">
  <div class="pct-wrap pct-grid-2">
    <div class="pct-col-7 pct-prose pct-lead">
      ${A.body.map((p, i) => `<p>${esc(p)}</p>${i === 2 ? '<!-- CONFIRM: "since 2013" taken from the client\'s old About page -->' : ''}`).join('')}
      <p class="pct-signature">${esc(A.sign)}</p>
    </div>
    <div class="pct-col-5">
      ${figure('stock-fabric-swatches-3', 'Client choosing suiting from swatch books on a low table', '', 'pct-ratio-4x5', { sizes: '(max-width: 767px) 100vw, 40vw' })}
    </div>
  </div>
</section>
<section class="pct-section pct-section--white" aria-labelledby="pct-values-title">
  <div class="pct-wrap">
    <h2 class="pct-h2" id="pct-values-title" style="margin-bottom:40px">${esc(A.valuesTitle)}</h2>
    <div class="pct-values">${A.values.map((v, i) => `<div class="pct-value"><p class="pct-value__n">${String(i + 1).padStart(2, '0')}</p><h3>${esc(v.title)}</h3><p>${esc(v.body)}</p></div>`).join('')}</div>
  </div>
</section>
<section class="pct-section" aria-labelledby="pct-villa-title">
  <div class="pct-wrap">
    <div class="pct-section-head">
      <h2 class="pct-h2" id="pct-villa-title">${esc(A.villaTitle)}</h2>
      <p class="pct-lead">${esc(A.villaBody)}<!-- CONFIRM: distance to Landmark 81 (from Tripadvisor's map) --></p>
    </div>
    <div class="pct-grid-2">
      <div class="pct-col-7">${figure('villa-lounge', 'Armchairs and a round table in the fitting lounge under the PHAN\'S sign', A.villaCaption1, 'pct-ratio-3x2', { sizes: '(max-width: 767px) 100vw, 58vw' })}</div>
      <div class="pct-col-5">${figure('stock-chalk-scissors-1', 'Tailor marking cloth with chalk at a wooden cutting table', A.villaCaption2, 'pct-ratio-4x5', { sizes: '(max-width: 767px) 100vw, 40vw' })}</div>
    </div>
  </div>
</section>`;
  return { body, jsonld: [breadcrumbLD(ctx, [{ name: T.nav.about, href: pagePath(lang, 'about') }])] };
}

function pageProcess(ctx) {
  const { lang, T } = ctx;
  const P = T.process;
  const imgs = [
    ['showroom', 'The villa showroom with cloth shelves and the cutting table'],
    ['stock-fabric-swatches-1', 'Swatch card of navy, grey and brown suitings'],
    ['stock-fitting-1', 'Hands adjusting the lapel of a grey jacket during a fitting'],
    ['stock-stitching-1', 'Close-up of a needle and thread finishing a garment by hand'],
    ['stock-fitting-2', 'Black and white photo of a client trying on a tailored jacket'],
  ];
  const body = `
${pageHead(ctx, 'process', { kicker: P.kicker, title: P.title, sub: P.sub, aside: visitAside(T) })}
<section class="pct-section" style="padding-top:0">
  <div class="pct-wrap">
    <ol class="pct-longsteps">
      ${T.steps.map((s, i) => `<li class="pct-longstep">
        <p class="pct-longstep__num" aria-hidden="true">${String(i + 1).padStart(2, '0')}</p>
        <div><h2 class="pct-h3">${esc(s.title)}</h2><p>${esc(s.long)}</p>${i === 0 ? `<div class="pct-btns" style="margin-top:24px"><a class="pct-btn" href="${config.contact.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="process_step">${esc(T.ui.book)}</a></div>` : ''}</div>
        ${figure(imgs[i][0], imgs[i][1], '', '', { sizes: '(max-width: 767px) 100vw, 45vw' })}
      </li>`).join('')}
    </ol>
  </div>
</section>
<section class="pct-section pct-section--white" aria-labelledby="pct-trip-title">
  <div class="pct-wrap">
    <div class="pct-section-head">
      <h2 class="pct-h2" id="pct-trip-title">${esc(P.tripTitle)}</h2>
      <p class="pct-lead">${esc(P.tripIntro)}</p>
    </div>
    <div class="pct-trip">${P.trip.map((t) => `<div><strong>${esc(t.label)}</strong><p>${esc(t.body)}</p></div>`).join('')}</div>
  </div>
</section>
<section class="pct-section" aria-labelledby="pct-life-title">
  <div class="pct-wrap pct-grid-2">
    <div class="pct-col-6">${figure('stock-pressing-1', 'Pressing a white shirt with an iron', '', 'pct-ratio-3x2', { sizes: '(max-width: 767px) 100vw, 50vw' })}</div>
    <div class="pct-col-6"><h2 class="pct-h2" id="pct-life-title">${esc(P.lifetimeTitle)}</h2><p class="pct-lead" style="margin-top:20px">${esc(P.lifetimeBody)}</p></div>
  </div>
</section>`;
  const ld = {
    '@context': 'https://schema.org', '@type': 'HowTo', name: P.title, inLanguage: T.htmlLang,
    step: T.steps.map((s, i) => ({ '@type': 'HowToStep', position: i + 1, name: s.title, text: s.long })),
  };
  return { body, jsonld: [ld, breadcrumbLD(ctx, [{ name: T.nav.process, href: pagePath(lang, 'process') }])] };
}

const BOOK_ICON = {
  consult: '<path d="M12 3l-4 3-3 1 1 14h12l1-14-3-1-4-3zM12 3v18M8 6l4 6 4-6"/>',
  urgent: '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M10 2h4"/>',
  group: '<circle cx="8" cy="7" r="3"/><circle cx="16" cy="7" r="3"/><path d="M2 21c0-4 3-7 6-7s6 3 6 7M12 21c0-4 2-7 4-7s6 3 6 7"/>',
  female: '<circle cx="12" cy="5" r="3"/><path d="M9 9l-3 12h12L15 9M9 9h6M10 9l2 5 2-5"/>',
  fitting: '<path d="M4 20l7-7M14 4l6 6-4 1-3 3-3-3 3-3 1-4zM6 14l4 4"/>',
  pickup: '<path d="M5 8h14l-1 13H6L5 8zM9 8V6a3 3 0 016 0v2M9 14l2 2 4-4"/>',
  repair: '<path d="M6 3l12 12M4 20c3 0 5-2 5-5M14 4a3 3 0 014 4M18 21l-4-4"/>',
};
const bookIcon = (k) => `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">${BOOK_ICON[k]}</svg>`;

function pageBook(ctx) {
  const { lang, T } = ctx;
  const K = T.book;
  const sys = config.bookingSystem;
  const facts = `<div class="pct-book__facts">${K.facts.map(([n, t]) => `<div><strong>${esc(n)}</strong><span>${esc(t)}</span></div>`).join('')}</div>`;
  const info = `<details class="pct-book__info" open><summary><span>${esc(K.readMore)}</span><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 9l6 6 6-6"/></svg></summary>
      ${facts}<div class="pct-book__policies">${K.policies.map((x, i) => `<section><h2><span>${String(i + 1).padStart(2, '0')}</span>${esc(x.t)}</h2><ul>${x.items.map((it) => `<li>${esc(it)}</li>`).join('')}</ul></section>`).join('')}</div></details>`;
  const side = `<aside class="pct-book__side" id="pct-book-policies">
    <figure class="pct-book__photo"><img src="${imgSmall('villa-lounge')}" alt="" width="${IMAGES['villa-lounge'].w}" height="${IMAGES['villa-lounge'].h}" decoding="async"><figcaption><span>${esc(K.kicker)}</span><strong>${esc(K.welcome)}</strong><em>${esc(K.welcomeSub)}</em></figcaption></figure>
    ${info}</aside>`;
  const progress = `<div class="pct-book__progress"><p class="pct-book__count" data-bcount>${esc(K.stepOf.replace('{n}', '1'))}</p><ol class="pct-book__dots">${K.steps.map((x, i) => `<li data-bdot="${i + 1}"${i === 0 ? ' class="is-on" aria-current="step"' : ''}><i></i><span>${esc(x)}</span></li>`).join('')}</ol></div>`;
  const services = sys.services.map((k) => `<button type="button" class="pct-book__svc pct-book__svc--${k}" data-service="${k}" aria-pressed="false"><span class="pct-book__svcicon">${bookIcon(k)}</span><span class="pct-book__svctext"><strong>${esc(K.services[k][0])}</strong><span>${esc(K.services[k][1])}</span></span><span class="pct-book__svcgo" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></button>`).join('');
  const chosen = `<div class="pct-book__chosen"><div data-bchosen></div><button type="button" class="pct-book__change" data-bback="1">${esc(K.change)}</button></div>`;
  const data = { lang, T: K, api: '/api/booking', sys: { timeZone: sys.timeZone, maxPerSlot: sys.maxPerSlot, slotMinutes: sys.slotMinutes, hours: sys.hours, lastStartBeforeClose: sys.lastStartBeforeClose, closedDates: sys.closedDates, fieldsFor: sys.fieldsFor } };
  const body = `
${pageHead(ctx, 'book', { kicker: K.kicker, title: K.title, sub: '' })}
<section class="pct-section pct-book-section" style="padding-top:0">
  <div class="pct-wrap pct-book" data-pct-book>
    ${side}
    <div class="pct-book__flow">
      ${progress}
      <noscript><p class="pct-book__hint">${esc(T.contact.chatBody)} <a class="pct-text-link" href="${wa(T.ui.waGeneral)}">WhatsApp</a> · <a class="pct-text-link" href="${config.contact.phoneHref}">${esc(config.contact.phoneDisplay)}</a></p></noscript>
      <div class="pct-book__step" data-bstep="1"><h2 class="pct-book__h">${esc(K.selectService)}</h2><div class="pct-book__svcs">${services}</div></div>
      <div class="pct-book__step" data-bstep="2" hidden><h2 class="pct-book__h">${esc(K.steps[1])}</h2>${chosen}<p class="pct-book__demo" data-bdemo hidden>${esc(K.demoNote)}</p>
        <div class="pct-book__when"><div class="pct-book__cal" data-bcal></div><div class="pct-book__times" data-bslots></div></div></div>
      <div class="pct-book__step" data-bstep="3" hidden><h2 class="pct-book__h">${esc(K.steps[2])}</h2>${chosen}
        <p class="pct-book__notice" data-burgent hidden>${esc(K.urgentNote)}</p>
        <form data-bformwrap novalidate><div class="pct-book__form" data-bform></div>
        <div class="pct-book__field pct-book__ack" data-field="ack"><label class="pct-book__check"><input type="checkbox" id="pb-ack" name="ack" required aria-describedby="pb-ack-err"> <span>${esc(K.ack)} <a class="pct-text-link" href="#pct-book-policies" data-bpolicies>${esc(K.readMore)}</a></span></label><p class="pct-book__err" id="pb-ack-err" aria-live="polite"></p></div>
        <p class="pct-book__almost">${esc(K.almost)}</p><p class="pct-book__err" data-bformerr aria-live="assertive"></p>
        <div class="pct-book__actions"><button type="button" class="pct-btn pct-btn--ghost" data-bback="2">${esc(K.back)}</button><button type="submit" class="pct-btn">${esc(K.confirm)}</button></div></form></div>
      <div class="pct-book__step pct-book__done" data-bstep="4" hidden>
        <span class="pct-book__tick" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="10"/><path d="M7.5 12.5l3 3 6-6.5"/></svg></span>
        <h2 class="pct-book__h" data-bdone-title></h2><p class="pct-book__donebody" data-bdone-body></p>
        <div class="pct-book__ticket"><p class="pct-book__ticketk">${esc(K.summary)}</p><div data-bchosen></div><p class="pct-book__where">${esc(K.where)}</p></div>
        <div class="pct-btns"><button type="button" class="pct-btn" data-bics hidden>${esc(K.addCal)}</button><a class="pct-btn pct-btn--ghost" href="${wa(T.ui.waGeneral)}" target="_blank" rel="noopener">${ICON.whatsapp}${esc(T.ui.whatsapp)}</a></div>
        <button type="button" class="pct-text-link pct-book__again" data-bagain>${esc(K.doneAgain)}</button></div>
    </div>
  </div>
  <script type="application/json" id="pct-book-data">${JSON.stringify(data).replace(/</g, '\\u003c')}</script>
</section>`;
  return { body, noBand: true, scripts: `<script type="module" src="/assets/js/booking.mjs?v=${ASSET_V}"></script>`, jsonld: [breadcrumbLD(ctx, [{ name: T.nav.book, href: pagePath(lang, 'book') }])] };
}

function pageDesign(ctx) {
  const { lang, T } = ctx;
  const D = T.design;
  const lbl = (o) => o[lang] || o.en;
  const st = { ...CFG_DEFAULTS };
  const steps = ['fabric', 'jacket', 'trousers', 'details', 'review'];
  const opt = (g, o) => {
    const on = st[g.key] === o.v;
    const thumb = g.thumb ? `<span class="pct-cfg__thumb" aria-hidden="true"></span>`
      : o.swatch ? `<span class="pct-cfg__sw" style="background:${o.swatch}"></span>` : '';
    return `<button type="button" class="pct-cfg__opt${on ? ' is-on' : ''}" role="radio" aria-checked="${on}" data-k="${g.key}" data-v="${o.v}"${g.thumb ? ` data-thumb="${g.thumb}"${g.back ? ' data-back="1"' : ''}` : ''}>${thumb}<span class="pct-cfg__optlabel">${esc(lbl(o.label))}</span></button>`;
  };
  const group = (g) => `<fieldset class="pct-cfg__group"><legend>${esc(lbl(g.label))}</legend><div class="pct-cfg__opts${g.thumb ? ' pct-cfg__opts--thumbs' : o_sw(g)}" role="radiogroup" aria-label="${esc(lbl(g.label))}">${g.options.map((o) => opt(g, o)).join('')}</div></fieldset>`;
  const o_sw = (g) => (g.options[0].swatch ? ' pct-cfg__opts--swatches' : '');
  const fabrics = `<p class="pct-cfg__note">${esc(D.fabricNote)}</p><div class="pct-cfg__fabrics" role="radiogroup" aria-label="${esc(D.steps.fabric)}">${CFG.fabrics.map((f) =>
    `<button type="button" class="pct-cfg__fab${st.fabric === f.id ? ' is-on' : ''}" role="radio" aria-checked="${st.fabric === f.id}" data-k="fabric" data-v="${f.id}"><i class="pct-cfg__fabimg" style="background-image:url(/assets/img/cfg/${f.id}.jpg)" aria-hidden="true"></i><span>${esc(lbl(f.name))}</span></button>`).join('')}</div>`;
  const pane = (k) => CFG.groups.filter((g) => g.step === k).map(group).join('');
  const nav = (i) => `<div class="pct-cfg__nav">${i > 0 ? `<button type="button" class="pct-btn pct-btn--ghost" data-go="${steps[i - 1]}">${esc(D.prev)}</button>` : '<span></span>'}${i < steps.length - 1 ? `<button type="button" class="pct-btn" data-go="${steps[i + 1]}">${esc(D.next)}: ${esc(D.steps[steps[i + 1]])}</button>` : ''}</div>`;
  const panes = {
    fabric: fabrics,
    jacket: pane('jacket'),
    trousers: pane('trousers'),
    details: pane('details') + `<fieldset class="pct-cfg__group"><legend>${esc(D.monogram)}</legend><label class="pct-cfg__mono"><input type="text" maxlength="3" autocomplete="off" spellcheck="false" placeholder="ABC" data-k="monogram" aria-describedby="pct-cfg-mono-hint"><span id="pct-cfg-mono-hint">${esc(D.monogramHint)}</span></label></fieldset>`,
    review: `<h2 class="pct-h3">${esc(D.reviewTitle)}</h2><dl class="pct-cfg__summary" data-cfg-summary></dl>
      <div class="pct-cfg__price"><span>${esc(D.priceFrom)}</span><strong data-cfg-price></strong></div><p class="pct-cfg__note">${esc(D.priceNote)}</p>
      <div class="pct-btns"><a class="pct-btn" data-cfg-wa href="${wa(D.waIntro)}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="designer">${ICON.whatsapp}${esc(D.send)}</a>
      <a class="pct-btn pct-btn--ghost" href="${config.contact.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="designer">${esc(D.book)}</a></div>
      <button type="button" class="pct-text-link pct-cfg__copy" data-cfg-copy data-done="${esc(D.copied)}">${esc(D.copy)}</button>
      <div class="pct-cfg__tryon"><h3>${esc(D.tryTitle)}</h3><p>${esc(D.tryBody)}</p><img data-cfg-tryimg alt="${esc(D.tryAlt)}" width="330" height="752" decoding="async"></div>`,
  };
  const data = {
    lang, fabrics: CFG.fabrics, groups: CFG.groups, D, defaults: CFG_DEFAULTS, wa: config.contact.whatsapp,
    prices: Object.fromEntries(PRICES.items.filter((p) => p.from).map((p) => [p.key, p.from])), currency: T.ui.currency,
  };
  const body = `
${pageHead(ctx, 'design', { kicker: D.kicker, title: D.title, sub: D.sub })}
<section class="pct-section" style="padding-top:0">
  <div class="pct-wrap pct-cfg" data-pct-cfg>
    <div class="pct-cfg__stage">
      <div class="pct-cfg__canvas" data-cfg-stage>${suitSVG(st, CFG_FAB, { label: D.title })}</div>
      <div class="pct-cfg__bar">
        <div class="pct-cfg__views" role="group" aria-label="${esc(D.front)} / ${esc(D.back)}"><button type="button" class="is-on" data-view="front" aria-pressed="true">${esc(D.front)}</button><button type="button" data-view="back" aria-pressed="false">${esc(D.back)}</button></div>
        <p class="pct-cfg__caption" data-cfg-caption>${esc(lbl(CFG.fabrics[0].name))}</p>
      </div>
      <p class="pct-cfg__note">${esc(D.previewNote)}</p>
    </div>
    <div class="pct-cfg__panel">
      <div class="pct-cfg__tabs" role="tablist">${steps.map((k, i) => `<button type="button" role="tab" id="pct-cfg-tab-${k}" aria-controls="pct-cfg-pane-${k}" aria-selected="${i === 0}" data-step="${k}"><span>${String(i + 1).padStart(2, '0')}</span>${esc(D.steps[k])}</button>`).join('')}</div>
      ${steps.map((k, i) => `<div class="pct-cfg__pane" role="tabpanel" id="pct-cfg-pane-${k}" aria-labelledby="pct-cfg-tab-${k}" data-pane="${k}"${i ? ' hidden' : ''}>${panes[k]}${nav(i)}</div>`).join('')}
    </div>
  </div>
  <script type="application/json" id="pct-cfg-data">${JSON.stringify(data).replace(/</g, '\\u003c')}</script>
</section>`;
  return { body, tryon: true, scripts: `<script type="module" src="/assets/js/configurator.mjs?v=${ASSET_V}"></script>`, jsonld: [breadcrumbLD(ctx, [{ name: T.nav.design, href: pagePath(lang, 'design') }])] };
}

function pagePricing(ctx) {
  const { lang, T } = ctx;
  const P = T.pricing;
  const occImgs = [['stock-man-suit-2', 'Light grey suit jacket with a dark tie and pocket square'], ['stock-man-suit-1', 'Man in a light grey suit with a buttonhole flower'], ['stock-linen-1', 'Men in linen on a sunny balcony above the city']];
  const body = `
${pageHead(ctx, 'pricing', { kicker: P.kicker, title: P.title, sub: P.sub, aside: visitAside(T) })}
<section class="pct-section" style="padding-top:0" aria-labelledby="pct-pricelist-title">
  <div class="pct-wrap pct-grid-2">
    <div class="pct-col-7">
      <h2 class="pct-sr" id="pct-pricelist-title">${esc(P.tableCaption)}</h2>
      <p class="pct-pricelist__caption">${esc(P.tableCaption)}</p>
      ${priceList(ctx)}
      <div class="pct-btns" style="margin-top:36px">
        <a class="pct-btn" href="${config.contact.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="pricing">${esc(T.ui.book)}</a>
        <a class="pct-btn pct-btn--ghost" href="${wa(T.ui.waPricing)}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="pricing">${ICON.whatsapp}${esc(T.ui.whatsapp)}</a>
      </div>
      <p style="margin-top:22px"><a class="pct-link" href="${pagePath(lang, 'design')}">${esc(T.nav.design)}</a></p>
    </div>
    <div class="pct-col-5">
      <h2 class="pct-h3" style="margin-bottom:18px">${esc(P.includedTitle)}</h2>
      <ul class="pct-checklist">${P.included.map((x) => `<li>${ICON.check}${esc(x)}</li>`).join('')}</ul>
    </div>
  </div>
</section>
<section class="pct-section pct-section--white" aria-labelledby="pct-women-title">
  <div class="pct-wrap pct-grid-2" style="align-items:center">
    <div class="pct-col-5">${figure('stock-woman-suit-1', 'Woman in a camel trouser suit standing in a stone doorway', '', 'pct-ratio-4x5', { sizes: '(max-width: 767px) 100vw, 40vw' })}</div>
    <div class="pct-col-7"><h2 class="pct-h2" id="pct-women-title">${esc(P.womenTitle)}</h2><p class="pct-lead" style="margin-top:20px">${esc(P.womenBody)}</p><!-- CONFIRM: prices for women's garments --></div>
  </div>
</section>
<section class="pct-section" aria-labelledby="pct-occ-title">
  <div class="pct-wrap">
    <h2 class="pct-h2" id="pct-occ-title" style="margin-bottom:40px">${esc(P.occasionsTitle)}</h2>
    <div class="pct-trio">${P.occasions.map((o, i) => `<div>${figure(occImgs[i][0], occImgs[i][1], '', 'pct-ratio-3x2', { sizes: '(max-width: 767px) 100vw, 33vw' })}<h3 style="margin-top:20px">${esc(o.title)}</h3><p>${esc(o.body)}</p></div>`).join('')}</div>
  </div>
</section>
<section class="pct-section pct-section--white" aria-labelledby="pct-ask-title">
  <div class="pct-wrap pct-wrap--narrow" style="text-align:left">
    <h2 class="pct-h2" id="pct-ask-title">${esc(P.askTitle)}</h2>
    <p class="pct-lead" style="margin-top:20px">${esc(P.askBody)}</p>
    <div class="pct-btns" style="margin-top:28px">
      <a class="pct-btn pct-btn--ghost" href="${pagePath(lang, 'contact')}#pct-enquiry">${esc(T.form.submit)}</a>
      <a class="pct-btn pct-btn--ghost" href="${wa(T.ui.waPricing)}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="pricing_ask">${ICON.whatsapp}${esc(T.ui.whatsapp)}</a>
    </div>
  </div>
</section>`;
  const ld = {
    '@context': 'https://schema.org', '@type': 'OfferCatalog', name: P.title, inLanguage: T.htmlLang,
    itemListElement: PRICES.items.filter((p) => p.from).map((p) => ({ '@type': 'Offer', itemOffered: { '@type': 'Service', name: T.prices[p.key].name }, priceSpecification: { '@type': 'PriceSpecification', minPrice: p.from, priceCurrency: 'VND' } })),
  };
  return { body, jsonld: [ld, breadcrumbLD(ctx, [{ name: T.nav.pricing, href: pagePath(lang, 'pricing') }])] };
}

function pageFabrics(ctx) {
  const { lang, T } = ctx;
  const F = T.fabrics;
  const body = `
${pageHead(ctx, 'fabrics', { kicker: F.kicker, title: F.title, sub: F.sub })}
<div class="pct-band">${img('stock-fabric-swatches-1', 'Swatch card of navy, grey and brown suitings with a glass paperweight', { sizes: '100vw', eager: true })}</div>
<section class="pct-section" aria-label="${esc(F.title)}">
  <div class="pct-wrap">
    <div class="pct-mills">${F.mills.map((m) => `<article class="pct-mill" id="pct-mill-${m.key}"><p class="pct-mill__origin">${esc(m.origin)}</p><h2 class="pct-h3">${esc(m.name)}</h2><p>${esc(m.body)}</p></article>`).join('')}</div>
    <!-- CONFIRM: other mill logos shown on the old site (Zegna, Loro Piana, Cerruti, Charles Clayton, Dolce & Taylor, Snow Berry, Luciano, Lord & Taylor) are not listed until the client confirms they are stocked -->
  </div>
</section>
<section class="pct-section pct-section--white" aria-labelledby="pct-nob-title" style="padding-top:0;background:var(--pct-paper)">
  <div class="pct-wrap pct-grid-2" style="align-items:center">
    <div class="pct-col-7">${figure('nobility-books', 'Nobility swatch books open on a table', F.bookCaption, 'pct-ratio-16x9', { sizes: '(max-width: 767px) 100vw, 58vw' })}</div>
    <div class="pct-col-5"><h2 class="pct-h2" id="pct-nob-title">${esc(F.shopTitle)}</h2><p class="pct-lead" style="margin-top:20px">${esc(F.shopBody)}</p><div style="margin-top:28px"><a class="pct-link" href="${pagePath(lang, 'shop')}">${esc(F.shopLink)}</a></div></div>
  </div>
</section>
<section class="pct-section pct-section--white" aria-labelledby="pct-climate-title">
  <div class="pct-wrap">
    <h2 class="pct-h2" id="pct-climate-title" style="margin-bottom:40px">${esc(F.climateTitle)}</h2>
    <div class="pct-grid-2">
      ${F.climate.map((c, i) => `<div class="pct-col-6">${figure(i ? 'stock-wool-texture-1' : 'stock-linen-2', i ? 'Folded navy check and grey wool suitings' : 'Close-up of natural linen cloth', '', 'pct-ratio-3x2', { sizes: '(max-width: 767px) 100vw, 50vw' })}<h3 class="pct-h3" style="margin:22px 0 10px">${esc(c.title)}</h3><p>${esc(c.body)}</p></div>`).join('')}
    </div>
  </div>
</section>
<section class="pct-section" aria-labelledby="pct-trims-title">
  <div class="pct-wrap pct-grid-2" style="align-items:center">
    <div class="pct-col-6"><h2 class="pct-h2" id="pct-trims-title">${esc(F.trimsTitle)}</h2><p class="pct-lead" style="margin-top:20px">${esc(F.trimsBody)}</p></div>
    <div class="pct-col-6">${figure('stock-hero-workroom-3', 'Choosing horn buttons against a suiting swatch card', '', 'pct-ratio-4x5', { sizes: '(max-width: 767px) 100vw, 50vw' })}</div>
  </div>
</section>`;
  return { body, jsonld: [breadcrumbLD(ctx, [{ name: T.nav.fabrics, href: pagePath(lang, 'fabrics') }])] };
}

// --- Shop ---
const pName = (p, lang) => p.pct_i18n?.[lang]?.name || p.name;
const pField = (p, lang, f) => p.pct_i18n?.[lang]?.[f] || p[f] || '';
const pPrice = (p) => Number(p.prices?.price || 0) / 10 ** (p.prices?.currency_minor_unit || 0);
const term = (group, slug, name, lang) => SAMPLE.terms[group]?.[slug]?.[lang] || name;
const attr = (p, name) => (p.attributes || []).find((a) => a.name === name);
function priceLabel(p, ctx) {
  return p.sample || !pPrice(p) ? `<span>${esc(ctx.T.ui.samplePrice)}</span>` : fmtPrice(pPrice(p), ctx.lang);
}
function productCard(ctx, p, products = [], eagerImg = false) {
  const { lang, T } = ctx;
  const cat = p.categories?.[0];
  const colour = attr(p, 'Colour')?.terms?.[0]?.slug || '';
  return `<li class="pct-product-card" data-pct-product data-cat="${esc(cat?.slug || '')}" data-colour="${esc(colour)}" data-price="${pPrice(p)}" data-date="${esc(p.date_created || '')}" data-index="${products.indexOf(p)}">
    <a href="${pathFor(lang, `shop/${p.slug}`)}" data-pct-cursor="view">
      ${p.images?.[0] ? `<figure class="pct-figure">${productImg(p.images[0], { sizes: '(max-width: 767px) 50vw, 25vw', eager: eagerImg })}</figure>` : ''}
      <p class="pct-product-card__cat">${esc(term('categories', cat?.slug, cat?.name, lang))}</p>
      <h3>${esc(pName(p, lang))}</h3>
      <p class="pct-product-card__price">${priceLabel(p, ctx)}</p>
      ${p.sample ? `<span class="pct-product-card__sample">${esc(T.ui.sampleNote)}</span>` : ''}
    </a>
  </li>`;
}
function pageShop(ctx, products) {
  const { lang, T } = ctx;
  const S = T.shop;
  const cats = [...new Map(products.flatMap((p) => p.categories || []).map((c) => [c.slug, c])).values()];
  const colours = [...new Map(products.flatMap((p) => attr(p, 'Colour')?.terms || []).map((t) => [t.slug, t])).values()];
  const radio = (name, value, label, checked) => `<label class="pct-radio"><input type="radio" name="${name}" value="${value}"${checked ? ' checked' : ''}> ${esc(label)}</label>`;
  const anySample = products.some((p) => p.sample);
  const body = `
${pageHead(ctx, 'shop', { kicker: S.kicker, title: S.title, sub: S.sub })}
<section class="pct-section" style="padding-top:0" aria-label="${esc(S.title)}">
  <div class="pct-wrap">
    ${anySample ? `<p class="pct-shop-note">${esc(S.proposalNote)}</p>` : ''}
    <div class="pct-shop" data-pct-shop>
      <form class="pct-filters" id="pct-filters" data-pct-filters aria-label="${esc(S.filterTitle)}">
        <div class="pct-filters__head"><h2 class="pct-h3">${esc(S.filterTitle)}</h2><button type="button" class="pct-link" data-pct-filters-close>${esc(T.ui.close)}</button></div>
        <fieldset class="pct-filters__group"><legend>${esc(S.category)}</legend>
          ${radio('cat', '', S.all, true)}${cats.map((c) => radio('cat', c.slug, term('categories', c.slug, c.name, lang))).join('')}
        </fieldset>
        <fieldset class="pct-filters__group"><legend>${esc(S.colour)}</legend>
          ${radio('colour', '', S.all, true)}${colours.map((c) => radio('colour', c.slug, term('colours', c.slug, c.name, lang))).join('')}
        </fieldset>
        <fieldset class="pct-filters__group"><legend>${esc(S.price)}</legend>
          ${radio('price', '', S.anyPrice, true)}${radio('price', '0-3000000', S.under3)}${radio('price', '3000000-6000000', S['3to6'])}${radio('price', '6000000-', S.over6)}
        </fieldset>
        <div class="pct-filters__group pct-filters__apply"><button type="button" class="pct-btn pct-btn--block" data-pct-filters-close>${esc(S.apply)}</button></div>
        <div class="pct-filters__group"><button type="reset" class="pct-link">${esc(S.clear)}</button></div>
      </form>
      <div>
        <div class="pct-shop__bar">
          <span data-pct-count data-template="${esc(S.count)}">${esc(fill(S.count, { n: products.length }))}</span>
          <span style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">
            <button type="button" class="pct-btn pct-btn--ghost pct-filter-btn" data-pct-filters-open aria-controls="pct-filters" aria-expanded="false" style="min-height:44px;padding:8px 16px">${esc(S.filterTitle)}</button>
            <label>${esc(S.sort)} <select class="pct-select" data-pct-sort form="pct-filters" name="sort">
              <option value="featured">${esc(S.sortFeatured)}</option><option value="newest">${esc(S.sortNewest)}</option><option value="price-asc">${esc(S.sortPriceAsc)}</option><option value="price-desc">${esc(S.sortPriceDesc)}</option>
            </select></label>
          </span>
        </div>
        <ul class="pct-products" data-pct-products>${products.map((p) => productCard(ctx, p, products)).join('')}</ul>
        <p class="pct-empty" data-pct-empty hidden>${esc(S.empty)}</p>
      </div>
    </div>
  </div>
</section>`;
  return { body, tryon: true, jsonld: [breadcrumbLD(ctx, [{ name: T.nav.shop, href: pagePath(lang, 'shop') }])] };
}
function pageProduct(ctx, p, products) {
  const { lang, T } = ctx;
  const name = pName(p, lang);
  const cat = p.categories?.[0];
  const isFabric = cat?.slug === 'nobility-fabrics';
  const related = products.filter((x) => x.id !== p.id && x.categories?.[0]?.slug === cat?.slug).slice(0, 3);
  const live = config.shop.checkoutEnabled && !p.sample;
  const bagHref = live ? `${config.shop.wooBase}/cart/?add-to-cart=${p.id}` : wa(fill(T.ui.waProduct, { name }));
  const attrs = (p.attributes || []).map((a) => `<div><dt>${esc(SAMPLE.terms.attributes[a.name]?.[lang] || a.name)}</dt><dd>${esc(a.terms.map((t) => (a.name === 'Colour' ? term('colours', t.slug, t.name, lang) : t.name)).join(', '))}</dd></div>`).join('');
  const body = `
<section class="pct-section" style="padding-top:clamp(40px,6vw,80px)">
  <div class="pct-wrap">
    ${crumbs(ctx, [{ name: T.nav.shop, href: pagePath(lang, 'shop') }, { name, href: pathFor(lang, `shop/${p.slug}`) }])}
    <div class="pct-pdp">
      <div class="pct-pdp__gallery">${(p.images || []).map((im, i) => productImg(im, { eager: i === 0, sizes: '(max-width: 1024px) 100vw, 58vw' })).join('')}</div>
      <div class="pct-pdp__info">
        <p class="pct-meta">${esc(term('categories', cat?.slug, cat?.name, lang))}</p>
        <h1 class="pct-h2" style="margin-top:12px">${esc(name)}</h1>
        <p class="pct-pdp__price">${priceLabel(p, ctx)}</p>
        ${p.sample ? `<p class="pct-product-card__sample">${esc(T.ui.sampleNote)}</p><!-- PLACEHOLDER: sample product for the proposal -->` : ''}
        <div class="pct-pdp__desc">${pField(p, lang, 'short_description')}${pField(p, lang, 'description')}</div>
        <div class="pct-pdp__actions">
          <a class="pct-btn pct-btn--block" href="${esc(bagHref)}" ${live ? '' : 'target="_blank" rel="noopener"'} data-pct-bag data-pct-live="${live}" data-pct-track="add_to_bag" data-pct-product-name="${esc(p.name)}">${esc(T.ui.addToBag)}</a>
          ${live ? '' : `<p class="pct-pdp__msg" data-pct-bag-msg hidden>${esc(T.ui.checkoutPending)}</p>`}
          ${isFabric ? `<a class="pct-btn pct-btn--ghost pct-btn--block" href="${wa(fill(T.ui.waFabric, { name }))}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="product_make_suit">${ICON.whatsapp}${esc(T.ui.askMakeSuit)}</a>` : `<a class="pct-btn pct-btn--ghost pct-btn--block" href="${wa(fill(T.ui.waProduct, { name }))}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="product">${ICON.whatsapp}${esc(T.ui.whatsapp)}</a>`}
        </div>
        ${attrs ? `<dl class="pct-pdp__attrs">${attrs}</dl>` : ''}
      </div>
    </div>
  </div>
</section>
${related.length ? `<section class="pct-section pct-section--white" aria-labelledby="pct-related-title"><div class="pct-wrap"><h2 class="pct-h2" id="pct-related-title" style="margin-bottom:36px">${esc(T.ui.related)}</h2><ul class="pct-products">${related.map((r) => productCard(ctx, r)).join('')}</ul><div style="margin-top:36px"><a class="pct-link" href="${pagePath(lang, 'shop')}">${esc(T.ui.backToShop)}</a></div></div></section>` : ''}`;
  const ld = {
    '@context': 'https://schema.org', '@type': 'Product', name, description: pField(p, lang, 'short_description').replace(/<[^>]+>/g, ''),
    image: (p.images || []).map((im) => (im.src.startsWith('img:') ? abs(`/assets/img/${im.src.slice(4)}.webp`) : im.src)),
    brand: { '@type': 'Brand', name: attr(p, 'Brand')?.terms?.[0]?.name || 'Nobility' },
    ...(pPrice(p) && !p.sample ? { offers: { '@type': 'Offer', price: pPrice(p), priceCurrency: 'VND', availability: p.is_in_stock ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock', url: abs(pathFor(lang, `shop/${p.slug}`)) } } : {}),
  };
  return { body, tryon: true, title: seoTitle(name), description: pField(p, lang, 'short_description').replace(/<[^>]+>/g, '').slice(0, 155), jsonld: [ld, breadcrumbLD(ctx, [{ name: T.nav.shop, href: pagePath(lang, 'shop') }, { name, href: pathFor(lang, `shop/${p.slug}`) }])], ogImage: p.images?.[0]?.src };
}

// --- Journal ---
function pageJournal(ctx) {
  const { lang, T } = ctx;
  const J = T.journal;
  const [lead, ...rest] = JOURNAL;
  const [key, alt] = COVERS[lead.slug];
  const body = `
${pageHead(ctx, 'journal', { kicker: J.kicker, title: J.title, sub: J.sub })}
<section class="pct-section" style="padding-top:0">
  <div class="pct-wrap">
    <article class="pct-post-lead">
      <a href="${pathFor(lang, `journal/${lead.slug}`)}" tabindex="-1" aria-hidden="true" data-pct-cursor="read">${figure(key, alt, '', 'pct-ratio-3x2', { sizes: '(max-width: 767px) 100vw, 58vw', eager: true })}</a>
      <div>
        <p class="pct-small">${fmtDate(lead.date, lang)}, ${esc(fill(T.ui.minRead, { n: lead.minutes[lang] }))}</p>
        <h2 class="pct-h2"><a href="${pathFor(lang, `journal/${lead.slug}`)}">${esc(lead.title[lang])}</a></h2>
        <p class="pct-lead">${esc(lead.excerpt[lang])}</p>
        <div style="margin-top:24px"><a class="pct-link" href="${pathFor(lang, `journal/${lead.slug}`)}">${esc(T.ui.readArticle)}</a></div>
      </div>
    </article>
    <div class="pct-postlist pct-postlist--two pct-postlist--all">${rest.map((p) => postCard(ctx, p, { sizes: '(max-width: 767px) 100vw, 50vw' })).join('')}</div>
  </div>
</section>`;
  return { body, jsonld: [breadcrumbLD(ctx, [{ name: T.nav.journal, href: pagePath(lang, 'journal') }])] };
}
function pagePost(ctx, post) {
  const { lang, T } = ctx;
  const title = post.title[lang];
  const [key, alt] = COVERS[post.slug];
  const author = AUTHORS[post.author][lang];
  const html = post.html[lang].replace(/<table>/g, '<div class="pct-table-scroll"><table>').replace(/<\/table>/g, '</table></div>');
  const video = post.youtube.map((id) => `<a class="pct-video" href="https://www.youtube.com/watch?v=${id}" target="_blank" rel="noopener" data-pct-video="${id}"><img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><span class="pct-video__play">${ICON.play}<span>${esc(T.ui.watchVideo)}</span><span class="pct-sr">(${esc(T.ui.videoNote)})</span></span></a>`).join('');
  const related = JOURNAL.filter((p) => p.slug !== post.slug).slice(0, 2);
  const body = `
<article>
  <header class="pct-article__head">
    <div class="pct-wrap pct-wrap--narrow">
      ${crumbs(ctx, [{ name: T.nav.journal, href: pagePath(lang, 'journal') }, { name: title, href: pathFor(lang, `journal/${post.slug}`) }])}
      <h1 class="pct-h1" style="font-size:clamp(38px,5vw,68px)">${esc(title)}</h1>
      <p class="pct-article__meta"><span>${esc(T.ui.by)} ${esc(author)}</span><time datetime="${post.date}">${fmtDate(post.date, lang)}</time><span>${esc(fill(T.ui.minRead, { n: post.minutes[lang] }))}</span></p>
    </div>
  </header>
  <div class="pct-wrap"><div class="pct-article__cover">${figure(key, alt, '', '', { eager: true, sizes: '(max-width: 1280px) 100vw, 1280px' })}</div></div>
  <div class="pct-article__body">
    <div class="pct-wrap">
      <div class="pct-rte">${html}${video ? `<div>${video}</div>` : ''}</div>
    </div>
  </div>
</article>
<section class="pct-section pct-section--white" aria-labelledby="pct-more-title">
  <div class="pct-wrap">
    <div class="pct-section-head"><h2 class="pct-h2" id="pct-more-title">${esc(T.journal.relatedTitle)}</h2><div><a class="pct-link" href="${pagePath(lang, 'journal')}">${esc(T.ui.backToJournal)}</a></div></div>
    <div class="pct-postlist pct-postlist--two">${related.map((p) => postCard(ctx, p, { sizes: '(max-width: 767px) 100vw, 50vw' })).join('')}</div>
  </div>
</section>`;
  const ld = {
    '@context': 'https://schema.org', '@type': 'BlogPosting', headline: title, datePublished: post.date, inLanguage: T.htmlLang,
    author: { '@type': post.author === 'team' ? 'Organization' : 'Person', name: AUTHORS[post.author].en },
    publisher: { '@type': 'Organization', name: "Phan's Custom Tailor", logo: { '@type': 'ImageObject', url: abs('/assets/brand/logo.png') } },
    image: abs(`/assets/img/${key}.webp`), mainEntityOfPage: abs(pathFor(lang, `journal/${post.slug}`)),
  };
  return { body, title: seoTitle(title), description: post.excerpt[lang], jsonld: [ld, breadcrumbLD(ctx, [{ name: T.nav.journal, href: pagePath(lang, 'journal') }, { name: title, href: pathFor(lang, `journal/${post.slug}`) }])], ogImage: `img:${key}`, ogType: 'article' };
}

function pageFaq(ctx) {
  const { lang, T } = ctx;
  const F = T.faq;
  const body = `
${pageHead(ctx, 'faq', { kicker: F.kicker, title: F.title, sub: F.sub, aside: visitAside(T) })}
<section class="pct-section" style="padding-top:0">
  <div class="pct-wrap pct-grid-2">
    <div class="pct-col-8 pct-faq">
      ${F.groups.map((g, gi) => `<div class="pct-faq-group"><h2 class="pct-h3">${esc(g.title)}</h2>${g.items.map((it, i) => `<details${gi === 0 && i === 0 ? ' open' : ''}><summary>${esc(it.q)}${ICON.plus}</summary><div class="pct-faq__a"><p>${esc(it.a)}</p>${gi === 2 && i >= 1 ? '<!-- CONFIRM: new FAQ answer, check with the client -->' : ''}</div></details>`).join('')}</div>`).join('')}
    </div>
    <aside class="pct-col-4" style="position:sticky;top:calc(var(--pct-header-h) + 32px)">
      ${figure('stock-fitting-2', 'Client trying on a jacket at a fitting', '', 'pct-ratio-4x5', { sizes: '(max-width: 767px) 100vw, 33vw' })}
      <div class="pct-btns" style="margin-top:24px;flex-direction:column">
        <a class="pct-btn pct-btn--block" href="${config.contact.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="faq">${esc(T.ui.book)}</a>
        <a class="pct-btn pct-btn--ghost pct-btn--block" href="${wa(T.ui.waGeneral)}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="faq">${ICON.whatsapp}${esc(T.ui.whatsapp)}</a>
      </div>
    </aside>
  </div>
</section>`;
  const ld = { '@context': 'https://schema.org', '@type': 'FAQPage', inLanguage: T.htmlLang, mainEntity: F.groups.flatMap((g) => g.items).map((it) => ({ '@type': 'Question', name: it.q, acceptedAnswer: { '@type': 'Answer', text: it.a } })) };
  return { body, jsonld: [ld, breadcrumbLD(ctx, [{ name: T.nav.faq, href: pagePath(lang, 'faq') }])] };
}

function enquiryForm(ctx) {
  const { lang, T } = ctx;
  const F = T.form;
  const email = config.forms.formsubmitEmail;
  return `
<form class="pct-form" action="https://formsubmit.co/${email}" method="POST" novalidate data-pct-form data-ajax="https://formsubmit.co/ajax/${email}" data-err-send="${esc(F.errSend)}" data-sending="${esc(F.sending)}" data-thanks="${pagePath(lang, 'thanks')}">
  <input type="hidden" name="_subject" value="${esc(F.subject)}">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_next" value="${abs(pagePath(lang, 'thanks'))}">
  <input type="hidden" name="language" value="${esc(T.label)}">
  <input type="text" name="_honey" class="pct-honey" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="pct-field">
    <label for="pct-name">${esc(F.name)}</label>
    <input class="pct-input" id="pct-name" name="name" type="text" autocomplete="name" required data-err="${esc(F.errName)}" aria-describedby="pct-name-err">
    <p class="pct-error" id="pct-name-err" hidden></p>
  </div>
  <div class="pct-field">
    <label for="pct-email">${esc(F.email)}</label>
    <input class="pct-input" id="pct-email" name="email" type="email" autocomplete="email" required data-err="${esc(F.errEmail)}" aria-describedby="pct-email-err">
    <p class="pct-error" id="pct-email-err" hidden></p>
  </div>
  <div class="pct-field">
    <label for="pct-phone">${esc(F.phone)} <span>(${esc(F.optional)})</span></label>
    <input class="pct-input" id="pct-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" data-err="${esc(F.errPhone)}" data-pct-phone aria-describedby="pct-phone-hint pct-phone-err">
    <p class="pct-hint" id="pct-phone-hint">${esc(F.phoneHint)}</p>
    <p class="pct-error" id="pct-phone-err" hidden></p>
  </div>
  <div class="pct-field">
    <label for="pct-country">${esc(F.country)} <span>(${esc(F.optional)})</span></label>
    <input class="pct-input" id="pct-country" name="country" type="text" autocomplete="country-name">
  </div>
  <div class="pct-field pct-field--full">
    <fieldset><legend>${esc(F.garments)} <span>(${esc(F.optional)})</span></legend>
      <div class="pct-checks">${F.garmentOptions.map((g, i) => `<label class="pct-check"><input type="checkbox" name="garments" value="${esc(I18N.en.form.garmentOptions[i])}"><span>${esc(g)}</span></label>`).join('')}</div>
    </fieldset>
  </div>
  <div class="pct-field pct-field--full">
    <fieldset><legend>${esc(F.dates)} <span>(${esc(F.optional)})</span></legend>
      <div class="pct-dates">
        <div class="pct-field"><label for="pct-arrive">${esc(F.arrive)}</label><input class="pct-input" id="pct-arrive" name="arrive" type="date"></div>
        <div class="pct-field"><label for="pct-leave">${esc(F.leave)}</label><input class="pct-input" id="pct-leave" name="leave" type="date" data-err="${esc(F.errDates)}" aria-describedby="pct-leave-err"></div>
      </div>
      <p class="pct-error" id="pct-leave-err" hidden></p>
    </fieldset>
  </div>
  <div class="pct-field pct-field--full">
    <label for="pct-message">${esc(F.message)}</label>
    <textarea class="pct-input" id="pct-message" name="message" required data-err="${esc(F.errMessage)}" aria-describedby="pct-message-err"></textarea>
    <p class="pct-error" id="pct-message-err" hidden></p>
  </div>
  <div class="pct-form-status" role="status" aria-live="polite" data-pct-status></div>
  <div class="pct-form__foot">
    <button class="pct-btn" type="submit">${esc(F.submit)}</button>
    <p class="pct-form__alt">${esc(F.chatInstead)} <a href="${wa(T.ui.waGeneral)}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="form">${esc(T.ui.whatsapp)}</a> / <a href="${config.contact.zalo}" target="_blank" rel="noopener" data-pct-track="zalo_click">${esc(T.ui.zalo)}</a></p>
  </div>
</form>`;
}

function pageContact(ctx) {
  const { lang, T } = ctx;
  const C = T.contact;
  const c = config.contact;
  const body = `
${pageHead(ctx, 'contact', { kicker: C.kicker, title: C.title, sub: C.sub })}
<section class="pct-section" style="padding-top:0">
  <div class="pct-wrap">
    <div class="pct-contact-grid">
      <div>
        <h2>${esc(C.bookTitle)}</h2><p>${esc(C.bookBody)}</p>
        <div class="pct-btns"><a class="pct-btn" href="${c.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="contact">${ICON.calendar}${esc(T.ui.book)}</a></div>
      </div>
      <div>
        <h2>${esc(C.chatTitle)}</h2><p>${esc(C.chatBody)}</p>
        <div class="pct-contact-list">
          <a href="${wa(T.ui.waGeneral)}" target="_blank" rel="noopener" data-pct-track="whatsapp_click" data-pct-where="contact">${ICON.whatsapp}WhatsApp</a>
          <a href="${c.zalo}" target="_blank" rel="noopener" data-pct-track="zalo_click">${ICON.zalo}Zalo</a>
          <a href="${c.messenger}" target="_blank" rel="noopener">${ICON.messenger}Messenger</a>
        </div>
      </div>
      <div>
        <h2>${esc(C.directTitle)}</h2>
        <div class="pct-contact-list">
          <a href="${c.phoneHref}" data-pct-track="call_click">${ICON.phone}${esc(c.phoneDisplay)}</a>
          <a href="mailto:${c.email}" data-pct-track="email_click">${ICON.mail}${esc(c.email)}</a>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="pct-section pct-section--white" aria-label="${esc(C.visitTitle)}">
  <div class="pct-wrap pct-visit">
    <dl>
      <div><dt>${esc(C.visitTitle)}</dt><dd><address style="font-style:normal">${T.footer.address.map(esc).join('<br>')}</address><a class="pct-text-link" href="${c.maps}" target="_blank" rel="noopener">${esc(T.ui.getDirections)}</a></dd></div>
      <div><dt>${esc(C.hoursTitle)}</dt><dd>${esc(T.footer.hours)}<br>${esc(T.footer.hoursNote)}</dd></div>
      <div><dt>${esc(C.parkingTitle)}</dt><dd>${esc(C.parkingBody)}</dd></div>
      <div class="pct-notice"><dt>${esc(C.holidayTitle)}</dt><dd>${esc(C.holidayBody)}<!-- CONFIRM: Tết closure dates --></dd></div>
    </dl>
    <iframe class="pct-map" src="${c.mapsEmbed}" title="${esc(C.mapTitle)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
</section>
<section class="pct-section" id="pct-enquiry" aria-labelledby="pct-form-title">
  <div class="pct-wrap pct-grid-2">
    <div class="pct-col-4"><h2 class="pct-h2" id="pct-form-title">${esc(C.formTitle)}</h2><p class="pct-lead" style="margin-top:20px">${esc(C.formIntro)}</p></div>
    <div class="pct-col-8">${enquiryForm(ctx)}</div>
  </div>
</section>`;
  return { body, noBand: true, jsonld: [breadcrumbLD(ctx, [{ name: T.nav.contact, href: pagePath(lang, 'contact') }])] };
}

function pageThanks(ctx) {
  const { lang, T } = ctx;
  const body = `
<section class="pct-section pct-404">
  <div class="pct-wrap pct-wrap--narrow">
    <h1 class="pct-h1" style="font-size:clamp(40px,5vw,72px)">${esc(T.thanks.title)}</h1>
    <p class="pct-lead" style="margin-top:24px">${esc(T.thanks.body)}</p>
    <div class="pct-btns" style="margin-top:32px">
      <a class="pct-btn" href="${config.contact.booking}" target="_blank" rel="noopener" data-pct-track="book_click" data-pct-where="thank_you">${esc(T.ui.book)}</a>
      <a class="pct-btn pct-btn--ghost" href="${pathFor(lang)}">${esc(T.thanks.back)}</a>
    </div>
  </div>
</section>`;
  return { body, noBand: true, robots: 'noindex, follow' };
}

function page404(ctx) {
  const { lang, T } = ctx;
  const body = `
<section class="pct-section pct-404">
  <div class="pct-wrap pct-wrap--narrow">
    <h1 class="pct-h1" style="font-size:clamp(40px,5vw,72px)">${esc(T.notFound.title)}</h1>
    <p class="pct-lead" style="margin-top:24px">${esc(T.notFound.body)}</p>
    <ul>${['process', 'pricing', 'fabrics', 'journal', 'contact'].map((k) => `<li><a class="pct-link" href="${pagePath(lang, k)}">${esc(T.nav[k])}</a></li>`).join('')}</ul>
    <div class="pct-btns" style="margin-top:36px"><a class="pct-btn" href="${config.contact.booking}" target="_blank" rel="noopener">${esc(T.ui.book)}</a><a class="pct-btn pct-btn--ghost" href="${pathFor(lang)}">${esc(T.nav.home)}</a></div>
  </div>
</section>`;
  return { body, noBand: true, robots: 'noindex, follow' };
}

// ---------------------------------------------------------------------------
// Document shell
// ---------------------------------------------------------------------------
const FONTS = {
  latin: 'https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600&family=Prata&display=swap',
};
let ASSET_V = '';

function documentHTML(ctx, page) {
  const { lang, T, alt, current, pathname } = ctx;
  const title = page.title || T.pages[current]?.title;
  const description = page.description || T.pages[current]?.description;
  const robots = !config.indexable ? 'noindex, nofollow' : page.robots || 'index, follow';
  let og = page.ogImage ? (page.ogImage.startsWith('img:') ? abs(`/assets/img/${page.ogImage.slice(4)}.webp`) : page.ogImage) : abs('/assets/share.jpg');
  const ld = (page.jsonld || []).map((j) => `<script type="application/ld+json">${JSON.stringify(j).replace(/</g, '\\u003c')}</script>`).join('\n');
  return `<!doctype html>
<html lang="${T.htmlLang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}">
<meta name="robots" content="${robots}">
<link rel="canonical" href="${abs(pathname)}">
${page.noAlternates ? '' : LANGS.map((l) => `<link rel="alternate" hreflang="${I18N[l].htmlLang}" href="${abs(alt[l])}">`).join('\n') + `\n<link rel="alternate" hreflang="x-default" href="${abs(alt.en)}">`}
<meta property="og:type" content="${page.ogType || 'website'}">
<meta property="og:site_name" content="Phan's Custom Tailor">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:url" content="${abs(pathname)}">
<meta property="og:image" content="${og}">
<meta property="og:locale" content="${{ en: 'en_US', vi: 'vi_VN', zh: 'zh_CN' }[lang]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(title)}">
<meta name="twitter:description" content="${esc(description)}">
<meta name="twitter:image" content="${og}">
<meta name="theme-color" content="#f7f6f3">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/brand/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
${page.preload || ''}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="${FONTS.latin}">
<link rel="stylesheet" href="/assets/css/site.css?v=${ASSET_V}">
<link rel="preload" as="script" href="/assets/js/site.js?v=${ASSET_V}">
<link rel="preload" as="script" href="/assets/vendor/gsap.min.js?v=3.13.0">
<link rel="preload" as="script" href="/assets/vendor/SplitText.min.js?v=3.13.0">
<link rel="preload" as="script" href="/assets/js/motion.js?v=${ASSET_V}">
<link rel="preload" as="script" href="/assets/vendor/ScrollTrigger.min.js?v=3.13.0">
${ld}
</head>
<body class="pct-root pct-lang-${lang}" data-pct-lang-code="${lang}" data-pct-three="/assets/vendor/three.module.min.js" data-pct-cursor-view="${esc(T.ui.cursorView)}" data-pct-cursor-read="${esc(T.ui.cursorRead)}">
<script>(function(b){b.classList.add('pct-js');var rm=window.matchMedia('(prefers-reduced-motion: reduce)').matches;try{if(sessionStorage.getItem('pct-transition')){sessionStorage.removeItem('pct-transition');if(!rm)b.classList.add('pct-arrive');}}catch(e){}if(!rm){b.classList.add('pct-anim');setTimeout(function(){b.classList.add('pct-anim-done');},4000);}})(document.body)</script>
<a class="pct-skip" href="#pct-main">${esc(T.ui.skip)}</a>
${header(ctx)}
<main id="pct-main" tabindex="-1">
${page.body}
${page.noBand ? '' : bookBand(ctx)}
</main>
${footer(ctx)}
<script src="/assets/js/site.js?v=${ASSET_V}" defer></script>
<script src="/assets/vendor/gsap.min.js?v=3.13.0" defer></script>
<script src="/assets/vendor/ScrollTrigger.min.js?v=3.13.0" defer></script>
<script src="/assets/vendor/SplitText.min.js?v=3.13.0" defer></script>
<script src="/assets/js/motion.js?v=${ASSET_V}" defer></script>
${page.scripts || ''}
${page.tryon ? '<script src="https://anywear.decart.ai/widget/latest/anywear.js?domain=phans-custom-tailor-demo.vercel.app" async></script>' : ''}
</body>
</html>
`;
}

// ---------------------------------------------------------------------------
// Build
// ---------------------------------------------------------------------------
function write(rel, content) {
  const file = path.join(DIST, rel);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content);
}
function copyDir(from, to) {
  if (!fs.existsSync(from)) return;
  fs.mkdirSync(to, { recursive: true });
  for (const f of fs.readdirSync(from)) {
    const s = path.join(from, f); const d = path.join(to, f);
    if (fs.statSync(s).isDirectory()) copyDir(s, d); else fs.copyFileSync(s, d);
  }
}

// Old Haravan URLs -> new pages (section 8.5 of the brief).
function redirects(products) {
  const r = [
    ['/pages/about-us', '/about/'],
    ['/pages/working-hours-appointments', '/book-an-appointment/'],
    ['/pages/lien-he', '/contact/'],
    ['/pages/frequently-asked-questions-faqs', '/faq/'],
    ['/pages/frequently-asked-questions-faqs-1', '/faq/'],
    ['/pages/testimonials', '/#reviews'],
    ['/pages/your-appointment-is-confirmed', '/contact/'],
    ['/pages/the-bespoke-dress-shirt', '/suits-and-pricing/'],
    ['/pages/fabric-collection', '/fabrics/'],
    ['/pages/vai-thuong-hieu-nobility', '/vi/fabrics/'],
    ['/pages/frontpage', '/'],
    ['/pages/chinh-sach-doi-tra', '/faq/'],
    ['/pages/chinh-sach-bao-mat', '/contact/'],
    ['/pages/dieu-khoan-dich-vu', '/contact/'],
    ['/pages/nghe-thuat-bespoke-che-tac-bo-suit-2-manh-hoan-hao-cua-rieng-ban', '/vi/journal/the-art-of-bespoke-crafting-your-perfect-2-piece-suit/'],
    ['/pages/5-classic-suit-mistakes-how-to-fix-them-like-an-expert', '/journal/5-classic-suit-mistakes-how-to-fix-them-like-an-expert/'],
    ['/pages/summer-suiting-2025', '/journal/summer-suiting-2025/'],
    ['/collections/all', '/shop/'],
    ['/collections/hot-products', '/shop/'],
    ['/collections/2-piece-suit', '/shop/'],
    ['/collections/onsale', '/shop/'],
    ['/collections/frontpage', '/shop/'],
    ['/collections/lining-fabric', '/fabrics/'],
    ['/blogs/news', '/journal/'],
    ['/account/login', '/shop/'],
    ['/account/register', '/shop/'],
    ['/account', '/shop/'],
    ['/cart', '/shop/'],
    ['/search', '/'],
  ];
  for (const p of JOURNAL) r.push([`/blogs/news/${p.slug}`, `/journal/${p.slug}/`]);
  for (const p of products) if (!p.sample) r.push([`/products/${p.slug}`, `/shop/${p.slug}/`]);
  return r;
}

function hostingFiles(r) {
  const vercel = {
    trailingSlash: true,
    cleanUrls: false,
    // trailingSlash adds the slash before redirects run, so match both forms
    redirects: r.flatMap(([source, destination]) => [{ source, destination, permanent: true }, { source: source + '/', destination, permanent: true }]),
    headers: [
      { source: '/assets/(.*)', headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }] },
      ...(config.indexable ? [] : [{ source: '/(.*)', headers: [{ key: 'X-Robots-Tag', value: 'noindex, nofollow' }] }]),
    ],
  };
  write('vercel.json', JSON.stringify(vercel, null, 2));
  // Root vercel.json for Git deployments: Vercel runs the build and serves dist/
  fs.writeFileSync(path.join(ROOT, 'vercel.json'), JSON.stringify({ buildCommand: 'node build.mjs', outputDirectory: 'dist', framework: null, functions: { 'api/suit.js': { includeFiles: '{assets/img/cfg/**,src/data/configurator.json,src/js/suit-svg.mjs}' }, 'api/booking.js': { includeFiles: 'src/config.json' } }, ...vercel }, null, 2) + '\n');
  write('.vercelignore', '_hosting\n.env*\n.gitignore\n');
  const htaccess = ['# Phan\'s Custom Tailor: Apache rules (copy to the web root as .htaccess)', 'ErrorDocument 404 /404.html', 'RewriteEngine On',
    ...r.map(([s, d]) => `RedirectMatch 301 ^${s.replace(/[.]/g, '\\.')}/?$ ${d}`),
    '<IfModule mod_expires.c>', '  ExpiresActive On', '  ExpiresByType image/webp "access plus 1 year"', '  ExpiresByType text/css "access plus 1 year"', '  ExpiresByType application/javascript "access plus 1 year"', '</IfModule>',
    ...(config.indexable ? [] : ['Header set X-Robots-Tag "noindex, nofollow"'])].join('\n');
  write('_hosting/.htaccess', htaccess + '\n');
  const nginx = ['# Phan\'s Custom Tailor: nginx rules (include inside the server block)', 'error_page 404 /404.html;',
    ...r.map(([s, d]) => `location ~ ^${s.replace(/[.]/g, '\\.')}/?$ { return 301 ${d}; }`),
    'location /assets/ { expires 1y; add_header Cache-Control "public, immutable"; }'].join('\n');
  write('_hosting/nginx-redirects.conf', nginx + '\n');
}

async function main() {
  // Clear dist/ but keep Vercel's project link (dist/.vercel) so redeploys go to the same project
  if (fs.existsSync(DIST)) for (const f of fs.readdirSync(DIST)) if (f !== '.vercel') fs.rmSync(path.join(DIST, f), { recursive: true, force: true });
  const products = await loadProducts();

  // Assets
  const css = fs.readFileSync(path.join(SRC, 'styles/site.css'), 'utf8');
  const js = fs.readFileSync(path.join(SRC, 'js/site.js'), 'utf8');
  const motion = fs.readFileSync(path.join(SRC, 'js/motion.js'), 'utf8');
  const suit = fs.readFileSync(path.join(SRC, 'js/suit-svg.mjs'), 'utf8');
  const cfgjs = fs.readFileSync(path.join(SRC, 'js/configurator.mjs'), 'utf8');
  const bookjs = fs.readFileSync(path.join(SRC, 'js/booking.mjs'), 'utf8');
  ASSET_V = crypto.createHash('md5').update(css + js + motion + suit + cfgjs + bookjs).digest('hex').slice(0, 8);
  write('assets/css/site.css', css);
  write('assets/js/site.js', js);
  write('assets/js/motion.js', motion);
  write('assets/js/suit-svg.mjs', suit);
  write('assets/js/booking.mjs', bookjs);
  write('assets/js/configurator.mjs', cfgjs.replace('./suit-svg.mjs', `./suit-svg.mjs?v=${ASSET_V}`));
  copyDir(path.join(SRC, 'vendor'), path.join(DIST, 'assets/vendor'));
  copyDir(path.join(ROOT, 'assets/img'), path.join(DIST, 'assets/img'));
  copyDir(path.join(ROOT, 'assets/brand-out'), path.join(DIST, 'assets/brand'));
  if (fs.existsSync(path.join(ROOT, 'assets/brand-out/favicon.ico'))) fs.copyFileSync(path.join(ROOT, 'assets/brand-out/favicon.ico'), path.join(DIST, 'favicon.ico'));
  if (fs.existsSync(path.join(ROOT, 'assets/share.jpg'))) fs.copyFileSync(path.join(ROOT, 'assets/share.jpg'), path.join(DIST, 'assets/share.jpg'));

  const PAGES = { home: pageHome, about: pageAbout, process: pageProcess, pricing: pagePricing, design: pageDesign, book: pageBook, fabrics: pageFabrics, journal: pageJournal, faq: pageFaq, contact: pageContact, thanks: pageThanks };
  const sitemap = [];
  let count = 0;
  for (const lang of LANGS) {
    const T = I18N[lang];
    const mk = (current, slug, extra = {}) => {
      const alt = Object.fromEntries(LANGS.map((l) => [l, pathFor(l, slug)]));
      return { lang, T, current, alt, pathname: pathFor(lang, slug), ...extra };
    };
    const emit = (ctx, page) => {
      const KOA = config.contact.booking, BK = pagePath(lang, 'book');
      const html = documentHTML(ctx, page).split(`${esc(T.ui.book)}<span class="pct-sr"> (${esc(T.ui.opensNewTab)})</span>`).join(esc(T.ui.book))
        .split(`href="${KOA}" target="_blank" rel="noopener"`).join(`href="${BK}"`).split(`href="${KOA}"`).join(`href="${BK}"`);
      write(path.join(ctx.pathname, 'index.html'), html);
      if (!page.robots) sitemap.push(ctx);
      count++;
    };
    for (const [key, fn] of Object.entries(PAGES)) { const ctx = mk(key, SLUGS[key].slug); emit(ctx, fn(ctx)); }
    { const ctx = mk('shop', SLUGS.shop.slug); emit(ctx, pageShop(ctx, products)); }
    for (const p of products) { const ctx = mk('shop', `shop/${p.slug}`); emit(ctx, pageProduct(ctx, p, products)); }
    for (const post of JOURNAL) { const ctx = mk('journal', `journal/${post.slug}`); emit(ctx, pagePost(ctx, post)); }
    // 404 per language (English one at the root is what hosts serve)
    const ctx404 = { ...mk('notFound', ''), pathname: pathFor(lang, '404') };
    const html404 = documentHTML(ctx404, { ...page404(ctx404), noAlternates: true });
    write(lang === 'en' ? '404.html' : `${lang}/404.html`, html404);
  }

  const r = redirects(products);
  hostingFiles(r);
  if (config.indexable) {
    write('robots.txt', `User-agent: *\nAllow: /\nSitemap: ${abs('/sitemap.xml')}\n`);
    const urls = sitemap.filter((c) => c.lang === 'en').map((c) => `  <url><loc>${abs(c.pathname)}</loc>${LANGS.map((l) => `<xhtml:link rel="alternate" hreflang="${I18N[l].htmlLang}" href="${abs(c.alt[l])}"/>`).join('')}</url>`);
    const others = sitemap.filter((c) => c.lang !== 'en').map((c) => `  <url><loc>${abs(c.pathname)}</loc></url>`);
    write('sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n${[...urls, ...others].join('\n')}\n</urlset>\n`);
  } else {
    write('robots.txt', 'User-agent: *\nDisallow: /\n');
  }
  console.log(`Built ${count} pages in ${LANGS.length} languages into dist/ (indexable: ${config.indexable}, products: ${config.shop.storeApiBase ? 'Store API' : 'sample data'}).`);
}

main().catch((e) => { console.error(e); process.exit(1); });
