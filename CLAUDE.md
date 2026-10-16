# Phan's Custom Tailor — proposal website

## Overview
- Client (prospect): **Phan's Custom Tailor**, bespoke tailor in a private villa at 08 D9, Saigon Pearl, Bình Thạnh, Ho Chi Minh City. Founders Mr. Thinh Phan and Ms. Thuong Phan (architecture graduates). Current site: https://tailormadesuit.net (Haravan template). Contact/booking facts live in `src/config.json`.
- What: an unsolicited **proposal/pitch** — full revamp as a trilingual static site (English main at `/`, Vietnamese `/vi/`, Simplified Chinese `/zh/`), 72 pages, with a shop that will read products from a headless WooCommerce Store API later.
- Demo URL: **https://phans-custom-tailor-demo.vercel.app** (Vercel project `phans-custom-tailor-demo`, team `thewebxiteai-6218s-projects` (thewebxite.ai account); noindex while `indexable` is false). Plan: demo on Vercel, later point to TWX hosting; WordPress only for the WooCommerce API/checkout (`shop.tailormadesuit.net`, unconfirmed).
- Repo: **https://github.com/TheWebxite/phans-custom-tailor** (private, branch `main`), connected to the Vercel project — every push to `main` builds (`node build.mjs` → `dist/`, settings in root `vercel.json`) and goes live.
- **AI fitting room** (headline selling point): Decart Anywear virtual try-on widget, one script tag in `documentHTML()` in `build.mjs` (`anywear.decart.ai/widget/latest/anywear.js?domain=phans-custom-tailor-demo.vercel.app`), added by teammate lautengsheng 2026-10-15. Adds "Try-On" badges on product photos and an "AI fitting room" pill; renders the garment on the visitor's camera feed in real time (follows body movement and folds).
- Platform: dependency-free Node build (`build.mjs`) → static `dist/`. Self-hosted GSAP 3.13 (ScrollTrigger, SplitText) + three.js r170. Enquiry form via FormSubmit.
- Pitch materials sent to the owners via WhatsApp/Zalo: Vietnamese + English PDF decks in `pitch/` (17 slides; slide 5 is the AI fitting room).

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
- `pitch/` → `De-xuat-website-Phans-VI.pdf` (client, Vietnamese) and `Website-proposal-Phans-EN.pdf` (English), 17 slides each, built by `pitch/build_pdf.py` from one source; `de-xuat-website-phans.html` + `De-xuat-website-Phans-Custom-Tailor.pdf` are the older 14-slide first version (2026-10-13); `tin-nhan-gui-Phans.txt` → draft outreach message; `tin-nhan-truoc-cuoc-goi.txt` + `pre-call-message-EN.txt` → pre-call message; `briefing-cuoc-goi-Kimlien.txt` + `pre-call-briefing-EN.txt` → call briefing for Kimlien (2026-10-17).

