"""Inline assets/partials/header.html and footer.html into site HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "assets" / "partials"
HEADER = PARTIALS / "header.html"
FOOTER = PARTIALS / "footer.html"

HEADER_SLOT = re.compile(
    r'  <div id="site-chrome-header" class="site-chrome-slot"></div>\n',
    re.MULTILINE,
)
FOOTER_SLOT = re.compile(
    r'  <div id="site-chrome-footer" class="site-chrome-slot"></div>\n',
    re.MULTILINE,
)
EXISTING_HEADER = re.compile(
    r"  <header class=\"site-header site-header--ramp\">.*?</header>\n",
    re.DOTALL,
)
EXISTING_FOOTER = re.compile(
    r"  <footer class=\"site-footer\">.*?</footer>\n",
    re.DOTALL,
)


def indent_block(text: str, prefix: str = "  ") -> str:
    lines = text.strip("\n").splitlines()
    return "\n".join(prefix + line if line else line for line in lines) + "\n"


def inline_file(path: Path, header: str, footer: str) -> None:
    text = path.read_text(encoding="utf-8")

    if HEADER_SLOT.search(text):
        text = HEADER_SLOT.sub(indent_block(header), text, count=1)
    elif EXISTING_HEADER.search(text):
        text = EXISTING_HEADER.sub(indent_block(header), text, count=1)

    if FOOTER_SLOT.search(text):
        text = FOOTER_SLOT.sub(indent_block(footer), text, count=1)
    elif EXISTING_FOOTER.search(text):
        text = EXISTING_FOOTER.sub(indent_block(footer), text, count=1)

    text = text.replace(
        '  <script src="assets/js/site-chrome.js"></script>\n', ""
    )

    path.write_text(text, encoding="utf-8")


def main() -> None:
    header = HEADER.read_text(encoding="utf-8")
    footer = FOOTER.read_text(encoding="utf-8")
    html_files = sorted(ROOT.glob("*.html"))
    for path in html_files:
        inline_file(path, header, footer)
        print("inlined", path.name)


if __name__ == "__main__":
    main()
