"""Space-ambient score + sound effects for the Venus short (self-synthesized, no AI, no credits)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'music')); sys.path.insert(0, HERE)
from synthlib import Score, SR, bp
import video as V

S = V.ST; T = V.T; TOTAL = V.TOTAL; B = 0.7
Dm = (['D3', 'F3', 'A3'], 'D2'); Bb = (['Bb2', 'D3', 'F3'], 'Bb1'); Fm = (['F3', 'A3', 'C4'], 'F2'); Cm = (['C3', 'E3', 'G3'], 'C2')
Gm = (['G3', 'Bb3', 'D4'], 'G2'); A7 = (['A2', 'C#3', 'E3'], 'A1')
m = Score(TOTAL, seed=7)
def shimmer(t0, t1, notes, step=B / 2, g=0.1):
    t, i = t0, 0
    while t < t1 - 0.05: m.bell(notes[i % len(notes)], t, g, 0.4 if i % 2 else -0.4); t += step; i += 1
# intro + day vs year: wide space pads with shimmering bells
for k, (ch, root) in enumerate([Dm, Bb, Fm, Cm]):
    a = S[0] + k * (S[2] - S[0]) / 4; b = a + (S[2] - S[0]) / 4
    m.pad(ch, a, b - a, 0.2, 900, att=1.0, rel=1.5); m.bass(root, a, b - a, 0.28)
shimmer(0.3, S[2], ['D5', 'A5', 'F5', 'C6', 'A5', 'E5'], B / 2, 0.07)
m.marimba('A4', T[4], 0.25); m.bell('D6', T[4] + 0.1, 0.12)
m.riser(S[2], 1.0, 0.05)
# spins backwards: reversed-feeling descending arps
m.progression([Gm, Dm, Bb, A7], S[2], S[3], B / 2, inst='pizz', argain=0.22, padg=0.16, cut=1100, pat=(2, 1, 0, 1))
m.ticks(S[2], S[3], B, 0.03)
# heat: tension drone + pulse
m.pad(['D2', 'A2', 'D3'], S[3], S[5] - S[3], 0.22, 600, att=0.5, rel=0.5)
t = S[3]; i = 0
while t < S[5] - 0.1:
    m.kick(t, 0.13 + 0.1 * (t - S[3]) / (S[5] - S[3]))
    if i % 2: m.tick(t + B / 2, 0.05)
    t += B; i += 1
m.arp(['D4', 'F4', 'A4', 'C5'], S[4], S[5], B / 4, 'pizz', 0.18, (0, 1, 2, 3, 2, 1))
m.riser(S[5], 1.2, 0.06)
# the reason: warm, heavy atmosphere
m.progression([Bb, Gm, Dm], S[5], S[6], B / 2, inst='marimba', argain=0.2, padg=0.2, cut=800)
# pressure: deep rumble going down
n = int((S[7] - S[6]) * SR); tt = np.arange(n) / SR
f = np.linspace(110, 45, n); rumble = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * tt))
m.add(rumble * Score.env(n, 0.5, 0.8), S[6], 0.25)
m.pad(['D2', 'F2', 'A2'], S[6], S[7] - S[6], 0.2, 500, att=0.6, rel=0.6)
shimmer(S[6] + 0.2, S[7], ['A4', 'F4', 'D4', 'A3'], B, 0.06)
# outro: uplifting resolution in D major
m.hit(S[7], 0.4, 'D')
m.pad(['D3', 'F#3', 'A3', 'D4'], S[7], TOTAL - S[7], 0.2, 1700, att=0.3, rel=1.5)
m.bass('D2', S[7], TOTAL - S[7], 0.33)
for k, nt in enumerate(['D5', 'F#5', 'A5', 'D6']): m.bell(nt, S[7] + 0.2 + k * 0.12, 0.12)
shimmer(S[7] + 1.0, TOTAL - 1.0, ['D6', 'A5', 'F#5', 'A5'], B / 2, 0.05)
print('music', round(m.write(os.path.join(HERE, 'out', 'music.wav')), 2), 's')

fx = Score(TOTAL, seed=9)
def pop(t0, g=0.25, f0=500, f1=1400):
    n = int(0.09 * SR); t = np.arange(n) / SR; fq = np.linspace(f0, f1, n)
    fx.add(np.sin(2 * np.pi * np.cumsum(fq) / SR) * np.exp(-t / 0.03), t0, g)
def whoosh(t0, g=0.25, dur=0.6):
    n = int(dur * SR); fx.add(bp(fx.rng.standard_normal(n), 300, 3000) * np.sin(np.linspace(0, np.pi, n)) ** 2, t0, g)
def ding(t0, g=0.2):
    n = int(1.0 * SR); t = np.arange(n) / SR
    fx.add((np.sin(2 * np.pi * 1318.5 * t) + 0.5 * np.sin(2 * np.pi * 1975.5 * t)) * np.exp(-t / 0.3), t0, g)
for k in range(1, len(S)): whoosh(S[k] - 0.3, 0.2)
pop(0.25, 0.2); pop(V.ev(1, 'longer'), 0.22)
for k in range(10): fx.tick(T[2] + 0.2 + k * V.D[2] * 0.085, 0.12)
for k in range(10): fx.tick(T[3] + 0.2 + k * V.D[3] * 0.085, 0.12)
ding(T[4] + 0.1, 0.18)
whoosh(T[5], 0.2, 0.8); pop(V.ev(6, 'west') - 0.1, 0.2)
for k in range(14): fx.tick(T[7] + 0.4 + k * V.D[7] * 0.8 / 14, 0.1)
pop(T[7] + V.D[7] * 0.85, 0.25)
pop(V.ev(8, 'mercury'), 0.2); pop(V.ev(8, 'closer') - 0.1, 0.2)
pop(V.ev(9, 'carbon'), 0.22)
pop(T[10] + V.D[10] * 0.85, 0.22)
pop(S[7] + 0.05, 0.25)
print('fx', round(fx.write(os.path.join(HERE, 'out', 'fx.wav'), fade=0.3), 2), 's')
