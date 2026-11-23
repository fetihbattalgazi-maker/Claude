"""Thumbnails for the sleep short: vertical Shorts cover (1080x1920) and 16:9 (1280x720)."""
import math, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import engine as E
from engine import P, txt, pill, icon, YEL, WHITE, RED, DARK, CYAN
for name, code in [('sleepy', '1f634'), ('brain', '1f9e0'), ('zzz', '1f4a4')]: E.load_icon(name, code)
PURPLE = (167, 139, 250)

def glow(d, x, y, r, col):
    for k in range(8, 0, -1):
        rr = r * (1 + k * 0.35); d.ellipse([P(x - rr), P(y - rr), P(x + rr), P(y + rr)], fill=col + (16 + (8 - k) * 6,))
    d.ellipse([P(x - r), P(y - r), P(x + r), P(y + r)], fill=col + (255,))

def vertical():
    fr = E.bg(); d = ImageDraw.Draw(fr, 'RGBA'); E.watermark(d)
    txt(d, 'WHY DO YOU', 540, 290, 110, WHITE, stroke=7, shadow=True)
    txt(d, 'GET SLEEPY?', 540, 420, 120, PURPLE, stroke=8, shadow=True)
    icon(fr, 'sleepy', 540, 800, 470); icon(fr, 'zzz', 800, 560, 200)
    icon(fr, 'brain', 300, 1230, 260)
    d.rounded_rectangle([P(285), P(1320), P(325), P(1420)], radius=P(18), fill=(244, 160, 180, 255))
    glow(d, 305, 1400, 22, CYAN)
    txt(d, 'SCIENTISTS', 720, 1180, 64, WHITE, stroke=5, shadow=True)
    txt(d, 'FOUND THE', 720, 1260, 64, WHITE, stroke=5, shadow=True)
    txt(d, 'SLEEP CELLS', 720, 1345, 72, YEL, stroke=6, shadow=True)
    pill(d, 'SHUT THEM OFF = -70% SLEEP', 540, 1600, 52, RED, WHITE)
    fr.resize((1080, 1920), Image.LANCZOS).save(os.path.join(HERE, 'out', 'cover_shorts_1080x1920.png'))

def horizontal():
    W, H = 1280, 720
    big = E.bg().resize((W * E.S, int(W * E.S * 1920 / 1080)), Image.LANCZOS).crop((0, 600 * E.S, W * E.S, 600 * E.S + H * E.S))
    d = ImageDraw.Draw(big, 'RGBA')
    txt(d, 'WHY DO YOU', 360, 140, 86, WHITE, stroke=6, shadow=True)
    txt(d, 'GET SLEEPY?', 360, 250, 94, PURPLE, stroke=7, shadow=True)
    txt(d, 'THE SLEEP CELLS', 360, 370, 66, YEL, stroke=5, shadow=True)
    pill(d, '-70% SLEEP', 360, 490, 58, RED, WHITE)
    icon(big, 'sleepy', 990, 360, 440); icon(big, 'zzz', 1180, 150, 170)
    big.resize((W, H), Image.LANCZOS).save(os.path.join(HERE, 'out', 'cover_1280x720.png'))

vertical(); horizontal(); print('covers ok')
