"""Background music + sound effects for the Birthday Paradox short (self-synthesized, no AI, no credits)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'music')); sys.path.insert(0, HERE)
from synthlib import Score, SR, bp, hp, Am, F, C, G, Dm, E
import video as V

S = V.SC_START; T = V.T; TOTAL = V.TOTAL; B = 0.6
m = Score(TOTAL, seed=23)
# A: the question + 365 days - curious pizzicato
m.progression([Am, F, C, G], 0.0, S[1], B / 2, cut=900)
m.progression([Am, F, Dm, E], S[1], S[2], B / 2, cut=1000)
m.ticks(0.0, S[2], B, 0.04)
m.riser(S[2], 1.0, 0.05)
# B: "The real answer?" - suspense, accelerating clock, then reveal
m.pad(['A2', 'E3'], S[2], T[4] - S[2], 0.2, 500, att=0.3, rel=0.2)
t = S[2]; step = B / 2
while t < T[4] - 0.05: m.tick(t, 0.07, True); t += step; step = max(B / 8, step * 0.93)
m.riser(T[4], 1.4, 0.09)
m.hit(T[4], 0.5, 'A')
for k, nt in enumerate(['A4', 'C#5', 'E5', 'A5']): m.bell(nt, T[4] + 0.05 + k * 0.1, 0.12)
m.pad(['A3', 'C#4', 'E4'], T[4], S[3] - T[4] + 0.3, 0.16, 1400, att=0.1)
# C: the trick + 253 pairs - marimba, denser in the pairs scene
m.progression([C, G, Am, F], S[3], S[4], B / 2, inst='marimba', argain=0.22, padg=0.14, cut=1200)
m.ticks(S[3], S[4], B, 0.03)
m.progression([C, G, Am, F], S[4], S[5], B / 4, inst='marimba', argain=0.2, padg=0.16, cut=1500, pat=(0, 1, 2, 1, 2, 0, 1, 2))
t = S[4]; i = 0
while t < S[5] - 0.1:
    if i % 2 == 0: m.kick(t, 0.16)
    else: m.clap(t, 0.08)
    t += B; i += 1
m.riser(S[5], 1.0, 0.06)
# D: the curve - rising
m.progression([F, G, Am, C], S[5], S[6], B / 4, cut=1700, argain=0.22, pat=(0, 1, 2, 1, 0, 2, 1, 2))
t = S[5]
while t < S[6] - 0.1: m.kick(t, 0.12 + 0.12 * (t - S[5]) / (S[6] - S[5])); t += B
for tt in (S[5] + 1.0, V.ev(10, 'ninety'), V.ev(11, 'ninety')): m.bell('E5', tt, 0.1); m.bell('B5', tt + 0.06, 0.06)
m.riser(S[6], 1.2, 0.07)
# E: people vs pairs - calm
m.progression([Am, F, C, G], S[6], S[7], B / 2, inst='marimba', argain=0.22, padg=0.14, cut=1200)
for k, nt in enumerate(['C5', 'E5', 'G5']): m.bell(nt, T[13] + k * 0.1, 0.1)
# F: outro - resolution
m.hit(S[7], 0.4, 'C')
m.pad(['C3', 'G3', 'C4', 'E4'], S[7], TOTAL - S[7], 0.2, 1800, att=0.3, rel=1.5)
m.bass('C2', S[7], TOTAL - S[7], 0.35)
m.arp(['C5', 'E5', 'G5'], S[7], S[7] + 3.0, B / 2, 'marimba', 0.18)
for k, nt in enumerate(['C5', 'E5', 'G5', 'C6']): m.bell(nt, S[7] + 0.2 + k * 0.12, 0.12)
print('music', round(m.write(os.path.join(HERE, 'out', 'music.wav')), 2), 's')

# ---------- sound effects (separate track, not ducked) ----------
fx = Score(TOTAL, seed=5)
def pop(t0, g=0.25, f0=500, f1=1400):
    n = int(0.09 * SR); t = np.arange(n) / SR; f = np.linspace(f0, f1, n)
    fx.add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03), t0, g)
def whoosh(t0, g=0.25, dur=0.6):
    n = int(dur * SR); s = bp(fx.rng.standard_normal(n), 300, 3000); e = np.sin(np.linspace(0, np.pi, n)) ** 2
    fx.add(s * e, t0, g)
def ding(t0, g=0.2):
    n = int(1.0 * SR); t = np.arange(n) / SR
    fx.add((np.sin(2 * np.pi * 1318.5 * t) + 0.5 * np.sin(2 * np.pi * 1975.5 * t)) * np.exp(-t / 0.3), t0, g)
for i in range(10): pop(V.ev(1, 'people') + i * 0.1, 0.12, 600 + i * 40, 1300 + i * 60)
pop(V.ev(1, 'fifty'), 0.25); ding(V.ev(1, 'share'), 0.12)
for k in range(12): fx.tick(T[2] + k * (V.ev(2, 'days') + 0.2 - T[2]) / 12, 0.18)
pop(V.ev(2, 'most'), 0.25)
for k in V.FADE_IN: whoosh(S[k] - 0.3, 0.22)
for i in range(23): pop(T[5] - 0.1 + i * 0.04, 0.07, 700 + i * 20, 1500)
pop(T[6] + 0.3, 0.2); whoosh(T[7] + 0.1, 0.2, 1.2)
for k in range(20): fx.tick(T[8] + k * V.D[8] * 0.85 / 20, 0.14)
ding(T[9] + V.D[9] * 0.7, 0.18)
pop(S[5] + 1.0, 0.2); pop(V.ev(10, 'ninety'), 0.2); pop(V.ev(11, 'ninety'), 0.2)
pop(T[12], 0.25); pop(T[13], 0.25); ding(T[13] + 0.5, 0.12)
pop(S[7] + 0.05, 0.25)
print('fx', round(fx.write(os.path.join(HERE, 'out', 'fx.wav'), fade=0.3), 2), 's')
