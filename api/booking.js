// Booking API for the /book-an-appointment/ page (Vercel serverless function).
// Cal.com does the real work: availability, 3 seats per slot, confirmation email with a calendar invite,
// reschedule and cancel links. This function only keeps the Cal.com key off the browser and stores uploads.
//   GET  /api/booking?service=consult&start=2026-10-01&end=2026-10-31  -> { demo, max, slots: { 'YYYY-MM-DD': [{ start, time, count }] } }
//   POST /api/booking  { service, start, name, email, phone, guest, status, lang, answers, file }  -> { ok, demo, uid }
// Env (Vercel project settings, never in the repo): CAL_API_KEY (optional), CAL_USERNAME (overrides config),
// BLOB_READ_WRITE_TOKEN (reference-image uploads). No Cal.com username = demo mode: nothing is booked.
import { readFileSync } from 'node:fs';

const config = JSON.parse(readFileSync(new URL('../src/config.json', import.meta.url), 'utf8'));
const B = config.bookingSystem;
const TZ = B.timeZone;
const CAL = 'https://api.cal.com/v2';
const user = () => process.env.CAL_USERNAME || B.calUsername;
const headers = (version) => ({
  'cal-api-version': version, 'Content-Type': 'application/json',
  ...(process.env.CAL_API_KEY ? { Authorization: `Bearer ${process.env.CAL_API_KEY}` } : {}),
});
const hhmm = (iso) => new Intl.DateTimeFormat('en-GB', { timeZone: TZ, hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date(iso));
const clip = (v, n = 500) => String(v ?? '').slice(0, n);

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  try {
    if (req.method === 'GET') return await slots(req, res);
    if (req.method === 'POST') return await book(req, res);
    res.status(405).json({ error: 'method' });
  } catch (e) {
    res.status(500).json({ error: 'server', detail: clip(e && e.message) });
  }
}

async function slots(req, res) {
  const { service, start, end } = req.query;
  if (!user()) return res.json({ demo: true });
  const slug = B.events[service];
  if (!slug || !/^\d{4}-\d{2}-\d{2}$/.test(start || '') || !/^\d{4}-\d{2}-\d{2}$/.test(end || '')) return res.status(400).json({ error: 'input' });
  const q = new URLSearchParams({ eventTypeSlug: slug, username: user(), start, end, timeZone: TZ, format: 'range' });
  const r = await fetch(`${CAL}/slots?${q}`, { headers: headers('2024-09-04') });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) return res.status(502).json({ error: 'cal' });
  const out = {};
  for (const [date, list] of Object.entries(j.data || {})) out[date] = (list || []).map((s) => ({ start: s.start, time: hhmm(s.start), count: s.attendeesCount || 0 }));
  res.json({ demo: false, max: B.maxPerSlot, slots: out });
}

async function book(req, res) {
  const b = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
  const okEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(b.email || '');
  if (!B.events[b.service] || !b.start || !b.name || !okEmail || String(b.phone || '').replace(/\D/g, '').length < 8) return res.status(400).json({ error: 'input' });
  if (!user()) return res.json({ ok: true, demo: true });

  let fileUrl = '';
  const m = b.file && /^data:(image\/(?:png|jpeg));base64,(.+)$/.exec(b.file.data || '');
  if (m && process.env.BLOB_READ_WRITE_TOKEN) {
    const buf = Buffer.from(m[2], 'base64');
    if (buf.length <= 10 * 1024 * 1024) {
      const { put } = await import('@vercel/blob');
      const name = String(b.file.name || 'reference').replace(/[^\w.-]+/g, '-').slice(0, 60);
      fileUrl = (await put(`booking-references/${Date.now()}-${name}`, buf, { access: 'public', contentType: m[1] })).url;
    }
  }
  const answers = Object.entries(b.answers || {}).filter(([, v]) => v && String(v).trim()).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`);
  const notes = [`Client status: ${b.status || '-'}`, ...answers, b.guest ? `Guest: ${b.guest}` : '', fileUrl ? `Reference image: ${fileUrl}` : (b.file ? 'Reference image: attached on the website but uploads are not set up; ask the client to send it on WhatsApp.' : '')].filter(Boolean).join('\n');
  const body = {
    start: b.start,
    eventTypeSlug: B.events[b.service], username: user(),
    attendee: { name: clip(b.name, 120), email: b.email, timeZone: TZ, phoneNumber: b.phone, language: b.lang === 'zh' ? 'zh-CN' : b.lang === 'vi' ? 'vi' : 'en' },
    guests: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test((b.guest || '').trim()) ? [b.guest.trim()] : [],
    bookingFieldsResponses: { notes: clip(notes, 2000) },
    metadata: { service: clip(b.service, 40), status: clip(b.status, 60), site: 'phans-website' },
  };
  const r = await fetch(`${CAL}/bookings`, { method: 'POST', headers: headers('2026-02-25'), body: JSON.stringify(body) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) return res.status(502).json({ error: 'cal', detail: clip(j && (j.error?.message || j.message)) });
  res.json({ ok: true, demo: false, uid: j.data?.uid || j.data?.[0]?.uid || '' });
}
