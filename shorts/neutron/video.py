"""LogicCoreLab short #5 - Neutron stars: a teaspoon weighs a billion tons. 4K vertical.
python3 video.py info | preview t1 t2 ... | render"""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from engine import *
HERE = os.path.dirname(os.path.abspath(__file__))

for name, code in [('spoon', '1f944'), ('boom', '1f4a5'), ('city', '1f3d9'), ('sun', '2600'), ('bulb', '1f4a1')]:
    load_icon(name, code)

EN = {1: "A single teaspoon of a neutron star would weigh about a billion tons.",
      2: "That's heavier than every human on Earth combined.",
      3: "Neutron stars are what's left when a giant star explodes.",
      4: "The core collapses so hard that more than the mass of our Sun gets squeezed into a ball only about twenty kilometers wide.",
      5: "That's about the size of a city.",
      6: "And some of them spin over seven hundred times every second.",
      7: "Space is stranger than fiction. Follow LogicCoreLab for more."}
TR = {1: "Bir nötron yıldızından tek bir çay kaşığı, yaklaşık 1 milyar ton gelir.",
      2: "Bu, Dünya'daki bütün insanların toplam ağırlığından fazla.",
      3: "Nötron yıldızları, dev bir yıldız patladığında geriye kalan çekirdektir.",
      4: "Çekirdek öyle sert çöker ki, Güneş'ten fazla kütle sadece 20 kilometre genişliğinde bir topa sıkışır.",
      5: "Bu, bir şehir büyüklüğünde.",
      6: "Ve bazıları saniyede 700'den fazla kez döner.",
      7: "Uzay, kurgudan daha tuhaf.|Daha fazlası için LogicCoreLab'i takip et!"}
SCN_S = [[1], [2], [3], [4, 5], [6], [7]]
T, D, ST, TOTAL, ev = make_timeline(EN, SCN_S, os.path.join(HERE, 'audio'))
ICE = (150, 215, 255); ORANGE = (251, 146, 60)
_r = random.Random(4)
STARS = [(_r.uniform(0, 1080), _r.uniform(200, 1350), _r.uniform(1.5, 4), _r.random() * 6.28) for _ in range(90)]
PART = [(_r.uniform(0, 6.283), _r.uniform(250, 700), _r.uniform(5, 12)) for _ in range(70)]

def starfield(d, t, a=1.0):
    for x, y, r, ph in STARS:
        al = a * (0.35 + 0.35 * math.sin(t * 2 + ph)); d.ellipse([P(x - r), P(y - r), P(x + r), P(y + r)], fill=(255, 255, 255, int(255 * al)))
def nstar(d, cx, cy, r, t, a=1.0, col=ICE):
    if r <= 0.5 or a <= 0: return
    pr = r * (1 + 0.05 * math.sin(t * 6))
    for k in range(10, 0, -1):
        rr = pr * (1 + k * 0.32); d.ellipse([P(cx - rr), P(cy - rr), P(cx + rr), P(cy + rr)], fill=col + (int(a * (6 + (10 - k) * 5)),))
    d.ellipse([P(cx - pr), P(cy - pr), P(cx + pr), P(cy + pr)], fill=(215, 240, 255, int(255 * a)))
    rr = pr * 0.55; d.ellipse([P(cx - rr), P(cy - rr), P(cx + rr), P(cy + rr)], fill=(255, 255, 255, int(255 * a)))

def s1(fr, d, t):
    starfield(d, t)
    title(d, ['NEUTRON', 'STAR'], t, colors=[WHITE, CYAN])
    nstar(d, 540, 610, 70 * back(prog(t, 0.2, 0.6)), t)
    sp = back(prog(t, ev(1, 'teaspoon') - 0.1, 0.45))
    icon(fr, 'spoon', 540, 900, 300 * sp)
    if sp > 0: nstar(d, 540, 900, 22 * sp, t * 1.5)
    c = eo(prog(t, ev(1, 'weigh'), ev(1, 'billion') + 0.4 - ev(1, 'weigh')))
    if c > 0:
        txt(d, f'{int(1e9 * c):,}', 540, 1120, 92, YEL, stroke=5, shadow=True)
        txt(d, 'TONS', 540, 1215, 56, WHITE, stroke=3)
