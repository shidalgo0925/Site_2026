"""Replace product-hero + flyer sections with unified solution-hero layout."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FLYER_FALLBACK = (
    "this.onerror=null;this.src='assets/images/logo-easytech-services.png';"
    "this.classList.add('solution-hero-fallback-img');"
)


def hero_block(cfg: dict) -> str:
    logo_class = "solution-hero-logo-img"
    if cfg.get("logo_contain"):
        logo_class += " solution-hero-logo-img--contain"

    soon = ""
    if cfg.get("soon"):
        soon = '              <span class="solution-hero-soon">Próximamente</span>\n'

    footnote = cfg.get("footnote")
    footnote_html = ""
    if footnote:
        footnote_html = f'              <p class="solution-hero-footnote">{footnote}</p>\n'

    actions = "\n".join(
        f'                <a href="{html.escape(a["href"], quote=True)}" class="{a["class"]}"'
        + (' target="_blank" rel="noopener noreferrer"' if a.get("external") else "")
        + f'>{html.escape(a["label"])}</a>'
        for a in cfg["actions"]
    )

    img_onerror = cfg.get("img_onerror", FLYER_FALLBACK)

    return f"""    <section class="solution-hero" aria-labelledby="{cfg["h1_id"]}">
      <div class="solution-hero-inner reveal">
        <div class="solution-hero-copy">
{soon}          <div class="solution-hero-logo-row">
            <img src="{html.escape(cfg["logo"], quote=True)}" alt="" width="88" height="88" class="{logo_class}" decoding="async" aria-hidden="true" />
            <div>
              <p class="solution-hero-wordmark">{html.escape(cfg["wordmark"])}</p>
              <p class="solution-hero-eyebrow">{html.escape(cfg["eyebrow"])}</p>
            </div>
          </div>
          <h1 id="{cfg["h1_id"]}" class="solution-hero-title">{html.escape(cfg["title"])}</h1>
          <p class="solution-hero-lede">{html.escape(cfg["lede"])}</p>
          <div class="solution-hero-actions">
{actions}
          </div>
{footnote_html}        </div>
        <div class="solution-hero-visual">
          <figure class="solution-hero-screenshot">
            <img src="{html.escape(cfg["flyer"], quote=True)}" alt="{html.escape(cfg["flyer_alt"])}" width="1200" height="1697" loading="eager" decoding="async" onerror="{img_onerror}">
          </figure>
        </div>
      </div>
    </section>
