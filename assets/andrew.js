/* Ported from Andrew's site: scroll-driven TOC ruler + active section ink, and the copy-link buttons. */
(function(){
'use strict';
var STIFF=240,DAMP=31;
var JIT=[.125,.625,.375,.875],TICK=[226,229,236],TICK_HOT=[117,109,255],INK=[112,112,125],INK_HOT=[17,17,23];
var mix=function(a,b,t){return 'rgb('+a.map(function(v,i){return Math.round(v+(b[i]-v)*t)}).join(' ')+')'};
var sstep=function(x){var t=Math.min(1,Math.max(0,x));return t*t*(3-2*t)};
var reduce=matchMedia('(prefers-reduced-motion: reduce)');

function toc(list,canvas){
  var ctx=canvas.getContext('2d');if(!ctx)return;
  var links=[].slice.call(list.querySelectorAll('a'));
  var heads=links.map(function(a){return document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)))});
  var inks=links.map(function(){return ''});
  var box=list.closest('nav')&&list.closest('nav').parentElement;
  var m=null,pos=null,vel=0,raf=0,last=0;
  function measure(){
    var h=list.offsetHeight,dpr=devicePixelRatio||1;
    canvas.width=28*dpr;canvas.height=Math.round(h*dpr);canvas.style.height=h+'px';
    m={tops:heads.map(function(e){return e?e.getBoundingClientRect().top+scrollY:Infinity}),
       anchors:links.map(function(a){return 6*Math.round((a.offsetTop+17-.5)/6)+.5}),
       line:(parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||64)+16,
       view:innerHeight,height:h};
  }
  function target(){
    var y=scrollY,t=m.tops,line=m.line,view=m.view;
    var v=t.reduce(function(acc,top,i){var span=Math.max(1,Math.min(.45*view,i?(top-t[i-1])*.6:Infinity));return acc+sstep((line-(top-y-span))/span)},-1);
    if(v<=0)return v;var f=Math.floor(v),r=v-f;return f+r*r*r*(r*(6*r-15)+10);
  }
  var art=document.querySelector('[class*="__articleMain"]')||document.querySelector('main article');
  function draw(p,speed){
    var dpr=devicePixelRatio||1,H=m.height;
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,28,H);
    // reading progress through the article: a thin track that fills with ink
    var r=art.getBoundingClientRect(),span=Math.max(1,r.height-innerHeight*.6);
    var prog=Math.min(1,Math.max(0,(innerHeight*.3-r.top)/span));
    ctx.fillStyle='rgb(226 229 236)';ctx.fillRect(0,0,2,H);
    ctx.fillStyle='rgb(1 1 16)';ctx.fillRect(0,0,2,Math.round(H*prog));
    var cur=Math.round(p);
    links.forEach(function(el,j){
      var col=mix(INK,INK_HOT,Math.max(0,1-Math.abs(p-j)));
      if(col!==inks[j]){inks[j]=col;el.style.setProperty('--toc-ink',col)}
      var on=j===cur&&p>-.5;
      if(on!==el.hasAttribute('aria-current')){
        if(on){el.setAttribute('aria-current','location');
          if(box&&box.scrollHeight>box.clientHeight+1){var br=box.getBoundingClientRect(),er=el.getBoundingClientRect();
            box.scrollTo({top:Math.max(0,box.scrollTop+er.top-br.top-(box.clientHeight-er.height)/2),behavior:reduce.matches?'auto':'smooth'})}}
        else el.removeAttribute('aria-current');
      }
    });
  }
  function frame(now){
    raf=0;if(!m)measure();if(m.height===0)return;
    var goal=target(),dt=last?Math.min(.05,(now-last)/1000):1/60;last=now;
    if(pos===null||reduce.matches){pos=goal;vel=0}
    else for(var t=dt;t>0;t-=.004){var s=Math.min(.004,t);vel+=(-STIFF*(pos-goal)-DAMP*vel)*s;pos+=vel*s}
    draw(pos,Math.abs(vel));
    if(Math.abs(pos-goal)>5e-4||Math.abs(vel)>5e-4)raf=requestAnimationFrame(frame);else last=0;
  }
  function kick(){if(!raf)raf=requestAnimationFrame(frame)}
  addEventListener('scroll',function(){if(m&&pos!==null)requestAnimationFrame(function(){draw(pos,0)})},{passive:true});
  function reset(){m=null;kick()}
  kick();
  var ro=new ResizeObserver(reset);ro.observe(list);ro.observe(document.body);
  addEventListener('scroll',kick,{passive:true});addEventListener('resize',reset);
}

function init(){
  document.querySelectorAll('[class*="__tocBody"]').forEach(function(b){
    var l=b.querySelector('ol'),c=b.querySelector('canvas');if(l&&c&&getComputedStyle(b).display!=='none')toc(l,c);
  });
  document.querySelectorAll('button[aria-label="Copy link"]').forEach(function(btn){
    var note=btn.parentElement.querySelector('[data-copied]'),timer;
    btn.addEventListener('click',function(){
      var done=function(){if(note){note.setAttribute('data-copied','true');note.textContent='Copied'}
        clearTimeout(timer);timer=setTimeout(function(){if(note){note.setAttribute('data-copied','false');note.textContent=''}},1600)};
      if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(location.href).then(done,done);else done();
    });
  });
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
