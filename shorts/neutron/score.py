"""Cosmic score + sfx for the neutron star short (self-synthesized, no AI, no credits)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'music')); sys.path.insert(0, HERE)
from synthlib import Score, SR, bp, hp, Dm, Am, F, C, G
import video as V
S = V.ST; T = V.T; TOTAL = V.TOTAL; B = 0.7
Bb = (['Bb2', 'D3', 'F3'], 'Bb1'); Gm = (['G3', 'Bb3', 'D4'], 'G2')
m = Score(TOTAL, seed=31)
def shimmer(t0, t1, notes, step, g):
    t, i = t0, 0
    while t < t1 - 0.05: m.bell(notes[i % len(notes)], t, g, 0.4 if i % 2 else -0.4); t += step; i += 1
# teaspoon + scale: deep space pads with shimmer
m.progression([Dm, Bb, Gm, Dm], 0.0, S[2], B / 2, inst='marimba', argain=0.16, padg=0.2, cut=900)
shimmer(0.3, S[2], ['D5', 'A5', 'F5', 'C6'], B / 2, 0.06)
m.bell('A5', V.ev(1, 'billion'), 0.12); m.kick(V.ev(2, 'heavier') - 0.1, 0.3)
# giant star: swelling tension then supernova hit
te = V.ev(3, 'explodes') - 0.1
m.pad(['D2', 'A2', 'D3'], S[2], te - S[2], 0.24, 500, att=0.8, rel=0.1)
m.riser(te, 2.0, 0.12)
m.hit(te, 0.6, 'D')
n = int(3.0 * SR); t = np.arange(n) / SR
m.add(bp(m.rng.standard_normal(n), 60, 900) * np.exp(-t / 0.9), te, 0.35)
# collapse: descending sweep, then city bells
tq = V.ev(4, 'squeezed') - 0.2
m.pad(['D3', 'F3', 'A3'], S[3], tq - S[3], 0.16, 800, att=0.6, rel=0.3)
n = int(1.4 * SR); t = np.arange(n) / SR; f = np.geomspace(900, 60, n)
m.add(np.sin(2 * np.pi * np.cumsum(f) / SR) * Score.env(n, 0.05, 0.3), tq, 0.25)
m.kick(tq + 1.3, 0.4)
m.progression([F, C, G], tq + 1.3, S[4], B / 2, inst='pizz', argain=0.2, padg=0.16, cut=1200)
for k, nt in enumerate(['C5', 'E5', 'G5']): m.bell(nt, T[5] + k * 0.1, 0.1)
# pulsar: ticks accelerating
t = S[4]; step = 0.5
while t < S[5] - 0.05: m.tick(t, 0.09, True); m.pizz('A4', t, 0.08); t += step; step = max(0.06, step * 0.9)
m.pad(['A2', 'E3', 'A3'], S[4], S[5] - S[4], 0.2, 900, att=0.3, rel=0.4)
m.riser(S[5], 1.5, 0.08)
# outro
m.hit(S[5], 0.45, 'D')
m.pad(['D3', 'F#3', 'A3', 'D4'], S[5], TOTAL - S[5], 0.2, 1700, att=0.3, rel=1.5); m.bass('D2', S[5], TOTAL - S[5], 0.33)
for k, nt in enumerate(['D5', 'F#5', 'A5', 'D6']): m.bell(nt, S[5] + 0.2 + k * 0.12, 0.12)
print('music', round(m.write(os.path.join(HERE, 'out', 'music.wav')), 2), 's')
fx = Score(TOTAL, seed=32)
def pop(t0, g=0.25, f0=500, f1=1400):
    n = int(0.09 * SR); tt = np.arange(n) / SR
    fx.add(np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * np.exp(-tt / 0.03), t0, g)
def whoosh(t0, g=0.22, dur=0.6):
    n = int(dur * SR); fx.add(bp(fx.rng.standard_normal(n), 300, 3000) * np.sin(np.linspace(0, np.pi, n)) ** 2, t0, g)
for k in range(1, len(S)): whoosh(S[k] - 0.3)
pop(0.25, 0.2); pop(V.ev(1, 'teaspoon') - 0.1, 0.22)
for k in range(12): fx.tick(V.ev(1, 'weigh') + k * (V.ev(1, 'billion') + 0.4 - V.ev(1, 'weigh')) / 12, 0.12)
whoosh(V.ev(2, 'heavier') - 0.1, 0.2, 1.0)
pop(V.ev(4, 'mass') - 0.2, 0.2); pop(V.ev(4, 'twenty') - 0.2, 0.2); pop(T[5] + 0.3, 0.22)
for k in range(10): fx.tick(V.ev(6, 'seven') - 0.3 + k * 0.1, 0.12)
pop(S[5] + 0.05, 0.25)
print('fx', round(fx.write(os.path.join(HERE, 'out', 'fx.wav'), fade=0.3), 2), 's')
