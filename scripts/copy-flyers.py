"""Copy numbered flyers from imagenes/ to assets/images/flyers/{slug}.png"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "imagenes"
DEST = ROOT / "assets" / "images" / "flyers"

# Números según lámina Productos.png (EASYTECH SERVICES)
FLYER_MAP = {
    "desarrollo-software": "11.png",
    "easy-odoo": "22.png",
    "facturacion-electronica": "33.png",
    "consultoria-ti": "44.png",
    "easynodeone": "55.png",
    "eclassone": "66.png",
    "ethesisone": "77.png",
    "eposone": "88.png",
    "epayroll": "Logo_EPayRoll.png",
}

EXTRA = {
    "ecosystem-overview": "Productos.png",
}


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for slug, name in {**FLYER_MAP, **EXTRA}.items():
        src = SRC / name
        if not src.is_file():
            print("skip missing", name)
            continue
        dest = DEST / f"{slug}.png"
        shutil.copy2(src, dest)
        print("copied", name, "->", dest.name)

    for junk in DEST.glob("*.png"):
        stem = junk.stem
        if stem.isdigit() or stem in {"productos", "111", "122", "442", "662", "881"}:
            junk.unlink()
            print("removed junk", junk.name)


if __name__ == "__main__":
    main()
