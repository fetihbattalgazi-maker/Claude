"""LogicCoreLab short #6 (trending, Nov 2026) - Voyager 1 reaches one light-day... and goes quiet. 4K vertical.
python3 video.py info | preview t1 t2 ... | render"""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from engine import *
HERE = os.path.dirname(os.path.abspath(__file__))

for name, code in [('earth', '1f30d'), ('dish', '1f4e1'), ('warn', '26a0'), ('pc', '1f5a5'), ('bulb', '1f4a1')]:
    load_icon(name, code)

EN = {1: "Right now, a spacecraft launched in nineteen seventy-seven is so far away that its signal takes a full day to reach us.",
      2: "On November eighteenth, Voyager 1 crossed one light-day from Earth.",
      3: "That's about twenty-six billion kilometers.",
      4: "But days before the milestone, it stopped sending science data.",
      5: "Its signal is still there, so engineers think the problem is in its nearly fifty-year-old computer.",
      6: "Fixing it is slow. Every command takes over a day to arrive, and the answer takes another day to come back.",
      7: "It runs on a transmitter about as powerful as a fridge light bulb, and carries a golden record for anyone out there.",
      8: "Will humanity's farthest explorer talk to us again? Follow LogicCoreLab to find out."}
TR = {1: "Şu an, 1977'de fırlatılan bir uzay aracı o kadar uzakta ki sinyali bize tam bir günde ulaşıyor.",
      2: "18 Kasım'da Voyager 1, Dünya'dan bir ışık günü uzaklığı geçti.",
      3: "Bu, yaklaşık 26 milyar kilometre.",
      4: "Ama bu dönüm noktasından günler önce bilim verisi göndermeyi kesti.",
      5: "Sinyali hâlâ geliyor; mühendisler sorunun yaklaşık 50 yıllık bilgisayarında olduğunu düşünüyor.",
      6: "Tamiri çok yavaş: her komut bir günden uzun sürede ulaşıyor, cevabı da bir gün daha.",
      7: "Bir buzdolabı ampulü kadar güçlü bir vericiyle çalışıyor ve olası dinleyiciler için altın bir plak taşıyor.",
      8: "İnsanlığın en uzaktaki kâşifi bizimle yeniden konuşacak mı?|Öğrenmek için LogicCoreLab'i takip et!"}
SCN_S = [[1], [2, 3], [4, 5], [6], [7], [8]]
T, D, ST, TOTAL, ev = make_timeline(EN, SCN_S, os.path.join(HERE, 'audio'), end_pad=1.8)
SILVER = (225, 230, 240); ORANGE = (251, 146, 60)
_r = random.Random(77)
STARS = [(_r.uniform(0, 1080), _r.uniform(200, 1350), _r.uniform(1.5, 4), _r.random() * 6.28) for _ in range(110)]
BITS = [(_r.random(), _r.choice('01'), _r.uniform(-28, 28)) for _ in range(40)]

def starfield(d, t, a=1.0):
    for x, y, r, ph in STARS:
        al = a * (0.35 + 0.35 * math.sin(t * 2 + ph)); d.ellipse([P(x - r), P(y - r), P(x + r), P(y + r)], fill=(255, 255, 255, int(255 * al)))
def probe(d, cx, cy, s, a=1.0):
    if s <= 0.01 or a <= 0: return
    A = int(255 * a); G = (150, 155, 170, A)
    d.line([(P(cx - 20 * s), P(cy + 40 * s)), (P(cx - 360 * s), P(cy + 140 * s))], fill=G, width=max(1, P(4 * s)))
    d.line([(P(cx + 30 * s), P(cy + 60 * s)), (P(cx + 200 * s), P(cy + 190 * s))], fill=G, width=max(1, P(6 * s)))
    for k in range(3):
        x = cx + (150 + k * 22) * s; y = cy + (150 + k * 17) * s
        d.rounded_rectangle([P(x - 14 * s), P(y - 14 * s), P(x + 14 * s), P(y + 14 * s)], radius=P(5 * s), fill=(90, 95, 110, A))
    d.line([(P(cx), P(cy)), (P(cx + 120 * s), P(cy - 70 * s))], fill=G, width=max(1, P(5 * s)))
    d.rectangle([P(cx + 105 * s), P(cy - 95 * s), P(cx + 150 * s), P(cy - 60 * s)], fill=(120, 125, 140, A))
    hx = [(cx + 62 * s * math.cos(math.radians(60 * k)), cy + 55 * s + 62 * s * math.sin(math.radians(60 * k))) for k in range(6)]
    d.polygon([(P(x), P(y)) for x, y in hx], fill=GOLD + (A,))
    d.ellipse([P(cx - 150 * s), P(cy - 140 * s), P(cx + 150 * s), P(cy + 140 * s)], fill=SILVER + (A,), outline=(150, 155, 170, A), width=max(1, P(4 * s)))
    d.ellipse([P(cx - 100 * s), P(cy - 93 * s), P(cx + 100 * s), P(cy + 93 * s)], outline=(185, 190, 205, A), width=max(1, P(3 * s)))
    d.ellipse([P(cx - 18 * s), P(cy - 18 * s), P(cx + 18 * s), P(cy + 18 * s)], fill=(120, 125, 140, A))
