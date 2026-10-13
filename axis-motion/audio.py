"""Soundtrack v2 for the AXIS Robotics 10s motion. 150 BPM, F# minor, hard-hitting. Synced to scene.html.
Run: python3 audio.py -> soundtrack.wav"""
import numpy as np, wave
from scipy import signal as ss

SR = 44100
DUR = 10.0
N = int(SR * DUR)
B = 0.4
rng = np.random.default_rng(11)
MUS = np.zeros((2, N))   # music bus (filtered in the "simulation" section)
SFX = np.zeros((2, N))   # hits / whooshes, unfiltered
REV = np.zeros(N)

def tt(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.uniform(-1, 1, int(SR * d))
def filt(x, f, kind, order=2): return ss.sosfilt(ss.butter(order, f, kind, fs=SR, output='sos'), x)
def hz(n): return 440.0 * 2 ** ((n - 69) / 12)

def add(sig, at, gain=1.0, pan=0.0, rev=0.0, bus=None):
    bus = MUS if bus is None else bus
    i = int(round(at * SR))
    if i >= N or i < 0: return
    s = sig[: N - i] * gain
    lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    bus[0, i:i + len(s)] += s * lg; bus[1, i:i + len(s)] += s * rg
    if rev: REV[i:i + len(s)] += s * rev

# ---------- instruments ----------
def kick(hard=1.0):
    t = tt(.45); f = 48 + 160 * np.exp(-t / .025)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .16)
    s += filt(noise(.45), 3000, 'high') * np.exp(-t / .004) * .5
    return np.tanh(3.0 * hard * s) * .95

def snare():
    t = tt(.3)
    body = np.sin(2 * np.pi * 200 * t) * np.exp(-t / .04)
    sn = filt(noise(.3), [1500, 10000], 'band') * np.exp(-t / .09)
    return np.tanh(2 * (body * .7 + sn))

def hat(d=.045, open_=False):
    d = .2 if open_ else d
    return filt(noise(d), 8000, 'high', 4) * np.exp(-tt(d) / (.06 if open_ else .012))

def crash(d=1.6):
    t = tt(d); return filt(noise(d), 5000, 'high') * np.exp(-t / .5) * .6

def reese(n, d):
    t = tt(d); f = hz(n)
    s = ss.sawtooth(2 * np.pi * f * t) + ss.sawtooth(2 * np.pi * f * 1.012 * t) + ss.sawtooth(2 * np.pi * f * .994 * t)
    s = filt(s, 900, 'low', 3)
    env = np.minimum(1, t / .004) * np.minimum(1, (d - t) / .01)
    sub = np.sin(2 * np.pi * f / 2 * t) * env
    return np.tanh(1.5 * s * env) * .7 + sub * .7

def stab(notes, d=.18, bright=5000):
    t = tt(d); s = np.zeros_like(t)
    for n in notes:
        for det in (-.15, 0, .15):
            s += ss.sawtooth(2 * np.pi * hz(n + det) * t + rng.uniform(0, 6))
    s = filt(s / (3 * len(notes)), bright, 'low', 2)
    return np.tanh(2 * s) * np.exp(-t / .07)

def pluck(n, d=.18, bright=3000):
    t = tt(d); f = hz(n)
    s = ss.square(2 * np.pi * f * t, .3) * .6 + ss.sawtooth(2 * np.pi * f * 1.005 * t) * .5
    return filt(s, bright, 'low') * np.exp(-t / .05) * .55

def pad(notes, d):
    t = tt(d); s = np.zeros_like(t)
    for n in notes:
        for det in (-.1, 0, .1):
            s += ss.sawtooth(2 * np.pi * hz(n + det) * t + rng.uniform(0, 6))
    return filt(s / (3 * len(notes)), 2000, 'low', 3) * np.minimum(1, t / .05) * np.exp(-t / 1.0)

def sweep(d, up=True, lo=200, hi=9000):
    x = noise(d); out = np.zeros_like(x); hop = 256; n = len(x)
    for i in range(0, n, hop):
        p = i / n; p = p if up else 1 - p
        fc = lo * (hi / lo) ** p
        seg = x[max(0, i - 2048): i + hop]
        o = filt(seg, [fc, min(fc * 1.8, 20000)], 'band')
        out[i:i + hop] = o[-len(out[i:i + hop]):]
    t = tt(d)
    env = (t / d) ** 2.5 if up else np.exp(-t / (d / 4))
    return out * env * 3

