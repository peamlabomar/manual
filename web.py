# -*- coding: utf-8 -*-
# Gera a versão para celular (PWA, funciona offline) do Manual da Exposição Marinha Itinerante.
# Reaproveita os textos de build.py, content.py e closing.py; saída em out/site.
import os, re, html, json, hashlib, shutil, unicodedata
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = ROOT + '/out/site'
VERSAO = '1.0-rascunho'
DATA = '13/11/2026'
BASE_URL = 'https://peamlabomar.github.io/manual/'
ASSETS = ROOT + '/assets/'
TRILHA = ROOT + '/base/'   # ícones e fontes
os.chdir(ROOT)

# ---------------------------------------------------------------- textos
SRC = open('build.py', encoding='utf-8').read()
head = SRC[:SRC.index('P=[]')].replace('from playwright.async_api import async_playwright', '')
front = SRC[SRC.index('P=[]'):SRC.index('# ---------- CAPÍTULOS')]
ns = {}
exec(head, ns)
ns['IM'] = 'img/'; ns['AS'] = 'img/'
def plain(title, inner, kicker=''):
    return f'<websec data-k="{kicker}" data-t="{html.escape(title)}">{inner}</websec>'
ns['plain'] = plain
exec(front, ns)
exec('from content import C', ns)
ns['CH_START'] = {}
exec(open('closing.py', encoding='utf-8').read(), ns)
C = ns['C']; LV = ns['LV']; hl = ns['hl']
BLUE, NAVY, SKY, YEL, CORAL, GREEN, INK, SOFT = (ns[k] for k in ['BLUE', 'NAVY', 'SKY', 'YEL', 'CORAL', 'GREEN', 'INK', 'SOFT'])

