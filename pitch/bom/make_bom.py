"""Phan's website BOM (VI for the client, EN copy for Xin): editable .xlsx + .pdf from one spec.
Run from anywhere: /Users/hengzhexin/anaconda3/bin/python3 pitch/bom/make_bom.py
The xlsx comes from build_bom.py (TWX house format, formulas driven by the rate cell). LibreOffice isn't
installed on this Mac, so the PDF is rendered from the same spec with Playwright; the totals use the same
arithmetic as the xlsx formulas. Edit RATE / items here, never the outputs."""
import os, sys, json, html, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, HERE)
import build_bom
from playwright.sync_api import sync_playwright

RATE = 3_000_000          # VND per man-day; 4.0 MD = 12,000,000 VND (Xin, 2026-10-23)
DEPOSIT = 50

def spec(L):
  t = lambda vi, en: vi if L == 'vi' else en
  return {
    'output_name': t("Bao gia website Phan's", "Phans website quotation EN"),
    'title': t('THEWEBXITE — BẢNG BÁO GIÁ', 'THEWEBXITE — BILL OF MATERIALS'),
    'subtitle': t("Website Phan's Custom Tailor (giai đoạn 1)", "Phan's Custom Tailor website (phase 1)"),
    'currency_format': '#,##0" ₫"',
    'rate': RATE, 'deposit_pct': DEPOSIT,
    'meta': {
      t('Ngày', 'Date'): t('23/10/2026', '23 October 2026'),
      t('Khách hàng', 'Client'): "Phan's Custom Tailor (anh Phan Thịnh, chị Phan Thương)",
      t('Dự án', 'Project'): t('Hoàn thiện bản mẫu thành website chính thức ba ngôn ngữ, có tích hợp phòng thử đồ AI', 'Turn the mock-up into the official three-language website, with the AI fitting room integrated'),
      t('Người lập', 'Prepared By'): 'Xin, TheWebxite',
    },
    'labels': {
      'rate': t('ĐƠN GIÁ', 'RATE'), 'rate_desc': t('Đơn giá một ngày công', 'Man-day rate'),
      'no': t('STT', 'No.'), 'desc': t('Hạng mục', 'Description'), 'md': t('Ngày công', 'MD'),
      'unit': t('Đơn giá', 'Unit Price'), 'amount': t('Thành tiền', 'Amount'), 'subtotal': t('Cộng', 'Subtotal'),
      'total_md': t('TỔNG NGÀY CÔNG / CỘNG', 'TOTAL MAN-DAYS / SUBTOTAL'),
      'deposit': t('ĐẶT CỌC {pct}% KHI XÁC NHẬN', '{pct}% DEPOSIT ON CONFIRMATION'),
      'balance': t('THANH TOÁN {pct}% KHI BÀN GIAO', '{pct}% BALANCE ON COMPLETION'),
      'total': t('TỔNG GIÁ TRỊ DỰ ÁN', 'TOTAL PROJECT VALUE'),
      'opt_note': t('Không nằm trong tổng giá trị dự án ở trên. Báo giá riêng, anh chị có thể chọn thêm bất cứ lúc nào.', 'Not included in the total project value above. Quoted separately and may be commissioned at any time.'),
      'opt_total': t('TỔNG NẾU CHỌN THÊM GIAI ĐOẠN 2', 'TOTAL IF PHASE 2 COMMISSIONED'),
    },
    'phases': [{
      'name': t('GIAI ĐOẠN 1 — WEBSITE CHÍNH THỨC', 'PHASE 1 — OFFICIAL WEBSITE'),
      'items': [
        {'title': t('Thiết kế và xây dựng bản mẫu ba ngôn ngữ (đã hoàn thành)', 'Design and build of the three-language mock-up (already done)'), 'md': 0, 'kind': 'free', 'bullets': [
          t('72 trang tiếng Anh, Việt, Trung; giao diện mới, hiệu ứng chuyển động', '72 pages in English, Vietnamese and Chinese; new design and motion'),
          t('Giữ lại từ web cũ: lịch đặt hẹn Koalendar ngay trên trang, 7 bài viết, thông tin vải, liên hệ', 'Kept from the current site: Koalendar booking on the page, the 7 articles, cloth information, contact'),
          t('Thêm mới: bảng giá, quy trình may, cửa hàng có bộ lọc, nút WhatsApp/Zalo, form gửi yêu cầu', 'New: price list, the tailoring process, a shop with filters, WhatsApp/Zalo buttons, an enquiry form')]},
        {'title': t('Nội dung thật của Phan\'s', "Phan's real content"), 'md': 1.0, 'bullets': [
          t('Thay ảnh minh hoạ bằng ảnh thật của villa, anh chị, sản phẩm và vải', 'Replace the sample photos with real photos of the villa, the founders, garments and cloth'),
          t('Bổ sung giá còn thiếu, năm thành lập, thời gian may, lịch nghỉ lễ', 'Add the missing prices, founding year, turnaround time and holiday closures')]},
        {'title': t('Cửa hàng trưng bày', 'Showcase shop'), 'md': 0.5, 'bullets': [
          t('Sản phẩm thật: vải Nobility và đồ may sẵn, có bộ lọc', 'Real products: Nobility cloth and ready-made pieces, with filters'),
          t('Khách xem rồi hỏi qua WhatsApp/Zalo hoặc đặt lịch; chưa có giỏ hàng và thanh toán online', 'Customers browse, then ask on WhatsApp/Zalo or book; no cart or online payment yet')]},
        {'title': t('Hoàn thiện ba ngôn ngữ', 'Final translations'), 'md': 0.5, 'bullets': [
          t('Rà soát bản tiếng Anh, Việt, Trung; sửa theo góp ý của Phan\'s', "Review English, Vietnamese and Chinese; apply Phan's corrections")]},
        {'title': t('Google và chuyển đổi từ web cũ', 'Google and moving from the current site'), 'md': 0.5, 'bullets': [
          t('Link cũ trên Google tự chuyển sang trang mới, không mất thứ hạng', 'Old Google links forward to the new pages, so ranking is kept'),
          t('Sitemap, gắn Google Business (Google Maps), đo lượt truy cập', 'Sitemap, Google Business (Maps) link, visitor tracking')]},
        {'title': t('Tích hợp phòng thử đồ AI (Anywear)', 'AI fitting room integration (Anywear)'), 'md': 0.5, 'bullets': [
          t('Gắn phòng thử đồ vào ảnh sản phẩm, chọn sản phẩm hiển thị đẹp, thử trên điện thoại', 'Attach the fitting room to product photos, pick the pieces that render well, test on phones'),
          t('Thông báo quyền riêng tư trước khi khách bật camera', 'Privacy notice before a visitor turns on the camera'),
          {'text': t('Phí sử dụng Anywear (nếu dùng bản trả phí) do Phan\'s trả trực tiếp cho Decart, không nằm trong báo giá này. Xem phụ lục.', "Anywear usage fees (if the paid plan is chosen) are paid by Phan's directly to Decart and are not in this quote. See the appendix."), 'kind': 'flag'}]},
        {'title': t('Tên miền, hosting và ra mắt', 'Domain, hosting and launch'), 'md': 0.5, 'bullets': [
          t('Cài đặt hosting, trỏ phanscustomtailor.com, chứng chỉ bảo mật https', 'Set up hosting, point phanscustomtailor.com, https certificate'),
          t('Email info@phantailor.com giữ nguyên; web cũ chạy đến ngày chuyển', 'Email info@phantailor.com unchanged; the old site runs until switch-over')]},
        {'title': t('Kiểm tra và bàn giao', 'Testing and handover'), 'md': 0.5, 'bullets': [
          t('Kiểm tra trên máy tính và điện thoại, sửa lỗi, hướng dẫn sử dụng', 'Test on computers and phones, fix issues, walk-through for Phan\'s')]},
      ]}],
    'notes': [
      t('Thời gian: khoảng 1 tuần làm việc, tính từ khi nhận đủ ảnh và thông tin.', 'Timeline: about one working week from when we receive all photos and details.'),
      t('Chưa gồm: phí gia hạn tên miền (Phan\'s đang tự trả), phí sử dụng phòng thử đồ AI, phí cổng thanh toán.', "Excludes: domain renewal (Phan's already pays this), AI fitting room usage fees, payment gateway fees."),
      t('Phí hosting và bảo trì hằng năm: báo riêng.', 'Yearly hosting and maintenance: quoted separately.'),
      t('Báo giá có hiệu lực 30 ngày.', 'Quotation valid for 30 days.'),
    ],
    'optional_phase': {
      'name': t('GIAI ĐOẠN 2 — TUỲ CHỌN', 'PHASE 2 — OPTIONAL'),
      'items': [
        {'title': t('Bán hàng và thanh toán online', 'Online sales and payment'), 'md': 4.0, 'bullets': [
          t('Giỏ hàng, thanh toán, email xác nhận đơn hàng', 'Cart, checkout, order confirmation emails'),
          t('Cổng thanh toán VNPay hoặc OnePay (Phan\'s đăng ký, phí giao dịch trả cho cổng thanh toán)', "VNPay or OnePay gateway (Phan's registers; transaction fees go to the gateway)")]},
        {'title': t('Trang trưng bày Web 3D', 'Web 3D showcase page'), 'md': 0.5, 'bullets': [
          t('Đặt trải nghiệm 3D của đội Web 3D vào một trang riêng trên website', "Give the Web 3D team's experience its own page on the site")]},
      ]},
    'appendix': anywear(L),
  }

