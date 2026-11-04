/* Article extras: "At a glance" stats, pull-quote callouts, and the closing CTA + "Keep reading" band.
   Per-post content lives in EXTRAS below (stats and quotes are taken from each article's own text).
   "Keep reading" uses assets/posts-data.js, generated from the landing page's POSTS. */
(function(){
'use strict';

var EXTRAS={
  'inside-the-stack-how-deel-is-turning-payroll-into-a-financial-account':{
    stats:[['80+','countries where contractors can hold a Deel dollar balance'],['74%','of payout recipients deposited into Earn'],['85%','30-day retention for contractors using Earn']],
    stack:[['Stripe','collects pay'],['Bridge','issues DLUSD'],['Privy','embedded wallets'],['Tempo','settlement'],['Morpho','yield vaults']],
    pulls:[['putting-a-paycheck-to-work','The paycheck doesn’t just arrive differently; the product around it can do more.']]
  },
  'inside-the-stack-how-kraken-is-expanding-beyond-the-exchange':{
    stats:[['$400M+','deposited into DeFi Earn across four vaults'],['600+','currencies and assets customers can spend with Krak Card'],['2%','cashback, paid in US dollars or Bitcoin']],
    stack:[['Privy','non-custodial wallets'],['Veda','yield vaults'],['Sentora','risk curation'],['Stripe','card issuing'],['Bridge','stablecoin orchestration']],
    pulls:[['one-product-experience-multiple-financial-rails','Users don’t need to choose between a crypto experience and a traditional financial one.']]
  },
  'inside-the-stack-how-courtyard-is-reinventing-the-collectibles-marketplace':{
    stats:[['$2M+','daily trading volume on Polygon, up from under $1M'],['50K+','trades on many days in 2026, up from about 10K'],['$4M+','in volume on peak trading days']],
    stack:[['Privy','collector wallets'],['Polygon','1:1 tokenized assets'],['Stripe','fiat pay-ins'],['Stripe','Crypto Onramp'],['USDC','payouts and settlement']],
    pulls:[['an-onchain-marketplace-funded-your-way','You shouldn’t need to own crypto, understand stablecoins, or know what chain your collectible lives on to participate.']]
  }
};

var esc=function(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')};
var slug=(location.pathname.split('/').pop()||'').replace(/\.html$/,'');

// same halftone dot edge as the landing page's cards
(function(){
  var dots='';
  for(var r=0;r<6;r++){var y=3+r*6,rad=(.55+r*.72).toFixed(2);
    [2.5,7.5].forEach(function(x){dots+='<circle cx="'+x+'" cy="'+y+'" r="'+rad+'" fill="white"/>'});}
  var svg='<svg xmlns="http://www.w3.org/2000/svg" width="10" height="37">'+dots+'<rect y="33" width="10" height="4" fill="white"/></svg>';
  document.documentElement.style.setProperty('--ax-halftone','url("data:image/svg+xml,'+encodeURIComponent(svg)+'")');
})();

function glance(main,x){
  var el=document.createElement('section');
  el.className='ax-glance';el.id='at-a-glance';el.setAttribute('aria-labelledby','ax-glance-h');
  el.innerHTML='<h2 class="ax-eyebrow" id="ax-glance-h">At a glance</h2>'
    +'<ul class="ax-stats">'+x.stats.map(function(s){return '<li><b>'+esc(s[0])+'</b><span>'+esc(s[1])+'</span></li>'}).join('')+'</ul>'
    +(x.stack?'<ul class="ax-chips" aria-label="The stack">'+x.stack.map(function(c){return '<li><b>'+esc(c[0])+'</b>'+esc(c[1])+'</li>'}).join('')+'</ul>':'');
  main.insertBefore(el,main.firstChild);
  // first entry in "On this page"; andrew.js builds the TOC ruler from these links afterwards
  var toc=document.querySelector('[class*="__tocList"]');
  if(toc){var li=document.createElement('li');li.innerHTML='<a href="#at-a-glance">At a glance</a>';toc.insertBefore(li,toc.firstChild);}
}

function pulls(x){
  (x.pulls||[]).forEach(function(p){
    var h=document.getElementById(p[0]);if(!h)return;
    var q=document.createElement('blockquote');q.className='ax-pull';q.innerHTML='<p>'+esc(p[1])+'</p>';
    h.parentNode.insertBefore(q,h);
  });
}

function keepReading(article){
  var P=window.PRIVY_POSTS,CAT=window.PRIVY_CAT;if(!P||!CAT)return;
  var posts=P.map(function(p){return {title:p[0],slug:p[1],img:p[2].indexOf('http')===0?p[2]:'../assets/img/'+p[2]+'.png',cat:p[3],date:p[4],text:p[5],url:p[6]?p[1]+'.html':'https://www.privy.io/blog/'+p[1],t:Date.parse(p[4])||0}});
  var me=posts.filter(function(p){return p.slug===slug})[0];
  var rest=posts.filter(function(p){return p.slug!==slug}).sort(function(a,b){return b.t-a.t});
  // same category first, newest first; topped up with the newest posts overall
  var pick=me?rest.filter(function(p){return p.cat===me.cat}).slice(0,3):[];
  rest.forEach(function(p){if(pick.length<3&&pick.indexOf(p)<0)pick.push(p)});
  var card=function(p){return '<a class="ax-card" href="'+esc(p.url)+'"><div class="ax-art"><img src="'+esc(p.img)+'" alt="" loading="lazy" decoding="async"></div>'
    +'<div class="ax-panel"><h3>'+esc(p.title)+'</h3><p>'+esc(p.text)+'</p><span class="ax-meta"><b>'+esc(CAT[p.cat])+'</b><i></i><span>'+esc(p.date)+'</span></span></div></a>'};
  var end=document.createElement('div');end.className='ax-end';
  end.innerHTML='<section class="ax-cta" aria-labelledby="ax-cta-h"><div class="ax-in"><div>'
    +'<h2 id="ax-cta-h"><em>Building something like this?</em><br>Talk to our team</h2>'
    +'<p>If your product spans traditional and onchain rails, we can walk through wallets, stablecoin issuance, and payouts on the Stripe stablecoin stack.</p>'
    +'<div class="ax-acts"><a class="ax-btn dark" href="https://www.privy.io/contact">Talk to sales</a><a class="ax-btn line" href="https://dashboard.privy.io/">Start building</a></div></div>'
    +'<div class="ax-stack" aria-hidden="true"><img src="../assets/img/Y1FmUxwPgSmgutb2e6Adpa6p8WQ.png" alt="" loading="lazy"></div></div></section>'
    +'<section class="ax-more" aria-labelledby="ax-more-h"><div class="ax-in"><div class="ax-head"><h2 id="ax-more-h"><em>Keep</em> reading</h2>'
    +'<a class="ax-all" href="../index.html#wall">View all posts <span aria-hidden="true">→</span></a></div>'
    +'<div class="ax-grid">'+pick.slice(0,3).map(card).join('')+'</div></div></section>';
  var related=article.querySelector('[class*="__relatedBand"]');
  if(related)related.parentNode.insertBefore(end,related);else article.appendChild(end);
  document.body.classList.add('ax-ready');
}

function init(){
  var article=document.querySelector('main article');if(!article)return;
  var x=EXTRAS[slug],main=article.querySelector('[class*="__articleMain"]');
  if(x&&main){glance(main,x);pulls(x);}
  keepReading(article);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
