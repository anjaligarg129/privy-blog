# Round 4: 6 privy.io-only posts rebuilt in Andrew's format, TL;DR callout,
# Ramp-style spotlight carousel, scrollable changelog with month jump.
import json,re,html as H,os
from datetime import datetime
from urllib.parse import quote
ROOT=os.path.expanduser('~/mnt/privy')
CAT={'pe':'Product and Engineering','cs':'Case Studies','an':'Announcement','mk':'Market','st':'Inside the stack','tu':'Team updates'}
AO='https://privy-blog.andrewliu.org'

def slugify(t): return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')

# ---------- 6 extra posts in Andrew's article markup ----------
TEMPLATE={'Case Studies':('building-enterprise-payroll-with-zebec','customers','Customers'),
          'Announcement':('building-enterprise-payroll-with-zebec','customers','Customers'),
          'Product and Engineering':('fiat-deposits-payouts-kyc-orchestration','product','Product')}
OVERRIDE_CRUMB={'building-payments-and-agentic-commerce-with-the-xrp-ledger':('product','Product')}
def avatar_for(posts,name):
    for p in posts:
        m=re.search(r'<img[^>]*?src="([^"]+)"[^>]*>\s*<span class="blog-module__R2lbeq__articleAuthor">'+re.escape(name)+'<',p['html'])
        if m: return m.group(1)
    return ''

def extra_posts(posts,sahith_rows,sahith_imgs):
    b2=json.load(open(f'{ROOT}/privy-bundle-2.json'))
    rows={r[1]:r for r in sahith_rows}
    bys={p['slug']:p for p in posts}
    out=[]
    for e in b2['posts']:
        tslug,cat,crumb=TEMPLATE[e['cat']]
        cat,crumb=OVERRIDE_CRUMB.get(e['slug'],(cat,crumb))
        t=bys[tslug]['html']; r=rows[e['slug']]
        d=datetime.strptime(r[4],'%b %d, %Y')
        body=re.sub(r'^\s*<p>[A-Z][a-z]{2} \d{1,2}, \d{4}</p>','',e['body'])
        toc=[]
        def addid(m):
            txt=re.sub('<[^>]+>','',m.group(1)); i=slugify(H.unescape(txt)); toc.append((i,txt)); return f'<h2 id="{i}">{m.group(1)}</h2>'
        body=re.sub(r'<h2>(.*?)</h2>',addid,body,flags=re.S)
        words=len(re.sub('<[^>]+>',' ',body).split()); mins=max(1,round(words/230))
        key=re.search(r'/images/([A-Za-z0-9]+)\.',e['cover'] or '')
        cover=f'../assets/img/{key.group(1)}.png' if key and key.group(1) in sahith_imgs else (e['cover'] or '')
        h=t
        h=re.sub(r'(articleTitle">).*?(</h1>)',lambda m:m.group(1)+H.escape(e['title'])+m.group(2),h,count=1,flags=re.S)
        h=re.sub(r'(articleDek">).*?(</p>)',lambda m:m.group(1)+H.escape(r[5])+m.group(2),h,count=1,flags=re.S)
        av=avatar_for(posts,e['author'])
        h=re.sub(r'(<img[^>]*?avatar"[^>]*?src=")[^"]*(")',lambda m:m.group(1)+av+m.group(2),h,count=1)
        h=re.sub(r'(<img[^>]*?src=")[^"]*("[^>]*>\s*<span class="blog-module__R2lbeq__articleAuthor">)',lambda m:m.group(1)+av+m.group(2),h,count=1) if av else h
        h=re.sub(r'(articleAuthor">)[^<]*(<)',lambda m:m.group(1)+e['author']+m.group(2),h,count=1)
        h=re.sub(r'<time datetime="[^"]*">[^<]*</time>',f'<time datetime="{d.strftime("%Y-%m-%d")}T00:00:00.000Z">{d.strftime("%B")} {d.day}, {d.year}</time>',h,count=1)
        h=re.sub(r'(articleReadTime"> · <!-- -->)\d+',lambda m:m.group(1)+str(mins),h,count=1)
        h=re.sub(r'(articleArt") style="[^"]*"',r'\1',h,count=1)
        h=re.sub(r'(articleArt"[^>]*>\s*<img[^>]*?src=")[^"]*(")',lambda m:m.group(1)+cover+m.group(2),h,count=1)
        h=re.sub(r'<p class="blog-module__R2lbeq__tldr">.*?</p>','',h,count=1,flags=re.S)
        i=re.search(r'<div class="blog-module__R2lbeq__prose"[^>]*>',h).end(); j=h.index('<aside class="blog-module__R2lbeq__share"',i)
        assert h[j-6:j]=='</div>'
        h=h[:i]+body+h[j-6:]
        h=re.sub(r'(<ol class="blog-module__R2lbeq__tocList">).*?(</ol>)',lambda m:m.group(1)+''.join(f'<li><a href="#{a}">{b}</a></li>' for a,b in toc)+m.group(2),h,flags=re.S)
        h=re.sub(r'(crumbType" href=")[^"]*(">)[^<]*',lambda m:m.group(1)+f'{AO}/blog/{cat}'+m.group(2)+crumb,h,count=1)
        h=h.replace(quote(f'{AO}/blog/'+bys[tslug]['cat']+'/'+tslug,safe=''),quote('https://www.privy.io/blog/'+e['slug'],safe=''))
        out.append({'href':f'/blog/{cat}/'+e['slug'],'slug':e['slug'],'cat':cat,'title':e['title']+' | Privy Blog','desc':r[5],'html':h,'t':e['title'],'date':r[4],'ts':d.timestamp(),'cover':cover,'dek':r[5]})
    return out

