"""Build the Phan's website proposal deck in Vietnamese and English from one source.
Run:  /Users/hengzhexin/anaconda3/bin/python3 pitch/build_pdf.py
Writes pitch/De-xuat-website-Phans-VI.pdf and pitch/Website-proposal-Phans-EN.pdf (plus the HTML sources)."""
import os
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# footer crop around the language links
f = Image.open('cap/a_footer.jpg'); W, H = f.size
f.crop((int(W * .55), int(H * .62), W, H)).save('cap/a_footer_c.jpg', 'JPEG', quality=88)

ICON = {
  'cal': '<path d="M4 6h16v14H4zM4 10h16M9 3v4M15 3v4"/>',
  'chat': '<path d="M4 5h16v11H9l-5 4z"/>',
  'tag': '<path d="M3 12l9-9h8v8l-9 9z"/><circle cx="16" cy="8" r="1.5"/>',
  'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
  'form': '<path d="M6 3h12v18H6zM9 8h6M9 12h6M9 16h4"/>',
  'cart': '<path d="M3 4h3l2 11h11l2-8H7"/><circle cx="10" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/>',
  'search': '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
  'chart': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
  'card': '<path d="M3 6h18v12H3zM3 10h18M7 15h4"/>',
  'ruler': '<path d="M3 16L16 3l5 5L8 21zM7 12l2 2M10 9l2 2M13 6l2 2"/>',
  'bell': '<path d="M6 16V11a6 6 0 0112 0v5l2 2H4zM10 20h4"/>',
  'steps': '<circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/><path d="M7 12h3M14 12h3"/>',
  'star': '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
  'bot': '<path d="M5 8h14v10H5zM12 4v4M9 13h.01M15 13h.01M9 16h6"/>',
  'gift': '<path d="M4 10h16v10H4zM3 7h18v3H3zM12 7v13M12 7c-2-4-6-3-5 0M12 7c2-4 6-3 5 0"/>',
  'group': '<circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M2 20c0-3 3-5 6-5s6 2 6 5M12 20c0-3 2-5 4-5s6 2 6 5"/>',
}
def icon(k): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICON[k]}</svg>'

LINK = 'https://phans-custom-tailor-demo.vercel.app/'

