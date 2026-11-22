"""LogicCoreLab - 'curious puzzle' background score, synthesized from scratch (no samples, no AI).
Usage: python3 puzzle_score.py out.wav [total_seconds] [scene_start,scene_start,...]
Sections follow the scene starts of the Monty Hall short by default."""
import sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
OUT = sys.argv[1] if len(sys.argv) > 1 else 'puzzle_score.wav'
TOTAL = float(sys.argv[2]) if len(sys.argv) > 2 else 60.91
ST = [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else \
    [0, 6.79, 9.35, 15.10, 19.25, 24.45, 32.75, 41.16, 46.13, 55.32]
WRONG = ST[4] + 3.62          # "Wrong." hit
SWITCH = ST[8] + 7.75         # "Would you switch now?"
rng = np.random.default_rng(42)
L = np.zeros((int(SR * (TOTAL + 3)), 2))

NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}
def hz(n): return 440.0 * 2 ** ((NOTE[n[:-1]] + 12 * (int(n[-1]) + 1) - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)

def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= len(L): return
    j = min(len(L), i + len(sig)); sig = sig[:j - i]
    L[i:j, 0] += sig * gain * np.cos((pan + 1) * np.pi / 4) * 1.414
    L[i:j, 1] += sig * gain * np.sin((pan + 1) * np.pi / 4) * 1.414

def env(n, a, r):
    e = np.ones(n); na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na)
    if nr < n: e[-nr:] *= np.linspace(1, 0, nr)
    return e

def saw(f, n, det=0.0):
    ph = (f * (1 + det) * np.arange(n) / SR + rng.random()) % 1.0
    return 2 * ph - 1

# ---------------- instruments ----------------
def pizz(note, t0, gain=0.3, pan=0.0, length=0.45):
    n = int(length * SR); t = np.arange(n) / SR; f = hz(note)
    s = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t) + 0.18 * np.sin(6 * np.pi * f * t)
    s *= np.exp(-t / 0.11); s[:40] *= np.linspace(0, 1, 40)
    s += bp(rng.standard_normal(n), 1500, 5000) * np.exp(-t / 0.006) * 0.25
    add(s, t0, gain, pan)

def marimba(note, t0, gain=0.25, pan=0.0):
    n = int(0.9 * SR); t = np.arange(n) / SR; f = hz(note)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.35) + 0.35 * np.sin(2 * np.pi * f * 3.99 * t) * np.exp(-t / 0.06)
    s[:30] *= np.linspace(0, 1, 30); add(s, t0, gain, pan)

def bell(note, t0, gain=0.2, pan=0.0):
    n = int(2.2 * SR); t = np.arange(n) / SR; f = hz(note)
    s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / d) for m, a, d in [(1, 1, 0.9), (2.76, 0.4, 0.4), (5.4, 0.2, 0.15), (8.93, 0.1, 0.08)])
    s[:40] *= np.linspace(0, 1, 40); add(s, t0, gain, pan)

def pad(notes, t0, dur, gain=0.2, cutoff=1100, att=0.8, rel=1.2):
    n = int((dur + rel) * SR); s = np.zeros(n)
    for nt in notes:
        for d in (-0.004, 0.0, 0.004): s += saw(hz(nt), n, d)
    s = lp(s, cutoff, 4) / (3 * len(notes)); add(s * env(n, att, rel), t0, gain)

def bass(note, t0, dur, gain=0.35):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(note)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    add(s * env(n, 0.01, min(0.25, dur * 0.5)) * np.exp(-t / 1.5), t0, gain)

def tick(t0, gain=0.05, hi=True):
    n = int(0.04 * SR); t = np.arange(n) / SR
    s = bp(rng.standard_normal(n), 3000 if hi else 1500, 9000 if hi else 4000) * np.exp(-t / 0.006)
    add(s, t0, gain, 0.35 if hi else -0.35)

def kick(t0, gain=0.4):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / 0.035)
    add(np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18)), t0, gain)

def riser(t_end, dur, gain=0.08):
    n = int(dur * SR); s = hp(rng.standard_normal(n), 2500) * np.linspace(0, 1, n) ** 2.5
    add(s, t_end - dur, gain)

def hit(t0, gain=0.5):
    kick(t0, gain)
    n = int(1.6 * SR); t = np.arange(n) / SR
    add(hp(rng.standard_normal(n), 3500) * np.exp(-t / 0.45), t0, gain * 0.12)
    for nt in ('A1', 'A2'): bass(nt, t0, 1.4, gain * 0.5)

# ---------------- score ----------------
B = 0.6  # 100 BPM
def arp(chord, t0, t1, step=B / 2, inst=pizz, gain=0.28, pattern=(0, 1, 2, 1)):
    t, i = t0, 0
    while t < t1 - 0.05:
        inst(chord[pattern[i % len(pattern)]], t, gain, 0.3 if i % 2 else -0.3); t += step; i += 1

def ticks(t0, t1, step=B, gain=0.05):
    t, i = t0, 0
    while t < t1 - 0.02: tick(t, gain, i % 2 == 0); t += step; i += 1

