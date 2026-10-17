"""Kimlien's call briefing as an A4 PDF, Vietnamese + English from one source.
Run: /Users/hengzhexin/anaconda3/bin/python3 pitch/build_briefing.py
Writes pitch/Briefing-cuoc-goi-Kimlien-VI.pdf and pitch/Call-briefing-Kimlien-EN.pdf."""
import os, html
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
DEMO = 'https://phans-custom-tailor-demo.vercel.app/'

def build(L):
  t = lambda vi, en: vi if L == 'vi' else en
  e = html.escape

  def section(n, title, body): return f'<section><h2><span class="n">{n}</span>{title}</h2>{body}</section>'
  def ul(items, cls=''): return f'<ul class="{cls}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
  def ol(items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'
  def table(rows, heads, cls=''):
    return f'<table class="{cls}"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in heads) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table>'

  # ---------- diagram: domain -> DNS -> hosting, email separate ----------
  dia = f'''<svg class="dia" viewBox="0 0 680 190" xmlns="http://www.w3.org/2000/svg" font-family="Be Vietnam Pro, sans-serif">
  <defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#1e2a3a"/></marker></defs>
  <rect x="6" y="20" width="170" height="78" rx="8" fill="#fff" stroke="#1e2a3a" stroke-width="1.5"/>
  <text x="91" y="48" text-anchor="middle" font-size="14" font-weight="600" fill="#141414">{t("Tên miền", "Domain")}</text>
  <text x="91" y="68" text-anchor="middle" font-size="11.5" fill="#5f5f5f">phanscustomtailor.com</text>
  <text x="91" y="86" text-anchor="middle" font-size="11" fill="#5f5f5f">{t("= địa chỉ nhà", "= street address")}</text>
  <line x1="178" y1="59" x2="250" y2="59" stroke="#1e2a3a" stroke-width="1.5" marker-end="url(#ar)"/>
  <rect x="254" y="20" width="170" height="78" rx="8" fill="#fff" stroke="#1e2a3a" stroke-width="1.5"/>
  <text x="339" y="48" text-anchor="middle" font-size="14" font-weight="600" fill="#141414">{t("Trỏ tên miền (DNS)", "Pointing (DNS)")}</text>
  <text x="339" y="68" text-anchor="middle" font-size="11" fill="#5f5f5f">{t("= chỉ đường đến nhà", "= directions to the house")}</text>
  <text x="339" y="86" text-anchor="middle" font-size="11" fill="#5f5f5f">{t("TWX cài đặt", "set up by TWX")}</text>
  <line x1="426" y1="59" x2="498" y2="59" stroke="#1e2a3a" stroke-width="1.5" marker-end="url(#ar)"/>
  <rect x="502" y="20" width="170" height="78" rx="8" fill="#1e2a3a"/>
  <text x="587" y="48" text-anchor="middle" font-size="14" font-weight="600" fill="#fff">Hosting</text>
  <text x="587" y="68" text-anchor="middle" font-size="11" fill="#d8d5cf">{t("= ngôi nhà chứa website", "= where the site lives")}</text>
  <text x="587" y="86" text-anchor="middle" font-size="11" fill="#d8d5cf">{t("TWX quản lý, mở 24/7", "managed by TWX, open 24/7")}</text>
  <rect x="254" y="122" width="418" height="56" rx="8" fill="#f7f6f3" stroke="#d8d5cf" stroke-dasharray="4 4"/>
  <text x="463" y="146" text-anchor="middle" font-size="12.5" font-weight="600" fill="#141414">{t("Email info@phantailor.com: tách riêng, không thay đổi", "Email info@phantailor.com: separate, not changed")}</text>
  <text x="463" y="165" text-anchor="middle" font-size="11" fill="#5f5f5f">{t("(Google Workspace, tên miền phantailor.com)", "(Google Workspace on phantailor.com)")}</text>
  <text x="6" y="146" font-size="11" fill="#5f5f5f">{t("Website cũ (Haravan) chạy đến", "Old site (Haravan) runs until")}</text>
  <text x="6" y="163" font-size="11" fill="#5f5f5f">{t("khi website mới hoạt động.", "the new one is live.")}</text>
</svg>'''

  # ---------- content ----------
  top = f'''<header class="top">
    <p class="kicker">{t("Tài liệu nội bộ · Dành cho Kimlien", "Internal · For Kimlien")}</p>
    <h1>{t("Briefing cuộc gọi với anh Thịnh", "Call briefing: Thinh Phan")}</h1>
    <p class="sub">Phan's Custom Tailor · {t("chuẩn bị bởi Xin, TheWebxite · 17/10/2026", "prepared by Xin, TheWebxite · 17 Oct 2026")}</p>
    <div class="links"><div><b>{t("Bản demo", "Demo")}</b> <a href="{DEMO}">phans-custom-tailor-demo.vercel.app</a></div>
      <div><b>{t("Website hiện tại", "Current site")}</b> <a href="https://tailormadesuit.net/">tailormadesuit.net</a></div></div>
  </header>
  <div class="summary"><h3>{t("Tóm tắt 30 giây", "The 30-second version")}</h3>
  {ul([t("Đề xuất: biến bản demo thành website chính thức, 3 ngôn ngữ, khoảng <b>1 tuần</b> sau khi có đủ thông tin.", "Proposal: turn the demo into the official 3-language site, about <b>1 week</b> after we have all the information."),
       t("Dùng tên miền <b>phanscustomtailor.com</b> (Phan's đã sở hữu), không mua tên miền mới; email không thay đổi.", "Use <b>phanscustomtailor.com</b> (Phan's already owns it), no new domain; email unchanged."),
       t("TWX lo hosting, bảo mật, sao lưu và bảo trì. Đặt lịch giữ <b>Koalendar</b> hiện tại.", "TWX handles hosting, security, backups and maintenance. Booking stays on the current <b>Koalendar</b>."),
       t("Cửa hàng chỉ <b>trưng bày</b> ở giai đoạn 1: khách nhắn WhatsApp/Zalo hoặc đặt lịch, chưa thanh toán online.", "Shop is <b>showcase only</b> in phase 1: customers message on WhatsApp/Zalo or book; no online payment yet."),
       t("<b>Không báo giá</b> trong cuộc gọi; Xin gửi báo giá sau. <b>Không nhắc</b> phòng thử đồ AI.", "<b>No prices</b> on the call; Xin sends the quote afterwards. <b>Don't mention</b> the AI fitting room.")])}</div>'''

  s1 = section(1, t("Anh Thịnh nêu 3 điểm, mình trả lời thế nào", "Thinh raised 3 points: how we answer"), table([
    (t("Đoán bên mình dùng AI (Claude)", "Guessed we used AI (Claude)"), t("Nói thẳng là đúng. AI giúp làm nhanh và chất lượng hơn; thiết kế, kiểm tra và hỗ trợ do người thật làm.", "Confirm it. AI makes us faster and better; design, testing and support are done by real people.")),
    (t("Đang làm với một đội Web 3D khác", "Working with a separate Web 3D team"), t("Bổ sung, không cạnh tranh: website là “ngôi nhà” chính, phần 3D đặt vào một trang hoặc mục bên trong. Bên mình sẵn sàng phối hợp.", "Complementary, not competing: the website is the main home, the 3D work sits on a page or section inside it. We're happy to coordinate.")),
    (t("Hỏi hợp tác theo hướng nào", "Asked what kind of collaboration"), t("Đề xuất giai đoạn 1 ở mục 4: hoàn thiện demo thành website chính thức, TWX lo hosting và bảo trì.", "The phase 1 proposal in section 4: turn the demo into the official site, TWX handles hosting and maintenance.")),
  ], [t("Anh Thịnh nói", "Thinh said"), t("Mình trả lời", "Our answer")], 'qa'))

  s2 = section(2, t("Mục tiêu và trình tự cuộc gọi", "Goals and running order"),
    '<div class="cols"><div>' + f'<h4>{t("Mục tiêu", "Goals")}</h4>' + ol([
      t("Hiểu anh Thịnh muốn gì cho website mới.", "Understand what Thinh wants from the new site."),
      t("Thống nhất phạm vi giai đoạn 1 (mục 4).", "Agree the phase 1 scope (section 4)."),
      t("Lấy các thông tin ở mục 7.", "Collect the information in section 7."),
      t("Hẹn Xin gửi báo giá và lịch trình sau cuộc gọi.", "Say Xin will send a quote and timeline after the call.")]) + '</div><div>' + f'<h4>{t("Gợi ý trình tự (khoảng 30 phút)", "Suggested order (about 30 min)")}</h4>' + ol([
      t("Cảm ơn anh đã xem demo và phản hồi.", "Thank him for looking at the demo and replying."),
      t("Hỏi anh: mục tiêu cho website mới, khách chính là ai, điều anh chưa hài lòng ở website cũ.", "Ask: his goals for the new site, his main customers, what he dislikes about the old site."),
      t("Trình bày đề xuất (mục 4) và cách phối hợp với đội 3D.", "Present the proposal (section 4) and how we'd work with the 3D team."),
      t("Giải thích tên miền và hosting bằng hình ở mục 3.", "Explain domain and hosting with the diagram in section 3."),
      t("Trả lời câu hỏi (mục 5).", "Answer his questions (section 5)."),
      t("Đi qua checklist thông tin (mục 7).", "Go through the information checklist (section 7)."),
      t("Chốt bước tiếp theo: Xin gửi báo giá; anh gửi thông tin.", "Agree next steps: Xin sends the quote; he sends the information.")]) + '</div></div>')

  gl = [
    (t("Tên miền (domain)", "Domain"), t("Địa chỉ website, như địa chỉ nhà, ví dụ phanscustomtailor.com. Mua theo năm, đứng tên chủ doanh nghiệp.", "The website's address, like a street address, e.g. phanscustomtailor.com. Paid yearly, owned by the business.")),
    ("Hosting", t("“Ngôi nhà” chứa website: máy chủ lưu nội dung và hình ảnh để website mở 24/7. Tên miền là địa chỉ, hosting là căn nhà ở địa chỉ đó.", "The “house” the website lives in: the server that stores content and photos so the site is open 24/7. The domain is the address; hosting is the house at that address.")),
    (t("Trỏ tên miền (DNS)", "Pointing the domain (DNS)"), t("Đổi chỉ dẫn để địa chỉ cũ dẫn đến ngôi nhà mới. Bên mình làm, chỉ cần quyền vào tài khoản quản lý tên miền.", "Changing the directions so the address leads to the new house. We do it; we only need access to the domain account.")),
    (t("https (ổ khoá)", "https (padlock)"), t("Website được bảo mật. Có sẵn, miễn phí.", "The site is secure. Included, free.")),
    (t("Chuyển hướng (redirect)", "Redirects"), t("Link cũ trên Google tự dẫn sang trang mới tương ứng, nên Phan's không mất thứ hạng tìm kiếm.", "Old Google links lead to the matching new pages, so Phan's keeps its search ranking.")),
    ("Haravan", t("Nền tảng của website cũ (vừa phần mềm vừa hosting). Giữ đến khi website mới chạy, sau đó mới ngừng.", "The platform behind the old site (software and hosting in one). Keep it until the new site is live, then stop it.")),
    ("Koalendar", t("Công cụ đặt lịch Phan's đang dùng. Website mới chỉ cần gắn link sang đó.", "The booking tool Phan's already uses. The new site just links to it.")),
    (t("Cổng thanh toán", "Payment gateway"), t("Dịch vụ cho khách trả tiền online bằng thẻ, ví. Ở Việt Nam thường dùng OnePay, VNPay. Chỉ cần nếu bán online (giai đoạn 2).", "A service for paying online by card or wallet. In Vietnam usually OnePay or VNPay. Only needed for online sales (phase 2).")),
    (t("Bảo trì", "Maintenance"), t("Sau khi website chạy: theo dõi, cập nhật, sao lưu, sửa lỗi và chỉnh nội dung nhỏ.", "After launch: monitoring, updates, backups, fixes and small content changes.")),
  ]
  s3 = section(3, t("Giải thích bằng lời dễ hiểu", "Plain-language explanations"),
    f'<p class="lead">{t("Dùng hình này khi giải thích cho anh Thịnh:", "Use this picture when explaining to Thinh:")}</p>' + dia +
    table(gl, [t("Khái niệm", "Term"), t("Giải thích", "What it means")], 'gloss'))

  pos = [
    t("<b>Phạm vi giai đoạn 1:</b> website ba ngôn ngữ (Anh là chính, Việt, Trung); bảng giá; quy trình may; thông tin vải; đặt lịch; WhatsApp và Zalo; trang cửa hàng dạng trưng bày; chuyển các bài viết cũ; tối ưu Google.", "<b>Phase 1 scope:</b> three-language site (English main, Vietnamese, Chinese); prices; process; fabrics; booking; WhatsApp and Zalo; showcase shop; old articles moved over; Google optimisation."),
    t("<b>Tên miền:</b> Phan's đã có <b>phanscustomtailor.com</b> (đang dùng trên Google Maps) và tailormadesuit.net. Đề xuất dùng phanscustomtailor.com làm chính vì đúng tên thương hiệu; tailormadesuit.net tự chuyển sang. Không cần mua tên miền mới. Nếu anh muốn giữ tailormadesuit.net làm chính cũng được. Tên miền luôn đứng tên Phan's.", "<b>Domain:</b> Phan's already owns <b>phanscustomtailor.com</b> (on Google Maps) and tailormadesuit.net. Suggest phanscustomtailor.com as main since it matches the brand; tailormadesuit.net forwards to it. No new domain needed. If he prefers tailormadesuit.net as main, that's fine too. The domain always stays in Phan's name."),
    t("<b>Hosting:</b> TWX lo toàn bộ: mua và quản lý hosting, bảo mật, sao lưu, bảo trì. Chi phí hosting và bảo trì sẽ có trong báo giá.", "<b>Hosting:</b> TWX handles everything: buying and managing hosting, security, backups, maintenance. Hosting and maintenance costs will be in the quote."),
    t("<b>Đặt lịch:</b> giữ lịch Koalendar anh đang dùng; nút đặt lịch trên website dẫn sang đó. Không làm hệ thống mới; anh vẫn quản lý lịch như hiện tại.", "<b>Booking:</b> keep his Koalendar calendar; the site's booking buttons link to it. No new system; he manages his calendar as today."),
    t("<b>Cửa hàng:</b> giai đoạn 1 chỉ trưng bày. Khách xem vải và đồ may sẵn, rồi hỏi giá qua WhatsApp/Zalo hoặc đặt lịch đến villa. Không giỏ hàng, không đăng nhập, không thanh toán online.", "<b>Shop:</b> phase 1 is showcase only. Customers browse cloth and ready-made pieces, then ask about price on WhatsApp/Zalo or book a visit. No cart, no login, no online payment."),
    t("<b>Vì sao chưa bán online:</b> cần người xử lý đơn mỗi ngày, đóng gói, giao hàng quốc tế, đổi trả, và đăng ký cổng thanh toán (OnePay, VNPay). Với may đo, khách vẫn phải đến villa lấy số đo, nên trưng bày là đủ. Muốn bán online thì làm ở giai đoạn 2.", "<b>Why not sell online yet:</b> it needs someone handling orders daily, packing, international shipping, returns, and a payment gateway (OnePay, VNPay). For made-to-measure, customers still come to the villa to be measured, so a showcase is enough. Online sales can be phase 2."),
    t("<b>Tài khoản khách và giỏ hàng</b> trên website cũ: không cần nữa ở giai đoạn 1 (website cũ chỉ có 1 sản phẩm).", "<b>Customer accounts and cart</b> on the old site: not needed in phase 1 (the old shop has one product)."),
    t("<b>Thời gian:</b> khoảng 1 tuần sau khi nhận đủ thông tin ở mục 7.", "<b>Timeline:</b> about 1 week after we receive everything in section 7."),
    t("<b>Đội Web 3D:</b> bổ sung, không cạnh tranh. Website là “ngôi nhà” chính; trải nghiệm 3D có thể đặt vào một trang hoặc một mục trong website. Bên mình sẵn sàng phối hợp kỹ thuật.", "<b>Web 3D team:</b> complementary, not competing. The website is the main home; their 3D experience can go on a page or section inside it. We're happy to coordinate."),
  ]
  s4 = section(4, t("Lập trường của bên mình (đã thống nhất với Xin)", "Our position (agreed with Xin)"), ol(pos))

  qa = [
    (t("Chi phí bao nhiêu?", "How much?"), t("“Xin sẽ gửi báo giá chi tiết ngay sau cuộc gọi, tuỳ các phần anh chọn hôm nay.” Không nói con số.", "“Xin will send a detailed quote right after this call, based on what you choose today.” No numbers.")),
    (t("Có phí hàng tháng không?", "Any monthly fee?"), t("“Có phí hosting và bảo trì; Xin sẽ ghi rõ trong báo giá.”", "“Yes, hosting and maintenance; Xin will list it in the quote.”")),
    (t("Bao lâu thì xong?", "How long?"), t("“Khoảng 1 tuần sau khi bên anh gửi đủ hình ảnh và thông tin.”", "“About 1 week after you send all the photos and information.”")),
    (t("Bên anh tự sửa nội dung được không?", "Can we edit content ourselves?"), t("“Anh chỉ cần nhắn nội dung cần đổi, bên em cập nhật trong gói bảo trì. Nếu anh muốn tự sửa, mình bàn thêm.” Không hứa trang quản trị.", "“Just message us what to change and we update it under maintenance. If you'd like to edit it yourselves, we can discuss.” Don't promise an admin panel.")),
    (t("Có ảnh hưởng thứ hạng Google không?", "Will it affect our Google ranking?"), t("“Không, các link cũ sẽ tự chuyển sang trang mới.”", "“No, old links forward to the new pages.”")),
    (t("Email có bị gián đoạn không?", "Will email be interrupted?"), t("“Không, email info@phantailor.com giữ nguyên.”", "“No, info@phantailor.com stays as it is.”")),
    (t("Khi nào tắt Haravan?", "When do we stop Haravan?"), t("“Sau khi website mới chạy ổn định; trước đó Haravan vẫn hoạt động bình thường.”", "“Once the new site runs smoothly; until then Haravan keeps working.”")),
    (t("Tên miền thuộc về ai?", "Who owns the domain?"), t("“Luôn đứng tên Phan's. Bên em chỉ cần quyền để trỏ tên miền.”", "“Always Phan's. We only need access to point it.”")),
    (t("Bán hàng, thanh toán online được không?", "Can customers buy and pay online?"), t("“Được, nhưng bên em đề xuất làm ở giai đoạn 2, vì cần người xử lý đơn và giao hàng quốc tế. Giai đoạn 1 khách xem mẫu rồi nhắn hoặc đặt lịch.”", "“Yes, but we suggest phase 2, since it needs someone handling orders and international shipping. In phase 1 customers browse, then message or book.”")),
    (t("Phòng thử đồ AI trên demo có kèm không?", "Is the AI fitting room on the demo included?"), t("“Đó là tính năng bên em đang thử nghiệm; còn đánh giá chi phí và độ ổn định nên chưa đưa vào đề xuất. Xin sẽ báo sau.” Đừng tự giới thiệu.", "“It's a feature we're testing; we're still assessing cost and reliability, so it isn't in the proposal yet. Xin will follow up.” Don't bring it up yourself.")),
    (t("Còn đội 3D thì sao?", "What about the 3D team?"), t("Xem mục 4, ý 9.", "See section 4, point 9.")),
    (t("Tiếng Trung ai dịch?", "Who translated the Chinese?"), t("“Bên em đã dịch sẵn. Bên anh chỉ cần một người đọc lại phần tiếng Việt.”", "“We did. You just need someone to read through the Vietnamese.”")),
    (t("Câu hỏi kỹ thuật khó", "A hard technical question"), t("“Em ghi lại và nhờ Xin trả lời bằng văn bản ngay sau cuộc gọi.”", "“I'll note it and Xin will answer in writing right after the call.”")),
  ]
  s5 = section(5, t("Câu anh Thịnh có thể hỏi và gợi ý trả lời", "Likely questions and suggested answers"), table(qa, [t("Câu hỏi", "Question"), t("Gợi ý trả lời", "Suggested answer")], 'qa'))

  s6 = section(6, t("Đừng hứa trong cuộc gọi", "Don't promise on the call"), ul([
    t("Giá cụ thể.", "A specific price."),
    t("Bán hàng hay thanh toán online ở giai đoạn 1.", "Online selling or payment in phase 1."),
    t("Phòng thử đồ AI.", "The AI fitting room."),
    t("Ngày ra mắt cố định trước khi có đủ thông tin.", "A fixed launch date before we have all the information."),
    t("Trang quản trị để anh tự chỉnh sửa website.", "A self-edit admin panel."),
    t("Mua tên miền mới (Phan's đã có).", "Buying a new domain (Phan's already has one).")], 'no'))

  ck = [
    t("Ai quản lý tên miền phanscustomtailor.com và tailormadesuit.net, cách cấp quyền cho bên mình (tài khoản đăng nhập), và anh chọn địa chỉ nào làm chính.", "Who manages phanscustomtailor.com and tailormadesuit.net, how to give us access (login account), and which address he wants as main."),
    t("Hình ảnh thật: villa, anh chị, sản phẩm hoàn thiện, vải; file logo gốc.", "Real photos: villa, the founders, finished garments, cloth; original logo file."),
    t("Giá còn thiếu: áo blazer, gilê, măng tô, đồ may cho nữ; hiển thị VND, USD hay đơn vị khác.", "Missing prices: blazer, waistcoat, overcoat, women's garments; show VND, USD or another currency."),
    t("Năm thành lập (website cũ ghi “từ 2013”), lịch nghỉ Tết và lễ, thời gian may chuẩn (5 ngày làm việc?), khách đặt may lại từ nước ngoài có được không.", "Founding year (old site says “since 2013”), Tết and holiday closures, standard turnaround (5 working days?), and whether customers can reorder from abroad."),
    t("Người bên Phan's đọc lại bản tiếng Việt.", "Someone at Phan's to read through the Vietnamese."),
    t("Link Koalendar, trang Facebook chính thức (facebook.com/phanstailor hay /phantailor), quyền Google Business.", "Koalendar link, official Facebook page (facebook.com/phanstailor or /phantailor), Google Business access."),
    t("Người liên hệ chính bên Phan's và kênh liên lạc (Zalo, WhatsApp, email).", "Main contact at Phan's and preferred channel (Zalo, WhatsApp, email)."),
    t("Liên hệ đội Web 3D, nếu anh muốn hai bên phối hợp.", "Contact for the Web 3D team, if he wants us to coordinate."),
  ]
  s7 = section(7, t("Thông tin cần lấy từ anh Thịnh (đánh dấu khi có)", "Information to collect (tick when received)"), ul(ck, 'check'))

  s8 = section(8, t("Sau cuộc gọi, gửi Xin", "After the call, send Xin"), ul([
    t("Anh Thịnh đồng ý phạm vi nào, muốn thêm hoặc bỏ gì.", "Which scope Thinh agreed to, and anything to add or remove."),
    t("Tên miền nào làm chính.", "Which domain he chose as main."),
    t("Câu hỏi mình chưa trả lời được.", "Any questions we couldn't answer."),
    t("Thông tin ở mục 7 đã có hoặc khi nào gửi.", "Which section 7 items we have, or when they'll come."),
    t("Khi nào anh muốn nhận báo giá.", "When he'd like the quote.")]) +
    f'<p class="note">{t("Liên hệ Xin qua WhatsApp nếu cần hỏi gấp trong cuộc gọi.", "Message Xin on WhatsApp if something urgent comes up during the call.")}</p>')

  body = top + s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8
  return f'''<!doctype html><html lang="{L}"><head><meta charset="utf-8"><title>{t("Briefing cuộc gọi – Phan's", "Call briefing – Phan's")}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600&family=Prata&display=swap">
<style>{CSS}</style></head><body>{body}</body></html>'''

CSS = r'''
@page { size: A4; margin: 18mm 16mm 20mm; }
:root { --ink:#141414; --paper:#f7f6f3; --stone:#d8d5cf; --mute:#5f5f5f; --navy:#1e2a3a; --red:#b3261e; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Be Vietnam Pro", system-ui, sans-serif; color: var(--ink); font-size: 10.5pt; line-height: 1.5; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: var(--navy); }
.top { border-bottom: 2px solid var(--navy); padding-bottom: 12px; margin-bottom: 14px; }
.kicker { font-size: 8.5pt; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: var(--mute); }
h1 { font-family: "Prata", Georgia, serif; font-weight: 400; font-size: 25pt; line-height: 1.15; margin: 6px 0 4px; }
.sub { color: var(--mute); font-size: 10pt; }
.links { display: flex; gap: 24px; margin-top: 8px; font-size: 9.5pt; }
.links b { color: var(--mute); font-weight: 600; margin-right: 6px; }
.summary { background: var(--paper); border-left: 4px solid var(--navy); padding: 12px 16px 10px; margin-bottom: 18px; break-inside: avoid; }
.summary h3 { font-size: 10.5pt; letter-spacing: .08em; text-transform: uppercase; color: var(--navy); margin-bottom: 6px; }
section { margin-bottom: 16px; }
h2 { font-family: "Prata", Georgia, serif; font-weight: 400; font-size: 15pt; margin: 6px 0 8px; display: flex; align-items: center; gap: 10px; break-after: avoid; }
h2 .n { display: inline-grid; place-items: center; width: 24px; height: 24px; border-radius: 50%; background: var(--navy); color: #fff; font-family: "Be Vietnam Pro"; font-size: 10pt; font-weight: 600; flex: none; }
h4 { font-size: 10pt; text-transform: uppercase; letter-spacing: .08em; color: var(--navy); margin-bottom: 4px; }
ul { padding-left: 18px; } ol { padding-left: 24px; }
li { margin: 3px 0; }
li b { font-weight: 600; }
.cols { display: grid; grid-template-columns: 1fr 1.25fr; gap: 22px; break-inside: avoid; }
.lead { color: var(--mute); margin-bottom: 4px; }
.dia { width: 100%; height: auto; margin: 2px 0 10px; break-inside: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 9.5pt; }
th { text-align: left; font-size: 8.5pt; text-transform: uppercase; letter-spacing: .08em; color: var(--mute); border-bottom: 1.5px solid var(--ink); padding: 5px 8px 5px 0; }
td { border-bottom: 1px solid var(--stone); padding: 6px 10px 6px 0; vertical-align: top; }
tr { break-inside: avoid; }
table.gloss td:first-child { width: 28%; font-weight: 600; }
table.qa td:first-child { width: 33%; font-weight: 600; }
ul.no { list-style: none; padding-left: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 2px 20px; }
ul.no li { padding-left: 20px; position: relative; }
ul.no li::before { content: ""; position: absolute; left: 0; top: 7px; width: 10px; height: 2px; background: var(--red); transform: rotate(45deg); box-shadow: 0 0 0 0 var(--red); }
ul.no li::after { content: ""; position: absolute; left: 0; top: 7px; width: 10px; height: 2px; background: var(--red); transform: rotate(-45deg); }
ul.check { list-style: none; padding-left: 0; }
ul.check li { padding-left: 26px; position: relative; margin: 5px 0; break-inside: avoid; }
ul.check li::before { content: ""; position: absolute; left: 0; top: 2px; width: 13px; height: 13px; border: 1.5px solid var(--navy); border-radius: 2px; }
.note { margin-top: 8px; color: var(--mute); font-size: 9.5pt; }
.appendix { break-before: page; }
.msg { background: var(--paper); border: 1px solid var(--stone); padding: 12px 16px; font-size: 8.5pt; line-height: 1.34; }
.msg p { margin: 0; }
.msg p.gap { height: 5px; }
'''

FOOT = '<div style="width:100%;font-family:Arial,sans-serif;font-size:7.5pt;color:#5f5f5f;padding:0 16mm;display:flex;justify-content:space-between"><span>{label}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'

if __name__ == '__main__':
  outs = {'vi': ('Briefing-cuoc-goi-Kimlien-VI', "Phan's Custom Tailor · Briefing cuộc gọi · Nội bộ"), 'en': ('Call-briefing-Kimlien-EN', "Phan's Custom Tailor · Call briefing · Internal")}
  with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for L, (name, label) in outs.items():
      open(f'{name}.html', 'w').write(build(L))
      pg.goto('file://' + os.path.abspath(f'{name}.html'), wait_until='load', timeout=90000); pg.wait_for_timeout(1500)
      ok = pg.evaluate("document.fonts.check('12px \"Be Vietnam Pro\"') && document.fonts.check('20px Prata')")
      pg.pdf(path=f'{name}.pdf', format='A4', print_background=True, display_header_footer=True,
             header_template='<span></span>', footer_template=FOOT.format(label=label),
             margin={'top': '18mm', 'bottom': '20mm', 'left': '16mm', 'right': '16mm'})
      print(name, 'fonts ok' if ok else 'FONTS NOT LOADED')
    b.close()
