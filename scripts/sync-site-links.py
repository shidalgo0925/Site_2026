"""Apply canonical external and internal link updates across site HTML."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    # Easy Odoo — mensaje WhatsApp según MAPA_CTA
    (
        "https://wa.me/50766884938?text=Quiero%20una%20demo%20de%20ERP%20EasyTech%20(Odoo)",
        "https://wa.me/50766884938?text=Quiero%20informaci%C3%B3n%20sobre%20Easy%20Odoo%20(ERP%20EasyTech)",
    ),
    (
        "https://wa.me/50766884938?text=Informaci%C3%B3n%20sobre%20ERP%20EasyTech%20%28Odoo%2C%20cheques%29",
        "https://wa.me/50766884938?text=Quiero%20informaci%C3%B3n%20sobre%20Easy%20Odoo%20(ERP%20EasyTech)",
    ),
    # Demo en landing → agenda interna
    (
        'href="https://wa.me/50766884938?text=Quiero%20ver%20una%20demo%20EasyTech"',
        'href="agenda.html"',
    ),
    # Anclas legacy → páginas del catálogo
    ('href="soluciones.html#producto-erp"', 'href="soluciones.html"'),
    # Hero landing: no apuntar al login EN1
    (
        """<a href="https://appprd.easynodeone.com/login" class="btn btn-primary" target="_blank" rel="noopener noreferrer">
                <span>Probar gratis</span>
                <svg class="btn-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M5 12h14M13 6l6 6-6 6"/>
                </svg>
              </a>
              <a href="#demo" class="btn btn-ghost">Ver capturas</a>""",
        """<a href="agenda.html" class="btn btn-primary">
                <span>Agendar demo</span>
                <svg class="btn-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M5 12h14M13 6l6 6-6 6"/>
                </svg>
              </a>
              <a href="contacto.html" class="btn btn-ghost">Contacto</a>""",
    ),
    (
        """<a href="https://appprd.easynodeone.com/login" class="btn btn-primary" target="_blank" rel="noopener noreferrer">
                <span>Probar gratis</span>
                <svg class="btn-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M5 12h14M13 6l6 6-6 6"/>
                </svg>
              </a>
              <a href="index.html#demo" class="btn btn-ghost">Ver capturas</a>""",
        """<a href="agenda.html" class="btn btn-primary">
                <span>Agendar demo</span>
                <svg class="btn-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M5 12h14M13 6l6 6-6 6"/>
                </svg>
              </a>
              <a href="contacto.html" class="btn btn-ghost">Contacto</a>""",
    ),
    # Pills del hero — catálogo completo
    (
        """<nav class="hero-pills" aria-label="Ir a cada solución">
              <a href="soluciones.html">ERP EasyTech</a>
              <a href="econverso.html">Econverso</a>
              <a href="easynodeone.html">EasyNodeOne</a>
            </nav>""",
        """<nav class="hero-pills" aria-label="Ir a cada solución">
              <a href="soluciones.html">Easy Odoo</a>
              <a href="facturacion-electronica.html">Facturación</a>
              <a href="econverso.html">Easy Converso</a>
              <a href="easynodeone.html">EasyNodeOne</a>
            </nav>""",
    ),
    # Tarjeta facturación → página dedicada
    (
        """<h3 class="value-card-title">Facturación y reportes</h3>
            <p class="value-card-desc">Facturas, notas y reportes listos para operar y decidir con respaldo contable.</p>
            <a href="soluciones.html" class="value-card-more">""",
        """<h3 class="value-card-title">Facturación y reportes</h3>
            <p class="value-card-desc">Facturas, notas y reportes listos para operar y decidir con respaldo contable.</p>
            <a href="facturacion-electronica.html" class="value-card-more">""",
    ),
    # Bloques de contacto — páginas internas + registro EN1
    (
        """<a href="https://econverso.com" target="_blank" rel="noopener noreferrer">Sitio de Econverso</a>""",
        """<a href="econverso.html">Easy Converso</a>""",
    ),
    (
        """<a href="https://appprd.easynodeone.com/login" target="_blank" rel="noopener noreferrer">Entrar</a>""",
        """<a href="https://appprd.easynodeone.com/register" target="_blank" rel="noopener noreferrer">Crear cuenta</a>""",
        "contacto.html",
    ),
    # Header — aclarar destino EN1
    (
        '<a href="https://appprd.easynodeone.com/login" class="header-link" target="_blank" rel="noopener noreferrer">Entrar</a>',
        '<a href="https://appprd.easynodeone.com/login" class="header-link" target="_blank" rel="noopener noreferrer" title="Iniciar sesión en EasyNodeOne">Entrar</a>',
    ),
]


def sync_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for item in REPLACEMENTS:
        if len(item) == 3:
            old, new, only = item
            if path.name != only:
                continue
        else:
            old, new = item
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated: list[str] = []
    for path in sorted(ROOT.glob("*.html")):
        if sync_file(path):
            updated.append(path.name)
    partial_header = ROOT / "assets" / "partials" / "header.html"
    if sync_file(partial_header):
        updated.append(str(partial_header.relative_to(ROOT)))
    if updated:
        print("Updated:", ", ".join(updated))
    else:
        print("No changes needed.")


if __name__ == "__main__":
    main()
