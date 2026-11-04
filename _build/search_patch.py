# Julian's pop-up search, applied to the home page. Imported by build.py.
OLD_LABEL='<label class="search"><span aria-hidden="true">⌕</span><span class="sr">Search posts</span><input id="q" type="search" placeholder="Search posts" autocomplete="off"></label>'
ICON='<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">{p}</svg>'
LENS='<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>'
NEW_LABEL=('<button class="search" id="openSearch" type="button" aria-label="Search posts" aria-haspopup="dialog" aria-expanded="false" title="Search (/)"><span aria-hidden="true">⌕</span><span class="sph">Search posts</span></button>'
 '<div class="overlay" id="overlay" role="dialog" aria-modal="true" aria-label="Search posts">'
 '<div class="o-head"><div class="o-row">'+ICON.format(s=24,p=LENS)+
 '<input id="sq" type="text" placeholder="Search anything" autocomplete="off" aria-controls="results" aria-label="Search posts">'
 '</div></div><div class="o-body"><div id="results" role="listbox"></div></div></div>')
CSS='''
/* pop-up search (from Julian's privy-blog-search) */
html{scrollbar-gutter:stable}
.wrow{position:relative}
button.search{cursor:text;text-align:left}
button.search .sph{color:#757575;font-size:14px}
.overlay{position:absolute;top:0;left:0;right:0;max-height:min(560px,calc(100vh - 160px));background:#fff;border:1px solid rgba(117,109,255,.28);border-radius:20px;box-shadow:0 14px 44px rgba(117,109,255,.18),0 2px 6px rgba(117,109,255,.06);overflow:hidden;z-index:61;display:flex;flex-direction:column;opacity:0;visibility:hidden;transform:translateY(-8px);transition:opacity .18s,transform .18s,visibility .18s;text-align:left}
.overlay.open{opacity:1;visibility:visible;transform:none;transition:opacity .18s,transform .18s,visibility 0s}
.dim{position:fixed;inset:0;background:rgba(1,1,16,.28);z-index:60;opacity:0;visibility:hidden;transition:opacity .18s,visibility .18s}
body.searching{overflow:hidden}
body.searching .dim{opacity:1;visibility:visible}
.o-row{display:flex;align-items:center;gap:18px;height:84px;padding:0 40px;color:#010110}
.o-row svg{flex:none}
.o-row input{flex:1;border:0;outline:0;font:400 19px var(--sans);color:#010110;background:none;min-width:0}
.o-row input::placeholder{color:#7a7a86}
.o-body{display:none;overflow-y:auto;min-height:0;padding:6px 24px 12px;border-top:1px solid rgba(117,109,255,.14);overscroll-behavior:contain}
.overlay.has-q .o-body{display:block}
.result{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:14px 16px;border-radius:12px;cursor:pointer;font-size:16px;color:#010110;transition:background .12s}
.result:hover,.result.sel{background:#f1f0ff}
.result.sel{box-shadow:inset 3px 0 0 #756dff}
.result small{font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:#8a8a96;white-space:nowrap}
.result mark{background:rgba(117,109,255,.18);color:inherit;border-radius:3px;padding:0 1px}
.empty{color:#7a7a86;font-size:15px;padding:14px 16px}
@media(max-width:760px){.o-row{padding:0 20px;height:68px}.o-row input{font-size:17px}.o-body{padding-left:12px;padding-right:12px}}
'''
JS=r'''
/* ---------- pop-up search (from Julian's privy-blog-search) ---------- */
(function(){
  const ov=$('#overlay'),sq=$('#sq'),res=$('#results'),btn=$('#openSearch');
  let sel=0,hits=[];
  const isOpen=()=>ov.classList.contains('open');
  const hesc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function render(){
    const q=sq.value.trim().toLowerCase();
    ov.classList.toggle('has-q',!!q);
    hits=q?POSTS.filter(p=>(p.title+' '+p.text+' '+CAT[p.cat]).toLowerCase().includes(q)):[];
    sel=Math.min(sel,Math.max(hits.length-1,0));
    const re=q?new RegExp(hesc(q).replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi'):null;
    const hl=t=>re?hesc(t).replace(re,m=>`<mark>${m}</mark>`):hesc(t);
    res.innerHTML=hits.length?`<div class="rgrid">`+hits.map((p,k)=>`<div class="result rcard${k===sel?' sel':''}" role="option" aria-selected="${k===sel}" data-k="${k}"><div class="rthumb"><img src="${p.img}" alt="" loading="lazy"></div><div class="rbody"><span class="rcat">${hesc(CAT[p.cat])}</span><span class="rtitle">${hl(p.title)}</span><span class="rdate">${p.date}</span></div></div>`).join('')+`</div>`:(q?`<div class="empty">No posts match “${hesc(q)}”.</div>`:'');
    const s=res.querySelector('.sel');if(s)s.scrollIntoView({block:'nearest'});
  }
  function open(){
    SC.on=false;scrollTo(0,$('#wall').offsetTop);SC.y=SC.t=scrollY;
    ov.classList.add('open');document.body.classList.add('searching');btn.setAttribute('aria-expanded','true');
    sq.value='';sel=0;render();sq.focus({preventScroll:true});setTimeout(()=>{if(document.activeElement!==sq)sq.focus({preventScroll:true});},60);
  }
  function close(){ov.classList.remove('open');document.body.classList.remove('searching');btn.setAttribute('aria-expanded','false');}
  function go(p){close();if(p.local)location.href=p.url;else openSheet(p);}
  btn.addEventListener('click',e=>{e.stopPropagation();open();});
  sq.oninput=()=>{sel=0;render();};
  res.onclick=e=>{const r=e.target.closest('.result');if(r)go(hits[+r.dataset.k]);};
  document.addEventListener('click',e=>{if(isOpen()&&!ov.contains(e.target)&&!btn.contains(e.target))close();});
  document.addEventListener('keydown',e=>{
    const o=isOpen(),typing=/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName);
    if(!o&&!sheet.open&&((e.key==='/'&&!typing)||(e.key==='k'&&(e.metaKey||e.ctrlKey)))){e.preventDefault();open();return;}
    if(!o)return;
    if(e.key==='Escape'){close();btn.focus();}
    if(/^Arrow(Down|Up|Left|Right)$/.test(e.key)&&hits.length){const cols=Math.max(1,Math.round(res.clientWidth/(res.querySelector('.rcard')?.offsetWidth||res.clientWidth)));const d={ArrowDown:cols,ArrowUp:-cols,ArrowRight:1,ArrowLeft:-1}[e.key];if((e.key==='ArrowLeft'||e.key==='ArrowRight')&&sq.value&&document.activeElement===sq&&cols===1)return;e.preventDefault();sel=Math.min(hits.length-1,Math.max(0,sel+d));render();}
    if(e.key==='Enter'&&hits[sel]){e.preventDefault();go(hits[sel]);}
  });
})();
'''
def apply(home):
    assert OLD_LABEL in home; home=home.replace(OLD_LABEL,NEW_LABEL)
    home=home.replace('</style>',CSS+'</style>',1)
    home=home.replace('<dialog class="sheet"','<div class="dim" aria-hidden="true"></div>\n<dialog class="sheet"',1)
    old="qInput.addEventListener('input',e=>{F.q=e.target.value.trim().toLowerCase();F.limit=PAGE;updateBento();});"
    assert old in home; home=home.replace(old,'')
    home=home.replace(",qInput=$('#q')","")
    old="if(e.ctrlKey||sheet.open)return;"
    assert old in home; home=home.replace(old,"if(e.ctrlKey||sheet.open||document.body.classList.contains('searching'))return;")
    home=home.replace('/* ---------- loop ---------- */',JS+'\n/* ---------- loop ---------- */',1)
    return home
