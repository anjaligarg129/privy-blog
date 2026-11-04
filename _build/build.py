import json,re,os,base64,sys,html as H
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from datetime import datetime
ROOT=os.path.expanduser('~/mnt/privy')
b=json.load(open(f'{ROOT}/privy-bundle.json'))
S=b['sahith']['html']; posts=b['posts']
os.makedirs(f'{ROOT}/assets/img',exist_ok=True);os.makedirs(f'{ROOT}/assets/fonts',exist_ok=True);os.makedirs(f'{ROOT}/posts',exist_ok=True)
def w(p,s,mode='w'):
    with open(f'{ROOT}/{p}',mode) as f:f.write(s)
# images
for k,d in b['sahith']['imgs'].items(): w(f'assets/img/{k}.png',base64.b64decode(d.split(',',1)[1]),'wb')
# andrew css + fonts
css=b['andrew']['css']
for u,d in b['andrew']['assets'].items():
    name=u.split('/')[-1]; w(f'assets/fonts/{name}',base64.b64decode(d.split(',',1)[1]),'wb')
    css=css.replace(u,'fonts/'+name)
css+='\n@font-face{font-family:"FFF Acid Grotesk";font-weight:400;font-display:swap;src:url("https://framerusercontent.com/assets/0ZgmlAxvIMzrFV9lD3Z5ufkSgg.woff2") format("woff2")}\n'
w('assets/andrew.css',css)
FONTCLS='geist_a71539c9-module__T19VSG__variable inter_fe8b9d92-module__LINzvG__variable geist_mono_8d43a2aa-module__8Li5zG__variable'

# ---- sahith pieces
style=S[S.index('<style>')+7:S.index('</style>')]
def sect(a,bm): i=style.index(a); j=style.index(bm,i); return style[i:j]
head_css=style[:style.index('*{box-sizing')]   # font-face + :root
chrome=sect('/* nav:','/* shared post card')+sect('/* footer */','/* post sheet */')
chrome=chrome.replace('var(--','var(--s-').replace('var(--s-cols)','var(--cols)')
root=re.search(r':root\{(.*?)\n\}',head_css,re.S).group(1)
root=root.replace('--','--s-').replace('var(--s-s-','var(--s-')
root=re.sub(r'var\(--(?!s-)',"var(--s-",root)
chrome_css=head_css[:head_css.index(':root')]+':root{'+root+'}\n'+'''
.site-nav,.site-nav *,.site-foot,.site-foot *{box-sizing:border-box}
.site-nav button{color:inherit;background:none;border:0;padding:0;cursor:pointer}
.site-nav a,.site-foot a{color:inherit;text-decoration:none}
.site-nav img{display:block;max-width:100%}
.site-nav h6{font-family:inherit}
.arrow{display:inline-block;transition:transform .5s var(--s-ease)}a:hover>.arrow{transform:translateX(4px)}
body.post-page{padding-top:73px}
.site-foot{border-top:1px solid rgba(1,1,16,.08);font-family:var(--s-sans)}
.site-foot .fbot .big{font-family:var(--s-display)}
'''+chrome.replace('footer{','.site-foot{')
import round4_patch as _r4
w('assets/chrome.css',chrome_css+_r4.TLDR_CSS)

svgdefs=S[S.index('<svg width="0"'):S.index('</svg>',S.index('<symbol id="mark"'))+6]
header=S[S.index('<header class="nav"'):S.index('<main>')]
footer=S[S.index('<footer>'):S.index('<dialog')]
js=S[S.index('<script>')+8:S.index('</script>')]
navjs=js[js.index('const nav=$'):js.index('const io=')]
NAVJS="(function(){'use strict';const $=s=>document.querySelector(s);const IMG=document.currentScript.dataset.img;\n"+navjs+"})();"
w('assets/nav.js',NAVJS)

# ---- andrew posts: metadata
def ptitle(t): return t.replace(' | Privy Blog','').strip()
def norm(t): return re.sub(r'[^a-z0-9]','',t.lower().replace('’',"'"))
amap={}
for p in posts:
    h=p['html']
    t=re.search(r'articleTitle">(.*?)</h1>',h,re.S); title=H.unescape(re.sub('<[^>]+>','',t.group(1))) if t else ptitle(p['title'])
    dt=re.search(r'<time datetime="([^"]+)"',h); d=datetime.fromisoformat(dt.group(1).replace('Z','+00:00')) if dt else None
    cov=re.search(r'articleArt".*?<img[^>]*src="([^"]+)"',h,re.S)
    dek=re.search(r'articleDek">(.*?)</p>',h,re.S)
    p.update(t=title,date=(d.strftime('%b ')+str(d.day)+d.strftime(', %Y')) if d else '',ts=d.timestamp() if d else 0,cover=H.unescape(cov.group(1)) if cov else '',dek=H.unescape(re.sub('<[^>]+>','',dek.group(1))) if dek else p['desc'])
    amap[norm(title)]=p
import round4_patch
_S_rows=eval('['+js[js.index('const POSTS=[')+len('const POSTS=['):js.index('].map((p,i)=>')]+']')
for _p in round4_patch.extra_posts(posts,_S_rows,b['sahith']['imgs']):
    posts.append(_p); amap[norm(_p['t'])]=_p
