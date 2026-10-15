"""Convert source photos to WebP (max 2000px wide) in assets/img and record sizes in src/data/images.json.
Run: python3 scripts/prepare-images.py"""
import json, os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, '_source')
# name: (source path relative to _source, crop box as fractions (l,t,r,b) or None, origin note)
MAP = {
  'villa-lounge':     ('images/ms_banner_img1.jpg', None, 'client'),
  'showroom':         ('images/blog_banner_1.png', None, 'client'),
  'campaign-group':   ('images/blog_banner_2.png', (0, 0.17, 1, 1), 'client'),
  'hs-cloth-navy':    ('images/breadcrumb_bg1.png', None, 'client (Holland & Sherry cloth image)'),
  'hs-cloth-navy-gl': ('images/breadcrumb_bg1.png', (0, 0, 0.74, 1), 'client (cropped texture for the WebGL cloth)'),
  'linen-swatch':     ('images/20220729_174323_2f258ac34e5443b9ba6f74fd03369472_master.jpeg', None, 'client'),
  'nobility-books':   ('images/screen_shot_2025-08-11_at_21.22.21_e2637d58fc3647ef81653123513e3c73_1024x1024.png', None, 'client'),
  'cavani-blazer':    ('images/screen_shot_2023-10-04_at_13.01.15_f71e29a0c3e741b69db90e5a11fa61ab_master.png', None, 'client (shop product image)'),
}
stock_json = os.path.join(S, 'stock', 'stock.json')
if os.path.exists(stock_json):
  for s in json.load(open(stock_json)):
    MAP['stock-' + os.path.splitext(s['file'])[0]] = ('stock/' + s['file'], None, 'unsplash: ' + s['unsplash_page_url'] + ' / ' + s['photographer'])
out = {}
for name, (src, crop, origin) in MAP.items():
  p = os.path.join(S, src)
  if not os.path.exists(p): print('missing', p); continue
  im = Image.open(p).convert('RGB')
  if crop:
    W, H = im.size; im = im.crop((int(crop[0]*W), int(crop[1]*H), int(crop[2]*W), int(crop[3]*H)))
  # longest side at most 2000px (portraits would otherwise be 3000px tall)
  scale = min(1, 2000 / max(im.size))
  if scale < 1: im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
  dst = os.path.join(ROOT, 'assets', 'img', name + '.webp')
  im.save(dst, 'WEBP', quality=(70 if 'swatch' in name or 'texture' in name else 80), method=6)
  # 900px variant for cards and mobile
  if im.width > 1000:
    sm = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    heavy = any(k in name for k in ('texture', 'swatch', 'linen', 'trousers', 'chalk', 'woman-suit-2'))
    sm.save(os.path.join(ROOT, 'assets', 'img', name + '-900.webp'), 'WEBP', quality=58 if heavy else 78, method=6)
  if im.width > 1500:
    md = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    md.save(os.path.join(ROOT, 'assets', 'img', name + '-1400.webp'), 'WEBP', quality=60 if any(k in name for k in ('texture', 'swatch', 'linen', 'trousers', 'chalk', 'woman-suit-2')) else 68, method=6)
  out[name] = {'w': im.width, 'h': im.height, 'small': im.width > 1000, 'mid': im.width > 1500, 'origin': origin}
  print(name, im.size, os.path.getsize(dst)//1024, 'KB')
json.dump(out, open(os.path.join(ROOT, 'src', 'data', 'images.json'), 'w'), indent=1)
