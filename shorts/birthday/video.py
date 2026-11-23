"""LogicCoreLab short #2 - The Birthday Paradox. 4K vertical.
python3 video.py info | preview t1 t2 ... | render"""
import json, math, os, random, subprocess, sys
from multiprocessing import Process
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from engine import *
HERE = os.path.dirname(os.path.abspath(__file__))

for name, code in [('cake', '1f382'), ('think', '1f914'), ('cal', '1f4c5'), ('bulb', '1f4a1'), ('party', '1f389')]:
    load_icon(name, code)

EN = {1: "How many people do you need in a room for a fifty percent chance that two of them share a birthday?",
      2: "There are three hundred sixty-five days in a year, so most people guess around one hundred eighty.",
      3: "The real answer?", 4: "Just twenty-three.", 5: "Here's the trick.",
      6: "You're not comparing one person to everyone.", 7: "You're comparing every possible pair.",
      8: "Twenty-three people make two hundred fifty-three different pairs.", 9: "That's a lot of chances for a match.",
      10: "With fifty people, the chance jumps to ninety-seven percent.", 11: "With seventy, it's ninety-nine point nine.",
      12: "Your intuition counts people.", 13: "Math counts pairs.", 14: "Logic beats intuition. Follow LogicCoreLab for more."}
TR = {1: "Bir odada kaç kişi olmalı ki, ikisinin aynı gün doğmuş olma ihtimali %50 olsun?",
      2: "Bir yılda 365 gün var, bu yüzden çoğu kişi 180 civarı der.",
      3: "Gerçek cevap mı?", 4: "Sadece 23!", 5: "İşin sırrı şu:",
      6: "Bir kişiyi herkesle karşılaştırmıyorsun.", 7: "Olası her ikiliyi karşılaştırıyorsun.",
      8: "23 kişi, 253 farklı ikili oluşturur.", 9: "Bu, eşleşme için çok fazla şans demek.",
      10: "50 kişide ihtimal %97'ye çıkar.", 11: "70 kişide ise %99,9.",
      12: "Sezgin insanları sayar.", 13: "Matematik ise ikilileri.",
      14: "Mantık sezgiyi yener.|Daha fazlası için LogicCoreLab'i takip et!"}
SCENES_S = [[1], [2], [3, 4], [5, 6, 7], [8, 9], [10, 11], [12, 13], [14]]
LEAD, GAP, TAIL = 0.3, 0.3, 0.45
GAPS = {4: 0.75}  # dramatic pause before "Just twenty-three"
FADE_IN = {1, 2, 3, 5, 6, 7}
TRF = 0.35

def adur(i):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                          os.path.join(HERE, 'audio', f'e{i:02d}.mp3')]))
D = {i: adur(i) for i in EN}
T = {}; SC_START = []; SC_DUR = []; t = 0.0
for k, sents in enumerate(SCENES_S):
    SC_START.append(t); tt = t + LEAD
    for j, i in enumerate(sents):
        if j: tt += GAPS.get(i, GAP)
        T[i] = tt; tt += D[i]
    end = tt + TAIL + (1.4 if k == len(SCENES_S) - 1 else 0)
    SC_DUR.append(end - t); t = end
TOTAL = t
def ev(i, word, occ=0):
    s = EN[i].lower(); pos = -1
    for _ in range(occ + 1): pos = s.find(word.lower(), pos + 1)
    return T[i] + D[i] * clamp(pos / len(s)) * 0.97 + 0.05

# ---------- scene helpers ----------
RC, RR, PS = (540, 850), 340, 84
RING = [(RC[0] + RR * math.cos(math.radians(-90 + i * 360 / 23)), RC[1] + RR * math.sin(math.radians(-90 + i * 360 / 23))) for i in range(23)]
PAIRS = [(a, b) for a in range(23) for b in range(a + 1, 23)]
random.Random(3).shuffle(PAIRS)
FLASH = [(1, 9), (4, 17), (12, 20), (6, 14), (2, 11)]
MATCH = (5, 16)

