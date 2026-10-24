// Phan's suit configurator: draws the suit as SVG from the chosen options.
// Shared by build.mjs (first render, so the page works without JavaScript) and the browser.
// Front and back views on a 400 x 780 canvas; the left half is drawn and mirrored for the right.

const MIRROR = 'translate(400 0) scale(-1 1)';
const BTN = { horn: ['#2a221e', '#4a3d35'], brown: ['#5a3c28', '#8a6248'], pearl: ['#e8e3d8', '#fbf8f1'], match: null };

export const DEFAULTS = {
  fabric: 'navy-twill', fit: 'slim', closure: 'sb2', lapel: 'notch', pockets: 'flap', breast: 'welt',
  vents: 'side', waistcoat: 'no', pleats: 'none', hem: 'plain', lining: 'burgundy', buttons: 'horn', monogram: '', view: 'front',
};

const rollY = (s) => ({ sb1: 320, sb2: 300, sb3: 268, db6: 300 }[s.closure] || 300);

function lapel(s, ry) {
  const mid = 124 + (ry - 124) * 0.62;
  if (s.lapel === 'peak') return `M200,${ry} L181,76 L157,86 L155,100 L127,92 L133,122 Q147,${mid} 200,${ry} Z`;
  if (s.lapel === 'shawl') return `M200,${ry} L181,76 Q150,82 138,126 Q148,${mid} 200,${ry} Z`;
  return `M200,${ry} L181,76 L155,86 L153,104 L164,110 L133,123 Q147,${mid} 200,${ry} Z`;
}

function frontPanel(s, ry) {
  const sw = s.fit === 'slim' ? 106 : 97, sh = s.fit === 'slim' ? 101 : 93;
  const hem = s.closure === 'db6' ? `L200,452` : `C128,456 160,458 179,452 C194,420 200,372 200,${ry + 4}`;
  return `M179,72 L124,90 C110,94 101,112 100,142 L${sw},300 L${sh},448 ${hem} L200,${ry} L186,150 Z`;
}
function backPanel(s) {
  const sw = s.fit === 'slim' ? 106 : 97, sh = s.fit === 'slim' ? 101 : 93;
  return `M176,70 L124,90 C110,94 101,112 100,142 L${sw},300 L${sh},450 L200,450 L200,68 Z`;
}
const SHOULDER = '<path d="M126,92 Q150,84 176,78" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="6" stroke-linecap="round" filter="url(#cfg-fold)"/>';
const SLEEVE = 'M124,90 C102,94 86,108 82,142 L66,426 L99,430 L105,192 C107,150 112,112 124,90 Z';
function leg(s) {
  const xo = s.fit === 'slim' ? 131 : 126, xi = s.fit === 'slim' ? 192 : 194;
  return { d: `M118,382 L200,382 L200,456 L${xi},744 L${xo},744 Z`, xo, xi };
}

function buttons(s, ry, fill) {
  const pos = { sb1: [[200, 320]], sb2: [[200, 300], [200, 352]], sb3: [[200, 268], [200, 312], [200, 356]],
    db6: [[180, 300], [220, 300], [180, 344], [220, 344], [170, 256], [230, 256]] }[s.closure];
  return pos.map(([x, y]) => btn(x, y, 6.2, fill)).join('');
}
function btn(x, y, r, [c, hi]) {
  return `<g><circle cx="${x + r * 0.25}" cy="${y + r * 0.35}" r="${r}" fill="#000" opacity=".35" filter="url(#cfg-soft)"/><circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/><circle cx="${x}" cy="${y}" r="${r * 0.72}" fill="none" stroke="${hi}" stroke-width="0.8" opacity=".7"/>` +
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([a, b]) => `<circle cx="${x + a * r * 0.28}" cy="${y + b * r * 0.28}" r="${r * 0.12}" fill="${hi}" opacity=".8"/>`).join('') + `</g>`;
}

function pocket(s) {
  if (s.pockets === 'patch') return `<path d="M110,350 L172,350 L172,404 Q172,412 164,412 L118,412 Q110,412 110,404 Z" fill="url(#cfg-fab)"/>` +
    `<path d="M110,350 L172,350 L172,404 Q172,412 164,412 L118,412 Q110,412 110,404 Z" fill="url(#cfg-lift)" stroke="rgba(0,0,0,.35)" stroke-width="1"/>` +
    `<path d="M114,354 L168,354 L168,403 Q168,408 163,408 L119,408 Q114,408 114,403 Z" fill="none" stroke="rgba(255,255,255,.28)" stroke-width=".8" stroke-dasharray="2 2"/>`;
  if (s.pockets === 'jetted') return `<rect x="114" y="368" width="54" height="5" rx="1" fill="rgba(0,0,0,.45)"/><line x1="114" y1="370.5" x2="168" y2="370.5" stroke="rgba(255,255,255,.18)" stroke-width=".7"/>`;
  return `<rect x="112" y="366" width="58" height="4" fill="rgba(0,0,0,.45)"/>` +
    `<path d="M112,368 L170,368 L169,386 Q169,388 167,388 L115,388 Q113,388 113,386 Z" fill="url(#cfg-fab)"/>` +
    `<path d="M112,368 L170,368 L169,386 Q169,388 167,388 L115,388 Q113,388 113,386 Z" fill="url(#cfg-lift)" stroke="rgba(0,0,0,.35)" stroke-width=".9"/>`;
}

