"""Soundtrack for the AXIS Robotics 10s motion. 120 BPM, A minor. Synced to scene.html cuts.
Run: python3 audio.py -> soundtrack.wav"""
import numpy as np, wave
from scipy import signal as ss

SR = 44100
DUR = 10.0
N = int(SR * DUR)
MIX = np.zeros((2, N)); REV = np.zeros(N); PAD = np.zeros((2, N))
rng = np.random.default_rng(3)
BEAT = 0.5
CUTS = [2.0, 4.4, 6.0, 7.5, 8.8]

def tt(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.uniform(-1, 1, int(SR * d))
def filt(x, f, kind, order=2): return ss.sosfilt(ss.butter(order, f, kind, fs=SR, output='sos'), x)
def hz(n): return 440.0 * 2 ** ((n - 69) / 12)

def add(sig, at, gain=1.0, pan=0.0, rev=0.0, bus=None):
    i = int(at * SR)
    if i >= N: return
    s = sig[: N - i] * gain
    lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    b = MIX if bus is None else bus
    b[0, i:i + len(s)] += s * lg; b[1, i:i + len(s)] += s * rg
    if rev: REV[i:i + len(s)] += s * rev

# ---------- instruments ----------
def kick():
    t = tt(.5); f = 45 + 130 * np.exp(-t / .03)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .2) + noise(.5) * np.exp(-t / .003) * .4
    return np.tanh(2.4 * s) * .9

def hat(d=.05):
    return filt(noise(d), 8000, 'high', 4) * np.exp(-tt(d) / (d / 3))

def clap():
    out = np.zeros(int(SR * .35))
    for d in (0, .01, .02):
        i = int(d * SR); s = filt(noise(.35), [900, 4000], 'band') * np.exp(-tt(.35) / .05)
        out[i:] += s[: len(out) - i]
    return np.tanh(out * 1.5)

def bass(n, d):
    t = tt(d); f = hz(n)
    s = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 7))
    s = filt(s, 700, 'low')
    env = np.minimum(1, t / .005) * np.exp(-t / .25)
    return np.tanh(1.8 * s * env) + np.sin(2 * np.pi * f / 2 * t) * env * .6

def pluck(n, d=.3, bright=3000):
    t = tt(d); f = hz(n)
    s = ss.sawtooth(2 * np.pi * f * t) + ss.sawtooth(2 * np.pi * f * 1.007 * t)
    return filt(s, bright, 'low') * np.exp(-t / .09) * .5

def pad(notes, d):
    t = tt(d); s = np.zeros_like(t)
    for n in notes:
        for det in (-.12, 0, .12):
            s += ss.sawtooth(2 * np.pi * hz(n + det / 12 * 1) * t + rng.uniform(0, 6))
    s = filt(s, 1400, 'low', 3) / (len(notes) * 3)
    return s * np.minimum(1, t / .4) * np.minimum(1, (d - t) / .4)

def whoosh(d, up=True):
    t = tt(d); x = noise(d); out = np.zeros_like(x); hop = 512
    for i in range(0, len(x), hop):
        p = i / len(x); fc = 300 * (40 ** (p if up else 1 - p))
        seg = x[max(0, i - 2048): i + hop]
        out[i:i + hop] = filt(seg, [fc, min(fc * 2.2, 20000)], 'band')[-len(out[i:i + hop]):]
    env = (t / d) ** 2 if up else np.exp(-t / (d / 4))
    return out * env * 2

def impact():
    t = tt(1.6); f = 32 + 90 * np.exp(-t / .05)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .5)
    crack = filt(noise(1.6), 2500, 'high') * np.exp(-t / .04)
    return np.tanh(2 * boom) * .9 + crack * .5

def blip(n, d=.12):
    t = tt(d); return np.sin(2 * np.pi * hz(n) * t) * np.exp(-t / .03)

def tick():
    t = tt(.03); return filt(noise(.03), 3000, 'high') * np.exp(-t / .004)

def shimmer(d=2.0):
    t = tt(d); s = np.zeros_like(t)
    for n in (81, 84, 88, 93):
        s += np.sin(2 * np.pi * hz(n) * t + rng.uniform(0, 6)) * (1 + .3 * np.sin(2 * np.pi * 6 * t))
    return s / 4 * np.minimum(1, t / .01) * np.exp(-t / .6)

# ---------- arrangement ----------
# intro: riser into logo burst, rays tick out, wordmark settles
add(whoosh(.35), 0, .35, rev=.2)
add(impact(), .15, .75, rev=.25)
add(shimmer(), .2, .25, rev=.6)
for i in range(16):
    add(tick(), .1 + i * .03, .25, pan=np.sin(i * 1.7) * .8, rev=.2)
