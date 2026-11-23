"""Tiny synth library for LogicCoreLab background scores (pure numpy/scipy, no samples, no AI)."""
import wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}
def hz(n): return 440.0 * 2 ** ((NOTE[n[:-1]] + 12 * (int(n[-1]) + 1) - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)

class Score:
    def __init__(self, total, seed=1):
        self.total = total; self.L = np.zeros((int(SR * (total + 3)), 2)); self.rng = np.random.default_rng(seed)

    def add(self, sig, t0, gain=1.0, pan=0.0):
        i = int(t0 * SR)
        if i >= len(self.L) or i < 0: return
        j = min(len(self.L), i + len(sig)); sig = sig[:j - i]
        self.L[i:j, 0] += sig * gain * np.cos((pan + 1) * np.pi / 4) * 1.414
        self.L[i:j, 1] += sig * gain * np.sin((pan + 1) * np.pi / 4) * 1.414

    @staticmethod
    def env(n, a, r):
        e = np.ones(n); na, nr = max(1, int(a * SR)), max(1, int(r * SR))
        e[:na] = np.linspace(0, 1, na)
        if nr < n: e[-nr:] *= np.linspace(1, 0, nr)
        return e

    def saw(self, f, n, det=0.0):
        ph = (f * (1 + det) * np.arange(n) / SR + self.rng.random()) % 1.0
        return 2 * ph - 1

    # ---- instruments ----
    def pizz(self, note, t0, gain=0.3, pan=0.0, length=0.45):
        n = int(length * SR); t = np.arange(n) / SR; f = hz(note)
        s = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t) + 0.18 * np.sin(6 * np.pi * f * t)
        s *= np.exp(-t / 0.11); s[:40] *= np.linspace(0, 1, 40)
        s += bp(self.rng.standard_normal(n), 1500, 5000) * np.exp(-t / 0.006) * 0.25
        self.add(s, t0, gain, pan)

    def marimba(self, note, t0, gain=0.25, pan=0.0):
        n = int(0.9 * SR); t = np.arange(n) / SR; f = hz(note)
        s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.35) + 0.35 * np.sin(2 * np.pi * f * 3.99 * t) * np.exp(-t / 0.06)
        s[:30] *= np.linspace(0, 1, 30); self.add(s, t0, gain, pan)

    def bell(self, note, t0, gain=0.2, pan=0.0):
        n = int(2.2 * SR); t = np.arange(n) / SR; f = hz(note)
        s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / d) for m, a, d in [(1, 1, 0.9), (2.76, 0.4, 0.4), (5.4, 0.2, 0.15), (8.93, 0.1, 0.08)])
        s[:40] *= np.linspace(0, 1, 40); self.add(s, t0, gain, pan)

    def pad(self, notes, t0, dur, gain=0.2, cutoff=1100, att=0.8, rel=1.2):
        n = int((dur + rel) * SR); s = np.zeros(n)
        for nt in notes:
            for d in (-0.004, 0.0, 0.004): s += self.saw(hz(nt), n, d)
        s = lp(s, cutoff, 4) / (3 * len(notes)); self.add(s * self.env(n, att, rel), t0, gain)

    def bass(self, note, t0, dur, gain=0.35):
        n = int(dur * SR); t = np.arange(n) / SR; f = hz(note)
        s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
        self.add(s * self.env(n, 0.01, min(0.25, dur * 0.5)) * np.exp(-t / 1.5), t0, gain)

    def tick(self, t0, gain=0.05, hi=True):
        n = int(0.04 * SR); t = np.arange(n) / SR
        s = bp(self.rng.standard_normal(n), 3000 if hi else 1500, 9000 if hi else 4000) * np.exp(-t / 0.006)
        self.add(s, t0, gain, 0.35 if hi else -0.35)

    def kick(self, t0, gain=0.4):
        n = int(0.45 * SR); t = np.arange(n) / SR
        f = 45 + 110 * np.exp(-t / 0.035)
        self.add(np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18)), t0, gain)

    def clap(self, t0, gain=0.12):
        n = int(0.2 * SR); t = np.arange(n) / SR
        self.add(bp(self.rng.standard_normal(n), 900, 4000) * np.exp(-t / 0.05), t0, gain)

    def riser(self, t_end, dur, gain=0.08):
        n = int(dur * SR); s = hp(self.rng.standard_normal(n), 2500) * np.linspace(0, 1, n) ** 2.5
        self.add(s, t_end - dur, gain)

    def hit(self, t0, gain=0.5, root='A'):
        self.kick(t0, gain)
        n = int(1.6 * SR); t = np.arange(n) / SR
        self.add(hp(self.rng.standard_normal(n), 3500) * np.exp(-t / 0.45), t0, gain * 0.12)
        for nt in (root + '1', root + '2'): self.bass(nt, t0, 1.4, gain * 0.5)

    # ---- patterns ----
    def arp(self, chord, t0, t1, step, inst='pizz', gain=0.26, pattern=(0, 1, 2, 1)):
        fn = getattr(self, inst); t, i = t0, 0
        while t < t1 - 0.05:
            fn(chord[pattern[i % len(pattern)]], t, gain, 0.3 if i % 2 else -0.3); t += step; i += 1

    def ticks(self, t0, t1, step, gain=0.05):
        t, i = t0, 0
        while t < t1 - 0.02: self.tick(t, gain, i % 2 == 0); t += step; i += 1

    def progression(self, chords, t0, t1, step, inst='pizz', argain=0.26, padg=0.16, cut=1000, bassg=0.3, pat=(0, 1, 2, 1)):
        seg = (t1 - t0) / len(chords)
        for k, (ch, root) in enumerate(chords):
            a = t0 + k * seg; b = a + seg
            self.pad(ch, a, seg, padg, cut); self.bass(root, a, seg, bassg)
            self.arp([c.replace('3', '4').replace('2', '3') for c in ch], a, b, step, inst, argain, pat)

    # ---- output ----
    def write(self, path, fade=2.0):
        L = self.L; rng = self.rng
        ir_n = int(1.6 * SR); tt = np.arange(ir_n) / SR
        ir = rng.standard_normal((ir_n, 2)) * np.exp(-tt / 0.4)[:, None]
        for c in range(2): ir[:, c] = lp(ir[:, c], 6000)
        ir /= np.sqrt((ir ** 2).sum(0))
        wet = np.stack([fftconvolve(L[:, c], ir[:, c])[:len(L)] for c in range(2)], 1)
        mix = hp((L * 0.85 + wet * 0.35).T, 35).T[:int(self.total * SR)]
        fo = int(fade * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
        mix = np.tanh(mix / np.max(np.abs(mix)) * 1.3) / np.tanh(1.3) * 0.9
        with wave.open(path, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((mix * 32767).astype('<i2').tobytes())
        return len(mix) / SR

# common chords: (chord tones, bass root)
Am = (['A3', 'C4', 'E4'], 'A2'); F = (['F3', 'A3', 'C4'], 'F2'); C = (['C4', 'E4', 'G4'], 'C3'); G = (['G3', 'B3', 'D4'], 'G2')
Dm = (['D4', 'F4', 'A4'], 'D3'); E = (['E3', 'G#3', 'B3'], 'E2'); Em = (['E3', 'G3', 'B3'], 'E2')
