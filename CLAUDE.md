# Phan's Custom Tailor — proposal website

## Overview
- Client (prospect): **Phan's Custom Tailor**, bespoke tailor in a private villa at 08 D9, Saigon Pearl, Bình Thạnh, Ho Chi Minh City. Founders Mr. Thinh Phan and Ms. Thuong Phan (architecture graduates). Current site: https://tailormadesuit.net (Haravan template). Contact/booking facts live in `src/config.json`.
- What: an unsolicited **proposal/pitch** — full revamp as a trilingual static site (English main at `/`, Vietnamese `/vi/`, Simplified Chinese `/zh/`), 72 pages, with a shop that will read products from a headless WooCommerce Store API later.
- Demo URL: **https://phans-custom-tailor-demo.vercel.app** (Vercel project `phans-custom-tailor-demo`, team `thewebxiteai-6218s-projects` (thewebxite.ai account); noindex while `indexable` is false). Plan: demo on Vercel, later point to TWX hosting; WordPress only for the WooCommerce API/checkout (`shop.tailormadesuit.net`, unconfirmed).
- Platform: dependency-free Node build (`build.mjs`) → static `dist/`. Self-hosted GSAP 3.13 (ScrollTrigger, SplitText) + three.js r170. Enquiry form via FormSubmit.
- Pitch materials sent to the owners via WhatsApp/Zalo: Vietnamese + English PDF decks in `pitch/`.