def deck(L):
  """L = 'vi' or 'en'. Returns the full HTML."""
  t = lambda vi, en: vi if L == 'vi' else en
  slides = []
  def add(html): slides.append(html)

  def head(kicker, title): return f'<header class="hd"><p class="kicker">{kicker}</p><h2>{title}</h2></header>'
  def pts(items, red=False): return f'<ul class="pts{" red" if red else ""}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
  def why(label, text): return f'<div class="why"><b>{label}</b>{text}</div>'
  def media(src, pos='center top', fit='cover', bg='#fff'):
    return f'<div class="media"><img src="{src}" style="object-position:{pos};object-fit:{fit};background:{bg}" alt=""></div>'
  WHY = t('Vì sao', 'Why')

  # 1 Cover
  add(f'''<section class="slide cover">
  <div class="left"><div>
    <img class="logo" src="logo-white.png" alt="PHAN'S">
    <h1>{t("Đề xuất website mới cho Phan's Custom Tailor", "A new website for Phan's Custom Tailor")}</h1>
    <p>{t("Bản mẫu (mock-up) để anh chị xem trước: website ba ngôn ngữ, thiết kế cho khách nước ngoài đặt may vest tại Sài Gòn.", "A working mock-up to preview: a three-language website designed for overseas customers who want a suit made in Saigon.")}</p></div>
    <div class="links">
      <div>{t("Bản mẫu website mới", "New website mock-up")}: <a href="{LINK}">phans-custom-tailor-demo.vercel.app</a></div>
      <div>{t("Website hiện tại", "Current website")}: <a href="https://tailormadesuit.net/">tailormadesuit.net</a></div>
      <div class="date">{t("Thực hiện bởi Yong, TheWebxite · Tháng 10/2026", "Prepared by Yong, TheWebxite · October 2026")}</div>
    </div></div>
  <div class="right"><img src="img/cover.jpg" alt=""></div></section>''')

  # 2 Context
  add(f'''<section class="slide">{head(t("Bối cảnh", "Context"), t("Phần lớn khách của Phan's là người nước ngoài, và họ quyết định trước khi đặt vé máy bay", "Most of Phan's customers are from overseas, and they decide before they book their flight"))}
  <div class="body two">
    <div class="col">
      <p class="lead">{t("Phan's đã có uy tín rất tốt với khách quốc tế. Một khách du lịch hay công tác thường chỉ ở Sài Gòn vài ngày, nên họ cần thấy rõ ngay trên website:", "Phan's already has an excellent reputation with international customers. A visitor is usually in Saigon for only a few days, so the website has to answer their questions up front:")}</p>
      {pts([t("<b>Giá bao nhiêu</b> cho vest, sơ mi, quần tây", "<b>How much</b> a suit, shirt or trousers cost"),
            t("<b>Mất bao lâu</b> và cần đến tiệm mấy lần", "<b>How long</b> it takes and how many visits"),
            t("<b>Có những loại vải nào</b>", "<b>Which fabrics</b> are available"),
            t("<b>Đặt lịch thế nào</b> khi còn ở nước ngoài", "<b>How to book</b> while still abroad"),
            t("<b>Có đáng tin không</b>: đánh giá thật từ khách trước", "<b>Can they trust it</b>: real reviews from past customers")])}
    </div>
    <div class="col stats">
      <div class="stat">{t("4,8", "4.8")}<small>{t("điểm Tripadvisor · 975 đánh giá", "on Tripadvisor · 975 reviews")}</small></div>
      <div class="stat">{t("4,9", "4.9")}<small>{t("điểm Google · 1.115 đánh giá", "on Google · 1,115 reviews")}</small></div>
      <div class="stat">5<small>{t("ngày làm việc để hoàn thành một bộ vest", "working days to finish a suit")}</small></div>
      <div class="stat">3<small>{t("ngôn ngữ: Anh, Việt, Trung", "languages: English, Vietnamese, Chinese")}</small></div>
      <div class="span2">{why(t("Mục tiêu", "Goal"), t("Khách tìm đủ thông tin trong vài phút và đặt lịch ngay, thay vì phải nhắn tin hỏi từng câu.", "Visitors find everything in a few minutes and book straight away, instead of messaging to ask one question at a time."))}</div>
    </div>
  </div></section>''')

  # 3 Current site
  add(f'''<section class="slide">{head(t("Website hiện tại", "Current website"), t("Những điểm khách nước ngoài đang gặp khó", "Where overseas visitors get stuck today"))}
  <div class="body split">
    <div class="text">
      {pts([t("<b>Chọn tiếng Trung nhưng trang vẫn hiện tiếng Anh</b>, xen chữ tiếng Việt như “Chưa có sản phẩm nào…”, “Mua ngay”.", "<b>Choosing Chinese still shows English</b>, mixed with Vietnamese system text such as “Chưa có sản phẩm nào…” and “Mua ngay”."),
            t("<b>Giá và thời gian may</b> chỉ có trong trang FAQ.", "<b>Prices and turnaround</b> are only in the FAQ."),
            t("<b>Mục Suit, Pants, Dress Shirt chưa có sản phẩm</b>; cả shop chỉ có một sản phẩm.", "<b>The Suit, Pants and Dress Shirt tabs are empty</b>; the shop has one product."),
            t("<b>Mục Testimonials chưa có đánh giá</b>, dù Phan's có hơn 2.000 đánh giá tốt.", "<b>The Testimonials section is empty</b>, despite 2,000+ great reviews online."),
            t("<b>Bài viết gộp ba thứ tiếng</b> trong cùng một trang.", "<b>Blog posts mix three languages</b> on one page.")], red=True)}
      {why(t("Nguyên nhân", "Cause"), t("Giao diện mẫu bán hàng của Haravan làm cho shop bán lẻ, chưa hợp với may đo theo lịch hẹn.", "The Haravan shop template is built for retail, not for made-to-measure by appointment."))}
    </div>
    <div class="stack">
      <div class="media half"><img src="img/old_zh_desktop.jpg" style="object-position:center top" alt=""></div>
      <div class="media half"><img src="img/old_zh_products.jpg" style="object-position:center 6%" alt=""></div>
    </div>
  </div></section>''')

  # 4 Home
  add(f'''<section class="slide">{head(t("Trang chủ", "Home page"), t("Ấn tượng đầu tiên: ảnh thật của Phan's, đi thẳng vào điều khách cần", "First impression: Phan's own photography, straight to what visitors need"))}
  <div class="body split">
    <div class="text">
      {pts([t("<b>Ảnh chiến dịch thật của Phan's</b>, toàn màn hình như Suitsupply, Brioni.", "<b>Phan's own campaign photo</b>, full screen like Suitsupply or Brioni."),
            t("<b>Sáu lối vào chính</b>: Vest, Sơ mi, Quần tây, May đo cho nữ, Vải, Đặt lịch thử đồ.", "<b>Six direct entry points</b>: Suits, Shirts, Trousers, Women's tailoring, Fabrics, Book a fitting."),
            t("<b>Rê chuột vào từng mục</b>, ảnh nền chuyển sang hình tương ứng như vải chuyển động.", "<b>Hovering a link</b> folds the photo into that section's image, like moving cloth."),
            t("<b>Nút “Đặt lịch hẹn”</b> luôn ở góc trên bên phải.", "<b>“Book an appointment”</b> always sits top right.")])}
      {why(WHY, t("Khách quyết định ở lại hay rời trang trong vài giây; đưa họ thẳng tới giá, vải và lịch hẹn.", "Visitors decide in seconds whether to stay, so we take them straight to prices, fabrics and booking."))}
    </div>
    {media('cap/hero.jpg')}
  </div></section>''')

  # 5 Language: where
  add(f'''<section class="slide">{head(t("Chuyển ngôn ngữ", "Switching language"), t("Khách đổi ngôn ngữ ở ba vị trí, trên máy tính và điện thoại", "Three places to switch language, on desktop and mobile"))}
  <div class="body langgrid">
    <figure class="lg-a"><div class="media fill"><img src="cap/a_menu.jpg" style="object-fit:cover;object-position:center bottom" alt=""></div><figcaption><span class="badge">2</span>{t("Trong menu toàn màn hình, phía dưới cùng.", "Inside the full-screen menu, at the bottom.")}</figcaption></figure>
    <figure class="lg-b"><div class="media fill"><img src="cap/a_lang.jpg" style="object-fit:cover;object-position:right top" alt=""></div><figcaption><span class="badge">1</span>{t("Góc trên bên phải mọi trang: bấm <b>EN</b> để chọn English, Tiếng Việt hoặc 中文.", "Top right of every page: tap <b>EN</b> to choose English, Tiếng Việt or 中文.")}</figcaption></figure>
    <figure class="lg-c"><div class="media fill dark"><img src="cap/a_footer_c.jpg" style="object-fit:cover;object-position:right bottom" alt=""></div><figcaption><span class="badge">3</span>{t("Cuối mỗi trang (footer).", "At the bottom of every page (footer).")}</figcaption></figure>
  </div>
  <p class="note">{t("Khi đổi ngôn ngữ, khách vẫn ở đúng trang đang xem: đang ở Bảng giá thì chuyển sang Bảng giá tiếng Trung.", "Switching keeps visitors on the same page: from the English price list straight to the Chinese price list.")}</p></section>''')

  # 6 Why multilingual
  add(f'''<section class="slide">{head(t("Vì sao cần ba ngôn ngữ", "Why three languages"), t("Mỗi nhóm khách đọc trọn vẹn bằng ngôn ngữ của mình", "Every customer reads the whole site in their own language"))}
  <div class="body split">
    <div class="text">
      <table class="mini">
        <tr><td>English</td><td>{t("Ngôn ngữ chính: phần lớn khách là người nước ngoài.", "Main language: most customers are from overseas.")}</td></tr>
        <tr><td>中文</td><td>{t("Khách Trung Quốc, Đài Loan, Hồng Kông, Singapore, Malaysia.", "Visitors from China, Taiwan, Hong Kong, Singapore, Malaysia.")}</td></tr>
        <tr><td>Tiếng Việt</td><td>{t("Khách trong nước và Việt kiều.", "Local customers and overseas Vietnamese.")}</td></tr>
      </table>
      {pts([t("<b>Dịch đầy đủ, không trộn lẫn</b>: menu, nút, giá, FAQ, biểu mẫu, bài viết.", "<b>Fully translated, never mixed</b>: menus, buttons, prices, FAQ, forms, articles."),
            t("<b>Đường dẫn riêng cho từng ngôn ngữ</b> (/vi/, /zh/) để Google hiển thị đúng ngôn ngữ khi khách tìm “may đo vest TP.HCM” hay “胡志明市 定制西装”.", "<b>Separate web address per language</b> (/vi/, /zh/), so Google shows the right version for searches like “custom suit Saigon” or “胡志明市 定制西装”.")])}
    </div>
    <div class="trio">
      <figure><div class="media fill"><img src="cap/pricing_en.jpg" style="object-position:left top" alt=""></div><figcaption>English</figcaption></figure>
      <figure><div class="media fill"><img src="cap/pricing_vi.jpg" style="object-position:left top" alt=""></div><figcaption>Tiếng Việt</figcaption></figure>
      <figure><div class="media fill"><img src="cap/pricing_zh.jpg" style="object-position:left top" alt=""></div><figcaption>中文</figcaption></figure>
    </div>
  </div></section>''')

  # 7 Menu
  add(f'''<section class="slide">{head("Menu", t("Menu toàn màn hình, rõ ràng và dễ bấm trên điện thoại", "A full-screen menu that is clear and easy to tap on a phone"))}
  <div class="body split">
    <div class="text">
      {pts([t("<b>Chín mục đánh số</b> theo đúng câu hỏi khách hay hỏi: quy trình, giá, vải, cửa hàng, liên hệ…", "<b>Nine numbered items</b> that follow the questions customers ask: process, prices, fabrics, shop, contact…"),
            t("<b>Rê chuột vào mục nào</b>, mục đó đổi màu, hiện logo “P” và ảnh minh hoạ.", "<b>Hovering an item</b> highlights it, shows the “P” monogram and a preview photo."),
            t("<b>Phía dưới</b>: mạng xã hội, đổi ngôn ngữ, nút đặt lịch.", "<b>At the bottom</b>: social links, language switch and booking.")])}
      {why(WHY, t("Menu cũ có các mục như “Men Measureguide”, “Search” khiến khách khó biết bắt đầu từ đâu.", "The old menu had items like “Men Measureguide” and “Search”, so visitors didn't know where to start."))}
    </div>
    {media('cap/menu.jpg', 'left top')}
  </div></section>''')

  # 8 Pricing
  add(f'''<section class="slide">{head(t("Vest và bảng giá", "Suits & pricing"), t("Bảng giá rõ ràng, trình bày như bảng giá của một tiệm may", "Clear prices, laid out like a tailor's price list"))}
  <div class="body split">
    <div class="text">
      {pts([t("<b>Giá khởi điểm</b>: Suit 2 mảnh từ 6.800.000 ₫, Suit 3 mảnh từ 8.400.000 ₫, Quần tây từ 2.200.000 ₫, Sơ mi từ 1.300.000 ₫.", "<b>Starting prices</b>: 2-piece suit from 6,800,000 VND, 3-piece from 8,400,000, trousers from 2,200,000, shirts from 1,300,000."),
            t("<b>Ghi rõ giá đã bao gồm gì</b>: tư vấn riêng, hơn 20 số đo, thử đồ, giặt hấp, sửa miễn phí trọn đời.", "<b>What every price includes</b>: private consultation, 20+ measurements, fittings, pressing, free lifetime alterations."),
            t("<b>Nút đặt lịch và WhatsApp</b> ngay dưới bảng giá.", "<b>Booking and WhatsApp buttons</b> right below the list.")])}
      {why(WHY, t("Khách nước ngoài luôn so sánh giá trước khi đi. Không thấy giá, họ thường nghĩ là đắt và chọn tiệm khác.", "Overseas visitors compare prices before they travel. With no price shown, they assume it's expensive and go elsewhere."))}
    </div>
    {media('cap/pricelist.jpg', 'left top')}
  </div></section>''')

  # 9 Process
  add(f'''<section class="slide">{head(t("Quy trình may đo", "The bespoke process"), t("Năm bước may một bộ vest, và cách sắp xếp trong chuyến đi ngắn", "Five steps to a suit, planned around a short trip"))}
  <div class="body split">
    <div class="text">
      {pts([t("<b>Năm bước</b>: đặt lịch, tư vấn và lấy số đo, thử đồ, hoàn thiện, chỉnh sửa trọn đời.", "<b>Five steps</b>: book, consultation and measuring, fitting, finishing, lifetime alterations."),
            t("<b>“Lên kế hoạch cho chuyến đi”</b>: lần 1 tư vấn, lần 2 thử đồ, lần 3 nhận đồ, trong 5 ngày làm việc.", "<b>“Planning around your trip”</b>: visit 1 consultation, visit 2 fitting, visit 3 collection, within 5 working days.")])}
      {why(WHY, t("Khách biết trước cần dành mấy ngày ở Sài Gòn, nên chủ động đặt lịch sớm hơn.", "Visitors know how many days to set aside in Saigon, so they book earlier."))}
    </div>
    <div class="stack">
      <div class="media half"><img src="cap/home_process.jpg" style="object-position:left 10%" alt=""></div>
      <div class="media half"><img src="cap/trip.jpg" style="object-position:left 8%" alt=""></div>
    </div>
  </div></section>''')

  # 10 Fabrics & reviews
  add(f'''<section class="slide">{head(t("Vải và đánh giá", "Fabrics and reviews"), t("Cho khách thấy chất liệu và lời khen thật từ khách trước", "Show the cloth, and what real customers say"))}
  <div class="body pair">
    <figure><div class="media fill"><img src="cap/mills.jpg" style="object-position:left top" alt=""></div><figcaption><b>{t("Trang Vải", "Fabrics page")}</b>: {t("Vitale Barberis Canonico (Ý), Holland &amp; Sherry (Anh), dòng Nobility của Phan's, và gợi ý vải cho khí hậu nóng.", "Vitale Barberis Canonico (Italy), Holland &amp; Sherry (England), Phan's own Nobility range, and cloth for hot weather.")}</figcaption></figure>
    <figure><div class="media fill"><img src="cap/reviews.jpg" style="object-position:left top" alt=""></div><figcaption><b>{t("Đánh giá", "Reviews")}</b>: {t("trích nguyên văn từ Tripadvisor (4,8 điểm, 975 đánh giá), có đường dẫn tới trang gốc.", "quoted word for word from Tripadvisor (4.8, 975 reviews), with a link to the original.")}</figcaption></figure>
  </div></section>''')

  # 11 Shop
  add(f'''<section class="slide">{head(t("Cửa hàng trực tuyến", "Online shop"), t("Bán vải Nobility và đồ may sẵn, quản lý bằng WooCommerce", "Sell Nobility cloth and ready-made pieces, managed in WooCommerce"))}
  <div class="body pair">
    <figure><div class="media fill"><img src="cap/shop.jpg" style="object-position:left top" alt=""></div><figcaption>{t("Lọc theo loại, màu, giá.", "Filter by category, colour and price.")}</figcaption></figure>
    <figure><div class="media fill"><img src="cap/pdp.jpg" style="object-position:center top" alt=""></div><figcaption>{t("Mỗi sản phẩm có trang riêng, nút mua và hỏi qua WhatsApp. Ngoài áo blazer Cavani, các sản phẩm khác là mẫu minh hoạ.", "Each product has its own page with buy and WhatsApp buttons. Apart from the Cavani blazer, products are placeholders.")}</figcaption></figure>
  </div></section>''')

  # 12 Contact
  add(f'''<section class="slide">{head(t("Liên hệ và đặt lịch", "Contact and booking"), t("Mọi kênh liên hệ ở một nơi, kể cả khi khách đang ở nước ngoài", "Every way to get in touch, in one place, even from abroad"))}
  <div class="body split">
    <div class="text">
      {pts([t("<b>Đặt lịch</b> qua lịch hẹn Koalendar anh chị đang dùng.", "<b>Booking</b> through the Koalendar calendar Phan's already uses."),
            t("<b>WhatsApp, Zalo, Messenger</b>; tin nhắn WhatsApp soạn sẵn theo ngôn ngữ của khách.", "<b>WhatsApp, Zalo, Messenger</b>; WhatsApp messages are pre-written in the visitor's language."),
            t("<b>Biểu mẫu yêu cầu</b> kèm ngày khách ở Sài Gòn để sắp lịch thử đồ.", "<b>Enquiry form</b> that asks for travel dates, to plan fittings."),
            t("<b>Bản đồ, giờ mở cửa, bãi đỗ xe</b> và lưu ý nghỉ Tết.", "<b>Map, opening hours, parking</b> and a Tết closure note.")])}
    </div>
    <div class="stack">
      <div class="media half"><img src="cap/contact.jpg" style="object-position:left 6%" alt=""></div>
      <div class="media half"><img src="cap/visit.jpg" style="object-position:left 10%" alt=""></div>
    </div>
  </div></section>''')

  # 13 Mobile
  add(f'''<section class="slide">{head(t("Trên điện thoại", "On mobile"), t("Thiết kế cho điện thoại, nơi nhiều khách tìm tiệm may khi đang du lịch", "Designed for phones, where many travellers look for a tailor"))}
  <div class="body split">
    <div class="text">
      {pts([t("<b>Thanh dưới cùng</b> luôn có hai nút: Đặt lịch và WhatsApp.", "<b>A bottom bar</b> always shows two buttons: Book and WhatsApp."),
            t("<b>Đổi ngôn ngữ</b> ở góc trên (1) hoặc trong menu (2).", "<b>Switch language</b> at the top (1) or in the menu (2)."),
            t("<b>Bố cục gọn</b>: chữ, nút và biểu mẫu đủ lớn để bấm dễ.", "<b>Compact layout</b>: text, buttons and forms are large enough to tap easily."),
            t("<b>Tải nhanh</b> trên mạng 4G.", "<b>Loads quickly</b> on 4G.")])}
    </div>
    <div class="phones">
      <div class="phone"><img src="cap/a_m_home.jpg" alt=""></div>
      <div class="phone"><img src="cap/a_m_menu.jpg" alt=""></div>
      <div class="phone"><img src="cap/m_zh_pricing.jpg" alt=""></div>
    </div>
  </div></section>''')

  # 14 Features built in
  def tiles(items):
    return '<div class="tiles">' + ''.join(f'<div class="tile"><div class="ic">{icon(k)}</div><div><h3>{h}</h3><p>{p}</p></div></div>' for k, h, p in items) + '</div>'
  add(f'''<section class="slide">{head(t("Tính năng đã có trong bản mẫu", "Features already in the mock-up"), t("Tiện lợi cho khách, và nhẹ việc cho Phan's", "More convenient for customers, less work for Phan's"))}
  <div class="body cols2">
    <div><p class="colhd">{t("Cho khách", "For customers")}</p>{tiles([
      ('cal', t("Đặt lịch online 24/7", "Book online, 24/7"), t("Chọn giờ trống trên lịch, không cần chờ trả lời tin nhắn.", "Pick a free slot on the calendar without waiting for a reply.")),
      ('chat', t("WhatsApp, Zalo, Messenger một chạm", "One-tap WhatsApp, Zalo, Messenger"), t("Tin nhắn soạn sẵn bằng ngôn ngữ của khách.", "Pre-written messages in the visitor's language.")),
      ('tag', t("Giá và quy trình rõ ràng", "Clear prices and process"), t("Biết trước chi phí và số ngày cần ở Sài Gòn.", "Know the cost and how many days to stay before flying.")),
      ('globe', t("Ba ngôn ngữ", "Three languages"), t("Đổi một chạm, vẫn giữ nguyên trang đang xem.", "Switch in one tap and stay on the same page."))])}</div>
    <div><p class="colhd">{t("Cho Phan's", "For Phan's")}</p>{tiles([
      ('form', t("Biểu mẫu thông minh", "Smart enquiry form"), t("Nhận yêu cầu qua email, kèm ngày khách ở Sài Gòn và đồ muốn may.", "Enquiries arrive by email with travel dates and garments wanted.")),
      ('cart', t("Tự quản lý cửa hàng", "Manage the shop yourselves"), t("Đăng sản phẩm, giá, hình qua WooCommerce, không cần biết lập trình.", "Add products, prices and photos in WooCommerce, no coding needed.")),
      ('search', t("Dễ tìm thấy trên Google", "Easier to find on Google"), t("Mỗi trang, mỗi ngôn ngữ có tiêu đề và mô tả riêng cho tìm kiếm.", "Every page and language has its own search title and description.")),
      ('chart', t("Đo lường khách truy cập", "Visitor tracking ready"), t("Sẵn sàng kết nối Google Analytics: biết khách bấm đặt lịch hay WhatsApp nhiều hơn.", "Ready for Google Analytics: see whether visitors book or WhatsApp more."))])}</div>
  </div></section>''')

  # 15 Add-ons
  add(f'''<section class="slide">{head(t("Có thể tích hợp thêm", "Optional add-ons"), t("Những tính năng có thể thêm vào khi website chính thức chạy", "Features we can add once the website goes live"))}
  <div class="body cols2">
    <div>{tiles([
      ('card', t("Thanh toán và đặt cọc online", "Online payments and deposits"), t("VNPay, MoMo, thẻ Visa/Mastercard: mua vải, đồ may sẵn, hoặc đặt cọc trước khi bay sang.", "VNPay, MoMo, Visa/Mastercard: buy cloth or ready-made pieces, or pay a deposit before flying in.")),
      ('ruler', t("Hồ sơ số đo khách hàng", "Customer measurement profiles"), t("Khách cũ đặt may lại từ nước ngoài dựa trên số đo đã lưu.", "Returning customers reorder from abroad using their saved measurements.")),
      ('bell', t("Nhắc lịch tự động", "Automatic reminders"), t("Email hoặc WhatsApp nhắc ngày thử đồ, ngày nhận đồ.", "Email or WhatsApp reminders for fittings and collection.")),
      ('steps', t("Theo dõi tiến độ đơn may", "Order progress tracking"), t("Khách xem đơn đang ở bước nào: cắt, thử đồ, hoàn thiện.", "Customers see where their order is: cutting, fitting, finishing."))])}</div>
    <div>{tiles([
      ('star', t("Đánh giá tự cập nhật", "Live review feed"), t("Hiển thị đánh giá mới nhất từ Google và Tripadvisor.", "Show the latest Google and Tripadvisor reviews automatically.")),
      ('bot', t("Trợ lý chat đa ngôn ngữ", "Multilingual chat assistant"), t("Trả lời câu hỏi thường gặp 24/7, chuyển sang nhân viên khi cần.", "Answers common questions 24/7 and hands over to staff when needed.")),
      ('gift', t("Thẻ quà tặng online", "Online gift vouchers"), t("Khách mua voucher may đo để tặng người thân.", "Customers buy a tailoring voucher as a gift.")),
      ('group', t("Đặt may theo nhóm", "Group orders"), t("Cho đám cưới, công ty: một biểu mẫu cho nhiều người.", "Weddings and companies: one form for the whole group."))])}</div>
  </div>
  <p class="note">{t("Đây là các lựa chọn mở rộng; chi phí và thời gian sẽ trao đổi cụ thể khi anh chị quan tâm.", "These are optional; we'll agree cost and timing for any you're interested in.")}</p></section>''')

  # 16 Next steps
  add(f'''<section class="slide">{head(t("Bước tiếp theo", "Next steps"), t("Để hoàn thiện website, chúng tôi cần anh chị xác nhận", "To finish the website, we need Phan's to confirm"))}
  <div class="body two">
    <div class="col">{pts([t("<b>Giá</b> cho blazer, gilê, măng tô và đồ nữ; có thêm giá USD không.", "<b>Prices</b> for blazers, waistcoats, overcoats and women's garments; whether to show USD."),
            t("<b>Hình ảnh thật</b> của tiệm, anh chị và sản phẩm.", "<b>Real photos</b> of the villa, the founders and finished work."),
            t("<b>Sản phẩm</b> vải Nobility và đồ may sẵn muốn bán online.", "<b>Products</b>: the Nobility cloth and ready-made pieces to sell online."),
            t("<b>Nội dung tiếng Việt, tiếng Trung</b>: chúng tôi đã dịch, anh chị đọc lại giúp.", "<b>Vietnamese and Chinese copy</b>: we've translated it; please review."),
            t("<b>Lịch nghỉ Tết</b> và các ngày lễ.", "<b>Tết and public holiday</b> closing dates.")])}</div>
    <div class="col">
      <p class="lead">{t("Mời anh chị trải nghiệm trực tiếp bản mẫu, nên mở trên điện thoại:", "Please try the mock-up yourselves, ideally on a phone:")}</p>
      <p class="biglink"><a href="{LINK}">phans-custom-tailor-demo.vercel.app</a></p>
      {why(t("Lưu ý", "Note"), t("Đây là bản mẫu để anh chị hình dung. Sản phẩm mẫu, ảnh minh hoạ và bản dịch sẽ hoàn thiện cùng anh chị trước khi chạy chính thức trên tailormadesuit.net.", "This is a preview. Sample products, placeholder photos and translations will be finalised with Phan's before it goes live on tailormadesuit.net."))}
      <p class="sig">Yong · TheWebxite</p>
    </div>
  </div></section>''')

  n = len(slides)
  footer = t("Phan's Custom Tailor · Đề xuất website mới", "Phan's Custom Tailor · Website proposal")
  body = ''.join(s.replace('</section>', f'<div class="foot"><span>{footer}</span><span>{i + 1} / {n}</span></div></section>') if i else s for i, s in enumerate(slides))
  return f'''<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{t("Đề xuất website mới cho Phan's Custom Tailor", "Website proposal for Phan's Custom Tailor")}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600&family=Prata&display=swap">
<link rel="stylesheet" href="deck.css"></head><body>{body}</body></html>'''

