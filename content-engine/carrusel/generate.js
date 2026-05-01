/**
 * CreActive Studio — Carrusel Generator (HTML/CSS + Puppeteer)
 *
 * Uso:  node generate.js [ideas/mi-brief.json]
 * Out:  slides/slide-01-hero.html   (previsualizable en browser)
 *       output/slide-01-hero.png    (exportacion final)
 *
 * El brief puede incluir "template_set": "tutorial" (default: "tutorial").
 * Los templates se leen desde templates/{template_set}/{layout}.html
 *
 * Sintaxis de acento: "Texto *palabras* mas texto"  →  color de acento del layout
 */

import puppeteer from 'puppeteer';
import { readFileSync, writeFileSync, existsSync, mkdirSync, rmSync } from 'fs';
import { join, dirname, basename } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ─── Normalización del schema ─────────────────────────────────────────────────
// Acepta tanto el schema viejo (layout, texto, cta, nota, template_set)
// como el nuevo (tipo, headline, boton, secundario, template, palabras_clave, codigo[])

function normalizeSlide(slide) {
  const s = { ...slide };

  // tipo → layout
  if (!s.layout && s.tipo) s.layout = s.tipo;

  // palabras_clave → inyecta *markers* en headline/titulo
  const kw = s.palabras_clave || [];
  if (kw.length) {
    const wrap = (text) => {
      if (!text) return text;
      let out = text;
      for (const word of kw) {
        // reemplaza la palabra exacta (case-sensitive) con *word*
        out = out.replace(new RegExp(`(${word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'g'), '*$1*');
      }
      return out;
    };
    if (s.headline) s.headline = wrap(s.headline);
    if (s.titulo)   s.titulo   = wrap(s.titulo);
  }

  // CTA: headline → texto, boton → cta, secundario → nota
  if (s.layout === 'cta') {
    if (!s.texto && s.headline) s.texto = s.headline;
    if (!s.cta   && s.boton)   s.cta   = s.boton;
    if (!s.nota  && s.secundario) s.nota = s.secundario;
  }

  // codigo array → string
  if (Array.isArray(s.codigo)) s.codigo = s.codigo.join('\n');

  return s;
}

function normalizeBrief(brief) {
  return {
    ...brief,
    template_set: brief.template_set || brief.template || 'tutorial',
    width:  brief.width  || 1080,
    height: brief.height || 1350,
    slides: (brief.slides || []).map(normalizeSlide),
  };
}

// ─── Utilidades de texto ──────────────────────────────────────────────────────

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// "Hola *mundo* esto" → "Hola <span class="accent">mundo</span> esto"
function parseAccent(text) {
  return escHtml(text).replace(/\*([^*]+)\*/g, '<span class="accent">$1</span>');
}

// ─── Builders de fragmentos HTML ──────────────────────────────────────────────

function buildEtiqueta(etiqueta) {
  if (!etiqueta) return '';
  return `<div class="etiqueta">${escHtml(etiqueta.toUpperCase())}</div>`;
}

function buildSubheadline(text) {
  if (!text) return '';
  return `<div class="subheadline">${escHtml(text)}</div>`;
}

function buildNota(text) {
  if (!text) return '';
  return `<div class="nota">${escHtml(text)}</div>`;
}

function buildAnalysis(text) {
  if (!text) return '';
  return `<div class="analysis">${escHtml(text)}</div>`;
}

// ─── Mockup builders ──────────────────────────────────────────────────────────

function buildMockup(type) {
  if (!type || type === 'none') return { html: '', cls: '' };

  const cls = 'has-mockup';

  if (type === 'dashboard') {
    const html = `
<div class="mockup">
  <div class="mockup-dashboard">
    <div class="md-sidebar">
      <div class="md-dots">
        <div class="md-dot red"></div><div class="md-dot amber"></div><div class="md-dot green"></div>
      </div>
      <div class="md-sidebar-label">Performance</div>
    </div>
    <div class="md-metrics">
      <div class="md-metric"><div class="md-num accent">+47%</div><div class="md-lbl">Eficiencia</div></div>
      <div class="md-metric"><div class="md-num">3.2x</div><div class="md-lbl">Velocidad</div></div>
      <div class="md-metric"><div class="md-num accent">$0</div><div class="md-lbl">Overhead</div></div>
      <div class="md-metric"><div class="md-num">24h</div><div class="md-lbl">Ciclo</div></div>
    </div>
    <div class="md-chart">
      <div class="db-bar" style="height:38%"></div>
      <div class="db-bar" style="height:52%"></div>
      <div class="db-bar" style="height:47%"></div>
      <div class="db-bar hi" style="height:78%"></div>
      <div class="db-bar hi" style="height:90%"></div>
      <div class="db-bar hi" style="height:85%"></div>
    </div>
  </div>
</div>`;
    return { html, cls };
  }

  if (type === 'agent') {
    const html = `
<div class="mockup">
  <div class="mockup-agent-h">
    <div class="ma-header-h">
      <div class="ma-avatar-h">IA</div>
      <div class="ma-title-h">Agente IA</div>
      <div class="ma-status-h">● activo</div>
    </div>
    <div class="ma-messages">
      <div class="ma-bubble ma-user">¿Cuántos clientes perdimos este mes?</div>
      <div class="ma-bubble ma-ai">Analicé 90 días. Churn 4.2%. Causa: seguimiento tardío.</div>
      <div class="ma-bubble ma-user">¿Qué hacemos?</div>
    </div>
  </div>
</div>`;
    return { html, cls };
  }

  return { html: '', cls: '' };
}

function buildBullets(bullets = []) {
  return bullets
    .slice(0, 4)
    .map((b, i) => `
    <div class="bullet">
      <div class="bullet-icon">${i + 1}</div>
      <div class="bullet-text">${escHtml(b)}</div>
    </div>`)
    .join('\n');
}

// Resaltado de sintaxis para shell/CLI
function highlightCode(codigo) {
  return codigo
    .split('\n')
    .map((line) => {
      if (line.trim() === '') return '<span class="code-plain"> </span>';

      // Comentario: # ...
      if (line.trim().startsWith('#')) {
        return `<span class="code-comment">${escHtml(line)}</span>`;
      }

      // Prompt REPL: > ...
      if (line.trim().startsWith('>')) {
        const rest = line.replace(/^\s*>/, '');
        return `<span class="code-repl">&gt;</span><span class="code-plain">${escHtml(rest)}</span>`;
      }

      // Comando normal: tokenizar
      let html = '';
      let firstToken = true;
      const tokens = line.split(/(\s+)/);

      for (const token of tokens) {
        if (/^\s+$/.test(token)) { html += token; continue; }

        if (firstToken) {
          html += `<span class="code-cmd">${escHtml(token)}</span>`;
          firstToken = false;
          continue;
        }
        if (/^--?[\w][\w-]*$/.test(token)) {
          html += `<span class="code-flag">${escHtml(token)}</span>`; continue;
        }
        if (/@|\//.test(token) && !/[;&|]/.test(token)) {
          html += `<span class="code-pkg">${escHtml(token)}</span>`; continue;
        }
        if (/^["'].*["']$/.test(token)) {
          html += `<span class="code-string">${escHtml(token)}</span>`; continue;
        }
        if (/^[&|;]+$/.test(token)) {
          html += `<span class="code-comment">${escHtml(token)}</span>`; continue;
        }
        html += `<span class="code-plain">${escHtml(token)}</span>`;
      }

      return html;
    })
    .join('\n');
}

// ─── Template engine ──────────────────────────────────────────────────────────

function fillTemplate(layoutName, templateSet, vars) {
  const tplPath = join(__dirname, 'templates', templateSet, `${layoutName}.html`);
  if (!existsSync(tplPath)) {
    throw new Error(`Template no encontrado: templates/${templateSet}/${layoutName}.html`);
  }
  let html = readFileSync(tplPath, 'utf-8');
  for (const [key, value] of Object.entries(vars)) {
    html = html.replaceAll(`{{${key}}}`, value ?? '');
  }
  return html;
}

// ─── Builders por layout ──────────────────────────────────────────────────────

function buildHero(slide, num, set) {
  return fillTemplate('hero', set, {
    slide_num:        num,
    etiqueta_html:    buildEtiqueta(slide.etiqueta),
    headline_html:    parseAccent(slide.headline || ''),
    subheadline_html: buildSubheadline(slide.subheadline),
  });
}

function buildContent(slide, num, set) {
  const { html: mockup_html, cls: mockup_class } = buildMockup(slide.mockup);
  return fillTemplate('content', set, {
    slide_num:      num,
    etiqueta:       (slide.etiqueta || '').toUpperCase(),
    headline_html:  parseAccent(slide.titulo || ''),
    analysis_html:  buildAnalysis(slide.analysis),
    bullets_html:   buildBullets(slide.bullets),
    mockup_html,
    mockup_class,
  });
}

function buildContentLight(slide, num, set) {
  const { html: mockup_html, cls: mockup_class } = buildMockup(slide.mockup);
  return fillTemplate('content-light', set, {
    slide_num:      num,
    etiqueta:       (slide.etiqueta || '').toUpperCase(),
    headline_html:  parseAccent(slide.titulo || ''),
    analysis_html:  buildAnalysis(slide.analysis),
    bullets_html:   buildBullets(slide.bullets),
    mockup_html,
    mockup_class,
  });
}

function buildCode(slide, num, set) {
  return fillTemplate('code', set, {
    slide_num:   num,
    etiqueta:    (slide.etiqueta || 'Código').toUpperCase(),
    codigo_html: highlightCode(slide.codigo || ''),
    explicacion: escHtml(slide.explicacion || ''),
  });
}

function buildCta(slide, num, set) {
  return fillTemplate('cta', set, {
    slide_num:     num,
    headline_html: parseAccent(slide.texto || ''),
    cta:           escHtml(slide.cta || ''),
    nota_html:     buildNota(slide.nota),
  });
}

function buildCtaLight(slide, num, set) {
  return fillTemplate('cta-light', set, {
    slide_num:     num,
    headline_html: parseAccent(slide.texto || ''),
    cta:           escHtml(slide.cta || ''),
    nota_html:     buildNota(slide.nota),
  });
}

// ─── Layouts adicionales (template set "minimalista" / "easyway" / clientes) ──

function brandPath(set) {
  const sub = (set === 'minimalista' || set === 'tutorial') ? '' : `${set}/`;
  return `public/brand/${sub}`;
}

function buildHeroDark(slide, num, set) {
  const __dirname_resolved = new URL('.', import.meta.url).pathname;
  return fillTemplate('hero-dark', set, {
    slide_num:        num,
    headshot_path:    `file://${__dirname_resolved}${brandPath(set)}headshot.jpg`,
    etiqueta_html:    buildEtiqueta(slide.etiqueta),
    headline_html:    parseAccent(slide.headline || ''),
    subheadline_html: buildSubheadline(slide.subheadline),
  });
}

function buildHeroLight(slide, num, set) {
  const __dirname_resolved = new URL('.', import.meta.url).pathname;
  return fillTemplate('hero-light', set, {
    slide_num:        num,
    headshot_path:    `file://${__dirname_resolved}${brandPath(set)}headshot.jpg`,
    etiqueta_html:    buildEtiqueta(slide.etiqueta),
    headline_html:    parseAccent(slide.headline || ''),
    subheadline_html: buildSubheadline(slide.subheadline),
  });
}

function buildQuote(slide, num, set) {
  const __dirname_resolved = new URL('.', import.meta.url).pathname;
  return fillTemplate('quote', set, {
    headshot_path: `file://${__dirname_resolved}${brandPath(set)}headshot.jpg`,
    slide_num:  num,
    quote_html: parseAccent(slide.quote || slide.headline || ''),
    author:     escHtml(slide.author || slide.etiqueta || ''),
  });
}

function buildStat(slide, num, set) {
  return fillTemplate('stat', set, {
    slide_num: num,
    etiqueta:  (slide.etiqueta || '').toUpperCase(),
    number:    escHtml(slide.number || ''),
    label:     escHtml(slide.label || slide.titulo || ''),
    context:   escHtml(slide.context || slide.subheadline || ''),
  });
}

// ─── Builders pumpalcerro-ads ─────────────────────────────────────────────────

function buildPhotoOverlay(slide, num, set) {
  const bgImage = slide.bg_image
    ? `file://${encodeURI(slide.bg_image)}`
    : '';
  return fillTemplate('photo-overlay', set, {
    slide_num:     num,
    bg_image:      bgImage,
    headline_html: parseAccent(slide.headline || ''),
    subline_html:  slide.subline ? `<div class="subline">${parseAccent(slide.subline)}</div>` : '',
    badge_html:    slide.badge ? `<div class="badge">${escHtml(slide.badge)}</div>` : '',
  });
}

function buildQuotePhoto(slide, num, set) {
  const bgImage = slide.bg_image
    ? `file://${encodeURI(slide.bg_image)}`
    : '';
  return fillTemplate('quote-photo', set, {
    slide_num:  num,
    bg_image:   bgImage,
    quote_html: parseAccent(slide.quote || slide.headline || ''),
    author:     escHtml(slide.author || ''),
  });
}

function buildInfoCard(slide, num, set) {
  return fillTemplate('info-card', set, {
    slide_num:     num,
    emoji:         slide.emoji || '',
    headline_html: parseAccent(slide.headline || ''),
    subline_html:  slide.subline ? `<div class="subline">${parseAccent(slide.subline)}</div>` : '',
    bg_color:      slide.bg_color || '#fefaf6',
    text_color:    slide.text_color || '#1c1717',
  });
}

function buildCtaBrand(slide, num, set) {
  return fillTemplate('cta-brand', set, {
    slide_num:     num,
    headline_html: parseAccent(slide.headline || slide.texto || ''),
    subline_html:  slide.subline ? `<div class="subline">${escHtml(slide.subline)}</div>` : '',
    bg_color:      slide.bg_color || '#fefaf6',
  });
}

const BUILDERS = {
  hero:           buildHero,
  'hero-dark':    buildHeroDark,
  'hero-light':   buildHeroLight,
  quote:          buildQuote,
  stat:           buildStat,
  content:         buildContent,
  'content-light': buildContentLight,
  code:           buildCode,
  cta:            buildCta,
  'cta-light':    buildCtaLight,
  'photo-overlay': buildPhotoOverlay,
  'quote-photo':   buildQuotePhoto,
  'info-card':     buildInfoCard,
  'cta-brand':     buildCtaBrand,
};

// ─── Generador por slide ──────────────────────────────────────────────────────

async function generateSlide(slide, index, total, browser, templateSet, carruselSlug, width, height) {
  const builderFn = BUILDERS[slide.layout];
  if (!builderFn) {
    throw new Error(`Layout desconocido: "${slide.layout}". Validos: hero | hero-dark | hero-light | quote | stat | content | code | cta`);
  }

  const num      = String(index + 1).padStart(2, '0');
  const filename = `slide-${num}-${slide.layout}`;

  // 1. Generar HTML → slides/{carruselSlug}/
  let html = builderFn(slide, num, templateSet);
  // Inject progress vars
  html = html.replaceAll('{{slide_idx}}', String(index + 1));
  html = html.replaceAll('{{slide_total}}', String(total));
  html = html.replaceAll('{{progress_pct}}', String(Math.round((index + 1) / total * 100)));
  const htmlPath = join(__dirname, 'slides', carruselSlug, `${filename}.html`);
  if (existsSync(htmlPath)) rmSync(htmlPath);
  writeFileSync(htmlPath, html, 'utf-8');

  // 2. Puppeteer → output/{carruselSlug}/
  const pngPath = join(__dirname, 'output', carruselSlug, `${filename}.png`);
  if (existsSync(pngPath)) rmSync(pngPath);

  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);

  await page.screenshot({ path: pngPath, type: 'png', clip: { x: 0, y: 0, width, height } });
  await page.close();

  console.log(`  v  ${filename}.png`);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const briefPath = process.argv[2]
    ? join(process.cwd(), process.argv[2])
    : join(__dirname, 'ideas/test.json');

  if (!existsSync(briefPath)) {
    console.error(`\nX  Brief no encontrado: ${briefPath}\n`);
    process.exit(1);
  }

  const brief        = normalizeBrief(JSON.parse(readFileSync(briefPath, 'utf-8')));
  const templateSet  = brief.template_set;
  const carruselSlug = brief.slug || basename(briefPath, '.json');

  // Crear carpetas de salida si no existen
  mkdirSync(join(__dirname, 'slides', carruselSlug), { recursive: true });
  mkdirSync(join(__dirname, 'output', carruselSlug), { recursive: true });

  console.log(`\n>  "${brief.titulo}"`);
  console.log(`   set: ${templateSet}  |  ${brief.slides.length} slides  |  ${carruselSlug}\n`);

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  try {
    for (let i = 0; i < brief.slides.length; i++) {
      await generateSlide(brief.slides[i], i, brief.slides.length, browser, templateSet, carruselSlug, brief.width, brief.height);
    }
  } finally {
    await browser.close();
  }

  console.log(`\nOK  slides/${carruselSlug}/   output/${carruselSlug}/\n`);
}

main().catch((err) => {
  console.error('\nX', err.message);
  process.exit(1);
});