def riser(d, n0=54, n1=78):
    t = tt(d); f = hz(n0) * (hz(n1) / hz(n0)) ** (t / d)
    s = ss.sawtooth(2 * np.pi * np.cumsum(f) / SR) + ss.sawtooth(2 * np.pi * np.cumsum(f * 1.01) / SR)
    return filt(s, 4000, 'low') * (t / d) ** 2 * .35

def impact(big=1.0):
    d = 2.0; t = tt(d); f = 30 + 110 * np.exp(-t / .06)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (.45 * big))
    crack = filt(noise(d), 1800, 'high') * np.exp(-t / .05)
    body = filt(noise(d), [80, 600], 'band') * np.exp(-t / .12)
    return np.tanh(2.2 * boom) * .9 + crack * .55 + body * .8

def slash(d=.25):
    return sweep(d, up=False, lo=600, hi=12000)

def blip(n, d=.1):
    t = tt(d); return np.sin(2 * np.pi * hz(n) * t) * np.exp(-t / .025)

def fall(n0, n1, d=.12):
    t = tt(d); f = hz(n0) * (hz(n1) / hz(n0)) ** (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .05)

# F#m - D - A - E (one bar = 4 beats = 1.6s; we change every 2 beats for energy)
CH = [[54, 57, 61], [50, 54, 57], [57, 61, 64], [52, 56, 59]]
ROOT = [30, 26, 33, 28]
def chord_at(t): return int(t / (2 * B)) % 4

# ---------- 0–0.4: intro riser ----------
add(sweep(.4, True), 0, .5, bus=SFX)
add(riser(.4, 42, 78), 0, .8, rev=.2)
for i in range(8): add(snare(), i * .05, .15 + i * .05)

# ---------- groove 0.4 -> 7.6 ----------
t = .4; k = 0
while t < 7.6 - 1e-6:
    add(kick(), t, .95)
    if k % 2 == 1: add(snare(), t, .5, rev=.25)
    for j in range(4):
        add(hat(), t + j * B / 4, .18 if j % 2 else .1, pan=.3 * (-1) ** j)
    add(hat(open_=True), t + B / 2, .14, pan=-.2)
    r = ROOT[chord_at(t)]
    add(reese(r, B * .42), t + B / 2, .42)
    add(reese(r, B * .18), t + B * .75, .25)
    t += B; k += 1

# arp 16ths 0.4->7.6, brightness rises
for i in range(int((7.6 - .4) / (B / 4))):
    tm = .4 + i * B / 4
    c = CH[chord_at(tm)]
    n = c[i % 3] + 12 + (12 if i % 8 in (3, 7) else 0)
    bright = 1500 + 3500 * min(1, (tm - .4) / 5)
    add(pluck(n, .16, bright), tm, .24, pan=.4 * np.sin(i * 1.3), rev=.15)

# ---------- hits & sfx ----------
add(impact(1.3), .4, 1.0, rev=.3, bus=SFX); add(crash(), .4, .5, bus=SFX)
add(sweep(.35, True), .85, .3, bus=SFX)
for i in range(13): add(blip(78 + i, .05), .7 + i * .025, .08, pan=-.6 + i * .1, bus=SFX)   # wordmark letters
add(impact(.6), 1.2, .55, bus=SFX); add(stab(CH[0], .25), 1.2, .45, rev=.3)              # BIGGER
add(impact(.6), 1.38, .55, bus=SFX); add(stab(CH[1], .25), 1.38, .45, rev=.3)            # MODELS?
add(slash(.3), 1.6, .7, bus=SFX); add(impact(.8), 1.6, .6, bus=SFX)                       # strike
add(sweep(.35, True), 1.65, .4, bus=SFX)
add(impact(1.0), 2.0, .8, rev=.3, bus=SFX); add(crash(), 2.0, .4, bus=SFX)              # BETTER DATA
for i in range(11): add(fall(96 - i, 60, .1), 2.0 + i * .025 + (.2 if i >= 6 else 0), .08, pan=-.5 + i * .1, bus=SFX)
for i, c in enumerate([2.8, 3.0, 3.2, 3.4]):                                               # strobe
    add(stab([n + 12 + i * 2 for n in CH[i % 4]], .18, 7000), c, .55, rev=.2)
    add(impact(.4), c, .35, bus=SFX)
