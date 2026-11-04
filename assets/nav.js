(function(){'use strict';const $=s=>document.querySelector(s);const IMG=document.currentScript.dataset.img;
const nav=$('#nav'),menu=$('#menu'),navList=$('#navList'),scrim=$('#scrim');
const P='https://www.privy.io';
const mcol=(t,items)=>`<div class="mcol"><h6>${t}</h6>${items.map(([a,b,h])=>`<a class="mi" href="${h.startsWith('http')?h:P+h}"><b>${a}</b><span>${b}</span></a>`).join('')}</div>`;
const promo=([a,b,img,h])=>`<a class="promo" href="${h.startsWith('http')?h:P+h}"><img src="${IMG+img}.png" alt="" loading="lazy"><b>${a}</b><span>${b}</span></a>`;
const pcol=(t,list,strip)=>`<div class="mcol promo-col"><h6>${t}</h6><div class="promos">${list.map(promo).join('')}</div>${strip?`<a class="mstrip" href="${strip[1].startsWith('http')?strip[1]:P+strip[1]}">${strip[0]} <span class="arrow">→</span></a>`:''}</div>`;
const MENUS=[
 ['Products','repeat(5,minmax(0,1fr))',
  mcol('Wallets',[['User wallets','Embedded wallets for seamless user onboarding and transactions','/user-wallets'],['Organization wallets','Shared wallets for teams managing funds, permissions, and approvals','/organization-wallets'],['Agent wallets','Wallets for autonomous agents to hold funds and execute transactions','/agent-wallets']])
  +mcol('Security and controls',[['Key management','Secure, programmable key infrastructure for every wallet','/keys'],['Policy engine','Programmable rules, approvals, and transfer controls','/keys#auth'],['Roles and permissions','Granular access controls for teams and workflows','/keys#auth'],['Security architecture','Institutional-grade security for digital asset operations','/security']])
  +mcol('Financial flows',[['Funding','Global funding infrastructure for fiat and digital assets','/funding'],['Cards and spend','Card programs connected directly to wallet balances','/cards-and-spend'],['Treasury management','Treasury infrastructure for managing reserves, liquidity, and capital flows','/treasury-management'],['Yield integrations','Onchain yield access and capital deployment','/yield-integrations']])
  +`<div class="mcol promo-col" style="grid-column:span 2"><h6>Now available</h6><div class="promos">${[['Digital asset accounts','Unified accounts to store, move, and manage digital assets','A8PkfcSjENkRmePCm3totf6sbg','/accounts'],['Universal deposit addresses','Fund wallets from any supported chain with a single address','pkmw3GUfH07GcxYJIeHWm7PBwQA','https://privy.io/blog/introducing-universal-deposit-addresses']].map(promo).join('')}</div></div>`],
 ['Solutions','repeat(5,minmax(0,1fr))',
  mcol('Institutions',[['Banking','Modernize account infrastructure with programmable wallets','/institutions'],['Asset management','Manage and deploy digital assets with built-in controls','/institutions'],['Market infrastructure','Bring markets and financial assets onchain','/institutions']])
  +mcol('Fintechs',[['Payments','Build global payment flows on stablecoin rails','/payments'],['Neobanks','Power modern banking experiences with programmable accounts','/neobanks'],['Payroll','Run global payroll with instant, programmable payouts','/payroll'],['Remittances','Send money across borders faster and more efficiently','/remittances']])
  +mcol('Trading',[['DeFi','Enable access to onchain markets and liquidity','/defi'],['Exchanges','Power high-performance trading infrastructure at scale','/defi'],['Prediction markets','Support real-time trading on event-driven markets','/defi']])
  +mcol('Consumer applications',[['Gaming','Power real-time economies for games, wagering, and interactive experiences','/gaming'],['Social and creator platforms','Embed ownership and monetization directly into user experiences','/consumer'],['Marketplaces','Enable payments, payouts, and asset flows between buyers and sellers','/consumer']])
  +mcol('AI',[['AI and agentic systems','Build systems where agents can transact and operate autonomously','/agent-wallets']])
  +`<a class="mstrip full" href="${P}/integrations">Partners<span>Integrate with leading providers across custody, payments, funding, and onchain infrastructure</span></a>`],
 ['Developer','repeat(2,minmax(0,1fr))',
  mcol('Developer resources',[['Docs','Everything you need to build with Privy','https://docs.privy.io/'],['Demo','Explore and customize auth, wallets, and user flows','https://demo.privy.io/'],['Agent CLI','Create, fund, and manage agent wallets from the command line','https://agents.privy.io/'],['GitHub','Access SDKs, examples, and open-source tools','https://github.com/privy-io'],['Support','Documentation, troubleshooting, and developer support','https://privy.io/slack']])
  +pcol('Security',[['Security Handbook','A modular series of security briefs on Privy’s infrastructure, written for builders, product teams, and reviewers.','Rzfx9zIgS11HoBs138BBrl1hQ','/security#handbook'],['Trust Center','Visit our Trust Center for full technical specifications and audits.','nhkOT0a3SxiHTFaEn9wA9FZxnI','https://trust.privy.io/']],['Learn more','/security'])],
 ['Resources','minmax(0,1fr) minmax(0,1fr) minmax(0,2fr)',
  mcol('Company',[['About','The team and mission behind Privy','/careers'],['Careers','Join the team','/careers'],['Guides','Key concepts and best practices for building with Privy','/learn'],['Brand guidelines','Downloadable brand assets and usage guidance','/brand-guidelines'],['Customer love','What customers are saying about Privy','/love']])
  +mcol('Contact',[['Contact Sales','Talk to our team about building with Privy','/contact'],['Become a partner','Explore ecosystem and integration partnerships across custody, blockchains, and financial infrastructure','/contact'],['Support','Documentation, troubleshooting, and developer support','https://privy.io/slack']])
  +pcol('Blog',[['Upleveling treasury operations','Learn how teams are scaling treasury on stablecoin rails with Privy','DnD1BgfOjamcVW5xzphBVDtMiw','https://privy.io/blog/upleveling-treasury-operations-with-privy-on-stablecoin-rails'],['Introducing wallet actions','A simpler way to build on crypto rails with Privy','RuQTj23CfaFkRbrOU8uUEij6ig','/blog/introducing-wallet-actions']],['View all blog posts','/blog'])]
];
const CHEV='<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 5.5L7 9.5L11 5.5" fill="none" stroke="#757575" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
navList.innerHTML=MENUS.map(([l,c,h],i)=>`<li class="ni"><button class="nl" type="button" aria-expanded="false" aria-controls="mega${i}">${l}${CHEV}</button><div class="mega" id="mega${i}"><div class="mgrid" style="--cols:${c}">${h}</div></div></li>`).join('')
 +`<li><a class="nl" href="${P}/pricing">Pricing</a></li><li class="only-menu"><a href="https://docs.privy.io/">Docs</a></li><li class="only-menu"><a href="https://dashboard.privy.io/">Log in</a></li>`;
const narrow=()=>innerWidth<1040;
const items=[...navList.querySelectorAll('.ni')];
function openItem(li){items.forEach(x=>{const o=x===li;x.classList.toggle('open',o);x.querySelector('.nl').setAttribute('aria-expanded',o);});nav.classList.toggle('has-open',!!li);scrim.classList.toggle('on',!!li&&!narrow());}
const setMenu=o=>{nav.classList.toggle('open',o);menu.setAttribute('aria-expanded',o);if(!o)openItem(null);};
let closeT;
items.forEach(li=>{
  li.querySelector('.nl').addEventListener('click',()=>openItem(li.classList.contains('open')?null:li));
  li.addEventListener('pointerenter',e=>{if(e.pointerType!=='mouse'||narrow())return;clearTimeout(closeT);openItem(li);});
});
navList.querySelectorAll('li:not(.ni)').forEach(li=>li.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'&&!narrow()){clearTimeout(closeT);openItem(null);}}));
nav.addEventListener('pointerleave',e=>{if(e.pointerType==='mouse'&&!narrow())closeT=setTimeout(()=>openItem(null),140);});
nav.addEventListener('pointerenter',()=>clearTimeout(closeT));
menu.onclick=e=>{e.stopPropagation();setMenu(!nav.classList.contains('open'));};
document.addEventListener('click',e=>{if(!nav.contains(e.target)){setMenu(false);openItem(null);}});
addEventListener('keydown',e=>{if(e.key==='Escape'){setMenu(false);openItem(null);}});
})();