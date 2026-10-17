"""Soundtrack for the Seismic confidential-contracts video. numpy only.
Reads cues.json (written by render.cjs) so hits land on the picture.
Run: python3 audio.py  -> soundtrack.wav"""
import json, wave
import numpy as np

SR = 44100
C = json.load(open('cues.json'))
DUR = C['DUR']
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N); REV = np.zeros(N)
rng = np.random.default_rng(11)

def tt(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.uniform(-1, 1, int(SR * d))
def fft_filter(x, lo=0, hi=SR / 2):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))
def add(sig, at, gain=1.0, pan=0.0, rev=0.0):
    i = int(at * SR)
    if i >= N or i + len(sig) <= 0: return
    if i < 0: sig = sig[-i:]; i = 0
    s = sig[:N - i] * gain
    lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(s)] += s * lg; R[i:i + len(s)] += s * rg
    if rev: REV[i:i + len(s)] += s * rev
def hz(n): return 440.0 * 2 ** ((n - 69) / 12)
def env(t, a, d): return np.minimum(t / a, 1) * np.exp(-np.maximum(t - a, 0) / d)

# ---------------- music ----------------
BEAT = 0.6                 # 100 BPM
HIT = C['impact'][1]       # the Seismic drop; the groove is phased to it
def grid(a, b, step=BEAT, off=0.0):
    k0 = int(np.ceil((a - HIT - off) / step))
    out = []
    while True:
        x = HIT + off + k0 * step
        if x >= b: return out
        out.append(x); k0 += 1

# chords (F minor): Fm, Db, Ab, Eb ; each 4 beats
CH = [[53, 56, 60, 65], [49, 53, 56, 61], [56, 60, 63, 68], [51, 55, 58, 63]]
def pad_note(f, d):
    t = tt(d)
    s = sum(np.sin(2 * np.pi * f * h * (1 + det) * t + h) / h ** 1.4
            for h in (1, 2, 3, 4) for det in (-.003, 0, .004))
    return s * np.minimum(t / .9, 1) * np.minimum((d - t) / .9, 1)

def pad_level(x):
    if x < 7: return .55
    if x < HIT: return .7
    if x < 64: return .5
    if x < 72.5: return .85
    return .8
bar = 4 * BEAT
start = HIT - bar * np.ceil(HIT / bar)
k = 0; x = start
while x < DUR:
    ch = CH[k % 4]
    for n in ch:
        add(pad_note(hz(n), bar + 1.0), x - .5, .018 * pad_level(max(x, 0)), pan=rng.uniform(-.5, .5), rev=.6)
    k += 1; x += bar

def kick():
    t = tt(.5); f = 45 + 110 * np.exp(-t / .03)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .2) + noise(.5) * np.exp(-t / .004) * .4
    return np.tanh(2 * s) * .9
def hat(d=.06):
    t = tt(d); return np.diff(np.concatenate([[0], noise(d)])) * np.exp(-t / .018) * .5
def sub(f, d=.55):
    t = tt(d); return np.sin(2 * np.pi * f * t) * env(t, .01, .22)
def bassnote(x):
    ch = CH[int(np.floor((x - start) / bar)) % 4]
    return hz(ch[0] - 24)

KK = kick()
# tension pulse in the problem scene (sub only)
for b in grid(7.2, HIT - .3):
    add(sub(bassnote(b)), b, .35)
# groove: steps 1-4
for b in grid(HIT, 63.7):
    add(KK, b, .55)
    add(sub(bassnote(b)), b + BEAT / 2, .3)
    add(hat(), b + BEAT / 2, .22, pan=.3)
    if b > 21.5: add(hat(.03), b + BEAT * .75, .1, pan=-.3)
# breakdown in "why", then a final pulse into the outro
for b in grid(64.2, 72.4, BEAT * 2):
    add(sub(bassnote(b), 1.0), b, .32)
for b in grid(74.0, 79.0):
    add(KK, b, .35); add(hat(), b + BEAT / 2, .14, pan=.3)

# ---------------- sfx ----------------
def whoosh(d=1.1):
    n = noise(d); t = tt(d)
    shape = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    lo = fft_filter(n, 200, 1800); hi = fft_filter(n, 1800, 9000)
    mixk = t / d
    return (lo * (1 - mixk) + hi * mixk * .7) * shape * 1.6
for w in C['whoosh']:
    add(whoosh(), w - .05, .55, pan=.4, rev=.2)

def impact():
    t = tt(2.2); f = 34 + 70 * np.exp(-t / .08)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .7)
    crack = fft_filter(noise(2.2), 1500, 12000) * np.exp(-t / .05)
    return np.tanh(1.6 * boom) * .9 + crack * .5
for i, x in enumerate(C['impact']):
    add(impact(), x, .8 if i == 1 else .55, rev=.5)

def swell(d=.85):
    t = tt(d); n = fft_filter(noise(d), 2000, 14000)
    return n * (t / d) ** 3
for x in C['swell']:
    add(swell(), x - .07 if x < 20 else x, .5, rev=.3)

def click():
    t = tt(.05)
    return (np.sin(2 * np.pi * 2600 * t) * np.exp(-t / .006) * .6 + noise(.05) * np.exp(-t / .002) * .5)
for x in C['clicks']:
    add(click(), x, .5, pan=.1)

def key():
    t = tt(.04)
    f = rng.uniform(1800, 3200)
    return (noise(.04) * np.exp(-t / .004) * .6 + np.sin(2 * np.pi * f * t) * np.exp(-t / .008) * .3)
for a, b in C['type']:
    x = a
    while x < b:
        add(key(), x, .22, pan=rng.uniform(-.3, .3)); x += rng.uniform(.045, .09)

def pop():
    t = tt(.18); f = 700 + 500 * (1 - np.exp(-t / .02))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, .004, .05)
for x in C['pops']:
    add(pop(), x, .18, pan=rng.uniform(-.4, .4), rev=.3)

for a, b in C['scramble']:
    x = a
    while x < b:
        t = tt(.03); f = rng.choice([1200, 1600, 2400, 3200])
        add(np.sign(np.sin(2 * np.pi * f * t)) * np.exp(-t / .01) * .25, x, .07, pan=rng.uniform(-.6, .6))
        x += .035

# ---------------- reverb + master ----------------
ir_t = tt(2.6)
ir = rng.normal(0, 1, len(ir_t)) * np.exp(-ir_t / .55)
ir = fft_filter(ir, 150, 7000); ir /= np.abs(ir).sum() ** .5 * 6
M = 1 << int(np.ceil(np.log2(N + len(ir))))
wet = np.fft.irfft(np.fft.rfft(REV, M) * np.fft.rfft(ir, M), M)[:N]
L += wet; R += np.roll(wet, int(.013 * SR))
st = np.stack([L, R])
fade = np.ones(N); fl = int(1.2 * SR); fade[-fl:] = np.linspace(1, 0, fl)
st *= fade
st = np.tanh(st / np.abs(st).max() * 1.4) * .89
with wave.open('soundtrack.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st.T * 32767).astype('<i2').tobytes())
print('ok', DUR)
