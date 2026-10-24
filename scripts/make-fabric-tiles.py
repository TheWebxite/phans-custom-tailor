"""Seamless fabric tiles for the suit configurator (assets/img/cfg/).
Flat cloth photos (linen): lighting flattened, then cross-faded with a half-offset copy so they wrap.
Everything else is woven in code (twill, flannel, stripes, checks) so it repeats cleanly.
These are illustrations until Phan's sends photos of their own cloth.
Run: /Users/hengzhexin/anaconda3/bin/python3 scripts/make-fabric-tiles.py"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets/img')
OUT = os.path.join(ROOT, 'assets/img/cfg')
os.makedirs(OUT, exist_ok=True)
N = 256
rng = np.random.default_rng(7)

def save(k, arr):
  Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(os.path.join(OUT, f'{k}.jpg'), quality=88)

def flatten(img):
  a = np.asarray(img).astype(np.float32)
  blur = np.asarray(img.filter(ImageFilter.GaussianBlur(40))).astype(np.float32)
  return Image.fromarray(np.clip(a - blur + a.reshape(-1, 3).mean(0), 0, 255).astype(np.uint8))

def seamless(img):
  a = np.asarray(img.resize((N, N), Image.LANCZOS)).astype(np.float32)
  b = np.roll(np.roll(a, N // 2, 0), N // 2, 1)
  y, x = np.mgrid[0:N, 0:N] / (N - 1)
  m = np.clip(np.minimum(np.minimum(x, 1 - x), np.minimum(y, 1 - y)) * 3.2, 0, 1)[..., None]
  return a * m + b * (1 - m)

for k, f, box in [('green-linen', 'linen-swatch.webp', (950, 250, 1650, 950)),
                  ('beige-linen', 'stock-linen-2.webp', (300, 250, 1000, 950))]:
  save(k, seamless(flatten(Image.open(os.path.join(SRC, f)).convert('RGB').crop(box))))

def noise(s=1.0):
  n = rng.normal(0, 1, (N, N)).astype(np.float32)
  for ax in (0, 1):
    n = (np.roll(n, 1, ax) + n + np.roll(n, -1, ax)) / 3
  return n * s

def twill(base, amp=6, period=4, grain=6):
  y, x = np.mgrid[0:N, 0:N]
  t = np.sin(2 * np.pi * (x + y) / period) * amp
  return np.array(base, np.float32)[None, None, :] + (t + noise(grain))[..., None]

def blend(a, col, w, k=0.85):
  return a * (1 - w[..., None] * k) + np.array(col, np.float32)[None, None, :] * (w[..., None] * k)

def dist(every):
  x = np.arange(N)
  return np.minimum(x % every, every - x % every).astype(np.float32)

save('navy-twill', twill((30, 40, 66), 6, 4, 5))
save('mid-grey', twill((118, 120, 124), 7, 4, 7))
save('light-grey', twill((176, 177, 181), 6, 4, 6))
save('black', twill((22, 22, 25), 4, 4, 4))
save('camel', twill((172, 126, 86), 7, 5, 7))
save('dark-brown', twill((68, 47, 36), 6, 5, 6))
fl = Image.fromarray(np.clip(twill((58, 59, 62), 3, 5, 10), 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
save('charcoal-flannel', np.asarray(fl).astype(np.float32))

d = dist(32); save('navy-pinstripe', blend(twill((28, 37, 62), 5, 4, 5), (190, 196, 210), np.broadcast_to(np.clip(1 - d / 1.2, 0, 1), (N, N))))
d = dist(64); chalk = np.clip(1 - d / 5, 0, 1)[None, :] * (0.6 + 0.4 * (noise(1.2) > -0.3))
save('grey-chalk', blend(twill((84, 86, 92), 5, 4, 5), (214, 214, 214), chalk, 0.7))

d = dist(64); w = np.maximum(np.clip(1 - d / 1.6, 0, 1)[None, :], np.clip(1 - d / 1.6, 0, 1)[:, None])
save('navy-check', blend(twill((26, 34, 56), 5, 4, 5), (110, 150, 200), w, 0.8))

# glen check: blocks of fine stripes crossing, plus an overcheck
x = np.arange(N); fine = ((x // 3) % 2 == 0).astype(np.float32); grp = ((x % 64) < 28).astype(np.float32)
gx = (fine * grp)[None, :]; gy = (fine * grp)[:, None]
glen = np.clip(0.45 * gx + 0.45 * gy, 0, 1)
over = np.maximum(np.clip(1 - dist(128) / 1.3, 0, 1)[None, :], np.clip(1 - dist(128) / 1.3, 0, 1)[:, None])
g = blend(twill((70, 72, 78), 4, 4, 5), (150, 152, 158), glen, 0.75)
save('grey-glen', blend(g, (96, 120, 160), over, 0.7))
print('tiles:', sorted(os.listdir(OUT)))