def photons(d, x0, y0, x1, y1, t, color, a=1.0, n=7, speed=0.35, r=8):
    for k in range(n):
        p = (t * speed + k / n) % 1.0; x = x0 + (x1 - x0) * p; y = y0 + (y1 - y0) * p
        d.ellipse([P(x - r), P(y - r), P(x + r), P(y + r)], fill=color + (int(230 * a),))
def dashed(d, x0, y0, x1, y1, color, a=1.0, w=3, dash=18, gap=16):
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; s_ = 0
    while s_ < L:
        e = min(L, s_ + dash); d.line([(P(x0 + ux * s_), P(y0 + uy * s_)), (P(x0 + ux * e), P(y0 + uy * e))], fill=color + (int(255 * a),), width=P(w)); s_ += dash + gap

def s1(fr, d, t):
    starfield(d, t)
    title(d, ['1 LIGHT-DAY', 'AWAY'], t, colors=[YEL, WHITE])
    sp = back(prog(t, 0.2, 0.6))
    icon(fr, 'earth', 170, 1170, 120 * back(prog(t, 0.5, 0.5)))
    if sp > 0.5:
        dashed(d, 600, 780, 205, 1130, CYAN, 0.35)
        photons(d, 600, 780, 205, 1130, t, CYAN, 1.0, n=6, speed=0.3)
    probe(d, 640 + 8 * math.sin(t * 0.7), 740, 1.0 * sp)
    pill(d, 'LAUNCHED 1977', 760, 1065, 40, GOLD, DARK, back(prog(t, ev(1, 'nineteen'), 0.4)))
    pill(d, 'SIGNAL: 24 HOURS', 360, 960, 38, CYAN, DARK, back(prog(t, ev(1, 'full day') - 0.1, 0.4)))
def s2(fr, d, t):
    starfield(d, t, 0.7)
    title(d, ['VOYAGER 1'], t, t0=ST[1] + 0.05, colors=[WHITE])
    a = prog(t, ST[1] + 0.1, 0.4)
    icon(fr, 'earth', 130, 820, 130 * back(a)); probe(d, 930, 810, 0.38 * back(a))
    if a > 0:
        dashed(d, 205, 820, 860, 820, CYAN, 0.4 * a)
        photons(d, 860, 820, 205, 820, t, CYAN, a, n=4, speed=0.4)
    pill(d, 'NOV 18, 2026', 540, 600, 46, GOLD, DARK, back(prog(t, ev(2, 'november') - 0.1, 0.4)))
    pill(d, '1 LIGHT-DAY', 540, 720, 50, CYAN, DARK, back(prog(t, ev(2, 'light-day') - 0.1, 0.4)))
    c = eo(prog(t, T[3], D[3] * 0.85))
    if c > 0:
        txt(d, f'{int(26e9 * c):,} KM', 540, 1040, 74, YEL, stroke=5, shadow=True)
        txt(d, '≈ 16 BILLION MILES', 540, 1130, 40, GRAY, c, stroke=2)
def s3(fr, d, t):
    starfield(d, t, 0.6)
    title(d, ['SIGNAL', 'LOST?'], t, t0=ST[2] + 0.05, colors=[WHITE, RED])
    a = prog(t, ST[2] + 0.1, 0.4); x0, y0, x1, y1 = 760, 600, 210, 1120
    probe(d, 800, 560, 0.55 * back(a)); icon(fr, 'earth', 170, 1160, 120 * back(a))
    stop = T[4] + D[4] * 0.55; da = a * (1 - prog(t, stop, 0.5))
    if da > 0:
        L = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        for p0, ch, off in BITS:
            p = (p0 + t * 0.25) % 1.0; x = x0 + (x1 - x0) * p + nx * off; y = y0 + (y1 - y0) * p + ny * off
            txt(d, ch, x, y, 34, GREEN, da)
    pill(d, 'NO SCIENCE DATA', 540, 830, 46, RED, WHITE, back(prog(t, stop + 0.2, 0.4)))
    cs = prog(t, T[5], 0.5)
    if cs > 0:
        pts = []
        for j in range(121):
            p = j / 120; x = x0 + (x1 - x0) * p; y = y0 + (y1 - y0) * p
            w = math.sin(p * 40 - t * 8) * 10; pts.append((P(x + w * 0.69), P(y + w * 0.72)))
        d.line(pts, fill=CYAN + (int(220 * cs),), width=P(4))
        pill(d, 'CARRIER SIGNAL: OK', 640, 960, 38, GREEN, DARK, back(cs))
    sc = back(prog(t, ev(5, 'computer') - 0.2, 0.45))
    icon(fr, 'pc', 250, 600, 190 * sc); icon(fr, 'warn', 340, 520, 80 * sc * (0.9 + 0.1 * pulse(t, 2)))
    pill(d, '~50 YEARS OLD', 250, 725, 34, YEL, DARK, sc)