"""


PAGES: dict[str, dict] = {
    "facturacion-electronica.html": {
        "h1_id": "fe-hero-h1",
        "logo": "assets/images/logo-easytech-services.png",
        "wordmark": "Facturación Electrónica Panamá",
        "eyebrow": "Solución · Panamá",
        "title": "Cumpla con la DGI y automatice su proceso de facturación",
        "lede": (
            "La Facturación Electrónica Panamá ayuda a empresas, comercios y profesionales "
            "a emitir documentos fiscales autorizados por la DGI, con cumplimiento normativo, "
            "seguridad y eficiencia operativa."
        ),
        "actions": [
            {
                "href": "https://wa.me/50766884938?text=Quiero%20informaci%C3%B3n%20sobre%20Facturaci%C3%B3n%20Electr%C3%B3nica%20Panam%C3%A1%20con%20EasyTech",
                "class": "btn btn-solution-primary",
                "label": "Solicitar información",
                "external": True,
            },
            {"href": "agenda.html", "class": "btn btn-solution-ghost", "label": "Agendar cita"},
        ],
        "footnote": '¿Implementación o integración? <a href="contacto.html">Contacto EasyTech</a> · <a href="agenda.html">Agendar cita</a>',
        "flyer": "assets/images/flyers/facturacion-electronica.png",
        "flyer_alt": "Flyer Facturación Electrónica Panamá — cumplimiento DGI e integración empresarial",
        "remove_flyer_section": True,
        "keep_after_hero": True,
    },
    "soluciones.html": {
        "h1_id": "odoo-hero-h1",
        "logo": "assets/images/logo-odoo-official.svg",
        "logo_contain": True,
        "wordmark": "Easy Odoo",
        "eyebrow": "Solución · Prioridad comercial",
        "title": "Implementamos Odoo para tu empresa",
        "lede": (
            "El ERP open source #1 del mundo para gestionar y automatizar todos los procesos "
            "de tu negocio en una sola plataforma. Easy Technology Services implementa, "
            "configura y acompaña la adopción por etapas."
        ),
        "actions": [
            {
                "href": "https://wa.me/50766884938?text=Quiero%20informaci%C3%B3n%20sobre%20Easy%20Odoo%20(ERP%20EasyTech)",
                "class": "btn btn-solution-primary",
                "label": "Solicitar demo ERP",
                "external": True,
            },
            {"href": "agenda.html", "class": "btn btn-solution-ghost", "label": "Agendar cita"},
        ],
        "footnote": '¿Diagnóstico o implementación? <a href="contacto.html">Contacto EasyTech</a> · <a href="agenda.html">Agendar cita</a>',
        "flyer": "assets/images/flyers/easy-odoo.png",
        "flyer_alt": "Flyer Easy Odoo — ERP EasyTech",
        "remove_flyer_section": True,
        "keep_after_hero": True,
    },
    "eclassone.html": {
        "h1_id": "eclassone-hero-h1",
        "logo": "assets/images/logo-easytech-services.png",
        "wordmark": "EClassOne",
        "eyebrow": "Plataforma EasyTech",
        "title": "Formación en línea con EClassOne",
        "lede": "Cursos, contenidos y seguimiento en una plataforma pensada para capacitar equipos y clientes.",
        "actions": [
            {
                "href": "https://wa.me/50766884938?text=Quiero%20una%20demo%20de%20EClassOne%20%E2%80%94%20EasyTech",
                "class": "btn btn-solution-primary",
                "label": "Solicitar demo",
                "external": True,
            },
            {"href": "agenda.html", "class": "btn btn-solution-ghost", "label": "Agendar cita"},
        ],
        "footnote": '¿Demo guiada? <a href="contacto.html">Contacto EasyTech</a> · <a href="agenda.html">Agendar cita</a>',
        "flyer": "assets/images/eclassone/eclassone-hero.png",
        "flyer_alt": "EClassOne — plataforma educativa con IA",
    },
    "ethesisone.html": {
        "h1_id": "ethesisone-hero-h1",
        "logo": "assets/images/logo-easytech-services.png",
        "wordmark": "EThesisOne",
        "eyebrow": "Plataforma EasyTech",
        "title": "Tesis y documentos académicos con EThesisOne",
        "lede": "Organizá revisiones, entregables y seguimiento académico en un solo flujo digital.",
        "actions": [
            {
                "href": "https://wa.me/50766884938?text=Quiero%20una%20demo%20de%20EThesisOne%20%E2%80%94%20EasyTech",
                "class": "btn btn-solution-primary",
                "label": "Solicitar demo",
                "external": True,
            },
            {"href": "agenda.html", "class": "btn btn-solution-ghost", "label": "Agendar cita"},
        ],
        "footnote": '¿Demo guiada? <a href="contacto.html">Contacto EasyTech</a> · <a href="agenda.html">Agendar cita</a>',
        "flyer": "assets/images/flyers/ethesisone.png",
        "flyer_alt": "Flyer EThesisOne — Tesis y documentos",
    },
    "eposone.html": {
        "h1_id": "eposone-hero-h1",
        "logo": "assets/images/logo-easytech-services.png",
        "wordmark": "EPOSOne",
        "eyebrow": "Plataforma EasyTech",
        "title": "Punto de venta moderno con EPOSOne",
        "lede": "Ventas en mostrador enlazadas a inventario, facturación y reportes de tu operación.",
        "actions": [
            {
                "href": "https://wa.me/50766884938?text=Quiero%20una%20demo%20de%20EPOSOne%20%E2%80%94%20EasyTech",
                "class": "btn btn-solution-primary",
                "label": "Solicitar demo",
                "external": True,
            },
            {"href": "agenda.html", "class": "btn btn-solution-ghost", "label": "Agendar cita"},
        ],
        "footnote": '¿Demo guiada? <a href="contacto.html">Contacto EasyTech</a> · <a href="agenda.html">Agendar cita</a>',
        "flyer": "assets/images/flyers/eposone.png",
        "flyer_alt": "Flyer EPOSOne — Punto de venta",
    },
    "epayroll.html": {
        "h1_id": "epayroll-hero-h1",
        "logo": "assets/images/logo-easytech-services.png",
        "wordmark": "EPayRoll",
        "eyebrow": "Plataforma EasyTech",
        "soon": True,
        "title": "Nómina y planilla con EPayRoll",
        "lede": "Estamos preparando la plataforma de planilla del ecosistema EasyTech. Escribinos si querés ser avisado.",
        "actions": [
            {
                "href": "mailto:easytechservices25@gmail.com?subject=Inter%C3%A9s%20en%20EPayRoll",
                "class": "btn btn-solution-primary",
                "label": "Avísame por email",
                "external": True,
            },
            {
                "href": "https://wa.me/50766884938?text=Inter%C3%A9s%20en%20EPayRoll%20%E2%80%94%20EasyTech",
                "class": "btn btn-solution-ghost",
                "label": "WhatsApp",
                "external": True,
            },
        ],
        "flyer": "assets/images/flyers/epayroll.png",
        "flyer_alt": "Flyer EPayRoll — Nómina",
    },
    "desarrollo-software.html": {
        "h1_id": "dev-hero-h1",
        "logo": "assets/images/logo-easytech-services.png",
        "wordmark": "Desarrollo de Software",
        "eyebrow": "Servicios profesionales",
        "title": "Desarrollo de software a medida",
        "lede": "Construimos integraciones, portales y automatizaciones conectadas a tu operación EasyTech.",
        "actions": [
            {
                "href": "https://wa.me/50766884938?text=Consulta%20sobre%20desarrollo%20de%20software%20con%20EasyTech",
                "class": "btn btn-solution-primary",
                "label": "WhatsApp",
                "external": True,
            },
            {"href": "agenda.html", "class": "btn btn-solution-ghost", "label": "Agendar cita"},
        ],
        "footnote": '¿Proyecto a medida? <a href="contacto.html">Contacto EasyTech</a> · <a href="agenda.html">Agendar cita</a>',
        "flyer": "assets/images/flyers/desarrollo-software.png",
        "flyer_alt": "Flyer Desarrollo de Software",
    },
    "consultoria-ti.html": {
        "h1_id": "consultoria-hero-h1",
        "logo": "assets/images/logo-easytech-services.png",
        "wordmark": "Consultoría TI",
        "eyebrow": "Servicios profesionales",
        "title": "Consultoría TI para digitalizar tu operación",
        "lede": "Diagnóstico, roadmap e implementación de plataformas EasyTech según tu etapa de negocio.",
        "actions": [
            {
                "href": "https://wa.me/50766884938?text=Consulta%20sobre%20consultor%C3%ADa%20TI%20con%20EasyTech",
                "class": "btn btn-solution-primary",
                "label": "WhatsApp",
                "external": True,
            },
            {"href": "agenda.html", "class": "btn btn-solution-ghost", "label": "Agendar cita"},
        ],
        "footnote": '¿Diagnóstico inicial? <a href="contacto.html">Contacto EasyTech</a> · <a href="agenda.html">Agendar cita</a>',
        "flyer": "assets/images/flyers/consultoria-ti.png",
        "flyer_alt": "Flyer Consultoría TI",
    },
}

PRODUCT_HERO_RE = re.compile(
    r"    <section class=\"product-hero\".*?</section>\n\n",
    re.DOTALL,
)

FLYER_SECTION_RE = re.compile(
    r"    <section class=\"section section--tight\" aria-labelledby=\"flyer-heading\">.*?"
    r"<p class=\"pillars-lede reveal product-flyer-fallback\" hidden>.*?</p>\n    </section>\n\n",
    re.DOTALL,
)


def patch_file(name: str, cfg: dict) -> None:
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    new_hero = hero_block(cfg) + "\n"

    if "product-hero" not in text:
        print(f"skip {name}: no product-hero")
        return

    text = PRODUCT_HERO_RE.sub(new_hero, text, count=1)
    if cfg.get("remove_flyer_section"):
        text = FLYER_SECTION_RE.sub("", text, count=1)
    else:
        text = FLYER_SECTION_RE.sub("", text, count=1)

    path.write_text(text, encoding="utf-8")
    print(f"patched {name}")


def main() -> None:
    for name, cfg in PAGES.items():
        patch_file(name, cfg)


if __name__ == "__main__":
    main()
