# Round 6: Privy-style dithered grid bands around the "All posts" section (replaces the cross field),
# taller category chips (search bar matches), no counts on changelog month chips.
import os,random
ROOT=os.path.expanduser('~/mnt/privy')
BAYER=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
def band_svg(flip=False,cols=48,rows=7,pitch=10,sq=6):
    rnd=random.Random(7);rects=[]
    for r in range(rows):
        dens=1-(r+.5)/rows
        for c in range(cols):
            t=(BAYER[r%4][c%4]+.5)/16*.8+rnd.random()*.2
            v=dens-t
            rr=rows-1-r if flip else r
            if v>.32: rects.append(f'<rect x="{c*pitch}" y="{rr*pitch}" width="{pitch}" height="{pitch}"/>')
            elif v>0:
                o=(pitch-sq)/2; rects.append(f'<rect x="{c*pitch+o}" y="{rr*pitch+o}" width="{sq}" height="{sq}" rx=".6"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{cols*pitch}" height="{rows*pitch}" fill="#fff">{"".join(rects)}</svg>'
def write_bands():
    os.makedirs(f'{ROOT}/assets/img',exist_ok=True)
    open(f'{ROOT}/assets/img/band-down.svg','w').write(band_svg(False))
    open(f'{ROOT}/assets/img/band-up.svg','w').write(band_svg(True))
CSS='''
/* Privy-style section separation: tinted band with dithered grid edges */
#field{display:none}
#spot{padding-bottom:56px}
#wall{position:relative;padding-top:calc(70px + clamp(28px,3.4vw,48px));padding-bottom:calc(70px + clamp(48px,6vw,80px));border-image:conic-gradient(#f8f9fc 0 0) fill 0//0 100vmax}
#wall::before,#wall::after{content:"";position:absolute;left:calc(50% - 50vw);width:100vw;height:70px;background-repeat:repeat-x;background-size:480px 70px;pointer-events:none}
#wall::before{top:0;background-image:url("assets/img/band-down.svg")}
#wall::after{bottom:0;background-image:url("assets/img/band-up.svg")}
/* taller chips; search bar matches */
.chip{height:40px;padding:0 17px;font-size:14px}
.crow .icon-btn{width:40px;height:40px}
.crow .overlay{top:calc(50% - 26px);border-radius:24px}
.crow .overlay.has-q{border-radius:24px}
.crow .o-row{height:50px;padding:0 22px;gap:12px}
.crow .o-row svg{width:17px;height:17px}
.crow .o-row input{font-size:15px}
'''
def home(h):
    write_bands()
    import re
    h=re.sub(r'(<button class="chip" type="button" data-m="[^"]+" aria-pressed="(?:true|false)">[^<]+?) <span>\d+</span>(</button>)',r'\1\2',h)
    return h.replace('</style>',CSS+'</style>',1)
