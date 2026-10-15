# Phan's Custom Tailor: items to confirm

Everything on the proposal site that is a placeholder, an assumption or needs the client's OK. The code marks each one with a `<!-- CONFIRM: ... -->` or `<!-- PLACEHOLDER -->` comment; strip those comments before launch.

## Ask the client

1. **Facebook page:** the old site links both facebook.com/phanstailor and facebook.com/phantailor. We used **phanstailor**. Which one is current?
2. **Domain:** the site is built for **tailormadesuit.net**, but the email is @phantailor.com. Which domain should the new site go on? Is the shop subdomain `shop.tailormadesuit.net`?
3. **"Since 2013":** this comes from the old About page and appears on the new About page. Is it correct?
4. **Claims left out:** we did not use "#1 bespoke tailor in Ho Chi Minh City" or "the only tailor shop in Saigon where both founders are architecture graduates". Neither can be verified. Does the client want either back, and on what evidence?
5. **Founders' names:**
   - English uses Thinh Phan and Thuong Phan.
   - Vietnamese uses Phan Thịnh and Phan Thương ("anh Phan Thịnh và chị Phan Thương").
   - Chinese uses Thinh Phan 先生 and Thuong Phan 女士.
   - Are the order and diacritics right?
6. **Prices still missing:** blazer or sport coat, waistcoat, overcoat, and all women's garments currently show "Price on consultation".
7. **Currency:** prices are shown in VND only. Should we show approximate USD, and if so at what rate and with what wording?
8. **Holiday closures:** the Contact page and FAQ say the shop closes for about two weeks over Tết. What are the dates for 2027, and which other public holidays does the shop close?
9. **Remote reorders:** the FAQ answer to "Can I reorder after I leave Vietnam?" only says the pattern is kept on file. Do they ship abroad? How do remote reorders and payment work?
10. **Reply time:** how quickly does the team usually reply to enquiries? We haven't stated a time anywhere.
11. **Fabric mills:**
    - The old home page showed ten logos: Charles Clayton, Lanificio F.lli Cerruti, Dolce & Taylor, Vitale Barberis Canonico, Snow Berry Uno (D&T), Ermenegildo Zegna, Loro Piana, Luciano Explorer and Lord & Taylor Xtra, plus one unidentified striped image (`brand_img4`).
    - The new site names only the mills confirmed in their FAQ (Vitale Barberis Canonico and Holland & Sherry) plus Nobility.
    - Which other mills do they actually stock? Do they have permission to show mill logos? (We use text names only.)
12. **Mill origins:** the Fabrics page labels them "Italy" (VBC), "England" (Holland & Sherry) and "Our own range" (Nobility). Nobility's description ("Italian-inspired designs woven by Kindawool from Australian Merino") comes from their own Journal post. Is that accurate?
13. **Women's tailoring:** Tripadvisor describes the business as "for men", but the client's FAQ says they tailor for women too. We followed the FAQ.
14. **Turnaround:** we state "5 working days as standard, rush orders on request". Reviews mention 2 to 4 days, but we didn't promise faster.
15. **Landmark 81:** the About page says the villa is "a few minutes from Landmark 81", based on Tripadvisor's map. Is that OK to say?
16. **Journal author:** the byline on "Suit Jacket vs. Blazer vs. Sport Coat" was "KA HRV" on the old site, which looks like an admin account. We credited it to Phan's Custom Tailor. Which founder wrote it?
17. **Google reviews:** Google Maps shows Phan's Custom Tailor at **4.9 from 1,115 reviews**, as of October 2026. The site currently quotes only Tripadvisor (4.8 from 975). Does the client want Google's rating shown too, and the Google Business Profile link added?

## Replace before launch

1. **Sample shop products:** six are placeholders, all marked "Sample product" on the site, priced "Price to be confirmed" and set to `"sample": true`:
   - Nobility All Seasons Pure Wool, Navy
   - Nobility All Seasons Wool Blend, Mid Grey
   - Nobility Autumn and Winter Flannel, Charcoal
   - Nobility Pure Linen, Green
   - Grey Wool Blazer
   - White Poplin Dress Shirt

   Only the **Cavani green linen blazer** (5,400,000 VND, sizes M to XXL) is real, taken from the old shop. The old shop showed 5,900,000 VND for some sizes; confirm the price per size.
