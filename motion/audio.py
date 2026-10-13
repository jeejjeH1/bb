"""Soundtrack for the MASTER intro. 20s, 120 BPM, F minor. Timeline matches scene.html.
Run: python3 audio.py  -> soundtrack.wav"""
import numpy as np, wave
from scipy import signal as ss

SR = 44100
DUR = 20.0
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
REV = np.zeros(N)          # reverb send (mono)
PADBUS = np.zeros((2, N))  # sidechained bus
rng = np.random.default_rng(7)

def tt(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.uniform(-1, 1, int(SR * d))
def bp(x, lo, hi, order=2): return ss.sosfilt(ss.butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)
def hp(x, f, order=2): return ss.sosfilt(ss.butter(order, f, 'high', fs=SR, output='sos'), x)
def lp(x, f, order=2): return ss.sosfilt(ss.butter(order, f, 'low', fs=SR, output='sos'), x)

def add(sig, at, gain=1.0, pan=0.0, rev=0.0, bus=None):
    i = int(at * SR)
    if i >= N: return
    s = sig[: N - i] * gain
    lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    if bus is not None:
        bus[0, i:i + len(s)] += s * lg; bus[1, i:i + len(s)] += s * rg
    else:
        L[i:i + len(s)] += s * lg; R[i:i + len(s)] += s * rg
    if rev: REV[i:i + len(s)] += s * rev

def note(n):  # midi -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)

# ---------------- instruments ----------------
def kick():
    t = tt(.55)
    f = 42 + 120 * np.exp(-t / .035)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .22)
    s += noise(.55) * np.exp(-t / .004) * .5
    return np.tanh(2.2 * s) * .9

def snare():
    t = tt(.4)
    body = np.sin(2 * np.pi * 185 * t) * np.exp(-t / .05)
    sn = bp(noise(.4), 1200, 9000) * np.exp(-t / .13)
    clap = np.zeros_like(t)
    for d in (0, .011, .022):
        i = int(d * SR); seg = bp(noise(.4), 900, 3000) * np.exp(-tt(.4) / .03)
        clap[i:] += seg[: len(clap) - i] * .6
    return np.tanh(1.6 * (body * .6 + sn * .9 + clap))

def hat(open_=False):
    d = .25 if open_ else .06
    t = tt(d)
    return hp(noise(d), 7000, 4) * np.exp(-t / (.08 if open_ else .018)) * .9

def sub(freq, d):
    t = tt(d)
    f = freq * (1 + .5 * np.exp(-t / .03))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    env = np.minimum(1, t / .005) * np.exp(-t / (d * .6))
    return np.tanh(2.5 * s) * env  # drive adds audible harmonics on phones

def saw(freq, d, detune=(0, -.11, .12)):
    t = tt(d); out = np.zeros_like(t)
    for c in detune:
        out += ss.sawtooth(2 * np.pi * freq * 2 ** (c / 12) * t + rng.uniform(0, 6.28))
    return out / len(detune)

def pad(freqs, d, cutoff=1600):
    t = tt(d)
    s = sum(saw(f, d) for f in freqs) / len(freqs)
    env = np.minimum(1, t / .25) * np.minimum(1, (d - t) / .2)
    return lp(s, cutoff, 2) * env

def pluck(freq, d=.22):
    t = tt(d)
    s = saw(freq, d, (0, .07)) + .4 * np.sin(2 * np.pi * freq * 2 * t)
    return lp(s * np.exp(-t / .07), 4200) * np.minimum(1, t / .002)

def stab(freqs, d=.8):
    t = tt(d)
    s = sum(saw(f, d) for f in freqs) / len(freqs)
    cut = lp(s, 5000) * np.exp(-t / .18)
    return np.tanh(2 * cut)

def riser(d, f0=180, f1=2600):
    t = tt(d)
    k = t / d
    f = f0 * (f1 / f0) ** k
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * .35
    nz = noise(d)
    # chunked rising bandpass noise
    out = np.zeros_like(t); ch = int(.04 * SR)
    for i in range(0, len(t), ch):
        c = f0 * 3 * (f1 / f0) ** (i / len(t))
        seg = bp(nz[i:i + ch * 2], max(80, c * .6), min(18000, c * 2.2))
        w = np.hanning(len(seg)); out[i:i + len(seg)] += seg * w
    return (tone + out * .9) * k ** 2

