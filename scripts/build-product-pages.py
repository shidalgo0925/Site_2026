"""Create product pages and inline shared chrome."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "assets" / "partials"
FLYERS_SRC = ROOT / "imagenes"
FLYERS_DEST = ROOT / "assets" / "images" / "flyers"

PRODUCTS = [
    {
        "slug": "facturacion-electronica",
        "title": "Facturación Electrónica Panamá",
        "meta": "Facturación electrónica en Panamá con EasyTech. Cumplimiento fiscal, emisión y acompañamiento.",
        "eyebrow": "Solución EasyTech",
        "h1": "Facturación electrónica lista para operar en Panamá",
        "lede": "Implementamos emisión electrónica alineada a tu operación comercial, con soporte del ecosistema EasyTech.",
        "primary": ("WhatsApp", "https://wa.me/50766884938?text=Quiero%20informaci%C3%B3n%20sobre%20Facturaci%C3%B3n%20Electr%C3%B3nica%20Panam%C3%A1%20con%20EasyTech"),
        "secondary": ("Agendar cita", "agenda.html"),
        "soon": False,
    },
    {
        "slug": "eclassone",
        "title": "EClassOne — Formación en línea",
        "meta": "EClassOne: plataforma de formación en línea del ecosistema EasyTech.",
        "eyebrow": "Plataforma EasyTech",
        "h1": "Formación en línea con EClassOne",
        "lede": "Cursos, contenidos y seguimiento en una plataforma pensada para capacitar equipos y clientes.",
        "primary": ("Solicitar demo", "https://wa.me/50766884938?text=Quiero%20una%20demo%20de%20EClassOne%20%E2%80%94%20EasyTech"),
        "secondary": ("Agendar cita", "agenda.html"),
        "soon": False,
    },
    {
        "slug": "ethesisone",
        "title": "EThesisOne — Tesis y documentos",
        "meta": "EThesisOne: gestión de tesis y documentos académicos. Plataforma EasyTech.",
        "eyebrow": "Plataforma EasyTech",
        "h1": "Tesis y documentos académicos con EThesisOne",
        "lede": "Organizá revisiones, entregables y seguimiento académico en un solo flujo digital.",
        "primary": ("Solicitar demo", "https://wa.me/50766884938?text=Quiero%20una%20demo%20de%20EThesisOne%20%E2%80%94%20EasyTech"),
        "secondary": ("Agendar cita", "agenda.html"),
        "soon": False,
    },
    {
        "slug": "eposone",
        "title": "EPOSOne — Punto de venta",
        "meta": "EPOSOne: punto de venta conectado al ecosistema EasyTech.",
        "eyebrow": "Plataforma EasyTech",
        "h1": "Punto de venta moderno con EPOSOne",
        "lede": "Ventas en mostrador enlazadas a inventario, facturación y reportes de tu operación.",
        "primary": ("Solicitar demo", "https://wa.me/50766884938?text=Quiero%20una%20demo%20de%20EPOSOne%20%E2%80%94%20EasyTech"),
        "secondary": ("Agendar cita", "agenda.html"),
        "soon": False,
    },
    {
        "slug": "epayroll",
        "title": "EPayRoll — Nómina",
        "meta": "EPayRoll: nómina y planilla del ecosistema EasyTech. Próximamente.",
        "eyebrow": "Plataforma EasyTech",
        "h1": "Nómina y planilla con EPayRoll",
        "lede": "Estamos preparando la plataforma de planilla del ecosistema EasyTech. Escribinos si querés ser avisado.",
        "primary": ("Avísame por email", "mailto:easytechservices25@gmail.com?subject=Inter%C3%A9s%20en%20EPayRoll"),
        "secondary": ("WhatsApp", "https://wa.me/50766884938?text=Inter%C3%A9s%20en%20EPayRoll%20%E2%80%94%20EasyTech"),
        "soon": True,
    },
    {
        "slug": "desarrollo-software",
        "title": "Desarrollo de Software",
        "meta": "Desarrollo de software a medida con EasyTech Services, Panamá.",
        "eyebrow": "Servicios profesionales",
        "h1": "Desarrollo de software a medida",
        "lede": "Construimos integraciones, portales y automatizaciones conectadas a tu operación EasyTech.",
        "primary": ("WhatsApp", "https://wa.me/50766884938?text=Consulta%20sobre%20desarrollo%20de%20software%20con%20EasyTech"),
        "secondary": ("Agendar cita", "agenda.html"),
        "soon": False,
    },
    {
        "slug": "consultoria-ti",
        "title": "Consultoría TI",
        "meta": "Consultoría TI e implementación con EasyTech Services, Panamá.",
        "eyebrow": "Servicios profesionales",
        "h1": "Consultoría TI para digitalizar tu operación",
        "lede": "Diagnóstico, roadmap e implementación de plataformas EasyTech según tu etapa de negocio.",
        "primary": ("WhatsApp", "https://wa.me/50766884938?text=Consulta%20sobre%20consultor%C3%ADa%20TI%20con%20EasyTech"),
        "secondary": ("Agendar cita", "agenda.html"),
        "soon": False,
    },
]

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{meta}">
  <title>{title} | EasyTech</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/main.css">
  <link rel="stylesheet" href="assets/css/ramp-theme.css">
</head>
<body class="ramp page-{slug}">
  <div id="site-chrome-header" class="site-chrome-slot"></div>

  <main id="page-main" class="page-surface">
    <section class="product-hero" aria-labelledby="product-h1">
      <div class="product-hero-inner reveal">
        {soon_badge}
        <p class="product-hero-eyebrow">{eyebrow}</p>
        <h1 id="product-h1" class="product-hero-title">{h1}</h1>
        <p class="product-hero-lede">{lede}</p>
        <div class="product-hero-actions">
          <a href="{primary_href}" class="btn btn-primary"{primary_external}>{primary_label}</a>
          <a href="{secondary_href}" class="btn btn-ghost"{secondary_external}>{secondary_label}</a>
        </div>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="flyer-heading">
      <h2 id="flyer-heading" class="section-title reveal">Material comercial</h2>
      <figure class="product-flyer reveal">
        <img src="assets/images/flyers/{slug}.png" alt="Flyer {title}" width="1200" height="1697" loading="lazy" decoding="async" onerror="this.closest('.product-flyer').classList.add('product-flyer--missing');this.remove();">
      </figure>
      <p class="pillars-lede reveal product-flyer-fallback" hidden>Flyer disponible próximamente. <a href="contacto.html">Contactanos</a> para recibir el material.</p>
    </section>

    <section class="section cta" aria-labelledby="cta-h2">
      <h2 id="cta-h2" class="reveal">¿Seguimos por WhatsApp o agenda?</h2>
      <p class="reveal">El equipo EasyTech te orienta sobre {title}.</p>
      <div class="cta-actions">
        <a href="{primary_href}" class="btn btn-primary reveal"{primary_external}>{primary_label}</a>
        <a href="agenda.html" class="btn btn-ghost reveal">Agendar cita</a>
        <a href="contacto.html" class="btn btn-ghost reveal">Contacto</a>
      </div>
    </section>
  </main>

  <div id="site-chrome-footer" class="site-chrome-slot"></div>

  <script src="assets/js/main.js"></script>
  <script src="assets/js/page-transitions.js"></script>
</body>
</html>
"""


