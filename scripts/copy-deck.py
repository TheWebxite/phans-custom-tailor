"""Write COPY.md, COPY.vi.md and COPY.zh.md from src/i18n, page by page, with target keywords.
Run: python3 scripts/copy-deck.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KW = {
  'en': {
    'home': ('bespoke tailor Ho Chi Minh City', 'custom suit Saigon, tailor in Saigon, tailor-made suit Vietnam, suit tailor HCMC'),
    'about': ('architect-trained tailors in Saigon', 'Thinh and Thuong Phan, family tailoring, Saigon Pearl villa'),
    'process': ('how a custom suit is made', 'suit fitting, made-to-measure process, measurements, lifetime alterations'),
    'pricing': ('custom suit price in Ho Chi Minh City', '2-piece suit price, 3-piece suit, tailored shirt, dress trousers, women\'s suit tailor, wedding suit'),
    'fabrics': ('suit fabrics in Saigon', 'Vitale Barberis Canonico, Holland & Sherry, linen suit, wool suit, cashmere, Nobility fabric'),
    'shop': ('Nobility suit fabric', 'buy suit fabric Vietnam, linen blazer, ready-made blazer'),
    'journal': ('menswear style guide', 'blazer vs suit jacket, summer suit fabric, suit mistakes'),
    'faq': ('getting a suit made in Vietnam', 'how long to make a suit in Vietnam, tailor appointment Saigon, alterations'),
    'contact': ('tailor in Bình Thạnh, Saigon Pearl', 'book tailor appointment Saigon, Ho Chi Minh City tailor address'),
  },
  'vi': {
    'home': ('may đo vest TP.HCM', 'tiệm may âu phục Sài Gòn, may suit nam cao cấp'),
    'about': ('thợ may xuất thân kiến trúc sư', 'Phan Thịnh, Phan Thương, Saigon Pearl'),
    'process': ('quy trình may đo vest', 'thử đồ, số đo, chỉnh sửa trọn đời'),
    'pricing': ('giá may vest TP.HCM', 'may vest cưới, may đo áo sơ mi, may suit nam cao cấp'),
    'fabrics': ('vải may vest', 'Vitale Barberis Canonico, Holland & Sherry, Nobility, linen'),
    'shop': ('vải Nobility', 'vải may suit, áo blazer may sẵn'),
    'journal': ('cẩm nang thời trang nam', 'blazer, áo vest, vải mùa hè'),
    'faq': ('may vest ở Việt Nam', 'đặt lịch may đo, thời gian may'),
    'contact': ('tiệm may Bình Thạnh, Saigon Pearl', 'đặt lịch, địa chỉ tiệm may'),
  },
  'zh': {
    'home': ('胡志明市 定制西装', '西贡 裁缝, 量身定制西服'),
    'about': ('建筑师出身的裁缝', 'Thinh Phan, Thuong Phan, Saigon Pearl'),
    'process': ('定制西装流程', '试衣, 量体, 终身免费修改'),
    'pricing': ('胡志明市定制西装价格', '两件套西装, 三件套西装, 手工定制衬衫'),
    'fabrics': ('西装面料', 'Vitale Barberis Canonico, Holland & Sherry, Nobility, 亚麻'),
    'shop': ('Nobility 西装面料', '西装面料购买, 成衣西装外套'),
    'journal': ('男士着装指南', '西装外套, 夏季西装面料'),
    'faq': ('在越南定制西装', '定制西装需要多久, 预约裁缝'),
    'contact': ('西贡 裁缝 平盛郡', '预约, 地址'),
  },
}
SECTIONS = {
  'home': ['home', 'steps', 'prices', 'bookBand'],
  'about': ['about'],
  'process': ['process', 'steps'],
  'pricing': ['pricing', 'prices'],
  'fabrics': ['fabrics'],
  'shop': ['shop'],
  'journal': ['journal'],
  'faq': ['faq'],
  'contact': ['contact', 'form', 'thanks'],
}
def dump(v, depth=0):
  pad = '  ' * depth
  if isinstance(v, dict):
    out = []
    for k, x in v.items():
      if k in ('slug',): continue
      if isinstance(x, (dict, list)): out.append(f'{pad}- **{k}**'); out += dump(x, depth + 1)
      else: out.append(f'{pad}- **{k}:** {x}')
    return out
  if isinstance(v, list):
    out = []
    for i, x in enumerate(v):
      if isinstance(x, (dict, list)): out.append(f'{pad}- {i + 1}.'); out += dump(x, depth + 1)
      else: out.append(f'{pad}- {x}')
    return out
  return [f'{pad}- {v}']
for lang, fname in (('en', 'COPY.md'), ('vi', 'COPY.vi.md'), ('zh', 'COPY.zh.md')):
  T = json.load(open(f'{ROOT}/src/i18n/{lang}.json'))
  lines = [f"# Phan's Custom Tailor: copy deck ({T['label']})", '',
           'Generated from `src/i18n/' + lang + '.json` by `scripts/copy-deck.py`. Edit the JSON, then rebuild and regenerate this file.',
           'Journal articles live in `src/data/journal/`; product copy in `src/data/products.sample.json`.', '']
  if lang != 'en': lines += ['**Pending native review.** We wrote this translation ourselves; see CONFIRM.md for the phrases to check.', '']
  lines += ['## Keyword map', '', '| Page | Primary keyword | Secondary keywords |', '|---|---|---|']
  lines += [f'| {k} | {p} | {s} |' for k, (p, s) in KW[lang].items()]
  lines += ['']
  for page, keys in SECTIONS.items():
    meta = T['pages'][page]
    lines += [f'## {T["nav"].get(page, page)} (`/{meta["slug"]}`)', '', f'Primary keyword: **{KW[lang][page][0]}**', '',
              f'- **SEO title:** {meta["title"]}', f'- **Meta description:** {meta["description"]}', '']
    for k in keys:
      lines += [f'### {k}', ''] + dump(T[k]) + ['']
  lines += ['## Shared', '', '### Navigation', ''] + dump(T['nav']) + ['', '### Buttons and labels', ''] + dump(T['ui']) + ['', '### Footer', ''] + dump(T['footer']) + ['']
  open(f'{ROOT}/{fname}', 'w').write('\n'.join(lines))
  print('wrote', fname)
