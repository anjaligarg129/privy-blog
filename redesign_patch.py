# Round 3: Privy footer, no pop-ups, icon search, static hero pattern.
P='https://www.privy.io'
COLS=[('Product',[('User wallets','/wallets'),('Organization wallets','/organization-wallets'),('Treasury wallets','/treasury'),('Agent wallets','/agent-wallets'),('Custodial wallets','/wallets'),('Digital asset accounts','/accounts'),('Key managment','/keys'),('Policy engine','/keys'),('Security architecture','/security'),('On- and off- ramps','/integrations#onramp'),('Cards and spend','/integrations'),('Yield integrations','/integrations#yield'),('User onboarding','/user-wallets')]),
 ('Solutions',[('Banking','/fintech'),('Asset management','/fintech'),('Payments','/fintech'),('Neobanks','/fintech'),('Payroll','/fintech'),('Remittances','/fintech'),('Defi + trading','/defi'),('Exchanges','/defi'),('Prediction markets','/defi'),('Gaming','/gaming'),('Social platforms','/consumer'),('Marketplaces','/consumer'),('AI and agentic systems','/ai')]),
 ('Developer',[('Docs','https://docs.privy.io/'),('Demo','https://demo.privy.io/'),('Agent CLI','https://www.npmjs.com/package/@privy-io/agent-wallet-cli'),('GitHub','https://github.com/privy-io'),('Security handbook','/security#handbook'),('Trust center','https://trust.privy.io/'),('Support','/slack'),('Bug bounty','/vulnerability-disclosure')]),
 ('Resources',[('About','/careers'),('Careers','/careers'),('Blog','BLOG'),('Guides','/learn'),('Contact','/#contact'),('Customer love','/love'),('Privacy policy','/privacy-policy'),('Acceptable use policy','/acceptable-use-policy'),('User terms of service','/user-terms-of-service'),('Dev terms of service','/developer-terms-of-service')])]
SOC=[('Slack','/slack','slack'),('Farcaster','https://farcaster.xyz/privy','farcaster'),('X','https://x.com/privy_io','x'),('GitHub','https://github.com/privy-io','github')]
def footer(root,blog):
    href=lambda h:blog if h=='BLOG' else (h if h.startswith('http') else P+h)
    cols=''.join(f'<div class="pf-col"><h2 class="pf-title">{t}</h2><ul>'+''.join(f'<li><a href="{href(h)}">{n}</a></li>' for n,h in items)+'</ul></div>' for t,items in COLS)
    soc=''.join(f'<li><a aria-label="{n}" href="{href(h)}"><img src="{root}assets/brand/{f}.svg" alt="" width="20" height="20"></a></li>' for n,h,f in SOC)
    return (f'<footer class="pf"><div class="pf-inner"><div class="pf-cols">{cols}</div><div class="pf-brand">'
            f'<a aria-label="Privy home" href="{P}/"><svg class="pf-mark" viewBox="0 0 108 24" aria-hidden="true"><use href="#wordmark" width="219" height="24"/></svg></a>'
            f'<a class="pf-tag" href="{P}/blog/privy-manifesto">Technical decisions are moral decisions.</a>'
            f'<div class="pf-br"><ul class="pf-soc">{soc}</ul><p class="pf-copy">©2027 Horkos, Inc.</p></div></div></div></footer>\n'
            '<div class="note">Concept, not an official Privy page</div>\n')

def swap_footer(page,root,blog):
    i=page.index('<footer');j=page.index('<div class="note">',i);j=page.index('</div>',j)+6
    page=page[:i]+footer(root,blog)+page[j:]
    return page.replace('</head>',f'<link rel="stylesheet" href="{root}assets/footer.css">\n</head>',1)

ICONBTN='<button class="icon-btn" id="openSearch" type="button" aria-label="Search posts" aria-haspopup="dialog" aria-expanded="false" title="Search (/)"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></button>'
CSS='''
/* search trigger: Julian's round icon */
.wrow .icon-btn{flex:none;width:38px;height:38px;border-radius:50%;border:1px solid #e3e3e3;background:#fafafa;display:grid;place-items:center;cursor:pointer;color:#555;transition:background .2s,color .2s}
.wrow .icon-btn:hover{background:#f0f0f0;color:#111}
'''
def R(s,a,b,n=1):
    assert s.count(a)>=1,a[:80]; return s.replace(a,b,n)

def home(h):
    import re
    # search trigger -> icon
    h=re.sub(r'<button class="search" id="openSearch".*?</button>',ICONBTN,h,count=1,flags=re.S)
    h=R(h,'</style>',CSS+'</style>')
    # no pop-ups: cards are plain links
    h=re.sub(r"const openLink=\(el,p\)=>el\.addEventListener\('click',e=>\{.*?\}\);",'const openLink=()=>{};',h,count=1)
    h=re.sub(r"\n\s*el\.firstElementChild\.addEventListener\('click',e=>\{.*?openSheet\(p,e\);\}\);",'',h,count=1)
    h=R(h,'function go(p){close();if(p.local)location.href=p.url;else openSheet(p);}','function go(p){close();location.href=p.url;}')
    # hero pattern: static, no hover response
    h=R(h,'const intro=reduced?1e4:t*1100;','const intro=1e4;')
    h=R(h,'const wave=reduced?0:Math.sin(t*.9+n.x*.008+n.y*.013)*.5+.5;','const wave=Math.sin(n.x*.008+n.y*.013)*.5+.5;')
    h=re.sub(r"spot\.addEventListener\('pointermove'.*?\n",'',h,count=1)
    h=re.sub(r"spot\.addEventListener\('pointerleave'.*?\n",'',h,count=1)
    h=R(h,'    field.draw(now);\n','')
    h=R(h,'function onResize(){field.resize();}','function onResize(){field.resize();field.draw(performance.now());}')
    h=R(h,'renderBento();\nfield.resize();','renderBento();\nonResize();')
    h=R(h,'document.fonts.ready.then(()=>field.resize())','document.fonts.ready.then(onResize)')
    return swap_footer(h,'','index.html')