# extra categories for posts Sahith lacks (from privy.io/blog)
XCAT={'building-for-AI-agents-that-spend':'mk','designing-a-capture-the-flag-challenge-in-the-era-of-ai-augmented-security':'an','reducing-trading-latency-on-privy':'pe','from-perps-to-prediction-markets-understanding-hip-4-and-hyperliquid-next-phase':'mk','privy-and-majority-bring-digital-asset-accounts-to-solana':'an','privy-at-stripe-sessions-building-for-stablecoins-and-agentic-commerce':'mk','building-crypto-neobanks-with-privy':'mk','building-on-megaeth-with-privy':'mk','security-in-an-agentic-world':'pe','privy-renews-soc-2-type-ii-compliance':'an','securely-equipping-openclaw-agents-with-privy-wallets':'pe','finding-react-vulnerabilities-as-part-of-our-security-work-at-privy':'pe','building-agentic-and-programmatic-payments-with-x402-and-privy':'pe'}

# ---- home page: rewrite POSTS
pstart=js.index('const POSTS=[')+len('const POSTS=[')
pend=js.index('].map((p,i)=>')
rows=eval('['+js[pstart:pend]+']')
used=set();out=[]
for r in rows:
    a=amap.get(norm(r[0]))
    if a: used.add(a['slug']); out.append([r[0],a['slug'],r[2],r[3],r[4],r[5],1])
    else: out.append(r+[0])
for p in posts:
    if p['slug'] in used: continue
    out.append([p['t'],p['slug'],p['cover'],XCAT.get(p['slug'],{'product':'pe','engineering':'pe','customers':'cs','perspectives':'mk'}[p['cat']]),p['date'],p['dek'],1])
def ts(r):
    try: return datetime.strptime(r[4],'%b %d, %Y').timestamp()
    except: return 0
first=out[0]; rest=sorted(out[1:],key=ts,reverse=True)  # keep Sahith's pinned first row
out=[first]+rest
newposts=json.dumps(out,ensure_ascii=False)[1:-1]
newmap="].map((p,i)=>({i,title:p[0],local:!!p[6],url:p[6]?'posts/'+p[1]+'.html':'https://www.privy.io/blog/'+p[1],img:p[2].startsWith('http')?p[2]:IMG+p[2]+'.png',cat:p[3],date:p[4],text:p[5]}));"
js2=js[:pstart]+newposts+newmap+js[js.index('\n',pend):]
# local posts: navigate instead of opening the sheet
js2=js2.replace("const openLink=(el,p)=>el.addEventListener('click',e=>{if(e.metaKey||e.ctrlKey)return;","const openLink=(el,p)=>el.addEventListener('click',e=>{if(e.metaKey||e.ctrlKey||p.local)return;")
js2=js2.replace("el.firstElementChild.addEventListener('click',e=>{if(e.metaKey||e.ctrlKey)return;","el.firstElementChild.addEventListener('click',e=>{if(e.metaKey||e.ctrlKey||p.local)return;")
assert js2.count('p.local)return')==2
js2=js2.replace("p.url.endsWith(","p.url.replace(/\\.html$/,'').endsWith(")
home=S[:S.index('<script>')+8]+js2+S[S.index('</script>'):]
home=home.replace('Student concept by Sahith &amp; Julian.','Student concept: home page by Sahith &amp; Julian, article pages by Andrew.')
import sys;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import search_patch,redesign_patch;import round5_patch,round6_patch;home=round6_patch.home(round5_patch.home(round4_patch.home(redesign_patch.home(search_patch.apply(home)),out,posts)))
w('index.html',home)

# ---- post pages
AO='https://privy-blog.andrewliu.org'
slugs={p['slug'] for p in posts}
for p in posts:
    h=p['html']
    h=re.sub(r'__POST__([^"#?]+)',lambda m:(m.group(1)+'.html') if m.group(1) in slugs else 'https://www.privy.io/blog/'+m.group(1),h)
    h=re.sub(r'href="'+re.escape(AO)+r'/blog(/[a-z]+)?/?"','href="../index.html#wall"',h)
    h=h.replace('data-fade="true"','')
    page=f'''<!doctype html>
<html lang="en" class="{FONTCLS}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{H.escape(p['title'])}</title>
<meta name="description" content="{H.escape(p['desc'])}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='10' r='9' fill='%23010110'/%3E%3Cellipse cx='12' cy='22.5' rx='6' ry='1.5' fill='%23010110'/%3E%3C/svg%3E">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/andrew.css">
<link rel="stylesheet" href="../assets/chrome.css">
</head>
<body class="post-page">
{svgdefs}
{header.replace('<header class="nav"','<header class="nav site-nav"').replace('href="https://www.privy.io/" aria-label','href="../index.html" aria-label')}
<main id="main">
{h}
</main>
{footer.replace('<footer>','<footer class="site-foot">').replace('Student concept by Sahith &amp; Julian.','Student concept: home page by Sahith &amp; Julian, article pages by Andrew.')}
<script src="../assets/nav.js" data-img="../assets/img/"></script>
<script src="../assets/andrew.js"></script>
</body>
</html>'''
    page=redesign_patch.swap_footer(page,'../','../index.html')
    w(f"posts/{p['slug']}.html",page)
print('home posts',len(out),'local',sum(r[6] for r in out),'pages',len(posts))

# ---- cache-busting: version every local CSS/JS reference by content hash
import hashlib,glob
def _ver(rel):
    return hashlib.md5(open(f'{ROOT}/assets/{rel}','rb').read()).hexdigest()[:8]
_files=['andrew.css','chrome.css','footer.css','nav.js','andrew.js']
_v={f:_ver(f) for f in _files}
for _p in [f'{ROOT}/index.html']+glob.glob(f'{ROOT}/posts/*.html'):
    _h=open(_p).read()
    for f in _files:
        _h=re.sub(r'(assets/'+re.escape(f)+r')(\?v=[0-9a-f]+)?"',r'\1?v='+_v[f]+'"',_h)
    open(_p,'w').write(_h)
print('versioned',_v)
