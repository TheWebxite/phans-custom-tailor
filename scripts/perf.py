"""Rough mobile performance check (slow 4G, 4x CPU) for LCP, CLS and page weight. Serve dist/ on :4321 first."""
import sys
from playwright.sync_api import sync_playwright
PATHS = sys.argv[1:] or ['/', '/zh/', '/vi/', '/suits-and-pricing/', '/shop/', '/fabrics/', '/about/', '/contact/', '/journal/summer-suiting-2025/']
JS = '''()=>new Promise(r=>{let l=0,el='',cls=0;
new PerformanceObserver(x=>{for(const e of x.getEntries()){l=e.startTime;el=(e.url||e.element?.tagName||'').slice(-36)}}).observe({type:'largest-contentful-paint',buffered:true});
new PerformanceObserver(x=>{for(const e of x.getEntries())if(!e.hadRecentInput)cls+=e.value}).observe({type:'layout-shift',buffered:true});
setTimeout(()=>{const kb=Math.round(performance.getEntriesByType('resource').reduce((a,x)=>a+(x.transferSize||0),0)/1024);r({lcp:Math.round(l),el,cls:+cls.toFixed(3),kb})},3000)})'''
with sync_playwright() as p:
  b = p.chromium.launch()
  ctx = b.new_context(viewport={'width': 412, 'height': 823}, device_scale_factor=2.6, is_mobile=True)
  for path in PATHS:
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    cdp.send('Network.enable'); cdp.send('Network.setCacheDisabled', {'cacheDisabled': True})
    cdp.send('Network.emulateNetworkConditions', {'offline': False, 'latency': 150, 'downloadThroughput': 1.6 * 1024 * 1024 / 8, 'uploadThroughput': 750 * 1024 / 8})
    cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
    try:
      pg.goto('http://localhost:4321' + path, wait_until='domcontentloaded', timeout=60000)
      print(path, pg.evaluate(JS), flush=True)
    except Exception as e:
      print(path, 'ERROR', str(e)[:120], flush=True)
    pg.close()
  b.close()
