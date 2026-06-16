"""Append ?v= query to local assets/css and assets/js references in root HTML."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260613"
PAT = re.compile(r'((?:href|src)=")(assets/(?:css|js)/[^"?]+)(")')


def bust(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        url = m.group(2)
        if "?v=" in url:
            return m.group(0)
        return f'{m.group(1)}{url}?v={VERSION}{m.group(3)}'

    return PAT.sub(repl, text)


def main() -> None:
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        new = bust(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("updated", path.name)


if __name__ == "__main__":
    main()
