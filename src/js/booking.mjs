// Phan's booking page: 3 steps (service, date and time, details) beside the fixed studio policies.
// Talks to /api/booking (Cal.com behind it). When the API answers demo:true, or isn't there (local preview),
// it shows sample availability and a clearly labelled preview confirmation: nothing is booked.
const root = document.querySelector('[data-pct-book]');
const dataEl = document.getElementById('pct-book-data');
if (root && dataEl) {
  const { lang, T, sys, api } = JSON.parse(dataEl.textContent);
  const TZ = sys.timeZone, MAX = sys.maxPerSlot;
  const esc = (t) => String(t ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const loc = { en: 'en-GB', vi: 'vi-VN', zh: 'zh-CN' }[lang] || 'en-GB';
  const ymd = (d) => new Intl.DateTimeFormat('en-CA', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit' }).format(d);
  const nowHM = () => new Intl.DateTimeFormat('en-GB', { timeZone: TZ, hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date());
  const today = ymd(new Date());
  const pad = (n) => String(n).padStart(2, '0');
  const isoICT = (date, time) => new Date(`${date}T${time}:00+07:00`).toISOString();

  const st = { service: null, month: today.slice(0, 7), date: null, time: null, start: null, demo: false, cache: {} };
  const $ = (s) => root.querySelector(s);
  const steps = [...root.querySelectorAll('[data-bstep]')];
  const show = (n) => {
    steps.forEach((el) => { el.hidden = Number(el.dataset.bstep) !== n; });
    root.querySelectorAll('[data-bdot]').forEach((d) => { const k = Number(d.dataset.bdot); d.classList.toggle('is-on', k === n); d.classList.toggle('is-done', k < n); d.setAttribute('aria-current', k === n ? 'step' : 'false'); });
    const panel = $('.pct-book__flow');
    if (panel && (window.matchMedia('(max-width: 899px)').matches || panel.getBoundingClientRect().top < 0)) window.scrollTo({ top: panel.getBoundingClientRect().top + scrollY - 96, behavior: 'smooth' });
    const cnt = $('[data-bcount]'); if (cnt) { cnt.textContent = T.stepOf.replace('{n}', String(Math.min(n, 3))); cnt.parentElement.hidden = n > 3; }
    const h = steps[n - 1].querySelector('h2'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
  };
  const chosen = () => {
    const s = T.services[st.service];
    const when = st.date ? `${new Intl.DateTimeFormat(loc, { timeZone: 'UTC', weekday: 'long', day: 'numeric', month: 'long' }).format(new Date(st.date + 'T00:00:00Z'))}${st.time ? ', ' + st.time + ' ' + T.tz : ''}` : '';
    root.querySelectorAll('[data-bchosen]').forEach((el) => { el.innerHTML = `<p class="pct-book__cs">${esc(s ? s[0] : '')}</p>${when ? `<p class="pct-book__cw">${esc(when)}</p>` : ''}`; });
    const u = $('[data-burgent]'); if (u) u.hidden = st.service !== 'urgent';
  };

  // ---------- step 1 ----------
  root.addEventListener('click', (e) => {
    const svc = e.target.closest('[data-service]');
    if (svc) { st.service = svc.dataset.service; st.date = st.time = null; root.querySelectorAll('[data-service]').forEach((b) => b.setAttribute('aria-pressed', String(b === svc))); chosen(); renderCal(); show(2); return; }
    const back = e.target.closest('[data-bback]'); if (back) { show(Number(back.dataset.bback)); return; }
    const mv = e.target.closest('[data-month]');
    if (mv) { const [y, m] = st.month.split('-').map(Number); const d = new Date(Date.UTC(y, m - 1 + Number(mv.dataset.month), 1)); st.month = `${d.getUTCFullYear()}-${pad(d.getUTCMonth() + 1)}`; renderCal(); return; }
    const day = e.target.closest('[data-day]'); if (day && !day.disabled) { st.date = day.dataset.day; st.time = null; renderCal(); renderSlots(); return; }
    const slot = e.target.closest('[data-slot]');
    if (slot && !slot.disabled) { st.time = slot.dataset.slot; st.start = slot.dataset.start; chosen(); buildForm(); show(3); return; }
  });

  // ---------- step 2: availability ----------
  function demoMonth(month) {
    const [y, m] = month.split('-').map(Number), out = {};
    const days = new Date(Date.UTC(y, m, 0)).getUTCDate();
    for (let d = 1; d <= days; d++) {
      const date = `${month}-${pad(d)}`, dow = new Date(date + 'T00:00:00Z').getUTCDay();
      const h = sys.hours[dow]; if (!h || sys.closedDates.includes(date)) continue;
      const [oh, om] = h[0].split(':').map(Number), [ch, cm] = h[1].split(':').map(Number);
      const list = [];
      for (let t = oh * 60 + om; t <= ch * 60 + cm - sys.lastStartBeforeClose; t += sys.slotMinutes) {
        const time = `${pad(Math.floor(t / 60))}:${pad(t % 60)}`;
        let hsh = 0; for (const c of date + time + st.service) hsh = (hsh * 31 + c.charCodeAt(0)) >>> 0;
        list.push({ time, start: isoICT(date, time), count: [0, 0, 1, 1, 2, 3][hsh % 6] });
      }
      out[date] = list;
    }
    return out;
  }
  async function load(month) {
    const key = `${st.service}|${month}`;
    if (st.cache[key]) return st.cache[key];
    const [y, m] = month.split('-').map(Number);
    const end = `${month}-${pad(new Date(Date.UTC(y, m, 0)).getUTCDate())}`;
    let slots;
    try {
      const r = await fetch(`${api}?service=${encodeURIComponent(st.service)}&start=${month}-01&end=${end}`, { headers: { Accept: 'application/json' } });
      const j = await r.json();
      if (j.demo) { st.demo = true; slots = demoMonth(month); } else if (r.ok) slots = j.slots || {}; else throw new Error('api');
    } catch (e) { st.demo = true; slots = demoMonth(month); }
    st.cache[key] = slots;
    return slots;
  }
  async function renderCal() {
    const box = $('[data-bcal]'); if (!st.service) return;
    const [y, m] = st.month.split('-').map(Number);
    const title = new Intl.DateTimeFormat(loc, { month: 'long', year: 'numeric', timeZone: 'UTC' }).format(new Date(Date.UTC(y, m - 1, 1)));
    const canPrev = st.month > today.slice(0, 7);
    box.innerHTML = `<div class="pct-book__calhead"><button type="button" class="pct-book__arrow" data-month="-1" aria-label="${esc(T.prevMonth)}"${canPrev ? '' : ' disabled'}>&#8249;</button><p class="pct-book__month" aria-live="polite">${esc(title)}</p><button type="button" class="pct-book__arrow" data-month="1" aria-label="${esc(T.nextMonth)}">&#8250;</button></div><div class="pct-book__grid is-loading"></div>`;
    const slots = await load(st.month);
    const first = (new Date(Date.UTC(y, m - 1, 1)).getUTCDay() + 6) % 7; // Monday first
    const days = new Date(Date.UTC(y, m, 0)).getUTCDate();
    const wd = [...Array(7)].map((_, i) => new Intl.DateTimeFormat(loc, { weekday: 'short', timeZone: 'UTC' }).format(new Date(Date.UTC(2024, 0, 1 + i))));
    let cells = wd.map((w) => `<span class="pct-book__wd" aria-hidden="true">${esc(w)}</span>`).join('') + '<span></span>'.repeat(first);
    for (let d = 1; d <= days; d++) {
      const date = `${st.month}-${pad(d)}`;
      const list = (slots[date] || []).filter((s) => date > today || s.time > nowHM());
      const closed = sys.closedDates.includes(date) || !sys.hours[new Date(date + 'T00:00:00Z').getUTCDay()];
      const open = date >= today && !closed && list.some((s) => s.count < MAX);
      const label = new Intl.DateTimeFormat(loc, { timeZone: 'UTC', weekday: 'long', day: 'numeric', month: 'long' }).format(new Date(date + 'T00:00:00Z'));
      const free = list.reduce((a, x) => a + Math.max(0, MAX - x.count), 0), cap = list.length * MAX || 1;
      const lvl = !open ? '' : free / cap > 0.55 ? ' is-many' : ' is-few';
      cells += `<button type="button" class="pct-book__day${st.date === date ? ' is-on' : ''}${closed && date >= today ? ' is-closed' : ''}${date === today ? ' is-today' : ''}${lvl}" data-day="${date}" ${open ? '' : 'disabled'} aria-pressed="${st.date === date}" aria-label="${esc(label)}${closed ? ', ' + esc(T.closed) : ''}"><span>${d}</span><i aria-hidden="true"></i></button>`;
    }
    const grid = box.querySelector('.pct-book__grid');
    grid.classList.remove('is-loading'); grid.innerHTML = cells;
    if (st.date && st.date.startsWith(st.month)) renderSlots(); else $('[data-bslots]').innerHTML = `<p class="pct-book__hint">${esc(T.pickDay)}</p>`;
    $('[data-bdemo]').hidden = !st.demo;
  }
  function renderSlots() {
    const list = (st.cache[`${st.service}|${st.month}`]?.[st.date] || []).filter((s) => st.date > today || s.time > nowHM());
    const box = $('[data-bslots]');
    if (!list.length) { box.innerHTML = `<p class="pct-book__hint">${esc(T.noSlots)}</p>`; return; }
    const part = (t) => (t < '12:00' ? 'morning' : t < '17:00' ? 'afternoon' : 'evening');
    const groups = ['morning', 'afternoon', 'evening'].map((g) => [g, list.filter((x) => part(x.time) === g)]).filter(([, l]) => l.length);
    box.innerHTML = `<p class="pct-book__tz"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>${esc(T.tz)}</p>` + groups.map(([g, l]) =>
      `<div class="pct-book__period"><p>${esc(T[g])}</p><div class="pct-book__slots">${l.map((x) => {
        const left = MAX - x.count, full = left <= 0;
        const note = full ? T.full : left < MAX ? T.left.replace('{n}', String(left)) : '';
        return `<button type="button" class="pct-book__slot${full ? '' : left === 1 ? ' is-last' : ''}" data-slot="${x.time}" data-start="${x.start}"${full ? ' disabled' : ''} aria-label="${x.time} ${esc(T.tz)}${note ? ', ' + esc(note) : ''}"><b>${x.time}</b>${note ? `<span>${esc(note)}</span>` : ''}</button>`;
      }).join('')}</div></div>`).join('');
  }

  // ---------- step 3: details ----------
  const F = T.f;
  const fld = (name, label, input, req = true, hint = '') => `<div class="pct-book__field" data-field="${name}"><label for="pb-${name}">${esc(label)}${req ? '' : ` <span class="pct-book__opt">(${esc(F.optional)})</span>`}</label>${input}${hint ? `<p class="pct-book__fhint" id="pb-${name}-hint">${esc(hint)}</p>` : ''}<p class="pct-book__err" id="pb-${name}-err" aria-live="polite"></p></div>`;
  const text = (name, type = 'text', req = true, extra = '') => `<input id="pb-${name}" name="${name}" type="${type}"${req ? ' required aria-required="true"' : ''} aria-describedby="pb-${name}-err pb-${name}-hint"${extra}>`;
  const area = (name, req = true) => `<textarea id="pb-${name}" name="${name}" rows="3"${req ? ' required aria-required="true"' : ''} aria-describedby="pb-${name}-err pb-${name}-hint"></textarea>`;
  const file = (name, req) => `<input id="pb-${name}" name="${name}" type="file" accept="image/jpeg,image/png"${req ? ' required aria-required="true"' : ''} aria-describedby="pb-${name}-err pb-${name}-hint">`;
  const CC = ['+84', '+1', '+44', '+61', '+64', '+65', '+60', '+66', '+62', '+63', '+81', '+82', '+86', '+852', '+886', '+91', '+971', '+33', '+49', '+31', '+41', '+46', '+47', '+45', '+39', '+34', '+353', '+7'];
  function buildForm() {
    const kind = sys.fieldsFor[st.service];
    let dyn = '';
    if (kind === 'bespoke') dyn = `<fieldset class="pct-book__field" data-field="items"><legend>${esc(F.items)}</legend><div class="pct-book__checks">${F.itemOpts.map((o, i) => `<label><input type="checkbox" name="items" value="${esc(o)}"${i === 0 ? ' checked' : ''}> ${esc(o)}</label>`).join('')}</div><p class="pct-book__err" id="pb-items-err" aria-live="polite"></p></fieldset>` +
      fld('flight', F.flight, text('flight', 'date', false), false) + fld('measure', F.measure, text('measure', 'text', false), false, F.measureHint) + fld('ref', F.refImg, file('ref', false), false, F.refHint);
    if (kind === 'group') dyn = fld('groupItems', F.groupItems, area('groupItems'), true, F.groupHint) + fld('event', F.event, text('event', 'date', false), false);
    if (kind === 'female') dyn = fld('fit', F.fit, area('fit')) + fld('ref', F.refStyles, file('ref', true), true, F.refHint) +
      `<div class="pct-book__field" data-field="dress"><label class="pct-book__check"><input type="checkbox" id="pb-dress" name="dress" required aria-describedby="pb-dress-err"> ${esc(F.dressPolicy)}</label><p class="pct-book__err" id="pb-dress-err" aria-live="polite"></p></div>`;
    if (kind === 'followup') dyn = fld('order', F.order, text('order')) + fld('concerns', F.concerns, area('concerns', false), false);
    const statusR = `<fieldset class="pct-book__field" data-field="status"><legend>${esc(F.status)}</legend><div class="pct-book__radios">${F.statusOpts.map((o, i) => `<label><input type="radio" name="status" value="${esc(o)}" required${i === 0 ? ' checked' : ''}> ${esc(o)}</label>`).join('')}</div></fieldset>`;
    $('[data-bform]').innerHTML =
      fld('name', F.name, text('name', 'text', true, ' autocomplete="name"')) +
      fld('email', F.email, text('email', 'email', true, ' autocomplete="email" inputmode="email"')) +
      fld('phone', F.phone, `<div class="pct-book__phone"><select id="pb-cc" name="cc" aria-label="Country code">${CC.map((c) => `<option>${c}</option>`).join('')}</select>${text('phone', 'tel', true, ' autocomplete="tel-national" inputmode="tel"')}</div>`, true, F.phoneHint) +
      fld('guest', F.guest, text('guest', 'text', false), false, F.guestHint) + statusR + dyn;
    const meas = $('[data-field="measure"]');
    const syncMeas = () => { if (meas) meas.hidden = ($('input[name="status"]:checked') || {}).value !== F.statusOpts[0]; };
    root.querySelectorAll('input[name="status"]').forEach((r) => r.addEventListener('change', syncMeas)); syncMeas();
    const ack = $('#pb-ack'); if (ack) ack.checked = false;
    try { const saved = JSON.parse(localStorage.getItem('pct-book-client') || 'null'); if (saved) ['name', 'email', 'phone', 'cc'].forEach((k) => { const el = $(`#pb-${k}`); if (el && saved[k]) el.value = saved[k]; }); } catch (e) { /* storage blocked */ }
  }
  const setErr = (name, msg) => { const e = $(`#pb-${name}-err`); if (e) e.textContent = msg || ''; const i = $(`#pb-${name}`); if (i) i.setAttribute('aria-invalid', msg ? 'true' : 'false'); return !msg; };
  function validate(fd) {
    let ok = true, firstBad = null;
    const bad = (n, m) => { ok = setErr(n, m) && ok; if (m && !firstBad) firstBad = n; };
    bad('name', fd.get('name').trim() ? '' : T.err.required);
    bad('email', /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(fd.get('email').trim()) ? '' : T.err.email);
    bad('phone', fd.get('phone').replace(/\D/g, '').length >= 8 ? '' : T.err.phone);
    const kind = sys.fieldsFor[st.service];
    if (kind === 'bespoke') bad('items', fd.getAll('items').length ? '' : T.err.required);
    if (kind === 'group') bad('groupItems', (fd.get('groupItems') || '').trim() ? '' : T.err.required);
    if (kind === 'female') { bad('fit', (fd.get('fit') || '').trim() ? '' : T.err.required); bad('dress', fd.get('dress') ? '' : T.err.policy); }
    if (kind === 'followup') bad('order', (fd.get('order') || '').trim() ? '' : T.err.required);
    const f = fd.get('ref');
    if (f && f.size) { if (!/^image\/(jpeg|png)$/.test(f.type)) bad('ref', T.err.fileType); else bad('ref', f.size > 10 * 1024 * 1024 ? T.err.file : ''); }
    else if (kind === 'female') bad('ref', T.err.required);
    bad('ack', fd.get('ack') ? '' : T.err.policy);
    if (firstBad) $(`#pb-${firstBad}`)?.focus();
    return ok;
  }
  async function shrink(f) { // keep uploads small enough for the API (photos up to ~2000 px, JPEG)
    const img = await createImageBitmap(f);
    const k = Math.min(1, 2000 / Math.max(img.width, img.height));
    const c = document.createElement('canvas'); c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
    c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
    return { name: f.name.replace(/\.\w+$/, '') + '.jpg', data: c.toDataURL('image/jpeg', 0.85) };
  }
  root.querySelector('[data-bformwrap]').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.currentTarget, fd = new FormData(form);
    if (!validate(fd)) return;
    const btn = form.querySelector('[type="submit"]'); const label = btn.textContent; btn.disabled = true; btn.textContent = T.sending;
    const kind = sys.fieldsFor[st.service];
    const pick = (k) => (fd.get(k) || '').toString().trim();
    const answers = {
      bespoke: { Items: fd.getAll('items'), 'Flight departure': pick('flight'), 'Height, weight, fit': pick('measure') },
      group: { 'Pieces and recipients': pick('groupItems'), 'Event date': pick('event') },
      female: { 'Desired fit': pick('fit'), 'Confirmed suit, not a dress': 'Yes' },
      followup: { 'Order / receipt': pick('order'), Concerns: pick('concerns') },
    }[kind];
    const phone = `${pick('cc')} ${pick('phone')}`;
    try { localStorage.setItem('pct-book-client', JSON.stringify({ name: pick('name'), email: pick('email'), phone: pick('phone'), cc: pick('cc') })); } catch (x) { /* ignore */ }
    let file = null; const f = fd.get('ref'); if (f && f.size) { try { file = await shrink(f); } catch (x) { file = null; } }
    const payload = { service: st.service, start: st.start, name: pick('name'), email: pick('email'), phone, guest: pick('guest'), status: pick('status'), lang, answers, file };
    let res = { ok: true, demo: true };
    if (!st.demo) {
      try { const r = await fetch(api, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }); res = await r.json(); if (!r.ok) res = { ok: false }; } catch (x) { res = { ok: false }; }
    }
    btn.disabled = false; btn.textContent = label;
    if (!res.ok) { $('[data-bformerr]').textContent = T.err.server; return; }
    if (window.dataLayer) window.dataLayer.push({ event: 'booking_confirmed', service: st.service, demo: !!res.demo });
    $('[data-bdone-title]').textContent = res.demo ? T.demoTitle : T.doneTitle;
    $('[data-bdone-body]').textContent = res.demo ? T.demoBody : T.doneBody;
    st.lastDemo = !!res.demo;
    const ics = $('[data-bics]'); if (ics) ics.hidden = !!res.demo;
    chosen(); show(4);
  });
  root.querySelector('[data-bics]')?.addEventListener('click', () => {
    const s = new Date(st.start), e = new Date(s.getTime() + 60 * 60000), f = (d) => d.toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
    const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Phans Custom Tailor//Booking//EN', 'BEGIN:VEVENT', `UID:${f(s)}-${st.service}@phanscustomtailor`, `DTSTAMP:${f(new Date())}`, `DTSTART:${f(s)}`, `DTEND:${f(e)}`,
      `SUMMARY:Phan's Custom Tailor: ${T.services[st.service][0]}`, `LOCATION:${T.where}`, 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' })); a.download = 'phans-appointment.ics'; a.click();
  });
  root.querySelector('[data-bpolicies]')?.addEventListener('click', (e) => { const d = $('.pct-book__info'); if (d) d.open = true; });
  root.querySelector('[data-bagain]').addEventListener('click', () => { st.service = st.date = st.time = null; root.querySelectorAll('[data-service]').forEach((b) => b.setAttribute('aria-pressed', 'false')); show(1); });
  if (window.matchMedia('(max-width: 899px)').matches) { const d = $('.pct-book__info'); if (d) d.open = false; }
}
