"""LogicCoreLab short #7 (finance / trending, Nov 23 2026) - Nvidia's 11 days: CEO out, record quarter, CEO back. 4K vertical.
Facts only from multiple outlets; no logos or likeness used. python3 video.py info | preview t1 t2 ... | render"""
import math, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from engine import *
HERE = os.path.dirname(os.path.abspath(__file__))

for name, code in [('ceo', '1f9d1-200d-1f4bc'), ('chair', '1fa91'), ('money', '1f4b0'), ('chart', '1f4c8'), ('warn', '26a0'), ('bulb', '1f4a1')]:
    load_icon(name, code)

EN = {1: "In just eleven days, Nvidia lost its CEO, posted record revenue, and then got him back.",
      2: "On November twelfth, Jensen Huang, who co-founded Nvidia in nineteen ninety-three, suddenly resigned.",
      3: "Reports had raised national security questions. He has not been accused of any crime.",
      4: "Five days later, without him, Nvidia reported one hundred fifteen point eight billion dollars in quarterly revenue. More than double a year earlier.",
      5: "The board said he would not return.",
      6: "Then, on November twenty-third, it reversed course and voted unanimously to reinstate him.",
      7: "Nvidia's stock jumped more than twenty-five percent in a single morning.",
      8: "The lesson? For investors, one leader can be worth hundreds of billions of dollars.",
      9: "Follow LogicCoreLab for more stories behind the headlines."}
TR = {1: "Sadece 11 günde Nvidia CEO'sunu kaybetti, rekor gelir açıkladı ve sonra onu geri aldı.",
      2: "12 Kasım'da, Nvidia'yı 1993'te kuranlardan Jensen Huang aniden istifa etti.",
      3: "Haberler ulusal güvenlik soruları gündeme getirmişti. Huang herhangi bir suçla itham edilmedi.",
      4: "Beş gün sonra, o olmadan, Nvidia çeyreklik 115,8 milyar dolar gelir açıkladı. Bir yıl öncesinin iki katından fazla.",
      5: "Yönetim kurulu geri dönmeyeceğini söyledi.",
      6: "Sonra 23 Kasım'da geri adım attı ve oybirliğiyle onu göreve iade etti.",
      7: "Nvidia hissesi tek bir sabahta yüzde 25'ten fazla yükseldi.",
      8: "Ders mi? Yatırımcılar için tek bir lider yüz milyarlarca dolar değerinde olabilir.",
      9: "Manşetlerin arkasındaki hikâyeler için LogicCoreLab'i takip et!"}
SCN_S = [[1], [2, 3], [4, 5], [6, 7], [8], [9]]
T, D, ST, TOTAL, ev = make_timeline(EN, SCN_S, os.path.join(HERE, 'audio'))
NG = (118, 185, 0); AMBER = (245, 158, 11)