CSS = r'''
@page { size: 1280px 720px; margin: 0; }
:root { --ink:#141414; --paper:#f7f6f3; --stone:#d8d5cf; --mute:#5f5f5f; --navy:#1e2a3a; --red:#e0362b; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Be Vietnam Pro", system-ui, sans-serif; color: var(--ink); font-size: 14.5px; line-height: 1.5; -webkit-print-color-adjust: exact; print-color-adjust: exact; background:#777; }
.slide { width: 1280px; height: 720px; background: var(--paper); position: relative; overflow: hidden; break-after: page; padding: 46px 64px 0; }
.slide:last-child { break-after: auto; }
/* fixed header band so every slide body starts at the same line */
.hd { height: 128px; }
.kicker { font-size: 11px; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: var(--mute); margin-bottom: 10px; }
h2 { font-family: "Prata", Georgia, serif; font-weight: 400; font-size: 30px; line-height: 1.2; max-width: 1050px; }
.body { position: absolute; left: 64px; right: 64px; top: 182px; bottom: 58px; }
.foot { position: absolute; left: 64px; right: 64px; bottom: 20px; display: flex; justify-content: space-between; font-size: 10.5px; color: var(--mute); border-top: 1px solid var(--stone); padding-top: 9px; }
.note { position: absolute; left: 64px; right: 64px; bottom: 50px; font-size: 12.5px; color: var(--mute); }
/* layouts: text 440 | gap 44 | media 668 */
.split { display: grid; grid-template-columns: 440px 1fr; gap: 44px; }
.split > .text { justify-content: center; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 56px; align-items: start; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
.cols2 { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
.text, .col { display: flex; flex-direction: column; gap: 18px; }
.stack { display: grid; grid-template-rows: 1fr 1fr; gap: 14px; min-height: 0; }
.media { background: #fff; border: 1px solid var(--stone); box-shadow: 0 14px 34px rgba(20,20,20,.09); overflow: hidden; height: 100%; min-height: 0; }
.media img { display: block; width: 100%; height: 100%; object-fit: cover; }
.media.dark { background: #141414; }
figure { display: flex; flex-direction: column; min-height: 0; gap: 8px; }
figure .media { flex: 1; }
figcaption { font-size: 12px; color: var(--mute); line-height: 1.45; }
.lead { font-size: 15.5px; color: #2b2b2b; }
ul.pts { list-style: none; counter-reset: pt; display: grid; gap: 11px; }
ul.pts li { position: relative; padding-left: 30px; font-size: 14px; }
ul.pts li b { font-weight: 600; }
ul.pts li::before { counter-increment: pt; content: counter(pt); position: absolute; left: 0; top: 1px; width: 20px; height: 20px; border-radius: 50%; background: var(--navy); color: #fff; font-size: 10.5px; font-weight: 600; display: grid; place-items: center; }
ul.pts.red li::before { background: var(--red); }
.why { border-left: 3px solid var(--navy); padding: 3px 0 3px 15px; font-size: 13.5px; color: #2b2b2b; }
.why b { display: block; font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--navy); margin-bottom: 3px; }
.badge { display: inline-grid; place-items: center; width: 20px; height: 20px; border-radius: 50%; background: var(--red); color: #fff; font-size: 11px; font-weight: 600; margin-right: 8px; vertical-align: -5px; }
.stats { display: grid; grid-template-columns: 1fr 1fr; gap: 26px 30px; align-content: start; padding-top: 6px; }
.stat { font-family: "Prata", serif; font-size: 44px; line-height: 1; }
.stat small { display: block; font-family: "Be Vietnam Pro"; font-size: 12.5px; color: var(--mute); margin-top: 8px; line-height: 1.4; }
.span2 { grid-column: 1 / -1; }
table.mini { border-collapse: collapse; width: 100%; font-size: 13.5px; }
table.mini td { padding: 8px 0; border-bottom: 1px solid var(--stone); vertical-align: top; }
table.mini td:first-child { width: 96px; font-weight: 600; }
.trio { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; min-height: 0; }
/* language slide: menu left (large), dropdown + footer right */
.langgrid { display: grid; grid-template-columns: 7fr 5fr; grid-template-rows: 1fr 1fr; gap: 16px 24px; bottom: 82px; }
.lg-a { grid-row: 1 / 3; }
.phones { display: flex; justify-content: flex-end; gap: 22px; align-items: flex-start; }
.phone { width: 212px; border-radius: 26px; border: 7px solid #141414; overflow: hidden; background: #141414; box-shadow: 0 14px 34px rgba(20,20,20,.16); }
.phone img { display: block; width: 100%; }
.colhd { font-size: 11px; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: var(--navy); margin-bottom: 10px; }
.tiles { display: grid; gap: 12px; grid-auto-rows: 1fr; height: calc(100% - 26px); }
.cols2 > div:not(:has(.colhd)) .tiles { height: calc(100% - 30px); }
.tile { display: grid; grid-template-columns: 44px 1fr; gap: 16px; align-items: center; background: #fff; border: 1px solid var(--stone); padding: 13px 16px; }
.tile .ic { width: 44px; height: 44px; border-radius: 50%; background: var(--navy); color: #fff; display: grid; place-items: center; }
.tile .ic svg { width: 20px; height: 20px; }
.tile h3 { font-size: 15.5px; font-weight: 600; margin-bottom: 2px; }
.tile p { font-size: 13px; color: var(--mute); line-height: 1.4; }
.biglink { font-family: "Prata", serif; font-size: 25px; }
.biglink a, a { color: var(--navy); }
.sig { font-size: 13px; color: var(--mute); }
/* cover */
.cover { padding: 0; display: flex; background: var(--ink); color: #fff; }
.cover .left { width: 46%; padding: 60px 56px 48px 64px; display: flex; flex-direction: column; justify-content: space-between; }
.cover .right { width: 54%; position: relative; }
.cover .right img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 38% 30%; }
.cover h1 { font-family: "Prata", serif; font-weight: 400; font-size: 42px; line-height: 1.14; margin: 26px 0 18px; }
.cover p { color: rgba(255,255,255,.85); font-size: 15.5px; max-width: 430px; }
.logo { width: 160px; }
.links { font-size: 13px; color: rgba(255,255,255,.85); display: grid; gap: 6px; }
.links a { color: #fff; }
.links .date { margin-top: 10px; color: rgba(255,255,255,.55); }
'''

