"""LogicCoreLab short #4 - The octopus: three hearts and blue blood. 4K vertical.
python3 video.py info | preview t1 t2 ... | render"""
import math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from engine import *
HERE = os.path.dirname(os.path.abspath(__file__))

for name, code in [('octo', '1f419'), ('heart', '1fac0'), ('blood', '1fa78'), ('drop', '1f4a7'), ('brain', '1f9e0'),
                   ('tongue', '1f445'), ('zap', '26a1'), ('bulb', '1f4a1')]:
    load_icon(name, code)

EN = {1: "An octopus has three hearts, and its blood is blue.",
      2: "Two hearts pump blood through the gills.",
      3: "The third pumps it to the rest of the body.",
      4: "But when the octopus swims, that third heart stops beating.",
      5: "That's one reason octopuses prefer crawling.",
      6: "Their blood is blue because it uses copper, not iron, to carry oxygen.",
      7: "And about two-thirds of their neurons are in their arms.",
      8: "Each arm can taste and react on its own.",
      9: "Nature is stranger than fiction. Follow LogicCoreLab for more."}
TR = {1: "Ahtapotun üç kalbi var ve kanı mavi.",
      2: "İki kalp, kanı solungaçlara pompalar.",
      3: "Üçüncüsü ise vücudun geri kalanına.",
      4: "Ama ahtapot yüzerken o üçüncü kalp durur.",
      5: "Ahtapotların sürünmeyi tercih etmesinin bir nedeni bu.",
      6: "Kanı mavidir, çünkü oksijeni taşımak için demir değil bakır kullanır.",
      7: "Ve nöronlarının yaklaşık üçte ikisi kollarındadır.",
      8: "Her kol kendi başına tadabilir ve tepki verebilir.",
      9: "Doğa, kurgudan daha tuhaf.|Daha fazlası için LogicCoreLab'i takip et!"}
SCN_S = [[1], [2, 3], [4, 5], [6], [7, 8], [9]]
T, D, ST, TOTAL, ev = make_timeline(EN, SCN_S, os.path.join(HERE, 'audio'))
BLUE = (59, 130, 246); COPPER = (217, 119, 6); IRON = (220, 38, 38)

def bob(t, f=0.5, a=12): return a * math.sin(2 * math.pi * f * t)
def beat(t, f=1.2): x = (t * f) % 1.0; return 1 + 0.12 * math.exp(-x * 9)

def s1(fr, d, t):
    title(d, ['THE', 'OCTOPUS'], t, colors=[WHITE, CYAN])
    icon(fr, 'octo', 540, 830 + bob(t), 430 * back(prog(t, 0.25, 0.6)))
    pill(d, '3 HEARTS', 330, 1235, 50, ROSE, WHITE, back(prog(t, ev(1, 'three'), 0.4)))
    pill(d, 'BLUE BLOOD', 750, 1235, 50, BLUE, WHITE, back(prog(t, ev(1, 'blue'), 0.4)))
def flow(d, x0, y0, x1, y1, t, color, a=1.0, n=6, speed=0.8):
    for k in range(n):
        p = (t * speed + k / n) % 1.0; x = x0 + (x1 - x0) * p; y = y0 + (y1 - y0) * p
        d.ellipse([P(x - 11), P(y - 11), P(x + 11), P(y + 11)], fill=color + (int(230 * a),))
def s2(fr, d, t):
    title(d, ['3 HEARTS'], t, t0=ST[1] + 0.05, colors=[ROSE])
    icon(fr, 'octo', 540, 560 + bob(t), 230 * back(prog(t, ST[1] + 0.1, 0.5)))
    g = prog(t, T[2], 0.45); b = prog(t, T[3], 0.45)
    for x in (210, 420):
        icon(fr, 'heart', x, 880, 180 * back(g) * beat(t))
    if g > 0:
        d.rounded_rectangle([P(150), P(1060), P(480), P(1140)], radius=P(40), fill=BLUE + (int(255 * g),))
        txt(d, 'GILLS', 315, 1100, 46, WHITE, g)
        for x in (210, 420): flow(d, x, 970, 315, 1060, t, CYAN, g, n=4)
    icon(fr, 'heart', 800, 880, 210 * back(b) * beat(t))
    if b > 0:
        d.rounded_rectangle([P(640), P(1060), P(960), P(1140)], radius=P(40), fill=ROSE + (int(255 * b),))
        txt(d, 'BODY', 800, 1100, 46, WHITE, b)
        flow(d, 800, 985, 800, 1060, t, (255, 150, 170), b, n=3)
    txt(d, '#3', 800, 750, 56 * back(b), YEL, stroke=4)
def ecg(d, x0, x1, y, t, stop_t, A=255):
    tt = t - 0.0; pts = []; n = 160
    for j in range(n + 1):
        x = x0 + (x1 - x0) * j / n; ph = (x / 260 - tt * 1.2) % 1.0
        amp = 1.0 - prog(t - (x1 - x) / 900, stop_t, 0.6)
        v = 0
        if 0.40 < ph < 0.44: v = -90 * (ph - 0.40) / 0.04
        elif 0.44 <= ph < 0.50: v = -90 + 170 * (ph - 0.44) / 0.06
        elif 0.50 <= ph < 0.54: v = 80 - 80 * (ph - 0.50) / 0.04
        pts.append((P(x), P(y + v * amp)))
    d.line(pts, fill=RED + (A,), width=P(7), joint='curve')