def anywear(L):
  t = lambda vi, en: vi if L == 'vi' else en
  return {
    'title': t('Phụ lục: phòng thử đồ AI, bản miễn phí và bản trả phí', 'Appendix: AI fitting room, free and paid'),
    'intro': t('Phòng thử đồ dùng Anywear của Decart (một công ty AI bên ngoài). Bên em tích hợp và cho anh chị xem thử; anh chị tự quyết có dùng hay không, và nếu dùng bản trả phí thì trả trực tiếp cho Decart. Có thể tắt bất cứ lúc nào.',
               "The fitting room uses Decart's Anywear (an outside AI company). We integrate it and show you how it works; you decide whether to use it, and if you choose the paid plan you pay Decart directly. It can be switched off at any time."),
    'heads': [t('', ''), t('Bản miễn phí (thử nghiệm)', 'Free (trial)'), t('Bản trả phí', 'Paid')],
    'rows': [
      (t('Chi phí', 'Cost'), t('Miễn phí trong giai đoạn beta của Decart', 'Free during Decart\'s beta'), t('Decart báo giá riêng theo lượng dùng (chưa công bố bảng giá)', 'Quoted by Decart based on usage (no public price list)')),
      (t('Ai dùng được', 'Who can use it'), t('Có giới hạn: Decart nói bản thử “không phục vụ toàn bộ lượng khách”. Trên bản mẫu, mỗi khách được khoảng 6 lượt thử', 'Limited: Decart says the trial "won\'t serve your whole traffic". On the mock-up each visitor gets about 6 tries'), t('Mở cho tất cả khách vào website', 'Open to every visitor')),
      (t('Lúc đông khách', 'At busy times'), t('Người dùng có báo phải chờ xếp hàng', 'Users have reported waiting in a queue'), t('Không giới hạn như bản thử', 'Without the trial limits')),
      (t('Sản phẩm', 'Products'), t('Nút thử chỉ hiện trên sản phẩm AI hiển thị đẹp', 'The try-on button only shows on pieces the AI renders well'), t('Decart rà soát chất lượng cả danh mục sản phẩm', 'Decart runs a quality pass on the whole catalogue')),
      (t('Thời hạn', 'How long'), t('Có thể kết thúc khi Decart hết giai đoạn beta', 'May end when Decart\'s beta ends'), t('Theo hợp đồng với Decart', 'Per the agreement with Decart')),
    ],
    'cost_title': t('Ước tính chi phí bản trả phí', 'Estimating the paid cost'),
    'cost': t('Decart chưa công bố giá cho bản dành cho cửa hàng. Để tham khảo, giá công bố cho nhà phát triển là 0,02 USD mỗi giây thử đồ, tức khoảng 1,2 USD mỗi phút. Ví dụ: 100 lượt thử mỗi tháng, mỗi lượt 1 phút, khoảng 120 USD/tháng; 300 lượt, mỗi lượt 1,5 phút, khoảng 540 USD/tháng. Đây chỉ là ước tính; giá thật do Decart báo, bên em sẽ hỏi giúp theo lượng khách của Phan\'s.',
              "Decart hasn't published a price for the store version. As a reference, its published developer rate is US$0.02 per second of try-on, about US$1.20 per minute. For example, 100 tries a month at 1 minute each is about US$120/month; 300 tries at 1.5 minutes is about US$540/month. These are estimates only; the real price comes from Decart, and we'll ask them based on Phan's visitor numbers."),
    'notes': [
      t('Phòng thử đồ cho khách thấy kiểu dáng, màu và chất vải trên người mình. Số đo thật vẫn lấy tại villa.', 'The fitting room shows style, colour and cloth on the visitor. Real measurements are still taken at the villa.'),
      t('Camera của khách được xử lý bởi Decart; website sẽ hiện thông báo trước khi bật camera.', "The visitor's camera feed is processed by Decart; the site shows a notice before the camera turns on."),
      t('Anh chị có thể dùng bản miễn phí trước, xem khách có dùng không, rồi mới quyết định trả phí.', 'You can start on the free version, see whether customers use it, then decide on the paid plan.'),
    ],
    'sources': 'anywear.decart.ai/business · docs.platform.decart.ai/getting-started/pricing (' + t('kiểm tra 23/10/2026', 'checked 23 Oct 2026') + ')',
  }