def packet(d, x, y, color, a=1.0):
    d.rounded_rectangle([P(x - 22), P(y - 16), P(x + 22), P(y + 16)], radius=P(5), fill=color + (int(255 * a),))
    d.line([(P(x - 22), P(y - 16)), (P(x), P(y + 2)), (P(x + 22), P(y - 16))], fill=DARK + (int(255 * a),), width=P(3))
def s4(fr, d, t):
    starfield(d, t, 0.6)
    title(d, ['FIXING IT', 'TAKES DAYS'], t, t0=ST[3] + 0.05, colors=[WHITE, YEL])
    a = prog(t, ST[3] + 0.1, 0.4)
    icon(fr, 'dish', 150, 820, 160 * back(a)); probe(d, 930, 810, 0.36 * back(a))
    tc = ev(6, 'command') - 0.2; ta = ev(6, 'answer') - 0.2
    c = prog(t, tc, 0.4)
    if c > 0:
        dashed(d, 240, 730, 860, 730, CYAN, 0.5 * c)
        packet(d, 240 + 620 * ((t - tc) * 0.35 % 1.0), 730, CYAN, c)
        pill(d, 'COMMAND: 1+ DAY', 550, 650, 38, CYAN, DARK, back(c))
    r = prog(t, ta, 0.4)
    if r > 0:
        dashed(d, 860, 910, 240, 910, YEL, 0.5 * r)
        packet(d, 860 - 620 * ((t - ta) * 0.35 % 1.0), 910, YEL, r)
        pill(d, 'REPLY: 1+ DAY', 550, 990, 38, YEL, DARK, back(r))
    h = eo(prog(t, ta + 0.6, 0.9))
    if h > 0: txt(d, f'{round(48 * h)}+ HOURS', 540, 1150, 96, WHITE, stroke=5, shadow=True)
def record(d, cx, cy, r, t, a=1.0):
    A = int(255 * a)
    d.ellipse([P(cx - r), P(cy - r), P(cx + r), P(cy + r)], fill=(212, 168, 60, A), outline=(255, 220, 120, A), width=P(5))
    for k in range(1, 9):
        rr = r * (0.35 + 0.08 * k); d.ellipse([P(cx - rr), P(cy - rr), P(cx + rr), P(cy + rr)], outline=(170, 128, 40, A), width=P(2))
    ang = t * 1.5
    d.line([(P(cx + r * 0.3 * math.cos(ang)), P(cy + r * 0.3 * math.sin(ang))), (P(cx + r * 0.95 * math.cos(ang)), P(cy + r * 0.95 * math.sin(ang)))], fill=(255, 240, 190, int(A * 0.8)), width=P(8))
    rr = r * 0.28; d.ellipse([P(cx - rr), P(cy - rr), P(cx + rr), P(cy + rr)], fill=(245, 215, 130, A))
    d.ellipse([P(cx - 8), P(cy - 8), P(cx + 8), P(cy + 8)], fill=DARK + (A,))
def s5(fr, d, t):
    starfield(d, t, 0.6)
    title(d, ['TINY POWER,', 'GOLDEN RECORD'], t, t0=ST[4] + 0.05, colors=[WHITE, GOLD])
    sb = back(prog(t, ev(7, 'transmitter') - 0.1, 0.45)); sr = back(prog(t, ev(7, 'golden') - 0.2, 0.5))
    icon(fr, 'bulb', 280, 760, 230 * sb)
    pill(d, '~22 WATTS', 280, 960, 44, YEL, DARK, sb)
    if sr > 0: record(d, 770, 760, 175 * sr, t)
    pill(d, 'GOLDEN RECORD', 770, 1000, 40, GOLD, DARK, sr)
    pill(d, 'SOUNDS & IMAGES OF EARTH', 540, 1150, 36, CYAN, DARK, back(prog(t, ev(7, 'anyone') - 0.2, 0.4)))
def s6(fr, d, t):
    starfield(d, t)
    lt = t - ST[5]
    probe(d, 540 + 10 * math.sin(t), 720 - lt * 6, 0.85 * back(prog(t, ST[5] + 0.05, 0.5)) * (1 - 0.02 * lt))
    s = back(prog(t, T[8] + 0.1, 0.45)); txt(d, 'WILL IT CALL HOME?', 540, 1030, 70 * s, WHITE, stroke=5, shadow=True)
    tb = T[8] + D[8] * 0.6
    s = back(prog(t, tb, 0.45)); txt(d, 'LogicCoreLab', 540, 1140, 104 * s, CYAN, stroke=5, shadow=True)
    s = back(prog(t, tb + 0.3, 0.45)) * (1 + 0.04 * math.sin(t * 6)); pill(d, 'FOLLOW FOR UPDATES', 540, 1270, 46, YEL, DARK, s)

frame = make_frame([s1, s2, s3, s4, s5, s6], ST, fade_in={1, 2, 3, 4, 5}, subs=subs_from(EN, TR, T, D), no_wm={5})
if __name__ == '__main__':
    if sys.argv[1] == 'info': print(round(TOTAL, 2), [round(x, 2) for x in ST])
    else: cli(frame, TOTAL, HERE)