# ---------- post pages: TL;DR callout ----------
TLDR_CSS='''
/* TL;DR as a callout */
.blog-module__R2lbeq__tldr{position:relative;margin:0 0 40px;padding:2px 0 2px 22px;border-left:3px solid #756dff;font-size:19px;line-height:1.6;font-style:italic;color:#4a4a57}
.blog-module__R2lbeq__tldr strong{display:block;margin-bottom:4px;font-style:normal;font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:#5954b8}
'''

# ---------- home: spotlight + changelog ----------
SPOT_SLUGS=['privy-treasury-management-for-onchain-capital','inside-the-stack-how-deel-is-turning-payroll-into-a-financial-account','launch-a-global-stablecoin-card-program','introducing-organization-wallets','stablecoin-orchestration-guide']
CSS='''
/* spotlight carousel (after ramp.com/blog) */
.spot{padding:clamp(56px,7vw,96px) 0 clamp(40px,5vw,64px);overflow:hidden}
.spot .head{width:var(--content);margin:0 auto clamp(24px,3vw,36px)}
.sptrack{display:flex;gap:24px;padding-left:calc((100% - var(--content))/2);transition:transform .9s var(--ease);will-change:transform}
.spcard{flex:none;width:var(--content);display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:clamp(16px,2vw,28px);padding:12px;border-radius:16px;background:#f4f4f7;color:var(--ink);opacity:.35;transition:opacity .7s ease}
.spcard.on{opacity:1}
.spcard:not(.on){cursor:pointer}
.sptext{display:flex;flex-direction:column;justify-content:center;padding:clamp(20px,3.4vw,52px)}
.sptext .eyebrow{color:var(--muted)}
.sptext h3{font-size:clamp(26px,2.6vw,38px);line-height:1.12;letter-spacing:-.03em;margin:16px 0 26px;transition:color .2s}
.spcard.on:hover h3{color:var(--deep)}
.spby{display:flex;align-items:center;gap:12px;font-size:14px;line-height:1.35}
.spby img{width:40px;height:40px;border-radius:50%;object-fit:cover;background:var(--wash)}
.spby b{display:block;font-weight:500}
.spby span{color:var(--muted)}
.spimg{position:relative;border-radius:10px;overflow:hidden;aspect-ratio:1.6;background:var(--wash)}
.spimg img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}
.spcard.on:hover .spimg img{transform:scale(1.03)}
.spfoot{width:var(--content);margin:22px auto 0;display:flex;align-items:center;gap:24px}
.spbars{flex:1;display:flex;gap:16px}
.spbar{flex:1;height:22px;display:flex;align-items:center;cursor:pointer}
.spbar i{position:relative;display:block;width:100%;height:2px;background:rgba(1,1,16,.12);overflow:hidden;border-radius:2px}
.spbar i::after{content:"";position:absolute;inset:0;background:var(--ink);transform:scaleX(0);transform-origin:left}
.spbar.done i::after{transform:none}
.spbar.on i::after{animation:spfill var(--spdur,7s) linear forwards}
.spot:hover .spbar.on i::after,.spot:focus-within .spbar.on i::after,.spot.paused .spbar.on i::after{animation-play-state:paused}
@keyframes spfill{to{transform:none}}
.rbtn{flex:none;width:40px;height:40px;border-radius:50%;background:#f4f4f7;display:grid;place-items:center;font-size:16px;transition:background .2s}
.rbtn:hover{background:#e9e9ef}
.rbtns{display:flex;gap:8px}
@media(max-width:820px){.spcard{grid-template-columns:1fr}.spimg{order:-1}.sptext{padding:20px 12px 16px}.spbars{gap:8px}}

/* changelog: full timeline, scrolls sideways, jump by month */
.clog .head{margin-bottom:20px}
.months{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding:2px;margin-bottom:6px}
.months::-webkit-scrollbar{display:none}
.months .chip span{font-size:11px;opacity:.55}
.rail{grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:minmax(258px,calc((100% - 42px)/4));scroll-behavior:smooth;margin-top:26px}
.rail.drag{scroll-behavior:auto}
.tick .mtag{position:absolute;left:18px;top:-3px;font-size:11px;font-weight:500;letter-spacing:.09em;text-transform:uppercase;color:var(--ink);background:#fff;padding:0 8px 0 0;opacity:0;transition:opacity .6s ease}
.rail.in .tick .mtag{opacity:1}
a.log{display:block;color:inherit;transition:background .25s}
a.log:hover{background:linear-gradient(to bottom,#ebecff,rgba(235,236,255,0))}
a.log:hover h3{color:var(--deep)}
.log p{display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.log .go{display:inline-block;margin-top:12px;font-size:13px;font-weight:500;color:var(--ink)}
'''
def spotlight_html(rows,posts):
    rb={r[1]:r for r in rows}; pb={p['slug']:p for p in posts}; cards=[]
    for n,s in enumerate(SPOT_SLUGS):
        r=rb[s]; p=pb[s]; ph=p['html']
        au=re.search(r'articleAuthor">([^<]+)<',ph); av=re.search(r'<img[^>]*?src="([^"]+)"[^>]*>\s*<span class="blog-module__R2lbeq__articleAuthor">',ph)
        rt=re.search(r'articleReadTime"> · <!-- -->(\d+)',ph)
        img=r[2] if r[2].startswith('http') else f'assets/img/{r[2]}.png'
        cards.append(f'<a class="spcard{" on" if n==0 else ""}" href="posts/{s}.html" role="group" aria-roledescription="slide" aria-label="{n+1} of {len(SPOT_SLUGS)}" data-i="{n}"'+('' if n==0 else ' tabindex="-1" aria-hidden="true"')+'>'
          f'<div class="sptext"><div class="eyebrow">{H.escape(CAT[r[3]])} · {rt.group(1) if rt else 3} min read</div><h3>{H.escape(r[0])}</h3>'
          f'<div class="spby">'+(f'<img src="{av.group(1)}" alt="" loading="lazy">' if av else '')+f'<div><b>{H.escape(au.group(1) if au else "Privy")}</b><span>{r[4]}</span></div></div></div>'
          f'<div class="spimg"><img src="{img}" alt="" loading="lazy"></div></a>')
    bars=''.join(f'<button class="spbar{" on" if n==0 else ""}" type="button" role="tab" aria-label="Go to slide {n+1}" aria-selected="{"true" if n==0 else "false"}" data-i="{n}"><i></i></button>' for n in range(len(SPOT_SLUGS)))
    return ('<section class="spot" id="spotlight" aria-roledescription="carousel" aria-label="Spotlight">'
      '<div class="head reveal"><h2><em>In the</em> spotlight</h2></div>'
      f'<div class="sptrack" id="spTrack">{"".join(cards)}</div>'
      f'<div class="spfoot"><div class="spbars" role="tablist" aria-label="Spotlight slides">{bars}</div>'
      '</div></section>\n')