def progression(chords, t0, t1, **kw):
    seg = (t1 - t0) / len(chords)
    for k, (ch, root) in enumerate(chords):
        a = t0 + k * seg; b = a + seg
        pad(ch, a, seg, kw.get('padg', 0.16), kw.get('cut', 1000)); bass(root, a, seg, kw.get('bassg', 0.3))
        arp([c.replace('3', '4').replace('2', '3') for c in ch], a, b, kw.get('step', B / 2), kw.get('inst', pizz), kw.get('argain', 0.26), kw.get('pat', (0, 1, 2, 1)))

Am, F, C, G, Dm, E = (['A3', 'C4', 'E4'], 'A2'), (['F3', 'A3', 'C4'], 'F2'), (['C4', 'E4', 'G4'], 'C3'), (['G3', 'B3', 'D4'], 'G2'), (['D4', 'F4', 'A4'], 'D3'), (['E3', 'G#3', 'B3'], 'E2')

# A: the game (S1-S3) - curious pizzicato + clock
progression([Am, F, C, G, Am, F], 0.0, ST[3], cut=900)
ticks(0.0, ST[3])
riser(ST[3], 1.0, 0.05)
# B: the question (S4) - tension
progression([Dm, E], ST[3], ST[4], cut=1300, step=B / 4, pat=(0, 1, 2, 1, 2, 1, 0, 1))
ticks(ST[3], ST[4], B / 2, 0.06)
riser(ST[4], 1.2, 0.07)
# C: 50/50 ... WRONG (S5) - suspense, then hit and silence
pad(['A2', 'E3'], ST[4], WRONG - ST[4], 0.2, 500, att=0.3, rel=0.3)
ticks(ST[4], WRONG - 0.1, B / 2, 0.07)
hit(WRONG, 0.55)
# D: explanation (S6-S7) - thoughtful marimba
progression([C, G, Am, F, C, G, F, G], ST[5], ST[7], inst=marimba, argain=0.22, padg=0.14, cut=1200, pat=(0, 1, 2, 1))
ticks(ST[5], ST[7], B, 0.035)
riser(ST[7], 1.0, 0.06)
# E: win rate (S8) - bright 'aha'
progression([F, G, C, C], ST[7], ST[8], inst=marimba, argain=0.24, padg=0.18, cut=1800, step=B / 4)
for k, nt in enumerate(['C5', 'E5', 'G5', 'C6']): bell(nt, ST[7] + 1.6 + k * 0.15, 0.12)
# F: 100 doors (S9) - accelerating build on A pedal
t = ST[8]; i = 0; seq = ['A3', 'C4', 'E4', 'A4', 'E4', 'C4']
while t < SWITCH - 0.1:
    prog = (t - ST[8]) / (SWITCH - ST[8]); step = B / 2 - (B / 2 - B / 6) * prog
    pizz(seq[i % 6], t, 0.22 + 0.1 * prog, 0.3 if i % 2 else -0.3); t += step; i += 1
pad(['A2', 'E3', 'A3'], ST[8], SWITCH - ST[8], 0.17, 700, att=1.0, rel=0.3)
bass('A1', ST[8], SWITCH - ST[8], 0.3)
t = ST[8]
while t < SWITCH - 0.1: kick(t, 0.12 + 0.18 * (t - ST[8]) / (SWITCH - ST[8])); t += B
riser(SWITCH, 2.0, 0.1)
hit(SWITCH, 0.45)
for k, nt in enumerate(['A4', 'C#5', 'E5']): bell(nt, SWITCH + k * 0.08, 0.1)
# G: outro (S10) - resolution
pad(['A3', 'C#4', 'E4'], SWITCH, ST[9] - SWITCH + 0.2, 0.15, 1500)
progression([C, G], ST[9], ST[9] + 2.4, inst=marimba, argain=0.22, padg=0.16, cut=1600)
pad(['C3', 'G3', 'C4', 'E4'], ST[9] + 2.4, TOTAL - ST[9] - 2.4, 0.2, 1800, att=0.3, rel=1.5)
bass('C2', ST[9] + 2.4, TOTAL - ST[9] - 2.4, 0.35)
for k, nt in enumerate(['C5', 'E5', 'G5', 'C6']): bell(nt, ST[9] + 2.4 + k * 0.12, 0.12)

# ---------------- mix ----------------
ir_n = int(1.6 * SR); tt = np.arange(ir_n) / SR
ir = rng.standard_normal((ir_n, 2)) * np.exp(-tt / 0.4)[:, None]
for c in range(2): ir[:, c] = lp(ir[:, c], 6000)
ir /= np.sqrt((ir ** 2).sum(0))
wet = np.stack([fftconvolve(L[:, c], ir[:, c])[:len(L)] for c in range(2)], 1)
mix = hp((L * 0.85 + wet * 0.35).T, 35).T[:int(TOTAL * SR)]
fo = int(2.0 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix = np.tanh(mix / np.max(np.abs(mix)) * 1.3) / np.tanh(1.3) * 0.9
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('wrote', OUT, round(len(mix) / SR, 2), 's')
