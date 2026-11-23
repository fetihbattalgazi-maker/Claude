"""LogicCoreLab short #8 - Why do you get sleepy? Brainstem neurons that build sleep pressure (Nature, 2026). 4K vertical.
python3 video.py info | preview t1 t2 ... | render"""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from engine import *
HERE = os.path.dirname(os.path.abspath(__file__))

for name, code in [('sleepy', '1f634'), ('mouse', '1f42d'), ('brain', '1f9e0'), ('moon', '1f319'), ('yawn', '1f971'), ('zzz', '1f4a4'), ('warn', '26a0')]:
    load_icon(name, code)

EN = {1: "Why do you get sleepy? Scientists just found brain cells that build up the urge to sleep.",
      2: "A team at the University of Basel studied mice.",
      3: "Deep in the brainstem, two groups of neurons get more active the longer the mice stay awake.",
      4: "Like a battery charging, they build up sleep pressure.",
      5: "When researchers switched these cells on, the mice slept longer and deeper.",
      6: "When they shut them down, their sleep dropped by almost seventy percent.",
      7: "But some of those mice didn't survive. Skipping sleep has a price.",
      8: "So next time you yawn at midnight, thank your brainstem. Follow LogicCoreLab for more."}
TR = {1: "Neden uykun gelir? Bilim insanları uyku isteğini biriktiren beyin hücrelerini buldu.",
      2: "Basel Üniversitesi'nden bir ekip fareleri inceledi.",
      3: "Beyin sapının derinlerinde iki grup nöron, fareler uyanık kaldıkça daha aktif hale geliyor.",
      4: "Şarj olan bir pil gibi, uyku basıncı biriktiriyorlar.",
      5: "Araştırmacılar bu hücreleri açtığında fareler daha uzun ve derin uyudu.",
      6: "Kapattıklarında ise uyku neredeyse yüzde 70 azaldı.",
      7: "Ama bu farelerin bazıları hayatta kalamadı. Uykusuzluğun bir bedeli var.",
      8: "Gece yarısı esnediğinde beyin sapına teşekkür et.|Daha fazlası için LogicCoreLab'i takip et!"}
SCN_S = [[1], [2, 3], [4], [5, 6], [7], [8]]
T, D, ST, TOTAL, ev = make_timeline(EN, SCN_S, os.path.join(HERE, 'audio'))
PURPLE = (167, 139, 250)
_r = random.Random(12)
STARS = [(_r.uniform(0, 1080), _r.uniform(200, 1350), _r.uniform(1.5, 3.5), _r.random() * 6.28) for _ in range(70)]
NEU = [(_r.gauss(0, 26), _r.gauss(0, 18), _r.random() * 6.28, k % 2) for k in range(36)]

def night(d, t, a=0.8):
    for x, y, r, ph in STARS:
        al = a * (0.3 + 0.3 * math.sin(t * 1.5 + ph)); d.ellipse([P(x - r), P(y - r), P(x + r), P(y + r)], fill=(255, 255, 255, int(255 * al)))
def zzz(fr, t, x0, y0, a=1.0):
    for k in range(3):
        p = (t * 0.35 + k / 3) % 1.0
        icon(fr, 'zzz', x0 + 60 * p + 15 * math.sin(t * 2 + k), y0 - 260 * p, (70 + 60 * p) * a, alpha=a * (1 - p) ** 0.7)
def s1(fr, d, t):
    night(d, t)
    title(d, ['WHY DO YOU', 'GET SLEEPY?'], t, colors=[WHITE, PURPLE])
    s = back(prog(t, 0.2, 0.6))
    icon(fr, 'sleepy', 540, 830 + 10 * math.sin(t * 1.3), 400 * s)
    if s > 0.5: zzz(fr, t, 740, 660)
    pill(d, 'NEW DISCOVERY', 540, 1180, 50, YEL, DARK, back(prog(t, ev(1, 'found') - 0.2, 0.4)))
