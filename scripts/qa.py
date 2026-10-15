"""QA for the built site. Serve dist/ first:  (cd dist && python3 -m http.server 4321)
Run:  python3 scripts/qa.py [--shots]
--shots also saves full-page screenshots at every breakpoint into qa/."""
import json, os, re, sys, glob, urllib.parse
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
BASE = 'http://localhost:4321'
fails, notes = [], []
def fail(msg): fails.append(msg); print('FAIL', msg)
def ok(msg): print('ok  ', msg)

pages = sorted('/' + os.path.relpath(p, DIST).replace('index.html', '') for p in glob.glob(f'{DIST}/**/index.html', recursive=True))
pages = [p if p.endswith('/') else p + '/' for p in pages]
pages = ['/' if p == '/./' else p for p in pages]

# ---------- 1. Static checks: links, anchors, emoji, leftovers ----------
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links = []; s.ids = set(); s.text = []; s.skip = 0
    def handle_starttag(s, t, a):
        a = dict(a)
        if 'id' in a: s.ids.add(a['id'])
        if t == 'a' and a.get('href'): s.links.append(a['href'])
        if t in ('script', 'style'): s.skip += 1
    def handle_endtag(s, t):
        if t in ('script', 'style'): s.skip -= 1
    def handle_data(s, d):
        if not s.skip: s.text.append(d)
parsed = {}
for p in pages:
    h = open(os.path.join(DIST, p.strip('/'), 'index.html') if p != '/' else os.path.join(DIST, 'index.html'), encoding='utf-8').read()
    x = P(); x.feed(h); parsed[p] = (h, x)
broken = set()
for p, (h, x) in parsed.items():
    for l in x.links:
        if l.startswith(('http', 'mailto:', 'tel:')): continue
        path, _, frag = l.partition('#')
        target = path or p
        if target not in parsed: broken.add(f'{p} -> {l}')
        elif frag and frag not in parsed[target][1].ids: broken.add(f'{p} -> {l} (missing anchor)')
(fail if broken else ok)(f'internal links and anchors across {len(pages)} pages' + (': ' + '; '.join(sorted(broken)[:10]) if broken else ''))

EMO = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️←-⇿]')
emo = [f'{p}: {m}' for p, (h, x) in parsed.items() for m in EMO.findall(h)]
(fail if emo else ok)('no emoji or pictographic symbols in pages' + (': ' + ', '.join(emo[:10]) if emo else ''))

LEFT = ['Haravan', 'hstatic', 'Giỏ hàng', 'Đăng ký', 'Mua ngay', 'cart.general', 'layout.customer', '#1 bespoke', 'only tailor shop', 'December 20', 'KA HRV', 'Montserrat', 'Tinos', "'Inter'", 'Cormorant', 'Be Vietnam', 'gemini_generated', 'lorem', 'TODO']
hits = [f'{w} in {p}' for p, (h, x) in parsed.items() for w in LEFT if w.lower() in h.lower()]
(fail if hits else ok)('no leftovers from the old site' + (': ' + '; '.join(hits[:10]) if hits else ''))

banned = ['experience the ultimate', 'discover', 'unlock', 'elevate', 'indulge', 'treat yourself', 'seamless', 'curated', 'holistic', 'cutting-edge', 'state-of-the-art', 'world-class', 'unparalleled', 'one-stop', 'sanctuary']
en_pages = [p for p in parsed if not p.startswith(('/vi/', '/zh/')) and '/journal/' not in p]
bhits = [f'"{w}" on {p}' for p in en_pages for w in banned if re.search(r'\b' + re.escape(w) + r'\b', ' '.join(parsed[p][1].text).lower())]
(fail if bhits else ok)('no banned marketing words in English page copy' + (': ' + '; '.join(bhits) if bhits else ''))

# Prices consistent everywhere
for p, (h, x) in parsed.items():
    for bad in ['6,900,000', '8,500,000']:
        if bad in h: fail(f'unexpected price {bad} on {p}')