if __name__ == '__main__':
  open('deck.css', 'w').write(CSS)
  outs = {'vi': 'De-xuat-website-Phans-VI', 'en': 'Website-proposal-Phans-EN'}
  with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 720})
    for L, name in outs.items():
      open(f'{name}.html', 'w').write(deck(L))
      pg.goto('file://' + os.path.abspath(f'{name}.html'), wait_until='load', timeout=90000); pg.wait_for_timeout(1500)
      pg.emulate_media(media='print')
      os.makedirs(f'check/{L}', exist_ok=True)
      for i, el in enumerate(pg.locator('.slide').all()): el.screenshot(path=f'check/{L}/s{i + 1:02d}.png')
      # overflow audit: any text or media spilling outside its slide body
      issues = pg.evaluate('''() => [...document.querySelectorAll('.slide')].flatMap((s, i) => {
        const sr = s.getBoundingClientRect(); const out = [];
        s.querySelectorAll('h2, .body, .note, .foot, li, p, figure, .tile, .phone').forEach(e => {
          const r = e.getBoundingClientRect(); if (r.bottom > sr.bottom - 2 || r.right > sr.right + 1) out.push(`slide ${i+1}: ${e.tagName}.${e.className} bottom ${Math.round(r.bottom - sr.top)}`);
        });
        const body = s.querySelector('.body'), foot = s.querySelector('.foot');
        if (body) { const bb = body.getBoundingClientRect();
          [...body.querySelectorAll('*')].forEach(e => { const r = e.getBoundingClientRect(); if (r.height && r.bottom > bb.bottom + 1) out.push(`slide ${i+1}: overflow ${e.tagName}.${e.className} by ${Math.round(r.bottom - bb.bottom)}px`); }); }
        const h = s.querySelector('h2'); if (h && h.getBoundingClientRect().height > 80) out.push(`slide ${i+1}: title wraps to 3 lines`);
        return out; })''')
      print(L, 'issues:', issues[:12] or 'none')
      pg.pdf(path=f'{name}.pdf', width='1280px', height='720px', print_background=True, prefer_css_page_size=True)
    b.close()
  print('done')
