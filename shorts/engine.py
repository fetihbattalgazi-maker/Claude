"""LogicCoreLab shorts engine: 4K vertical (2160x3840) frame renderer with brand look,
animated Turkish subtitles and parallel chunked encoding. Design coordinates are 1080x1920."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

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
def outro(fr, d, t, t_logic, t_brand, tagline='LOGIC > INTUITION'):
    p = prog(t, 0.3, 0.5)
    if p > 0:
        for j in range(12):
            a = math.radians(j * 30 + t * 25); r1, r2 = 230, 300 + 20 * math.sin(t * 4 + j)
            d.line([(P(540 + r1 * math.cos(a)), P(700 + r1 * math.sin(a))), (P(540 + r2 * math.cos(a)), P(700 + r2 * math.sin(a)))],
                   fill=YEL + (int(170 * p),), width=P(10))
    icon(fr, 'bulb', 540, 700, 330 * back(prog(t, 0.05, 0.5)))
    s = back(prog(t, t_logic, 0.45)); txt(d, tagline, 540, 1010, 76 * s, WHITE, stroke=5, shadow=True)
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

# ---------- planets (drawn, not images) ----------
_pl = {}
def planet(fr, cx, cy, r, base, bands, rot=0.0, alpha=1.0, glow=None, glow_a=0.0):
    R = int(r * S)
    if R < 3 or alpha <= 0: return
    size = 2 * R
    if glow and glow_a > 0:
        d = ImageDraw.Draw(fr, 'RGBA')
        for k in range(8, 0, -1):
            e = k * 9; a = int(glow_a * alpha * (46 - k * 5))
            if a > 0: d.ellipse([P(cx - r - e), P(cy - r - e), P(cx + r + e), P(cy + r + e)], fill=glow + (a,))
    layer = Image.new('RGBA', (size, size), base + (255,)); ld = ImageDraw.Draw(layer, 'RGBA')
    nb = len(bands); hgt = size * 0.075
    for k, col in enumerate(bands):
        y = size * (0.08 + 0.84 * k / max(1, nb - 1)); stp = max(2, size // 48)
        top = [(xx, y + math.sin(xx / size * 6.283 * 1.3 + rot + k * 1.7) * hgt * 0.7) for xx in range(0, size + stp, stp)]
        ld.polygon(top + [(xx, yy + hgt) for xx, yy in reversed(top)], fill=col + (150,))
    if R not in _pl:
        sh = Image.new('L', (size, size), 0); ImageDraw.Draw(sh).ellipse([int(size * 0.3), int(size * 0.22), int(size * 1.4), int(size * 1.32)], fill=185)
        sh = sh.filter(ImageFilter.GaussianBlur(size * 0.07))
        hl = Image.new('L', (size, size), 0); ImageDraw.Draw(hl).ellipse([int(size * 0.14), int(size * 0.1), int(size * 0.5), int(size * 0.42)], fill=80)
        hl = hl.filter(ImageFilter.GaussianBlur(size * 0.09))
        circ = Image.new('L', (size, size), 0); ImageDraw.Draw(circ).ellipse([0, 0, size - 1, size - 1], fill=255)
        _pl[R] = (sh, hl, circ)
    sh, hl, circ = _pl[R]
    layer = Image.composite(Image.new('RGBA', (size, size), (6, 6, 24, 255)), layer, sh)
    layer = Image.composite(Image.new('RGBA', (size, size), (255, 255, 255, 255)), layer, hl)
    layer.putalpha(circ if alpha >= 1 else circ.point(lambda v: int(v * alpha)))
    fr.paste(layer, (P(cx) - R, P(cy) - R), layer)

# ---------- timeline + CLI shared by every short ----------
def make_timeline(EN, scenes, audio_dir, lead=0.3, gap=0.3, tail=0.45, gaps=None, end_pad=1.4):
    gaps = gaps or {}
    def adur(i):
        return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                              os.path.join(audio_dir, f'e{i:02d}.mp3')]))
    D = {i: adur(i) for i in EN}; T = {}; st = []; t = 0.0
    for k, sents in enumerate(scenes):
        st.append(t); tt = t + lead
        for j, i in enumerate(sents):
            if j: tt += gaps.get(i, gap)
            T[i] = tt; tt += D[i]
        t = tt + tail + (end_pad if k == len(scenes) - 1 else 0)
    def ev(i, word, occ=0):
        s_ = EN[i].lower(); pos = -1
        for _ in range(occ + 1): pos = s_.find(word.lower(), pos + 1)
        return T[i] + D[i] * clamp(pos / len(s_)) * 0.97 + 0.05
    return T, D, st, t, ev
def subs_from(EN, TR, T, D):
    items = []
    for i in EN:
        end = T[i] + D[i] + 0.3; parts = TR[i].split('|')
        tot = sum(len(p) for p in parts); a = T[i]
        for p_ in parts:
            b = a + (end - T[i]) * len(p_) / tot; items.append((a, b, p_)); a = b
    return build_subs(items)
def make_frame(scene_fns, starts, fade_in, subs, no_wm=(), trf=0.35):
    def scene_abs(k, t):
        fr = bg(); d = ImageDraw.Draw(fr, 'RGBA'); r = scene_fns[k](fr, d, t)
        fr = r if isinstance(r, Image.Image) else fr
        if k not in no_wm: watermark(ImageDraw.Draw(fr, 'RGBA'))
        return fr
    def frame(t):
        k = max(i for i in range(len(starts)) if starts[i] <= t + 1e-9)
        fr = scene_abs(k, t); lt = t - starts[k]
        if k in fade_in and lt < trf: fr = Image.blend(scene_abs(k - 1, starts[k] - 0.001), fr, eio(lt / trf))
        draw_sub(ImageDraw.Draw(fr, 'RGBA'), subs, t)
        return fr
    return frame
def cli(frame, total, here, workers=2):
    from multiprocessing import Process
    out = os.path.join(here, 'out'); os.makedirs(out, exist_ok=True); mode = sys.argv[1]
    if mode == 'preview':
        for ts in sys.argv[2:]: frame(float(ts)).resize((540, 960), Image.LANCZOS).save(os.path.join(out, f'prev_{ts}.jpg'), quality=88)
    elif mode == 'render':
        F = int(total * FPS); step = (F + workers - 1) // workers; ps = []
        for i in range(workers):
            p = Process(target=encode_chunk, args=(frame, i * step, min(F, (i + 1) * step), os.path.join(out, f'chunk_{i}.mp4'))); p.start(); ps.append(p)
        for p in ps: p.join()
        with open(os.path.join(out, 'list.txt'), 'w') as f:
            for i in range(workers): f.write(f"file 'chunk_{i}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-i', os.path.join(out, 'list.txt'), '-c', 'copy',
                        os.path.join(out, 'video_4k.mp4')], check=True)
        print('RENDER_OK', F, 'frames')
def mix(here, T, total, final_name, music_vol=0.5, fx_vol=0.55):
    O = os.path.join(here, 'out'); A = os.path.join(here, 'audio'); ids = sorted(T); inp, fc = [], []
    for i in ids: inp += ['-i', os.path.join(A, f'e{i:02d}.mp3')]
    inp += ['-i', os.path.join(O, 'music.wav'), '-i', os.path.join(O, 'fx.wav')]; n = len(ids)
    for k, i in enumerate(ids):
        ms = int(T[i] * 1000); fc.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms}[n{k}]")
    fc.append(''.join(f'[n{k}]' for k in range(n)) + f"amix=inputs={n}:normalize=0,apad,atrim=0:{total:.2f},asplit=2[vo][sc]")
    fc.append(f"[{n}:a]volume={music_vol},apad,atrim=0:{total:.2f}[m]")
    fc.append("[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md]")
    fc.append(f"[{n + 1}:a]volume={fx_vol},apad,atrim=0:{total:.2f}[fx]")
    fc.append(f"[vo][md][fx]amix=inputs=3:normalize=0,atrim=0:{total:.2f},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *inp, '-filter_complex', ';'.join(fc), '-map', '[a]', '-c:a', 'aac', '-b:a', '192k',
                    '-ar', '48000', os.path.join(O, 'audio.m4a')], check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(O, 'video_4k.mp4'), '-i', os.path.join(O, 'audio.m4a'),
                    '-map', '0:v', '-map', '1:a', '-c', 'copy', '-shortest', '-movflags', '+faststart', os.path.join(O, final_name)], check=True)
    print('FINAL OK', final_name)