def s2(fr, d, t):
    night(d, t, 0.5)
    title(d, ['INSIDE THE', 'BRAINSTEM'], t, t0=ST[1] + 0.05, colors=[WHITE, CYAN])
    sm = back(prog(t, T[2] - 0.1, 0.45))
    if t < T[3] + 0.3:
        a = 1 - prog(t, T[3] - 0.1, 0.4)
        icon(fr, 'mouse', 290, 720, 260 * sm, alpha=a)
        pill(d, 'UNIVERSITY OF BASEL', 700, 670, 38, CYAN, DARK, back(prog(t, ev(2, 'basel') - 0.2, 0.4)), a)
        pill(d, 'NATURE · 2026', 700, 770, 38, WHITE, DARK, back(prog(t, ev(2, 'basel'), 0.4)), a)
    b = prog(t, T[3] - 0.1, 0.5)
    if b > 0:
        icon(fr, 'brain', 540, 780, 380 * back(b))
        A = int(255 * b); cx, cy = 585, 1030
        d.rounded_rectangle([P(cx - 30), P(915), P(cx + 30), P(1110)], radius=P(24), fill=(244, 160, 180, A))
        act = prog(t, ev(3, 'active') - 0.6, 1.8)
        for dx, dy, ph, grp in NEU:
            col = CYAN if grp == 0 else PURPLE; al = b * (0.3 + 0.7 * act) * (0.6 + 0.4 * math.sin(t * 7 + ph)); r = 8 + 7 * act
            x = cx + dx * 1.1 + (-30 if grp == 0 else 30); y = cy + dy * 1.2 + 20
            d.ellipse([P(x - r * 2.2), P(y - r * 2.2), P(x + r * 2.2), P(y + r * 2.2)], fill=col + (int(60 * al),))
            d.ellipse([P(x - r), P(y - r), P(x + r), P(y + r)], fill=col + (int(255 * al),))
        pill(d, '2 NEURON GROUPS', 280, 1120, 36, PURPLE, DARK, back(prog(t, ev(3, 'two groups') - 0.2, 0.4)))
        h = eo(prog(t, ev(3, 'longer') - 0.3, 1.4))
        if h > 0: txt(d, f'AWAKE: {round(16 * h)} H', 540, 1215, 60, YEL, stroke=4, shadow=True)
def s3(fr, d, t):
    night(d, t, 0.5)
    title(d, ['LIKE A', 'BATTERY'], t, t0=ST[2] + 0.05, colors=[WHITE, YEL])
    a = prog(t, ST[2] + 0.1, 0.35); A = int(255 * a)
    x0, x1, y0, y1 = 250, 790, 640, 960
    d.rounded_rectangle([P(x0), P(y0), P(x1), P(y1)], radius=P(36), outline=WHITE + (A,), width=P(10))
    d.rounded_rectangle([P(x1 + 8), P(y0 + 100), P(x1 + 50), P(y1 - 100)], radius=P(10), fill=WHITE + (A,))
    lv = eio(prog(t, T[4] - 0.1, D[4] + 0.3))
    if lv > 0.02:
        col = (int(74 + (239 - 74) * lv), int(222 - (222 - 68) * lv), int(128 - (128 - 68) * lv))
        d.rounded_rectangle([P(x0 + 22), P(y0 + 22), P(x0 + 22 + (x1 - x0 - 44) * lv), P(y1 - 22)], radius=P(22), fill=col + (A,))
        txt(d, f'{round(100 * lv)}%', (x0 + x1) / 2, (y0 + y1) / 2, 110, WHITE, a, stroke=6, shadow=True)
    pill(d, 'SLEEP PRESSURE', 540, 1060, 50, PURPLE, WHITE, back(prog(t, ev(4, 'pressure') - 0.2, 0.4)))
    icon(fr, 'moon', 540, 1200, 120 * back(prog(t, ev(4, 'pressure'), 0.4)))
def toggle(d, cx, cy, on, a=1.0):
    A = int(255 * a); col = GREEN if on else RED
    d.rounded_rectangle([P(cx - 70), P(cy - 38), P(cx + 70), P(cy + 38)], radius=P(38), fill=col + (A,))
    kx = cx + (32 if on else -32); d.ellipse([P(kx - 30), P(cy - 30), P(kx + 30), P(cy + 30)], fill=WHITE + (A,))
    txt(d, 'ON' if on else 'OFF', cx, cy + 70, 34, col, a, stroke=2)
