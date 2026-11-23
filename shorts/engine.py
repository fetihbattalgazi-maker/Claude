"""LogicCoreLab shorts engine: 4K vertical (2160x3840) frame renderer with brand look,
animated Turkish subtitles and parallel chunked encoding. Design coordinates are 1080x1920."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
S = 2; W, H = 1080 * S, 1920 * S; FPS = 30
FONT = os.path.join(HERE, 'assets', 'Montserrat-ExtraBold.ttf')
BG1 = (9, 13, 34); BG2 = (24, 30, 72)
CYAN = (34, 211, 238); YEL = (250, 204, 21); ROSE = (214, 40, 80); GOLD = (245, 184, 64)
WHITE = (255, 255, 255); RED = (239, 68, 68); GREEN = (74, 222, 128); DARK = (18, 16, 40); GRAY = (148, 156, 180)
PEOPLE = [(56, 189, 248), (250, 204, 21), (244, 114, 182), (74, 222, 128), (167, 139, 250), (251, 146, 60)]

_fc = {}
def font(sz):
    k = max(2, int(sz * S))
    if k not in _fc: _fc[k] = ImageFont.truetype(FONT, k)
    return _fc[k]
def P(v): return int(round(v * S))
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, dur): return clamp((t - t0) / dur) if dur > 0 else float(t >= t0)
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def back(x):
    x = clamp(x)
    if x <= 0: return 0.0
    c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def pulse(t, f=1.4): return 0.65 + 0.35 * math.sin(2 * math.pi * f * t)

# ---------- icons (Twemoji, CC-BY 4.0) ----------
_raw, _ic = {}, {}
def load_icon(name, code): _raw[name] = Image.open(os.path.join(HERE, 'assets', f'{code}.png')).convert('RGBA')
def icon(fr, name, cx, cy, size, alpha=1.0):
    px = int(size * S)
    if px < 4 or alpha <= 0: return
    key = (name, px)
    if key not in _ic:
        if len(_ic) > 400: _ic.clear()
        _ic[key] = _raw[name].resize((px, px), Image.LANCZOS)
    im = _ic[key]; m = im.getchannel('A')
    if alpha < 1: m = m.point(lambda v: int(v * alpha))
    fr.paste(im, (P(cx) - px // 2, P(cy) - px // 2), m)

# ---------- background ----------
def make_bg():
    bg = Image.new('RGB', (W, H)); d = ImageDraw.Draw(bg)
    for y in range(0, H, 4):
        f = y / H; d.rectangle([0, y, W, y + 4], fill=tuple(int(BG1[k] * (1 - f) + BG2[k] * f) for k in range(3)))
    g = Image.new('RGBA', (W // 8, H // 8), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([W // 8 * 0.05, H // 8 * 0.28, W // 8 * 0.95, H // 8 * 0.68], fill=(70, 100, 255, 70))
    g = g.filter(ImageFilter.GaussianBlur(25)).resize((W, H), Image.BILINEAR)
    bg = Image.alpha_composite(bg.convert('RGBA'), g)
    d = ImageDraw.Draw(bg, 'RGBA'); st = P(60)
    for x in range(0, W, st): d.line([(x, 0), (x, H)], fill=(130, 170, 255, 16), width=2)
    for y in range(0, H, st): d.line([(0, y), (W, y)], fill=(130, 170, 255, 16), width=2)
    return bg.convert('RGB')
BG = None
def bg():
    global BG
    if BG is None: BG = make_bg()
    return BG.copy()

# ---------- drawing helpers ----------
def txt(d, s, cx, cy, sz, fill, alpha=1.0, stroke=0, sfill=DARK, anchor='mm', shadow=False):
    if sz < 2 or alpha <= 0.01: return
    f = font(sz); a = int(255 * clamp(alpha))
    if shadow:
        d.text((P(cx) + P(5), P(cy) + P(6)), s, font=f, fill=(0, 0, 0, int(a * 0.55)), anchor=anchor,
               stroke_width=P(stroke), stroke_fill=(0, 0, 0, int(a * 0.55)))
    d.text((P(cx), P(cy)), s, font=f, fill=fill + (a,), anchor=anchor,
           stroke_width=P(stroke) if stroke else 0, stroke_fill=sfill + (a,))
def text_w(d, s, sz):
    bb = d.textbbox((0, 0), s, font=font(sz)); return (bb[2] - bb[0]) / S
def pill(d, s, cx, cy, sz, bgc, fg, scale=1.0, alpha=1.0):
    if scale <= 0.02 or alpha <= 0: return
    f = font(sz * scale); bb = d.textbbox((0, 0), s, font=f, anchor='mm'); tw = (bb[2] - bb[0]) / S; th = (bb[3] - bb[1]) / S
    px = 26 * scale; py = 16 * scale; A = int(255 * alpha)
    d.rounded_rectangle([P(cx - tw / 2 - px), P(cy - th / 2 - py), P(cx + tw / 2 + px), P(cy + th / 2 + py)],
                        radius=P(th / 2 + py), fill=bgc + (A,))
    txt(d, s, cx, cy, sz * scale, fg, alpha)
def title(d, lines, t, t0=0.05, cy=280, sz=82, colors=None, alpha=1.0):
    p = prog(t, t0, 0.45)
    if p <= 0: return
    s = back(p)
    for i, l in enumerate(lines):
        txt(d, l, 540, cy + i * sz * 1.12, sz * s, (colors[i] if colors else WHITE), alpha * min(1, p * 3), stroke=5, shadow=True)
def watermark(d):
    txt(d, 'LOGICCORELAB', 540, 140, 34, CYAN, 0.8)
    d.rounded_rectangle([P(470), P(168), P(610), P(173)], radius=P(2), fill=CYAN + (150,))
def person(d, cx, cy, size, color, alpha=1.0, outline=None):
    A = int(255 * alpha); r = size * 0.22
    d.ellipse([P(cx - r), P(cy - size * 0.47), P(cx + r), P(cy - size * 0.47 + 2 * r)], fill=color + (A,))
    d.pieslice([P(cx - size * 0.38), P(cy - 0.02 * size), P(cx + size * 0.38), P(cy + size * 0.74)], 180, 360, fill=color + (A,))
    if outline:
        d.ellipse([P(cx - size * 0.62), P(cy - size * 0.62), P(cx + size * 0.62), P(cy + size * 0.5)], outline=outline + (A,), width=P(5))
def outro(fr, d, t, t_logic, t_brand):
    p = prog(t, 0.3, 0.5)
    if p > 0:
        for j in range(12):
            a = math.radians(j * 30 + t * 25); r1, r2 = 230, 300 + 20 * math.sin(t * 4 + j)
            d.line([(P(540 + r1 * math.cos(a)), P(700 + r1 * math.sin(a))), (P(540 + r2 * math.cos(a)), P(700 + r2 * math.sin(a)))],
                   fill=YEL + (int(170 * p),), width=P(10))
    icon(fr, 'bulb', 540, 700, 330 * back(prog(t, 0.05, 0.5)))
    s = back(prog(t, t_logic, 0.45)); txt(d, 'LOGIC > INTUITION', 540, 1010, 76 * s, WHITE, stroke=5, shadow=True)
    s = back(prog(t, t_brand, 0.45)); txt(d, 'LogicCoreLab', 540, 1125, 104 * s, CYAN, stroke=5, shadow=True)
    s = back(prog(t, t_brand + 0.3, 0.45)) * (1 + 0.04 * math.sin(t * 6)); pill(d, 'FOLLOW FOR MORE', 540, 1262, 46, YEL, DARK, s)

# ---------- subtitles ----------
def up_tr(s): return s.replace('i', 'İ').replace('ı', 'I').upper()
def groups(text, maxc=13, maxw=3):
    out, cur = [], []
    for x in text.split():
        if cur and (len(' '.join(cur + [x])) > maxc or len(cur) >= maxw): out.append(' '.join(cur)); cur = []
        cur.append(x)
    if cur: out.append(' '.join(cur))
    return out
def build_subs(items):
    """items: list of (start, end, turkish_text). Returns timed word groups."""
    subs, ci = [], 0
    for a, b, tx in items:
        gs = groups(up_tr(tx)); tot = sum(len(g) for g in gs); tt = a
        for g in gs:
            L = (b - a) * len(g) / tot; subs.append((tt, tt + L, g, ci)); ci += 1; tt += L
    return subs
def draw_sub(d, subs, t, y=1440, base=104):
    for (a, b, g, ci) in subs:
        if a <= t < b:
            age = t - a
            sc = 0.6 + 0.52 * age / 0.11 if age < 0.11 else (1.12 - 0.12 * (age - 0.11) / 0.09 if age < 0.2 else 1.0)
            al = min(1.0, 0.4 + age / 0.08); col = YEL if ci % 2 else WHITE
            w = text_w(d, g, base)
            fit = min(1.0, 980 / w) if w > 0 else 1.0
            sz = base * fit * sc
            txt(d, g, 540, y, sz, col, al, stroke=10 * fit, sfill=(0, 0, 0), shadow=True)
            return

# ---------- encoding ----------
def encode_chunk(frame_fn, a, b, path):
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium',
                          '-crf', '17', '-threads', '2', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-g', '60', path], stdin=subprocess.PIPE)
    for n in range(a, b): p.stdin.write(frame_fn(n / FPS).tobytes())
    p.stdin.close(); p.wait()
