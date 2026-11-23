"""LogicCoreLab short #3 - A day on Venus is longer than its year. 4K vertical.
python3 video.py preview t1 t2 ... | render"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from engine import *
HERE = os.path.dirname(os.path.abspath(__file__))

for name, code in [('sun', '2600'), ('earth', '1f30d'), ('therm', '1f321'), ('fire', '1f525'), ('fog', '1f32b'), ('wave', '1f30a'), ('bulb', '1f4a1')]:
    load_icon(name, code)

EN = {1: "On Venus, one spin takes longer than one trip around the Sun.",
      2: "Venus needs two hundred forty-three Earth days to rotate once.",
      3: "But it orbits the Sun in just two hundred twenty-five.",
      4: "So its day is longer than its year.",
      5: "And it spins backwards.",
      6: "On Venus, the Sun rises in the west and sets in the east.",
      7: "It's also the hottest planet, around four hundred sixty-five degrees Celsius.",
      8: "Hotter than Mercury, even though Mercury is closer to the Sun.",
      9: "The reason? A thick carbon dioxide atmosphere that traps the heat.",
      10: "Standing there would feel like being nine hundred meters under the ocean.",
      11: "Space is stranger than fiction. Follow LogicCoreLab for more."}
TR = {1: "Venüs'te kendi etrafında bir tur, Güneş etrafında bir turdan daha uzun sürer.",
      2: "Venüs kendi etrafında bir kez dönmek için 243 Dünya günü harcar.",
      3: "Ama Güneş'in etrafını sadece 225 günde dolaşır.",
      4: "Yani bir günü, bir yılından uzundur!",
      5: "Üstelik ters yönde döner.",
      6: "Venüs'te Güneş batıdan doğar, doğudan batar.",
      7: "Aynı zamanda en sıcak gezegendir: yaklaşık 465 °C.",
      8: "Güneş'e daha yakın olan Merkür'den bile sıcak.",
      9: "Sebebi mi? Isıyı hapseden kalın bir karbondioksit atmosferi.",
      10: "Orada durmak, okyanusun 900 metre altında olmak gibi hissettirir.",
      11: "Uzay, kurgudan daha tuhaf.|Daha fazlası için LogicCoreLab'i takip et!"}
SCN_S = [[1], [2, 3, 4], [5, 6], [7], [8], [9], [10], [11]]
T, D, ST, TOTAL, ev = make_timeline(EN, SCN_S, os.path.join(HERE, 'audio'), gaps={4: 0.45})

VEN = (226, 160, 80); VB = [(245, 205, 130), (196, 118, 58), (242, 192, 112), (186, 106, 52), (236, 184, 104)]
MER = (150, 150, 162); MB = [(175, 175, 185), (120, 120, 132), (165, 165, 175)]
ORANGE = (251, 146, 60)
def venus(fr, cx, cy, r, t, spin=-0.6, alpha=1.0, glow=0.8): planet(fr, cx, cy, r, VEN, VB, rot=t * spin, alpha=alpha, glow=(255, 190, 110), glow_a=glow)

def s1(fr, d, t):
    title(d, ['A DAY ON', 'VENUS'], t, colors=[WHITE, YEL])
    venus(fr, 540, 850, 250 * back(prog(t, 0.25, 0.6)), t)
    pill(d, '1 DAY  >  1 YEAR ?', 540, 1240, 52, YEL, DARK, back(prog(t, ev(1, 'longer'), 0.4)))
def hbar(d, y, label, val, vmax, color, t0, dur, t, glow=0.0):
    txt(d, label, 130, y, 50, color, anchor='lm', stroke=3, shadow=True)
    x0, x1 = 130, 950; yb = y + 50; hb = 96
    if glow > 0:
        for k in range(4, 0, -1):
            e = k * 7; d.rounded_rectangle([P(x0 - e), P(yb - e), P(x1 + e), P(yb + hb + e)], radius=P(hb / 2 + e), outline=color + (int(glow * (60 - k * 12)),), width=P(6))
    d.rounded_rectangle([P(x0), P(yb), P(x1), P(yb + hb)], radius=P(hb / 2), fill=(255, 255, 255, 28))
    p = eo(prog(t, t0, dur)); fw = (x1 - x0) * val / vmax * p
    if fw > hb: d.rounded_rectangle([P(x0), P(yb), P(x0 + fw), P(yb + hb)], radius=P(hb / 2), fill=color + (255,))
    if fw > 260: txt(d, f'{round(val * p)} DAYS', x0 + fw - 30, yb + hb / 2, 46, DARK, anchor='rm')
def s2(fr, d, t):
    title(d, ['DAY vs YEAR'], t, t0=ST[1] + 0.05, colors=[WHITE])
    venus(fr, 540, 520, 105 * back(prog(t, ST[1] + 0.1, 0.5)), t, glow=0.5)
    hbar(d, 720, '1 SPIN = 1 DAY', 243, 255, YEL, T[2] + 0.2, D[2] * 0.85, t, glow=prog(t, T[4], 0.3) * pulse(t))
    hbar(d, 970, '1 ORBIT = 1 YEAR', 225, 255, CYAN, T[3] + 0.2, D[3] * 0.85, t)
    pill(d, 'DAY  >  YEAR!', 540, 1250, 60, YEL, DARK, back(prog(t, T[4] + 0.1, 0.45)))
def arc_arrow(d, cx, cy, r, a0, a1, color, prog_, width=10):
    """Arc from angle a0 to a1 (degrees, screen coords), arrowhead at the end."""
    if prog_ <= 0.02: return
    a1p = a0 + (a1 - a0) * prog_; n = 40
    pts = [(cx + r * math.cos(math.radians(a0 + (a1p - a0) * j / n)), cy + r * math.sin(math.radians(a0 + (a1p - a0) * j / n))) for j in range(n + 1)]
    d.line([(P(x), P(y)) for x, y in pts], fill=color + (255,), width=P(width), joint='curve')
    (xa, ya), (xb, yb) = pts[-2], pts[-1]; ang = math.atan2(yb - ya, xb - xa); sz = 32
    d.polygon([(P(xb + math.cos(ang) * 12), P(yb + math.sin(ang) * 12)), (P(xb - sz * math.cos(ang - 0.55)), P(yb - sz * math.sin(ang - 0.55))),
               (P(xb - sz * math.cos(ang + 0.55)), P(yb - sz * math.sin(ang + 0.55)))], fill=color + (255,))
def s3(fr, d, t):
    title(d, ['IT SPINS', 'BACKWARDS'], t, t0=ST[2] + 0.05, colors=[WHITE, YEL])
    se = back(prog(t, ST[2] + 0.15, 0.5)); sv = back(prog(t, ST[2] + 0.3, 0.5))
    icon(fr, 'earth', 290, 640, 230 * se)
    venus(fr, 790, 640, 115 * sv, t, spin=1.2, glow=0.5)
    pa = eio(prog(t, T[5], 0.7))
    arc_arrow(d, 290, 640, 150, 200, 340, CYAN, pa)
    arc_arrow(d, 790, 640, 150, 340, 200, YEL, pa)
    txt(d, 'EARTH', 290, 830, 44 * se, CYAN, stroke=3); txt(d, 'VENUS', 790, 830, 44 * sv, YEL, stroke=3)
    h = prog(t, T[6] - 0.2, 0.4)
    if h > 0:
        A = int(255 * h); gy0 = 1190
        sp = eo(prog(t, ev(6, 'rises') - 0.2, 1.2))
        sx, sy = 250, 1230 - 190 * sp
        icon(fr, 'sun', sx, sy, 150 * h)
        d.rectangle([P(60), P(gy0), P(1020), P(1300)], fill=(120, 60, 30, A))
        d.line([(P(60), P(gy0)), (P(1020), P(gy0))], fill=ORANGE + (A,), width=P(6))
        txt(d, 'W', 250, 1250, 56, WHITE, h, stroke=3); txt(d, 'E', 830, 1250, 56, WHITE, h, stroke=3)
        pill(d, 'SUN RISES IN THE WEST', 540, 940, 40, YEL, DARK, back(prog(t, ev(6, 'west') - 0.1, 0.4)))
def thermo(d, x, top, bot, level, A=255):
    rb = 70; w = 64
    d.rounded_rectangle([P(x - w / 2), P(top), P(x + w / 2), P(bot)], radius=P(w / 2), fill=(255, 255, 255, int(A * 0.18)), outline=WHITE + (A,), width=P(5))
    d.ellipse([P(x - rb), P(bot - 20), P(x + rb), P(bot + 2 * rb - 20)], fill=RED + (A,), outline=WHITE + (A,), width=P(5))
    ylev = bot - (bot - top - 20) * level
    d.rounded_rectangle([P(x - w / 2 + 14), P(ylev), P(x + w / 2 - 14), P(bot + 30)], radius=P(16), fill=RED + (A,))
    for k in range(6):
        y = top + 40 + k * (bot - top - 60) / 5; d.line([(P(x + w / 2 + 8), P(y)), (P(x + w / 2 + 36), P(y))], fill=WHITE + (int(A * 0.7),), width=P(4))
def s4(fr, d, t):
    title(d, ['HOTTEST', 'PLANET'], t, t0=ST[3] + 0.05, colors=[WHITE, RED])
    a = prog(t, ST[3] + 0.1, 0.3)
    lv = eo(prog(t, T[7] + 0.4, D[7] * 0.8))
    thermo(d, 300, 520, 1080, lv * 0.93, int(255 * a))
    if lv > 0:
        txt(d, f'{round(465 * lv)}°C', 690, 760, 150, YEL if lv < 1 else ORANGE, stroke=6, shadow=True)
    icon(fr, 'fire', 690, 990, 200 * back(prog(t, T[7] + D[7] * 0.85, 0.4)) * (0.95 + 0.05 * pulse(t, 3)))
def s5(fr, d, t):
    title(d, ['HOTTER THAN', 'MERCURY'], t, t0=ST[4] + 0.05, colors=[WHITE, YEL])
    icon(fr, 'sun', 110, 840, 340 * back(prog(t, ST[4] + 0.1, 0.5)))
    sm = back(prog(t, ev(8, 'mercury'), 0.45)); sv = back(prog(t, ST[4] + 0.3, 0.45))
    planet(fr, 450, 840, 58 * sm, MER, MB, rot=t * 0.3)
    venus(fr, 790, 840, 100 * sv, t, glow=0.6 + 0.4 * pulse(t))
    txt(d, 'MERCURY', 450, 960, 40 * sm, GRAY, stroke=3); txt(d, '~430°C MAX', 450, 1015, 40 * sm, GRAY, stroke=3)
    txt(d, 'VENUS', 790, 990, 46 * sv, YEL, stroke=3); txt(d, '~465°C', 790, 1050, 52 * sv, ORANGE, stroke=3)
    c = prog(t, ev(8, 'closer') - 0.1, 0.4)
    if c > 0:
        x1 = 260 + (390 - 260) * eo(c); d.line([(P(260), P(1130)), (P(x1), P(1130))], fill=CYAN + (255,), width=P(7))
        pill(d, 'CLOSER TO THE SUN', 380, 1210, 36, CYAN, DARK, back(c))
def s6(fr, d, t):
    title(d, ['THE REASON'], t, t0=ST[5] + 0.05, colors=[YEL])
    cx, cy, r = 540, 860, 215
    at = prog(t, ev(9, 'thick') - 0.2, 0.6)
    venus(fr, cx, cy, r * back(prog(t, ST[5] + 0.15, 0.5)), t, glow=0.3)
    if at > 0:
        for k in range(7):
            rr = r + 12 + k * 13; d.ellipse([P(cx - rr), P(cy - rr), P(cx + rr), P(cy + rr)], outline=(250, 225, 160, int(at * (90 - k * 10))), width=P(13))
        for j in range(5):
            sx, sy = 70, 440 + j * 60; tx, ty = cx - r * 0.8 + j * 30, cy - r * 0.7 + j * 40
            L = math.hypot(tx - sx, ty - sy); ux, uy = (tx - sx) / L, (ty - sy) / L; off = (t * 260) % 70; s_ = -off
            while s_ < L:
                a0, a1 = max(0, s_), min(L, s_ + 40)
                if a1 > a0: d.line([(P(sx + ux * a0), P(sy + uy * a0)), (P(sx + ux * a1), P(sy + uy * a1))], fill=YEL + (int(230 * at),), width=P(8))
                s_ += 70
        for j in range(10):
            a = math.radians(j * 36 + t * 70); rr = r + 45
            x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
            d.ellipse([P(x - 11), P(y - 11), P(x + 11), P(y + 11)], fill=RED + (int(230 * at),))
    pill(d, 'CO2 BLANKET TRAPS HEAT', 540, 1235, 42, ORANGE, DARK, back(prog(t, ev(9, 'carbon'), 0.45)))
def s7(fr, d, t):
    title(d, ['CRUSHING', 'PRESSURE'], t, t0=ST[6] + 0.05, colors=[WHITE, CYAN])
    a = prog(t, ST[6] + 0.1, 0.35); A = int(255 * a)
    x0, x1, y0, y1 = 300, 700, 520, 1180
    if a > 0:
        n = 44
        for k in range(n):
            f = k / n; c = (int(70 * (1 - f) + 6 * f), int(170 * (1 - f) + 22 * f), int(230 * (1 - f) + 70 * f))
            d.rectangle([P(x0), P(y0 + (y1 - y0) * k / n), P(x1), P(y0 + (y1 - y0) * (k + 1) / n + 1)], fill=c + (A,))
        d.rectangle([P(x0), P(y0), P(x1), P(y1)], outline=WHITE + (A,), width=P(4))
        for m in (0, 300, 600, 900):
            y = y0 + (y1 - y0) * m / 1000
            d.line([(P(x1), P(y)), (P(x1 + 30), P(y))], fill=WHITE + (A,), width=P(4))
            txt(d, f'{m} m', x1 + 45, y, 36, WHITE, a, anchor='lm')
    dp = eio(prog(t, T[10] + 0.2, D[10] * 0.8)); y = y0 + (y1 - y0) * 0.9 * dp
    if a > 0:
        d.polygon([(P(x0 - 10), P(y)), (P(x0 - 50), P(y - 24)), (P(x0 - 50), P(y + 24))], fill=YEL + (A,))
        d.line([(P(x0), P(y)), (P(x1), P(y))], fill=YEL + (A,), width=P(5))
        txt(d, f'{round(900 * dp)} m', x0 - 70, y, 44, YEL, a, anchor='rm', stroke=3)
    pill(d, '≈ 92× EARTH PRESSURE', 540, 1255, 44, CYAN, DARK, back(prog(t, T[10] + D[10] * 0.85, 0.45)))
def s8(fr, d, t): outro(fr, d, t - ST[7], T[11] - ST[7], T[11] - ST[7] + D[11] * 0.5, tagline='SPACE > FICTION')

frame = make_frame([s1, s2, s3, s4, s5, s6, s7, s8], ST, fade_in={1, 2, 3, 4, 5, 6, 7}, subs=subs_from(EN, TR, T, D), no_wm={7})
if __name__ == '__main__':
    if sys.argv[1] == 'info': print(round(TOTAL, 2), [round(x, 2) for x in ST])
    else: cli(frame, TOTAL, HERE)
