"""Copy and slice EPOSOne flyer from Cursor assets or imagenes/."""
from __future__ import annotations

import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets" / "images" / "eposone"
FLYER_DEST = ROOT / "assets" / "images" / "flyers" / "eposone.png"
CURSOR_ASSETS = (
    Path.home()
    / ".cursor"
    / "projects"
    / "c-Users-shidalgo-Documents-0-Tecnologia-0-Easytech-Services-Site-2026"
    / "assets"
)
LOCAL_CANDIDATES = [
    ROOT / "imagenes" / "88.png",
    ROOT / "imagenes" / "EPOSOne.png",
]


def find_source() -> Path | None:
    for candidate in LOCAL_CANDIDATES:
        if candidate.is_file():
            return candidate
    if CURSOR_ASSETS.is_dir():
        match = next(CURSOR_ASSETS.glob("*images_88-*"), None)
        if match and match.is_file():
            return match
    return None


def slice_flyer(src: Path) -> None:
    if Image is None:
        raise SystemExit("Pillow required: pip install pillow")

    DEST.mkdir(parents=True, exist_ok=True)
    FLYER_DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, DEST / "flyer-full.png")
    shutil.copy2(src, FLYER_DEST)

    im = Image.open(src)
    w, h = im.size
    regions = {
        "hero": (int(w * 0.41), int(h * 0.057), int(w * 0.962), int(h * 0.264)),
        "pillars": (0, int(h * 0.28), w, int(h * 0.34)),
        "modules": (0, int(h * 0.34), w, int(h * 0.58)),
        "benefits": (0, int(h * 0.58), w, int(h * 0.78)),
        "testimonials": (0, int(h * 0.78), w, int(h * 0.90)),
        "cta": (0, int(h * 0.90), w, h),
    }
    for name, box in regions.items():
        im.crop(box).save(DEST / f"{name}.png", optimize=True)

    mod = Image.open(DEST / "modules.png")
    mw, mh = mod.size
    cols, rows = 3, 2
    cw, ch = mw // cols, mh // rows
    names = [
        "mod-pos",
        "mod-inventario",
        "mod-clientes",
        "mod-promociones",
        "mod-reportes",
        "mod-config",
    ]
    idx = 0
    for row in range(rows):
        for col in range(cols):
            box = (
                col * cw,
                row * ch,
                mw if col == cols - 1 else (col + 1) * cw,
                mh if row == rows - 1 else (row + 1) * ch,
            )
            mod.crop(box).save(DEST / f"{names[idx]}.png", optimize=True)
            idx += 1

    shutil.copy2(DEST / "hero.png", DEST / "hero-card.png")
    print("sliced EPOSOne flyer into", DEST)


def main() -> None:
    src = find_source()
    if not src:
        print("no EPOSOne flyer found")
        return
    slice_flyer(src)


if __name__ == "__main__":
    main()
