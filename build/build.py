"""Builds the site: index.html (works injected) + one page per project in work/<slug>/.
Run from anywhere: python3 build/build.py"""
import json, os, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from works_meta import META

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://master-portfolio-navy-sigma.vercel.app'
GH = 'https://raw.githubusercontent.com/jeejjeH1/'
works = json.load(open(os.path.join(ROOT, 'build/works.json')))
for w in works:
    m = META[w['slug']]
    w['sum'] = m['sum']; w['beats'] = m['beats']; w['stack'] = m['stack']
    d = w.get('duration', 0); w['len'] = f"{d//60}:{d%60:02d}"

# ---------- index ----------
pub = [{k: w[k] for k in ('slug', 'title', 'brand', 'repo', 'branch', 'path', 'mb', 'len', 'sum')} for w in works]
tpl = open(os.path.join(ROOT, 'build/index.template.html')).read()
tpl = tpl.replace('/*@WORKS@*/[]', json.dumps(pub, ensure_ascii=False))
tpl = tpl.replace('<meta property="og:image" content="assets/banner-master.jpg">',
                  f'<meta property="og:image" content="{BASE}/assets/banner-master.jpg">\n<meta name="twitter:card" content="summary_large_image">\n<meta property="og:url" content="{BASE}/">')
open(os.path.join(ROOT, 'index.html'), 'w').write(tpl)

# ---------- project pages ----------
E = html.escape
PAGE = open(os.path.join(ROOT, 'build/project.template.html')).read()
n = len(works)
for i, w in enumerate(works):
    prv, nxt = works[(i - 1) % n], works[(i + 1) % n]
    src = GH + w['repo'] + '/' + w['branch'] + '/' + w['path']
    beats = '\n'.join(f'<li><span>{E(b)}</span></li>' for b in w['beats'])
    stack = ''.join(f'<span><b>{E(s)}</b></span>' for s in w['stack'])
    def card(x, label):
        return (f'<a class="pn" href="../{x["slug"]}/"><span class="mono">{label}</span>'
                f'<img src="../../assets/works/{x["slug"]}.jpg" alt="" loading="lazy" width="640" height="360">'
                f'<b>{E(x["title"])}</b><i class="mono">{E(x["brand"])}</i></a>')
    rep = {
        '@TITLE@': E(w['title']), '@BRAND@': E(w['brand']), '@SUM@': E(w['sum']), '@SLUG@': w['slug'],
        '@IDX@': f'{i+1:02d} / {n:02d}', '@LEN@': w['len'], '@RES@': w.get('res', '1920x1080').replace('x', '×'),
        '@SRC@': E(src), '@REPO@': E('https://github.com/jeejjeH1/' + w['repo']), '@REPONAME@': E('jeejjeH1/' + w['repo']),
        '@BEATS@': beats, '@STACK@': stack, '@PREV@': card(prv, '← Previous'), '@NEXT@': card(nxt, 'Next →'),
        '@OGIMG@': f'{BASE}/assets/works/{w["slug"]}.jpg', '@URL@': f'{BASE}/work/{w["slug"]}/',
    }
    page = PAGE
    for k, v in rep.items():
        page = page.replace(k, v)
    os.makedirs(os.path.join(ROOT, 'work', w['slug']), exist_ok=True)
    open(os.path.join(ROOT, 'work', w['slug'], 'index.html'), 'w').write(page)
print('built index +', n, 'project pages')
