# Round 5: search icon sits in the category-chip row; the bar opens in place over that row.
CSS='''
/* search lives on the chip row */
.crow{position:relative;display:flex;align-items:center;gap:12px;margin:18px 0 24px}
.crow .chips{flex:1;min-width:0;margin:0}
.crow .icon-btn{flex:none;width:34px;height:34px;border-radius:50%;border:1px solid var(--line);background:#fff;display:grid;place-items:center;color:var(--muted);cursor:pointer;transition:color .2s,border-color .2s}
.crow .icon-btn:hover{color:var(--ink);border-color:rgba(1,1,16,.26)}
.crow .icon-btn svg{width:15px;height:15px}
.crow .overlay{top:-11px;border-radius:28px;border-color:rgba(117,109,255,.16);box-shadow:0 10px 34px rgba(117,109,255,.09),0 1px 3px rgba(117,109,255,.04)}
.crow .o-row{height:56px;padding:0 24px;gap:14px}
.crow .o-row svg{width:20px;height:20px}
.crow .o-row input{font-size:16px}
.crow .o-body{border-top-color:rgba(117,109,255,.08);padding:6px 10px 10px}
.crow .result{border-radius:18px;padding:12px 14px}
.crow .result:hover,.crow .result.sel{background:rgba(117,109,255,.05);box-shadow:none}
.crow .result mark{background:rgba(117,109,255,.12)}
body.searching .dim{background:rgba(1,1,16,.16)}
/* search results as cards */
.crow .rgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;padding:8px 4px 4px}
.crow .result.rcard{display:flex;flex-direction:column;align-items:stretch;gap:0;padding:0;border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff;font-size:inherit;transition:border-color .2s,box-shadow .2s}
.crow .result.rcard:hover,.crow .result.rcard.sel{background:#fff;border-color:rgba(117,109,255,.32);box-shadow:0 6px 20px rgba(117,109,255,.08)}
.rthumb{position:relative;aspect-ratio:2.4;background:var(--wash);overflow:hidden}
.rthumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .8s var(--ease)}
.rcard:hover .rthumb img,.rcard.sel .rthumb img{transform:scale(1.04)}
.rbody{display:flex;flex-direction:column;gap:6px;padding:12px 14px 14px}
.rcat{font-size:10.5px;font-weight:500;letter-spacing:.07em;text-transform:uppercase;color:var(--muted)}
.rtitle{font:400 16px/1.25 var(--display);letter-spacing:-.015em;color:var(--ink);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.rdate{font-size:12px;color:var(--muted)}
@media(max-width:900px){.crow .rgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.crow .rgrid{grid-template-columns:1fr}}
/* changelog: no timeline line, dots or month tags */
.clog .tick{padding-top:0}
.clog .tick::before,.clog .tick::after,.clog .tick .mtag{display:none}
'''
def home(h):
    b0=h.index('<button class="icon-btn" id="openSearch"'); b1=h.index('</button>',b0)+9
    btn=h[b0:b1]; h=h[:b0]+h[b1:]
    o0=h.index('<div class="overlay" id="overlay"'); end='<div id="results" role="listbox"></div></div></div>'
    o1=h.index(end,o0)+len(end); ov=h[o0:o1]; h=h[:o0]+h[o1:]
    chips='<div class="chips" id="chips" role="group" aria-label="Filter by category"></div>'
    assert chips in h
    h=h.replace(chips,f'<div class="crow">{chips}{btn}{ov}</div>',1)
    old="SC.on=false;scrollTo(0,$('#wall').offsetTop);SC.y=SC.t=scrollY;"
    assert old in h
    h=h.replace(old,"SC.on=false;{const r=ov.parentElement.getBoundingClientRect();if(r.top<20||r.bottom>innerHeight-240)scrollTo(0,scrollY+r.top-innerHeight*.25);}SC.y=SC.t=scrollY;")
    # spotlight: two-finger horizontal swipe on a trackpad moves between slides
    old="  addEventListener('resize',()=>show(i));\n  show(0);"
    assert old in h
    h=h.replace(old,'''  let acc=0,lockUntil=0,quiet;
  sec.addEventListener('wheel',e=>{
    if(Math.abs(e.deltaX)<=Math.abs(e.deltaY))return;
    e.preventDefault();e.stopPropagation();
    clearTimeout(quiet);quiet=setTimeout(()=>{acc=0;lockUntil=0;},180);
    const now=performance.now();if(now<lockUntil)return;
    acc+=e.deltaX;if(Math.abs(acc)>40){show(i+(acc>0?1:-1));acc=0;lockUntil=now+650;}
  },{passive:false});
  addEventListener('resize',()=>show(i));
  show(0);''')
    old="const hz=e.target.closest&&e.target.closest('.rail,.chips');"
    assert old in h
    h=h.replace(old,"const hz=e.target.closest&&e.target.closest('.rail,.chips,.spot');")
    return h.replace('</style>',CSS+'</style>',1)
