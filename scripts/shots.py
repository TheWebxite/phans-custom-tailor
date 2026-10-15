"""Full-page screenshots of the main pages at every breakpoint into qa/<width>/. Serve dist/ on :4321 first."""
import os, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['/', '/about/', '/bespoke-process/', '/suits-and-pricing/', '/fabrics/', '/shop/', '/shop/men-linen-blazer-green-linen-cavani-2-button-slim-fit/',
         '/journal/', '/journal/the-story-of-nobility-weaving-heritage-technology-and-timeless-styl/', '/faq/', '/contact/', '/contact/thank-you/',
         '/vi/', '/vi/suits-and-pricing/', '/vi/contact/', '/zh/', '/zh/suits-and-pricing/', '/zh/contact/']
SIZES = [(360, 800), (390, 844), (414, 896), (768, 1024), (820, 1180), (1024, 1366), (1280, 800), (1440, 900), (1920, 1080), (844, 390)]
with sync_playwright() as p:
  b = p.chromium.launch()
  for w, h in SIZES:
    label = f'{w}x{h}' if w > h and w == 844 else str(w)
    os.makedirs(f'{ROOT}/qa/{label}', exist_ok=True)
    pg = b.new_page(viewport={'width': w, 'height': h})
    for path in PAGES:
      try:
        pg.goto('http://localhost:4321' + path, wait_until='domcontentloaded', timeout=30000)
        pg.evaluate('async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,30));}window.scrollTo(0,0);}')
        pg.wait_for_timeout(250)
        pg.screenshot(path=f"{ROOT}/qa/{label}/{(path.strip('/').replace('/', '_') or 'home')}.png", full_page=True, timeout=60000)
      except Exception as e:
        print('skip', label, path, str(e)[:80], flush=True)
    pg.close(); print('done', label, flush=True)
  b.close()
