"""Kimlien's beginner handbook for the meeting at Phan's villa, Vietnamese + English from one source.
Run from the project root: /Users/hengzhexin/anaconda3/bin/python3 pitch/meet/build_handbook.py
Writes pitch/meet/Cam-nang-Kimlien-VI.pdf and pitch/meet/Handbook-Kimlien-EN.pdf. Internal, not for the client."""
import os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
DEMO = 'https://phans-custom-tailor-demo.vercel.app/'

def build(L):
  t = lambda vi, en: vi if L == 'vi' else en
  def sec(title, body, cls=''): return f'<section class="{cls}"><h2>{title}</h2>{body}</section>'
  def ul(items, cls=''): return f'<ul class="{cls}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
  def p(x): return f'<p>{x}</p>'
  def table(rows, heads, cls=''):
    return f'<table class="{cls}"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in heads) + '</tr></thead><tbody>' + ''.join(
      '<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table>'
  def tip(x): return f'<div class="tip">{x}</div>'

  dia = f'''<svg class="dia" viewBox="0 0 680 200" xmlns="http://www.w3.org/2000/svg" font-family="Hanken Grotesk, sans-serif">
  <defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#1e2a3a"/></marker></defs>
  <rect x="6" y="14" width="200" height="92" fill="#fff" stroke="#1e2a3a" stroke-width="1.5"/>
  <text x="106" y="44" text-anchor="middle" font-size="15" font-weight="600" fill="#141414">{t("Tên miền", "Domain")}</text>
  <text x="106" y="66" text-anchor="middle" font-size="12" fill="#5f5f5f">phanscustomtailor.com</text>
  <text x="106" y="88" text-anchor="middle" font-size="12" fill="#1e2a3a">{t("= ĐỊA CHỈ NHÀ", "= THE STREET ADDRESS")}</text>
  <line x1="208" y1="60" x2="268" y2="60" stroke="#1e2a3a" stroke-width="1.5" marker-end="url(#ar)"/>
  <rect x="272" y="14" width="160" height="92" fill="#fff" stroke="#1e2a3a" stroke-width="1.5"/>
  <text x="352" y="44" text-anchor="middle" font-size="15" font-weight="600" fill="#141414">DNS</text>
  <text x="352" y="66" text-anchor="middle" font-size="12" fill="#5f5f5f">{t("= tấm biển chỉ đường", "= the signpost")}</text>
  <text x="352" y="88" text-anchor="middle" font-size="12" fill="#5f5f5f">{t("bên mình cài", "we set it up")}</text>
  <line x1="434" y1="60" x2="494" y2="60" stroke="#1e2a3a" stroke-width="1.5" marker-end="url(#ar)"/>
  <rect x="498" y="14" width="176" height="92" fill="#1e2a3a"/>
  <text x="586" y="44" text-anchor="middle" font-size="15" font-weight="600" fill="#fff">Hosting</text>
  <text x="586" y="66" text-anchor="middle" font-size="12" fill="#d8d5cf">{t("= NGÔI NHÀ", "= THE HOUSE")}</text>
  <text x="586" y="88" text-anchor="middle" font-size="12" fill="#d8d5cf">{t("chứa website, mở 24/7", "where the site lives, 24/7")}</text>
  <rect x="272" y="130" width="402" height="58" fill="#f7f6f3" stroke="#d8d5cf" stroke-dasharray="4 4"/>
  <text x="473" y="155" text-anchor="middle" font-size="13" font-weight="600" fill="#141414">{t("Email info@phantailor.com = HỘP THƯ RIÊNG", "Email info@phantailor.com = A SEPARATE MAILBOX")}</text>
  <text x="473" y="175" text-anchor="middle" font-size="12" fill="#5f5f5f">{t("không liên quan, không bị đụng tới", "not connected, not touched")}</text>
  <text x="6" y="152" font-size="12" fill="#5f5f5f">{t("Website cũ (Haravan) vẫn chạy", "The old site (Haravan) keeps")}</text>
  <text x="6" y="170" font-size="12" fill="#5f5f5f">{t("cho đến ngày đổi sang web mới.", "running until switch-over day.")}</text>
</svg>'''

  cover = f'''<header class="top">
  <p class="kicker">{t("Nội bộ · Dành cho Kimlien · Không đưa cho khách", "Internal · For Kimlien · Not for the client")}</p>
  <h1>{t("Cẩm nang kỹ thuật", "Tech cheat sheet")}</h1>
  <p class="sub">{t("Để tra nhanh khi anh chị hỏi về tên miền, hosting, email, đặt lịch hay chuyển sang website mới. Câu nào không có ở đây, cứ nói: “Em ghi lại, Xin sẽ trả lời bằng tin nhắn sau buổi gặp.”", "For quick answers when they ask about the domain, hosting, email, booking or switching to the new site. If a question isn't here, say: “I'll note it and Xin will reply in writing after the meeting.”")}</p></header>
  <div class="box"><h3>{t("Trả lời nhanh", "Quick answers")}</h3>
  <ol>
    <li>{t("<b>Tên miền</b> là địa chỉ, <b>hosting</b> là ngôi nhà. Phan's đã có tên miền, không cần mua mới, và tên miền luôn đứng tên Phan's.", "The <b>domain</b> is the address, <b>hosting</b> is the house. Phan's already owns its domains, nothing new to buy, and they always stay in Phan's name.")}</li>
    <li>{t("<b>Email</b> info@phantailor.com không bị ảnh hưởng gì.", "<b>Email</b> (info@phantailor.com) isn't affected at all.")}</li>
    <li>{t("<b>Đặt lịch</b> vẫn bằng Koalendar như bây giờ, lịch hiện ngay trên trang Liên hệ.", "<b>Booking</b> stays on Koalendar as now, with the calendar right on the Contact page.")}</li>
    <li>{t("<b>Web cũ</b> chạy đến ngày đổi. Link cũ trên Google tự dẫn sang trang mới, không mất khách.", "The <b>old site</b> runs until switch-over day. Old Google links lead to the new pages, so no customers are lost.")}</li>
    <li>{t("<b>Thanh toán online</b> để giai đoạn sau. Giai đoạn đầu cửa hàng chỉ trưng bày.", "<b>Online payment</b> comes in a later phase. At first the shop is a showcase only.")}</li>
  </ol></div>'''

  gl = [
    (t("Tên miền (domain)", "Domain"), t("Địa chỉ website, như địa chỉ nhà. Phan's đã có phanscustomtailor.com và tailormadesuit.net. Trả phí theo năm, luôn đứng tên Phan's.", "The site's address, like a street address. Phan's already owns phanscustomtailor.com and tailormadesuit.net. Paid yearly, always in Phan's name.")),
    ("Hosting", t("Ngôi nhà chứa website (nội dung, hình ảnh) để mở được 24/7. TheWebxite lo hết.", "The house the website lives in, so it's open 24/7. TheWebxite looks after it.")),
    (t("DNS / trỏ tên miền", "DNS / pointing the domain"), t("Tấm biển chỉ đường: đổi biển để địa chỉ cũ dẫn đến nhà mới. Bên mình làm, chỉ cần quyền vào tài khoản tên miền.", "The signpost: we change it so the address leads to the new house. We do it; we just need access to the domain account.")),
    (t("Chuyển hướng (redirect)", "Redirects"), t("Ai bấm link cũ trên Google vẫn tới đúng trang mới. Nên Phan's không mất khách tìm kiếm.", "Anyone clicking an old Google link still lands on the right new page, so Phan's keeps its search visitors.")),
    ("Haravan", t("Nơi đang chứa website cũ. Vẫn chạy cho tới ngày đổi, sau đó anh chị ngưng gói.", "Where the old site lives now. It keeps running until switch-over, then they can cancel it.")),
    ("Koalendar", t("Lịch đặt hẹn Phan's đang dùng. Website mới hiện lịch này ngay trên trang Liên hệ (như web cũ) và có nút đặt lịch trên mọi trang. Lịch hẹn vẫn về Koalendar, không đổi gì.", "The booking calendar Phan's already uses. The new site shows it on the Contact page (like the old site) with a booking button on every page. Appointments still go to Koalendar, nothing changes.")),
    (t("Cổng thanh toán", "Payment gateway"), t("Dịch vụ để khách trả tiền bằng thẻ trên mạng (ở Việt Nam: OnePay, VNPay). Chỉ cần nếu sau này bán online.", "A service for paying by card online (in Vietnam: OnePay, VNPay). Only needed if they sell online later.")),
    (t("Bảo trì", "Maintenance"), t("Sau khi website chạy: bên mình theo dõi, sao lưu, sửa lỗi, cập nhật nội dung nhỏ khi anh chị nhắn.", "After launch we watch over it, back it up, fix problems and make small updates when they ask.")),
    ("Google Business", t("Trang của Phan's trên Google Maps (giờ mở cửa, đánh giá). Cần quyền để gắn website mới vào.", "Phan's page on Google Maps (hours, reviews). We need access to link the new site to it.")),
  ]
  s3 = sec(t("1. Website hoạt động thế nào", "1. How a website works"),
    p(t("Hình dung website như một căn nhà. Có ba thứ: <b>địa chỉ</b> (tên miền), <b>ngôi nhà</b> (hosting), và <b>tấm biển chỉ đường</b> (DNS) để khách gõ địa chỉ là tới đúng nhà. Email là hộp thư riêng, không nằm trong nhà nên không bị ảnh hưởng.",
          "Think of a website as a house. There are three parts: the <b>address</b> (domain), the <b>house</b> (hosting), and the <b>signpost</b> (DNS) that sends visitors who type the address to the right house. Email is a separate mailbox, not inside the house, so it's not affected.")) +
    dia + p(t("Khi đổi sang website mới, mình chỉ dựng nhà mới rồi đổi biển chỉ đường. Địa chỉ giữ nguyên, khách không thấy gián đoạn.", "When we switch, we build the new house and change the signpost. The address stays the same, so customers notice no break.")) +
    f'<h3>{t("Từ ngữ có thể nghe thấy", "Words you might hear")}</h3>' + table(gl, [t("Từ", "Word"), t("Nghĩa là gì", "What it means")], 'gloss'))

  inc = [
    (t("Website 3 ngôn ngữ: Anh (chính), Việt, Trung", "3-language site: English (main), Vietnamese, Chinese"), t("Có", "Yes")),
    (t("Bảng giá, quy trình may, thông tin vải", "Prices, the process, cloth"), t("Có", "Yes")),
    (t("Đặt lịch hẹn đến đo ngay trên website (lịch Koalendar), WhatsApp, Zalo", "Booking a measuring visit on the site (Koalendar calendar), WhatsApp, Zalo"), t("Có, như web cũ", "Yes, as today")),
    (t("Cửa hàng trưng bày: khách xem rồi nhắn hoặc đặt lịch", "Showcase shop: customers browse, then message or book"), t("Có", "Yes")),
    (t("Chuyển 7 bài viết từ web cũ, tối ưu Google", "Move the 7 old articles, Google optimisation"), t("Có", "Yes")),
    (t("Hosting, sao lưu, bảo trì", "Hosting, backups, maintenance"), t("TheWebxite lo", "TheWebxite")),
    (t("Bán online, giỏ hàng, thanh toán thẻ", "Online sales, cart, card payment"), t("Để sau", "Later")),
    (t("Phòng thử đồ AI", "AI fitting room"), t("Chưa đề xuất", "Not offered yet")),
  ]
  s4 = sec(t("2. Website mới làm được gì", "2. What the new site does"),
    p(t("Biến bản mẫu thành website chính thức của Phan's. Khoảng <b>1 tuần</b> làm việc, tính từ khi anh chị gửi đủ ảnh và thông tin.", "Turn the mock-up into Phan's official website. About <b>one week</b> of work, counted from when they send all the photos and details.")) +
    table(inc, [t("Hạng mục", "Item"), t("Giai đoạn đầu", "First phase")], 'inc') +
    p(t("<b>Vì sao chưa bán online?</b> Bán online cần người xử lý đơn mỗi ngày, đóng gói, gửi hàng ra nước ngoài, đổi trả, và đăng ký cổng thanh toán. Còn may đo thì khách vẫn phải đến villa lấy số đo. Nên giai đoạn đầu trưng bày là đủ; khi nào anh chị muốn bán online thì làm sau.",
          "<b>Why no online sales yet?</b> It needs someone handling orders every day, packing, overseas shipping, returns and a payment gateway. And for made-to-measure, customers still have to come in to be measured. So a showcase is enough for now; online sales can come later.")))

  s5 = sec(t("4. Khi cho xem bản mẫu", "4. Showing the mock-up"), ul([
      t("Mở link, bấm <b>MENU</b> góc trên bên trái để xem các trang: Vest và giá, Quy trình, Vải, Cửa hàng, Liên hệ.", "Open the link and tap <b>MENU</b> (top left) to see the pages: Suits & pricing, Process, Fabrics, Shop, Contact."),
      t("Bấm <b>EN</b> cạnh nút đặt lịch để đổi sang <b>VI</b> (tiếng Việt) hoặc <b>中文</b> (tiếng Trung). Trang đang xem giữ nguyên.", "Tap <b>EN</b> next to the booking button to switch to <b>VI</b> or <b>中文</b>. You stay on the same page."),
      t("Đưa điện thoại cho anh chị tự lướt, khách thường xem trên điện thoại.", "Hand them the phone to scroll themselves; most customers look on a phone."),
      t("Trang <b>Liên hệ</b>, kéo xuống <b>“Chọn giờ hẹn tư vấn”</b>: lịch Koalendar của Phan's hiện ngay trong website, giống web cũ. Bấm “Book now” để anh chị thấy giờ trống, nhưng <b>đừng đặt hết các bước</b>: sẽ tạo lịch hẹn thật.", "On the <b>Contact</b> page, scroll to <b>“Choose a time for your consultation”</b>: Phan's Koalendar calendar shows right inside the site, like the old one. Tap “Book now” to show the free times, but <b>don't finish a booking</b>: it would create a real appointment."),
      t("Đừng gửi thử form “Gửi yêu cầu” trên trang Liên hệ: nó gửi email thật tới Phan's.", "Don't test the enquiry form on the Contact page: it sends a real email to Phan's."),
      t("Nút <b>“Try-On”</b> (thử đồ bằng AI) trên ảnh sản phẩm: mình chưa giới thiệu. Nếu anh chị bấm hoặc hỏi, xem câu trả lời ở mục 3.", "The <b>“Try-On”</b> buttons (AI try-on) on product photos: we're not offering this yet. If they tap or ask, see the answer in section 3."),
    ]))

  qa = [
    (t("Có phí hàng tháng không?", "Is there a monthly fee?"), t("“Có phí hosting và bảo trì, Xin sẽ ghi rõ trong báo giá.”", "“Yes, for hosting and maintenance. Xin will list it in the quote.”")),
    (t("Bao lâu xong?", "How long?"), t("“Khoảng 1 tuần sau khi anh chị gửi đủ ảnh và thông tin.”", "“About a week after you send all the photos and details.”")),
    (t("Tự sửa nội dung được không?", "Can we edit it ourselves?"), t("“Anh chị chỉ cần nhắn, bên em sửa trong gói bảo trì. Muốn tự sửa thì mình bàn thêm.”", "“Just message us and we update it under maintenance. If you want to edit it yourselves, we can discuss.”")),
    (t("Khách còn đặt lịch hẹn đến đo được như web cũ không?", "Can customers still book a measuring appointment like on the old site?"), t("“Được ạ. Trang Liên hệ có lịch Koalendar ngay trong trang, khách chọn ngày giờ như bây giờ. Lịch hẹn vẫn về Koalendar của anh chị, không đổi gì. Nút đặt lịch còn có trên mọi trang.”", "“Yes. The Contact page has your Koalendar calendar built in, so customers pick a day and time as they do now. Appointments still go to your Koalendar, nothing changes. There's also a booking button on every page.”")),
    (t("Có mất thứ hạng Google không?", "Will we lose our Google ranking?"), t("“Không, link cũ tự chuyển sang trang mới.”", "“No, old links lead to the new pages.”")),
    (t("Email có bị ảnh hưởng không?", "Will email be affected?"), t("“Không, info@phantailor.com giữ nguyên.”", "“No, info@phantailor.com stays as it is.”")),
    (t("Khi nào ngưng Haravan?", "When do we cancel Haravan?"), t("“Sau khi website mới chạy ổn. Trước đó web cũ vẫn chạy bình thường.”", "“Once the new site runs smoothly. Until then the old one keeps working.”")),
    (t("Tên miền của ai?", "Who owns the domain?"), t("“Luôn là của Phan's. Bên em chỉ cần quyền để trỏ.”", "“Always Phan's. We only need access to point it.”")),
    (t("Bán online được không?", "Can we sell online?"), t("“Giai đoạn này website chưa gắn cổng thanh toán. Khách xem được toàn bộ sản phẩm, rồi nhắn WhatsApp/Zalo hoặc đặt lịch đến villa, chưa đặt hàng và trả tiền trên web. Nếu anh chị muốn bán và thanh toán online, mình làm ở giai đoạn sau.”", "“In this phase the site has no payment gateway. Customers can view all the products, then message on WhatsApp/Zalo or book a visit, but they can't check out or pay on the site. If you'd like online sales and payment, we can add it in the next phase.”")),
    (t("Nút Try-On / thử đồ AI là gì?", "What's the Try-On / AI button?"), t("“Tính năng bên em đang thử nghiệm, chưa nằm trong đề xuất. Xin sẽ báo thêm.”", "“A feature we're testing, not part of the proposal yet. Xin will follow up.”")),
    (t("Còn đội 3D thì sao?", "What about the 3D team?"), t("“Hai bên bổ sung cho nhau. Website là ngôi nhà, phần 3D có thể là một trang trong đó. Bên em sẵn sàng làm việc với họ.”", "“They fit together. The website is the house, the 3D work can be a page inside it. We're happy to work with them.”")),
    (t("Ai dịch tiếng Trung?", "Who did the Chinese?"), t("“Bên em dịch. Anh chị chỉ cần một người đọc lại bản tiếng Việt.”", "“We did. You just need someone to read the Vietnamese.”")),
    (t("Có dùng AI không?", "Did you use AI?"), t("“Có. TheWebxite là công ty phần mềm và AI, dùng AI để làm nhanh và tốt hơn. Thiết kế, kiểm tra và hỗ trợ đều do người thật làm.”", "“Yes. TheWebxite is a software and AI company; AI helps us work faster and better. Design, testing and support are done by real people.”")),
  ]
  s6 = sec(t("3. Câu hỏi kỹ thuật và cách trả lời", "3. Technical questions and what to say"), table(qa, [t("Nếu anh chị hỏi", "If they ask"), t("Em trả lời", "You say")], 'qa'))

  ck = [
    t("<b>Tên miền:</b> ai giữ tài khoản quản lý phanscustomtailor.com và tailormadesuit.net (để bên mình được mời vào), và chọn tên nào làm chính. Bên mình đề xuất phanscustomtailor.com.", "<b>Domain:</b> who holds the account for phanscustomtailor.com and tailormadesuit.net (so they can invite us), and which one as main. We suggest phanscustomtailor.com."),
    t("<b>Koalendar:</b> ai đang quản lý lịch. Lịch ghi may 7–10 ngày, còn web cũ ghi 5 ngày làm việc: hỏi con số nào đúng.", "<b>Koalendar:</b> who manages the calendar. It says 7–10 days for a suit, the old site says 5 working days: ask which is right."),
    t("<b>Google Business</b> (trang Phan's trên Google Maps): ai có quyền quản lý, để gắn website mới vào.", "<b>Google Business</b> (Phan's page on Google Maps): who can manage it, so the new site can be linked."),
    t("<b>Facebook:</b> trang chính thức là facebook.com/phanstailor hay /phantailor?", "<b>Facebook:</b> is the official page facebook.com/phanstailor or /phantailor?"),
    t("<b>Đội 3D:</b> nếu anh chị muốn hai bên phối hợp, xin liên hệ người phụ trách kỹ thuật bên đó.", "<b>3D team:</b> if they want us to coordinate, get their technical contact."),
  ]
  s7 = sec(t("5. Thông tin kỹ thuật cần xin", "5. Technical details to ask for"), ul(ck, 'check'))

  s8 = sec(t("6. Đừng hứa", "6. Don't promise"), ul([
    t("Bán online hay thanh toán thẻ ở giai đoạn đầu.", "Online sales or card payment in the first phase."),
    t("Phòng thử đồ AI.", "The AI fitting room."),
    t("Ngày ra mắt cụ thể.", "A specific launch date."),
    t("Trang quản trị để anh chị tự sửa website.", "A dashboard for them to edit the site themselves."),
    t("Mua tên miền mới (Phan's đã có).", "Buying a new domain (Phan's already has one)."),
  ], 'no'))

  body = cover + s3 + s4 + s6 + s5 + s7 + s8
  return f'''<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{t("Cẩm nang kỹ thuật", "Tech cheat sheet")}</title>
<link rel="stylesheet" href="fonts/fonts.css"><style>{CSS}</style></head><body>{body}</body></html>'''