def changelog_html():
    clog=json.load(open(f'{ROOT}/privy-bundle-2.json'))['clog']
    items=[];months=[]
    for date,title,text,href in clog:
        d=datetime.strptime(date.title(),'%b %d, %Y'); m=d.strftime('%Y-%m')
        if not months or months[-1][0]!=m: months.append([m,d.strftime('%b %Y'),d.strftime('%B %Y'),0])
        months[-1][3]+=1; items.append((d,m,title,text,href))
    chips=''.join(f'<button class="chip" type="button" data-m="{m}" aria-pressed="{"true" if k==0 else "false"}">{s} <span>{c}</span></button>' for k,(m,s,l,c) in enumerate(months))
    seen=set();ticks=[]
    for k,(d,m,title,text,href) in enumerate(items):
        tag=''
        if m not in seen: seen.add(m); tag=f'<span class="mtag">{d.strftime("%B %Y")}</span>'
        delay=f' style="--d:{k*180}ms"' if k<4 else ''
        ticks.append(f'<article class="tick" data-m="{m}"{delay}>{tag}<a class="log" href="{H.escape(href or "https://docs.privy.io/")}" target="_blank" rel="noopener"><small>{d.strftime("%b").upper()} {d.day}, {d.year}</small><h3>{H.escape(title)}</h3><p>{H.escape(text)}</p><span class="go">Read the docs <span class="arrow">↗</span></span></a></article>')
    return ('<div class="sec clog" style="padding-top:0">\n'
      '  <div class="head reveal"><h2>Changelog</h2></div>\n'
      f'  <div class="months" id="months" role="group" aria-label="Jump to month">{chips}</div>\n'
      f'  <div class="rail" id="rail" tabindex="0" aria-label="Changelog, newest first">{"".join(ticks)}</div>\n</div>\n')

