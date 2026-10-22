"""In-person proposal for Phan's (Kimlien presents it at the villa), Vietnamese + English from one source,
plus Kimlien's presenter notes.
Run from the project root:
  node build.mjs && python3 pitch/meet/capture.py      # only when the demo changes
  /Users/hengzhexin/anaconda3/bin/python3 pitch/meet/build_meeting.py
Writes pitch/meet/Gap-mat-Phans-VI.pdf, Meeting-Phans-EN.pdf, Ghi-chu-trinh-bay-Kimlien-VI.pdf, Presenter-notes-Kimlien-EN.pdf.
Rules: ~/Desktop/Website Skill Folder/fe-web-design-skills/library/pitch-deck.md (no AI-deck tells)."""
import os, random, html
from PIL import Image
import qrcode
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
LINK = 'https://phans-custom-tailor-demo.vercel.app/'
A = '../../assets/img/'
# Set when Xin has decided the price, e.g. {'build': '...', 'monthly': '...'}; the price slide is skipped while None.
PRICE = None

# ---------- image prep ----------
def crop(src, box, out):
  Image.open(src).convert('RGB').crop(box).save(out, 'JPEG', quality=86); return Image.open(out).size
SZ = {
  'pricing_c': crop('img/pricing.jpg', (80, 870, 2140, 2500), 'img/pricing_c.jpg'),
  'shop_c': crop('img/shop.jpg', (100, 820, 2160, 2250), 'img/shop_c.jpg'),
  'contact_c': crop('img/contact.jpg', (60, 880, 2160, 1450), 'img/contact_c.jpg'),
}
q = qrcode.QRCode(border=0, box_size=12); q.add_data(LINK); q.make()
q.make_image(fill_color='#141414', back_color='#f7f6f3').save('img/qr.png')

# ---------- hand-drawn markup ----------
PEN = '#b5412f'
def ring(cx, cy, rx, ry, seed=1):
  r = random.Random(seed); pts = []
  a0 = r.uniform(0, 6.28); n = 34
  for i in range(n + 5):
    a = a0 + i * (6.6 / n)
    k = 1 + r.uniform(-.045, .045) + (i / n) * .06
    pts.append((cx + rx * k * __import__('math').cos(a), cy + ry * k * __import__('math').sin(a)))
  d = f'M{pts[0][0]:.0f},{pts[0][1]:.0f} ' + ' '.join(f'L{x:.0f},{y:.0f}' for x, y in pts[1:])
  return f'<path d="{d}" fill="none" stroke="{PEN}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