CSS = r'''
@page { size: A4; margin: 16mm 16mm 18mm; }
:root { --ink:#141414; --paper:#f7f6f3; --stone:#d8d5cf; --mute:#5f5f5f; --navy:#1e2a3a; --red:#b3261e; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Hanken Grotesk", sans-serif; color: var(--ink); font-size: 11pt; line-height: 1.5; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: var(--navy); }
b { font-weight: 600; }
.top { border-bottom: 2px solid var(--navy); padding-bottom: 12px; margin-bottom: 16px; }
.kicker { font-size: 9pt; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: var(--mute); }
h1 { font-family: "Prata", serif; font-weight: 400; font-size: 26pt; line-height: 1.2; margin: 8px 0 8px; }
.sub { color: var(--mute); margin-bottom: 4px; }
.box { background: var(--paper); border-left: 4px solid var(--navy); padding: 14px 18px 12px; margin-bottom: 20px; break-inside: avoid; }
.box h3, h3 { font-family: "Prata", serif; font-weight: 400; font-size: 14pt; margin-bottom: 6px; }
h3 { margin: 14px 0 6px; break-after: avoid; }
.box ol { padding-left: 20px; } .box li { margin: 5px 0; }
section { margin-bottom: 20px; }
section.brk { break-before: page; }
h2 { font-family: "Prata", serif; font-weight: 400; font-size: 17pt; margin: 4px 0 10px; break-after: avoid; border-bottom: 1px solid var(--stone); padding-bottom: 6px; }
p { margin-bottom: 8px; }
ul { padding-left: 18px; margin-bottom: 8px; } li { margin: 4px 0; }
.dia { width: 100%; height: auto; margin: 6px 0 8px; break-inside: avoid; }
.tip { border: 1.5px solid var(--red); padding: 10px 14px; margin-top: 10px; break-inside: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 10pt; margin-bottom: 8px; }
th { text-align: left; font-size: 9pt; text-transform: uppercase; letter-spacing: .06em; color: var(--mute); border-bottom: 1.5px solid var(--ink); padding: 5px 8px 5px 0; }
td { border-bottom: 1px solid var(--stone); padding: 7px 10px 7px 0; vertical-align: top; }
tr { break-inside: avoid; }
table.gloss td:first-child, table.qa td:first-child { width: 30%; font-weight: 600; }
table.inc td:last-child { width: 22%; color: var(--navy); font-weight: 600; }
table.flow td:first-child { width: 9%; color: var(--mute); } table.flow td:nth-child(2) { width: 30%; font-weight: 600; }
ul.check { list-style: none; padding-left: 0; }
ul.check li { padding-left: 28px; position: relative; margin: 8px 0; break-inside: avoid; }
ul.check li::before { content: ""; position: absolute; left: 0; top: 3px; width: 14px; height: 14px; border: 1.5px solid var(--navy); }
ul.no { list-style: none; padding-left: 0; columns: 2; column-gap: 24px; }
ul.no li { padding-left: 20px; position: relative; break-inside: avoid; }
ul.no li::before, ul.no li::after { content: ""; position: absolute; left: 0; top: 10px; width: 11px; height: 2px; background: var(--red); transform: rotate(45deg); }
ul.no li::after { transform: rotate(-45deg); }
'''

