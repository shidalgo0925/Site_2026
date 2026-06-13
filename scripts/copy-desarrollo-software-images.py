"""Generate conceptual Desarrollo de Software illustrations (no flyer crops)."""
from __future__ import annotations

import math
import shutil
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    Image = None  # type: ignore
    ImageDraw = None  # type: ignore
    ImageFont = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets" / "images" / "desarrollo-software"
FLYER_SRC = ROOT / "imagenes" / "111.png"
FLYER_FALLBACK = ROOT / "imagenes" / "11.png"
FLYER_DEST = ROOT / "assets" / "images" / "flyers" / "desarrollo-software.png"

NAVY = (15, 23, 42)       # #0f172a
INDIGO = (99, 102, 241)   # #6366f1
CYAN = (6, 182, 212)      # #06b6d4
PURPLE = (139, 92, 246)   # #8b5cf6
WHITE = (255, 255, 255)
LIGHT = (238, 242, 255)   # #eef2ff
MUTED = (100, 116, 139)
SOFT = (199, 210, 254)

INCLUDES = [
    ("inc-web", "Aplicaciones web", "browser"),
    ("inc-mobile", "Apps móviles", "mobile"),
    ("inc-apis", "APIs e integraciones", "api"),
    ("inc-ai", "IA y automatización", "ai"),
    ("inc-saas", "Plataformas SaaS", "cloud"),
    ("inc-dashboards", "Dashboards e BI", "chart"),
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


def draw_browser(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    draw.rounded_rectangle((cx - 70, cy - 48, cx + 70, cy + 48), radius=10, fill=WHITE, outline=INDIGO, width=2)
    draw.rectangle((cx - 70, cy - 48, cx + 70, cy - 24), fill=INDIGO)
    for dx in (-48, -32, -16):
        draw.ellipse((cx + dx - 4, cy - 40, cx + dx + 4, cy - 32), fill=SOFT)
    for i, color in enumerate([CYAN, PURPLE, INDIGO, SOFT]):
        draw.rounded_rectangle((cx - 58, cy - 8 + i * 14, cx + 40, cy + 4 + i * 14), radius=4, fill=color)


def draw_mobile(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    draw.rounded_rectangle((cx - 34, cy - 56, cx + 34, cy + 56), radius=16, fill=NAVY, outline=INDIGO, width=3)
    draw.rounded_rectangle((cx - 26, cy - 44, cx + 26, cy + 40), radius=8, fill=WHITE)
    draw.ellipse((cx - 8, cy + 44, cx + 8, cy + 52), fill=SOFT)
    draw.rounded_rectangle((cx - 18, cy - 30, cx + 18, cy - 6), radius=6, fill=CYAN)
    draw.rounded_rectangle((cx - 18, cy + 2, cx + 18, cy + 26), radius=6, fill=PURPLE)


def draw_api(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    for ox, color in [(-72, INDIGO), (72, PURPLE)]:
        draw.rounded_rectangle((cx + ox - 36, cy - 28, cx + ox + 36, cy + 28), radius=10, fill=color)
        draw.text((cx + ox - 22, cy - 10), "API", fill=WHITE, font=find_font(16, bold=True))
    draw.line([(cx - 36, cy), (cx + 36, cy)], fill=CYAN, width=4)
    draw.polygon([(cx + 28, cy - 8), (cx + 44, cy), (cx + 28, cy + 8)], fill=CYAN)
    draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=WHITE, outline=CYAN, width=2)


def draw_ai(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    draw.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), fill=PURPLE, outline=WHITE, width=2)
    for i in range(6):
        a = i * math.pi / 3
        x1 = cx + math.cos(a) * 28
        y1 = cy + math.sin(a) * 28
        x2 = cx + math.cos(a) * 52
        y2 = cy + math.sin(a) * 52
        draw.line([(x1, y1), (x2, y2)], fill=CYAN, width=3)
        draw.ellipse((x2 - 6, y2 - 6, x2 + 6, y2 + 6), fill=CYAN)
    draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=WHITE)


def draw_cloud(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    draw.ellipse((cx - 52, cy - 8, cx - 8, cy + 28), fill=SOFT, outline=INDIGO, width=2)
    draw.ellipse((cx - 28, cy - 22, cx + 18, cy + 24), fill=WHITE, outline=INDIGO, width=2)
    draw.ellipse((cx + 4, cy - 10, cx + 48, cy + 26), fill=SOFT, outline=INDIGO, width=2)
    draw.polygon([(cx - 8, cy + 18), (cx + 8, cy + 34), (cx + 24, cy + 18)], fill=INDIGO)


def draw_chart(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    base_y = cy + 36
    bars = [(cx - 48, 28, INDIGO), (cx - 16, 44, CYAN), (cx + 16, 34, PURPLE), (cx + 48, 52, INDIGO)]
    for x, height, color in bars:
        draw.rectangle((x - 12, base_y - height, x + 12, base_y), fill=color, outline=WHITE, width=1)
    draw.line([(cx - 62, base_y), (cx + 62, base_y)], fill=NAVY, width=3)
    draw.line([(cx - 62, base_y - 58), (cx - 62, base_y)], fill=NAVY, width=3)


def draw_code(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    draw.rounded_rectangle((cx - 8, cy - 8, cx + 8, cy + 8), fill=CYAN)
    draw.polygon([(cx - 28, cy), (cx - 12, cy - 16), (cx - 12, cy + 16)], fill=INDIGO)
    draw.polygon([(cx + 28, cy), (cx + 12, cy - 16), (cx + 12, cy + 16)], fill=PURPLE)


def draw_icon(draw: ImageDraw.ImageDraw, kind: str, cx: int, cy: int) -> None:
    drawers = {
        "browser": draw_browser,
        "mobile": draw_mobile,
        "api": draw_api,
        "ai": draw_ai,
        "cloud": draw_cloud,
        "chart": draw_chart,
        "code": draw_code,
    }
    drawers[kind](draw, cx, cy)


def make_include_card(slug: str, title: str, icon: str) -> None:
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
    title_font = find_font(26, bold=True)
    sub_font = find_font(17)
    mono = find_font(15)

    draw.rounded_rectangle((32, 40, 520, 500), radius=20, fill=NAVY, outline=SOFT, width=2)
    draw.rectangle((32, 40, 520, 78), fill=(30, 41, 59))
    for i, c in enumerate([CYAN, PURPLE, INDIGO]):
        draw.ellipse((52 + i * 22, 52, 64 + i * 22, 64), fill=c)
    draw.text((88, 48), "app.py — EasyTech", fill=SOFT, font=sub_font)

    code_lines = [
        ("def ", "build_solution", "(client):"),
        ("    stack ", "= ", "[\"Python\", \"Flutter\", \"Odoo\"]"),
        ("    return ", "integrate", "(ecosystem=True)"),
    ]
    colors = [CYAN, PURPLE, WHITE, INDIGO, CYAN, SOFT]
    y = 110
    for parts in code_lines:
        x = 56
        idx = 0
        for part in parts:
            draw.text((x, y), part, fill=colors[idx % len(colors)], font=mono)
            bbox = draw.textbbox((x, y), part, font=mono)
            x = bbox[2] + 2
            idx += 1
        y += 34

    draw.rounded_rectangle((56, 230, 496, 470), radius=12, fill=(30, 41, 59), outline=SOFT, width=1)
    draw.text((76, 250), "Pipeline de entrega", fill=WHITE, font=sub_font)
    steps = ["Diseño", "Desarrollo", "QA", "Deploy"]
    sx = 90
    for i, step in enumerate(steps):
        draw.ellipse((sx - 12, 300, sx + 12, 324), fill=[INDIGO, CYAN, PURPLE, INDIGO][i])
        if i < 3:
            draw.line([(sx + 12, 312), (sx + 68, 312)], fill=SOFT, width=3)
        bbox = draw.textbbox((0, 0), step, font=mono)
        draw.text((sx - (bbox[2] - bbox[0]) // 2, 338), step, fill=SOFT, font=mono)
        sx += 96

    draw.rounded_rectangle((560, 48, 928, 492), radius=20, fill=WHITE, outline=SOFT, width=2)
    draw.text((590, 78), "Conectado al ecosistema", fill=NAVY, font=title_font)
    draw.text((590, 112), "EasyTech", fill=INDIGO, font=title_font)

    hubs = [
        (744, 200, "EasyNodeOne", INDIGO),
        (660, 300, "Easy Odoo", CYAN),
        (828, 300, "Easy Converso", PURPLE),
        (744, 400, "APIs / DGI", NAVY),
    ]
    draw.ellipse((724, 268, 764, 308), fill=INDIGO)
    draw.text((734, 278), "ET", fill=WHITE, font=find_font(14, bold=True))
    for hx, hy, label, color in hubs:
        draw.rounded_rectangle((hx - 58, hy - 22, hx + 58, hy + 22), radius=10, fill=color)
        bbox = draw.textbbox((0, 0), label, font=mono)
        tw = bbox[2] - bbox[0]
        draw.text((hx - tw // 2, hy - 8), label, fill=WHITE, font=mono)
        draw.line([(744, 288), (hx, hy - 22)], fill=SOFT, width=2)

    draw_icon(draw, "code", 744, 180)

    img.save(DEST / "hero.png", optimize=True)
    shutil.copy2(DEST / "hero.png", DEST / "hero-card.png")


def make_tech_stack() -> None:
    w, h = 960, 280
    img = gradient_bg(w, h, WHITE, LIGHT)
    draw = ImageDraw.Draw(img)
    font = find_font(22, bold=True)
    tag_font = find_font(18, bold=True)
    draw.text((48, 36), "Stack moderno y mantenible", fill=NAVY, font=font)

    tags = [
        "Python", "Flask", "FastAPI", "Flutter", "Odoo",
        "PostgreSQL", "IA generativa", "APIs", "Cloud",
    ]
    colors = [INDIGO, CYAN, PURPLE, INDIGO, CYAN, PURPLE, INDIGO, CYAN, PURPLE]
    x, y = 48, 100
    for tag, color in zip(tags, colors):
        bbox = draw.textbbox((0, 0), tag, font=tag_font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pad_x, pad_y = 18, 12
        if x + tw + pad_x * 2 > w - 48:
            x = 48
            y += th + pad_y * 2 + 16
        draw.rounded_rectangle((x, y, x + tw + pad_x * 2, y + th + pad_y * 2), radius=999, fill=color)
        draw.text((x + pad_x, y + pad_y), tag, fill=WHITE, font=tag_font)
        x += tw + pad_x * 2 + 16

    draw.rounded_rectangle((48, 210, 912, 256), radius=12, fill=WHITE, outline=SOFT, width=2)
    draw.text((64, 224), "Integración nativa con EasyNodeOne · Easy Converso · Easy Odoo", fill=MUTED, font=find_font(16))
    img.save(DEST / "tech-stack.png", optimize=True)


def make_delivery_process() -> None:
    w, h = 960, 200
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((8, 8, w - 8, h - 8), radius=16, fill=LIGHT, outline=SOFT, width=2)
    steps = ["Descubrimiento", "Prototipo", "Desarrollo", "Entrega"]
    icons = ["chart", "browser", "code", "cloud"]
    slot = w // 4
    font = find_font(18, bold=True)
    for i, (step, icon) in enumerate(zip(steps, icons)):
        cx = slot * i + slot // 2
        draw.ellipse((cx - 28, 36, cx + 28, 92), fill=WHITE, outline=INDIGO, width=2)
        draw_icon(draw, icon, cx, 64)
        bbox = draw.textbbox((0, 0), step, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, 118), step, fill=NAVY, font=font)
        if i < 3:
            draw.line([(cx + 34, 64), (cx + slot - 34, 64)], fill=INDIGO, width=3)
    img.save(DEST / "delivery-process.png", optimize=True)


def copy_flyer_only() -> None:
    src = FLYER_SRC if FLYER_SRC.is_file() else FLYER_FALLBACK
    if src.is_file():
        shutil.copy2(src, DEST / "flyer-full.png")
        FLYER_DEST.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, FLYER_DEST)


def main() -> None:
    if Image is None:
        raise SystemExit("Pillow required: pip install pillow")
    DEST.mkdir(parents=True, exist_ok=True)
    copy_flyer_only()
    make_hero()
    make_tech_stack()
    make_delivery_process()
    for slug, title, icon in INCLUDES:
        make_include_card(slug, title, icon)

    modules = Image.new("RGB", (640 * 3, 360 * 2), LIGHT)
    for i, (slug, _, _) in enumerate(INCLUDES):
        tile = Image.open(DEST / f"{slug}.png")
        col, row = i % 3, i // 3
        modules.paste(tile, (col * 640, row * 360))
    modules.save(DEST / "modules-grid.png", optimize=True)
    print("generated conceptual Desarrollo de Software assets into", DEST)


if __name__ == "__main__":
    main()