2. **Stock photos:** 23 Unsplash photos are in use, listed below. All are free-licence, with sources in `_source/stock/stock.json`. Replace them with the client's own photos where possible, starting with the hero, the fitting and the founder shots. The client's Instagram (@phanstailor) is the obvious source.

   | File | What it shows | Photographer, page |
   |---|---|---|
   | stock-hero-workroom-1 (home hero, share image) | Shears on navy cloth | SIL Group, unsplash.com/photos/oshVSMH6JZQ |
   | stock-hero-workroom-3 | Buttons on a swatch card | Yasamine June, unsplash.com/photos/U4Ewfl8ewq0 |
   | stock-fitting-1 | Adjusting a jacket lapel | Tai's Captures, unsplash.com/photos/eLfDCe9Prr8 |
   | stock-fitting-2 | Jacket fitting, black and white | Lisa Marie Theck, unsplash.com/photos/Ri3KQSmrvn8 |
   | stock-fabric-swatches-1 | Swatch card | Yasamine June, unsplash.com/photos/SLipZqBFLHU |
   | stock-fabric-swatches-2 | Swatch card | Yasamine June, unsplash.com/photos/Vxuk3rhzVxc |
   | stock-fabric-swatches-3 | Client browsing swatch books | Yasamine June, unsplash.com/photos/-6haRt0Ntyc |
   | stock-wool-texture-1 | Navy check and grey wools | Victor Volkov, unsplash.com/photos/kwpJY3RbObo |
   | stock-chalk-scissors-1 | Chalk-marked tweed | Salvador Godoy, unsplash.com/photos/ksLWYYmK-0k |
   | stock-man-suit-1 | Man in a grey suit with a buttonhole flower | Samantha Gades, unsplash.com/photos/bFYoyKivbmg |
   | stock-man-suit-2 | Lapel and pocket square | Hardini Lestari, unsplash.com/photos/MujZAKea8Lw |
   | stock-woman-suit-1 | Woman in a camel suit | Alekon pictures, unsplash.com/photos/UuFX_dLxDSQ |
   | stock-shirt-detail-2 | Shirts on hangers | Nimble Made, unsplash.com/photos/kY8hmUQV9Ek |
   | stock-linen-1 | Men in linen on a balcony | Fotógrafo Samuel Cruz, unsplash.com/photos/6dwlLzbMYhM |
   | stock-linen-2 | Linen texture | Annie Spratt, unsplash.com/photos/xTaOPMa6wAE |
   | stock-trousers-1 | Trouser hem | Clem Onojeghuo, unsplash.com/photos/kg3N8vqvMd8 |
   | stock-pressing-1 | Pressing a shirt | Dzulfikar Alkautsar, unsplash.com/photos/Bf8ojHnEvVc |
   | stock-stitching-1 | Hand stitching | Elio Santos, unsplash.com/photos/5ZQn_gWKvLE |
   | stock-stitching-2 | Sewing machine on dark wool | Alexander Andrews, unsplash.com/photos/jNKv4QohAk0 |

   Prepared but not currently used: hero-workroom-2, wool-texture-2, woman-suit-2 and shirt-detail-1.
3. **Client photos reused from the old site:**
   - villa lounge
   - showroom
   - Holland & Sherry cloth band
   - green linen swatch
   - Nobility swatch books
   - Cavani blazer product image

   These are low resolution (1024 to 1360px wide); higher-resolution originals would help, especially for the About page band. The Holland & Sherry band is the mill's own marketing image, so confirm it may be used.
4. **AI-generated blog images:** these were not reused. The four Gemini images and the AI-looking blazer, jacket and "golden rule" infographics were replaced by real or stock photos. Journal covers are stock except "The Story of Nobility", which uses the client's own swatch-book photo.
5. **Tripadvisor figures:** "4.8 from 975 reviews" was taken in October 2026. Refresh it before launch, and re-check that every quote in `src/data/reviews.json` matches the live listing.
6. **Map coordinates:** structured data has no `geo` coordinates yet. Add the villa's latitude and longitude.
7. **FormSubmit activation:** see README. Enquiries pass through FormSubmit, a third-party service; check the client is comfortable with that.
8. **Logo:** the SVG wordmark was traced from the 737px PNG and matches it closely, but the original vector file from the client would be better.
9. **Strip comments:** remove all `<!-- CONFIRM ... -->` and `<!-- PLACEHOLDER ... -->` comments, and set `indexable` to true.

## Native review of translations

