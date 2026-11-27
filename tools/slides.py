"""Генератор слайдов 4015 для Instagram (1080x1350, JPEG).

Использование:
  python3 tools/slides.py spec.json
spec.json:
{
  "out_dir": "2026-11-28",
  "slides": [
    {"name": "post05_1", "num": "1/4", "kicker": "РУБРИКА", "title": "Заголовок\\nв две строки",
     "body": "Короткий текст под заголовком", "foot": "4015.рф"}
  ]
}
num, kicker, body, foot — необязательны. Заголовок: до 2 строк по ~12 символов.
Нужны Pillow и шрифт Inter (/usr/share/fonts/opentype/inter); иначе берётся DejaVu.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

INTER = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
DEJAVU = {"Black": "DejaVuSans-Bold", "ExtraBold": "DejaVuSans-Bold", "Bold": "DejaVuSans-Bold",
          "SemiBold": "DejaVuSans-Bold", "Medium": "DejaVuSans"}

def font(weight, size):
    p = INTER % weight
    if not os.path.exists(p):
        p = "/usr/share/fonts/truetype/dejavu/%s.ttf" % DEJAVU[weight]
    return ImageFont.truetype(p, size)

BG = (18, 53, 40); LINE = (40, 90, 70); LIME = (200, 230, 60); WHITE = (245, 245, 240); GREY = (170, 190, 180)
W, H = 1080, 1350

def base():
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.rectangle([60, 60, W - 60, H - 60], outline=LINE, width=4)
    for y in (H // 2 - 330, H // 2, H // 2 + 330):
        d.line([60, y, W - 60, y], fill=LINE, width=4)
    d.line([W // 2, H // 2 - 330, W // 2, H // 2 + 330], fill=LINE, width=4)
    return im, d

def logo(d, x=100, y=100, s=0.8):
    """Логотип «40:15»: двоеточие — две салатовые точки (мячи)."""
    f = font("Black", int(70 * s))
    d.text((x, y), "40", font=f, fill=WHITE)
    cx = x + d.textlength("40", font=f) + int(16 * s)
    r = int(7 * s)
    top, bottom = d.textbbox((x, y), "40", font=f)[1], d.textbbox((x, y), "40", font=f)[3]
    for cy in (top + (bottom - top) * 0.32, top + (bottom - top) * 0.78):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LIME)
    d.text((cx + r + int(14 * s), y), "15", font=f, fill=LIME)

def wrap(d, text, f, maxw):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split():
            t = (line + " " + w).strip()
            if d.textlength(t, font=f) <= maxw: line = t
            else: out.append(line); line = w
        out.append(line)
    return out

def block(d, y, text, f, fill, gap):
    for l in wrap(d, text, f, W - 200):
        d.text((100, y), l, font=f, fill=fill); y += int(f.size * gap)
    return y

def slide(s, out_dir):
    im, d = base(); logo(d)
    if s.get("num"): d.text((W - 100, 110), s["num"], font=font("SemiBold", 34), fill=GREY, anchor="ra")
    if s.get("kicker"): d.text((100, 330), s["kicker"], font=font("Bold", 46), fill=LIME)
    tsize = 120 if max(len(l) for l in s["title"].split("\n")) <= 12 else 84
    y = block(d, 420, s["title"], font("Black", tsize), WHITE, 1.05)
    d.rectangle([100, y + 30, 220, y + 40], fill=LIME)
    if s.get("body"): block(d, y + 90, s["body"], font("Medium", 46), GREY, 1.35)
    if s.get("foot"): d.text((100, H - 170), s["foot"], font=font("Bold", 44), fill=LIME)
    path = os.path.join(out_dir, s["name"] + ".jpg")
    im.save(path, quality=92); return path

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, spec["out_dir"]); os.makedirs(out, exist_ok=True)
    for s in spec["slides"]: print(slide(s, out))