def arrow(x1, y1, x2, y2, bend=60):
  import math
  mx, my = (x1 + x2) / 2, (y1 + y2) / 2; dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1
  cx, cy = mx - dy / L * bend, my + dx / L * bend
  ang = math.atan2(y2 - cy, x2 - cx); h = 34
  a1 = (x2 - h * math.cos(ang - .45), y2 - h * math.sin(ang - .45)); a2 = (x2 - h * math.cos(ang + .45), y2 - h * math.sin(ang + .45))
  return (f'<path d="M{x1},{y1} Q{cx:.0f},{cy:.0f} {x2},{y2}" fill="none" stroke="{PEN}" stroke-width="6" stroke-linecap="round"/>'
          f'<path d="M{a1[0]:.0f},{a1[1]:.0f} L{x2},{y2} L{a2[0]:.0f},{a2[1]:.0f}" fill="none" stroke="{PEN}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
def note(x, y, text, size=62, anchor='start'):
  lines = text.split('\n')
  return f'<text x="{x}" y="{y}" font-family="Patrick Hand" font-size="{size}" fill="{PEN}" text-anchor="{anchor}">' + ''.join(
    f'<tspan x="{x}" dy="{0 if i == 0 else size * 1.08:.0f}">{html.escape(l)}</tspan>' for i, l in enumerate(lines)) + '</text>'
def marked(img, size, marks, style=''):
  w, h = size
  return (f'<div class="marked" style="{style}"><img src="{img}" alt=""><svg viewBox="0 0 {w} {h}" preserveAspectRatio="none">{"".join(marks)}</svg></div>')

def deck(L):
  t = lambda vi, en: vi if L == 'vi' else en
  S = []
  def slide(cls, body, num=True): S.append((cls, body, num))

  # 1 cover: the villa showroom
  slide('cover', f'''<img class="bleed" src="{A}showroom.webp" alt="">
  <div class="shade"></div>
  <img class="logo" src="../logo-white.png" alt="PHAN'S">
  <div class="cover-txt"><h1>{t("Website mới<br>cho Phan's", "A new website<br>for Phan's")}</h1>
  <p>{t("Kimlien gặp anh Thịnh và chị Thương tại villa, Saigon Pearl<br>Tháng 10 năm 2026", "Kimlien with Thinh and Thuong Phan at the villa, Saigon Pearl<br>October 2026")}</p></div>
  <p class="cover-by">TheWebxite</p>''', num=False)

  # 2 letter from Xin
  slide('letter', f'''<div class="ph"><img src="{A}villa-lounge.webp" alt=""></div>
  <div class="txt">
  <p class="salut">{t("Anh Thịnh, chị Thương thân mến,", "Dear Thinh and Thuong,")}</p>
  <p>{t("Cảm ơn anh chị đã xem bản mẫu và muốn trao đổi tiếp. Hôm nay Kimlien đến villa để cùng anh chị đi qua từng phần: website mới trông thế nào, giai đoạn đầu gồm những gì, chuyển từ website cũ sang ra sao, và bên em cần anh chị chuẩn bị những gì.",
        "Thank you for looking at the mock-up and wanting to take it further. Kimlien is at the villa today to go through it with you: how the new site looks, what the first phase includes, how we move over from the current site, and what we'll need from you.")}</p>
  <p>{t("TheWebxite thiết kế và xây dựng website cho nhiều doanh nghiệp, trong đó có các công ty đa quốc gia và công ty niêm yết. Với Phan's, điều bên em muốn là một website xứng với những gì khách đã viết về anh chị.",
        "TheWebxite designs and builds websites for companies, including multinationals and listed companies. For Phan's, we want a website that lives up to what your customers already write about you.")}</p>
  <p>{t("Anh chị cứ hỏi Kimlien bất cứ điều gì. Câu nào cần trả lời kỹ hơn, em sẽ gửi lại bằng văn bản ngay sau buổi gặp.", "Ask Kimlien anything. If something needs a fuller answer, I'll send it in writing straight after the meeting.")}</p>
  <p class="sign">Xin<br><span>TheWebxite</span></p></div>''', num=False)

  # 3 the number
  slide('number', f'''<div class="big">975</div>
  <div class="num-txt">
  <p class="lede">{t("đánh giá trên Tripadvisor, điểm 4,8. Trên Google là 1.115 đánh giá, điểm 4,9.", "reviews on Tripadvisor, rated 4.8. On Google, 1,115 reviews at 4.9.")}</p>
  <blockquote>“Finding a truly exceptional tailor is a rare feat, but finding one that pairs flawless technical precision with genuinely warm, selfless hospitality is nearly impossible.”
  <cite>Benjamin C., Vancouver · Tripadvisor, {t("tháng 6/2026", "June 2026")}</cite></blockquote>
  {t('<p class="tr">Tạm dịch: “Tìm được một thợ may thật sự giỏi đã hiếm, tìm được nơi vừa chuẩn xác về kỹ thuật vừa hiếu khách chân thành gần như là không thể.”</p>', '')}
  <p>{t("Khách nước ngoài tìm Phan's trên mạng trước khi lên máy bay. Website là nơi đầu tiên họ gặp anh chị, nên nó cần tốt như chính bộ vest.", "Overseas customers look Phan's up before they fly. The website is where they meet you first, so it has to be as good as the suit.")}</p></div>''')

  # 4 the new home page, full bleed
  slide('hero', f'''<img src="img/hero.jpg" alt="">
  <div class="side"><p class="h">{t("Trang chủ", "The home page")}</p>
  <p>{t("Mở ra là ảnh của chính Phan's. Không khẩu hiệu, không chữ thừa. Khách bấm thẳng vào vest, sơ mi, vải hoặc đặt lịch.", "It opens on Phan's own photograph. No slogans, nothing extra. Visitors go straight to suits, shirts, cloth or booking.")}</p>
  <p class="url">phans-custom-tailor-demo<br>.vercel.app</p></div>''')

  # 5 pricing, marked up
  pm = [ring(1044, 207, 165, 78, 3), arrow(1290, 610, 1190, 270, -50),
        note(1260, 680, t("Khách biết giá\ntrước khi bay sang", "Prices are clear\nbefore they fly")),
        ring(1009, 1002, 190, 62, 7), arrow(1300, 960, 1215, 1000, 20),
        note(1260, 900, t("Còn trống, anh chị\nbổ sung giúp", "Still blank, please\nsend us these")),
        ring(560, 1525, 400, 82, 11), note(1000, 1545, t("Đặt lịch hoặc nhắn ngay tại đây", "Book or message right here"))]
  slide('pricing', marked('img/pricing_c.jpg', SZ['pricing_c'], pm, 'width:910px') + f'''
  <div class="col"><h2>{t("Bảng giá", "Prices")}</h2>
  <p>{t("Câu khách hỏi nhiều nhất trước chuyến đi là may một bộ vest hết bao nhiêu. Trang này trả lời ngay, kèm những gì đã gồm trong giá: thử đồ, sửa miễn phí trọn đời.", "The first thing people ask before the trip is what a suit costs. This page answers it, along with what the price includes: fittings and free alterations for life.")}</p>
  <p>{t("Giá đang lấy từ website hiện tại. Mấy món còn trống, anh chị cho bên em giá là xong.", "The prices come from your current site. For the blank ones, just send us the figures.")}</p></div>''')

  # 6 phones
  slide('phones', f'''<div class="col"><h2>{t("Ba thứ tiếng,<br>ngay trên điện thoại", "Three languages,<br>on a phone")}</h2>
  <p>{t("Tiếng Anh là chính vì phần lớn khách là người nước ngoài. Có thêm tiếng Việt và tiếng Trung. Khách đổi ngôn ngữ thì vẫn ở đúng trang đang xem.", "English comes first because most customers are from overseas, with Vietnamese and Chinese alongside. Switching language keeps the visitor on the same page.")}</p>
  <p>{t("Bên em tự dịch cả ba. Anh chị chỉ cần một người đọc lại bản tiếng Việt.", "We translate all three ourselves. You only need someone to read through the Vietnamese.")}</p></div>
  <div class="row">
    <figure><div class="phone"><img src="img/m_vi_home.jpg" alt=""></div><figcaption>{t("Tiếng Việt", "Vietnamese")}</figcaption></figure>
    <figure class="up"><div class="phone"><img src="img/m_zh_pricing.jpg" alt=""></div><figcaption>{t("Tiếng Trung, trang giá", "Chinese, prices")}</figcaption></figure>
    <figure><div class="phone"><img src="img/m_vi_contact.jpg" alt=""></div><figcaption>{t("Liên hệ và đặt lịch", "Contact and booking")}</figcaption></figure>
  </div>''')

  # 7 before / after
  slide('split', f'''<h2>{t("Hôm nay, và sắp tới", "Today, and next")}</h2>
  <p class="lead">{t("Cùng một villa, cùng những bộ vest. Chỉ khác lần đầu khách nhìn thấy Phan's trên mạng.", "The same villa, the same suits. What changes is the first time a customer sees Phan's online.")}</p>
  <div class="pair">
    <figure><img src="../img/old_en_desktop.jpg" alt=""><figcaption>tailormadesuit.net {t("hiện tại", "today")}</figcaption></figure>
    <figure><img src="img/vi_home_d.jpg" alt=""><figcaption>{t("Website mới, bản tiếng Việt", "The new site, in Vietnamese")}</figcaption></figure>
  </div>''')

  # 8 booking, marked up strip
  cm = [ring(256, 313, 240, 64, 5), arrow(260, 640, 256, 395, 30),
        note(70, 690, t("Dẫn sang lịch Koalendar\nanh chị đang dùng", "Goes to the Koalendar\ncalendar you already use"), 56),
        ring(835, 1230 - 880 + 0, 150, 100, 9), arrow(1150, 640, 930, 430, -40),
        note(1060, 700, t("WhatsApp cho khách nước ngoài,\nZalo cho khách Việt", "WhatsApp for overseas guests,\nZalo for local ones"), 54)]
  slide('booking', f'''<div class="top"><h2>{t("Đặt lịch vẫn như cũ", "Booking stays as it is")}</h2>
  <p>{t("Nút đặt lịch có trên mọi trang và dẫn thẳng sang Koalendar. Không thêm hệ thống mới, anh chị quản lý lịch hẹn như bây giờ. Ai chưa muốn đặt lịch thì nhắn một tin là được.", "The booking button is on every page and goes straight to Koalendar. No new system: you manage appointments exactly as you do now. Anyone not ready to book can just send a message.")}</p></div>''' +
    marked('img/contact_c.jpg', SZ['contact_c'], cm, 'width:1180px;margin-left:50px'))

  # 9 shop, marked up
  sm = [ring(1065, 1105, 215, 95, 13), arrow(1330, 230, 1150, 1000, -120),
        note(1200, 110, t("Sản phẩm mẫu. Sẽ thay bằng\nvải và đồ thật của Phan's", "Sample products, to be replaced\nwith Phan's real cloth and pieces"), 58)]
  slide('shop', f'''<div class="col"><h2>{t("Cửa hàng có cần thanh toán online?", "Does the shop need online payment?")}</h2>
  <p>{t("Giai đoạn đầu thì chưa cần. Khách xem vải Nobility và đồ may sẵn, rồi nhắn hỏi hoặc đặt lịch đến villa. Với đồ may đo, khách vẫn phải đến lấy số đo.", "Not at first. Customers browse Nobility cloth and ready-made pieces, then message or book a visit. For made-to-measure, they still come in to be measured.")}</p>
  <p>{t("Bán online cần người xử lý đơn mỗi ngày, đóng gói, gửi hàng ra nước ngoài, đổi trả và cổng thanh toán như OnePay hay VNPay. Khi anh chị sẵn sàng, mình làm ở giai đoạn sau.", "Selling online needs someone on orders every day, packing, overseas shipping, returns and a payment gateway such as OnePay or VNPay. When you're ready, that's a later phase.")}</p></div>''' +
    marked('img/shop_c.jpg', SZ['shop_c'], sm, 'width:850px'))

  # 10 domain and hosting
  slide('domain', f'''<h2>{t("Tên miền và hosting, nói cho dễ hiểu", "Domain and hosting, in plain words")}</h2>
  <div class="three">
    <div><p class="k">{t("Tên miền là địa chỉ", "The domain is the address")}</p>
    <p>{t("Phan's đã có <b>phanscustomtailor.com</b>, cái tên đang hiện trên Google Maps. Bên em đề xuất dùng tên này làm địa chỉ chính, còn tailormadesuit.net tự chuyển về. Không cần mua tên mới, và tên miền luôn đứng tên Phan's.", "Phan's already owns <b>phanscustomtailor.com</b>, the name on your Google Maps listing. We suggest it as the main address, with tailormadesuit.net forwarding to it. No new domain to buy, and it always stays in Phan's name.")}</p></div>
    <div><p class="k">{t("Hosting là ngôi nhà", "Hosting is the house")}</p>
    <p>{t("Nơi chứa toàn bộ nội dung và hình ảnh để website mở 24/7. TheWebxite lo hết: mua, bảo mật, sao lưu, cập nhật. Máy chủ đặt ở nhiều nước nên khách ở đâu mở cũng nhanh.", "Where the content and photos live so the site is open 24/7. TheWebxite handles it all: buying it, security, backups, updates. The servers sit in many countries, so it loads fast wherever the customer is.")}</p></div>
    <div><p class="k">{t("Email giữ nguyên", "Email stays put")}</p>
    <p>{t("info@phantailor.com nằm ở chỗ khác và không bị đụng tới. Website cũ trên Haravan vẫn chạy đến ngày chuyển, và các link cũ trên Google sẽ tự dẫn sang trang mới.", "info@phantailor.com lives elsewhere and isn't touched. The Haravan site keeps running until switch-over day, and old Google links lead to the matching new pages.")}</p></div>
  </div>
  <div class="addr"><p class="dn">phanscustomtailor.com</p><p>{t("tailormadesuit.net và các link cũ tự chuyển về đây", "tailormadesuit.net and the old links all lead here")}</p></div>''')

  # 11 the 3D team
  slide('statement', f'''<img class="side-ph" src="{A}nobility-books.webp" alt="">
  <div class="st"><p class="quote">{t("Website là ngôi nhà. Phần 3D có thể là một căn phòng đẹp trong đó.", "The website is the house. The 3D work can be a beautiful room inside it.")}</p>
  <p>{t("Anh có nhắc đang làm với một đội Web 3D. Hai phần này không giẫm chân nhau. Bên em sẵn sàng làm việc với đội 3D để đặt trải nghiệm của họ vào một trang riêng trên website.", "You mentioned you're working with a Web 3D team. The two don't overlap. We're happy to work with them and give their experience its own page on the site.")}</p></div>''')

  # 12 phase table
  Y, N = t('Có', 'Yes'), ''
  rows = [
    (t("Website tiếng Anh, Việt, Trung", "Website in English, Vietnamese, Chinese"), Y, N),
    (t("Bảng giá, quy trình may, thông tin vải", "Prices, the process, cloth"), Y, N),
    (t("Đặt lịch Koalendar, nút WhatsApp và Zalo", "Koalendar booking, WhatsApp and Zalo"), Y, N),
    (t("Cửa hàng trưng bày vải Nobility và đồ may sẵn", "Showcase of Nobility cloth and ready-made pieces"), Y, N),
    (t("Chuyển 7 bài viết từ website cũ", "The 7 articles from the current site"), Y, N),
    (t("Tối ưu Google, chuyển link cũ sang trang mới", "Google optimisation, old links forwarded"), Y, N),
    (t("Hosting, sao lưu, bảo trì", "Hosting, backups, maintenance"), t("TheWebxite lo", "TheWebxite"), N),
    (t("Giỏ hàng và thanh toán online", "Cart and online payment"), N, t("Khi anh chị muốn bán online", "When you want to sell online")),
    (t("Tài khoản khách hàng", "Customer accounts"), N, t("Đi cùng bán online", "With online sales")),
  ]
  slide('table', f'''<h2>{t("Làm gì trước, để gì sau", "What comes first, what waits")}</h2>
  <table><thead><tr><th></th><th>{t("Giai đoạn đầu", "First phase")}</th><th>{t("Để sau", "Later")}</th></tr></thead><tbody>''' +
    ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows) + '</tbody></table>')

  # 13 what we need
  slide('need', f'''<h2>{t("Bên em cần anh chị chuẩn bị", "What we need from you")}</h2>
  <div class="four">
    <div><p class="k">{t("Tên miền", "The domain")}</p><p>{t("Tài khoản đang quản lý phanscustomtailor.com và tailormadesuit.net, hoặc mời bên em vào. Và anh chị chọn địa chỉ nào làm chính.", "The account that manages phanscustomtailor.com and tailormadesuit.net, or an invite for us. And which address you'd like as the main one.")}</p></div>
    <div><p class="k">{t("Hình ảnh", "Photos")}</p><p>{t("Ảnh villa, ảnh anh chị, đồ đã may xong và vải. File logo gốc nếu còn. Ảnh chụp điện thoại cũng được, miễn rõ nét.", "The villa, the two of you, finished garments and cloth. The original logo file if you have it. Phone photos are fine if they're sharp.")}</p></div>
    <div><p class="k">{t("Giá và vài chi tiết", "Prices and details")}</p><p>{t("Giá blazer, gilê, măng tô và đồ nữ. Hiện giá bằng VND hay thêm USD. Năm thành lập, lịch nghỉ Tết, thời gian may một bộ.", "Prices for blazers, waistcoats, overcoats and women's pieces. VND only, or USD too. The year you started, Tết closures, how long a suit takes.")}</p></div>
    <div><p class="k">{t("Tài khoản", "Accounts")}</p><p>{t("Link Koalendar, trang Facebook chính thức, quyền vào Google Business. Và một người đọc lại bản tiếng Việt.", "The Koalendar link, the official Facebook page, Google Business access. And someone to read the Vietnamese.")}</p></div>
  </div>''')

  # 14 timeline
  steps = [
    (t("Hôm nay", "Today"), t("Thống nhất những phần anh chị muốn làm", "Agree what you'd like us to build")),
    (t("Sau buổi gặp", "After today"), t("Xin gửi báo giá và lịch trình", "Xin sends the quote and timeline")),
    (t("Khi anh chị sẵn sàng", "When you're ready"), t("Anh chị gửi ảnh và thông tin", "You send the photos and details")),
    (t("Khoảng 1 tuần sau", "About a week later"), t("Bên em hoàn thiện, kiểm tra trên máy tính và điện thoại", "We finish and test on computers and phones")),
    (t("Ngày ra mắt", "Launch"), t("Anh chị duyệt, website chạy trên tên miền chính", "You approve, the site goes live on the main domain")),
    (t("Sau đó", "After that"), t("Bên em bảo trì, cập nhật khi anh chị cần", "We look after it and update it when you need")),
  ]
  slide('time', f'''<h2>{t("Từ hôm nay đến ngày ra mắt", "From today to launch")}</h2>
  <div class="line">''' + ''.join(f'<div class="st"><span class="tick"></span><p class="when">{a}</p><p>{b}</p></div>' for a, b in steps) + '</div>' +
    f'<p class="foot">{t("Một tuần tính từ lúc bên em nhận đủ ảnh và thông tin.", "The week counts from when we have all the photos and details.")}</p>')

  # 15 price (only when set)
  if PRICE:
    slide('price', f'''<h2>{t("Chi phí", "Cost")}</h2><p class="pr">{PRICE.get('build', '')}</p><p>{PRICE.get('monthly', '')}</p>''')

  # 16 close
  slide('close', f'''<img class="ph" src="{A}campaign-group.webp" alt="">
  <div class="txt">
  <h2>{t("Mở bản mẫu trên điện thoại", "Open the mock-up on your phone")}</h2>
  <div class="qr"><img src="img/qr.png" alt=""><p>{t("Quét mã để xem lại bất cứ lúc nào", "Scan to look again any time")}<br><a href="{LINK}">phans-custom-tailor-demo.vercel.app</a></p></div>
  <p>{t("Nếu anh chị thấy hợp, bên em rất mong được làm cùng Phan's. Còn nếu chưa, cảm ơn anh chị đã dành thời gian tiếp Kimlien hôm nay.", "If it feels right, we'd be glad to build this with Phan's. If not, thank you all the same for having Kimlien over today.")}</p>
  <p class="sign">Xin, TheWebxite<br><span>{t("và Kimlien", "with Kimlien")}</span></p></div>''', num=False)

  body = ''
  for i, (cls, b, num) in enumerate(S, 1):
    body += f'<section class="slide {cls}">{b}' + (f'<span class="pg">{i}</span>' if num else '') + '</section>'
  return f'''<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{t("Website mới cho Phan's", "A new website for Phan's")}</title>
<link rel="stylesheet" href="fonts/fonts.css">
<style>{CSS}</style></head><body>{body}</body></html>'''

