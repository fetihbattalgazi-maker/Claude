"""Dreamy music-box score + sfx for the sleep short (self-synthesized, no AI, no credits)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'music')); sys.path.insert(0, HERE)
from synthlib import Score, SR, bp, Am, F, C, G, Dm, E, Em
import video as V
S = V.ST; T = V.T; D = V.D; TOTAL = V.TOTAL; B = 0.62
m = Score(TOTAL, seed=88)
def musicbox(t0, t1, chords, g=0.11):
    seg = (t1 - t0) / len(chords)
    for k, (ch, root) in enumerate(chords):
        a = t0 + k * seg; notes = [c.replace('3', '5').replace('4', '5') for c in ch] + [ch[0].replace('3', '6').replace('4', '6')]
        m.pad(ch, a, seg, 0.14, 900, att=0.8, rel=1.0); m.bass(root, a, seg, 0.22)
        t, i = a, 0
        while t < a + seg - 0.05: m.bell(notes[[0, 1, 2, 3, 2, 1][i % 6]], t, g, 0.3 if i % 2 else -0.3); t += B / 2; i += 1
musicbox(0.0, S[2], [C, Am, F, G, C, Am, F, G])
# battery charging: ascending arps
t = S[2]; seq = ['C4', 'E4', 'G4', 'C5', 'E5', 'G5', 'C6']; i = 0
while t < S[3] - 0.05:
    m.marimba(seq[min(len(seq) - 1, int((t - S[2]) / (S[3] - S[2]) * len(seq)))], t, 0.2); t += B / 3; i += 1
m.pad(['C3', 'G3', 'C4'], S[2], S[3] - S[2], 0.16, 1100, att=0.4, rel=0.4)
# switch on: calm and warm; switch off: tension and drop
musicbox(S[3], T[6], [F, C, G], 0.1)
m.pad(['A2', 'E3'], T[6], S[4] - T[6], 0.22, 500, att=0.2, rel=0.3)
t = T[6]; step = B / 2
while t < V.ev(6, 'dropped') - 0.2: m.tick(t, 0.07); t += step
n = int(1.2 * SR); tt = np.arange(n) / SR; f = np.geomspace(600, 70, n)
m.add(np.sin(2 * np.pi * np.cumsum(f) / SR) * Score.env(n, 0.02, 0.3), V.ev(6, 'dropped') - 0.2, 0.22)
m.kick(V.ev(6, 'seventy') - 0.2, 0.35)
# warning: dark pulse
m.pad(['D2', 'A2', 'D3'], S[4], S[5] - S[4], 0.22, 500, att=0.3, rel=0.3)
t = S[4]
while t < S[5] - 0.1: m.kick(t, 0.16); m.kick(t + 0.22, 0.1); t += 0.9
# outro: lullaby resolution
musicbox(S[5], TOTAL - 0.5, [F, G, C], 0.1)
print('music', round(m.write(os.path.join(HERE, 'out', 'music.wav'), fade=2.0), 2), 's')
fx = Score(TOTAL, seed=89)
def pop(t0, g=0.25, f0=500, f1=1400):
    n = int(0.09 * SR); x = np.arange(n) / SR
    fx.add(np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * np.exp(-x / 0.03), t0, g)
def whoosh(t0, g=0.22, dur=0.6):
    n = int(dur * SR); fx.add(bp(fx.rng.standard_normal(n), 300, 3000) * np.sin(np.linspace(0, np.pi, n)) ** 2, t0, g)
def click(t0, g=0.25):
    n = int(0.03 * SR); x = np.arange(n) / SR; fx.add(bp(fx.rng.standard_normal(n), 2000, 7000) * np.exp(-x / 0.004), t0, g)
for k in range(1, len(S)): whoosh(S[k] - 0.3)
pop(0.25, 0.2); pop(V.ev(1, 'found') - 0.2, 0.22)
pop(V.ev(2, 'basel') - 0.2, 0.2); pop(T[3] - 0.1, 0.2); pop(V.ev(3, 'two groups') - 0.2, 0.2)
for k in range(10): fx.tick(V.ev(3, 'longer') - 0.3 + k * 0.14, 0.1)
pop(V.ev(4, 'pressure') - 0.2, 0.22)
click(T[5] - 0.1); pop(V.ev(5, 'deeper') - 0.2, 0.2)
click(T[6] - 0.1); pop(V.ev(6, 'seventy') - 0.2, 0.25)
pop(V.ev(7, 'survive') - 0.3, 0.2); pop(V.ev(7, 'price') - 0.3, 0.2)
pop(V.ev(8, 'thank') - 0.1, 0.2); pop(V.ev(8, 'follow') - 0.1, 0.22)
print('fx', round(fx.write(os.path.join(HERE, 'out', 'fx.wav'), fade=0.3), 2), 's')
