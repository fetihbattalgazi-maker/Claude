"""Lonely-but-hopeful score + sfx for the Voyager 1 short (self-synthesized, no AI, no credits)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'music')); sys.path.insert(0, HERE)
from synthlib import Score, SR, bp, Am, F, C, G, Em, Dm
import video as V
S = V.ST; T = V.T; D = V.D; TOTAL = V.TOTAL; B = 0.75
m = Score(TOTAL, seed=1977)
def beeps(t0, t1, g=0.08, f=1400):
    t = t0; pat = [0.12, 0.12, 0.36, 0.12, 0.36, 0.36]; i = 0
    while t < t1:
        n = int(pat[i % len(pat)] * 0.5 * SR); tt = np.arange(n) / SR
        m.add(np.sin(2 * np.pi * f * tt) * Score.env(n, 0.005, 0.02), t, g, 0.3); t += pat[i % len(pat)] + 0.15; i += 1
        if i % 6 == 0: t += 0.8
# 1-2: lonely and vast
m.progression([Am, F, C, G], 0.0, S[1], B, inst='marimba', argain=0.18, padg=0.18, cut=850)
beeps(0.6, S[1] - 0.5, 0.04)
m.progression([Am, F, C, Em], S[1], S[2], B / 2, inst='marimba', argain=0.18, padg=0.18, cut=1000)
m.bell('E5', T[2] + 1.0, 0.1); m.bell('A5', T[3] + 0.2, 0.1)
# 3: signal lost - music thins to a drone + distant beeps that stop
stop = T[4] + D[4] * 0.55
m.pad(['A2', 'E3'], S[2], S[3] - S[2], 0.2, 500, att=0.4, rel=0.4)
beeps(S[2] + 0.2, stop, 0.07)
m.kick(stop + 0.1, 0.3)
m.pad(['A3', 'C4', 'E4'], T[5], S[3] - T[5], 0.12, 900, att=1.0, rel=0.5)
# 4: waiting - slow clock
m.progression([Dm, Am, Em, Am], S[3], S[4], B, inst='pizz', argain=0.16, padg=0.16, cut=900)
m.ticks(S[3], S[4], 0.5, 0.06)
# 5: golden record - warm and nostalgic
m.progression([C, G, Am, F], S[4], S[5], B / 2, inst='marimba', argain=0.2, padg=0.18, cut=1400)
for k, nt in enumerate(['C5', 'E5', 'G5', 'C6']): m.bell(nt, V.ev(7, 'golden') - 0.2 + k * 0.12, 0.1)
# 6: open question - hopeful but unresolved
m.pad(['F3', 'A3', 'C4', 'E4'], S[5], 3.0, 0.2, 1300, att=0.4, rel=1.0)
m.pad(['G3', 'B3', 'D4', 'E4'], S[5] + 3.0, TOTAL - S[5] - 3.0, 0.2, 1300, att=0.6, rel=1.5)
m.bass('F2', S[5], 3.0, 0.3); m.bass('G2', S[5] + 3.0, TOTAL - S[5] - 3.0, 0.3)
m.arp(['E5', 'G5', 'B5', 'D6'], S[5] + 0.5, TOTAL - 1.0, B / 2, 'bell', 0.06)
beeps(TOTAL - 3.0, TOTAL - 0.8, 0.05)
print('music', round(m.write(os.path.join(HERE, 'out', 'music.wav'), fade=1.5), 2), 's')
fx = Score(TOTAL, seed=1978)
def pop(t0, g=0.25, f0=500, f1=1400):
    n = int(0.09 * SR); tt = np.arange(n) / SR
    fx.add(np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * np.exp(-tt / 0.03), t0, g)
def whoosh(t0, g=0.22, dur=0.6):
    n = int(dur * SR); fx.add(bp(fx.rng.standard_normal(n), 300, 3000) * np.sin(np.linspace(0, np.pi, n)) ** 2, t0, g)
def static(t0, dur=0.6, g=0.08):
    n = int(dur * SR); fx.add(bp(fx.rng.standard_normal(n), 1500, 6000) * Score.env(n, 0.02, 0.3), t0, g)
for k in range(1, len(S)): whoosh(S[k] - 0.3)
pop(V.ev(1, 'nineteen'), 0.2); pop(V.ev(1, 'full day') - 0.1, 0.2)
pop(V.ev(2, 'november') - 0.1, 0.2); pop(V.ev(2, 'light-day') - 0.1, 0.22)
for k in range(14): fx.tick(T[3] + k * D[3] * 0.85 / 14, 0.12)
static(stop, 0.9, 0.12); pop(stop + 0.2, 0.22)
pop(T[5], 0.2); pop(V.ev(5, 'computer') - 0.2, 0.22)
pop(V.ev(6, 'command') - 0.2, 0.2); pop(V.ev(6, 'answer') - 0.2, 0.2)
pop(V.ev(7, 'transmitter') - 0.1, 0.2); pop(V.ev(7, 'golden') - 0.2, 0.22)
pop(T[8] + 0.1, 0.22)
print('fx', round(fx.write(os.path.join(HERE, 'out', 'fx.wav'), fade=0.3), 2), 's')
