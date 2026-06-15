"""Build index.html from home partials and shared chrome."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "assets" / "partials"
HOME = PARTIALS / "home"
INDEX = ROOT / "index.html"

HOME_PARTIALS = (
    "hero.html",
    "metricas.html",
    "soluciones.html",
    "odoo-fe.html",
    "ecosistema.html",
    "casos-exito.html",
    "metodologia.html",
    "cta.html",
)


def indent_block(text: str, prefix: str = "  ") -> str:
    lines = text.strip("\n").splitlines()
    return "\n".join(prefix + line if line else line for line in lines) + "\n"


def load_partial(name: str) -> str:
    return (HOME / name).read_text(encoding="utf-8")


def build_index() -> str:
    header = PARTIALS.joinpath("header.html").read_text(encoding="utf-8")
    footer = PARTIALS.joinpath("footer.html").read_text(encoding="utf-8")
    main = "".join(load_partial(name) for name in HOME_PARTIALS)

    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Implementamos ERP, automatización, plataformas educativas y soluciones empresariales integradas para organizaciones en Panamá y Latinoamérica.">
  <title>EasyTech Services | ERP, Automatización y Transformación Digital</title>
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