def external_attrs(href: str) -> str:
    if href.startswith("http") or href.startswith("mailto:"):
        return ' target="_blank" rel="noopener noreferrer"'
    return ""


def copy_flyers() -> None:
    FLYERS_DEST.mkdir(parents=True, exist_ok=True)
    if not FLYERS_SRC.is_dir():
        return
    aliases = {
        "facturacion-electronica": ["facturacion", "factura", "electronica", "fe"],
        "eclassone": ["eclass", "classone"],
        "ethesisone": ["ethesis", "thesis"],
        "eposone": ["epos", "pos"],
        "epayroll": ["epayroll", "payroll", "nomina", "planilla"],
        "desarrollo-software": ["desarrollo", "software", "dev"],
        "consultoria-ti": ["consultoria", "consultoría", "ti"],
        "easynodeone": ["nodeone", "easynode"],
        "econverso": ["converso"],
        "easy-odoo": ["odoo", "erp"],
    }
    for path in FLYERS_SRC.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        name = path.stem.lower()
        slug = None
        for key, keys in aliases.items():
            if key in name or any(k in name for k in keys):
                slug = key
                break
        if not slug:
            slug = re.sub(r"[^a-z0-9]+", "-", name).strip("-")
        dest = FLYERS_DEST / f"{slug}.png"
        shutil.copy2(path, dest)
        print("flyer", path.name, "->", dest.name)


def render_product(p: dict) -> str:
    return PAGE_TEMPLATE.format(
        slug=p["slug"],
        title=p["title"],
        meta=p["meta"],
        eyebrow=p["eyebrow"],
        h1=p["h1"],
        lede=p["lede"],
        primary_label=p["primary"][0],
        primary_href=p["primary"][1],
        primary_external=external_attrs(p["primary"][1]),
        secondary_label=p["secondary"][0],
        secondary_href=p["secondary"][1],
        secondary_external=external_attrs(p["secondary"][1]),
        soon_badge='<p class="product-soon-badge">Próximamente</p>' if p["soon"] else "",
    )


def inline_chrome(path: Path, header: str, footer: str) -> None:
    text = path.read_text(encoding="utf-8")
    slot_h = '  <div id="site-chrome-header" class="site-chrome-slot"></div>\n'
    slot_f = '  <div id="site-chrome-footer" class="site-chrome-slot"></div>\n'

    def indent_block(block: str) -> str:
        return "\n".join("  " + line if line else line for line in block.strip().splitlines()) + "\n"

    if slot_h in text:
        text = text.replace(slot_h, indent_block(header), 1)
    if slot_f in text:
        text = text.replace(slot_f, indent_block(footer), 1)
    text = text.replace('  <script src="assets/js/site-chrome.js"></script>\n', "")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    copy_flyers()
    for p in PRODUCTS:
        out = ROOT / f"{p['slug']}.html"
        out.write_text(render_product(p), encoding="utf-8")
        print("page", out.name)

    header = (PARTIALS / "header.html").read_text(encoding="utf-8")
    footer = (PARTIALS / "footer.html").read_text(encoding="utf-8")
    for path in sorted(ROOT.glob("*.html")):
        inline_chrome(path, header, footer)
        print("inlined", path.name)


if __name__ == "__main__":
    main()