add(blip(76, .3), .85, .18, rev=.5)   # wordmark
add(blip(81, .3), 1.25, .14, rev=.5)  # tagline
add(whoosh(.6), 1.4, .45, rev=.3)     # riser into cut 1

# harmony: Am - F - C - G (2 beats each), pad sidechained
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
roots = [45, 41, 48, 43]
t0 = 0.0; ci = 0
while t0 < DUR:
    add(pad(chords[ci % 4], 1.0 + .4), t0, .35, rev=.3, bus=PAD)
    t0 += 1.0; ci += 1

# arp (16ths) filtered in intro, open later
arp = [69, 72, 76, 72, 69, 76, 79, 76]
for k in range(int(DUR / (BEAT / 4))):
    t = k * BEAT / 4
    if t >= 9.5: break
    c = chords[int(t) % 4]
    n = c[k % 3] + 12 + (12 if k % 8 == 6 else 0)
    bright = 900 if t < 2 else (2200 if t < 6 else 4200)
    if t >= 8.8: bright = 1500
    add(pluck(n, .25, bright), t, .22 if t >= 2 else .14, pan=.35 * np.sin(k), rev=.25)

# drums + bass 2.0 -> 8.8
k = 0; t = 2.0
while t < 8.8 - 1e-6:
    add(kick(), t, .9)
    add(hat(), t + BEAT / 2, .25, pan=.3)
    add(hat(.03), t + BEAT * .75, .12, pan=-.3)
    if k % 2 == 1: add(clap(), t, .35, rev=.3)
    r = roots[int(t) % 4]
    add(bass(r, BEAT * .45), t + BEAT / 2, .35)
    add(bass(r, BEAT * .2), t + BEAT * .75, .2)
    t += BEAT; k += 1
# build fill before finale
for i in range(8):
    add(hat(.04), 8.4 + i * .05, .2 + i * .03, pan=(-1) ** i * .4)

# per-cut whoosh + hit
for c in CUTS:
    add(whoosh(.45), c - .45, .4, rev=.2)
    add(impact(), c, .35 if c != 8.8 else .95, rev=.3)

# word reveals (scene 2) and grid pops (scene 3)
for i in range(13): add(tick(), 2.2 + i * .09, .18, pan=-.6 + i * .1)
for i in range(0, 40, 3): add(blip(84 + (i % 5) * 2, .06), 4.55 + i * .018, .06, pan=.5)
# loop scene: node pops + highlight blips
for i in range(4): add(blip(72 + [0, 3, 7, 12][i], .15), 6.1 + i * .18, .16, rev=.3)
for j in range(4): add(blip(88, .08), 6.8 + j / 2.2, .1, pan=.4, rev=.4)
# sim->real badges
add(blip(79, .15), 8.0, .16, rev=.3); add(blip(83, .15), 8.3, .16, rev=.3)
# finale: shimmer + URL pop
add(shimmer(1.2), 8.8, .35, rev=.7)
add(pad([45, 57, 64, 69, 72], 1.2), 8.8, .4, rev=.6)
add(blip(81, .25), 9.5, .25, rev=.5); add(blip(88, .25), 9.55, .15, rev=.5)

# ---------- sidechain pad bus ----------
sc = np.ones(N)
t = 2.0
while t < 8.8:
    i = int(t * SR); d = tt(BEAT); g = 1 - .75 * np.exp(-d / .09)
    sc[i:i + len(g)] = np.minimum(sc[i:i + len(g)], g[: N - i]); t += BEAT
MIX += PAD * sc

# ---------- reverb ----------
ir_t = tt(1.8)
for ch, seed in ((0, 1), (1, 2)):
    ir = np.random.default_rng(seed).standard_normal(len(ir_t)) * np.exp(-ir_t / .45)
    ir = filt(ir, 6000, 'low')
    wet = ss.fftconvolve(filt(REV, 200, 'high'), ir)[:N]
    MIX[ch] += wet / np.max(np.abs(ir)) * .02

# ---------- master ----------
MIX = filt(MIX, 25, 'high')
fade = np.ones(N); f0 = int(9.6 * SR); fade[f0:] = np.linspace(1, 0, N - f0) ** 1.5
MIX *= fade
MIX = np.tanh(MIX * 1.2)
MIX /= np.max(np.abs(MIX)) / .89
pcm = (MIX.T * 32767).astype(np.int16)
with wave.open('soundtrack.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', MIX.shape)