def s4(fr, d, t):
    night(d, t, 0.4)
    title(d, ['SWITCH ON,', 'SWITCH OFF'], t, t0=ST[3] + 0.05, colors=[GREEN, RED])
    bx0, bx1, hb = 300, 960, 84
    a1 = prog(t, T[5] - 0.1, 0.4)
    if a1 > 0:
        toggle(d, 160, 660, True, a1); y = 620
        d.rounded_rectangle([P(bx0), P(y), P(bx1), P(y + hb)], radius=P(hb / 2), fill=(255, 255, 255, int(28 * a1)))
        w = (bx1 - bx0) * (0.45 + 0.55 * eo(prog(t, ev(5, 'longer') - 0.3, 1.0)))
        d.rounded_rectangle([P(bx0), P(y), P(bx0 + w), P(y + hb)], radius=P(hb / 2), fill=GREEN + (int(255 * a1),))
        txt(d, 'SLEEP', bx0 + 30, y + hb / 2, 38, DARK, a1, anchor='lm')
        pill(d, 'LONGER & DEEPER', 630, 770, 38, GREEN, DARK, back(prog(t, ev(5, 'deeper') - 0.2, 0.4)))
        if w > 700: zzz(fr, t, 900, 600, a1)
    a2 = prog(t, T[6] - 0.1, 0.4)
    if a2 > 0:
        toggle(d, 160, 960, False, a2); y = 920
        d.rounded_rectangle([P(bx0), P(y), P(bx1), P(y + hb)], radius=P(hb / 2), fill=(255, 255, 255, int(28 * a2)))
        w = (bx1 - bx0) * (1 - 0.7 * eio(prog(t, ev(6, 'dropped') - 0.2, 1.0)))
        d.rounded_rectangle([P(bx0), P(y), P(bx0 + w), P(y + hb)], radius=P(hb / 2), fill=RED + (int(255 * a2),))
        txt(d, 'SLEEP', bx0 + 30, y + hb / 2, 38, WHITE, a2, anchor='lm')
        s = back(prog(t, ev(6, 'seventy') - 0.2, 0.4)); txt(d, '-70%', 760, 1110, 130 * s, RED, stroke=6, shadow=True)
def s5(fr, d, t):
    night(d, t, 0.3)
    title(d, ['SLEEP IS NOT', 'OPTIONAL'], t, t0=ST[4] + 0.05, colors=[WHITE, RED])
    icon(fr, 'warn', 540, 760, 300 * back(prog(t, ST[4] + 0.15, 0.5)) * (0.95 + 0.05 * pulse(t, 2)))
    pill(d, "SOME MICE DIDN'T SURVIVE", 540, 1030, 44, RED, WHITE, back(prog(t, ev(7, 'survive') - 0.3, 0.4)))
    pill(d, 'SKIPPING SLEEP HAS A PRICE', 540, 1140, 42, YEL, DARK, back(prog(t, ev(7, 'price') - 0.3, 0.4)))
def s6(fr, d, t):
    night(d, t)
    icon(fr, 'yawn', 540, 700, 330 * back(prog(t, ST[5] + 0.05, 0.5)))
    s = back(prog(t, ev(8, 'thank') - 0.1, 0.45)); txt(d, 'THANK YOUR BRAINSTEM', 540, 1010, 66 * s, WHITE, stroke=5, shadow=True)
    tb = ev(8, 'follow') - 0.1
    s = back(prog(t, tb, 0.45)); txt(d, 'LogicCoreLab', 540, 1125, 104 * s, CYAN, stroke=5, shadow=True)
    s = back(prog(t, tb + 0.3, 0.45)) * (1 + 0.04 * math.sin(t * 6)); pill(d, 'FOLLOW FOR MORE', 540, 1262, 46, YEL, DARK, s)

frame = make_frame([s1, s2, s3, s4, s5, s6], ST, fade_in={1, 2, 3, 4, 5}, subs=subs_from(EN, TR, T, D), no_wm={5})
if __name__ == '__main__':
    if sys.argv[1] == 'info': print(round(TOTAL, 2), [round(x, 2) for x in ST])
    else: cli(frame, TOTAL, HERE)