def reverse_cym(d):
    t = tt(d)
    return hp(noise(d), 4000, 2) * (t / d) ** 3

def impact():
    t = tt(2.6)
    f = 32 + 60 * np.exp(-t / .08)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .9)
    crack = lp(noise(2.6), 3500) * np.exp(-t / .25)
    hi = hp(noise(2.6), 3000) * np.exp(-t / .5) * .4
    return np.tanh(1.8 * (boom * 1.2 + crack * .8 + hi))

def whoosh(d=.32):
    t = tt(d)
    k = t / d
    env = np.sin(np.pi * k) ** 2
    out = np.zeros_like(t); nz = noise(d); ch = int(.02 * SR)
    for i in range(0, len(t), ch):
        c = 400 + 3200 * np.sin(np.pi * i / len(t))
        seg = bp(nz[i:i + ch * 2], c * .7, c * 1.6); out[i:i + len(seg)] += seg * np.hanning(len(seg))
    return out * env

def crackle(d=.45, seed=1):
    r = np.random.default_rng(seed)
    out = np.zeros(int(SR * d))
    for _ in range(70):
        i = r.integers(0, len(out) - 400)
        out[i:i + 300] += hp(r.uniform(-1, 1, 300), 2500) * r.uniform(.3, 1)
    t = tt(d)
    return out * np.exp(-t / .2)

def tick(f=3200):
    t = tt(.025)
    return np.sin(2 * np.pi * f * t) * np.exp(-t / .006)

# ---------------- arrangement ----------------
# chords per bar (bar = 2s). F minor: Fm, Db, Eb, Ab
CH = {'Fm': [53, 56, 60], 'Db': [49, 53, 56], 'Eb': [51, 55, 58], 'Ab': [56, 60, 63]}
ROOT = {'Fm': 41, 'Db': 37, 'Eb': 39, 'Ab': 44}
BARS = ['Fm', 'Fm', 'Db', 'Eb', 'Fm', 'Db', 'Ab', 'Eb', 'Fm', 'Fm']