add(sweep(.3, True), 3.3, .4, bus=SFX)
add(impact(1.0), 3.6, .7, rev=.3, bus=SFX); add(crash(), 3.6, .35, bus=SFX)              # engine
for i in range(5): add(blip(73 + [0, 2, 4, 7, 12][i], .14), 3.6 + i * .32, .25, rev=.4, bus=SFX)
add(sweep(.4, True), 4.8, .4, bus=SFX)
add(impact(.8), 5.2, .5, bus=SFX)                                                          # simulation
add(sweep(.25, True), 5.55, .5, bus=SFX)
add(impact(1.2), 5.8, .9, rev=.3, bus=SFX); add(crash(), 5.8, .5, bus=SFX); add(slash(.3), 5.8, .5, bus=SFX)  # REALITY
add(impact(.7), 6.4, .55, bus=SFX)                                                         # marquee
add(stab([66, 69, 73, 78], .3, 6000), 6.65, .5, rev=.3)                                     # box pop

# ---------- 7.6–8.4 build ----------
times = []; tm = 7.6; step = B / 2
while tm < 8.3:
    times.append(tm); tm += step; step = max(.03, step * .8)
for i, tm in enumerate(times): add(snare(), tm, .25 + .5 * i / len(times), rev=.1)
add(riser(.7, 54, 90), 7.6, 1.0, rev=.2)
add(sweep(.7, True, 150, 14000), 7.6, .7, bus=SFX)
for i in range(4): add(kick(.6), 7.6 + i * .1, .3)

# ---------- 8.4 finale ----------
add(impact(2.0), 8.4, 1.2, rev=.5, bus=SFX); add(crash(2.0), 8.4, .7, bus=SFX)
add(pad([42, 54, 57, 61, 66, 69], 1.6), 8.4, .7, rev=.5)
for i, tm in enumerate([8.4, 8.8, 9.2, 9.6]):
    add(kick(.9), tm, .8 if i else 0)
    add(reese(30, B * .9), tm, .35 if i < 3 else .2)
    add(hat(open_=True), tm + B / 2, .12)
for i in range(8): add(blip(78 + (i % 4) * 3, .05), 8.52 + i * .03, .06, pan=.5, bus=SFX)  # wordmark
add(blip(85, .2), 9.05, .2, rev=.5, bus=SFX); add(blip(90, .2), 9.1, .12, rev=.5, bus=SFX)  # URL

# ---------- automation: kick sidechain on music, lowpass during "simulation" ----------
sc = np.ones(N)
for tm in np.arange(.4, 7.6, B):
    i = int(tm * SR); g = 1 - .55 * np.exp(-tt(B) / .07)
    sc[i:i + len(g)] = np.minimum(sc[i:i + len(g)], g[: N - i])
a, b = int(5.2 * SR), int(5.8 * SR)
low = np.stack([filt(MUS[ch, a - 2048:b], 700, 'low', 4)[2048:] for ch in (0, 1)])
xf = np.ones(b - a); r = int(.02 * SR); xf[:r] = np.linspace(0, 1, r); xf[-r:] = np.linspace(1, 0, r)
MUS[:, a:b] = MUS[:, a:b] * (1 - xf) + low * xf * 1.3
# gap of silence right before the drop
g0, g1 = int(8.32 * SR), int(8.4 * SR)
MUS[:, g0:g1] *= np.linspace(1, 0, g1 - g0) ** 3
MIX = MUS * np.minimum(1, sc + .0) + SFX

# ---------- reverb ----------
ir_t = tt(1.6)
for ch, seed in ((0, 1), (1, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / .4)
    wet = ss.fftconvolve(filt(REV, 250, 'high'), filt(ir, 6000, 'low'))[:N]
    MIX[ch] += wet / np.max(np.abs(ir)) * .018

# ---------- master ----------
MIX = filt(MIX, 28, 'high')
f0 = int(9.75 * SR); MIX[:, f0:] *= np.linspace(1, 0, N - f0) ** 1.5
MIX = np.tanh(MIX * 1.4) / np.tanh(1.4)
MIX /= np.max(np.abs(MIX)) / .9
pcm = (MIX.T * 32767).astype(np.int16)
with wave.open('soundtrack.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