## Client preferences / rules
- Phase 1 decisions (user, 2026-10-17): shop is **showcase/catalogue only** (browse → WhatsApp/Zalo or book), no cart, login, WooCommerce or payment gateway; booking stays on their existing **Koalendar** (link, no new system); TWX buys/manages hosting and does maintenance; domain stays in Phan's name; build in ~1 week after materials; **don't present the AI fitting room to the client** until Decart pricing is confirmed (free beta, no published pricing as of 2026-10-17). Payment gateways for a later phase: OnePay/VNPay (Razorpay/Curlec doesn't serve Vietnam).
- Domains (checked 2026-10-17): Phan's owns **phanscustomtailor.com** (on their Google Maps listing; DNS on Google Cloud DNS, currently forwards to tailormadesuit.net) and tailormadesuit.net (same DNS, Haravan IP). phantailor.com is at Mắt Bão with Google Workspace email (MX) and a broken website. Recommended main domain: phanscustomtailor.com, others forward to it; never touch the email (MX) records.
- The AI fitting room is one of the main selling points of the pitch — feature it prominently (own slide, cover line, features tile). Frame it honestly: it shows style/colour/cloth on the visitor; real measurements are still taken at the villa.
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
- Deploy: commit and `git push` to `main` (Vercel builds from GitHub). Fallback: `node build.mjs` then `npx vercel deploy --prod --yes --scope thewebxiteai-6218s-projects` from the project root. GitHub CLI installed at `~/.local/bin/gh` (logged in as TheWebxite). Commits in this repo must be authored as `TheWebxite <thewebxite.ai@gmail.com>` (set in the repo's local git config) — Vercel blocks deploys from commit authors outside the team (e.g. the global `ZX <hengzhexin@gmail.com>` identity). The Vercel CLI installs slowly in the sandbox (install into a scratch folder, may need outside-sandbox approval). Vercel login is saved on this machine — never write tokens into the project; `.vercelignore` excludes `_hosting/` and `.env*`.
- Don't test the live enquiry form during demos — it posts to the client's real email (FormSubmit activation). Use your own address in `config.forms.formsubmitEmail` for tests.
- Pitch decks: edit `pitch/build_pdf.py`, which builds VI + EN HTML and PDFs from one source (needs network for Google Fonts).
- User sends outreach as "Yong – TheWebxite" in Vietnamese via WhatsApp/Zalo; preferred to be upfront that TWX is a web agency.
- Assistant memory note: `~/.claude/projects/-Users-hengzhexin-Desktop-Client-PhanCustom/memory/phans-vercel-deploy.md`.

## Open items
- AI fitting room: on phones the "AI fitting room" pill is hidden (widget collapses to the left edge); entry is via the "Try-On" badges, which open it full screen — test on a real phone before the demo. Widget shows "6 free passes" per visitor; check Decart usage limits/costs and the `domain=` parameter if the site moves to tailormadesuit.net.
- Old copy of the site (pre-mobile-fix) still live at https://phans-custom-tailor.vercel.app on the other Vercel account (hengzhexin-7856, team `zxheng`) — delete it or leave it; don't send that link.
- Call with anh Thịnh handled by Kimlien (Vietnamese; Yong doesn't speak Vietnamese). Pre-call message `pitch/tin-nhan-truoc-cuoc-goi.txt` (EN `pre-call-message-EN.txt`) and Kimlien's call briefing `pitch/briefing-cuoc-goi-Kimlien.txt` (EN `pre-call-briefing-EN.txt`). Still to decide before the quote: price, payment terms, monthly hosting/maintenance fee. He's also working with a separate Web 3D team — position our site as the home that can embed their 3D work.
- The live demo still loads the AI fitting room widget although it isn't being pitched yet — hide it (remove the script in `documentHTML()`) if the client shouldn't see it.
- Demo still shows sample products with "Add to bag"; switch the shop to catalogue mode (enquire/book buttons) in the real build.
- Before launch (see `CONFIRM.md`): Facebook page, final domain, "since 2013", founder names, missing prices (blazer, waistcoat, overcoat, women's), VND vs USD, Tết closure dates, six sample shop products, 23 stock photos to replace with client photos, geo coordinates, FormSubmit activation, native review of VI/ZH translations, set `indexable: true`, strip CONFIRM/PLACEHOLDER comments, connect WooCommerce.

## Change log
- 2026-10-17 — Call briefing PDF for Kimlien (VI + EN, 5 pages A4: summary, context, call order, domain/hosting diagram, positions, Q&A, don't-promise, checklist, pre-call message appendix) built by `pitch/build_briefing.py`.
- 2026-10-17 — Finalised pre-call message (catalogue-only shop, Koalendar booking, phanscustomtailor.com recommended, AI fitting room left out) and wrote Kimlien's call briefing (VI + EN): plain-language glossary, our positions, likely questions + answers, don't-promise list, info checklist.
- 2026-10-16 — Drafted pre-call message to anh Thịnh (VI + EN): collaboration scope, how hosting/domain/shop work in plain terms, what changes at switch-over, info needed, next steps.
- 2026-10-15 — Pitch decks (VI + EN) now 17 slides: new slide 5 "AI fitting room" with before/after try-on (grey suit → Cavani linen blazer), cover line, shop slide shows Try-On badges, features tile. Try-on tested with a fake camera feed from a stock photo (one pass used).
- 2026-10-15 — First Git deploy was blocked (commit author ZX not on the Vercel team); repo git identity set to TheWebxite <thewebxite.ai@gmail.com>.
- 2026-10-15 — Pushed to GitHub (TheWebxite/phans-custom-tailor, private) and connected it to the Vercel project; deploys now run from Git pushes.
- 2026-10-15 — Git repo initialised (main), `.gitignore`/`.vercelignore` set for Git deploys, build now writes root `vercel.json` (build `node build.mjs`, output `dist`); clean clone builds OK. Not pushed yet (no GitHub auth on this Mac).
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