# ---------- 2. Keyword placement (English) ----------
KW = {
    '/': ['bespoke tailor', 'ho chi minh city'],
    '/about/': ['architect', 'saigon'],
    '/bespoke-process/': ['custom suit', 'made'],
    '/suits-and-pricing/': ['custom suit price', 'ho chi minh city'],
    '/fabrics/': ['suit fabrics', 'saigon'],
    '/shop/': ['nobility', 'fabric'],
    '/journal/': ['menswear style guide'],
    '/faq/': ['suit made in vietnam'],
    '/contact/': ['saigon pearl', 'bình thạnh'],
}
report = []
for p, kws in KW.items():
    h, x = parsed[p]
    title = re.search(r'<title>(.*?)</title>', h).group(1).lower()
    desc = re.search(r'<meta name="description" content="(.*?)"', h).group(1).lower()
    h1 = re.sub('<[^>]+>', ' ', re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S).group(1)).lower()
    main = re.sub(r'(?s)<header.*?</header>', '', h)
    main = re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', '', main)
    body_txt = re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', main)).lower()
    words = body_txt.split()
    first100 = ' '.join(words[:130])
    h2s = ' '.join(re.sub('<[^>]+>', ' ', m) for m in re.findall(r'<h2[^>]*>(.*?)</h2>', main, re.S)).lower()
    def has(t): return any(k in t for k in kws)
    res = {'title': all(k in title for k in kws[:1]), 'h1': has(h1), 'first100': has(first100), 'h2/intro': has(h2s) or has(first100), 'meta': has(desc)}
    report.append((p, res))
    if not all(res.values()): notes.append(f'keyword placement weak on {p}: {res}')
print('keyword placement:', json.dumps(report, ensure_ascii=False))

