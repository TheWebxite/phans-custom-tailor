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
  <h1>{t("Cẩm nang trước buổi gặp Phan's", "Handbook for the Phan's meeting")}</h1>
  <p class="sub">{t("Mọi thứ em cần biết, viết cho người không làm kỹ thuật. Đọc một lần trước khi đi, mang theo để tra khi cần.", "Everything you need to know, written for someone who isn't technical. Read it once before you go, and keep it handy.")}</p>
  <p class="sub">{t("Xin, TheWebxite · tháng 10/2026", "Xin, TheWebxite · October 2026")}</p></header>
  <div class="box"><h3>{t("Nếu chỉ nhớ được 5 điều", "If you remember only five things")}</h3>
  <ol>
    <li>{t("Mục tiêu hôm nay: cho anh chị xem, thống nhất phần việc, và lấy thông tin. <b>Không ký, không chốt giá.</b>", "Today's goal: show them, agree what we'll build, collect information. <b>No signing, no prices.</b>")}</li>
    <li>{t("Giá do Xin gửi sau buổi gặp. Nếu hỏi giá, nói: “Xin sẽ gửi báo giá chi tiết ngay sau hôm nay.”", "Xin sends the price after the meeting. If they ask: “Xin will send a detailed quote right after today.”")}</li>
    <li>{t("Tên miền là địa chỉ, hosting là ngôi nhà. Email không bị ảnh hưởng. Đặt lịch giữ Koalendar như cũ.", "The domain is the address, hosting is the house. Email isn't affected. Booking stays on Koalendar.")}</li>
    <li>{t("Giai đoạn đầu cửa hàng chỉ để trưng bày, chưa thanh toán online.", "In the first phase the shop is a showcase only, no online payment.")}</li>
    <li>{t("Câu nào không chắc: “Em ghi lại, Xin sẽ trả lời bằng tin nhắn sau buổi gặp.” Không sao cả.", "Not sure of an answer? “I'll note it and Xin will reply in writing after the meeting.” That's completely fine.")}</li>
  </ol></div>'''

  s1 = sec(t("1. Câu chuyện đến giờ", "1. The story so far"), ul([
    t("<b>Phan's Custom Tailor</b> là tiệm may vest trong một villa ở Saigon Pearl, Bình Thạnh, do anh Thịnh và chị Thương (đều học kiến trúc) làm chủ. Khách chủ yếu là người nước ngoài: 975 đánh giá Tripadvisor (4,8 điểm), 1.115 đánh giá Google (4,9 điểm).", "<b>Phan's Custom Tailor</b> is a tailor in a villa in Saigon Pearl, Binh Thanh, run by Thinh and Thuong Phan (both trained as architects). Most customers are from overseas: 975 Tripadvisor reviews (4.8), 1,115 Google reviews (4.9)."),
    t("Website hiện tại của họ là <b>tailormadesuit.net</b>, làm trên Haravan, khá cũ.", "Their current site is <b>tailormadesuit.net</b>, built on Haravan, and dated."),
    t("Xin làm sẵn một <b>bản mẫu</b> (demo) website mới để họ xem: " + f'<a href="{DEMO}">phans-custom-tailor-demo.vercel.app</a>' + ". Em đã gửi bản mẫu và tin nhắn cho anh Thịnh, và đã nói chuyện qua điện thoại.", "Xin built a <b>mock-up</b> (demo) of a new site for them to see: " + f'<a href="{DEMO}">phans-custom-tailor-demo.vercel.app</a>' + ". You've sent it to Thinh with our messages and spoken on the phone."),
    t("Anh chị muốn làm tiếp. Hôm nay em đến villa để trình bày trực tiếp.", "They want to go ahead. Today you present in person at the villa."),
    t("Anh Thịnh có làm việc với một đội <b>Web 3D</b> khác. Mình không cạnh tranh với họ (xem mục 8).", "Thinh also works with a separate <b>Web 3D</b> team. We're not competing with them (see section 8)."),
  ]))

  s2 = sec(t("2. Mang theo và chuẩn bị trước", "2. What to bring and prepare"), ul([
    t("Tải sẵn file <b>Gap-mat-Phans-VI.pdf</b> vào laptop hoặc iPad (đừng phụ thuộc wifi của khách). Mở thử một lần ở nhà.", "Download <b>Gap-mat-Phans-VI.pdf</b> onto your laptop or iPad beforehand (don't rely on their wifi). Open it once at home to check."),
    t("Mở sẵn bản mẫu trên trình duyệt (Chrome hoặc Safari). Bật 4G/phát wifi từ điện thoại phòng khi mạng chậm.", "Have the mock-up open in a browser (Chrome or Safari). Keep your phone hotspot ready in case the internet is slow."),
    t("Sạc đầy máy. Mang theo sổ và bút, hoặc in mục 7 (checklist) của cẩm nang này để đánh dấu.", "Charge your devices. Bring a notebook and pen, or print section 7 (the checklist) to tick off."),
    t("Để điện thoại có ghi chú trình bày (Ghi-chu-trinh-bay-Kimlien-VI.pdf) để liếc khi cần.", "Keep the presenter notes (Ghi-chu-trinh-bay-Kimlien-VI.pdf) on your phone to glance at."),
    t("Hỏi trước anh chị có muốn gửi file trình bày không. File giờ chỉ khoảng 2 MB, gửi qua Zalo được.", "Offer to send them the deck afterwards. It's only about 2 MB now and goes through Zalo easily."),
  ], 'check') + tip(t("Lưu ý: bản mẫu đang có nút <b>“Try-On”</b> (thử đồ bằng AI) trên ảnh sản phẩm. Mình <b>chưa</b> giới thiệu tính năng này. Nếu anh chị bấm vào hoặc hỏi: “Đó là tính năng bên em đang thử nghiệm, chưa nằm trong đề xuất. Xin sẽ báo thêm.”", "Note: the mock-up shows <b>“Try-On”</b> buttons (AI try-on) on product photos. We are <b>not</b> offering this yet. If they tap it or ask: “It's a feature we're testing, not part of the proposal yet. Xin will follow up.”")))

  gl = [
    (t("Website", "Website"), t("“Cửa hàng trên mạng” của Phan's. Khách ở nước ngoài xem giá, vải, cách đặt lịch trước khi bay sang.", "Phan's “shop on the internet”. Overseas customers check prices, cloth and booking before they fly.")),
    (t("Bản mẫu (demo / mock-up)", "Mock-up (demo)"), t("Bản xem thử Xin làm sẵn. Một số ảnh và sản phẩm là mẫu, sẽ thay bằng ảnh thật của Phan's.", "A preview Xin built. Some photos and products are samples, to be swapped for Phan's real ones.")),
    (t("Tên miền (domain)", "Domain"), t("Địa chỉ website, như địa chỉ nhà. Phan's đã có phanscustomtailor.com và tailormadesuit.net. Trả phí theo năm, luôn đứng tên Phan's.", "The site's address, like a street address. Phan's already owns phanscustomtailor.com and tailormadesuit.net. Paid yearly, always in Phan's name.")),
    ("Hosting", t("Ngôi nhà chứa website (nội dung, hình ảnh) để mở được 24/7. TheWebxite lo hết.", "The house the website lives in, so it's open 24/7. TheWebxite looks after it.")),
    (t("DNS / trỏ tên miền", "DNS / pointing the domain"), t("Tấm biển chỉ đường: đổi biển để địa chỉ cũ dẫn đến nhà mới. Bên mình làm, chỉ cần quyền vào tài khoản tên miền.", "The signpost: we change it so the address leads to the new house. We do it; we just need access to the domain account.")),
    (t("Chuyển hướng (redirect)", "Redirects"), t("Ai bấm link cũ trên Google vẫn tới đúng trang mới. Nên Phan's không mất khách tìm kiếm.", "Anyone clicking an old Google link still lands on the right new page, so Phan's keeps its search visitors.")),
    ("Haravan", t("Nơi đang chứa website cũ. Vẫn chạy cho tới ngày đổi, sau đó anh chị ngưng gói.", "Where the old site lives now. It keeps running until switch-over, then they can cancel it.")),
    ("Koalendar", t("Lịch đặt hẹn Phan's đang dùng. Website mới chỉ gắn nút dẫn sang đó, không đổi gì.", "The booking calendar Phan's already uses. The new site just links to it, nothing changes.")),
    (t("Cổng thanh toán", "Payment gateway"), t("Dịch vụ để khách trả tiền bằng thẻ trên mạng (ở Việt Nam: OnePay, VNPay). Chỉ cần nếu sau này bán online.", "A service for paying by card online (in Vietnam: OnePay, VNPay). Only needed if they sell online later.")),
    (t("Bảo trì", "Maintenance"), t("Sau khi website chạy: bên mình theo dõi, sao lưu, sửa lỗi, cập nhật nội dung nhỏ khi anh chị nhắn.", "After launch we watch over it, back it up, fix problems and make small updates when they ask.")),
    ("Google Business", t("Trang của Phan's trên Google Maps (giờ mở cửa, đánh giá). Cần quyền để gắn website mới vào.", "Phan's page on Google Maps (hours, reviews). We need access to link the new site to it.")),
  ]
  s3 = sec(t("3. Website hoạt động thế nào (giải thích như kể chuyện)", "3. How a website works, explained simply"),
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
  s4 = sec(t("4. Mình đề xuất gì", "4. What we're offering"),
    p(t("Biến bản mẫu thành website chính thức của Phan's. Khoảng <b>1 tuần</b> làm việc, tính từ khi anh chị gửi đủ ảnh và thông tin.", "Turn the mock-up into Phan's official website. About <b>one week</b> of work, counted from when they send all the photos and details.")) +
    table(inc, [t("Hạng mục", "Item"), t("Giai đoạn đầu", "First phase")], 'inc') +
    p(t("<b>Vì sao chưa bán online?</b> Bán online cần người xử lý đơn mỗi ngày, đóng gói, gửi hàng ra nước ngoài, đổi trả, và đăng ký cổng thanh toán. Còn may đo thì khách vẫn phải đến villa lấy số đo. Nên giai đoạn đầu trưng bày là đủ; khi nào anh chị muốn bán online thì làm sau.",
          "<b>Why no online sales yet?</b> It needs someone handling orders every day, packing, overseas shipping, returns and a payment gateway. And for made-to-measure, customers still have to come in to be measured. So a showcase is enough for now; online sales can come later.")))

  flow = [
    ("1–2", t("Bìa và thư của Xin", "Cover and Xin's letter"), t("Chào, cảm ơn. Để anh chị tự đọc thư.", "Greet, thank them. Let them read the letter.")),
    ("3", "975", t("Khách nước ngoài tìm Phan's trên mạng trước khi bay. Website là nơi gặp đầu tiên.", "Overseas customers look Phan's up before flying. The site is where they meet Phan's first.")),
    ("4–7", t("Trang chủ, giá, điện thoại, cũ và mới", "Home, prices, phones, old vs new"), t("Cho xem website. Hỏi giá còn thiếu. Hỏi ai đọc lại bản tiếng Việt.", "Show the site. Ask for missing prices. Ask who can read the Vietnamese.")),
    ("8–9", t("Đặt lịch, cửa hàng", "Booking, shop"), t("Koalendar giữ nguyên. Cửa hàng chỉ trưng bày, bán online để sau.", "Koalendar stays. The shop is a showcase; online sales later.")),
    ("10–11", t("Tên miền, đội 3D", "Domain, 3D team"), t("Giải thích bằng hình ngôi nhà. Hỏi chọn tên miền nào làm chính.", "Explain with the house picture. Ask which domain they want as main.")),
    ("12–14", t("Giai đoạn, cần chuẩn bị, lịch trình", "Phases, what we need, timeline"), t("Đi qua checklist mục 7. Không hứa ngày cụ thể.", "Go through the section 7 checklist. No fixed dates.")),
    ("15", t("Kết", "Close"), t("Cho quét mã QR. Xin gửi báo giá sau. Cảm ơn.", "Let them scan the QR. Xin sends the quote. Thank them.")),
  ]
  s5 = sec(t("5. Đi qua bản trình bày (khoảng 20 phút)", "5. Going through the deck (about 20 minutes)"),
    table(flow, [t("Trang", "Slides"), t("Nội dung", "What's on it"), t("Em nói / hỏi gì", "What to say or ask")], 'flow') +
    f'<h3>{t("Cho xem bản mẫu thật (nếu có mạng)", "Showing the live mock-up (if there’s internet)")}</h3>' + ul([
      t("Mở link, bấm <b>MENU</b> góc trên bên trái để xem các trang: Vest và giá, Quy trình, Vải, Cửa hàng, Liên hệ.", "Open the link and tap <b>MENU</b> (top left) to see the pages: Suits & pricing, Process, Fabrics, Shop, Contact."),
      t("Bấm <b>EN</b> cạnh nút đặt lịch để đổi sang <b>VI</b> (tiếng Việt) hoặc <b>中文</b> (tiếng Trung). Trang đang xem giữ nguyên.", "Tap <b>EN</b> next to the booking button to switch to <b>VI</b> or <b>中文</b>. You stay on the same page."),
      t("Đưa điện thoại cho anh chị tự lướt, khách thường xem trên điện thoại.", "Hand them the phone to scroll themselves; most customers look on a phone."),
      t("Trang <b>Liên hệ</b>, kéo xuống <b>“Chọn giờ hẹn tư vấn”</b>: lịch Koalendar của Phan's hiện ngay trong website, giống web cũ. Bấm “Book now” để anh chị thấy giờ trống, nhưng <b>đừng đặt hết các bước</b>: sẽ tạo lịch hẹn thật.", "On the <b>Contact</b> page, scroll to <b>“Choose a time for your consultation”</b>: Phan's Koalendar calendar shows right inside the site, like the old one. Tap “Book now” to show the free times, but <b>don't finish a booking</b>: it would create a real appointment."),
      t("Đừng gửi thử form “Gửi yêu cầu” trên trang Liên hệ: nó gửi email thật tới Phan's.", "Don't test the enquiry form on the Contact page: it sends a real email to Phan's."),
    ]))

  qa = [
    (t("Hết bao nhiêu tiền?", "How much?"), t("“Xin sẽ gửi báo giá chi tiết ngay sau hôm nay, theo những phần anh chị chọn.” Không nói con số.", "“Xin will send a detailed quote right after today, based on what you choose.” No numbers.")),
    (t("Có phí hàng tháng không?", "Is there a monthly fee?"), t("“Có phí hosting và bảo trì, Xin sẽ ghi rõ trong báo giá.”", "“Yes, for hosting and maintenance. Xin will list it in the quote.”")),
    (t("Bao lâu xong?", "How long?"), t("“Khoảng 1 tuần sau khi anh chị gửi đủ ảnh và thông tin.”", "“About a week after you send all the photos and details.”")),
    (t("Tự sửa nội dung được không?", "Can we edit it ourselves?"), t("“Anh chị chỉ cần nhắn, bên em sửa trong gói bảo trì. Muốn tự sửa thì mình bàn thêm.”", "“Just message us and we update it under maintenance. If you want to edit it yourselves, we can discuss.”")),
    (t("Khách còn đặt lịch hẹn đến đo được như web cũ không?", "Can customers still book a measuring appointment like on the old site?"), t("“Được ạ. Trang Liên hệ có lịch Koalendar ngay trong trang, khách chọn ngày giờ như bây giờ. Lịch hẹn vẫn về Koalendar của anh chị, không đổi gì. Nút đặt lịch còn có trên mọi trang.”", "“Yes. The Contact page has your Koalendar calendar built in, so customers pick a day and time as they do now. Appointments still go to your Koalendar, nothing changes. There's also a booking button on every page.”")),
    (t("Có mất thứ hạng Google không?", "Will we lose our Google ranking?"), t("“Không, link cũ tự chuyển sang trang mới.”", "“No, old links lead to the new pages.”")),
    (t("Email có bị ảnh hưởng không?", "Will email be affected?"), t("“Không, info@phantailor.com giữ nguyên.”", "“No, info@phantailor.com stays as it is.”")),
    (t("Khi nào ngưng Haravan?", "When do we cancel Haravan?"), t("“Sau khi website mới chạy ổn. Trước đó web cũ vẫn chạy bình thường.”", "“Once the new site runs smoothly. Until then the old one keeps working.”")),
    (t("Tên miền của ai?", "Who owns the domain?"), t("“Luôn là của Phan's. Bên em chỉ cần quyền để trỏ.”", "“Always Phan's. We only need access to point it.”")),
    (t("Bán online được không?", "Can we sell online?"), t("“Được, nhưng nên làm ở giai đoạn sau. Xin sẽ gửi phương án riêng nếu anh chị muốn.”", "“Yes, but better as a later phase. Xin can send options if you'd like.”")),
    (t("Nút Try-On / thử đồ AI là gì?", "What's the Try-On / AI button?"), t("“Tính năng bên em đang thử nghiệm, chưa nằm trong đề xuất. Xin sẽ báo thêm.”", "“A feature we're testing, not part of the proposal yet. Xin will follow up.”")),
    (t("Còn đội 3D thì sao?", "What about the 3D team?"), t("“Hai bên bổ sung cho nhau. Website là ngôi nhà, phần 3D có thể là một trang trong đó. Bên em sẵn sàng làm việc với họ.”", "“They fit together. The website is the house, the 3D work can be a page inside it. We're happy to work with them.”")),
    (t("Ai dịch tiếng Trung?", "Who did the Chinese?"), t("“Bên em dịch. Anh chị chỉ cần một người đọc lại bản tiếng Việt.”", "“We did. You just need someone to read the Vietnamese.”")),
    (t("Có dùng AI không?", "Did you use AI?"), t("“Có. TheWebxite là công ty phần mềm và AI, dùng AI để làm nhanh và tốt hơn. Thiết kế, kiểm tra và hỗ trợ đều do người thật làm.”", "“Yes. TheWebxite is a software and AI company; AI helps us work faster and better. Design, testing and support are done by real people.”")),
  ]
  s6 = sec(t("6. Câu anh chị có thể hỏi và cách trả lời", "6. Questions they may ask, and what to say"), table(qa, [t("Nếu anh chị hỏi", "If they ask"), t("Em trả lời", "You say")], 'qa'))

  ck = [
    t("<b>Tên miền:</b> ai giữ tài khoản phanscustomtailor.com và tailormadesuit.net; chọn tên nào làm chính (bên mình đề xuất phanscustomtailor.com).", "<b>Domain:</b> who holds the account for phanscustomtailor.com and tailormadesuit.net; which one as main (we suggest phanscustomtailor.com)."),
    t("<b>Ảnh:</b> villa, anh chị, đồ đã may xong, vải; file logo gốc. Hỏi khi nào gửi được.", "<b>Photos:</b> the villa, the two of them, finished garments, cloth; the original logo. Ask when they can send them."),
    t("<b>Giá còn thiếu:</b> blazer, gilê, măng tô, đồ nữ. Hiện giá bằng VND hay thêm USD?", "<b>Missing prices:</b> blazer, waistcoat, overcoat, women's. VND only, or USD too?"),
    t("<b>Chi tiết:</b> năm thành lập (web cũ ghi “từ 2013”), lịch nghỉ Tết, khách ở nước ngoài đặt may lại được không. <b>Thời gian may:</b> web cũ ghi 5 ngày làm việc, nhưng lịch Koalendar ghi 7–10 ngày. Hỏi con số nào đúng.", "<b>Details:</b> the year they started (old site says “since 2013”), Tết closures, whether customers abroad can reorder. <b>Turnaround:</b> the old site says 5 working days but their Koalendar says 7–10 days. Ask which is right."),
    t("<b>Người đọc lại bản tiếng Việt</b> bên Phan's.", "<b>Someone at Phan's to read the Vietnamese.</b>"),
    t("<b>Tài khoản:</b> link Koalendar, trang Facebook chính thức, quyền Google Business.", "<b>Accounts:</b> the Koalendar link, the official Facebook page, Google Business access."),
    t("<b>Người liên hệ chính</b> và kênh (Zalo, WhatsApp, email).", "<b>Main contact person</b> and channel (Zalo, WhatsApp, email)."),
    t("<b>Đội 3D:</b> có muốn hai bên phối hợp không, xin liên hệ.", "<b>3D team:</b> do they want us to coordinate? Get a contact."),
  ]
  s7 = sec(t("7. Thông tin cần lấy (đánh dấu khi có)", "7. Information to collect (tick as you go)"),
    p(t("Không cần có đủ hôm nay. Chỉ cần hỏi và ghi lại khi nào anh chị gửi.", "You don't need everything today. Just ask, and note when they'll send it.")) + ul(ck, 'check'))

  s8 = sec(t("8. Đừng hứa", "8. Don't promise"), ul([
    t("Giá cụ thể, giảm giá, hay điều khoản thanh toán.", "A specific price, a discount or payment terms."),
    t("Bán online hay thanh toán thẻ ở giai đoạn đầu.", "Online sales or card payment in the first phase."),
    t("Phòng thử đồ AI.", "The AI fitting room."),
    t("Ngày ra mắt cụ thể.", "A specific launch date."),
    t("Trang quản trị để anh chị tự sửa website.", "A dashboard for them to edit the site themselves."),
    t("Mua tên miền mới (Phan's đã có).", "Buying a new domain (Phan's already has one)."),
  ], 'no'))

  s9 = sec(t("9. Khi bí, nói thế này", "9. When you're stuck, say this"), ul([
    t("“Câu này hay, em ghi lại để Xin trả lời chính xác bằng tin nhắn nhé anh.”", "“Good question. I'll note it so Xin can answer properly in writing.”"),
    t("“Phần kỹ thuật bên em lo hết, anh chị chỉ cần gửi ảnh và thông tin thôi ạ.”", "“We handle all the technical side. You only need to send photos and details.”"),
    t("“Cái này nằm trong báo giá, Xin sẽ gửi ngay sau hôm nay.”", "“That will be in the quote, which Xin sends right after today.”"),
  ]) + p(t("Trong buổi gặp, có gì gấp thì nhắn Xin qua WhatsApp.", "If something urgent comes up during the meeting, message Xin on WhatsApp.")))

  s10 = sec(t("10. Sau buổi gặp, nhắn Xin", "10. After the meeting, send Xin"), ul([
    t("Anh chị đồng ý những phần nào, muốn thêm hay bỏ gì.", "What they agreed to, and anything to add or drop."),
    t("Tên miền chọn làm chính, và ai giữ tài khoản.", "The main domain, and who holds the account."),
    t("Giá còn thiếu và các chi tiết đã có.", "The missing prices and details you got."),
    t("Câu hỏi mình chưa trả lời được.", "Questions we couldn't answer."),
    t("Khi nào anh chị gửi ảnh và thông tin, và muốn nhận báo giá lúc nào.", "When they'll send photos and details, and when they want the quote."),
    t("Ấn tượng chung: anh chị có vẻ hài lòng không, lo ngại điều gì.", "Your overall feel: did they seem happy, what worried them."),
  ]))

  body = cover + s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9 + s10
  return f'''<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{t("Cẩm nang Kimlien", "Kimlien handbook")}</title>
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
  outs = {'vi': ('Cam-nang-Kimlien-VI', "Cẩm nang buổi gặp Phan's · Nội bộ"), 'en': ('Handbook-Kimlien-EN', "Phan's meeting handbook · Internal")}
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