CSS = r'''
@page { size: 1280px 720px; margin: 0; }
:root { --ink:#141414; --paper:#f7f6f3; --stone:#d8d5cf; --mute:#5f5f5f; --navy:#1e2a3a; --pen:#b5412f; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #888; }
body { font-family: "Hanken Grotesk", sans-serif; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.slide { width: 1280px; height: 720px; position: relative; overflow: hidden; background: var(--paper); break-after: page; margin: 0 auto; }
h1, h2, .big, .quote, .k, .salut, .h { font-family: "Prata", serif; font-weight: 400; }
h2 { font-size: 40px; line-height: 1.12; letter-spacing: -.005em; }
p { font-size: 17px; line-height: 1.55; }
b { font-weight: 600; }
.pg { position: absolute; right: 30px; bottom: 22px; font-size: 12px; color: var(--mute); }
.marked { position: relative; }
.marked img { display: block; width: 100%; }
.marked svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }

.cover .bleed { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.cover .shade { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(10,12,16,.82) 0%, rgba(10,12,16,.55) 45%, rgba(10,12,16,.05) 80%); }
.cover .logo { position: absolute; left: 72px; top: 60px; width: 170px; }
.cover-txt { position: absolute; left: 72px; bottom: 84px; color: #fff; }
.cover h1 { font-size: 76px; line-height: 1.06; margin-bottom: 26px; }
.cover-txt p { font-size: 17px; color: #e6e3dd; }
.cover-by { position: absolute; right: 48px; bottom: 40px; color: #e6e3dd; font-size: 14px; letter-spacing: .04em; }

.letter .ph { position: absolute; left: 0; top: 0; bottom: 0; width: 470px; }
.letter .ph img { width: 100%; height: 100%; object-fit: cover; }
.letter .txt { position: absolute; left: 540px; right: 90px; top: 74px; }
.letter .txt p { font-size: 17.5px; margin-bottom: 16px; }
.letter .salut { font-size: 26px !important; margin-bottom: 22px !important; }
.letter .sign { font-family: "Patrick Hand", cursive; font-size: 34px !important; line-height: 1.05 !important; margin-top: 22px; color: var(--navy); }
.letter .sign span { font-family: "Hanken Grotesk"; font-size: 14px; color: var(--mute); }

.number { background: #efede8; }
.number .big { position: absolute; left: 50px; top: 120px; font-size: 330px; line-height: 1; color: var(--navy); letter-spacing: -.02em; }
.number .num-txt { position: absolute; left: 640px; right: 80px; top: 64px; }
.number .lede { font-size: 24px; line-height: 1.4; margin-bottom: 30px; }
.number blockquote { font-family: "Prata"; font-size: 22px; line-height: 1.45; border-top: 1px solid var(--ink); padding-top: 20px; margin-bottom: 12px; }
.number cite { display: block; font-family: "Hanken Grotesk"; font-style: normal; font-size: 13px; color: var(--mute); margin-top: 12px; }
.number .tr { font-size: 15px; color: var(--mute); margin-bottom: 22px; }
.number .num-txt > p:last-child { font-size: 20px; }

.hero { background: var(--ink); }
.hero > img { position: absolute; left: 0; top: 4px; width: 1136px; }
.hero .side { position: absolute; left: 1156px; right: 18px; bottom: 34px; color: #e6e3dd; }
.hero .side p { font-size: 13px; line-height: 1.5; margin-bottom: 12px; }
.hero .side .h { font-size: 21px; color: #fff; line-height: 1.2; }
.hero .side .url { font-size: 11px; color: #9a978f; }

.pricing .marked { position: absolute; left: 0; top: 0; }
.pricing .col { position: absolute; left: 950px; right: 44px; top: 80px; }
.pricing .col h2 { margin-bottom: 22px; }
.pricing .col p { font-size: 18px; margin-bottom: 14px; }

.phones .col { position: absolute; left: 70px; top: 90px; width: 360px; }
.phones .col h2 { margin-bottom: 24px; }
.phones .col p { margin-bottom: 14px; }
.phones .row { position: absolute; left: 470px; right: 50px; top: 56px; display: flex; gap: 34px; justify-content: center; }
.phones figure { width: 228px; }
.phones figure.up { margin-top: -26px; }
.phone { height: 494px; border: 9px solid var(--ink); border-radius: 36px; overflow: hidden; background: #fff; }
.phone img { width: 100%; display: block; }
figcaption { font-size: 13px; color: var(--mute); margin-top: 12px; }

.split h2 { position: absolute; left: 64px; top: 52px; }
.split .lead { position: absolute; left: 64px; top: 116px; width: 760px; font-size: 19px; color: var(--mute); }
.split .pair { position: absolute; left: 64px; right: 0; top: 200px; display: grid; grid-template-columns: 520px 1fr; gap: 36px; align-items: start; }
.split img { width: 100%; display: block; border: 1px solid var(--stone); }
.split figure:first-child img { filter: saturate(.9); }

.booking .top { position: absolute; left: 70px; right: 70px; top: 56px; display: grid; grid-template-columns: 400px 1fr; gap: 60px; align-items: start; }
.booking .top p { font-size: 18.5px; }
.booking .marked { position: absolute; top: 190px; border-top: 1px solid var(--stone); border-bottom: 1px solid var(--stone); }

.shop .col { position: absolute; left: 56px; top: 64px; width: 340px; }
.shop .col h2 { font-size: 36px; margin-bottom: 22px; }
.shop .col p { font-size: 17px; margin-bottom: 14px; }
.shop .marked { position: absolute; right: 0; top: 70px; border-left: 1px solid var(--stone); }

.domain h2 { position: absolute; left: 70px; top: 64px; width: 900px; }
.three { position: absolute; left: 70px; right: 70px; top: 150px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; border-top: 1px solid var(--ink); }
.three > div { padding: 26px 30px 0 0; }
.three > div + div { padding-left: 30px; border-left: 1px solid var(--stone); }
.k { font-size: 23px; line-height: 1.2; margin-bottom: 14px; }
.three p:not(.k) { font-size: 17.5px; }
.addr { position: absolute; left: 70px; right: 70px; bottom: 56px; display: flex; align-items: baseline; gap: 30px; border-top: 1px solid var(--stone); padding-top: 22px; }
.addr .dn { font-family: Prata; font-size: 50px; color: var(--navy); }
.addr p:not(.dn) { color: var(--mute); }

.statement { background: #e9e6df; }
.statement .side-ph { position: absolute; right: 0; top: 0; height: 100%; width: 430px; object-fit: cover; }
.statement .st { position: absolute; left: 80px; top: 50%; transform: translateY(-50%); width: 680px; }
.statement .quote { font-size: 50px; line-height: 1.2; margin-bottom: 34px; color: var(--navy); }
.statement .st > p:last-child { font-size: 20px; width: 600px; }

.table h2 { position: absolute; left: 70px; top: 54px; }
.table table { position: absolute; left: 70px; right: 70px; top: 140px; border-collapse: collapse; font-size: 19px; }
.table th { text-align: left; font-weight: 500; font-size: 14px; color: var(--mute); padding: 0 12px 10px 0; border-bottom: 1.5px solid var(--ink); }
.table td { padding: 13px 12px 13px 0; border-bottom: 1px solid var(--stone); }
.table td:first-child { width: 52%; }
.table td:nth-child(2) { width: 18%; color: var(--navy); font-weight: 500; }
.table td:nth-child(3) { color: var(--mute); }

.need h2 { position: absolute; left: 70px; top: 58px; }
.four { position: absolute; left: 70px; right: 70px; top: 190px; display: grid; grid-template-columns: 1fr 1fr; column-gap: 70px; row-gap: 70px; }
.four > div { border-top: 1px solid var(--ink); padding-top: 18px; }
.four p:not(.k) { font-size: 19.5px; }
.four .k { font-size: 27px; }

.time h2 { position: absolute; left: 70px; top: 60px; }
.time .line { position: absolute; left: 70px; right: 70px; top: 290px; display: grid; grid-template-columns: repeat(6, 1fr); gap: 22px; border-top: 2px solid var(--navy); }
.time .st { position: relative; padding-top: 30px; }
.time .tick { position: absolute; left: 0; top: -9px; width: 2px; height: 16px; background: var(--navy); }
.time .st:nth-child(4) .tick { width: 8px; left: -3px; }
.time .when { font-family: "Prata"; font-size: 24px; margin-bottom: 10px; line-height: 1.25; }
.time .st p:not(.when) { font-size: 18px; }
.time .foot { position: absolute; left: 70px; bottom: 70px; font-size: 18px; color: var(--mute); }

.price h2 { position: absolute; left: 70px; top: 60px; }
.price .pr { position: absolute; left: 70px; top: 200px; font-family: "Prata"; font-size: 56px; }

.close .ph { position: absolute; left: 0; top: 0; width: 560px; height: 100%; object-fit: cover; object-position: 30% center; }
.close .txt { position: absolute; left: 630px; right: 80px; top: 80px; }
.close h2 { margin-bottom: 30px; }
.close .qr { display: flex; gap: 24px; align-items: center; margin-bottom: 34px; }
.close .qr img { width: 150px; height: 150px; }
.close .qr p { font-size: 15px; color: var(--mute); }
.close .qr a { color: var(--ink); }
.close .txt > p { font-size: 18px; }
.close .sign { font-family: "Patrick Hand"; font-size: 32px !important; line-height: 1.1; margin-top: 26px; color: var(--navy); }
.close .sign span { font-family: "Hanken Grotesk"; font-size: 14px; color: var(--mute); }
'''

