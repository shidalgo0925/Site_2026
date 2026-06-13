"""Generate conceptual Consultoría TI illustrations (no flyer crops)."""
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
DEST = ROOT / "assets" / "images" / "consultoria-ti"
FLYER_SRC = ROOT / "imagenes" / "442.png"
FLYER_DEST = ROOT / "assets" / "images" / "flyers" / "consultoria-ti.png"

NAVY = (16, 42, 67)       # #102a43
BLUE = (37, 99, 235)      # #2563eb
BLUE_DARK = (29, 78, 216)
PURPLE = (124, 58, 237)
WHITE = (255, 255, 255)
LIGHT = (239, 246, 255)
MUTED = (100, 116, 139)
SOFT = (219, 234, 254)

SERVICES = [
    ("svc-transformacion", "Transformación digital", "rocket"),
    ("svc-arquitectura", "Arquitectura empresarial", "cubes"),
    ("svc-automatizacion", "Automatización", "gears"),
    ("svc-ciberseguridad", "Gobierno TI", "shield"),
    ("svc-analitica", "Análisis e inteligencia", "chart"),
    ("svc-nube", "Migración a la nube", "cloud"),
]


def find_font(size: int, bold: bool = False):
    names = ["segoeuib.ttf", "segoeui.ttf", "arialbd.ttf", "arial.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
    for name in names:
        path = Path("C:/Windows/Fonts") / name
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def gradient_bg(w: int, h: int, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (w, h), top)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(0, y), (w, y)], fill=color)
    return img


def draw_rocket(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1) -> None:
    s = scale
    body = [(cx - 18 * s, cy + 20 * s), (cx + 18 * s, cy + 20 * s), (cx + 12 * s, cy - 30 * s), (cx - 12 * s, cy - 30 * s)]
    draw.polygon(body, fill=BLUE)
    draw.polygon([(cx, cy - 44 * s), (cx + 14 * s, cy - 18 * s), (cx - 14 * s, cy - 18 * s)], fill=PURPLE)
    draw.polygon([(cx - 22 * s, cy + 8 * s), (cx - 34 * s, cy + 28 * s), (cx - 10 * s, cy + 20 * s)], fill=BLUE_DARK)
    draw.polygon([(cx + 22 * s, cy + 8 * s), (cx + 34 * s, cy + 28 * s), (cx + 10 * s, cy + 20 * s)], fill=BLUE_DARK)
    draw.ellipse((cx - 8 * s, cy - 8 * s, cx + 8 * s, cy + 8 * s), fill=WHITE)