KICK_PAT = {2: [0, 6, 10], 4: [0, 6, 10], 6: [0, 8], 8: [0, 4, 8, 12], 10: [0, 4, 8, 12], 12: [0, 4, 8, 12], 16: [0, 6, 10]}
S = .125
k_, s_ = kick(), snare()
kick_times = []
for b, steps in KICK_PAT.items():
    for st in steps:
        tk = b + st * S; kick_times.append(tk)
        add(k_, tk, 1.0)
        add(sub(note(ROOT[BARS[int(tk // 2)]] - 12 + 12), .45), tk, .55)
for b in [2, 4, 8, 10, 12, 16]:
    for beat in (1, 3):
        add(s_, b + beat * .5, .75, 0, rev=.25)
# hats
for b in [2, 4, 8, 10, 12, 16]:
    for st in range(16):
        tk = b + st * S
        if b in (8, 10, 12):
            add(hat(st % 4 == 2), tk, .28 if st % 4 == 2 else .16, .3)
        elif st % 2 == 0:
            add(hat(), tk, .22 if st % 4 == 2 else .12, .3)
    # roll on the last beat
    for j in range(6):
        add(hat(), b + 1.5 + j * (.5 / 6), .1 + j * .02, -.3)
# stats bar: ticks with counters
for i in range(24):
    add(tick(2600 + (i % 3) * 400), 6 + i * .0625, .18, (i % 2) * .6 - .3)

# pads (whole piece, sidechained)
for i, c in enumerate(BARS):
    st = i * 2
    if 14 <= st < 16:
        add(pad([note(n) for n in CH[c]], 2.0, 900), st, .22, rev=.4, bus=PADBUS)
    else:
        add(pad([note(n) for n in CH[c]], 2.1, 1800 if st >= 2 else 700), st, .28 if st else .18, rev=.35, bus=PADBUS)
# arp plucks in drop sections
ARP = [0, 1, 2, 1, 2, 0, 1, 2]
for b in [2, 4, 8, 10, 12]:
    c = CH[BARS[b // 2]]
    for st in range(16):
        n = c[ARP[st % 8]] + 12 + (12 if st % 8 == 7 else 0)
        add(pluck(note(n)), b + st * S, .16, (st % 2) * .5 - .25, rev=.3)
# lead hook on the statement + finale
HOOK = [(4.0, 72, .25), (4.25, 75, .25), (4.5, 77, .5), (5.0, 80, .25), (5.25, 79, .25), (5.5, 77, .5),
        (16.5, 77, .25), (16.75, 80, .25), (17.0, 84, .5), (17.5, 82, .25), (17.75, 80, .5)]
for tm, n, d in HOOK:
    add(stab([note(n), note(n - 12)], d + .2), tm, .22, 0, rev=.4)

# FX
add(riser(2.0), 0, .55, rev=.3)
add(reverse_cym(.9), 1.1, .35)
for p in (2, 16, 18):
    add(impact(), p, 1.0, rev=.5)
    add(stab([note(n) for n in CH['Fm']] + [note(41 + 12)], 1.2), p, .45, rev=.6)
for c in [4, 6, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14]:
    add(whoosh(), c - .2, .45, ((c * 2) % 2) - .5)
for p, sd in [(2, 1), (3, 2), (4.5, 3), (5.5, 4), (16, 5), (18, 6)]:
    add(crackle(.45, sd), p, .35, .4 if sd % 2 else -.4, rev=.2)
add(hp(noise(.08), 5000) * np.exp(-tt(.08) / .02), 5.5, .5)  # "HIT." snap
# typing ticks in the boot
for i in range(25):
    add(tick(1800 + (i * 137) % 900), .25 + i * .03, .12, .2)
# build: snare roll + riser + reverse cymbal, then silence before the drop
roll_t = 14.0
while roll_t < 15.85:
    prog = (roll_t - 14) / 1.85
    add(s_, roll_t, .2 + .55 * prog, 0, rev=.15)
    roll_t += .25 if roll_t < 14.5 else .125 if roll_t < 15 else .0625 if roll_t < 15.5 else .03125
add(riser(1.85, 120, 4000), 14.0, .6, rev=.3)
add(reverse_cym(1.0), 14.85, .45)
add(sub(note(29), 1.8) * .6, 14.0, .5)

# ---------------- mix ----------------
side = np.ones(N)
for kt in kick_times + [2, 16, 18]:
    i = int(kt * SR); d = int(.3 * SR)
    side[i:i + d] = np.minimum(side[i:i + d], 1 - .65 * np.exp(-np.arange(min(d, N - i)) / (SR * .09)))
L += PADBUS[0] * side; R += PADBUS[1] * side
ir_t = tt(2.2)
irL = rng.uniform(-1, 1, len(ir_t)) * np.exp(-ir_t / .55)
irR = rng.uniform(-1, 1, len(ir_t)) * np.exp(-ir_t / .55)
rv = lp(hp(REV, 250), 6000)
L += ss.fftconvolve(rv, irL)[:N] * .05
R += ss.fftconvolve(rv, irR)[:N] * .05
# silence gap before final drop
g0, g1 = int(15.9 * SR), int(16.0 * SR)
fade = np.linspace(1, 0, int(.03 * SR))
for ch in (L, R):
    ch[g0:g0 + len(fade)] *= fade; ch[g0 + len(fade):g1] = 0
mix = np.stack([hp(L, 28), hp(R, 28)])
mix = np.tanh(mix * 1.1)
mix /= np.max(np.abs(mix)) / .93
tail = int(1.2 * SR); mix[:, -tail:] *= np.linspace(1, 0, tail) ** 1.5
pcm = (mix.T * 32767).astype(np.int16)
with wave.open('soundtrack.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', pcm.shape)