def ring(fr, d, lt0, t, lines_from0=0.0, all_lines=0.0, highlight0=0.0, flash_t0=None, match_t=None):
    n_all = int(253 * all_lines)
    for a, b in PAIRS[:n_all]:
        (x1, y1), (x2, y2) = RING[a], RING[b]
        d.line([(P(x1), P(y1)), (P(x2), P(y2))], fill=(140, 180, 255, 60), width=P(2))
    if lines_from0 > 0:
        n0 = int(22 * lines_from0)
        for b in range(1, 1 + n0):
            (x1, y1), (x2, y2) = RING[0], RING[b]
            d.line([(P(x1), P(y1)), (P(x2), P(y2))], fill=YEL + (int(220 * (1 - all_lines * 0.7)),), width=P(4))
    if flash_t0 is not None:
        for k, (a, b) in enumerate(FLASH):
            f = prog(t, flash_t0 + k * 0.28, 0.12) * (1 - prog(t, flash_t0 + k * 0.28 + 0.3, 0.2))
            if f > 0:
                (x1, y1), (x2, y2) = RING[a], RING[b]
                d.line([(P(x1), P(y1)), (P(x2), P(y2))], fill=YEL + (int(255 * f),), width=P(6))
    mm = prog(t, match_t, 0.25) if match_t is not None else 0
    if mm > 0:
        (x1, y1), (x2, y2) = RING[MATCH[0]], RING[MATCH[1]]
        d.line([(P(x1), P(y1)), (P(x2), P(y2))], fill=(244, 114, 182, int(255 * mm)), width=P(9))
    for i, (x, y) in enumerate(RING):
        s = back(prog(t, lt0 + i * 0.04, 0.35))
        if s <= 0.01: continue
        out = None
        if i == 0 and highlight0 > 0: out = YEL
        if mm > 0 and i in MATCH: out = (244, 114, 182)
        person(d, x, y, PS * s, PEOPLE[i % len(PEOPLE)], outline=out)
    if mm > 0:
        for i in MATCH:
            x, y = RING[i]; icon(fr, 'cake', x, y - 78, 64 * back(mm) * (0.9 + 0.1 * pulse(t, 2)))

def s1(fr, d, t):
    title(d, ['THE BIRTHDAY', 'PARADOX'], t, colors=[WHITE, YEL])
    icon(fr, 'cake', 540, 830, 250 * back(prog(t, 0.3, 0.5)))
    tp = ev(1, 'people'); ts = ev(1, 'share')
    for i in range(10):
        a = math.radians(-90 + i * 36); x = 540 + 330 * math.cos(a); y = 830 + 300 * math.sin(a)
        s = back(prog(t, tp + i * 0.1, 0.35))
        if s > 0.01:
            hl = i in (2, 7) and t >= ts
            person(d, x, y, 105 * s, PEOPLE[i % len(PEOPLE)], outline=YEL if hl else None)
            if hl: icon(fr, 'cake', x, y - 95, 62 * back(prog(t, ts, 0.35)) * (0.9 + 0.1 * pulse(t, 2)))
    pill(d, '50% CHANCE?', 540, 1240, 52, YEL, DARK, back(prog(t, ev(1, 'fifty'), 0.4)))
def s2(fr, d, t):
    title(d, ['365 DAYS...'], t, t0=SC_START[1] + 0.05, colors=[WHITE])
    icon(fr, 'cal', 540, 680, 280 * back(prog(t, SC_START[1] + 0.1, 0.5)))
    c = eo(prog(t, T[2], ev(2, 'days') + 0.2 - T[2]))
    if c > 0:
        txt(d, str(round(365 * c)), 540, 960, 160, WHITE, stroke=6, shadow=True)
        txt(d, 'DAYS', 540, 1070, 54, CYAN, stroke=3)
    tm = ev(2, 'most')
    icon(fr, 'think', 330, 1225, 120 * back(prog(t, tm, 0.4)))
    txt(d, '~180 ?', 610, 1230, 110 * back(prog(t, tm + 0.15, 0.4)), YEL, stroke=5, shadow=True)
def rays(d, t, cx, cy, p, r1=250, r2=330, n=14, color=YEL):
    if p <= 0: return
    for j in range(n):
        a = math.radians(j * 360 / n + t * 30); rr = r2 + 25 * math.sin(t * 5 + j)
        d.line([(P(cx + r1 * math.cos(a)), P(cy + r1 * math.sin(a))), (P(cx + rr * math.cos(a)), P(cy + rr * math.sin(a)))],
               fill=color + (int(170 * p),), width=P(10))
def s3(fr, d, t):
    t4 = T[4]
    if t < t4 + 0.1:
        a = 1 - prog(t, t4 - 0.05, 0.15)
        txt(d, '?', 540, 830, 380 * back(prog(t, SC_START[2] + 0.15, 0.5)) * (0.95 + 0.05 * pulse(t, 2.5)), WHITE, a, stroke=8, shadow=True)
    p = prog(t, t4, 0.4)
    if p > 0:
        rays(d, t, 540, 800, p)
        txt(d, '23', 540, 800, 400 * back(p), YEL, stroke=10, shadow=True)
        txt(d, 'PEOPLE', 540, 1165, 72 * back(prog(t, t4 + 0.25, 0.4)), WHITE, stroke=4, shadow=True)
        pill(d, '≈ 50.7% MATCH', 540, 1275, 46, CYAN, DARK, back(prog(t, t4 + 0.6, 0.4)))
