// PNG of a suit design for the AI fitting room (Decart Anywear needs a real image URL, not inline SVG).
// GET /api/suit?fabric=navy-twill&lapel=peak&...  -> image/png, front view on white, cached for a year.
// Same drawing as the website (src/js/suit-svg.mjs); fabric tiles are embedded so the renderer needs no network.
import { readFileSync } from 'node:fs';
import resvg from '@resvg/resvg-js';
import { suitSVG, DEFAULTS } from '../src/js/suit-svg.mjs';

const cfg = JSON.parse(readFileSync(new URL('../src/data/configurator.json', import.meta.url), 'utf8'));
const FAB = {};
for (const f of cfg.fabrics) {
  const b64 = readFileSync(new URL(`../assets/img/cfg/${f.id}.jpg`, import.meta.url)).toString('base64');
  FAB[f.id] = { tile: `data:image/jpeg;base64,${b64}`, tone: f.tone, scale: f.scale };
}
const valid = Object.fromEntries(cfg.groups.map((g) => [g.key, new Set(g.options.map((o) => o.v))]));

export default function handler(req, res) {
  const s = { view: 'front' };
  for (const k of Object.keys(DEFAULTS)) {
    const v = req.query[k];
    if (typeof v !== 'string') continue;
    if (k === 'fabric' ? FAB[v] : valid[k] && valid[k].has(v)) s[k] = v;
  }
  const svg = suitSVG(s, FAB, { viewBox: '56 40 288 730', bg: false, label: 'Suit design' });
  const png = new resvg.Resvg(svg, { fitTo: { mode: 'height', value: 1200 }, background: '#ffffff' }).render().asPng();
  res.setHeader('Content-Type', 'image/png');
  res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
  res.status(200).send(Buffer.from(png));
}
