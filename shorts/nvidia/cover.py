"""Thumbnails for the Nvidia short: vertical Shorts cover (1080x1920) and 16:9 (1280x720). No logos, no likeness."""
import math, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import engine as E
from engine import P, txt, pill, icon, YEL, WHITE, RED, DARK, GRAY
for name, code in [('ceo', '1f9d1-200d-1f4bc'), ('chair', '1fa91')]: E.load_icon(name, code)
NG = (118, 185, 0)

def spike(d, x0, y0, x1, y1, w=14):
    n = 30; pts = []
    for i in range(n + 1):
        f = i / n; v = 0.78 - 0.5 * f + 0.04 * math.sin(i * 1.9)
        pts.append((x0 + (x1 - x0) * 0.72 * f, y1 - (y1 - y0) * v))
    up = [(pts[-1][0] + (x1 - x0) * 0.28 * k / 6, y1 - (y1 - y0) * (0.28 + 0.7 * (k / 6) ** 0.6)) for k in range(7)]
    d.line([(P(x), P(y)) for x, y in pts], fill=RED + (255,), width=P(w), joint='curve')
    d.line([(P(x), P(y)) for x, y in up], fill=NG + (255,), width=P(w + 4), joint='curve')
    (xa, ya), (xb, yb) = up[-2], up[-1]; a = math.atan2(yb - ya, xb - xa); s = 46
    d.polygon([(P(xb + math.cos(a) * 16), P(yb + math.sin(a) * 16)), (P(xb - s * math.cos(a - 0.55)), P(yb - s * math.sin(a - 0.55))),
               (P(xb - s * math.cos(a + 0.55)), P(yb - s * math.sin(a + 0.55)))], fill=NG + (255,))

def vertical():
    fr = E.bg(); d = ImageDraw.Draw(fr, 'RGBA')
    E.watermark(d)
    txt(d, 'NVIDIA', 540, 300, 150, NG, stroke=8, shadow=True)
    txt(d, 'CEO QUIT...', 540, 450, 110, WHITE, stroke=7, shadow=True)
    icon(fr, 'chair', 330, 800, 330); icon(fr, 'ceo', 760, 760, 330)
    d.rounded_rectangle([P(80), P(1010), P(1000), P(1440)], radius=P(30), fill=(0, 0, 0, 120), outline=(255, 255, 255, 60), width=P(3))
    spike(d, 130, 1050, 960, 1400)
    txt(d, '+25%', 790, 1110, 110, NG, stroke=7, shadow=True)
    txt(d, '...THEN CAME BACK', 540, 1560, 84, YEL, stroke=7, shadow=True)
    pill(d, 'IN JUST 11 DAYS', 540, 1700, 60, RED, WHITE)
    fr.resize((1080, 1920), Image.LANCZOS).save(os.path.join(HERE, 'out', 'cover_shorts_1080x1920.png'))

def horizontal():
    W, H = 1280, 720; S = E.S
    big = E.bg().resize((W * S, int(W * S * 1920 / 1080)), Image.LANCZOS).crop((0, 600 * S, W * S, 600 * S + H * S))
    d = ImageDraw.Draw(big, 'RGBA')
    txt(d, 'NVIDIA CEO', 345, 130, 90, NG, stroke=7, shadow=True)
    txt(d, 'QUIT...', 345, 255, 100, WHITE, stroke=7, shadow=True)
    txt(d, '...CAME BACK', 345, 380, 80, YEL, stroke=6, shadow=True)
    pill(d, 'IN 11 DAYS', 345, 500, 54, RED, WHITE)
    icon(big, 'ceo', 980, 210, 300)
    d.rounded_rectangle([P(700), P(380), P(1250), P(690)], radius=P(24), fill=(0, 0, 0, 130))
    spike(d, 720, 400, 1230, 670, w=11)
    txt(d, '+25%', 1105, 445, 80, NG, stroke=6, shadow=True)
    big.resize((W, H), Image.LANCZOS).save(os.path.join(HERE, 'out', 'cover_1280x720.png'))

vertical(); horizontal(); print('covers ok')