function defs(fab, lining) {
  const sc = fab.scale || 110;
  return `<defs>
<pattern id="cfg-fab" patternUnits="userSpaceOnUse" width="${sc}" height="${sc}"><rect width="${sc}" height="${sc}" fill="${fab.tone}"/><image href="${fab.tile}" width="${sc}" height="${sc}" preserveAspectRatio="none"/></pattern>
<linearGradient id="cfg-side" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".34"/><stop offset=".28" stop-color="#000" stop-opacity=".06"/><stop offset=".62" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".12"/></linearGradient>
<linearGradient id="cfg-down" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".07"/><stop offset=".7" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".18"/></linearGradient>
<linearGradient id="cfg-lift" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#000" stop-opacity=".12"/></linearGradient>
<linearGradient id="cfg-lapel" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#000" stop-opacity=".1"/></linearGradient>
<linearGradient id="cfg-leg" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".28"/><stop offset=".45" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient>
<filter id="cfg-soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.4"/></filter><filter id="cfg-fold" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.2"/></filter><filter id="cfg-ao" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter><clipPath id="cfg-legc"><path d="M118,382 L200,382 L200,456 L196,744 L124,744 Z"/></clipPath><clipPath id="cfg-slv"><path d="${SLEEVE}"/></clipPath><radialGradient id="cfg-chest" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient><radialGradient id="cfg-bg" cx=".5" cy=".38" r=".75"><stop offset="0" stop-color="#f4f2ee"/><stop offset="1" stop-color="#dcd8d1"/></radialGradient>
</defs>`;
}

// soft folds: a dark crease with a light ridge beside it, blurred, so the cloth reads as draped rather than flat
const fold = (d, k = 1) => `<path d="${d}" fill="none" stroke="#000" stroke-opacity="${0.42 * k}" stroke-width="5" stroke-linecap="round" filter="url(#cfg-fold)"/>` +
  `<path d="${d}" fill="none" stroke="#fff" stroke-opacity="${0.16 * k}" stroke-width="3" stroke-linecap="round" filter="url(#cfg-fold)" transform="translate(3 -2)"/>`;
const ao = (d, o = .5) => `<path d="${d}" fill="#000" fill-opacity="${o}" filter="url(#cfg-ao)"/>`;
const half = (inner) => `<g>${inner}</g><g transform="${MIRROR}">${inner}</g>`;