def draw_cubes(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    size = 36
    offsets = [(-42, -10, BLUE), (0, -28, PURPLE), (42, -10, BLUE_DARK), (-21, 22, NAVY)]
    for ox, oy, color in offsets:
        x, y = cx + ox, cy + oy
        draw.rectangle((x, y, x + size, y + size), fill=color, outline=WHITE, width=2)
        draw.polygon([(x, y), (x + 10, y - 10), (x + size + 10, y - 10), (x + size, y)], fill=tuple(min(255, c + 30) for c in color))


def draw_gears(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    for gx, gy, r, color in [(cx - 30, cy, 26, BLUE), (cx + 28, cy + 8, 20, PURPLE)]:
        draw.ellipse((gx - r, gy - r, gx + r, gy + r), fill=color, outline=WHITE, width=2)
        for i in range(8):
            import math
            a = i * math.pi / 4
            x1 = gx + math.cos(a) * (r - 4)
            y1 = gy + math.sin(a) * (r - 4)
            x2 = gx + math.cos(a) * (r + 8)
            y2 = gy + math.sin(a) * (r + 8)
            draw.line([(x1, y1), (x2, y2)], fill=color, width=6)


def draw_shield(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    draw.polygon([(cx, cy - 42), (cx + 38, cy - 22), (cx + 30, cy + 32), (cx, cy + 48), (cx - 30, cy + 32), (cx - 38, cy - 22)], fill=BLUE)
    draw.line([(cx - 14, cy + 2), (cx - 2, cy + 16), (cx + 20, cy - 12)], fill=WHITE, width=5)


def draw_chart(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    base_y = cy + 36
    bars = [(cx - 48, 28, BLUE), (cx - 16, 44, PURPLE), (cx + 16, 34, BLUE_DARK), (cx + 48, 52, BLUE)]
    for x, height, color in bars:
        draw.rectangle((x - 12, base_y - height, x + 12, base_y), fill=color, outline=WHITE, width=1)
    draw.line([(cx - 62, base_y), (cx + 62, base_y)], fill=NAVY, width=3)


def draw_cloud(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    draw.ellipse((cx - 52, cy - 8, cx - 8, cy + 28), fill=SOFT, outline=BLUE, width=2)
    draw.ellipse((cx - 28, cy - 22, cx + 18, cy + 24), fill=WHITE, outline=BLUE, width=2)
    draw.ellipse((cx + 4, cy - 10, cx + 48, cy + 26), fill=SOFT, outline=BLUE, width=2)
    draw.polygon([(cx - 8, cy + 18), (cx + 8, cy + 34), (cx + 24, cy + 18)], fill=BLUE)


def draw_icon(draw: ImageDraw.ImageDraw, kind: str, cx: int, cy: int) -> None:
    drawers = {
        "rocket": draw_rocket,
        "cubes": draw_cubes,
        "gears": draw_gears,
        "shield": draw_shield,
        "chart": draw_chart,
        "cloud": draw_cloud,
    }
    drawers[kind](draw, cx, cy)


def make_service_card(slug: str, title: str, icon: str) -> None:
    w, h = 640, 360
    img = gradient_bg(w, h, LIGHT, WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w, 64), fill=NAVY)
    font = find_font(22, bold=True)
    draw.text((24, 18), title, fill=WHITE, font=font)
    draw_icon(draw, icon, w // 2, h // 2 + 20)
    img.save(DEST / f"{slug}.png", optimize=True)


def make_hero() -> None:
    w, h = 960, 540
    img = gradient_bg(w, h, LIGHT, WHITE)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((32, 40, 520, 500), radius=20, fill=WHITE, outline=SOFT, width=2)
    title_font = find_font(28, bold=True)
    sub_font = find_font(18)
    draw.text((56, 68), "Hoja de ruta tecnológica", fill=NAVY, font=title_font)

    steps = ["Diagnóstico", "Estrategia", "Arquitectura", "Implementación", "Evolución"]
    colors = [BLUE, PURPLE, BLUE_DARK, BLUE, NAVY]
    x = 70
    for i, (step, color) in enumerate(zip(steps, colors)):
        draw.ellipse((x - 14, 130, x + 14, 130 + 28), fill=color)
        if i < len(steps) - 1:
            draw.line([(x + 14, 144), (x + 66, 144)], fill=SOFT, width=4)
        bbox = draw.textbbox((0, 0), step, font=sub_font)
        tw = bbox[2] - bbox[0]
        draw.text((x - tw // 2, 168), step, fill=NAVY, font=sub_font)
        x += 80

    draw.rounded_rectangle((56, 230, 496, 470), radius=14, fill=LIGHT, outline=SOFT, width=1)
    draw.pieslice((120, 270, 300, 450), 200, 340, fill=BLUE)
    draw.pieslice((120, 270, 300, 450), 340, 420, fill=PURPLE)
    draw.pieslice((120, 270, 300, 450), 420, 520, fill=BLUE_DARK)
    draw.ellipse((175, 325, 245, 395), fill=WHITE)
    draw.text((310, 300), "Estrategia de", fill=NAVY, font=sub_font)
    draw.text((310, 326), "Transformación Digital", fill=BLUE, font=title_font)
    for i, label in enumerate(["Personas", "Procesos", "Negocio", "Datos"]):
        draw.text((310, 372 + i * 24), f"• {label}", fill=MUTED, font=sub_font)

    draw.rounded_rectangle((560, 48, 928, 492), radius=20, fill=NAVY)
    draw.text((590, 78), "Acompañamiento", fill=WHITE, font=title_font)
    draw.text((590, 112), "estratégico EasyTech", fill=SOFT, font=sub_font)
    draw_icon(draw, "shield", 744, 280)
    draw.rounded_rectangle((590, 390, 898, 460), radius=12, fill=BLUE)
    draw.text((620, 418), "Decisiones con criterio · Resultados medibles", fill=WHITE, font=sub_font)

    img.save(DEST / "hero.png", optimize=True)
    shutil.copy2(DEST / "hero.png", DEST / "hero-card.png")


def make_value_process() -> None:
    w, h = 960, 200
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((8, 8, w - 8, h - 8), radius=16, fill=LIGHT, outline=SOFT, width=2)
    steps = ["Analizamos", "Diseñamos", "Implementamos", "Optimizamos"]
    icons = ["chart", "cubes", "gears", "rocket"]
    slot = w // 4
    font = find_font(20, bold=True)
    for i, (step, icon) in enumerate(zip(steps, icons)):
        cx = slot * i + slot // 2
        draw.ellipse((cx - 28, 36, cx + 28, 92), fill=WHITE, outline=BLUE, width=2)
        draw_icon(draw, icon, cx, 64)
        bbox = draw.textbbox((0, 0), step, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, 118), step, fill=NAVY, font=font)
        if i < 3:
            draw.line([(cx + 34, 64), (cx + slot - 34, 64)], fill=BLUE, width=3)
    img.save(DEST / "value-process.png", optimize=True)


def make_methodology() -> None:
    w, h = 960, 280
    img = gradient_bg(w, h, WHITE, LIGHT)
    draw = ImageDraw.Draw(img)
    font = find_font(22, bold=True)
    sub = find_font(16)
    items = [
        ("1", "Diagnóstico", "Entorno y procesos actuales"),
        ("2", "Propuesta", "Estrategia personalizada"),
        ("3", "Implementación", "Ejecución y gestión del cambio"),
        ("4", "Evaluación", "Resultados y mejora continua"),
    ]
    for i, (num, title, desc) in enumerate(items):
        x = 24 + i * 234
        draw.rounded_rectangle((x, 24, x + 210, 256), radius=14, fill=WHITE, outline=SOFT, width=2)
        draw.ellipse((x + 16, 40, x + 56, 80), fill=BLUE)
        draw.text((x + 28, 48), num, fill=WHITE, font=font)
        draw.text((x + 16, 96), title, fill=NAVY, font=font)
        draw.multiline_text((x + 16, 132), desc, fill=MUTED, font=sub, spacing=4)
    img.save(DEST / "methodology.png", optimize=True)


def make_results() -> None:
    w, h = 960, 320
    img = gradient_bg(w, h, NAVY, (10, 34, 58))
    draw = ImageDraw.Draw(img)
    font = find_font(26, bold=True)
    sub = find_font(18)
    draw.text((48, 48), "Impacto medible", fill=WHITE, font=font)
    metrics = [("-30%", "Costos operativos"), ("+25%", "Productividad"), ("100%", "Trazabilidad")]
    for i, (val, label) in enumerate(metrics):
        x = 48 + i * 300
        draw.rounded_rectangle((x, 120, x + 260, 260), radius=16, fill=(255, 255, 255, 20))
        draw.rounded_rectangle((x, 120, x + 260, 260), radius=16, outline=BLUE, width=2)
        draw.text((x + 24, 148), val, fill=SOFT, font=find_font(40, bold=True))
        draw.text((x + 24, 210), label, fill=WHITE, font=sub)
    img.save(DEST / "results.png", optimize=True)


def copy_flyer_only() -> None:
    if FLYER_SRC.is_file():
        shutil.copy2(FLYER_SRC, DEST / "flyer-full.png")
        FLYER_DEST.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(FLYER_SRC, FLYER_DEST)


def main() -> None:
    if Image is None:
        raise SystemExit("Pillow required: pip install pillow")
    DEST.mkdir(parents=True, exist_ok=True)
    copy_flyer_only()
    make_hero()
    make_value_process()
    make_methodology()
    make_results()
    for slug, title, icon in SERVICES:
        make_service_card(slug, title, icon)

    modules = Image.new("RGB", (640 * 3, 360 * 2), LIGHT)
    for i, (slug, _, _) in enumerate(SERVICES):
        tile = Image.open(DEST / f"{slug}.png")
        col, row = i % 3, i // 3
        modules.paste(tile, (col * 640, row * 360))
    modules.save(DEST / "modules-grid.png", optimize=True)
    print("generated conceptual Consultoría TI assets into", DEST)


if __name__ == "__main__":
    main()