FOOT = '<div style="width:100%;font-family:Arial,sans-serif;font-size:7.5pt;color:#5f5f5f;padding:0 16mm;display:flex;justify-content:space-between"><span>{label}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'

if __name__ == '__main__':
  outs = {'vi': ('Cam-nang-Kimlien-VI', "Cẩm nang kỹ thuật · Phan's · Nội bộ"), 'en': ('Handbook-Kimlien-EN', "Tech cheat sheet · Phan's · Internal")}
  with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for L, (name, label) in outs.items():
      open(f'{name}.html', 'w', encoding='utf-8').write(build(L))
      pg.goto('file://' + os.path.abspath(f'{name}.html'), wait_until='load', timeout=90000)
      pg.evaluate("""Promise.all(['20px Prata','16px "Hanken Grotesk"','600 16px "Hanken Grotesk"'].map(f=>document.fonts.load(f,'Aăữ')))"""); pg.wait_for_timeout(600)
      ok = pg.evaluate("""document.fonts.check('20px Prata','ữ') && document.fonts.check('16px "Hanken Grotesk"','ữ')""")
      pg.pdf(path=f'{name}.pdf', format='A4', print_background=True, display_header_footer=True,
             header_template='<span></span>', footer_template=FOOT.format(label=label),
             margin={'top': '16mm', 'bottom': '18mm', 'left': '16mm', 'right': '16mm'})
      print(name, 'fonts ok' if ok else 'FONTS NOT LOADED', round(os.path.getsize(f'{name}.pdf') / 1024), 'KB')
    b.close()