def slug(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

# seções de texto (exceto capa, folha de rosto e sumário)
SECS = []   # (id, kicker, título, html)
for item in ns['P']:
    m = re.match(r'<websec data-k="([^"]*)" data-t="([^"]*)">(.*)</websec>$', item, re.S)
    if not m: continue
    k, t, inner = m.group(1), html.unescape(m.group(2)), m.group(3)
    if t == 'Sumário': continue
    if SECS and SECS[-1][2] == t: SECS[-1] = (SECS[-1][0], SECS[-1][1], t, SECS[-1][3] + inner)
    else: SECS.append((slug(t), k, t, inner))
# referências: todas as seções num lugar só
R = ns['R']
refs_html = '<p>Fontes consultadas na revisão técnica desta edição, organizadas pelo capítulo em que são usadas. Acesso aos endereços eletrônicos em novembro de 2026.</p>' + ns['refs'](list(R))
SECS = [(i, k, t, refs_html if t == 'Referências' else h) for i, k, t, h in SECS]
# ficha técnica (página de créditos do PDF)
cred_raw = ns['P'][2]
cred_inner = cred_raw[cred_raw.index('>', cred_raw.index('class="body sans"')) + 1:cred_raw.rindex('</div></section>')]
SECS.append(('ficha', 'Pós-textual', 'Ficha técnica', cred_inner))
SEC = {s[0]: s for s in SECS}
INTRO = ['como-usar-este-guia', 'ods-14-vida-na-agua', 'educacao-ambiental-na-pratica']
FIM = [s[0] for s in SECS if s[0] not in INTRO]

# ---------------------------------------------------------------- animais
def cards(k, items):
    col = LV[k][2]
    return ''.join(f'<div class="card"><div class="dot" style="background:{col}">{i}</div><div><h3>{t}</h3><p>{hl(x)}</p></div></div>'
                   for i, (t, x) in enumerate(items, 1))
def marks(ms):
    return ''.join(f'<span class="mk" style="left:{x}%;top:{y}%">{l}</span>' for x, y, l in (ms or []))
def material(ch):
    o = f'<div class="box"><b>Com a peça em mãos.</b> {hl(ch["x_intro"])}</div>' if ch.get('x_intro') else ''
    for i, d in enumerate(ch['x'], 1):
        o += (f'<figure class="fig"><div class="ph"><img loading="lazy" src="img/{d["img"]}" alt="{html.escape(d["t"])}">'
              f'<span class="tag">{i}</span>{marks(d.get("marks"))}</div>'
              f'<figcaption><h3>{d["t"]}</h3><p>{hl(d["x"])}</p></figcaption></figure>')
    return o

ANIM = []
for ch in C:
    ch['id'] = slug(ch['nome']); ANIM.append(ch)
caps = []
for ch in C:
    if not caps or caps[-1][0] != ch['cap']: caps.append((ch['cap'], ch['grupo'], []))
    caps[-1][2].append(ch)

def lvbtn(k):
    n, name, col, _ = LV[k]
    return f'<button class="tb" data-k="{k}" role="tab"><span style="background:{col}">{n}</span>{name}</button>'

def animal_view(i, ch):
    ks = [k for k in 'bma' if ch.get(k)] + ['x']
    panels = ''
    for k in ks:
        who = LV[k][3]
        body = material(ch) if k == 'x' else cards(k, ch[k])
        panels += f'<div class="panel" data-k="{k}" role="tabpanel"><p class="who">{who}</p>{body}</div>'
    prv = ANIM[i - 1] if i > 0 else None
    nxt = ANIM[i + 1] if i + 1 < len(ANIM) else None
    pn = '<nav class="pn">' + (f'<a href="#{prv["id"]}">‹ {prv["nome"]}</a>' if prv else '<span></span>') + \
         (f'<a href="#{nxt["id"]}" class="nx">{nxt["nome"]} ›</a>' if nxt else '<a href="#para-quem-chega-e-para-quem-fica" class="nx">Fechamento ›</a>') + '</nav>'
    return f'''<section class="view an" id="{ch['id']}" data-t="{html.escape(ch['nome'])}">
<div class="hero"><img src="img/{ch['foto']}" alt="{html.escape(ch['nome'])}" style="object-position:{ch.get('pos', '50% 50%')}">
<span class="cred">Foto: {ch['cred']}</span>
<div class="ht"><div class="kick">Capítulo {ch['cap']} · {ch['grupo']}</div><h1>{ch['nome']}</h1></div></div>
<div class="tabs" role="tablist">{''.join(lvbtn(k) for k in ks)}</div>
<div class="wrap">{panels}{pn}</div></section>'''

def sec_view(sid):
    _, k, t, inner = SEC[sid]
    order = INTRO + FIM
    j = order.index(sid)
    prv = order[j - 1] if j > 0 else None
    nxt = order[j + 1] if j + 1 < len(order) else None
    if sid == INTRO[-1]: nxt_a = f'<a href="#{ANIM[0]["id"]}" class="nx">Capítulo 1 · Esponja ›</a>'
    elif nxt: nxt_a = f'<a href="#{nxt}" class="nx">{SEC[nxt][2]} ›</a>'
    else: nxt_a = '<a href="#inicio" class="nx">Início ›</a>'
    if sid == FIM[0]: prv_a = f'<a href="#{ANIM[-1]["id"]}">‹ {ANIM[-1]["nome"]}</a>'
    elif prv: prv_a = f'<a href="#{prv}">‹ {SEC[prv][2]}</a>'
    else: prv_a = '<a href="#inicio">‹ Início</a>'
    return f'''<section class="view tx" id="{sid}" data-t="{html.escape(t)}"><div class="wrap">
{f'<div class="kick">{k}</div>' if k else ''}<h1 class="tit">{t}</h1><div class="bar"></div>{inner}
<nav class="pn">{prv_a}{nxt_a}</nav></div></section>'''

# ---------------------------------------------------------------- início
def chip(sid, n=None):
    t = SEC[sid][2]
    return f'<a class="row" href="#{sid}"><span class="rn">{n or "•"}</span><b>{t}</b><span class="ar">›</span></a>'
grid = ''
for cap, grupo, chs in caps:
    grid += f'<h3 class="cg"><span>{cap}</span>{grupo}</h3><div class="grid">'
    for ch in chs:
        grid += f'<a class="ac" href="#{ch["id"]}"><img loading="lazy" src="img/t_{ch["foto"]}" alt=""><b>{ch["nome"]}</b></a>'
    grid += '</div>'
home = f'''<section class="view" id="inicio" data-t="Início">
<div class="cover"><svg viewBox="0 0 400 300" preserveAspectRatio="none" aria-hidden="true"><path d="M0 220c70-34 130-6 200-18s130-40 200-22v120H0z" fill="{SKY}" opacity=".45"/><path d="M0 250c80-24 150 4 220-6s120-26 180-14v70H0z" fill="{SKY}"/></svg>
<div class="ci"><div class="kick" style="color:{YEL}">Guia para educadores ambientais</div>
<h1>Manual da Exposição <span class="hl">Marinha Itinerante</span></h1>
<p class="sub">Um guia para monitores sobre a fauna marinha e como apresentá-la para diferentes públicos</p>
<p class="au">Maiara Maia Borges</p></div></div>
<div class="wrap">
<div class="off" id="off"><div class="oi">✓</div><div><p id="offmsg"><b>Vai sair para uma ação?</b> Abra este manual uma vez com internet. Depois ele funciona <b>sem sinal</b>, na escola, na praça ou na praia.</p>
<p class="ios" id="ios">No iPhone: toque em <b>Compartilhar</b> e depois em <b>Adicionar à Tela de Início</b>.</p>
<button id="inst" hidden>Instalar no celular</button></div></div>
<h2 class="h2">Comece por aqui</h2>
<div class="list">{''.join(chip(s) for s in INTRO)}</div>
<h2 class="h2">Os 25 animais da exposição</h2>
<p class="note">Em cada animal, escolha o nível: <span class="lv" style="background:{GREEN}">1</span> Básico, <span class="lv" style="background:{YEL}">2</span> Moderado, <span class="lv" style="background:{CORAL}">3</span> Avançado ou <span class="lv" style="background:{SKY}">4</span> Material. O manual lembra o último nível escolhido.</p>
{grid}
<h2 class="h2">Para depois</h2>
<div class="list">{''.join(chip(s) for s in FIM)}</div>
<p class="ver">Versão {VERSAO} · {DATA}<br>CC BY-NC-ND 4.0 · Distribuição gratuita · Venda proibida</p>
</div></section>'''

# ---------------------------------------------------------------- CSS
CSS = f"""
@font-face{{font-family:'Inter';src:url(fonts/inter-regular.woff) format('woff');font-weight:400;font-style:normal;font-display:swap}}
@font-face{{font-family:'Inter';src:url(fonts/inter-italic.woff) format('woff');font-weight:400;font-style:italic;font-display:swap}}
@font-face{{font-family:'Inter';src:url(fonts/inter-medium.woff) format('woff');font-weight:500 600;font-style:normal;font-display:swap}}
@font-face{{font-family:'Inter';src:url(fonts/inter-bold.woff) format('woff');font-weight:700;font-style:normal;font-display:swap}}
@font-face{{font-family:'Inter';src:url(fonts/inter-extrabold.woff) format('woff');font-weight:800;font-style:normal;font-display:swap}}
:root{{color-scheme:light}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;font-family:Inter,system-ui,sans-serif;color:{INK};background:#fff;font-size:17px;line-height:1.55}}
a{{color:{BLUE}}}
mark{{background:linear-gradient(transparent 12%,{YEL} 12%,{YEL} 88%,transparent 88%);padding:0 .12em;border-radius:2px;color:inherit}}
.top{{position:sticky;top:0;z-index:20;background:#fff;box-shadow:0 1px 0 #e3ebf5}}
.tr{{display:flex;align-items:center;gap:10px;padding:10px 14px;max-width:760px;margin:0 auto}}
.tr .lg{{height:34px;display:block}}
.tr .tt{{font-weight:800;font-size:14px;line-height:1.15;color:{BLUE}}}
.tr .tt span{{font-weight:500;color:#5b6b82}}
.sb{{margin-left:auto;flex:none;width:40px;height:40px;border-radius:50%;border:0;background:{SOFT};color:{BLUE};display:flex;align-items:center;justify-content:center}}
.sr{{display:none;padding:0 14px 12px;max-width:760px;margin:0 auto;position:relative}}
.sr.on{{display:block}}
#q{{width:100%;font:inherit;font-size:16px;padding:11px 14px;border:2px solid #cfdcec;border-radius:99px;outline:none}}
#q:focus{{border-color:{SKY}}}
#res{{list-style:none;margin:6px 0 0;padding:0;background:#fff;border-radius:14px;box-shadow:0 8px 24px rgba(8,39,88,.14);max-height:60vh;overflow:auto}}
#res a{{display:block;padding:11px 16px;text-decoration:none;border-bottom:1px solid #eef3f9}}
#res small{{color:#6b7a90;margin-left:6px}}
.view{{display:none}}
.view.on{{display:block}}
.wrap{{max-width:760px;margin:0 auto;padding:18px 18px 40px}}
.kick{{font-weight:700;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:{SKY}}}
.tit{{font-size:30px;line-height:1.08;font-weight:800;letter-spacing:-.015em;color:{BLUE};margin:6px 0 12px}}
.bar{{width:56px;height:7px;border-radius:7px;background:{YEL};margin:0 0 18px}}
p{{margin:0 0 12px}}
.lead{{font-size:19px;line-height:1.45;color:{BLUE};font-weight:500}}
.sans{{font-family:Inter,system-ui,sans-serif}}
.box{{background:{SOFT};border-radius:16px;padding:16px 18px;margin:0 0 16px}}
.box b:first-child{{color:{BLUE}}}
.card{{display:flex;gap:14px;padding:14px 0;border-bottom:1px solid #dfe7f1}}
.card:last-child{{border-bottom:0}}
.card .dot{{flex:none;width:30px;height:30px;border-radius:50%;margin-top:1px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;color:{NAVY}}}
.card h3{{font-size:18px;line-height:1.25;color:{BLUE};margin:0 0 4px}}
.card p{{margin:0}}
.num{{flex:none;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:20px;color:{NAVY}}}
.tx h3{{line-height:1.3}}
.tx [style*="columns:2"]{{columns:1!important}}
.tx [style*="width:125mm"]{{width:auto!important}}
.tx img{{max-width:100%}}
.tx [style*="display:flex;gap:7mm"]{{flex-direction:column}}
.hero{{position:relative;height:min(62vh,460px);background:{NAVY};overflow:hidden}}
.hero img{{width:100%;height:100%;object-fit:cover;display:block}}
.hero::after{{content:'';position:absolute;inset:0;background:linear-gradient(transparent 45%,rgba(8,39,88,.88))}}
.cred{{position:absolute;right:10px;top:10px;z-index:2;background:rgba(8,39,88,.6);color:#fff;font-size:11px;border-radius:99px;padding:4px 10px;max-width:70%}}
.ht{{position:absolute;left:18px;right:18px;bottom:16px;z-index:2;color:#fff}}
.ht .kick{{color:{YEL}}}
.ht h1{{font-size:42px;line-height:1;font-weight:800;letter-spacing:-.02em;margin:6px 0 0}}
.tabs{{position:sticky;top:55px;z-index:10;display:flex;gap:6px;overflow-x:auto;padding:10px 14px;background:{NAVY};scrollbar-width:none}}
.tabs::-webkit-scrollbar{{display:none}}
.tb{{flex:none;display:flex;align-items:center;gap:7px;font:inherit;font-size:15px;font-weight:700;color:#dbe7f8;background:transparent;border:1.5px solid rgba(255,255,255,.3);border-radius:99px;padding:6px 13px 6px 7px;cursor:pointer}}
.tb span{{width:24px;height:24px;border-radius:50%;color:{NAVY};display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800}}
.tb.on{{background:#fff;color:{BLUE};border-color:#fff}}
.panel{{display:none}}
.panel.on{{display:block}}
.who{{font-size:14px;color:#5b6b82;margin:0 0 4px}}
.fig{{margin:0;padding:14px 0 18px;border-bottom:1px solid #dfe7f1}}
.fig:last-of-type{{border-bottom:0}}
.ph{{position:relative;border-radius:14px;overflow:hidden;background:{SOFT}}}
.ph img{{width:100%;display:block}}
.tag{{position:absolute;left:10px;top:10px;width:30px;height:30px;border-radius:50%;background:{YEL};color:{NAVY};font-weight:800;display:flex;align-items:center;justify-content:center}}
.mk{{position:absolute;width:32px;height:32px;margin:-16px 0 0 -16px;border-radius:50%;border:4px solid {YEL};background:rgba(8,39,88,.55);color:#fff;font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center}}
.fig h3{{font-size:18px;color:{BLUE};margin:12px 0 4px}}
.fig p{{margin:0}}
.pn{{display:flex;justify-content:space-between;gap:10px;margin-top:26px;padding-top:16px;border-top:2px solid {SOFT}}}
.pn a{{font-weight:700;text-decoration:none;padding:10px 14px;border-radius:99px;background:{SOFT};font-size:15px}}
.pn a.nx{{background:{BLUE};color:#fff;margin-left:auto}}
.cover{{position:relative;background:{NAVY};color:#fff;overflow:hidden}}
.cover svg{{position:absolute;inset:0;width:100%;height:100%}}
.ci{{position:relative;max-width:760px;margin:0 auto;padding:34px 22px 110px}}
.ci h1{{font-size:40px;line-height:1.05;font-weight:800;letter-spacing:-.02em;margin:12px 0 0}}
.ci .hl{{background:{YEL};color:{NAVY};padding:0 8px 2px;border-radius:6px;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.ci .sub{{font-size:18px;color:#e3ecf9;margin:16px 0 0;max-width:30em}}
.ci .au{{font-weight:800;margin:22px 0 0;font-size:17px}}
.off{{display:flex;gap:14px;background:#fff;border:1px solid #e3ebf5;border-left:6px solid {GREEN};border-radius:18px;padding:16px;margin:-60px 0 22px;position:relative;box-shadow:0 8px 24px rgba(8,39,88,.1)}}
.off .oi{{flex:none;width:38px;height:38px;border-radius:50%;background:#e4f7ea;color:#1f8a4c;font-weight:800;display:flex;align-items:center;justify-content:center}}
.off p{{margin:0 0 6px}}
.ios{{font-size:15px;color:#3d4d66}}
#inst{{font:inherit;font-weight:700;background:{BLUE};color:#fff;border:0;border-radius:99px;padding:9px 16px;margin-top:6px}}
.h2{{font-size:22px;font-weight:800;color:{BLUE};margin:26px 0 10px}}
.list{{border-radius:16px;background:{SOFT};padding:4px 14px}}
.row{{display:flex;align-items:center;gap:12px;padding:13px 0;text-decoration:none;color:{INK};border-bottom:1px solid #dbe5f1}}
.row:last-child{{border-bottom:0}}
.rn{{color:{SKY};font-weight:800;width:14px}}
.row .ar{{margin-left:auto;color:{SKY};font-size:22px;line-height:1}}
.note{{font-size:15px;color:#3d4d66}}
.lv{{display:inline-flex;width:22px;height:22px;border-radius:50%;align-items:center;justify-content:center;font-weight:800;font-size:12px;color:{NAVY}}}
.cg{{display:flex;align-items:center;gap:10px;font-size:17px;color:{BLUE};margin:20px 0 10px}}
.cg span{{width:28px;height:28px;border-radius:50%;background:{BLUE};color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}}
.ac{{position:relative;display:block;border-radius:14px;overflow:hidden;aspect-ratio:4/3;background:{NAVY};text-decoration:none}}
.ac img{{width:100%;height:100%;object-fit:cover;display:block}}
.ac b{{position:absolute;left:0;right:0;bottom:0;padding:22px 10px 8px;color:#fff;font-size:15px;line-height:1.2;background:linear-gradient(transparent,rgba(8,39,88,.9))}}
.ver{{text-align:center;font-size:13px;color:#6b7a90;margin-top:30px}}
.logos{{display:flex;justify-content:center;align-items:center;gap:22px;padding:20px 12px;border-top:1px solid #e3ebf5}}
footer{{text-align:center;font-size:13px;color:#6b7a90;padding:0 16px 30px}}
"""

# ---------------------------------------------------------------- JS
JS = """
const views=[...document.querySelectorAll('.view')];
function lvGet(){try{return localStorage.getItem('nivel')||'b'}catch(e){return 'b'}}
function lvSet(k){try{localStorage.setItem('nivel',k)}catch(e){}}
function setLv(sec,k){
  const tabs=[...sec.querySelectorAll('.tb')];
  if(!tabs.some(t=>t.dataset.k===k)) k=tabs[0].dataset.k;
  tabs.forEach(t=>{const on=t.dataset.k===k;t.classList.toggle('on',on);t.setAttribute('aria-selected',on)});
  sec.querySelectorAll('.panel').forEach(p=>p.classList.toggle('on',p.dataset.k===k));
}
document.querySelectorAll('.an').forEach(sec=>{
  sec.querySelectorAll('.tb').forEach(t=>t.addEventListener('click',()=>{
    setLv(sec,t.dataset.k); lvSet(t.dataset.k);
    const tb=sec.querySelector('.tabs'); window.scrollTo({top:Math.max(0,sec.offsetTop+sec.querySelector('.hero').offsetHeight-56),behavior:'smooth'});
  }));
});
function route(){
  const id=(location.hash||'#inicio').slice(1)||'inicio';
  let v=document.getElementById(id); if(!v||!v.classList.contains('view')) v=document.getElementById('inicio');
  views.forEach(x=>x.classList.toggle('on',x===v));
  if(v.classList.contains('an')) setLv(v,lvGet());
  document.title=(v.id==='inicio'?'':v.dataset.t+' · ')+'Manual da Exposição Marinha Itinerante';
  window.scrollTo(0,0); requestAnimationFrame(()=>window.scrollTo(0,0)); closeSearch();
  const a=v.querySelector('.tb.on'); if(a){const t=a.parentElement; t.scrollLeft=a.offsetLeft-t.clientWidth/2+a.offsetWidth/2;}
}
// busca
const sb=document.getElementById('sb'),sr=document.getElementById('sr'),q=document.getElementById('q'),res=document.getElementById('res');
const idx=views.filter(v=>v.id!=='inicio').map(v=>({id:v.id,t:v.dataset.t,g:v.querySelector('.kick')?v.querySelector('.kick').textContent:'',txt:v.textContent}));
const norm=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
function closeSearch(){sr.classList.remove('on');q.value='';res.innerHTML=''}
sb.addEventListener('click',()=>{sr.classList.toggle('on');if(sr.classList.contains('on'))q.focus()});
q.addEventListener('input',()=>{
  const s=norm(q.value.trim()); if(s.length<2){res.innerHTML='';return}
  const a=idx.filter(x=>norm(x.t).includes(s)).map(x=>[x,0]).concat(idx.filter(x=>!norm(x.t).includes(s)&&norm(x.txt).includes(s)).map(x=>[x,1]));
  res.innerHTML=a.slice(0,12).map(([x,w])=>`<li><a href="#${x.id}">${x.t}<small>${w?'menciona “'+q.value.trim()+'”':x.g}</small></a></li>`).join('')||'<li><a>Nada encontrado</a></li>';
});
// offline
const off=document.getElementById('offmsg');
if('serviceWorker' in navigator){
  navigator.serviceWorker.register('sw.js').then(()=>navigator.serviceWorker.ready).then(r=>{
    navigator.serviceWorker.addEventListener('message',e=>{if(e.data==='cached'){off.innerHTML+=' <b>Pronto:</b> este manual já está salvo neste celular e funciona sem internet.'}});
    setTimeout(()=>r.active&&r.active.postMessage('check'),1500);
  }).catch(()=>{});
}
const ua=navigator.userAgent; if(!/iPhone|iPad/.test(ua)||navigator.standalone) document.getElementById('ios').hidden=true;
window.addEventListener('hashchange',route); route();
let dp; window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();dp=e;const b=document.getElementById('inst');b.hidden=false;b.onclick=()=>{dp.prompt();b.hidden=true}});
"""

desc = 'Manual da Exposição Marinha Itinerante (PEAM/LABOMAR/UFC), de Maiara Maia Borges: 25 animais marinhos em quatro níveis para educadores ambientais. Funciona sem internet.'
doc = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Manual da Exposição Marinha Itinerante · PEAM</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="{NAVY}">
<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="icons/icon-180.png"><link rel="icon" href="icons/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Manual PEAM">
<meta property="og:type" content="website"><meta property="og:title" content="Manual da Exposição Marinha Itinerante · PEAM">
<meta property="og:description" content="{desc}"><meta property="og:image" content="{BASE_URL}img/og.jpg"><meta property="og:url" content="{BASE_URL}">
<meta name="twitter:card" content="summary_large_image">
<style>{CSS}</style></head><body>
<header class="top"><div class="tr"><a href="#inicio"><img class="lg" src="img/peam-horizontal.png" alt="PEAM"></a><div class="tt">Manual da Exposição<br><span>Marinha Itinerante</span></div>
<button class="sb" id="sb" aria-label="Buscar"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="7"/><path d="M20 20l-4.2-4.2"/></svg></button></div>
<div class="sr" id="sr"><input id="q" type="search" placeholder="Buscar: polvo, cnidócito, tubarão…" autocomplete="off"><ul id="res"></ul></div></header>
<main>{home}{''.join(sec_view(s) for s in INTRO)}{''.join(animal_view(i, ch) for i, ch in enumerate(ANIM))}{''.join(sec_view(s) for s in FIM)}</main>
<div class="logos"><img src="img/ufc.png" alt="UFC" style="height:40px"><img src="img/labomar.png" alt="LABOMAR" style="height:24px"><img src="img/mcti-mec-governo.png" alt="MEC e MCTI" style="height:30px"></div>
<footer>Programa de Educação Ambiental Marinha · LABOMAR · UFC<br>Versão {VERSAO} · {DATA}</footer>
<script>{JS}</script></body></html>'''

# ---------------------------------------------------------------- arquivos
shutil.rmtree(OUT + '/img', ignore_errors=True)
for d in ['img', 'icons', 'fonts']: os.makedirs(OUT + '/' + d, exist_ok=True)
for f in os.listdir(TRILHA + 'fonts'): shutil.copy(TRILHA + 'fonts/' + f, OUT + '/fonts/' + f)
for f in os.listdir(TRILHA + 'icons'): shutil.copy(TRILHA + 'icons/' + f, OUT + '/icons/' + f)
for f in ['peam-horizontal.png', 'labomar.png', 'ufc.png', 'mcti-mec-governo.png']:
    im = Image.open(ASSETS + f); im.thumbnail((600, 200)); im.save(OUT + '/img/' + f, optimize=True)

used = sorted(set(re.findall(r'src="img/([^"]+\.(?:jpg|jpeg|png))"', doc)) - {'peam-horizontal.png', 'labomar.png', 'ufc.png', 'mcti-mec-governo.png'})
for f in used:
    thumb = f.startswith('t_')
    src = ROOT + '/img/' + (f[2:] if thumb else f)
    im = Image.open(src)
    im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
    im.thumbnail((420, 420) if thumb else (1100, 1100))
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[3]); im = bg
    im.save(OUT + '/img/' + re.sub(r'\.(jpg|jpeg|png)$', '.webp', f), 'WEBP', quality=78, method=6)
    doc = doc.replace(f'src="img/{f}"', f'src="img/{re.sub(r"[.](jpg|jpeg|png)$", ".webp", f)}"')
open(OUT + '/index.html', 'w', encoding='utf-8').write(doc)

# prévia de link (WhatsApp, Instagram)
og = Image.new('RGB', (1200, 630), NAVY)
ph = Image.open(ROOT + '/img/op_polvo.jpg').convert('RGB')
ph = ph.resize((560, int(ph.height * 560 / ph.width))); og.paste(ph.crop((0, 0, 560, 630)), (640, 0))
d = ImageDraw.Draw(og)
fb = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', 56)
fm = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf', 26)
fk = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 20)
d.text((60, 70), 'GUIA PARA EDUCADORES AMBIENTAIS', font=fk, fill=YEL)
d.text((60, 112), 'Manual da\nExposição Marinha\nItinerante', font=fb, fill='white', spacing=6)
d.text((60, 345), '25 animais em quatro níveis\nFunciona sem internet', font=fm, fill='#dbe7f8', spacing=8)
lg = Image.open(ASSETS + 'peam-horizontal.png').convert('RGBA'); lg.thumbnail((300, 80))
box = Image.new('RGB', (lg.width + 40, lg.height + 30), 'white'); box.paste(lg, (20, 15), lg)
og.paste(box, (60, 470))
d.text((60, 590 - 10), 'Maiara Maia Borges · PEAM/LABOMAR/UFC', font=fk, fill='#dbe7f8')
og.save(OUT + '/img/og.jpg', quality=85)

man = {'name': 'Manual da Exposição Marinha Itinerante · PEAM', 'short_name': 'Manual PEAM',
       'description': desc, 'lang': 'pt-BR', 'start_url': './', 'scope': './', 'display': 'standalone',
       'background_color': '#ffffff', 'theme_color': NAVY,
       'icons': [{'src': 'icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                 {'src': 'icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                 {'src': 'icons/maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]}
json.dump(man, open(OUT + '/manifest.webmanifest', 'w'), ensure_ascii=False, indent=1)

files = ['./', 'index.html', 'manifest.webmanifest']
for sub in ['fonts', 'icons', 'img']:
    files += [f'{sub}/{f}' for f in sorted(os.listdir(OUT + '/' + sub))]
h = hashlib.md5(open(OUT + '/index.html', 'rb').read()).hexdigest()[:8]
SW = '''const CACHE='manual-%s-%s';
const FILES=%s;
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;
 e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request).catch(()=>caches.match('index.html'))));});
self.addEventListener('message',e=>{if(e.data==='check'){caches.open(CACHE).then(c=>c.keys()).then(ks=>{if(ks.length>=FILES.length-1)e.source.postMessage('cached');});}});
''' % (VERSAO, h, json.dumps(files))
open(OUT + '/sw.js', 'w').write(SW)
open(OUT + '/.nojekyll', 'w').write('')
tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs if '.git' not in dp)
print(len(files), 'arquivos', round(tot / 1e6, 2), 'MB', [s[0] for s in SECS])
