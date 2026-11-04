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
    return h.replace('</style>',CSS+'</style>',1)