The Vietnamese and Simplified Chinese copy was written by us; the client did not supply it. A native speaker should read `COPY.vi.md` and `COPY.zh.md`, and the four journal posts we translated ("The Wardrobe Workhorse", "What is a Suit Jacket?", "Suit Jacket vs. Blazer vs. Sport Coat" and "Summer Suiting 2025"). The other three posts use the client's own Vietnamese and Chinese text.

Phrases to check first:

**Vietnamese**
- "Hai nhà sáng lập tự tay cắt và thử" (hero headline)
- "Cắt theo vòng mông, đũng quần và độ dài gấu bạn muốn" (trousers: "rise" and "break")
- "Áo gi-lê" (waistcoat), "Áo măng tô" (overcoat), "mex" (interlinings)
- "cảm giác tay đầy đặn hơn" (a richer handle), "len dệt thưa" (open-weave wool)
- "Bởi" for "By" on articles; "Tác giả" may read better
- "4,8 điểm trên Tripadvisor": this uses a decimal comma
- "vải tuytsi (len pha)" in the suit jacket article

**Chinese**
- "高级定制" for bespoke; "定制流程" for bespoke process
- "Saigon Pearl 区": is 区 the right label for the development?
- "手感更为丰厚" (richer handle), "疏织羊毛" (open-weave wool)
- "新郎及伴郎团" (the groom and the wedding party)
- "裁剪台札记" (Notes from the cutting table)
- "预约到店" (Book an appointment)
- Article terms: 西装上衣 (suit jacket), 西装外套 (blazer), 运动外套 (sport coat), 落单 (the "orphaning" rule)

## Assumptions made

0. **Home hero and menu redesign** (from your feedback):
   - **Hero:** it now uses the client's own campaign photo of four men in suits, from the old site's banner, with the old logo cropped out. Large section links sit bottom-left, Suitsupply-style. Hovering a link folds the photo into that section's photo with a WebGL cloth transition; without WebGL, it's a crossfade. Confirm the client is happy to feature this photo and has the rights to it.
   - **Header:** the inline nav is replaced by a full-screen menu, styled after the Torii reference. It has numbered items, hairline dividers, a hover state that turns the item navy with a "P" monogram, a photo preview per item, socials, languages and booking.

1. **Brief checkpoint:** you said "build it", so we skipped the brief's stop-for-plan step and built using the defaults the brief lists. These decisions are open to change:
   - **Accent colour:** navy `#1E2A3A`, chosen over bottle green.
   - **Fonts:**
     - headings in Prata, body in Hanken Grotesk (both support Vietnamese). This replaced the first choice, Cormorant Garamond with Be Vietnam Pro, after feedback that it looked AI-generated; the comparison is in `_source/font-options/`.
     - on `/zh/`, the reader's system Chinese fonts: PingFang SC or Microsoft YaHei for text, Songti for headings. Latin text keeps the brand fonts. The brief named Noto Serif SC and Noto Sans SC, but they stalled the Chinese pages for over 30 seconds on a throttled mobile connection, so we dropped them.
   - **Motion:** rich, using GSAP and three.js. This changed from the brief's "subtle, no libraries" after feedback that the site felt static. On a slow-4G phone simulation, inner-page titles and images now appear at 2.0 to 2.9s, against 0.9 to 2.3s for the static version. Visitors who set "reduce motion" still get the static site.
   - **Testimonials page:** the old `/pages/testimonials` redirects to the reviews section on Home (`/#reviews`).
   - **Koalendar:** opens in a new tab rather than being embedded.
2. **Proposal mode:** every page is `noindex`, the footer shows "Proposal preview. Not yet live.", and there is no sitemap.
3. **Shop handover:** the shop hands cart and checkout to WooCommerce's own pages. While checkout isn't connected, "Add to bag" opens WhatsApp with the product name.
4. **Enquiry form fields:** Country, the garment choices and the travel dates were added to the client's original Name, Email, Phone and Message fields, to help plan fittings around a visitor's stay. Any of them can be dropped.
5. **New FAQ questions:** three were added:
   - "Can I come on a Sunday or a public holiday?"
   - "Where are you, and is there parking?"
   - "Can I reorder after I leave Vietnam?"
6. **Reviews language:** reviews stay in English on all three language versions, with a translated note saying they are quoted from Tripadvisor.
7. **Keyword map:** built without search-volume data. It draws on the client's own terms, the Tripadvisor listing and how other HCMC tailors and travel guides phrase things. See `COPY.md`.
8. **Holland & Sherry image:** the cloth band image on Home was cropped to hide the mill's wordmark.
