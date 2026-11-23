"""Business-news score + sfx for the Nvidia short (self-synthesized, no AI, no credits)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'music')); sys.path.insert(0, HERE)
from synthlib import Score, SR, bp, Am, F, C, G, Dm, E, Em
import video as V
S = V.ST; T = V.T; D = V.D; TOTAL = V.TOTAL; B = 0.55
m = Score(TOTAL, seed=2026)
def groove(t0, t1, g=0.16):
    t = t0; i = 0
    while t < t1 - 0.05:
        if i % 4 in (0, 2): m.kick(t, g)
        if i % 4 in (1, 3): m.clap(t, g * 0.5)
        m.tick(t + B / 2, 0.035, True); t += B; i += 1
# intro: urgent news pulse
m.progression([Am, F, C, G], 0.0, S[1], B / 2, inst='pizz', argain=0.2, padg=0.15, cut=1100)
groove(0.0, S[1], 0.14)
# exit: tense, sparse
m.pad(['A2', 'E3', 'A3'], S[1], S[2] - S[1], 0.2, 600, att=0.5, rel=0.4)
m.ticks(S[1], S[2], B, 0.06)
m.kick(V.ev(2, 'resigned') - 0.1, 0.35)
m.progression([Dm, Am, E], T[3], S[2], B / 2, inst='marimba', argain=0.16, padg=0.1, cut=800)
m.riser(S[2], 1.0, 0.06)
# record quarter: uplifting, then board says no (darker)
m.progression([F, G, C, Am], S[2], T[5], B / 2, inst='marimba', argain=0.2, padg=0.16, cut=1500)
groove(S[2], T[5], 0.13)
for k, nt in enumerate(['C5', 'E5', 'G5']): m.bell(nt, V.ev(4, 'double') - 0.2 + k * 0.1, 0.1)
m.pad(['A2', 'C3', 'E3'], T[5], S[3] - T[5], 0.2, 600, att=0.1, rel=0.3); m.bass('A1', T[5], S[3] - T[5], 0.3)
# u-turn: suspense -> hit on REINSTATED -> triumphant rally
tr = V.ev(6, 'reinstate') - 0.2
m.pad(['E2', 'B2', 'E3'], S[3], tr - S[3], 0.2, 700, att=0.3, rel=0.1)
t = S[3]; step = B
while t < tr - 0.05: m.tick(t, 0.07); t += step; step = max(B / 6, step * 0.9)
m.riser(tr, 1.4, 0.1); m.hit(tr, 0.55, 'C')
m.progression([C, G, Am, F], tr, S[4], B / 4, inst='pizz', argain=0.18, padg=0.18, cut=1800, pat=(0, 1, 2, 1, 0, 2, 1, 2))
groove(tr, S[4], 0.17)
# lesson: reflective
m.progression([Am, F, C, G], S[4], S[5], B, inst='marimba', argain=0.18, padg=0.16, cut=1100)
# outro
m.hit(S[5], 0.4, 'C')
m.pad(['C3', 'G3', 'C4', 'E4'], S[5], TOTAL - S[5], 0.2, 1700, att=0.3, rel=1.5); m.bass('C2', S[5], TOTAL - S[5], 0.33)
for k, nt in enumerate(['C5', 'E5', 'G5', 'C6']): m.bell(nt, S[5] + 0.2 + k * 0.12, 0.12)
print('music', round(m.write(os.path.join(HERE, 'out', 'music.wav')), 2), 's')
fx = Score(TOTAL, seed=2027)
def pop(t0, g=0.25, f0=500, f1=1400):
    n = int(0.09 * SR); tt = np.arange(n) / SR
    fx.add(np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * np.exp(-tt / 0.03), t0, g)
def whoosh(t0, g=0.22, dur=0.6):
    n = int(dur * SR); fx.add(bp(fx.rng.standard_normal(n), 300, 3000) * np.sin(np.linspace(0, np.pi, n)) ** 2, t0, g)
def cash(t0, g=0.18):
    for k, f in enumerate([2093, 2637, 3136]):
        n = int(0.5 * SR); tt = np.arange(n) / SR; fx.add(np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.12), t0 + k * 0.05, g)
for k in range(1, len(S)): whoosh(S[k] - 0.3)
for key in ('lost', 'record', 'back'): pop(V.ev(1, key) - 0.1, 0.22)
pop(V.ev(2, 'nineteen') - 0.1, 0.2); whoosh(V.ev(2, 'resigned') - 0.1, 0.25, 0.8)
pop(T[3] - 0.15, 0.2); pop(V.ev(3, 'accused') - 0.3, 0.2)
for k in range(14): fx.tick(V.ev(4, 'reported') - 0.1 + k * 0.1, 0.12)
cash(V.ev(4, 'reported') + 1.3); pop(V.ev(4, 'double') - 0.2, 0.22); pop(T[5], 0.22)
pop(V.ev(6, 'unanimously') - 0.1, 0.2)
cash(T[7] + D[7] * 0.85, 0.2)
pop(V.ev(8, 'hundreds') - 0.1, 0.22); cash(V.ev(8, 'hundreds'), 0.16)
pop(S[5] + 0.05, 0.25)
print('fx', round(fx.write(os.path.join(HERE, 'out', 'fx.wav'), fade=0.3), 2), 's')