# ---------- 3. Browser checks ----------
WIDTHS = [360, 390, 414, 768, 820, 1024, 1280, 1440, 1920]
shots = '--shots' in sys.argv
with sync_playwright() as pw:
    br = pw.chromium.launch()
    # Responsive overflow (and screenshots)
    targets = [p for p in pages if not p.startswith(('/vi/', '/zh/'))] + ['/vi/', '/vi/suits-and-pricing/', '/vi/contact/', '/zh/', '/zh/suits-and-pricing/', '/zh/contact/']
    over = []
    for w in WIDTHS + ['844x390']:
        vw, vh = (844, 390) if w == '844x390' else (w, 900)
        pg = br.new_page(viewport={'width': vw, 'height': vh})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'favicon' not in m.text else None)
        for p in targets if shots or w in (360, 768, 1440) else []:
            pg.goto(BASE + p, wait_until='domcontentloaded')
            pg.wait_for_timeout(150)
            sw = pg.evaluate('document.documentElement.scrollWidth')
            if sw > vw: over.append(f'{p}@{w} ({sw}px)')
            if shots:
                pg.evaluate('async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,30));}window.scrollTo(0,0);}')
                pg.wait_for_timeout(250)
                os.makedirs(f'{ROOT}/qa/{w}', exist_ok=True)
                try:
                    pg.screenshot(path=f"{ROOT}/qa/{w}/{(p.strip('/').replace('/', '_') or 'home')}.png", full_page=True, timeout=90000)
                except Exception as e:
                    notes.append(f'screenshot skipped {p}@{w}: {str(e)[:60]}')
        real = [e for e in errs if 'ERR_' not in e and 'google' not in e.lower()]
        if real: fail(f'console errors at {w}: {real[:3]}')
        pg.close()
    (fail if over else ok)('no horizontal scroll' + (': ' + ', '.join(over) if over else ''))

    # Motion layer: after scrolling through, nothing in <main> may stay hidden
    mpg = br.new_page(viewport={'width': 1440, 'height': 900})
    stuck = []
    for p in ['/', '/about/', '/suits-and-pricing/', '/fabrics/', '/shop/', '/journal/', '/faq/', '/contact/', '/zh/']:
        mpg.goto(BASE + p); mpg.wait_for_timeout(1500)
        mpg.evaluate('async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,80));}window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,1800));}')
        stuck += [p + ' ' + x for x in mpg.evaluate('''()=>[...document.querySelectorAll('main h1,main h2,main h3,main p,main li,main img,main a')].filter(e=>{const s=getComputedStyle(e);return (s.visibility==='hidden'||+s.opacity<0.05)&&e.offsetParent!==null&&!e.closest('.pct-gl-on')}).slice(0,3).map(e=>e.tagName+' '+(e.textContent||'').trim().slice(0,30))''')]
    (fail if stuck else ok)('motion layer: everything revealed after scrolling' + (': ' + '; '.join(stuck) if stuck else ''))
    mpg.close()

    # Functional checks run with reduced motion (motion layer off), so clicks and counts are immediate
    fctx = br.new_context(reduced_motion='reduce', viewport={'width': 1280, 'height': 900})
    pg = fctx.new_page()
    # Language switch keeps the page
    pg.goto(BASE + '/suits-and-pricing/')
    pg.click('[data-pct-lang] button'); pg.click('[data-pct-lang] a[hreflang="vi"]'); pg.wait_for_load_state()
    (ok if pg.url.endswith('/vi/suits-and-pricing/') else fail)(f'language switch keeps the page ({pg.url})')
    # hreflang present
    alts = pg.eval_on_selector_all('link[rel=alternate]', 'els=>els.map(e=>e.hreflang)')
    (ok if set(alts) >= {'en', 'vi', 'zh-Hans', 'x-default'} else fail)(f'hreflang alternates {alts}')

    # Shop filters + URL state
    pg.goto(BASE + '/shop/')
    total = pg.locator('[data-pct-product]:visible').count()
    pg.check('input[name=cat][value="ready-made"]')
    rm = pg.locator('[data-pct-product]:visible').count()
    (ok if 0 < rm < total and 'cat=ready-made' in pg.url else fail)(f'shop category filter ({total} -> {rm}, url {pg.url})')
    pg.goto(BASE + '/shop/?cat=nobility-fabrics&colour=navy')
    n = pg.locator('[data-pct-product]:visible').count()
    (ok if n == 1 else fail)(f'shop filters restored from URL (navy Nobility = {n})')
    pg.goto(BASE + '/shop/?price=6000000-')
    n = pg.locator('[data-pct-product]:visible').count(); e = pg.locator('[data-pct-empty]').is_visible()
    (ok if n == 0 and e else fail)(f'empty state for price over 6M ({n} shown, empty visible {e})')
    pg.goto(BASE + '/shop/')
    first = pg.locator('[data-pct-product] h3').first.inner_text()
    (ok if 'Cavani' in first else fail)(f'featured sort shows the real product first ({first})')

    # Add to bag in proposal mode
    pg.goto(BASE + '/shop/men-linen-blazer-green-linen-cavani-2-button-slim-fit/')
    href = pg.get_attribute('[data-pct-bag]', 'href')
    (ok if href.startswith('https://wa.me/84826977888') else fail)(f'add to bag falls back to WhatsApp in proposal mode: {urllib.parse.unquote(href)}')

    # WhatsApp prefill text in each language
    for lang in ['', 'vi/', 'zh/']:
        pg.goto(f'{BASE}/{lang}contact/')
        u = pg.get_attribute('a[data-pct-where="contact"][data-pct-track="whatsapp_click"]', 'href')
        txt = urllib.parse.unquote(u.split('text=')[1])
        (ok if txt and not EMO.search(txt) else fail)(f'WhatsApp prefill /{lang}: "{txt}"')

    # Form validation and submission (FormSubmit is intercepted, nothing is sent)
    pg.goto(BASE + '/contact/')
    posted = []
    pg.route('https://formsubmit.co/**', lambda route: (posted.append(route.request.post_data or ''), route.fulfill(status=200, content_type='application/json', body='{"success":"true"}')))
    pg.click('form[data-pct-form] button[type=submit]')
    errs = pg.locator('.pct-error:visible').all_inner_texts()
    (ok if len(errs) == 3 else fail)(f'empty submit shows 3 inline errors: {errs}')
    pg.fill('#pct-name', 'Test Visitor'); pg.fill('#pct-email', 'not-an-email'); pg.fill('#pct-phone', '12'); pg.fill('#pct-message', 'A navy 2-piece suit.')
    pg.fill('#pct-arrive', '2026-11-10'); pg.fill('#pct-leave', '2026-11-05')
    pg.click('form[data-pct-form] button[type=submit]')
    errs = pg.locator('.pct-error:visible').all_inner_texts()
    (ok if len(errs) == 3 else fail)(f'bad email, short phone and reversed dates flagged: {errs}')
    pg.fill('#pct-email', 'visitor@example.com'); pg.fill('#pct-phone', '+44 7700 900123'); pg.fill('#pct-leave', '2026-11-15')
    pg.click('label.pct-check:has-text("2-piece suit")'); pg.click('label.pct-check:has-text("Shirt")')
    pg.click('form[data-pct-form] button[type=submit]')
    pg.wait_for_url('**/contact/thank-you/', timeout=5000)
    body = posted[0] if posted else ''
    good = posted and 'visitor@example.com' in body and '2-piece suit, Shirt' in body and '_subject' in body
    (ok if good else fail)(f'valid submit posts to FormSubmit ajax and lands on thank-you ({len(body)} bytes)')
    dl = pg.evaluate('window.dataLayer') if pg.url else None

    # dataLayer events on clicks
    pg.goto(BASE + '/')
    pg.evaluate("document.querySelectorAll('a[target=_blank]').forEach(a=>a.removeAttribute('target'))")
    pg.evaluate("document.querySelector('[data-pct-where=hero][data-pct-track=book_click]').addEventListener('click',e=>e.preventDefault())")
    pg.click('[data-pct-where=hero][data-pct-track=book_click]')
    ev = pg.evaluate('window.dataLayer.map(e=>e.event)')
    (ok if 'book_click' in ev else fail)(f'dataLayer gets book_click ({ev})')

    # Mobile menu + keyboard
    m = fctx.new_page(); m.set_viewport_size({'width': 390, 'height': 800})
    m.goto(BASE + '/')
    m.click('[data-pct-menu-open]')
    m.wait_for_timeout(500)
    vis = m.locator('.pct-menu__list a').first.is_visible()
    m.keyboard.press('Escape')
    m.wait_for_timeout(500)
    closed = not m.locator('[data-pct-menu]').evaluate('e=>e.classList.contains("pct-is-open")') and not m.locator('.pct-menu__list a').first.is_visible()
    (ok if vis and closed else fail)(f'mobile menu opens and closes with Escape ({vis}, {closed})')
    m.goto(BASE + '/')
    m.keyboard.press('Tab')
    f1 = m.evaluate('document.activeElement.className')
    (ok if 'pct-skip' in f1 else fail)(f'first Tab reaches the skip link ({f1})')
    m.close()

    # Without JavaScript
    ctx = br.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 800})
    nj = ctx.new_page()
    nj.goto(BASE + '/shop/')
    cnt = nj.locator('[data-pct-product]:visible').count()
    nj.goto(BASE + '/faq/')
    nj.locator('summary').nth(2).evaluate("e=>e.scrollIntoView({block:'center'})")
    nj.click('summary >> nth=2')
    opened = nj.locator('details >> nth=2').get_attribute('open') is not None
    nj.goto(BASE + '/')
    hero = nj.locator('.pct-hero h1').is_visible() and nj.locator('.pct-hero__links a').first.is_visible()
    nj.click('[data-pct-menu-open]'); nj.wait_for_timeout(500)
    drawer = nj.locator('.pct-menu__list a').first.is_visible()
    (ok if cnt == 7 and opened and hero and drawer else fail)(f'without JS: products {cnt}, FAQ opens {opened}, hero visible {hero}, mobile nav visible {drawer}')
    ctx.close()

    # Reduced motion: hero animation off
    rm_ctx = br.new_context(reduced_motion='reduce'); r = rm_ctx.new_page(); r.goto(BASE + '/')
    anim = r.evaluate("getComputedStyle(document.querySelector('.pct-hero__media img')).animationName")
    (ok if anim == 'none' else fail)(f'prefers-reduced-motion turns off the hero motion ({anim})')
    rm_ctx.close()
    br.close()

print('\n' + ('ALL CHECKS PASSED' if not fails else f'{len(fails)} FAILED'))
for n in notes: print('NOTE', n)
sys.exit(1 if fails else 0)
