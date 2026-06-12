"""Update WhatsApp number across site files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_WA = "50766884938"
NEW_WA = "50766884938"
OLD_PHONE = "<a href="https://wa.me/50766884938?text=Hola%20EasyTech" target="_blank" rel="noopener noreferrer">+507 6688-4938</a> · WhatsApp"
NEW_PHONE = (
    '<a href="https://wa.me/50766884938?text=Hola%20EasyTech" '
    'target="_blank" rel="noopener noreferrer">+507 6688-4938</a> · WhatsApp'
)

GLOBS = ["*.html", "assets/js/*.js", "scripts/*.py", "docs/*.md"]


def main() -> None:
    updated: list[str] = []
    for pattern in GLOBS:
        for path in ROOT.glob(pattern):
            text = path.read_text(encoding="utf-8")
            original = text
            text = text.replace(OLD_WA, NEW_WA)
            text = text.replace(OLD_PHONE, NEW_PHONE)
            if text != original:
                path.write_text(text, encoding="utf-8")
                updated.append(str(path.relative_to(ROOT)))
    if updated:
        print("Updated:", ", ".join(sorted(updated)))
    else:
        print("No changes needed.")


if __name__ == "__main__":
    main()