## Key files
- `phans-custom-tailor-claude-code-prompt.md` → original build brief (from the website-prompt-builder skill): business facts, truth rules, design direction, keyword map, sitemap, QA.
- `README.md` → how to build, preview, edit content, deploy to Vercel, launch on own hosting, connect WooCommerce, QA, motion, analytics events.
- `CONFIRM.md` → client questions, placeholders to replace before launch, stock photo list, assumptions.
- `COPY.md`, `COPY.vi.md`, `COPY.zh.md` → copy decks generated from `src/i18n/*.json` by `scripts/copy-deck.py` (don't edit by hand).
- `build.mjs` → generates every page in 3 languages; also holds `MENU` (menu preview photos), `COVERS` (journal covers), `menuOverlay()`, `documentHTML()`, Vercel redirects.
- `src/config.json` (contacts, siteUrl, indexable, shop + form settings), `src/i18n/{en,vi,zh}.json` (all copy), `src/data/` (prices, reviews, journal posts, sample products), `src/styles/site.css` (tokens at top), `src/js/site.js` (menu, shop filters, form, tracking), `src/js/motion.js` (GSAP + three.js effects), `src/vendor/`, `src/brand/logo.svg` (wordmark traced from PNG).
- `assets/img/` → WebP photos (made by `scripts/prepare-images.py`); `assets/brand/` original logo/favicon; `assets/brand-out/` icons; `assets/share.jpg`.
- `scripts/` → `qa.py`, `shots.py`, `perf.py`, `copy-deck.py`, `prepare-images.py`. `qa/` → screenshots, `motion-home.webm`.
- `_source/` → crawl of old site, blog extraction, stock photos + sources (`stock/stock.json`), `font-options/` (font comparison). Not deployed.
- `dist/` → built site (deploy this; contains `.vercel/` link, `vercel.json`, `_hosting/` .htaccess/nginx redirects).
- `pitch/` → `De-xuat-website-Phans-VI.pdf` (client, Vietnamese) and `Website-proposal-Phans-EN.pdf` (English), 16 slides each, built by `pitch/build_pdf.py` from one source; `de-xuat-website-phans.html` + `De-xuat-website-Phans-Custom-Tailor.pdf` are the older 14-slide first version (2026-10-13); `tin-nhan-gui-Phans.txt` → draft outreach message.

## Client preferences / rules
- Premium, editorial, in the spirit of **Suitsupply, Brioni, Sacoor Brothers** (references the user chose) — borrow feel only, never copy text/photos/layout. Must **not look AI-generated**; no emoji anywhere; no Unicode symbols as icons.
- Keep the PHAN'S wordmark and "P" monogram; refresh everything else (drop old Montserrat/Tinos/Inter, grey #9b9b9b, red).
- Palette: ink #141414, paper #f7f6f3, stone #d8d5cf, mute #5f5f5f, accent worsted navy #1e2a3a. Square corners, hairline rules.
- Fonts: **Prata** (headings, single weight — no bold/italic) + **Hanken Grotesk** (body). User rejected Cormorant Garamond as "too AI" (2026-10-07). Must support Vietnamese; Chinese pages use system CJK fonts. Never Inter or Playfair Display.
- Motion: user asked for GSAP + three.js and much more hover/movement (home felt too static) — overrides the brief's "subtle motion only". Keep content visible without JS and respect reduced motion.
- Menu: full-screen overlay after a "Torii" reference (numbered 01–09 items, hairline dividers, hover preview photo, "P" monogram). Header: menu button left, logo centred, language + "Book an appointment" right.
- Home hero after Suitsupply: client's own campaign photo full-bleed, section links bottom-left, no big headline/subline/buttons (those looked AI).
- English is the main language (most customers are foreign); TWX writes the VI/ZH translations ourselves (client won't supply). Language switch keeps the visitor on the same page.
- Booking (Koalendar) is the primary CTA; WhatsApp/Zalo/form secondary; fixed Book/WhatsApp bar on phones.
- Truth rules: don't use "#1 bespoke tailor in HCMC" or "only tailor where both founders are architects". Real Tripadvisor quotes only (4.8 / 975, Oct 2026). Use the Facebook page found first (phanstailor) since it's a proposal.
- Copy: British spelling, sentence case, no exclamation marks outside reviews; banned-word list in the brief §5. Avoid card-heavy layouts, alternating image/text rows, lone dark sections, stats bands, popups.
- Mobile: keep pages short (compact process steps, squarer photos, no duplicate address/booking blocks in footer).

## Workflow notes
- Edit copy in `src/i18n/*.json` → `node build.mjs` → `python3 scripts/copy-deck.py`. Preview: `cd dist && python3 -m http.server 4321` → http://localhost:4321. Run `python3 scripts/qa.py` (and `shots.py`, `perf.py`) after changes.
- Deploy: `node build.mjs` then `cd dist && npx vercel deploy --prod --yes --scope thewebxiteai-6218s-projects`. The Vercel CLI installs slowly in the sandbox (install into a scratch folder, may need outside-sandbox approval). Vercel login is saved on this machine — never write tokens into the project; `.vercelignore` excludes `_hosting/` and `.env*`.
- Don't test the live enquiry form during demos — it posts to the client's real email (FormSubmit activation). Use your own address in `config.forms.formsubmitEmail` for tests.
- Pitch decks: edit `pitch/build_pdf.py`, which builds VI + EN HTML and PDFs from one source (needs network for Google Fonts).
- User sends outreach as "Yong – TheWebxite" in Vietnamese via WhatsApp/Zalo; preferred to be upfront that TWX is a web agency.
- Assistant memory note: `~/.claude/projects/-Users-hengzhexin-Desktop-Client-PhanCustom/memory/phans-vercel-deploy.md`.

## Open items
- Old copy of the site (pre-mobile-fix) still live at https://phans-custom-tailor.vercel.app on the other Vercel account (hengzhexin-7856, team `zxheng`) — delete it or leave it; don't send that link.
- Awaiting client response to the pitch.
- Before launch (see `CONFIRM.md`): Facebook page, final domain, "since 2013", founder names, missing prices (blazer, waistcoat, overcoat, women's), VND vs USD, Tết closure dates, six sample shop products, 23 stock photos to replace with client photos, geo coordinates, FormSubmit activation, native review of VI/ZH translations, set `indexable: true`, strip CONFIRM/PLACEHOLDER comments, connect WooCommerce.

## Change log
- 2026-10-15 — Redeployed latest build to thewebxite.ai Vercel (phans-custom-tailor-demo); old 14-slide deck re-rendered with the new demo link.
- 2026-10-15 — Moved the demo to the thewebxite.ai Vercel account: project `phans-custom-tailor-demo` in team `thewebxiteai-6218s-projects`, live at https://phans-custom-tailor-demo.vercel.app (includes the 2026-10-14 mobile fixes). Updated the link in both PDF decks (rebuilt with real fonts), the outreach message draft and README.
- 2026-10-14 — Mobile audit + fixes (shorter pages, compact process steps, squarer photos, simplified footer); not yet deployed due to network outage. Pitch decks rebuilt as 16-slide VI + EN PDFs from `pitch/build_pdf.py`.
- 2026-10-13 — Wrote Vietnamese outreach message + 14-slide Vietnamese proposal PDF with annotated screenshots of old vs new site; reviewed the user's own message version (recommended sending the user's version).
- 2026-10-07 — Side research for the user: Phan's suit prices vs KL tailors (Google ratings, price bands).
- 2026-10-07 — Deployed to Vercel (https://phans-custom-tailor-demo.vercel.app), old Haravan URL redirects fixed, internal hosting files excluded.
- 2026-10-07 — New full-screen menu (Torii reference) and Suitsupply-style home hero with client campaign photo.
- 2026-10-07 — Added GSAP + three.js motion (rippling hero, 3D cloth band, marquee, reveals, magnetic buttons, cursor, page curtain).
- 2026-10-07 — Fonts changed from Cormorant Garamond / Be Vietnam Pro to Prata / Hanken Grotesk ("too AI").
- 2026-10-06 — Brief written via website-prompt-builder (Tripadvisor reviews, references Suitsupply/Brioni/Sacoor); full build: 72 pages in EN/VI/ZH, shop on sample data, 7 journal posts migrated/translated, QA + Lighthouse, README, CONFIRM.