def s3(fr, d, t):
    title(d, ['SWIM =', 'HEART STOPS'], t, t0=ST[2] + 0.05, colors=[WHITE, RED])
    a = prog(t, ST[2] + 0.1, 0.3)
    st = ev(4, 'stops')
    if a > 0:
        d.rounded_rectangle([P(110), P(500), P(970), P(760)], radius=P(30), fill=(0, 0, 0, int(110 * a)), outline=RED + (int(180 * a),), width=P(4))
        ecg(d, 130, 950, 640, t, st, int(255 * a))
        icon(fr, 'heart', 180, 545, 80 * a * (beat(t) if t < st else 1), alpha=1.0 if t < st else 0.45)
        txt(d, 'HEART #3', 250, 545, 34, WHITE, a, anchor='lm')
    pill(d, 'STOPPED', 820, 545, 34, RED, WHITE, back(prog(t, st + 0.3, 0.35)))
    cr = prog(t, T[5] - 0.1, 0.4)
    if t < T[5]:
        x = 140 + 800 * ((t - ST[2]) / (T[5] - ST[2])); icon(fr, 'octo', x, 980 + 30 * math.sin(t * 5), 230 * a, alpha=1 - cr)
    if cr > 0:
        d.rectangle([P(60), P(1120), P(1020), P(1170)], fill=(120, 90, 60, int(255 * cr)))
        x = 200 + 120 * (t - T[5]); icon(fr, 'octo', x, 1010 + 6 * math.sin(t * 9), 220 * cr)
        pill(d, 'PREFERS CRAWLING', 620, 860, 42, CYAN, DARK, back(prog(t, T[5] + 0.3, 0.4)))
def tile(d, cx, cy, sym, num, name, color, s):
    if s <= 0.01: return
    w, h = 250 * s, 290 * s
    d.rounded_rectangle([P(cx - w / 2), P(cy - h / 2), P(cx + w / 2), P(cy + h / 2)], radius=P(26 * s), fill=color + (255,), outline=WHITE + (255,), width=P(5))
    txt(d, str(num), cx - w / 2 + 28 * s, cy - h / 2 + 34 * s, 36 * s, WHITE, anchor='lm')
    txt(d, sym, cx, cy - 5 * s, 130 * s, WHITE, stroke=3)
    txt(d, name, cx, cy + h / 2 - 38 * s, 34 * s, WHITE)
def s4(fr, d, t):
    title(d, ['WHY BLUE?'], t, t0=ST[3] + 0.05, colors=[CYAN])
    sc = back(prog(t, ev(6, 'copper') - 0.1, 0.45)); si = back(prog(t, ev(6, 'iron') - 0.1, 0.45))
    big = back(prog(t, ST[3] + 0.15, 0.5)) * (1 - eio(prog(t, ev(6, 'copper') - 0.4, 0.35)))
    icon(fr, 'drop', 540, 800, 300 * big * (0.95 + 0.05 * pulse(t, 1.5)))
    tile(d, 310, 760, 'Fe', 26, 'IRON', IRON, si)
    tile(d, 770, 760, 'Cu', 29, 'COPPER', COPPER, sc)
    icon(fr, 'blood', 310, 1010, 120 * si); icon(fr, 'drop', 770, 1010, 120 * sc)
    txt(d, 'HUMANS: RED', 310, 1110, 40 * si, (252, 165, 165), stroke=3)
    txt(d, 'OCTOPUS: BLUE', 770, 1110, 40 * sc, (147, 197, 253), stroke=3)
    if si > 0.5:
        a = prog(t, ev(6, 'iron') + 0.3, 0.3)
        d.line([(P(200), P(640)), (P(420), P(880))], fill=(0, 0, 0, int(160 * a)), width=P(12))
    pill(d, 'CARRIES OXYGEN', 770, 1240, 44, CYAN, DARK, back(prog(t, ev(6, 'oxygen') - 0.1, 0.4)))
_rng = random.Random(8)
NEU = [(_rng.uniform(330, 750), _rng.uniform(880, 1010), _rng.random() * 6.28) for _ in range(70)]
def s5(fr, d, t):
    title(d, ['A BRAIN IN', 'EVERY ARM'], t, t0=ST[4] + 0.05, colors=[WHITE, YEL])
    icon(fr, 'octo', 540, 820 + bob(t, 0.4, 8), 420 * back(prog(t, ST[4] + 0.1, 0.5)))
    n = prog(t, T[7] + 0.2, 0.8)
    if n > 0:
        for x, y, ph in NEU:
            a = n * (0.5 + 0.5 * math.sin(t * 6 + ph)); r = 9
            d.ellipse([P(x - r), P(y - r), P(x + r), P(y + r)], fill=YEL + (int(255 * a),))
        icon(fr, 'brain', 900, 600, 120 * back(n)); txt(d, '1/3', 900, 700, 50 * back(n), WHITE, stroke=3)
        txt(d, '2/3 IN THE ARMS', 540, 1110, 64 * back(prog(t, ev(7, 'arms') - 0.1, 0.4)), YEL, stroke=5, shadow=True)
    icon(fr, 'tongue', 220, 1010, 120 * back(prog(t, ev(8, 'taste'), 0.4)))
    icon(fr, 'zap', 860, 1010, 120 * back(prog(t, ev(8, 'react'), 0.4)))
    pill(d, 'TASTE + REACT', 540, 1240, 46, CYAN, DARK, back(prog(t, ev(8, 'own') - 0.2, 0.4)))
def s6(fr, d, t): outro(fr, d, t - ST[5], T[9] - ST[5], T[9] - ST[5] + D[9] * 0.5, tagline='NATURE > FICTION')

frame = make_frame([s1, s2, s3, s4, s5, s6], ST, fade_in={1, 2, 3, 4, 5}, subs=subs_from(EN, TR, T, D), no_wm={5})
if __name__ == '__main__':
    if sys.argv[1] == 'info': print(round(TOTAL, 2), [round(x, 2) for x in ST])
    else: cli(frame, TOTAL, HERE)