def s4(fr, d, t):
    title(d, ['THE TRICK'], t, t0=SC_START[3] + 0.05, colors=[YEL])
    l0 = eio(prog(t, T[6] + 0.2, D[6] * 0.8)); la = eio(prog(t, T[7] + 0.1, D[7] + 0.3))
    ring(fr, d, T[5] - 0.1, t, lines_from0=l0, all_lines=la, highlight0=prog(t, T[6], 0.2))
    if t < T[7] + 0.1: pill(d, '1 vs 22', 540, 1265, 48, YEL, DARK, back(prog(t, T[6] + 0.3, 0.4)))
    else: pill(d, 'EVERY PAIR', 540, 1265, 48, CYAN, DARK, back(prog(t, T[7] + 0.1, 0.4)))
def s5(fr, d, t):
    title(d, ['THE TRICK'], t, t0=-1, colors=[YEL])
    ring(fr, d, -9, t, all_lines=1.0, flash_t0=T[9] + 0.05, match_t=T[9] + D[9] * 0.7)
    d.ellipse([P(540 - 165), P(850 - 165), P(540 + 165), P(850 + 165)], fill=(10, 12, 32, 235), outline=YEL + (255,), width=P(6))
    c = eo(prog(t, T[8], D[8] * 0.85))
    txt(d, str(round(253 * c)), 540, 830, 128, YEL, stroke=5)
    txt(d, 'PAIRS', 540, 920, 44, WHITE)
    pill(d, 'MATCH!', 540, 1265, 52, (244, 114, 182), DARK, back(prog(t, T[9] + D[9] * 0.7, 0.4)))
def prob(n):
    p = 1.0
    for k in range(int(n)): p *= (365 - k) / 365
    return 1 - p
GX0, GX1, GY0, GY1 = 160, 960, 560, 1180
def gx(n): return GX0 + (GX1 - GX0) * n / 80
def gy(p): return GY1 - (GY1 - GY0) * p
def s6(fr, d, t):
    title(d, ['CHANCE OF A MATCH'], t, t0=SC_START[5] + 0.05, sz=70, colors=[WHITE])
    a = prog(t, SC_START[5] + 0.1, 0.3); A = int(255 * a)
    for pv, lab in [(0.5, '50%'), (1.0, '100%')]:
        y = gy(pv); x = GX0
        while x < GX1: d.line([(P(x), P(y)), (P(min(x + 16, GX1)), P(y))], fill=(255, 255, 255, int(70 * a)), width=P(2)); x += 30
        txt(d, lab, GX0 - 18, y, 32, GRAY, a, anchor='rm')
    d.line([(P(GX0), P(GY0 - 20)), (P(GX0), P(GY1)), (P(GX1 + 20), P(GY1))], fill=(255, 255, 255, A), width=P(5))
    for n in (0, 20, 40, 60, 80): txt(d, str(n), gx(n), GY1 + 38, 32, GRAY, a)
    txt(d, 'PEOPLE IN THE ROOM', 560, GY1 + 95, 34, CYAN, a)
    cp = eio(prog(t, SC_START[5] + 0.3, 2.0)); nmax = 80 * cp
    if nmax > 0.5:
        pts = [(gx(n), gy(prob(n))) for n in [x * 0.5 for x in range(int(nmax * 2) + 1)]]
        d.polygon([(P(x), P(y)) for x, y in pts] + [(P(pts[-1][0]), P(GY1)), (P(GX0), P(GY1))], fill=YEL + (40,))
        d.line([(P(x), P(y)) for x, y in pts], fill=YEL + (255,), width=P(9), joint='curve')
    for n, pv, lab, t0, lx, ly in [(23, 0.507, '23 → 50.7%', SC_START[5] + 1.0, 140, 10), (50, 0.970, '50 → 97%', ev(10, 'ninety'), 130, 70),
                                   (70, 0.999, '70 → 99.9%', ev(11, 'ninety'), -60, -75)]:
        s = back(prog(t, t0, 0.4))
        if s <= 0.01: continue
        x, y = gx(n), gy(pv)
        yy = y
        while yy < GY1: d.line([(P(x), P(yy)), (P(x), P(min(yy + 12, GY1)))], fill=CYAN + (160,), width=P(3)); yy += 24
        r = 15 * s; d.ellipse([P(x - r), P(y - r), P(x + r), P(y + r)], fill=CYAN + (255,), outline=WHITE + (255,), width=P(4))
        pill(d, lab, x + lx, y + ly, 36, CYAN, DARK, s)
