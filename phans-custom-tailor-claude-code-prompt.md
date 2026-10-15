# Phan's Custom Tailor: trilingual static site with a WooCommerce-powered shop, Vercel proposal first

You're building a new website for **Phan's Custom Tailor**, a tailor making suits, trousers and shirts to measure for men and women. They work from a private villa in Saigon Pearl, Bình Thạnh, Ho Chi Minh City, and most customers are foreign visitors. Customers book a consultation on the founders' booking calendar (Koalendar) or message the team on WhatsApp or Zalo. They come in for measurements, return for a fitting, and collect within about five working days.

**How it will be used:** it starts as a **proposal site on Vercel** for the client to review. Once approved, the same static files move to our own hosting under the client's domain. There's no CMS for the pages. WordPress with WooCommerce runs on a separate subdomain only to manage shop products, and its REST API feeds the shop pages (section 8.3).

This replaces their current site, **https://tailormadesuit.net/** (a Haravan shop template with leftover Vietnamese system text, a broken cart, an empty Testimonials page and one product). Use it as the source for content, photos, blog posts and the logo; the design is new.

- **Audience:** mainly foreign visitors to Ho Chi Minh City (business travellers, tourists, grooms and wedding parties), often with only a few days in town and booking from abroad. A smaller share are local Vietnamese and Chinese-speaking customers. English is the main language, with Vietnamese and Simplified Chinese versions.
- **Goal:** get the visitor to book a consultation (Koalendar). Second, get them to message on WhatsApp or Zalo, or send an enquiry. Every page should make that easier.
- **Working folder:** the current directory (`PhanCustom`). Code prefix: `pct`.

---

## 0. What the client asked for

Check every item before you report back.

1. A complete revamp that feels **premium and editorial**, in the spirit of Suitsupply, Brioni and Sacoor Brothers (section 5). It must not look AI-generated, and there's no emoji anywhere.
2. Keep the PHAN'S logo and refresh everything else: palette, type and layout (section 5).
3. A multi-page site: Home, About, The Bespoke Process, Suits & Pricing, Fabrics, Shop, Journal, FAQ, Contact (section 8).
4. An online shop for Nobility fabrics and ready-made items, with products managed in WooCommerce and pulled in through its API (section 8.3).
5. English as the main language, plus Vietnamese and Simplified Chinese versions of every page. We write the translations ourselves (section 10.3).
6. "Book an appointment" (Koalendar) is the main button everywhere. WhatsApp, Zalo and an enquiry form are secondary (section 11).
7. Real customer reviews from Tripadvisor, quoted accurately (section 9.6).
8. The seven existing blog posts move into the new Journal (section 9.8).
9. Social links: Instagram, Facebook, WhatsApp, Zalo and Messenger (section 6).
10. Copy written for Phan's and around the words its customers search with (section 10).
11. Works properly on desktop, tablet and mobile (section 4).

## 1. How to work