JS=r'''
/* ---------- spotlight carousel ---------- */
(function(){
  const sec=$('#spotlight'),track=$('#spTrack'),cards=[...track.children],bars=[...sec.querySelectorAll('.spbar')];
  let i=0;const n=cards.length;
  if(reduced)sec.classList.add('paused');
  function show(k){
    i=(k+n)%n;
    const w=cards[0].offsetWidth+parseFloat(getComputedStyle(track).columnGap||24);
    track.style.transform=`translateX(${-i*w}px)`;
    cards.forEach((c,j)=>{const on=j===i;c.classList.toggle('on',on);c.setAttribute('aria-hidden',!on);c.tabIndex=on?0:-1;});
    bars.forEach((b,j)=>{b.classList.remove('on');b.classList.toggle('done',j<i);b.setAttribute('aria-selected',j===i);});
    void bars[i].offsetWidth;bars[i].classList.add('on');
  }
  bars.forEach(b=>{b.onclick=()=>show(+b.dataset.i);b.querySelector('i').addEventListener('animationend',()=>{if(b.classList.contains('on'))show(i+1);});});
  cards.forEach(c=>c.addEventListener('click',e=>{if(!c.classList.contains('on')){e.preventDefault();show(+c.dataset.i);}}));
  sec.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){show(i+1);}if(e.key==='ArrowLeft'){show(i-1);}});
  let sx=null;track.addEventListener('pointerdown',e=>{sx=e.clientX;});
  addEventListener('pointerup',e=>{if(sx===null)return;const dx=e.clientX-sx;sx=null;if(Math.abs(dx)>60)show(i+(dx<0?1:-1));});
  addEventListener('resize',()=>show(i));
  show(0);
})();

/* ---------- changelog: month jump + live month ---------- */
(function(){
  const rail=$('#rail'),months=$('#months'),chips=[...months.querySelectorAll('.chip')],ticks=[...rail.querySelectorAll('.tick')];
  const first={};ticks.forEach(t=>{if(!(t.dataset.m in first))first[t.dataset.m]=t;});
  let cur='';
  function mark(m){if(m===cur)return;cur=m;chips.forEach(c=>{const on=c.dataset.m===m;c.setAttribute('aria-pressed',on);if(on)months.scrollTo({left:c.offsetLeft-months.clientWidth/2+c.offsetWidth/2,behavior:'smooth'});});}
  function sync(){const x=rail.scrollLeft+8;let m=ticks[0].dataset.m;for(const t of ticks){if(t.offsetLeft<=x)m=t.dataset.m;else break;}
    if(rail.scrollLeft+rail.clientWidth>=rail.scrollWidth-4)m=ticks[ticks.length-1].dataset.m;mark(m);}
  let st;rail.addEventListener('scroll',()=>{cancelAnimationFrame(st);st=requestAnimationFrame(sync);},{passive:true});
  chips.forEach(c=>c.onclick=()=>{rail.scrollTo({left:first[c.dataset.m].offsetLeft});mark(c.dataset.m);});
  rail.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();rail.scrollBy({left:280});}if(e.key==='ArrowLeft'){e.preventDefault();rail.scrollBy({left:-280});}});
  let dx0=null,moved=false;rail.addEventListener('pointerdown',e=>{dx0=e.clientX;moved=false;});
  rail.addEventListener('pointermove',e=>{if(dx0!==null&&Math.abs(e.clientX-dx0)>6)moved=true;});
  rail.addEventListener('click',e=>{if(moved){e.preventDefault();moved=false;}},true);
  sync();
})();
'''
def home(h,rows,posts):
    i=h.index('<div class="sec clog"');j=h.index('<section class="cta"',i)
    h=h[:i]+spotlight_html(rows,posts)+changelog_html()+'\n'+h[j:]
    h=h.replace('</style>',CSS+'</style>',1)
    h=h.replace('/* ---------- loop ---------- */',JS+'\n/* ---------- loop ---------- */',1)
    return h