def card(d, cy, label, sub, num, color, s, glow=False):
    if s <= 0.01: return
    h = 250 * s; w = 820 * s; x0, x1 = 540 - w / 2, 540 + w / 2
    if glow:
        for k in range(4, 0, -1):
            e = k * 8; d.rounded_rectangle([P(x0 - e), P(cy - h / 2 - e), P(x1 + e), P(cy + h / 2 + e)], radius=P(40 + e), outline=color + (60 - k * 12,), width=P(6))
    d.rounded_rectangle([P(x0), P(cy - h / 2), P(x1), P(cy + h / 2)], radius=P(40), fill=(255, 255, 255, 24), outline=color + (255,), width=P(5))
    txt(d, label, x0 + 50 * s, cy - 35 * s, 58 * s, color, anchor='lm', stroke=3)
    txt(d, sub, x0 + 50 * s, cy + 45 * s, 34 * s, GRAY, anchor='lm')
    txt(d, num, x1 - 50 * s, cy, 140 * s, color, anchor='rm', stroke=5, shadow=True)
def s7(fr, d, t):
    title(d, ['PEOPLE vs PAIRS'], t, t0=SC_START[6] + 0.05, colors=[WHITE])
    card(d, 720, 'INTUITION', 'COUNTS PEOPLE', '23', GRAY, back(prog(t, T[12], 0.45)))
    card(d, 1040, 'MATH', 'COUNTS PAIRS', '253', YEL, back(prog(t, T[13], 0.45)), glow=True)
    if t > T[13] + 0.5: icon(fr, 'party', 900, 905, 110 * back(prog(t, T[13] + 0.5, 0.4)))
def s8(fr, d, t): outro(fr, d, t - SC_START[7], T[14] - SC_START[7], T[14] - SC_START[7] + D[14] * 0.45)

SCN = [s1, s2, s3, s4, s5, s6, s7, s8]
# scene functions take absolute time t (sentence times T are absolute)
def scene_abs(k, t):
    fr = bg(); d = ImageDraw.Draw(fr, 'RGBA')
    SCN[k](fr, d, t)
    if k != 7: watermark(d)
    return fr

items = []
for i in EN:
    end = T[i] + D[i] + 0.3
    parts = TR[i].split('|')
    if len(parts) == 1: items.append((T[i], end, parts[0]))
    else:
        tot = sum(len(p) for p in parts); a = T[i]
        for p_ in parts:
            b = a + (end - T[i]) * len(p_) / tot; items.append((a, b, p_)); a = b
SUBS = build_subs(items)

def frame(t):
    k = max(i for i in range(len(SC_START)) if SC_START[i] <= t + 1e-9)
    fr = scene_abs(k, t)
    lt = t - SC_START[k]
    if k in FADE_IN and lt < TRF:
        fr = Image.blend(scene_abs(k - 1, SC_START[k] - 0.001), fr, eio(lt / TRF))
    draw_sub(ImageDraw.Draw(fr, 'RGBA'), SUBS, t)
    return fr

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'info':
        print(json.dumps({'total': TOTAL, 'frames': int(TOTAL * FPS), 'scene_starts': SC_START, 'T': T, 'D': D}, indent=0))
    elif mode == 'preview':
        os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
        for ts in sys.argv[2:]:
            frame(float(ts)).resize((540, 960), Image.LANCZOS).save(os.path.join(HERE, 'out', f'prev_{ts}.jpg'), quality=88)
    elif mode == 'render':
        out = os.path.join(HERE, 'out'); os.makedirs(out, exist_ok=True)
        F = int(TOTAL * FPS); W_ = 2; step = (F + W_ - 1) // W_; ps = []
        for i in range(W_):
            a, b = i * step, min(F, (i + 1) * step)
            p = Process(target=encode_chunk, args=(frame, a, b, os.path.join(out, f'chunk_{i}.mp4'))); p.start(); ps.append(p)
        for p in ps: p.join()
        with open(os.path.join(out, 'list.txt'), 'w') as f:
            for i in range(W_): f.write(f"file 'chunk_{i}.mp4'\n")
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-i', os.path.join(out, 'list.txt'), '-c', 'copy',
                        os.path.join(out, 'video_4k.mp4')], check=True)
        print('RENDER_OK', F, 'frames')
