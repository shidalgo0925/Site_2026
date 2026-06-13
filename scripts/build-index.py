"""Build index.html from home partials, ecosystem catalog JSON, and shared chrome."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "assets" / "partials"
HOME = PARTIALS / "home"
CATALOG = ROOT / "assets" / "data" / "ecosystem-catalog.json"
INDEX = ROOT / "index.html"


def indent_block(text: str, prefix: str = "  ") -> str:
    lines = text.strip("\n").splitlines()
    return "\n".join(prefix + line if line else line for line in lines) + "\n"


def load_partial(name: str) -> str:
    return (HOME / name).read_text(encoding="utf-8")


def render_features(items: list[str]) -> str:
    lis = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f'<ul class="value-card-features">{lis}</ul>'


def render_cta_primary(cta: dict) -> str:
    attrs = f'href="{html.escape(cta["href"], quote=True)}" class="btn btn-primary btn-sm"'
    if cta.get("external"):
        attrs += ' target="_blank" rel="noopener noreferrer"'
    return f'<a {attrs}>{html.escape(cta["label"])}</a>'


def render_card(product: dict) -> str:
    classes = ["value-card", "reveal"]
    if product.get("visualStyle") != "tarjeta":
        classes.append("value-card--brand-visual")
    variant = product.get("variant")
    if variant == "easynodeone":
        classes.insert(1, "value-card--easynodeone")
    elif variant == "econverso":
        classes.insert(1, "value-card--econverso")
    if product.get("featured"):
        classes.append("value-card--featured")
    if product.get("soon"):
        classes.append("value-card--soon")
    if product.get("visualStyle") == "tarjeta":
        classes.append("value-card--tarjeta")

    soon_badge = ""
    if product.get("soon"):
        soon_badge = '              <span class="product-soon-badge">Próximamente</span>\n'

    actions = ['              <div class="value-card-actions">']
    cta = product.get("ctaPrimary")
    if cta:
        actions.append(f"                {render_cta_primary(cta)}")
    page_href = product.get("pageHref")
    page_label = product.get("pageLinkLabel", "Ver más")
    if page_href:
        actions.append(
            f'                <a href="{html.escape(page_href, quote=True)}" class="value-card-more">'
            f'{html.escape(page_label)} <span aria-hidden="true">→</span></a>'
        )
    actions.append("              </div>")

    img_src = html.escape(product["image"], quote=True)
    img_attrs = (
        f'src="{img_src}" alt="" width="480" height="320" '
        f'loading="lazy" decoding="async"'
    )
    fallback = product.get("imageFallback")
    if fallback:
        fb = html.escape(fallback, quote=True)
        img_attrs += f' onerror="this.onerror=null;this.src=\'{fb}\';"'

    class_attr = " ".join(classes)
    return f"""          <article class="{class_attr}">
            <div class="value-card-body">
{soon_badge}              <p class="value-card-kicker">{html.escape(product["kicker"])}</p>
              <h3 class="value-card-title">{html.escape(product["title"])}</h3>
              <p class="value-card-desc">{html.escape(product["description"])}</p>
              <p class="value-card-features-label">{html.escape(product["featuresLabel"])}</p>
              {render_features(product["features"])}
{chr(10).join(actions)}
            </div>
            <div class="value-card-visual">
              <img {img_attrs}>
            </div>
          </article>"""


def render_ecosystem(catalog: dict) -> str:
    section_id = catalog["sectionId"]
    parts = [
        f'    <section id="{section_id}" class="section value-pillars" aria-labelledby="ecosystem-heading">',
        f'      <h2 id="ecosystem-heading" class="section-title reveal">{html.escape(catalog["sectionTitle"])}</h2>',
        f'      <p class="pillars-lede reveal">{html.escape(catalog["sectionLede"])}</p>',
        "",
    ]

    for category in catalog["categories"]:
        grid_class = "value-pillars-grid"
        if category.get("grid") == "duo":
            grid_class += " value-pillars-grid--duo"
        parts.append('      <div class="ecosystem-category">')
        parts.append(
            f'        <h3 class="ecosystem-category-title reveal">{html.escape(category["title"])}</h3>'
        )
        parts.append(f'        <div class="{grid_class}">')
        for product in category["products"]:
            parts.append(render_card(product))
        parts.append("        </div>")
        parts.append("      </div>")
        parts.append("")

    parts.append(
        f'      <p class="odoo-relation-note reveal" role="note">{catalog["odooNote"]}</p>'
    )
    parts.append("    </section>")
    return "\n".join(parts) + "\n"


def build_index() -> str:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    header = PARTIALS.joinpath("header.html").read_text(encoding="utf-8")
    footer = PARTIALS.joinpath("footer.html").read_text(encoding="utf-8")

    main = "".join(
        [
            load_partial("hero.html"),
            render_ecosystem(catalog),
            load_partial("roadmap.html"),
            load_partial("cta.html"),
            load_partial("scale.html"),
        ]
    )

    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Easy Technology Services — escaparate comercial del EasyTech Ecosystem: plataformas SaaS, soluciones de negocio y servicios profesionales en Panamá.">
  <title>Easy Technology Services — EasyTech Ecosystem</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/main.css">
  <link rel="stylesheet" href="assets/css/ramp-theme.css">
  <link rel="stylesheet" href="assets/css/home.css">
</head>
<body class="ramp page-home">
{indent_block(header, "  ").rstrip()}
  <main id="page-main" class="page-surface">
{main}  </main>
{indent_block(footer, "  ").rstrip()}
  <script src="assets/js/main.js"></script>
  <script src="assets/js/page-transitions.js"></script>
</body>
</html>
"""
    return doc


def main() -> None:
    INDEX.write_text(build_index(), encoding="utf-8")
    print("built", INDEX.name)


if __name__ == "__main__":
    main()