def s2(fr, d, t):
    starfield(d, t, 0.6)
    title(d, ['HEAVIER THAN', 'ALL HUMANS'], t, t0=ST[1] + 0.05, colors=[WHITE, YEL])
    a = prog(t, ST[1] + 0.1, 0.35); A = int(255 * a)
    cx, cy, L = 540, 700, 285
    th = math.radians(9) * eio(prog(t, ev(2, 'heavier') - 0.1, 1.0))
    lx, ly = cx - L * math.cos(th), cy + L * math.sin(th); rx, ry = cx + L * math.cos(th), cy - L * math.sin(th)
    d.polygon([(P(cx), P(cy)), (P(cx - 70), P(1180)), (P(cx + 70), P(1180))], fill=(120, 130, 170, A))
    d.rounded_rectangle([P(cx - 170), P(1170), P(cx + 170), P(1200)], radius=P(12), fill=(150, 160, 200, A))
    d.line([(P(lx), P(ly)), (P(rx), P(ry))], fill=GOLD + (A,), width=P(16))
    d.ellipse([P(cx - 22), P(cy - 22), P(cx + 22), P(cy + 22)], fill=GOLD + (A,))
    for ex, ey in ((lx, ly), (rx, ry)):
        py = ey + 200
        d.line([(P(ex), P(ey)), (P(ex - 125), P(py))], fill=(220, 220, 235, A), width=P(4))
        d.line([(P(ex), P(ey)), (P(ex + 125), P(py))], fill=(220, 220, 235, A), width=P(4))
        d.chord([P(ex - 145), P(py - 50), P(ex + 145), P(py + 60)], 0, 180, fill=GOLD + (A,))
    icon(fr, 'spoon', lx, ly + 125, 190 * a); nstar(d, lx, ly + 125, 16 * a, t)
    k = 0
    for row in range(3):
        for col in range(5 - row):
            x = rx - 112 + col * 56 + row * 28; y = ry + 170 - row * 54
            person(d, x, y, 58 * back(prog(t, ST[1] + 0.3 + k * 0.03, 0.3)), PEOPLE[k % len(PEOPLE)]); k += 1
    txt(d, '1 TEASPOON', lx, ly + 300, 40, CYAN, a, stroke=3)
    txt(d, '8 BILLION', rx, ry + 290, 40, WHITE, a, stroke=3); txt(d, 'PEOPLE', rx, ry + 340, 40, WHITE, a, stroke=3)
def s3(fr, d, t):
    starfield(d, t, 0.7)
    title(d, ['A STAR', 'EXPLODES'], t, t0=ST[2] + 0.05, colors=[WHITE, ORANGE])
    te = ev(3, 'explodes') - 0.1; cx, cy = 540, 820
    if t < te + 0.15:
        g = back(prog(t, ST[2] + 0.1, 0.6)) * (1 - 0.15 * prog(t, te - 0.8, 0.8)); r = 250 * g
        for k in range(8, 0, -1):
            rr = r * (1 + k * 0.08); d.ellipse([P(cx - rr), P(cy - rr), P(cx + rr), P(cy + rr)], fill=(255, 90, 40, 18))
        d.ellipse([P(cx - r), P(cy - r), P(cx + r), P(cy + r)], fill=(230, 70, 40, 255))
        rr = r * 0.75; d.ellipse([P(cx - rr), P(cy - rr), P(cx + rr), P(cy + rr)], fill=(250, 130, 50, 255))
        rr = r * 0.45; d.ellipse([P(cx - rr), P(cy - rr), P(cx + rr), P(cy + rr)], fill=(255, 200, 90, 255))
        if t < te: txt(d, 'GIANT STAR', 540, 1150, 50 * back(prog(t, ST[2] + 0.4, 0.4)), ORANGE, stroke=3)
    if t >= te:
        a = t - te
        for ang, dist, sz in PART:
            p = eo(min(1, a / 1.4)); x = cx + math.cos(ang) * dist * p; y = cy + math.sin(ang) * dist * p
            al = max(0, 1 - a / 2.2); d.ellipse([P(x - sz), P(y - sz), P(x + sz), P(y + sz)], fill=(255, 170, 80, int(255 * al)))
        for k, c in enumerate([(255, 220, 150), (255, 120, 60)]):
            rr = 100 + 650 * eo(min(1, (a - k * 0.12) / 1.3)); al = max(0, 1 - a / 1.6)
            if a > k * 0.12: d.ellipse([P(cx - rr), P(cy - rr), P(cx + rr), P(cy + rr)], outline=c + (int(255 * al),), width=P(14))
        icon(fr, 'boom', cx, cy, 420 * back(min(1, a / 0.25)) * max(0, 1 - a / 0.9), alpha=max(0, 1 - a / 0.9))
        nstar(d, cx, cy, 45 * prog(t, te + 0.5, 0.6), t)
        pill(d, 'SUPERNOVA', 540, 1240, 52, ORANGE, DARK, back(prog(t, te + 0.15, 0.4)))
        if a < 0.25: d.rectangle([0, 0, W, H], fill=(255, 255, 255, int(170 * (1 - a / 0.25))))