1. **Study the inputs.**
   - If `./_source/` has an export of the current site, use it; otherwise crawl https://tailormadesuit.net/. Write `_source/inventory.md` listing every page with its sections and copy, every image worth keeping (download them to `_source/images/`), the seven blog posts (full text, in every language they contain), the ten fabric-brand logos on the home page (`brand_img1.png` to `brand_img10.png`, identify which brand each is), contact details, and the colours and fonts from its CSS. Several blog images are AI-generated (filenames start with `gemini_generated_image`): flag them, and don't reuse them as hero or section photos.
   - Look at each reference in section 5 for the listed traits only.
   - Use `assets/brand/` (logo and favicon, already there) and `assets/photos/` (photos from the client's Instagram, if added). Use `docs/` if it exists.
2. **Plan, then stop.** Before writing code, send me:
   - the sitemap with each page's sections, in order
   - the design tokens: palette in hex, typefaces and their roles (including Vietnamese and Chinese coverage), type scale, spacing and radius
   - layout ideas for the home hero, the Suits & Pricing table, the Fabrics page and the Shop listing, for desktop and mobile (ASCII wireframes are fine)
   - how the shop reads from WooCommerce, and how it works in the proposal before the WooCommerce site exists (section 8.3)
   - the URL plan for the three languages, and the redirect list from the old Haravan URLs (section 8.5)
   - the keyword map from section 10, confirmed or corrected
   - anything in this brief you think is wrong or missing
   - these assumptions, confirmed or corrected: motion is subtle; photos come from the current site and Instagram, with stock only to fill gaps; the primary Facebook page is facebook.com/phanstailor; prices are shown in VND only; the enquiry form sends by email through FormSubmit; the shop hands off to WooCommerce's own cart and checkout; the proposal is `noindex` until launch.

   Then wait for my OK.
3. **Build**, following sections 2 to 12.
4. **QA and report**, following sections 13 and 14.

If the `frontend-design` skill is available, use it.

## 2. Delivery format

Build a plain static site with no framework:
- One folder per page with its own `index.html` (`/about/index.html`), so URLs stay clean, all sharing `assets/`. Language versions live under `/vi/` and `/zh/` with the same slugs (`/vi/about/`, `/zh/about/`).
- Source lives in `src/`: design tokens, components, the header and footer partials, the link map, one copy file per language (`src/i18n/en.json`, `vi.json`, `zh.json`) and data files (`src/data/prices.json`, `reviews.json`, `fabrics.json`, `journal/`, `products.sample.json`). A small Node build script (no dependencies beyond what Node ships with, or a single small templating package if you justify it in the plan) generates every page in every language into `dist/`. A nav, price or footer change is one edit and a rebuild.
- Vanilla JavaScript only; no CSS or JS frameworks or libraries. Google Fonts load with a `<link>` in the head (`display=swap`). The Chinese font loads only on `/zh/` pages.
- Images live in `assets/img/` as WebP, no wider than 2000px, with width and height set. The first large image on each page is eager with `fetchpriority="high"`; the rest are lazy.
- Photos: reuse the best photos from the current site and anything in `assets/photos/` (from the client's Instagram, @phanstailor). If you need an extra photo, use Unsplash: men's and women's tailoring, cloth, workroom details, natural light, muted tones, never staged-looking. List every stock photo in `CONFIRM.md` for replacement with the client's own.
- Logo: `assets/brand/logo.png` (737×227, black wordmark "PHAN'S / CUSTOM TAILOR" on transparent). Trace it to a clean inline SVG so it stays sharp and can turn white on dark photos. If tracing isn't faithful, keep the PNG, add a white version, and note it in `CONFIRM.md`. The favicon is `assets/brand/favicon.png` (a white serif "P" in a black circle); generate the favicon sizes and an apple-touch icon from it.
- Add a `.vercelignore` excluding `_source/`, `qa/`, `docs/`, `src/` and all `.md` files, so internal files never go live. Vercel serves `dist/`.
- This is a proposal: every page gets `<meta name="robots" content="noindex, nofollow">` behind one build flag (`INDEXABLE=false`). Switching it to `true` for launch removes the tag and generates `robots.txt` and `sitemap.xml`.
- The output has to run on ordinary static hosting after the proposal stage, not just on Vercel. Put the redirects in `vercel.json` and also generate an equivalent `.htaccess` and an nginx snippet in `dist/_hosting/` (section 8.5).

## 3. Built to move cleanly

There's no Elementor in this build, but keep the code easy to lift and maintain:
- Prefix every class, ID, custom property, keyframe name, `data-` attribute and form field name with `pct`.
- Custom properties are defined once on a root wrapper, and component CSS is scoped to its component class. No styling of bare tags outside a base reset.
- No `100vw` (it causes horizontal scroll next to the scrollbar). Full-bleed sections are `width: 100%`.
- Each page works before JavaScript runs: all content is visible, accordions use native `<details>`, and collapsed states (mobile menu, language menu, shop filters) only apply once the script adds `pct-js` to the root.

## 4. Desktop, tablet and mobile

Use breakpoints at **767px and 1024px** (mobile up to 767px, tablet 768–1024px, desktop 1025px and up). Content caps at about 1280px on large screens; photo bands run full width.

| Part | Desktop | Tablet | Mobile |
|---|---|---|---|
| Header | Logo left; nav centre or right; language switch (EN / VI / 中文); "Book an appointment" button. Becomes a slim bar on scroll | Logo, language switch, button, menu icon | Logo and menu icon; the booking button lives in a sticky bottom bar instead |
| Mobile bottom bar | None | None | Two actions: "Book an appointment" and WhatsApp. Hides while a form is on screen |
| Home hero | Full-bleed photo, headline over a calm area of the photo, two buttons | Same, shorter | Photo above or behind, headline below the fold line is fine; buttons stack |
| Bespoke process | Five steps in a horizontal sequence with photos | Two columns | One column, numbered |
| Suits & Pricing table | Garment, what's included and "from" price set out like a printed price list | Same | Each garment as a row block; no horizontal scroll |
| Fabrics | Mill sections with swatch photography and short notes | Two columns | One column |
| Shop listing | Four products per row, filters on the left | Three per row, filters in a drawer | Two per row, filters in a drawer |
| Journal | Lead post large, then a two-column list | Two columns | One column |
| Reviews | Pull quotes in a wide editorial layout | Two columns | One column, three quotes then "Read more on Tripadvisor" |
| Footer | Four columns: visit, contact, explore, social | Two columns | One column |

Also:
- Form fields use at least 16px text on mobile (anything smaller makes iOS zoom in on tap), run full width, and have tap targets of at least 44px.
- No horizontal scroll at any width; long names, Vietnamese diacritics and Chinese lines wrap cleanly.
- Floating and bottom-bar buttons hide while a form is on screen.
- Hover effects only apply on devices that can hover (`@media (hover: hover)`); everything works by tap.
- Tall hero areas use `svh` with a `vh` fallback, never plain `100vh`.

## 5. Design direction

**Keep:** the PHAN'S wordmark (a wide-tracked classical serif, black) and the "P" monogram.

**Refresh:** everything else. The current site's colours and fonts (Montserrat, Tinos, Inter, theme grey `#9b9b9b`, red `#d61114`) are template defaults, not brand choices; don't carry them over.

**Starting proposal for tokens** (refine in your plan):
- Ink `#141414` for type and the logo; a clean warm-white page `#F7F6F3`; a cool stone `#D8D5CF` for rules and hairlines; a mid grey `#6B6B6B` for secondary text.
- One accent drawn from cloth, used only on buttons, links and a few details. Try a deep worsted navy (around `#1E2A3A`) or a bottle green (around `#22372B`). Pick one and show both in the plan.
- Headings in a refined high-contrast serif that echoes the logo's capitals and supports Vietnamese, for example Cormorant Garamond or Bodoni Moda; body in a quiet sans that supports Vietnamese, for example Be Vietnam Pro or Manrope. On `/zh/`, use Noto Serif SC for headings and Noto Sans SC for body. Don't use Inter or Playfair Display.
- Square or near-square corners (0–2px radius), hairline rules instead of boxes, no shadows except on menus and drawers.

**The feel:** premium and editorial. Large photography of real garments, cloth and the villa; a lot of white space; the serif doing the work at large sizes; short copy; prices set out like a printed tailor's list; slow, subtle motion (one gentle hero entrance and quiet hover states, nothing else).

**References:**
- https://suitsupply.com/en-my/: borrow the clean, image-led product grid, the confident full-bleed campaign photography, and the way services (custom made, alterations, fit advice) sit as short, plain lines next to the product range. Don't copy its text, photos, logo or exact layout.
- https://www.brioni.com/en/my: borrow the restraint. Black and white, a lot of space, a single large image per screen, small, precise navigation type and a quiet luxury tone. Don't copy its text, photos, logo or exact layout.
- https://my.sacoorbrothers.com/: borrow the editorial home page rhythm. Large lifestyle bands alternate with focused collection rows, and the tailoring and occasion edits (wedding, business) have clear entry points. Don't copy its text, photos, logo or exact layout.

**The client doesn't want:** anything that looks like their current shop template (busy widgets, popups, cart clutter, mixed Vietnamese and English system text) or like a generic AI site.

**What makes it look designed rather than generated:**
- Vary how sections are built (a full-width photo band, a text-led section, a menu or spec table laid out like print, a directory-style list) instead of repeating "centred heading plus three cards".
- Let type carry the hierarchy: a real type scale, lines under about 70 characters, size and weight doing the work instead of boxes and badges.
- One accent colour, used sparingly (buttons and a few key details).
- Icons only where they mean something (values, contact details, buttons), from one line set with one stroke weight.
- Quick, quiet interaction states (150–200ms), and at most one deliberate motion moment unless the brief asks for more.
- Real, specific content everywhere: the client's actual garments, prices, fabrics, founders, address and hours.

**Avoid:**
- identical card grids section after section, the same radius and shadow on everything, icons in coloured circles
- rounded, card-heavy layouts everywhere (clients have rejected these as looking AI-made)
- image-left/text-right rows alternating section after section (one alternating pair is fine; a whole page of them has been rejected)
- gradient text, gradient washes, glassmorphism, glowing blobs, sparkles, floating shapes
- a small all-caps label above every heading, one word of a headline picked out in italic or colour, big-number stats bands
- a fade-up entrance on every section, bouncy or looping animation
- "A · B · C" middle-dot strings, arrows tacked onto link text
- a lone dark section dropped into an otherwise light page (clients have called it messy)
- stock clichés used as filler (tape measures draped over everything, generic handshake or skyline shots)
- popups, newsletter modals and cookie walls beyond what's legally needed
- walls of text; stick to the word budgets

**No emoji anywhere:** page copy, buttons, WhatsApp prefilled messages, form emails, alt text, JSON-LD and code comments. The current site's blog posts and FAQ use flag and sparkle emoji; don't carry them over. Don't use Unicode symbols as icons either (star, tick, arrow or sparkle characters); use inline SVG.

**Copy:** plain English with British spelling (colour, centre, organise), sentence-case headings, short sentences that describe rather than sell, and no exclamation marks outside quoted reviews. Copy is in English, Vietnamese and Simplified Chinese (section 10.3). The language switch keeps visitors on the same page in the other language. Don't use: experience the ultimate, discover, unlock, elevate, indulge, treat yourself, your journey, "where X meets Y", look no further, seamless, curated, holistic, cutting-edge, state-of-the-art, world-class, unparalleled, one-stop solution, leverage, empower, synergy, sanctuary, masterpiece, or slogan triplets like "Measure. Cut. Fit." **Exception:** "bespoke" is allowed, because it's the service customers search for, but use it where it's precise (the garment and the process), not as decoration.

| Part | Budget |
|---|---|
| Hero headline | Up to 8 words |
| Hero subline | Up to 25 words |
| Section intro | Up to 40 words |
| Card or list item | Up to 20 words |
| About page, body copy (captions and lists extra) | Up to 250 words |
| Product or service description | Up to 150 words |
| FAQ answer | Up to 60 words |

Journal posts keep their full length (they're articles), but trim any that read as padding.

**Quality floor:** visible keyboard focus, `prefers-reduced-motion` respected, WCAG AA contrast, semantic HTML, labelled form fields, and descriptive alt text.

## 6. Business facts (the only source of truth)

| Item | Value |
|---|---|
| Brand name on site | Phan's Custom Tailor (wordmark: PHAN'S) |
| Founders | Mr. Thinh Phan and Ms. Thuong Phan (in Vietnamese: Phan Thịnh and Phan Thương; CONFIRM the order and diacritics) |
| Phone | +84 826 977 888 (`tel:+84826977888`) |
| WhatsApp | +84 826 977 888 (`https://wa.me/84826977888`) |
| Zalo | `https://zalo.me/0826977888` |
| Messenger | `https://m.me/108520260558644` |
| Email | info@phantailor.com |
| Address | Villa, 08 D9 Street, Saigon Pearl, Bình Thạnh, Ho Chi Minh City, Vietnam (Vietnamese form: Villa, 08 Đ. D9, Saigon Pearl, Bình Thạnh, Thành phố Hồ Chí Minh) |
| Hours | Monday to Saturday, 9:00 AM to 7:00 PM. Sundays and public holidays by prior appointment |
| Parking | Motorbike and car parking directly in front of the villa |
| Booking | `https://koalendar.com/e/phantailor` (opens in a new tab) |
| Instagram | `https://www.instagram.com/phanstailor/` |
| Facebook | `https://www.facebook.com/phanstailor/` (the old site also links facebook.com/phantailor; CONFIRM which is current) |
| Tripadvisor | `https://www.tripadvisor.com/Attraction_Review-g293925-d4795476-Reviews-Phan_s_Custom_Tailor-Ho_Chi_Minh_City.html` |
| Price notes | "From" prices in VND, including the full tailoring process and lifetime free alterations (9.2) |
| Turnaround | Standard 5 working days; rush orders discussed at the consultation |
| Domain | tailormadesuit.net (assumed to stay; the email uses phantailor.com; CONFIRM which domain the new site goes on) |

The old site wrote the phone three ways ("(+84)826977888", "0826977888", "+84826977888"). Use "+84 826 977 888" everywhere in visible text. Write hours as "9:00 AM to 7:00 PM" in English, "9:00 – 19:00" in Vietnamese and "9:00–19:00" in Chinese, and prices as "6,800,000 VND" in English, "6.800.000 ₫" in Vietnamese and "6,800,000 越南盾" in Chinese.

## 7. Truth rules

- Only state facts that are in this brief. Anything unconfirmed gets a `<!-- CONFIRM: ... -->` comment in the code and a line in `CONFIRM.md` (these comments are stripped before launch).
- Where the current site disagrees with this brief, this brief wins; list each difference in `CONFIRM.md`.
- Don't invent numbers, years in business, certifications, awards, clients, team members or testimonials. These are true if you want figures on the page:
  - The founders are both graduates of the Ho Chi Minh City University of Architecture (class of 2003).
  - The business has operated since 2013 (from the client's About page; CONFIRM).
  - Over 20 measurements are taken at the first consultation.
  - Tripadvisor shows 4.8 of 5 from 975 reviews, ranked #10 of 891 shopping listings in Ho Chi Minh City, and a Travellers' Choice 2026 badge (as of October 2026; show it as "4.8 on Tripadvisor from 975 reviews", with the month noted in a CONFIRM comment so it gets updated).
- **Don't use** the old About page's claim to be "the #1 bespoke tailor in Ho Chi Minh City" or "the only tailor shop in Saigon where both founders are architecture graduates". Neither can be verified. The architecture background is a strong, true story without the superlative. List both in `CONFIRM.md` in case the client wants to defend them.
- The Tripadvisor listing describes the business as "for men", but the client's FAQ says they tailor for women too (suits, trousers, skirts). Use the FAQ, and list it in `CONFIRM.md`.
- Reviews mention suits finished in 2 to 4 days. The official line is 5 working days, with rush orders possible. Don't promise faster.
- Drop the old homepage notice about closing from 20 to 22 December; it's out of date.
- No price conversions to USD or other currencies unless the client approves a rate (CONFIRM).
- The current shop's single product (Men Linen Blazer, Green Linen, Cavani, 2 button, slim fit, 5,400,000 VND) is real. Any other product in the proposal is a sample, marked as such (section 8.3).

## 8. Site map

### 8.1 Shared parts
- **Source:** tokens, components, header, footer, the link map, copy files and data files live in `src/`; the build script generates every page in all three languages.
- **Header:** logo; nav: Bespoke Process, Suits & Pricing, Fabrics, Shop, Journal, About, Contact (FAQ sits in the footer and on Contact); language switch EN / VI / 中文 that keeps the visitor on the same page; "Book an appointment" button. Sticky, slimming on scroll.
- **Footer:** the address with a "Get directions" Google Maps link, hours, phone, WhatsApp, Zalo and email; explore links (all pages plus FAQ); Instagram, Facebook, Messenger and Tripadvisor icons; the language switch; "© Phan's Custom Tailor".
- **Mobile bottom bar:** "Book an appointment" and WhatsApp, as in section 4. On desktop, a small WhatsApp button sits bottom right instead.

### 8.2 Pages

| Page | Slug | Sections, in order |
|---|---|---|
| Home | `/` | Hero; short introduction to the founders and the villa; the five-step process in brief; garments and "from" prices (short, links to Suits & Pricing); fabric mills strip; reviews; journal highlights (three posts); visit and book band |
| About | `/about/` | The founders' letter (rewritten, shorter); the architecture background; the four values; the villa (photos); book band |
| The Bespoke Process | `/bespoke-process/` | Intro; the five steps (9.1), each with a photo; timing for visitors (consultation, first fitting, collection within 5 working days, rush on request); lifetime alterations; book band |
| Suits & Pricing | `/suits-and-pricing/` | Intro; the price list (9.2); women's tailoring; what's included; occasions (business, wedding, travel); book band |
| Fabrics | `/fabrics/` | Intro; each mill (9.3) with swatch photography; cloth by season (linen and cotton for the heat, wool and cashmere for travel home); link to the Shop for Nobility cloth |
| Shop | `/shop/` and product detail pages | Listing with filters (category: Nobility fabrics, Ready-made; colour; price) and product detail (section 8.3) |
| Journal | `/journal/` and `/journal/<slug>/` | Listing and the seven migrated posts (9.8) |
| FAQ | `/faq/` | Grouped accordion (9.7) |
| Contact | `/contact/` | Book a consultation (main action); WhatsApp, Zalo, phone and email; enquiry form (section 11); address, hours, parking and a Google Maps embed; holiday closures note |
| 404 | `/404.html` | A simple page in the site's style with links to Home, Book and Contact |

- **Home:** the main message is that the founders cut and fit every garment themselves in a private villa, so visitors get a precise fit within one short trip. Keep it a doorway: every block is short and links to its full page.
- **About:** photo-led. Use the founders' letter as the voice, but rewrite it (it's long and uses phrases from the banned list). Up to 250 words of body copy.
- **Suits & Pricing:** this page sells to someone deciding from abroad. Show the prices plainly, say what's included, and make "Book an appointment" and WhatsApp obvious.
- **Contact:** add a short, clear note on holiday closures, especially Tết (Lunar New Year), when the shop closes for about two weeks (CONFIRM dates). One recent Tripadvisor review describes arriving for a confirmed appointment during Tết and finding the shop closed; this note helps prevent that.

### 8.3 Shop (WooCommerce as a headless product source)
- The shop pages read products from the **WooCommerce Store API** (`/wp-json/wc/store/v1/products`, public and read-only, no API keys in the browser) on a WordPress subdomain, assumed to be `shop.tailormadesuit.net` (CONFIRM). The base URL is one setting in `src/config.json`.
- **Proposal mode:** the WooCommerce site doesn't exist yet. When the API base is empty, the shop reads `src/data/products.sample.json`, which uses the same field shape as the Store API response, so switching to live data is a config change. Sample products: the real Cavani linen blazer (5,400,000 VND, from the current site), plus three or four Nobility fabric samples and two or three ready-made items, each marked `"sample": true` and shown with a small "Sample product" note in the proposal. Every sample goes in `CONFIRM.md`.
- **Listing:** category filters (Nobility fabrics, Ready-made), colour and price; sort by newest and price. Product grids on Home or Fabrics use the same data and the same card component.
- **Product detail:** generate a static page per product at build time from whichever data source is active (`/shop/<slug>/`), so pages are indexable. Photos, name, price, description, attributes (composition, weight, width for fabrics; size and fit for ready-made), and related products from the same category.
- **Cart and checkout:** out of scope for this build. "Add to bag" sends the visitor to WooCommerce's own cart on the subdomain (`https://shop.../cart/?add-to-cart=<id>`), where WooCommerce handles the cart, checkout, payment and emails. List the WooCommerce setup we need (CORS for the static domain, the permalink base, the theme for the cart and checkout pages, payment gateways) in `README.md`.
- Fabrics by the metre also get "Ask about making this into a suit", which opens WhatsApp with the fabric name prefilled.
- Product names, descriptions and attributes in Vietnamese and Chinese depend on how WooCommerce is set up (a multilingual plugin or separate fields). For the proposal, translate the sample products in `products.sample.json`, and describe the options in the plan.

### 8.4 Links and languages
- English at `/`, Vietnamese at `/vi/`, Simplified Chinese at `/zh/`, with the same slugs under each. Every page carries `hreflang` alternates for `en`, `vi`, `zh-Hans` and `x-default` (English).
- The language switch links to the same page in the other language. Don't auto-redirect by browser language.
- Internal links come from one link map in `src/`, end with a slash, and use descriptive text.

### 8.5 Redirects from the old site
Generate 301 redirects from the old Haravan URLs (all languages point to the English page) in `vercel.json`, `dist/_hosting/.htaccess` and `dist/_hosting/nginx-redirects.conf`:

| Old URL | New URL |
|---|---|
| `/pages/about-us` | `/about/` |
| `/pages/working-hours-appointments` | `/contact/` |
| `/pages/lien-he` | `/contact/` |
| `/pages/frequently-asked-questions-faqs` | `/faq/` |
| `/pages/testimonials` | `/#reviews` on Home (or `/about/#reviews`; pick one in the plan) |
| `/pages/nghe-thuat-bespoke-che-tac-bo-suit-2-manh-hoan-hao-cua-rieng-ban` | `/vi/journal/the-art-of-bespoke-crafting-your-perfect-2-piece-suit/` |
| `/collections/all`, `/collections/hot-products`, `/collections/2-piece-suit` | `/shop/` |
| `/products/men-linen-blazer-green-linen-cavani-2-button-slim-fit` | `/shop/men-linen-blazer-green-linen-cavani-2-button-slim-fit/` |
| `/blogs/news` | `/journal/` |
| `/blogs/news/<slug>` | `/journal/<slug>/` (keep each slug as it is, including the truncated ones) |
| `/account/login`, `/account/register`, `/cart` | `/shop/` |

Add any other URLs the crawl finds.

## 9. Content

### 9.1 The bespoke process (from the client's home page, rewritten in the brief's voice)
1. **Book your appointment.** Book ahead so the founders can reserve time for a private consultation.
2. **Consultation and measurement.** At the villa, a one-to-one conversation with Ms. Thuong Phan or Mr. Thinh Phan about the occasion and your style; choosing the cloth together; over 20 measurements; a pattern drafted for your build.
3. **First fitting and refinement.** The first garment is close to finished. You try it on, and every detail is adjusted for comfort in movement and a clean fit. This fitting confirms the fit before the rest of a multi-piece order is completed.
4. **Finishing and handover.** Final adjustments, then professional dry-cleaning to clean and set the shape, ready to wear.
5. **A lifetime commitment.** Your pattern and measurements are kept on file, and alterations are free for life.

### 9.2 Prices ("from", in VND; all include the full tailoring process and lifetime free alterations)

| Garment | From |
|---|---|
| 2-piece suit | 6,800,000 VND |
| 3-piece suit | 8,400,000 VND |
| Dress trousers | 2,200,000 VND |
| Tailored shirt | 1,300,000 VND |

The old site also lists coats, vests (waistcoats) and blazers as categories, without prices; show them as "Price on consultation" (CONFIRM prices). Women's tailoring: suits, trousers and skirts (CONFIRM prices; if none, "Price on consultation").

Standard turnaround: 5 working days. Rush orders: discussed at the consultation.

### 9.3 Fabrics
- **Vitale Barberis Canonico (VBC):** Italian mill.
- **Holland & Sherry:** English cloth merchant.
- **Nobility:** Phan's own fabric line (the client's Journal has a post on its story; use it).
- Also wool, cotton, linen and cashmere from other suppliers in Europe and South Korea.
- The home page shows ten fabric-brand logos (`brand_img1` to `brand_img10`); identify them in the inventory. Use only the mills you can confirm, and list the rest in `CONFIRM.md`. Don't use mill logos without permission (CONFIRM); text names are fine.
- Imported linings, buttons, interlinings and shoulder pads (from the About page).

### 9.4 Founders and values (from the About page)
- Mr. Thinh Phan and Ms. Thuong Phan, both graduates of the Ho Chi Minh City University of Architecture (class of 2003). They apply proportion, structure and balance to cutting: each cut is planned to suit the wearer's build. The business combines a family tailoring tradition with that design training.
- Values, rewritten in plain words:
  1. **You work with the founders.** They guide every client from the first consultation to the final fitting.
  2. **Quality controlled end to end.** They import the cloth, linings, buttons, interlinings and shoulder pads themselves, and the workroom tailors are trained by Mr. Thinh Phan.
  3. **A private villa, not a shopfront.** Consultations and fittings happen in a quiet, private space.
  4. **Alterations free for life.** Every garment can be adjusted as you change.
- The letter is signed "Thuong & Thinh Phan". A short signature line at the end of the About text works well.

### 9.5 For visitors (from reviews and the FAQ; the facts customers need)
- Book before you fly, using the calendar or WhatsApp.
- Plan for the consultation, at least one fitting and collection within 5 working days. Rush orders are possible; ask at the consultation.
- The team stores your measurements, so reorders from abroad are possible (CONFIRM whether they ship internationally and how remote reorders work).
- Opening hours, the Sunday and holiday rule, and the Tết closure (CONFIRM dates).

### 9.6 Reviews (real, from Tripadvisor; quote exactly, trimmed with an ellipsis where needed; no emoji)
Heading: "4.8 on Tripadvisor from 975 reviews". Show 5 or 6 of these, each with first name and initial, month and year, and a link to the listing:

- **Korey E., Chicago, August 2026:** "Prices are incredible, turnaround time was expeditious - a full custom tailored suit in five days, with multiple fittings and great attention to detail." Also: "plenty of fabric choices, pushing back when things wouldn't work well together".
- **Benjamin C., Vancouver, June 2026** (title: "Came back to Vietnam for Phan's Custom tailor - 3rd Suit"): "Finding a truly exceptional tailor is a rare feat, but finding one that pairs flawless technical precision with genuinely warm, selfless hospitality is nearly impossible."
- **Benjamin C., October 2025:** "I came in with high expectations—and left with four suits, six shirts, two ties, and two pocket squares." Also: "They were patient, thoughtful, and meticulous—making me feel like I was their only client."
- **D W, November 2025:** "In just 2 days I had a custom 3 piece suit, shirt and another pair of pants made that fits me like a glove." (Use with care, since it's faster than the official turnaround.) Also: "Even though they were closing at 7 they stayed past their closing time just to make perfect adjustments".
- **Vincent L., January 2026:** "Phan's Custom Tailor created 6 pairs of pants for me." Also: "They are my favorite pairs now and i wear them every day."
- **Elikem D., August 2026:** "Wide selection of designs and materials for suit composition and accessories. Would certainly recommend to anyone visiting HCM."
- **Alexander K., Corfu, November 2025:** "Perfect service from A-Z."
- **Liangyu G., March 2026:** "not only did they come through with the short timeline I had, the suit turned out great!" (the original ends with an emoji; drop it)

Keep reviewers' spelling as written. Save the full set with sources in `src/data/reviews.json`. Reviews stay in English on all three language versions, with a short translated line saying they're quoted from Tripadvisor. Before launch, check them against the live listing and ask the client whether they'd like any Google reviews added (CONFIRM).

### 9.7 FAQ (from the client's FAQ, typo-fixed and shortened; each answer starts with the direct answer)
1. **What's the difference between bespoke and ready-to-wear?** Ready-to-wear is made in standard sizes. A bespoke garment starts from a pattern drafted for your measurements and build, then is adjusted over fittings until it fits.
2. **How long does a suit take?** Five working days as standard, including the fittings. Rush orders are possible; we'll discuss timing at your consultation.
3. **What fabrics do you use?** Cloth from Vitale Barberis Canonico in Italy and Holland & Sherry in England, our own Nobility range, and wool, cotton, linen and cashmere from European and South Korean suppliers.
4. **How much does a tailored suit cost?** From 6,800,000 VND for a 2-piece suit and 8,400,000 VND for a 3-piece. Dress trousers from 2,200,000 VND, shirts from 1,300,000 VND. Prices include lifetime free alterations.
5. **Do you offer alterations?** Yes, free for life on everything we make, even if your measurements change.
6. **Do I need an appointment?** We recommend it, so the founders can give you their full attention. Book on our calendar or message us on WhatsApp.
7. **Do you tailor for women?** Yes: suits, trousers and skirts, made to measure.
8. **Can I come on a Sunday or a public holiday?** By prior appointment only. We close for about two weeks over Tết (Lunar New Year) (CONFIRM dates).
9. **Where are you, and is there parking?** At a villa on D9 Street in Saigon Pearl, Bình Thạnh. There's parking for motorbikes and cars in front of the villa.
10. **Can I reorder after I leave Vietnam?** We keep your pattern and measurements on file. (CONFIRM whether they ship abroad and how remote orders work; until confirmed, keep the answer to this sentence.)

Questions 8 to 10 are new; list them in `CONFIRM.md`.

### 9.8 Journal (migrate all seven; full text from the crawl)
1. The Wardrobe Workhorse: A Guide to the Versatile Blazer (30/10/2025, Mr. Thịnh)
2. What is a Suit Jacket? Anatomy, Fabrics and the "Orphaning" Rule (29/10/2025, Mr. Thịnh)
3. Suit Jacket vs. Blazer vs. Sport Coat: A Gentleman's Guide (29/10/2025; the old byline "KA HRV" looks like an admin account, so CONFIRM the author)
4. The Story of Nobility: Weaving Heritage, Technology and Timeless Style for the Modern Gentleman (11/08/2025, Mr. Thịnh)
5. Summer Suiting 2025: Choosing Fabric for Hot and Humid Climates (11/08/2025, Mr. Thịnh)
6. 5 Classic Suit Mistakes and How to Fix Them Like an Expert (11/08/2025, Mr. Thịnh)
7. The Art of Bespoke: Crafting Your Perfect 2-Piece Suit (11/08/2025, Ms. Thương)

Several posts contain all three languages in one article. Split them so each language version of the site shows that language's text. Where a post has only English, translate it as in section 10.3. Remove the emoji flags and language buttons inside the posts. Replace AI-generated header images with real photos where possible, and list any you keep in `CONFIRM.md`. Each post gets an author line, a date, an estimated reading time and links to two related posts plus the booking button.

## 10. Copy and keywords

Every line of copy should belong to Phan's Custom Tailor: built from the facts in sections 6 and 9, and written around the words customers actually search with. Voice and banned words are in section 5.

### 10.1 Keyword map
Built from the client's own garment and service names, their Tripadvisor listing and its review language, the current site's titles, and how other tailors and travel guides in Ho Chi Minh City describe the same service. There's no search-volume data yet, so confirm or correct it in your plan.

| Page | Primary keyword | Secondary keywords | Heading idea | Where it goes |
|---|---|---|---|---|
| Home | bespoke tailor Ho Chi Minh City | custom suit Saigon, tailor in Saigon, tailor-made suit Vietnam, suit tailor HCMC | A bespoke tailor in Ho Chi Minh City, run by its founders | SEO title, H1, first 100 words, meta description |
| About | architect-trained tailors in Saigon | Thinh and Thuong Phan, family tailoring, Saigon Pearl villa | Two architects who became tailors | Title, H1, intro |
| The Bespoke Process | how a custom suit is made | suit fitting, made-to-measure process, measurements, lifetime alterations | From the first measurement to the final fitting | Title, H1, step headings |
| Suits & Pricing | custom suit price in Ho Chi Minh City | 2-piece suit price, 3-piece suit, tailored shirt Vietnam, dress trousers, women's suit tailor Saigon, wedding suit Saigon | Suits, shirts and trousers, with prices | Title, H1, table headings, intro |
| Fabrics | suit fabrics in Saigon | Vitale Barberis Canonico, Holland & Sherry, linen suit, wool suit, cashmere, Nobility fabric | Cloth from Biella, Huddersfield and our own mill line (only if the mill locations are confirmed) | Title, H1, mill headings |
| Shop | Nobility suit fabric | buy suit fabric Vietnam, linen blazer, ready-made blazer | Nobility cloth and ready-to-wear pieces | Title, H1, category names |
| Journal | menswear style guide | blazer vs suit jacket, summer suit fabric, suit mistakes | Notes from the cutting table | Title, H1 |
| FAQ | getting a suit made in Vietnam | how long to make a suit in Vietnam, tailor appointment Saigon, alterations | Questions before your first fitting | Title, H1, questions |
| Contact | tailor in Bình Thạnh, Saigon Pearl | book tailor appointment Saigon, Ho Chi Minh City tailor address | Visit the villa in Saigon Pearl | Title, H1, address block |

### 10.2 Placement
- Each page's primary keyword goes in its SEO title (keyword first, brand last), its H1, the first 100 words, at least one H2 and the meta description. If a headline reads better without the keyword, put a short keyword line inside the H1 as its smaller first line: `<h1><span class="pct-kicker">Bespoke tailor in Ho Chi Minh City</span> Cut and fitted by the founders</h1>`.
- Secondary keywords go where they're true: section headings, intros, garment and fabric names, list items and FAQ questions. Use natural variations ("Saigon", "Ho Chi Minh City", "HCMC") rather than repeating one phrase.
- Use the exact primary phrase at most three times in a page's visible copy. No keyword lists, no hidden text, no stuffed alt text, and never a service the business doesn't offer.
- Alt text describes what the photo shows; add a keyword only when it's accurate.
- FAQ questions use the words people search with; each answer starts with the direct answer.
- Slugs are short and keyword-led (section 8.2). Internal links use descriptive text with the target page's keyword, never "click here". Keep the old blog slugs and redirect the old URLs (section 8.5).

### 10.3 Vietnamese and Chinese versions
- You write the translations; the client won't supply them. Write natural, idiomatic copy for each language, not word-for-word translation, keeping the same facts, prices and structure. Where the client's own Vietnamese or Chinese text exists (the FAQ, the trilingual blog posts, the Vietnamese page slug), start from it.
- Vietnamese keywords: may đo vest TP.HCM, may suit nam cao cấp, tiệm may âu phục Sài Gòn, may vest cưới, may đo áo sơ mi. Use the natural Vietnamese term: "may đo" and "âu phục/vest" rather than "bespoke" in body copy, with "Bespoke" kept as the brand's term where the client uses it.
- Chinese keywords (Simplified): 胡志明市 定制西装, 西贡 裁缝, 量身定制西服, 手工定制衬衫. Use 胡志明市 in titles and 西贡 where natural.
- Each language gets its own SEO title and meta description (section 12), not a translation of the English one.
- Mark all Vietnamese and Chinese copy as "pending native review" in `CONFIRM.md` (one line per language, plus any phrases you're unsure of, quoted). Don't add CONFIRM comments to every translated string.

### 10.4 Write it for Phan's
- Run the swap test on every heading and section intro: if another tailor in Ho Chi Minh City could paste it onto their site unchanged, rewrite it with something only Phan's can say (the founders by name, the architecture training, the villa in Saigon Pearl, over 20 measurements, the five-day turnaround, lifetime alterations, the mills, the Nobility range, the prices).
  - Generic: "We craft high-quality suits tailored to your unique style."
  - Specific: "Thinh and Thuong Phan take over 20 measurements, draft your pattern and fit it themselves, ready within five working days."
- Lead with what the customer gets, backed by a fact from this brief, never by a claim the brief doesn't support (section 7).
- Use the client's own names for garments (2-piece suit, 3-piece suit, dress trousers, tailored shirt) and fabrics, and customers' own words from the reviews (fit, fittings, turnaround, fabric choices, short timeline).
- Most readers are foreign visitors with a few days in the city: give clear logistics (how many visits, how long, where, when it's open, how to book from abroad), in calm, confident language.
- Buttons say what happens ("Book an appointment", "Message us on WhatsApp", "Chat on Zalo", "Send enquiry", "Add to bag"), and one action keeps one label everywhere, in each language.
- Keep to the word budgets in section 5.

**Copy deck.** Also write all final copy into `COPY.md`, page by page and section by section, with the keywords each section targets, and the same for Vietnamese and Chinese in `COPY.vi.md` and `COPY.zh.md`, so the client can review the wording separately from the design.

## 11. Forms and contact actions

**Main action:** "Book an appointment" opens `https://koalendar.com/e/phantailor` in a new tab. Don't embed the calendar unless Koalendar's embed is clean on mobile; test it and decide in the plan.

**Enquiry form** (Contact page; also linked from Suits & Pricing):

| Field | Input | Required |
|---|---|---|
| Name | text, `autocomplete="name"` | Yes |
| Email | email, `autocomplete="email"` | Yes |
| WhatsApp or phone | tel, `autocomplete="tel"`; accept +, spaces, dashes and foreign numbers; at least 8 digits | No |
| Country | text, `autocomplete="country-name"` | No |
| What would you like made? | checkboxes: 2-piece suit, 3-piece suit, Trousers, Shirt, Coat or blazer, Women's tailoring, Not sure yet | No |
| Dates in Ho Chi Minh City | two date fields (arrive, leave) | No |
| Message | textarea | Yes |

The client's current form has Name, Email, Phone number and Message. Country, garments and travel dates are additions that help the team plan fittings around a visitor's stay; list them in `CONFIRM.md` so the client can drop them. The form is translated on `/vi/` and `/zh/`.

Behaviour:
- Specific inline validation messages under each field, in the page's language; no alert boxes. The leave date can't be before the arrive date.
- The form posts to `https://formsubmit.co/info@phantailor.com`. With JavaScript, send it to `https://formsubmit.co/ajax/info@phantailor.com` instead and show the thank-you state inline; without JavaScript, the normal post still works.
- Hidden fields: `_subject` ("New enquiry from the website", plus the language), `_template` set to `table`, `_next` set to `/contact/thank-you/` (in the page's language), and a `_honey` honeypot. Keep FormSubmit's captcha on.
- The first submission sends an activation email to info@phantailor.com that the client must click. Put this in `README.md`, and note in `CONFIRM.md` that enquiries pass through FormSubmit, a third-party service.
- Under the form: "Prefer to chat? Message us on WhatsApp" and "Chat on Zalo" links.

**WhatsApp:** links go to `https://wa.me/84826977888?text=` with a prefilled message in the page's language, no emoji, for example: "Hello Phan's Custom Tailor, I'd like to ask about a custom suit." From a fabric or product page: "Hello Phan's Custom Tailor, I'm interested in {product name}."

**Thank-you page:** `/contact/thank-you/` in each language. It confirms the enquiry, says the team usually replies by email or WhatsApp (CONFIRM the typical reply time before stating one), and repeats the booking button.

Push `dataLayer` events (create `window.dataLayer` if missing): `book_click` with where it was clicked, `form_submit` with the garments chosen, `whatsapp_click`, `zalo_click`, `call_click`, `email_click`, `add_to_bag` with the product, and `language_switch`, so GA4 or Meta Pixel can be connected later.

## 12. SEO

- Every page: `<html lang="en">` (`vi` or `zh-Hans` on the other versions), one H1, a `<title>` (up to 60 characters), a meta description (up to 155 characters), canonical, `hreflang` alternates, Open Graph and Twitter tags, a 1200×630 share image, a favicon, and descriptive alt text.

Titles and descriptions follow the keyword map in section 10 (keyword first, brand last). English starting points:

| Page | Title | Meta description |
|---|---|---|
| Home | Bespoke Tailor in Ho Chi Minh City \| Phan's Custom Tailor | Suits, shirts and trousers cut and fitted by founders Thinh and Thuong Phan in a Saigon Pearl villa. Ready in 5 working days. Book an appointment. |
| About | Architect-Trained Tailors in Saigon \| Phan's Custom Tailor | Thinh and Thuong Phan trained as architects before founding Phan's Custom Tailor. Meet the founders and visit the villa in Saigon Pearl. |
| The Bespoke Process | How a Custom Suit Is Made \| Phan's Custom Tailor | Consultation, over 20 measurements, a fitting and handover within 5 working days, with lifetime free alterations. See each step. |
| Suits & Pricing | Custom Suit Prices in Ho Chi Minh City \| Phan's | 2-piece suits from 6,800,000 VND, 3-piece from 8,400,000 VND, shirts from 1,300,000 VND. Lifetime free alterations included. |
| Fabrics | Suit Fabrics in Saigon: VBC, Holland & Sherry \| Phan's | Choose cloth from Vitale Barberis Canonico, Holland & Sherry and our own Nobility range, plus linen, cotton, wool and cashmere. |
| Shop | Nobility Suit Fabric and Ready-Made Pieces \| Phan's | Buy Nobility suiting by the metre and ready-made pieces from Phan's Custom Tailor in Ho Chi Minh City. |
| Journal | Menswear Style Guide \| Phan's Custom Tailor | Notes from Phan's on blazers, suit jackets, summer fabrics and the details that make a suit fit. |
| FAQ | Getting a Suit Made in Vietnam: FAQ \| Phan's | How long a suit takes, what it costs, which fabrics we use and how to book. Answers from Phan's Custom Tailor. |
| Contact | Tailor in Saigon Pearl, Bình Thạnh \| Phan's Custom Tailor | Visit our villa at 08 D9 Street, Saigon Pearl. Open Monday to Saturday, 9 AM to 7 PM. Book, WhatsApp or send an enquiry. |

Write equivalent titles and descriptions for `/vi/` and `/zh/` around the keywords in 10.3.

- JSON-LD `ClothingStore` (with `TailorShop`-style details in the description) on the home page, in each language: name, url, logo, image, telephone, email, address, geo (CONFIRM coordinates), openingHoursSpecification (Monday to Saturday, 09:00 to 19:00), priceRange ("1,300,000–8,400,000 VND"), founders, `sameAs` (Instagram, Facebook, Tripadvisor). `Product` JSON-LD on product pages, with `Offer` from the active data source. `BlogPosting` on Journal posts and `FAQPage` on the FAQ. Never add `aggregateRating` or `review` markup for the Tripadvisor quotes; self-published review markup isn't eligible for stars and can get flagged.
- During the proposal: `noindex`, no sitemap (section 2). At launch (`INDEXABLE=true`): `robots.txt` and `sitemap.xml` with all three languages and `hreflang`.
- A 404 page in the site's style.

## 13. QA

Test, and fix until everything passes:
1. **Responsive:** full-page screenshots of every page in English, plus Home, Suits & Pricing and Contact in Vietnamese and Chinese, at 360, 390, 414, 768, 820, 1024, 1280, 1440 and 1920px, plus 844×390 landscape, saved in `./qa/` (Playwright). Look at them and fix what's off. No horizontal scroll anywhere.
2. **Keyboard and motion:** the menu, language switch, shop filters, FAQ and form are all reachable and usable with visible focus; `prefers-reduced-motion` turns motion off.
3. **Without JavaScript:** all content is visible, the FAQ opens, the shop listing shows products (static HTML at build time), nothing is hidden.
4. **Links:** crawl every internal link and anchor in all three languages; no 404s. Every page's language switch lands on the same page in the other language. Every redirect in section 8.5 returns a 301 to the right page (test `vercel.json` locally with `vercel dev`, or by checking the rules).
5. **Forms:** each validation message in each language; a normal submission (to a test inbox, not the client's, until the client has seen the proposal); the no-JavaScript post; date ordering; the honeypot. Log the WhatsApp URLs and check the decoded text in all three languages.
6. **Shop:** sample data renders; switching `src/config.json` to a mock Store API server (serve the sample JSON locally with the same paths) renders the same pages; "Add to bag" builds the right WooCommerce URL; filters and sorting work; filter state is in the URL.
7. **Content:** prices match 9.2 on every page and in every language; hours, phone and address match section 6 everywhere; review quotes match 9.6 word for word; all seven Journal posts exist in all three languages.
8. **Keywords and copy:** for every page, the primary keyword is in the title, the H1, the first 100 words, at least one H2 and the meta description; the exact primary phrase appears no more than three times in visible copy; every heading and section intro passes the swap test. List the keyword placements for each page in the report.
9. **Performance:** Lighthouse on mobile scores at least 90 for performance and 95 for accessibility and best practices (check one `/zh/` page too, since the Chinese fonts are heavy; subset or use `unicode-range` if needed).
10. **Leftovers and emoji:** search the project for `Haravan`, `hstatic`, `Giỏ hàng`, `Đăng ký`, `Mua ngay`, `cart.general`, `layout.customer`, `#1 bespoke`, `only tailor shop`, `December 20`, `KA HRV`, `Montserrat`, `Tinos`, `Inter` and `gemini_generated`, and review every hit. Search the pages for emoji code points; there must be none (the © in the footer is fine).
11. **Client checklist:** go through section 0 item by item.

## 14. Deliverables

1. The site in `dist/`, deployable to Vercel as-is, and portable to static hosting with the files in `dist/_hosting/`.
2. `COPY.md`, `COPY.vi.md` and `COPY.zh.md`: all final copy by page and section, with the keywords each section targets.
3. `README.md`: how to preview locally, build, deploy to Vercel, move to our hosting, switch `INDEXABLE` for launch, connect the WooCommerce Store API (the WordPress and WooCommerce settings needed, including CORS), and activate FormSubmit.
4. `CONFIRM.md`: every placeholder and assumption, grouped as "Ask the client", "Replace before launch" and "Assumptions made". Start with: which Facebook page is current; the final domain (tailormadesuit.net or phantailor.com) and the shop subdomain; the "since 2013" date; whether to keep the "#1" and "only tailor shop" claims (we've left them out); founders' name order and diacritics; prices for coats, waistcoats, blazers and women's garments; whether to show USD equivalents; Tết and holiday closure dates; international shipping and remote reorders; typical reply time; the ten fabric-brand logos and permission to show mill logos; mill locations; the Journal author of "Suit Jacket vs. Blazer vs. Sport Coat"; AI-generated blog images still in use; all sample shop products; the added form fields; the new FAQ questions 8 to 10; Tripadvisor figures to refresh before launch; Google reviews; map coordinates; native review of the Vietnamese and Chinese copy; the keyword map; every stock photo; the logo tracing result; FormSubmit as a third-party service.
5. `./qa/` screenshots.
6. A short report: what changed from the current site, what was dropped from it and why, and the section 0 checklist with each item confirmed.