# ---------- presenter notes for Kimlien ----------
def notes(L):
  t = lambda vi, en: vi if L == 'vi' else en
  N = [
    (t("Bìa", "Cover"), t("Chào anh chị, cảm ơn đã tiếp. Nói ngắn: hôm nay đi qua bản đề xuất khoảng 20 phút, rồi nghe anh chị hỏi.", "Greet them, thank them. Say today takes about 20 minutes, then questions.")),
    (t("Thư của Xin", "Xin's letter"), t("Để anh chị đọc, không cần đọc to. Nhắc: câu nào khó, Xin trả lời bằng văn bản sau buổi gặp.", "Let them read it. Mention that Xin answers hard questions in writing afterwards.")),
    ("975", t("Ý chính: khách nước ngoài tìm Phan's trên mạng trước chuyến đi, website là nơi gặp đầu tiên. Hỏi: anh chị thấy khách thường tìm thấy Phan's qua đâu?", "Main point: overseas customers look them up before the trip. Ask: where do customers usually find Phan's?")),
    (t("Trang chủ", "Home page"), t("Mở bản mẫu trên laptop hoặc điện thoại nếu tiện, cho anh chị bấm thử menu và đổi ngôn ngữ.", "If possible, open the live mock-up and let them tap the menu and switch language.")),
    (t("Bảng giá", "Prices"), t("Chỉ vào các ô còn trống: blazer, gilê, măng tô, đồ nữ. Hỏi luôn giá và hiện VND hay thêm USD. Ghi lại.", "Point at the blank prices (blazer, waistcoat, overcoat, women's). Ask for them and VND vs USD. Note it down.")),
    (t("Ba thứ tiếng", "Three languages"), t("Hỏi ai bên Phan's có thể đọc lại bản tiếng Việt.", "Ask who at Phan's can read the Vietnamese.")),
    (t("Hôm nay và sắp tới", "Today and next"), t("Không chê website cũ. Chỉ để anh chị tự so sánh.", "Don't criticise the old site; let them compare.")),
    (t("Đặt lịch", "Booking"), t("Xác nhận link Koalendar hiện tại và ai đang quản lý lịch.", "Confirm the current Koalendar link and who manages it.")),
    (t("Cửa hàng", "Shop"), t("Nếu anh chị muốn bán online ngay: ghi nhận, nói Xin sẽ báo phương án và chi phí riêng cho giai đoạn sau. Đừng hứa ngày.", "If they want online sales now: note it, say Xin will send options and cost for a later phase. No dates.")),
    (t("Tên miền", "Domain"), t("Hỏi anh chị chọn tên nào làm chính và ai giữ tài khoản tên miền. Nhấn mạnh email không bị ảnh hưởng.", "Ask which domain they want as main and who holds the domain account. Stress that email isn't affected.")),
    (t("Đội 3D", "3D team"), t("Xin liên hệ đội 3D nếu anh chị muốn hai bên phối hợp.", "Ask for the 3D team's contact if they want us to coordinate.")),
    (t("Giai đoạn", "Phases"), t("Hỏi có muốn thêm hoặc bỏ phần nào không.", "Ask if they'd add or drop anything.")),
    (t("Cần chuẩn bị", "What we need"), t("Đi qua 4 nhóm, hỏi khi nào anh chị gửi được. Không cần đủ ngay hôm nay.", "Go through the four groups and ask when they can send them. Not needed today.")),
    (t("Lịch trình", "Timeline"), t("Một tuần tính từ khi đủ ảnh và thông tin. Không hứa ngày ra mắt cụ thể.", "A week from when everything arrives. No fixed launch date.")),
    (t("Kết", "Close"), t("Cho anh chị quét mã QR. Chốt: Xin gửi báo giá sau buổi gặp. Cảm ơn và chào.", "Let them scan the QR. Close: Xin sends the quote after the meeting. Thank them.")),
  ]
  never = [t("Không nói giá cụ thể; báo giá do Xin gửi.", "No specific price; Xin sends the quote."),
           t("Không giới thiệu phòng thử đồ AI. Nếu anh chị hỏi: tính năng đang thử nghiệm, Xin sẽ báo sau.", "Don't bring up the AI fitting room. If asked: it's being tested, Xin will follow up."),
           t("Không hứa bán online, trang quản trị tự sửa hay ngày ra mắt cố định.", "Don't promise online sales, a self-edit admin panel or a fixed launch date.")]
  after = t("Sau buổi gặp, nhắn Xin: phần anh chị đồng ý, tên miền chọn làm chính, giá còn thiếu, các câu chưa trả lời được, và khi nào anh chị gửi ảnh và thông tin.",
            "After the meeting, send Xin: what they agreed, the main domain, the missing prices, unanswered questions, and when they'll send photos and details.")
  rows = ''.join(f'<tr><td>{i}</td><td>{a}</td><td>{b}</td></tr>' for i, (a, b) in enumerate(N, 1))
  return f'''<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{t("Ghi chú trình bày", "Presenter notes")}</title>
<link rel="stylesheet" href="fonts/fonts.css">
<style>@page {{ size: A4; margin: 16mm 15mm; }} body {{ font-family: "Hanken Grotesk"; font-size: 10.5pt; line-height: 1.45; color: #141414; }}
h1 {{ font-family: Prata; font-weight: 400; font-size: 21pt; margin: 0 0 4px; }} .sub {{ color: #5f5f5f; margin: 0 0 14px; }}
table {{ width: 100%; border-collapse: collapse; }} td {{ border-bottom: 1px solid #d8d5cf; padding: 6px 8px 6px 0; vertical-align: top; }}
td:first-child {{ width: 22px; color: #5f5f5f; }} td:nth-child(2) {{ width: 24%; font-weight: 600; }} tr {{ break-inside: avoid; }}
h2 {{ font-family: Prata; font-weight: 400; font-size: 14pt; margin: 18px 0 6px; }} ul {{ margin: 0; padding-left: 18px; }} li {{ margin: 3px 0; }}</style></head><body>
<h1>{t("Ghi chú trình bày cho Kimlien", "Presenter notes for Kimlien")}</h1>
<p class="sub">{t("Đi kèm bản đề xuất gặp mặt tại villa. Nội bộ, không đưa cho khách.", "Goes with the in-person proposal. Internal, not for the client.")}</p>
<table>{rows}</table>
<h2>{t("Đừng hứa", "Don't promise")}</h2><ul>{''.join(f'<li>{x}</li>' for x in never)}</ul>
<h2>{t("Sau buổi gặp", "After the meeting")}</h2><p>{after}</p>
<p class="sub" style="margin-top:14px">{t("Chi tiết hơn (giải thích tên miền, hosting, các câu hỏi thường gặp): xem Briefing-cuoc-goi-Kimlien-VI.pdf.", "More detail (domain/hosting explanations, likely questions): see Call-briefing-Kimlien-EN.pdf.")}</p>
</body></html>'''

