"""Copy EPayRoll logo and generate landing assets."""
from __future__ import annotations

import shutil
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    Image = None  # type: ignore
    ImageDraw = None  # type: ignore
    ImageFont = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets" / "images" / "epayroll"
FLYER_DEST = ROOT / "assets" / "images" / "flyers" / "epayroll.png"
SRC = ROOT / "imagenes" / "Logo_EPayRoll.png"
CURSOR_ASSETS = Path(
    r"\\?\C:\Users\shidalgo\.cursor\projects"
    r"\c-Users-shidalgo-Documents-0-Tecnologia-0-Easytech-Services-Site-2026\assets"
)

# Colores extraídos del logo oficial EPayRoll
TEAL = (0, 152, 144)       # #009890
NAVY = (0, 32, 96)         # #002060
TEAL_DARK = (0, 96, 112)   # #006070
WHITE = (255, 255, 255)
LIGHT = (232, 248, 248)    # #e8f8f8

MODULES = [
    ("mod-motor", "Motor de cálculo", "Configuración sobre código"),
    ("mod-vacaciones", "Vacaciones programadas", "Módulo obligatorio"),
    ("mod-planilla", "Planilla y conceptos", "Ingresos, descuentos y provisiones"),
    ("mod-liquidacion", "Liquidación laboral", "Renuncia, despido y fin de contrato"),
    ("mod-asistencia", "Asistencia y turnos", "Marcación, extras y recargos"),
    ("mod-cumplimiento", "CSS, DGI y banca", "SIPE, ISR y exportación ACH"),
]


def find_source() -> Path | None:
    if SRC.is_file():
        return SRC
    if CURSOR_ASSETS.is_dir():
        match = next(CURSOR_ASSETS.glob("*Logo_EPayRoll-*"), None)
        if match and match.is_file():
            return match
    return None


def find_font(size: int):
    candidates = [
        Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def paste_rgba(base: Image.Image, overlay: Image.Image, xy: tuple[int, int]) -> None:
    if overlay.mode == "RGBA":
        base.paste(overlay, xy, overlay)
    else:
        base.paste(overlay, xy)


def make_module_card(name: str, title: str, subtitle: str, icon: Image.Image, accent: tuple[int, int, int]) -> None:
    w, h = 640, 360
    card = Image.new("RGB", (w, h), LIGHT)
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 0, w, 72), fill=accent)
    draw.rectangle((0, 72, w, h), fill=WHITE)

    title_font = find_font(28)
    sub_font = find_font(18)
    draw.text((24, 18), title, fill=WHITE, font=title_font)

    icon_size = 220
    icon_resized = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    paste_rgba(card, icon_resized, ((w - icon_size) // 2, 96))

    bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, h - 44), subtitle, fill=NAVY, font=sub_font)

    card.save(DEST / f"{name}.png", optimize=True)


def slice_assets(src: Path) -> None:
    if Image is None:
        raise SystemExit("Pillow required: pip install pillow")

    DEST.mkdir(parents=True, exist_ok=True)
    FLYER_DEST.parent.mkdir(parents=True, exist_ok=True)

    im = Image.open(src).convert("RGBA")
    w, h = im.size

    shutil.copy2(src, DEST / "flyer-full.png")
    shutil.copy2(src, FLYER_DEST)
    im.convert("RGB").save(DEST / "logo-full.png", optimize=True)

    # Ilustración (monitor + iconos) — sin wordmark inferior
    illustration = im.crop((int(w * 0.08), int(h * 0.04), int(w * 0.92), int(h * 0.60)))
    illustration.convert("RGB").save(DEST / "hero.png", optimize=True)

    # Wordmark EPayRoll + tagline
    brand = im.crop((0, int(h * 0.58), w, h)).convert("RGB")
    brand.save(DEST / "brand-lockup.png", optimize=True)

    icon = im.crop((int(w * 0.20), int(h * 0.10), int(w * 0.80), int(h * 0.58)))

    for slug, title, subtitle in MODULES:
        accent = TEAL if slug != "mod-vacaciones" else TEAL_DARK
        make_module_card(slug, title, subtitle, icon, accent)

    modules_strip = Image.new("RGB", (640 * 3, 360 * 2), LIGHT)
    for i, (slug, _, _) in enumerate(MODULES):
        tile = Image.open(DEST / f"{slug}.png")
        col, row = i % 3, i // 3
        modules_strip.paste(tile, (col * 640, row * 360))
    modules_strip.save(DEST / "modules.png", optimize=True)

    hero_card = im.copy()
    hero_card.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
    hero_card.convert("RGB").save(DEST / "hero-card.png", optimize=True)

    shutil.copy2(DEST / "mod-vacaciones.png", DEST / "vacaciones-featured.png")

    arch = Image.new("RGB", (1024, 320), WHITE)
    draw = ImageDraw.Draw(arch)
    draw.rectangle((0, 0, 1024, 320), fill=LIGHT)
    draw.rectangle((0, 0, 8, 320), fill=TEAL)
    title_font = find_font(34)
    body_font = find_font(20)
    draw.text((32, 36), "Configuración sobre código", fill=NAVY, font=title_font)
    draw.text(
        (32, 92),
        "Motor genérico gobernado por tablas maestras — no reglas fijas en código.",
        fill=(71, 85, 105),
        font=body_font,
    )
    icon_small = icon.convert("RGB").resize((200, 200), Image.Resampling.LANCZOS)
    arch.paste(icon_small, (780, 60))
    arch.save(DEST / "architecture.png", optimize=True)

    print("generated EPayRoll assets into", DEST)


def main() -> None:
    src = find_source()
    if not src:
        print("no EPayRoll logo found")
        return
    if src != SRC:
        shutil.copy2(src, SRC)
    slice_assets(SRC)


if __name__ == "__main__":
    main()