export function suitSVG(state, fabrics, opts = {}) {
  const s = { ...DEFAULTS, ...state };
  const fab = fabrics[s.fabric] || Object.values(fabrics)[0];
  const ry = rollY(s);
  const bfill = BTN[s.buttons] || [fab.btn || '#1d1d1d', '#666'];
  const L = leg(s);
  const box = opts.viewBox || '40 40 320 730';
  const shoe = `<path d="M${L.xo - 6},742 L${L.xi + 2},742 Q${L.xi + 8},756 ${L.xi - 4},760 L${L.xo - 12},760 Q${L.xo - 18},752 ${L.xo - 6},742 Z" fill="#231a14"/>`;
  const trouser = `<path d="${L.d}" fill="url(#cfg-fab)"/><path d="${L.d}" fill="url(#cfg-leg)"/>` +
    `<g clip-path="url(#cfg-legc)">${ao('M196,440 L204,440 L204,744 L196,744 Z', .35)}${ao('M110,446 L200,446 L200,480 L110,480 Z', .55)}${fold(`M${L.xo + 8},${s.hem === 'turnup' ? 704 : 716} Q${(L.xo + L.xi) / 2 - 4},${s.hem === 'turnup' ? 694 : 704} ${(L.xo + L.xi) / 2 + 2},${s.hem === 'turnup' ? 714 : 726} Q${(L.xo + L.xi) / 2 + 10},${s.hem === 'turnup' ? 698 : 708} ${L.xi - 6},${s.hem === 'turnup' ? 708 : 718}`, .6)}${fold(`M${(L.xo + L.xi) / 2},470 L${(L.xo + L.xi) / 2 + 1},600`, .18)}</g>` +
    `<line x1="${(L.xo + L.xi) / 2 + 1}" y1="460" x2="${(L.xo + L.xi) / 2}" y2="742" stroke="rgba(255,255,255,.14)" stroke-width="1.2"/>` +
    (s.pleats !== 'none' ? `<line x1="176" y1="386" x2="178" y2="436" stroke="rgba(0,0,0,.35)" stroke-width="1"/>` : '') +
    (s.pleats === 'double' ? `<line x1="163" y1="386" x2="164" y2="424" stroke="rgba(0,0,0,.3)" stroke-width="1"/>` : '') +
    (s.hem === 'turnup' ? `<path d="M${L.xo - 0.6},724 L${L.xi + 0.4},724 L${L.xi},744 L${L.xo},744 Z" fill="url(#cfg-fab)"/><path d="M${L.xo - 0.6},724 L${L.xi + 0.4},724 L${L.xi},744 L${L.xo},744 Z" fill="rgba(0,0,0,.12)" stroke="rgba(0,0,0,.4)" stroke-width=".9"/>`
      : `<line x1="${L.xo}" y1="743" x2="${L.xi}" y2="743" stroke="rgba(0,0,0,.35)" stroke-width="1"/>`);
  const sleeve = `<path d="${SLEEVE}" fill="url(#cfg-fab)"/><path d="${SLEEVE}" fill="url(#cfg-side)"/><path d="${SLEEVE}" fill="rgba(0,0,0,.1)" stroke="rgba(0,0,0,.28)" stroke-width=".8"/>` +
    `<g clip-path="url(#cfg-slv)">${fold('M80,244 Q91,262 102,258', .8)}${fold('M77,274 Q88,286 100,296', .55)}${fold('M72,392 Q84,400 98,396', .35)}${fold('M86,150 Q93,196 97,232', .5)}</g>` +
    [404, 395, 386].map((y, i) => btn(88 + i * 0.6, y, 2.6, bfill)).join('');

  let body, extraDefs = '';
  if (s.view === 'back') {
    const P = backPanel(s);
    const sh = s.fit === 'slim' ? 101 : 93;
    const vent = s.vents === 'centre' ? `<line x1="201.6" y1="372" x2="201.6" y2="450" stroke="rgba(255,255,255,.32)" stroke-width="1"/><line x1="200" y1="372" x2="200" y2="450" stroke="rgba(0,0,0,.7)" stroke-width="1.8"/><path d="M200,372 L206,376 L206,450" fill="none" stroke="rgba(0,0,0,.45)" stroke-width="1.2"/><path d="M200,372 L206,376 L206,450 L200,450 Z" fill="rgba(0,0,0,.16)"/>`
      : s.vents === 'side' ? `<path d="M${sh + 6},368 L${sh + 12},368 L${sh + 11},449 L${sh + 4},449 Z" fill="rgba(0,0,0,.18)"/><line x1="${sh + 13.6}" y1="368" x2="${sh + 12.6}" y2="449" stroke="rgba(255,255,255,.32)" stroke-width="1"/><line x1="${sh + 12}" y1="368" x2="${sh + 11}" y2="449" stroke="rgba(0,0,0,.7)" stroke-width="1.8"/>` : '';
    body = half(sleeve) + half(`<path d="${P}" fill="url(#cfg-fab)"/><path d="${P}" fill="url(#cfg-side)"/><path d="${P}" fill="url(#cfg-down)" stroke="rgba(0,0,0,.25)" stroke-width=".8"/>` + (s.vents === 'side' ? vent : '')) +
      `<line x1="200" y1="70" x2="200" y2="${s.vents === 'centre' ? 372 : 450}" stroke="rgba(0,0,0,.32)" stroke-width="1"/>` + (s.vents === 'centre' ? vent : '') +
      `<path d="M168,68 Q200,58 232,68 L228,86 Q200,78 172,86 Z" fill="url(#cfg-fab)"/><path d="M168,68 Q200,58 232,68 L228,86 Q200,78 172,86 Z" fill="rgba(0,0,0,.18)" stroke="rgba(0,0,0,.3)" stroke-width=".8"/>`;
  } else {
    const P = frontPanel(s, ry);
    extraDefs = `<clipPath id="cfg-pnl"><path d="${P}"/></clipPath>`;
    const shirt = `<path d="M168,64 L232,64 L236,386 L164,386 Z" fill="#f3f1ec"/><path d="M164,380 L236,380 L236,392 L164,392 Z" fill="url(#cfg-fab)"/><path d="M164,380 L236,380 L236,392 L164,392 Z" fill="rgba(0,0,0,.25)"/>` +
      half(`<path d="M171,68 L200,92 L187,114 L176,100 Z" fill="#fbfaf7" stroke="rgba(0,0,0,.16)" stroke-width=".8"/>`) +
      `<path d="M193,91 L207,91 L210,106 L205,${ry + 6} L195,${ry + 6} L190,106 Z" fill="#1e2a3a"/><path d="M193,89 L207,89 L205,104 L195,104 Z" fill="#26344a"/>` +
      `<path d="M173,64 Q200,56 227,64 Q200,72 173,64 Z" fill="url(#cfg-fab)"/><path d="M173,64 Q200,56 227,64 Q200,72 173,64 Z" fill="rgba(0,0,0,.35)"/>`;
    const vest = s.waistcoat === 'yes' ? `<path d="M178,118 L200,198 L222,118 L230,${ry + 8} L170,${ry + 8} Z" fill="url(#cfg-fab)"/><path d="M178,118 L200,198 L222,118 L230,${ry + 8} L170,${ry + 8} Z" fill="rgba(0,0,0,.08)" stroke="rgba(0,0,0,.3)" stroke-width=".8"/>` +
      [214, 236, 258, 280].filter((y) => y < ry - 6).map((y) => btn(200, y, 3, bfill)).join('') : '';
    const panel = `<path d="${P}" fill="url(#cfg-fab)"/><path d="${P}" fill="url(#cfg-side)"/><path d="${P}" fill="url(#cfg-down)" stroke="rgba(0,0,0,.25)" stroke-width=".8"/>` +
      `<path d="M150,214 Q147,300 151,362" fill="none" stroke="rgba(0,0,0,.18)" stroke-width=".9"/>` +
      `<g clip-path="url(#cfg-pnl)"><ellipse cx="150" cy="190" rx="46" ry="64" fill="url(#cfg-chest)"/>${fold('M104,170 Q122,236 118,300', .6)}${fold('M112,318 Q132,330 156,326', .35)}${fold('M180,330 Q186,380 178,440', .35)}</g>` + pocket(s);
    const lp = lapel(s, ry);
    const lap = `<path d="${lp}" fill="rgba(0,0,0,.5)" filter="url(#cfg-ao)" transform="translate(5 6)"/><path d="${lp}" fill="rgba(0,0,0,.4)" filter="url(#cfg-soft)" transform="translate(3 4)"/><path d="${lp}" fill="url(#cfg-fab)"/><path d="${lp}" fill="url(#cfg-lapel)" stroke="rgba(0,0,0,.32)" stroke-width=".9"/>` +
      `<path d="M181,76 L${s.lapel === 'shawl' ? '196' : '198'},${ry - 2}" stroke="rgba(255,255,255,.16)" stroke-width="1"/>`;
    const collar = s.lapel === 'shawl' ? '' : `<path d="M157,86 Q200,60 243,86 L222,79 Q200,70 178,79 Z" fill="url(#cfg-fab)"/><path d="M157,86 Q200,60 243,86 L222,79 Q200,70 178,79 Z" fill="rgba(0,0,0,.2)"/>`;
    const breast = s.breast === 'none' ? '' :
      `<g transform="rotate(-6 256 198)">` + (s.breast === 'square' ? `<path d="M238,195 L246,182 L252,190 L258,180 L266,194 Z" fill="#f3f1ec" stroke="rgba(0,0,0,.15)" stroke-width=".6"/>` : '') +
      `<rect x="236" y="194" width="40" height="7" fill="url(#cfg-fab)"/><rect x="236" y="194" width="40" height="7" fill="rgba(255,255,255,.06)" stroke="rgba(0,0,0,.4)" stroke-width=".8"/></g>`;
    const milanese = `<line x1="247" y1="134" x2="257" y2="138" stroke="rgba(0,0,0,.55)" stroke-width="1.4" stroke-linecap="round"/>`;
    body = shirt + vest + half(sleeve) + `<g>${panel}</g><g transform="${MIRROR}">${panel}</g>` + half(SHOULDER) + collar + half(lap) + breast + (s.lapel !== 'shawl' ? milanese : '') + buttons(s, ry, bfill);
  }
  const floor = `<ellipse cx="200" cy="762" rx="96" ry="7" fill="rgba(0,0,0,.12)" filter="url(#cfg-soft)"/>`;
  const bg = opts.bg === false ? '' : `<rect x="0" y="0" width="400" height="800" fill="url(#cfg-bg)"/>`;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${box}" role="img" aria-label="${opts.label || ''}" class="pct-suit">${defs(fab).replace('</defs>', extraDefs + '</defs>')}${bg}${floor}${half(shoe)}${half(trouser)}${body}</svg>`;
  const id = opts.id || 'cfg';
  return id === 'cfg' ? svg : svg.replace(/cfg-/g, id + '-');
}