# ---------- PDF from the same spec ----------
def vnd(x): return f'{x:,.0f} ₫'.replace(',', '.') if LANG == 'vi' else f'{x:,.0f} ₫'
def pdf_html(S):
  e = html.escape; lab = S['labels']; R = S['rate']
  rows = []; n = 0; sub_total_md = 0
  def items_html(items):
    nonlocal n
    out = ''; md_sum = 0
    for it in items:
      n += 1; md = it.get('md', 0); md_sum += md; free = it.get('kind') == 'free'
      out += f'<tr class="item{" free" if free else ""}"><td class="c">{n}</td><td><b>{e(it["title"])}</b></td><td class="c">{md:.1f}</td><td class="r">{vnd(R) if md else ""}</td><td class="r"><b>{vnd(md * R)}</b></td></tr>'
      for b in it.get('bullets', []):
        txt, kind = (b, it.get('kind', 'normal')) if isinstance(b, str) else (b['text'], b.get('kind', 'normal'))
        mark = {'flag': '▶', 'free': '✓'}.get(kind, '•')
        out += f'<tr class="b {kind}"><td></td><td><span>{mark}</span>{e(txt)}</td><td></td><td></td><td></td></tr>'
    return out, md_sum
  body = ''
  for ph in S['phases']:
    h, md = items_html(ph['items']); sub_total_md += md
    label = ph['name'].split('—')[-1].strip()
    body += f'<tr class="ph"><td colspan="5">{e(ph["name"])}</td></tr>' + h + f'<tr class="sub"><td colspan="2">{lab["subtotal"]} — {e(label)}</td><td class="c">{md:.1f}</td><td></td><td class="r">{vnd(md * R)}</td></tr>'
  tot = sub_total_md * R; p = S['deposit_pct']
  body += f'<tr class="gap"><td colspan="5"></td></tr><tr class="sub"><td colspan="2">{lab["total_md"]}</td><td class="c">{sub_total_md:.1f}</td><td></td><td class="r">{vnd(tot)}</td></tr>'
  body += f'<tr class="pl"><td colspan="2">{lab["deposit"].format(pct=p)}</td><td></td><td></td><td class="r">{vnd(tot * p / 100)}</td></tr>'
  body += f'<tr class="pl"><td colspan="2">{lab["balance"].format(pct=100 - p)}</td><td></td><td></td><td class="r">{vnd(tot * (100 - p) / 100)}</td></tr>'
  body += f'<tr class="sub big"><td colspan="2">{lab["total"]}</td><td></td><td></td><td class="r">{vnd(tot)}</td></tr>'
  notes = ''.join(f'<p class="note">{e(x)}</p>' for x in S.get('notes', []))
  op = S.get('optional_phase'); opt = ''
  if op:
    h, md = items_html(op['items'])
    opt = (f'<table class="bom"><thead><tr><th>{lab["no"]}</th><th>{lab["desc"]}</th><th>{lab["md"]}</th><th>{lab["unit"]}</th><th>{lab["amount"]}</th></tr></thead><tbody>'
           f'<tr class="ph"><td colspan="5">{e(op["name"])}</td></tr>{h}<tr class="sub"><td colspan="2">{lab["subtotal"]} — {e(op["name"].split("—")[-1].strip())}</td><td class="c">{md:.1f}</td><td></td><td class="r">{vnd(md * R)}</td></tr>'
           f'<tr class="pl"><td colspan="5" class="note">{e(lab["opt_note"])}</td></tr>'
           f'<tr class="sub"><td colspan="2">{lab["opt_total"]}</td><td class="c">{sub_total_md + md:.1f}</td><td></td><td class="r">{vnd((sub_total_md + md) * R)}</td></tr></tbody></table>')
  meta = ''.join(f'<tr><th>{e(k)}</th><td>{e(v)}</td></tr>' for k, v in S['meta'].items())
  A = S['appendix']
  app = (f'<section class="app"><h2>{e(A["title"])}</h2><p>{e(A["intro"])}</p><table class="cmp"><thead><tr>' + ''.join(f'<th>{e(h)}</th>' for h in A['heads']) + '</tr></thead><tbody>' +
         ''.join(f'<tr><th>{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in A['rows']) + '</tbody></table>' +
         f'<h3>{e(A["cost_title"])}</h3><p>{e(A["cost"])}</p>' + ''.join(f'<p class="li">• {e(x)}</p>' for x in A['notes']) + f'<p class="src">{e(A["sources"])}</p></section>')
  return f'''<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><title>{e(S["output_name"])}</title><style>
@page {{ size: A4; margin: 13mm 12mm 16mm; }}
body {{ font-family: Arial, Helvetica, sans-serif; font-size: 9.5pt; color: #000; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.banner {{ background: #1F3864; color: #fff; text-align: center; font-weight: bold; font-size: 14pt; padding: 7px; }}
.subt {{ text-align: center; color: #1F3864; font-weight: bold; font-size: 11pt; margin: 6px 0 10px; }}
table {{ width: 100%; border-collapse: collapse; }}
.meta th {{ text-align: left; width: 18%; padding: 2px 0; font-weight: bold; vertical-align: top; }} .meta td {{ padding: 2px 0; }}
.rate {{ margin: 10px 0 12px; display: flex; align-items: center; gap: 14px; }} .rate b {{ width: 18%; }} .rate i {{ flex: 1; }}
.rate span {{ border: 1px solid #BFBFBF; padding: 3px 16px; color: #1F3864; font-weight: bold; font-size: 10.5pt; }}
.bom th {{ background: #1F3864; color: #fff; padding: 5px; border: 1px solid #BFBFBF; }}
.bom td {{ border: 1px solid #BFBFBF; padding: 4px 6px; vertical-align: top; }}
.bom thead {{ display: table-header-group; }} tr {{ break-inside: avoid; }}
.c {{ text-align: center; }} .r {{ text-align: right; white-space: nowrap; }}
.bom td:first-child {{ width: 6%; }} .bom td:nth-child(3) {{ width: 9%; }} .bom td:nth-child(4) {{ width: 14%; }} .bom td:nth-child(5) {{ width: 15%; }}
tr.ph td {{ background: #1F3864; color: #fff; font-weight: bold; font-size: 10.5pt; padding: 6px; }}
tr.b td {{ font-size: 8.8pt; color: #404040; padding: 2px 6px 2px 16px; }} tr.b span {{ display: inline-block; width: 14px; }}
tr.b.flag td {{ background: #FCE4D6; color: #833C0C; font-weight: bold; }} tr.b.free td {{ background: #E2EFDA; color: #375623; font-weight: bold; }}
tr.item.free td b {{ color: #375623; }}
tr.sub td {{ background: #EAF0F7; font-weight: bold; }} tr.sub td:first-child {{ text-align: right; color: #1F3864; }}
tr.sub.big td {{ font-size: 11.5pt; padding: 7px 6px; }} tr.pl td:first-child {{ text-align: right; }}
tr.gap td {{ border: 0; height: 8px; }}
.note {{ font-size: 8.8pt; font-style: italic; color: #595959; margin: 4px 0; }}
.opt {{ margin-top: 16px; }}
.app {{ break-before: page; }} .app h2 {{ color: #1F3864; font-size: 13pt; margin: 0 0 8px; }} .app h3 {{ color: #1F3864; font-size: 11pt; margin: 14px 0 4px; }}
.app p {{ line-height: 1.45; margin: 4px 0; }}
.cmp th, .cmp td {{ border: 1px solid #BFBFBF; padding: 6px; vertical-align: top; text-align: left; }}
.cmp thead th {{ background: #1F3864; color: #fff; }} .cmp tbody th {{ width: 18%; background: #F2F2F2; }}
.li {{ margin: 3px 0; }} .src {{ font-size: 8pt; color: #808080; margin-top: 10px; }}
</style></head><body>
<div class="banner">{e(S["title"])}</div><div class="subt">{e(S["subtitle"])}</div>
<table class="meta">{meta}</table>
<div class="rate"><b>{lab["rate"]}</b><i>{lab["rate_desc"]}</i><span>{vnd(R)}</span></div>
<table class="bom"><thead><tr><th>{lab["no"]}</th><th>{lab["desc"]}</th><th>{lab["md"]}</th><th>{lab["unit"]}</th><th>{lab["amount"]}</th></tr></thead><tbody>{body}</tbody></table>
{notes}<div class="opt">{opt}</div>{app}</body></html>'''

FOOT = '<div style="width:100%;font-family:Arial;font-size:7.5pt;color:#808080;padding:0 12mm;display:flex;justify-content:space-between"><span>TheWebxite — {name}</span><span>{pg} <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'

if __name__ == '__main__':
  with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for LANG in ('vi', 'en'):
      S = spec(LANG); name = S['output_name']
      json.dump(S, open(f'{name}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
      build_bom.build_workbook(S, f'{name}.xlsx'); build_bom.clear_row_heights(f'{name}.xlsx')
      open(f'{name}.html', 'w', encoding='utf-8').write(pdf_html(S))
      pg.goto('file://' + os.path.abspath(f'{name}.html')); pg.wait_for_timeout(300)
      pg.pdf(path=f'{name}.pdf', format='A4', print_background=True, display_header_footer=True, header_template='<span></span>',
             footer_template=FOOT.format(name=html.escape(name), pg='Trang' if LANG == 'vi' else 'Page'),
             margin={'top': '13mm', 'bottom': '16mm', 'left': '12mm', 'right': '12mm'})
      print(name, 'ok')
    b.close()