def disclaimer(d): txt(d, 'NOT FINANCIAL ADVICE · SOURCES IN DESCRIPTION', 540, 1335, 24, GRAY, 0.8)
_st = {}
def stamp(fr, text, cx, cy, color, s, angle=-10):
    if s <= 0.01: return
    key = (text, color)
    if key not in _st:
        f = font(96); bb = ImageDraw.Draw(Image.new('RGBA', (8, 8))).textbbox((0, 0), text, font=f, anchor='lt')
        tw, th = bb[2] - bb[0], bb[3] - bb[1]; pad = P(30)
        L = Image.new('RGBA', (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
        ld.rounded_rectangle([P(6), P(6), L.width - P(6), L.height - P(6)], radius=P(22), outline=color + (255,), width=P(11))
        ld.text((pad - bb[0], pad - bb[1]), text, font=f, fill=color + (255,)); _st[key] = L
    L = _st[key]; L2 = L.resize((max(2, int(L.width * s * 0.85)), max(2, int(L.height * s * 0.85))), Image.BICUBIC).rotate(-angle, resample=Image.BICUBIC, expand=True)
    fr.paste(L2, (P(cx) - L2.width // 2, P(cy) - L2.height // 2), L2)

def s1(fr, d, t):
    title(d, ['11 DAYS', 'OF CHAOS'], t, colors=[YEL, WHITE])
    lp = eio(prog(t, 0.4, 1.0)); y = 830
    if lp > 0: d.line([(P(140), P(y)), (P(140 + 800 * lp), P(y))], fill=(255, 255, 255, 200), width=P(6))
    for x, date, lab, col, ic, key in [(180, 'NOV 12', 'CEO OUT', RED, 'chair', 'lost'), (540, 'NOV 17', 'RECORD $', NG, 'money', 'record'), (900, 'NOV 23', 'CEO BACK', YEL, 'ceo', 'back')]:
        s = back(prog(t, ev(1, key) - 0.1, 0.4))
        if s <= 0.01: continue
        d.ellipse([P(x - 20 * s), P(y - 20 * s), P(x + 20 * s), P(y + 20 * s)], fill=col + (255,), outline=WHITE + (255,), width=P(4))
        icon(fr, ic, x, y - 150, 130 * s)
        txt(d, date, x, y + 60, 40 * s, WHITE, stroke=3); pill(d, lab, x, y + 130, 34, col, DARK if col != RED else WHITE, s)
    disclaimer(d)
def s2(fr, d, t):
    title(d, ['THE EXIT'], t, t0=ST[1] + 0.05, colors=[RED])
    a = back(prog(t, ST[1] + 0.1, 0.5)); tr = ev(2, 'resigned') - 0.1; out = eio(prog(t, tr, 0.9))
    icon(fr, 'chair', 540, 790, 300 * a)
    if out < 1: icon(fr, 'ceo', 540 + 420 * out, 700, 250 * a, alpha=1 - out)
    q = prog(t, T[3] - 0.15, 0.3)
    pill(d, 'CO-FOUNDER · 1993', 540, 1010, 42, GOLD, DARK, back(prog(t, ev(2, 'nineteen') - 0.1, 0.4)), 1 - q)
    pill(d, 'RESIGNED · NOV 12', 540, 1110, 46, RED, WHITE, back(prog(t, tr + 0.1, 0.4)), 1 - q)
    if q > 0:
        pill(d, 'NATIONAL SECURITY QUESTIONS', 540, 1010, 38, AMBER, DARK, back(q))
        pill(d, 'NOT ACCUSED OF ANY CRIME', 540, 1110, 40, WHITE, DARK, back(prog(t, ev(3, 'accused') - 0.3, 0.4)))
        icon(fr, 'warn', 860, 560, 110 * back(q))
    disclaimer(d)
def s3(fr, d, t):
    title(d, ['RECORD', 'QUARTER'], t, t0=ST[2] + 0.05, colors=[WHITE, NG])
    base = 1130; Hmax = 470; a = prog(t, ST[2] + 0.1, 0.3)
    d.line([(P(150), P(base)), (P(930), P(base))], fill=(255, 255, 255, int(200 * a)), width=P(5))
    p1 = eo(prog(t, T[4] + 0.2, 0.8)); h1 = Hmax * 57 / 115.8 * p1
    if h1 > 2: d.rounded_rectangle([P(240), P(base - h1), P(440), P(base)], radius=P(16), fill=(120, 130, 160, 255))
    if p1 > 0.6: txt(d, '~$57B', 340, base - h1 - 45, 50, GRAY, stroke=3)
    txt(d, 'A YEAR AGO', 340, base + 45, 34, GRAY, a)
    p2 = eo(prog(t, ev(4, 'reported') - 0.1, 1.4)); h2 = Hmax * p2
    if h2 > 2: d.rounded_rectangle([P(640), P(base - h2), P(840), P(base)], radius=P(16), fill=NG + (255,))
    if p2 > 0.05: txt(d, f'${115.8 * p2:.1f}B', 740, base - h2 - 45, 56, NG, stroke=4, shadow=True)
    txt(d, 'NOV 17', 740, base + 45, 34, WHITE, a)
    pill(d, '+103% YEAR OVER YEAR', 540, 490, 42, NG, DARK, back(prog(t, ev(4, 'double') - 0.2, 0.4)))
    pill(d, 'BOARD: HE WON\'T RETURN', 540, 1262, 40, RED, WHITE, back(prog(t, T[5], 0.4)))
    disclaimer(d)
SERIES = [0.80 - 0.42 * (x / 40) + 0.03 * math.sin(x * 1.7) + 0.02 * math.sin(x * 4.3) for x in range(41)] + [0.42 + 0.33 * (k / 6) ** 0.6 for k in range(1, 7)]
def s4(fr, d, t):
    title(d, ['THE U-TURN'], t, t0=ST[3] + 0.05, colors=[YEL])
    tr = ev(6, 'reinstate') - 0.2
    icon(fr, 'ceo', 300, 620, 230 * back(prog(t, ev(6, 'reversed') - 0.1, 0.5)))
    ss = 2.0 - 1.0 * eo(prog(t, tr, 0.2)) if t >= tr else 0
    stamp(fr, 'REINSTATED', 700, 600, NG, ss)
    pill(d, 'UNANIMOUS VOTE', 720, 730, 38, NG, DARK, back(prog(t, ev(6, 'unanimously') - 0.1, 0.4)))
    a = prog(t, T[7] - 0.3, 0.4)
    if a > 0:
        x0, x1, y0, y1 = 130, 950, 880, 1250; A = int(255 * a)
        d.rounded_rectangle([P(x0 - 10), P(y0 - 10), P(x1 + 10), P(y1 + 10)], radius=P(20), fill=(0, 0, 0, int(110 * a)), outline=(255, 255, 255, int(60 * a)), width=P(3))
        txt(d, 'NVDA', x0 + 20, y0 + 30, 34, GRAY, a, anchor='lm')
        n = len(SERIES); pr = eio(prog(t, T[7], D[7] * 0.85)); k = max(2, int(n * pr))
        pts = [(x0 + (x1 - x0) * i / (n - 1), y1 - (y1 - y0) * SERIES[i]) for i in range(k)]
        dn = [p for i, p in enumerate(pts) if i <= 40]; upp = [p for i, p in enumerate(pts) if i >= 40]
        if len(dn) > 1: d.line([(P(x), P(y)) for x, y in dn], fill=RED + (A,), width=P(7), joint='curve')
        if len(upp) > 1: d.line([(P(x), P(y)) for x, y in upp], fill=NG + (A,), width=P(9), joint='curve')
        if k >= n: pill(d, '+25%+ IN ONE MORNING', 690, 960, 40, NG, DARK, back(prog(t, T[7] + D[7] * 0.85, 0.4)))
    disclaimer(d)
def s5(fr, d, t):
    title(d, ['THE LESSON'], t, t0=ST[4] + 0.05, colors=[YEL])
    a = back(prog(t, ST[4] + 0.15, 0.5))
    icon(fr, 'ceo', 270, 760, 230 * a)
    txt(d, '=', 520, 760, 150 * a, WHITE, stroke=5)
    for k, (dx, dy) in enumerate([(0, 0), (-95, 70), (95, 70), (-45, 150), (45, 150), (-140, 150), (140, 150)]):
        icon(fr, 'money', 790 + dx, 650 + dy, 130 * back(prog(t, ev(8, 'one leader') + k * 0.07, 0.35)))
    s = back(prog(t, ev(8, 'hundreds') - 0.1, 0.45))
    txt(d, 'HUNDREDS OF', 540, 1010, 76 * s, YEL, stroke=5, shadow=True)
    txt(d, 'BILLIONS $', 540, 1100, 76 * s, YEL, stroke=5, shadow=True)
    disclaimer(d)
def s6(fr, d, t): outro(fr, d, t - ST[5], T[9] - ST[5] - 0.2, T[9] - ST[5] + D[9] * 0.2, tagline='BEHIND THE HEADLINES')

frame = make_frame([s1, s2, s3, s4, s5, s6], ST, fade_in={1, 2, 3, 4, 5}, subs=subs_from(EN, TR, T, D), no_wm={5})
if __name__ == '__main__':
    if sys.argv[1] == 'info': print(round(TOTAL, 2), [round(x, 2) for x in ST])
    else: cli(frame, TOTAL, HERE)
