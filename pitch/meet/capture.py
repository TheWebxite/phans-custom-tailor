"""Fresh screenshots of the demo for the in-person deck (AI try-on widget blocked).
Run from the project root after `node build.mjs`:  python3 pitch/meet/capture.py"""
import os, subprocess, time
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cap')
srv = subprocess.Popen(['python3', '-m', 'http.server', '4399'], cwd=os.path.join(ROOT, 'dist'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
B = 'http://localhost:4399'
DESK = [('d_home', '/', False), ('d_pricing', '/suits-and-pricing/', True), ('d_process', '/bespoke-process/', True),
        ('d_fabrics', '/fabrics/', True), ('d_shop', '/shop/', True), ('d_pdp', '/shop/nobility-all-seasons-pure-wool-navy/', True),
        ('d_contact', '/contact/', True), ('d_about', '/about/', True), ('d_home_full', '/', True), ('d_journal', '/journal/', False),
        ('d_vi_home_full', '/vi/', True)]
PHONE = [('m_vi_home', '/vi/', True), ('m_zh_pricing', '/zh/suits-and-pricing/', True), ('m_en_home', '/', True), ('m_vi_contact', '/vi/contact/', True)]
HIDE = '.cursor,[class*="cursor"]{display:none!important}'
try:
  with sync_playwright() as p:
    b = p.chromium.launch()
    def shoot(name, path, full, vp, dpr, mobile=False):
      ctx = b.new_context(viewport=vp, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile, reduced_motion='reduce')
      ctx.route('**/*decart*/**', lambda r: r.abort()); ctx.route('**/anywear*', lambda r: r.abort())
      pg = ctx.new_page(); pg.goto(B + path, wait_until='networkidle'); pg.add_style_tag(content=HIDE)
      if full:  # trigger lazy images
        h = pg.evaluate('document.body.scrollHeight')
        for y in range(0, h, 600): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(60)
        pg.evaluate('window.scrollTo(0,0)')
      pg.wait_for_timeout(900)
      pg.screenshot(path=f'{OUT}/{name}.png', full_page=full); ctx.close(); print(name)
    for n, u, f in DESK: shoot(n, u, f, {'width': 1440, 'height': 900}, 1.5)
    for n, u, f in PHONE: shoot(n, u, f, {'width': 390, 'height': 844}, 3, True)
    # menu open, desktop
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1.5, reduced_motion='reduce'); ctx.route('**/anywear*', lambda r: r.abort())
    pg = ctx.new_page(); pg.goto(B + '/', wait_until='networkidle'); pg.add_style_tag(content=HIDE)
    btn = pg.locator('button[aria-controls], .menu-toggle, [data-menu-open]').first; btn.click(); pg.wait_for_timeout(1200)
    pg.screenshot(path=f'{OUT}/d_menu.png'); print('d_menu')
    b.close()
finally:
  srv.terminate()
