"""Underwater-curious score + sfx for the octopus short (self-synthesized, no AI, no credits)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'music')); sys.path.insert(0, HERE)
from synthlib import Score, SR, bp, Am, F, C, G, Dm, E, Em
import video as V
S = V.ST; T = V.T; TOTAL = V.TOTAL; B = 0.65
m = Score(TOTAL, seed=11)
def bubbles(t0, t1, g=0.06):
    t = t0
    while t < t1:
        n = int(0.06 * SR); tt = np.arange(n) / SR; f0 = m.rng.uniform(500, 1200)
        m.add(np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f0 * 2.2, n)) / SR) * np.exp(-tt / 0.02), t, g, m.rng.uniform(-0.6, 0.6))
        t += m.rng.uniform(0.15, 0.5)
def heartbeat(t0, t1, g=0.3, stop=None):
    t = t0
    while t < t1 - 0.1 and (stop is None or t < stop):
        m.kick(t, g); m.kick(t + 0.22, g * 0.6); t += 0.85
# intro: curious marimba + bubbles
m.progression([Am, F, C, E], 0.0, S[1], B / 2, inst='marimba', argain=0.22, padg=0.16, cut=1000)
bubbles(0.2, S[1], 0.05)
# 3 hearts: heartbeat under a warm progression
m.progression([Am, Dm, F, E], S[1], S[2], B / 2, inst='pizz', argain=0.2, padg=0.16, cut=1100)
heartbeat(S[1] + 0.2, S[2], 0.22)
# swim: heartbeat continues, then stops -> silence -> soft crawl groove
stop = V.ev(4, 'stops')
heartbeat(S[2], stop, 0.26)
m.pad(['A2', 'E3'], S[2], stop - S[2], 0.18, 600, att=0.3, rel=0.2)
m.bell('E4', stop + 0.1, 0.1); m.bell('A3', stop + 0.25, 0.08)
m.progression([Em, C], T[5] - 0.1, S[3], B / 2, inst='pizz', argain=0.2, padg=0.14, cut=900)
# why blue: mysterious
m.progression([Dm, Am, E], S[3], S[4], B / 2, inst='marimba', argain=0.2, padg=0.18, cut=900, pat=(2, 1, 0, 1))
bubbles(S[3], S[4], 0.04)
# neurons: sparkling bells over a lifting progression
m.progression([F, G, Am, C], S[4], S[5], B / 4, inst='marimba', argain=0.18, padg=0.16, cut=1500)
t = T[7] + 0.2
while t < S[5] - 0.2: m.bell(['A5', 'E6', 'C6', 'G5'][int(t * 7) % 4], t, 0.05, m.rng.uniform(-0.5, 0.5)); t += 0.18
# outro
m.hit(S[5], 0.4, 'C')
m.pad(['C3', 'G3', 'C4', 'E4'], S[5], TOTAL - S[5], 0.2, 1700, att=0.3, rel=1.5); m.bass('C2', S[5], TOTAL - S[5], 0.33)
for k, nt in enumerate(['C5', 'E5', 'G5', 'C6']): m.bell(nt, S[5] + 0.2 + k * 0.12, 0.12)
bubbles(S[5] + 0.5, TOTAL - 1.0, 0.04)
print('music', round(m.write(os.path.join(HERE, 'out', 'music.wav')), 2), 's')
fx = Score(TOTAL, seed=12)
def pop(t0, g=0.25, f0=500, f1=1400):
    n = int(0.09 * SR); t = np.arange(n) / SR
    fx.add(np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * np.exp(-t / 0.03), t0, g)
def whoosh(t0, g=0.22, dur=0.6):
    n = int(dur * SR); fx.add(bp(fx.rng.standard_normal(n), 300, 3000) * np.sin(np.linspace(0, np.pi, n)) ** 2, t0, g)
def flatline(t0, dur=1.2, g=0.08):
    n = int(dur * SR); t = np.arange(n) / SR; fx.add(np.sin(2 * np.pi * 1000 * t) * Score.env(n, 0.01, 0.3), t0, g)
for k in range(1, len(S)): whoosh(S[k] - 0.3)
pop(0.3, 0.2); pop(V.ev(1, 'three'), 0.22); pop(V.ev(1, 'blue'), 0.22)
pop(T[2], 0.2); pop(T[3], 0.2)
flatline(stop + 0.2)
pop(T[5] + 0.3, 0.2)
pop(V.ev(6, 'copper') - 0.1, 0.22); pop(V.ev(6, 'iron') - 0.1, 0.22); pop(V.ev(6, 'oxygen') - 0.1, 0.2)
pop(V.ev(7, 'arms') - 0.1, 0.22); pop(V.ev(8, 'taste'), 0.2); pop(V.ev(8, 'react'), 0.2)
pop(S[5] + 0.05, 0.25)
print('fx', round(fx.write(os.path.join(HERE, 'out', 'fx.wav'), fade=0.3), 2), 's')