def s4(fr, d, t):
    starfield(d, t, 0.6)
    title(d, ['CRUSHED', 'TO 20 KM'], t, t0=ST[3] + 0.05, colors=[WHITE, CYAN])
    cx, cy = 540, 820; tq = ev(4, 'squeezed') - 0.2
    q = eio(prog(t, tq, 1.2))
    sun_sz = 460 * back(prog(t, ST[3] + 0.1, 0.5)) * (1 - q) + 0
    if q < 1: icon(fr, 'sun', cx, cy, max(0, sun_sz * (1 - q) + 60 * q), alpha=1 - q * 0.9)
    pill(d, 'MORE THAN 1 SUN OF MASS', 540, 1190, 40, YEL, DARK, back(prog(t, ev(4, 'mass') - 0.2, 0.4)) * (1 - prog(t, T[5] - 0.2, 0.3)))
    city = prog(t, T[5], 0.6)
    rs = 34 + (215 - 34) * eio(city)
    if q > 0.6: nstar(d, cx, cy, rs * prog(t, tq + 0.8, 0.4), t, a=1 - 0.55 * city)
    if city > 0:
        icon(fr, 'city', cx, cy + 10, 330 * back(city), alpha=0.95)
        x = 0.0
        while x < 360:
            a0 = math.radians(x); a1 = math.radians(x + 7)
            d.line([(P(cx + 230 * math.cos(a0)), P(cy + 230 * math.sin(a0))), (P(cx + 230 * math.cos(a1)), P(cy + 230 * math.sin(a1)))], fill=CYAN + (int(255 * city),), width=P(6))
            x += 14
        pill(d, 'CITY-SIZED', 540, 1190, 52, CYAN, DARK, back(prog(t, T[5] + 0.3, 0.4)))
    k = prog(t, ev(4, 'twenty') - 0.2, 0.35) * (1 - prog(t, T[5] - 0.2, 0.3))
    if k > 0:
        A = int(255 * k); y = cy + 90
        d.line([(P(cx - 60), P(y)), (P(cx + 60), P(y))], fill=WHITE + (A,), width=P(5))
        for xx in (cx - 60, cx + 60): d.line([(P(xx), P(y - 16)), (P(xx), P(y + 16))], fill=WHITE + (A,), width=P(5))
        txt(d, '~20 km', cx, y + 60, 64, WHITE, k, stroke=4, shadow=True)
def s5(fr, d, t):
    starfield(d, t, 0.8)
    title(d, ['700+ SPINS', 'PER SECOND'], t, t0=ST[4] + 0.05, colors=[YEL, WHITE])
    cx, cy = 540, 800; lt = t - ST[4]
    ang = 2 * math.pi * (0.3 * lt + 0.9 * max(0, lt - 1) ** 2 / 2) if lt < 3 else 2 * math.pi * (0.3 * 3 + 0.9 * 2 + 2.7 * (lt - 3))
    a = prog(t, ST[4] + 0.1, 0.4)
    for off in (0, math.pi):
        th = ang + off; Lb = 640
        for sp, al in ((0.2, 50), (0.1, 90), (0.035, 170)):
            d.polygon([(P(cx), P(cy)), (P(cx + Lb * math.cos(th - sp)), P(cy + Lb * math.sin(th - sp) * 0.55)),
                       (P(cx + Lb * math.cos(th + sp)), P(cy + Lb * math.sin(th + sp) * 0.55))], fill=ICE + (int(al * a),))
    nstar(d, cx, cy, 70 * back(a), t)
    c = eo(prog(t, ev(6, 'seven') - 0.3, 1.0))
    if c > 0:
        txt(d, f'{round(700 * c)}+', 540, 1110, 140, YEL, stroke=6, shadow=True)
        txt(d, 'TIMES EVERY SECOND', 540, 1215, 44, WHITE, stroke=3)
def s6(fr, d, t): starfield(d, t, 0.5); outro(fr, d, t - ST[5], T[7] - ST[5], T[7] - ST[5] + D[7] * 0.5, tagline='SPACE > FICTION')

frame = make_frame([s1, s2, s3, s4, s5, s6], ST, fade_in={1, 2, 3, 4, 5}, subs=subs_from(EN, TR, T, D), no_wm={5})
if __name__ == '__main__':
    if sys.argv[1] == 'info': print(round(TOTAL, 2), [round(x, 2) for x in ST])
    else: cli(frame, TOTAL, HERE)