if __name__ == '__main__':
  with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
    for L, name in (('vi', 'Gap-mat-Phans-VI'), ('en', 'Meeting-Phans-EN')):
      open(f'{name}.html', 'w', encoding='utf-8').write(deck(L))
      pg.goto('file://' + os.path.abspath(f'{name}.html'), wait_until='load', timeout=90000); pg.evaluate("""Promise.all(['20px Prata','16px "Hanken Grotesk"','600 16px "Hanken Grotesk"','30px "Patrick Hand"'].map(f=>document.fonts.load(f,'Aăữ西')))"""); pg.wait_for_timeout(800)
      ok = pg.evaluate("""document.fonts.check('20px Prata','ữ') && document.fonts.check('16px "Hanken Grotesk"','ữ') && document.fonts.check('30px "Patrick Hand"', 'ữ')""")
      issues = pg.evaluate("""[...document.querySelectorAll('.slide')].flatMap((s,i)=>{const r=s.getBoundingClientRect();return [...s.querySelectorAll('p,h1,h2,table,figure,.four,.three,.line')].filter(e=>{const b=e.getBoundingClientRect();return b.bottom>r.bottom+1||b.right>r.right+1}).map(e=>(i+1)+':'+e.tagName+':'+e.textContent.slice(0,30))})""")
      pg.emulate_media(media='print')
      pg.pdf(path=f'{name}.pdf', width='1280px', height='720px', print_background=True, prefer_css_page_size=True)
      pg.emulate_media(media='screen')
      print(name, 'fonts ok' if ok else 'FONTS NOT LOADED', 'overflow:', issues or 'none')
    for L, name in (('vi', 'Ghi-chu-trinh-bay-Kimlien-VI'), ('en', 'Presenter-notes-Kimlien-EN')):
      open(f'{name}.html', 'w', encoding='utf-8').write(notes(L))
      pg.goto('file://' + os.path.abspath(f'{name}.html'), wait_until='load', timeout=90000); pg.wait_for_timeout(1000)
      pg.pdf(path=f'{name}.pdf', format='A4', print_background=True); print(name)
    b.close()
