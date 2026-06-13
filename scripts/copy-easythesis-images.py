"""Copy Easy Thesis marketing images from Cursor assets or imagenes/EasyThesis/."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets" / "images" / "easythesis"
CURSOR_ASSETS = (
    Path.home()
    / ".cursor"
    / "projects"
    / "c-Users-shidalgo-Documents-0-Tecnologia-0-Easytech-Services-Site-2026"
    / "assets"
)
LOCAL_SRC = ROOT / "imagenes" / "EasyThesis"

MAP = {
    "easythesis-logo-mark": "logo-mark.png",
    "easythesis-logo-horizontal": "logo-horizontal.png",
    "easythesis-logo-badge-dark": "logo-badge-dark.png",
    "01-expediente-unico-laptop": "expediente-unico.png",
    "easythesis-hero-portada": "hero-portada.png",
    "easythesis-flujo-operativo": "flujo-operativo.png",
    "07-problema-caos-documental": "problema-caos-documental.png",
    "06-hero-dashboard-maria": "hero-dashboard.png",
    "05-modulo-documentos-tabla": "modulo-documentos.png",
    "04-hero-confianza-cinco-columnas": "hero-confianza.png",
    "02-brand-board-montserrat": "brand-board.png",
    "03-grid-16-value-props": "grid-modulos.png",
}


def copy_from_dir(src_dir: Path) -> int:
    copied = 0
    DEST.mkdir(parents=True, exist_ok=True)
    for key, name in MAP.items():
        match = next(src_dir.glob(f"*{key}*"), None)
        if match and match.is_file():
            shutil.copy2(match, DEST / name)
            print("copied", match.name, "->", name)
            copied += 1
    return copied


def main() -> None:
    if LOCAL_SRC.is_dir():
        n = copy_from_dir(LOCAL_SRC)
        if n:
            return
    if CURSOR_ASSETS.is_dir():
        copy_from_dir(CURSOR_ASSETS)
        return
    print("no source images found")


if __name__ == "__main__":
    main()
