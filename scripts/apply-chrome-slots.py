import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "index.html",
    "soluciones.html",
    "econverso.html",
    "easynodeone.html",
    "agenda.html",
    "contacto.html",
]

HEADER_SLOT = '  <div id="site-chrome-header" class="site-chrome-slot"></div>\n'
FOOTER_SLOT = '  <div id="site-chrome-footer" class="site-chrome-slot"></div>\n'


def main() -> None:
    for name in FILES:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")

        text = re.sub(
            r'  <header class="site-header site-header--ramp">.*?</header>\n',
            HEADER_SLOT,
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(
            r'  <footer class="site-footer">.*?</footer>\n',
            FOOTER_SLOT,
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(
            r'  <script>\s*document\.getElementById\("y"\)\.textContent = new Date\(\)\.getFullYear\(\);\s*</script>\s*\n',
            "",
            text,
        )

        if "site-chrome.js" not in text:
            text = text.replace(
                '  <script src="assets/js/main.js"></script>',
                '  <script src="assets/js/site-chrome.js"></script>\n'
                '  <script src="assets/js/main.js"></script>',
            )

        if name == "contacto.html":
            text = text.replace('<body class="ramp">', '<body class="ramp page-contacto">')

        path.write_text(text, encoding="utf-8")
        print("updated", name)


if __name__ == "__main__":
    main()
