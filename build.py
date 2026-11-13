import asyncio, os, re
from playwright.async_api import async_playwright
AS='file:///home/claude/social/assets/'; IM='file://'+os.path.abspath('img')+'/'
BLUE='#0c3c86'; NAVY='#082758'; SKY='#53a3d5'; YEL='#fbce5d'; CORAL='#f26f71'; GREEN='#53db76'; INK='#1b2a41'; SOFT='#eef4fb'
LV={'b':('1','Básico',GREEN,'Para crianças menores de 10 anos e para quem teve pouco contato com o mar.'),
    'm':('2','Moderado',YEL,'Para quem quer saber como o animal funciona e qual é o seu papel no ambiente.'),
    'a':('3','Avançado',CORAL,'Para estudantes da área, outros educadores e pessoas muito curiosas.'),
    'x':('4','Material',SKY,'O que mostrar e como conduzir a conversa com a peça da exposição em mãos.')}
def hl(t): return re.sub(r'==(.+?)==', r'<mark>\1</mark>', t)
CSS=f"""
@page{{size:210mm 297mm;margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{font-family:'Lora',serif;color:{INK};font-size:10.6pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}}
.sans{{font-family:'Inter',sans-serif}}
h1,h2,h3,.disp{{font-family:'Inter Display','Inter',sans-serif;font-weight:800;letter-spacing:-.015em;margin:0}}
mark{{background:linear-gradient(transparent 12%,{YEL} 12%,{YEL} 88%,transparent 88%);padding:0 .12em;border-radius:2px;color:inherit}}
.body{{position:absolute;left:20mm;right:20mm;top:46mm;bottom:22mm}}
.head{{position:absolute;left:0;top:0;width:100%;height:38mm;background:{BLUE};color:#fff}}
.head svg{{position:absolute;left:0;bottom:-1px;width:100%;height:14mm}}
.head .in{{position:absolute;left:20mm;right:20mm;top:9mm;display:flex;align-items:center;gap:5mm}}
.num{{flex:none;width:15mm;height:15mm;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Inter Display';font-weight:800;font-size:22pt;color:{NAVY}}}
.head h2{{font-size:24pt;line-height:1}}
.head .who{{font-family:'Inter';font-size:8.6pt;line-height:1.3;color:#dbe7f8;margin-top:1.4mm;max-width:118mm}}
.head .chip{{margin-left:auto;font-family:'Inter';font-weight:700;font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:#fff;border:1.2px solid rgba(255,255,255,.6);border-radius:99px;padding:1.4mm 3.6mm;white-space:nowrap}}
.foot{{position:absolute;left:20mm;right:20mm;bottom:9mm;display:flex;align-items:center;justify-content:space-between;font-family:'Inter';font-size:7.6pt;color:#6b7a90}}
.foot .n{{width:10mm;height:10mm;border-radius:50%;background:{SOFT};color:{BLUE};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:9pt}}
.card{{display:flex;gap:4.5mm;padding:.75em 0;border-bottom:1px solid #dfe7f1;break-inside:avoid}}
.card:last-child{{border-bottom:0}}
.card .dot{{flex:none;width:8mm;height:8mm;border-radius:50%;margin-top:.6mm;display:flex;align-items:center;justify-content:center;font-family:'Inter';font-weight:800;font-size:8.6pt;color:{NAVY}}}
.card h3{{font-size:1.1em;line-height:1.25;color:{BLUE};margin-bottom:1mm}}
.card p{{margin:0;text-align:left}}
p{{margin:0 0 3mm}}
.lead{{font-family:'Inter';font-size:12pt;line-height:1.45;color:{BLUE};font-weight:500}}
.tit{{font-size:30pt;line-height:1.02;color:{BLUE}}}
.bar{{width:16mm;height:2.2mm;border-radius:2mm;background:{YEL};margin:0 0 5mm}}
.box{{background:{SOFT};border-radius:4mm;padding:5mm 6mm;break-inside:avoid}}
.fig{{display:grid;grid-template-columns:62mm 1fr;gap:8mm;align-items:center;padding:5mm 0;border-bottom:1px solid #dfe7f1}}
.fig:last-child{{border-bottom:0}}
.fig.r{{grid-template-columns:1fr 62mm}}
.fig .ph{{position:relative}}
.fig img{{width:62mm;height:58mm;object-fit:cover;border-radius:3mm;display:block}}
.tag{{position:absolute;left:2.5mm;top:2.5mm;width:10mm;height:10mm;border-radius:50%;background:{YEL};color:{NAVY};font-family:'Inter';font-weight:800;font-size:11pt;display:flex;align-items:center;justify-content:center;box-shadow:0 1mm 2mm rgba(8,39,88,.25)}}
.fig h3{{font-size:1.12em;color:{BLUE};margin-bottom:1.5mm}}
"""
WAVE=f'<svg viewBox="0 0 210 14" preserveAspectRatio="none"><path d="M0 14V8c22-9 48-7 78-1s62 8 92 0c16-4 30-5 40-4v11z" fill="{SKY}" opacity=".55"/><path d="M0 14V10c28-7 55-4 86 0s70 5 124-5v9z" fill="#fff"/></svg>'
STATE={'n':0,'run':''}
def foot(show=True):
    STATE['n']+=1
    if not show: return ''
    return f'<div class="foot"><span>Manual da Exposição Marinha Itinerante · PEAM</span><span>{STATE["run"]}</span><span class="n">{STATE["n"]:02d}</span></div>'
def level_page(k,chap,inner):
    n,name,col,who=LV[k]
    return f'<section class="pg"><div class="head"><div class="in"><div class="num" style="background:{col}">{n}</div><div><h2>{name}</h2><div class="who">{who}</div></div><div class="chip">{chap}</div></div>{WAVE}</div><div class="body fit">{inner}</div>{foot()}</section>'
def cards(k,items):
    col=LV[k][2]
    return ''.join(f'<div class="card"><div class="dot" style="background:{col}">{i}</div><div><h3>{t}</h3><p>{hl(x)}</p></div></div>' for i,(t,x) in enumerate(items,1))
def marks(ms):
    return ''.join(f'<div style="position:absolute;left:{x}%;top:{y}%;width:9mm;height:9mm;margin:-4.5mm 0 0 -4.5mm;border-radius:50%;border:1.1mm solid {YEL};background:rgba(8,39,88,.55);color:#fff;font-family:Inter;font-weight:800;font-size:9pt;display:flex;align-items:center;justify-content:center">{l}</div>' for x,y,l in (ms or []))
def figs(items,hh=58):
    o=''
    for i,(img,t,x,ms) in enumerate(items,1):
        ph=f'<div class="ph"><img src="{IM}{img}" style="height:{hh}mm"><div class="tag">{i}</div>{marks(ms)}</div>'; tx=f'<div><h3>{t}</h3><p style="margin:0">{hl(x)}</p></div>'
        o+=f'<div class="fig {"r" if i%2==0 else ""}">{tx+ph if i%2==0 else ph+tx}</div>'
    return o
def plain(title,inner,kicker=''):
    return f'<section class="pg"><div style="position:absolute;left:0;top:0;width:100%;height:9mm;background:{BLUE}"></div><div class="body fit" style="top:26mm">{f"<div class=&quot;sans&quot; style=&quot;font-weight:700;font-size:8.6pt;letter-spacing:.1em;text-transform:uppercase;color:{SKY};margin-bottom:2mm&quot;>{kicker}</div>".replace("&quot;",chr(34)) if kicker else ""}<h1 class="tit">{title}</h1><div class="bar" style="margin-top:4mm"></div>{inner}</div>{foot()}</section>'
P=[]
# ---------- CAPA
P.append(f'''<section class="pg" style="background:{NAVY};color:#fff">
<svg viewBox="0 0 210 297" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">
<path d="M0 0h210v120c-40 26-78 8-118 22S30 170 0 150z" fill="{BLUE}"/>
<path d="M0 205c40-22 70-4 108-14s70-30 102-16v122H0z" fill="{BLUE}"/>
<path d="M0 232c44-18 76 2 112-8s66-26 98-14v87H0z" fill="{SKY}" opacity=".5"/>
<path d="M0 258c50-14 84 6 120-4s60-18 90-10v53H0z" fill="{SKY}"/>
<circle cx="182" cy="52" r="30" fill="none" stroke="{YEL}" stroke-width="9"/><circle cx="150" cy="200" r="9" fill="none" stroke="{GREEN}" stroke-width="4"/><circle cx="172" cy="214" r="4" fill="{CORAL}"/>
</svg>
<div style="position:absolute;left:20mm;top:20mm;background:#fff;border-radius:5mm;padding:4mm 6mm"><img src="{AS}peam-horizontal.png" style="height:17mm;display:block"></div>
<div style="position:absolute;left:20mm;right:20mm;top:84mm">
<div class="sans" style="font-weight:700;font-size:11pt;letter-spacing:.14em;text-transform:uppercase;color:{YEL}">Guia para educadores ambientais</div>
<h1 style="font-size:50pt;line-height:1;margin-top:6mm">Manual da<br>Exposição<br><span style="background:{YEL};color:{NAVY};padding:1mm 4mm 2mm;border-radius:2mm;display:inline-block;margin-top:3mm;margin-left:-4mm;white-space:nowrap">Marinha Itinerante</span></h1>
<p class="sans" style="font-size:14pt;line-height:1.4;margin-top:9mm;max-width:130mm;color:#e3ecf9">Um guia para monitores sobre a fauna marinha e como apresentá-la para diferentes públicos</p>
</div>
<div class="sans" style="position:absolute;left:20mm;bottom:20mm;color:{NAVY}"><div style="font-weight:800;font-size:13pt">Maiara Maia Borges</div><div style="font-size:9.6pt;font-weight:500">Programa de Educação Ambiental Marinha · LABOMAR/UFC</div></div>
</section>'''); STATE['n']+=1
# ---------- FOLHA DE ROSTO
P.append(f'''<section class="pg"><div class="body" style="top:40mm;text-align:left">
<div class="sans" style="font-size:12pt;font-weight:600;color:{INK}">Maiara Maia Borges</div>
<h1 class="tit" style="font-size:38pt;margin-top:46mm">Manual da Exposição<br>Marinha Itinerante</h1><div class="bar" style="margin-top:6mm"></div>
<p class="lead" style="max-width:120mm">Um guia para monitores sobre a fauna marinha e como apresentá-la para diferentes públicos</p>
<div class="sans" style="position:absolute;left:0;bottom:8mm;font-size:10pt;line-height:1.5"><img src="{AS}peam-horizontal.png" style="height:15mm;display:block;margin-bottom:5mm">1ª edição<br>Fortaleza · 2026</div>
</div>{foot(False)}</section>''')
# ---------- CRÉDITOS
P.append(f'''<section class="pg"><div class="body sans" style="top:30mm;font-size:8.8pt;line-height:1.55">
<p><b>© 2026 Maiara Maia Borges</b><br>Programa de Educação Ambiental Marinha (PEAM) · Instituto de Ciências do Mar (LABOMAR) · Universidade Federal do Ceará (UFC)</p>
<p><b>Autoria e concepção visual original</b><br>Maiara Maia Borges</p>
<p><b>Coordenação</b><br>Ravena Sthefany Alves Nogueira</p>
<p><b>Revisão técnica</b><br>Ravena Sthefany Alves Nogueira</p><p><b>Fotografias</b><br>Peças do acervo: Maiara Maia Borges<br>Aberturas de capítulo: Esponja, NOAA-OE; Água-viva, Neal Ziring; Caravela, NOAA/OER; Coral, Andy Collins/NOAA; Polvo, Albert Kok; Bivalves e Ermitão, National Park Service; Gastrópodes, Lagosta e Siri, NOAA; Ouriço, Laura Francis/NOAA; Camarão, USDA-ARS; Baleia, Robert Schwemmer/NOAA; Golfinho, NASA; Tartaruga, John Burns/NOAA; Tubarão, Ryan Eckert/NOAA; Arraia, Becky A. Dayhuff/NOAA; Cavalo-marinho, Mohammed Al Momany/NOAA; Peixe-morcego, NOAA/NURP; Peixe-cofre, ThC (todas em domínio público). Lula, Rickard Zerpe; Estrela-do-mar, Pedro Lastra/Unsplash; Baiacu, Di (CC0). Bolacha-da-praia, John Tracy (CC BY 2.0). Uçá: ilustração de Clara Costa D'Elia (CC BY 4.0). Imagens via Wikimedia Commons e bancos públicos. </p><p><b>Projeto gráfico desta edição</b><br>PEAM</p>
<div class="box" style="margin:6mm 0;display:flex;gap:5mm;align-items:center">
<div style="flex:none;font-weight:800;font-size:9pt;color:#fff;background:{INK};border-radius:2mm;padding:2.4mm 3mm;letter-spacing:.04em">CC BY-NC-ND 4.0</div>
<div>Esta obra está licenciada sob a <b>Creative Commons Atribuição-NãoComercial-SemDerivações 4.0 Internacional</b>. Você pode copiar e compartilhar este material, em qualquer formato, desde que dê o crédito à autora, não o utilize para fins comerciais e não o modifique. Licença completa: creativecommons.org/licenses/by-nc-nd/4.0/deed.pt-br</div></div>
<p><b>Como citar</b><br>BORGES, Maiara Maia. <b>Manual da exposição marinha itinerante</b>: um guia para monitores sobre a fauna marinha e como apresentá-la para diferentes públicos. Fortaleza: PEAM/LABOMAR/UFC, 2026. E-book.</p>
<div style="border:1px solid {INK};padding:5mm 6mm;margin-top:6mm;width:125mm;font-size:8.2pt;line-height:1.5"><div style="text-align:center;margin-bottom:3mm">Dados Internacionais de Catalogação na Publicação (CIP)</div><span style="color:#b4530a">[Espaço reservado para a ficha catalográfica, elaborada pela Biblioteca Universitária da UFC]</span><br><br>ISBN <span style="color:#b4530a">[a solicitar]</span></div>
<p style="margin-top:6mm">Distribuição gratuita. Venda proibida.<br>Contato: Instagram @peam_ufc</p>
</div>{foot(False)}</section>''')
# ---------- SUMÁRIO
def row(n,t,sub,p): return f'<div style="display:flex;align-items:baseline;gap:3mm;padding:1.5mm 0;border-bottom:1px solid #dfe7f1"><span class="sans" style="flex:none;width:8mm;font-weight:800;color:{SKY}">{n}</span><span style="flex:1"><b class="sans" style="color:{BLUE}">{t}</b>{f"<br><span style=&quot;font-size:9pt;color:#5b6b82&quot;>{sub}</span>".replace("&quot;",chr(34)) if sub else ""}</span><span class="sans" style="font-weight:700">{p}</span></div>'
P.append(plain('Sumário',''.join([row('','Como usar este guia','','5'),row('','ODS 14: vida na água','','6'),row('','Educação ambiental na prática','','7'),
 row('1','Esponjas','','8'),row('2','Cnidários','Água-viva, caravela e coral','13'),row('3','Moluscos','Polvo, lula, bivalves e gastrópodes','28'),row('4','Equinodermos','Estrela-do-mar, bolacha-da-praia e ouriço','49'),
 row('5','Crustáceos','Caranguejo-ermitão, caranguejo-uçá, camarão, lagosta e siri-azul','63'),row('6','Mamíferos marinhos','Baleias e golfinhos','84'),row('7','Tartarugas marinhas','','93'),row('8','Peixes cartilaginosos','Tubarões e arraias','98'),row('9','Peixes ósseos','Cavalo-marinho, peixe-cofre, baiacu e peixe-morcego','107'),row('','Carta da coordenação','','119'),row('','Checklist do monitor','','120'),row('','O público sempre pergunta…','','121'),row('','Glossário','','123'),row('','Para saber mais','','126'),row('','Referências','','127'),row('','Sobre a autora','','129')])))
# ---------- COMO USAR
def lvbox(k,txt):
    n,name,col,_=LV[k]
    return f'<div style="display:flex;gap:5mm;padding:4mm 0;border-bottom:1px solid #dfe7f1"><div class="num" style="background:{col};width:13mm;height:13mm;font-size:18pt">{n}</div><div><h3 style="font-size:13pt;color:{BLUE}">{name}</h3><p style="margin:1mm 0 0">{txt}</p></div></div>'
P.append(plain('Como usar este guia',f'''<p class="lead">Olá, jovem educador ambiental! Seja muito bem-vindo ao PEAM.</p>
<p>Dentro de pouco tempo você estará rodando toda Fortaleza (e, às vezes, até outros municípios) apresentando a exposição marinha itinerante para os mais diversos públicos e nos mais diversos contextos. Para sensibilizar as pessoas a conhecer e respeitar a biodiversidade marinha, é necessário que você esteja familiarizado com as peças que compõem a exposição. Cada uma pode ser apresentada de um jeito diferente e, como você vai descobrir, as informações que mais chamam a atenção variam bastante de acordo com o público.</p>
<p>O objetivo deste guia é preparar nossos educadores ambientais com diferentes níveis de informação e indicar formas de apresentar os materiais do acervo. Cada animal tem quatro páginas, sempre na mesma ordem:</p>
{lvbox('b','Informações simples, de vocabulário fácil, quase sempre com comparações com o cotidiano. Indicado para ==crianças menores (abaixo dos 10 anos)== e para adultos ou idosos que tiveram pouco ou nenhum contato com o oceano e sua biodiversidade.')}
{lvbox('m','Curiosidades que vão além do animal em si: aspectos ecológicos, ciclo de vida e papel no ecossistema. Indicado para pessoas de qualquer idade que não se contentam em saber o que é, mas querem entender ==como funciona==. É mais comum em crianças a partir dos 7 ou 8 anos e em adolescentes.')}
{lvbox('a','Informações mais técnicas, com vocabulário complexo (que você precisa saber explicar, caso a pessoa não pegue de primeira): anatomia, fisiologia e temas mais densos. Indicado para outros educadores e para ==quem estuda áreas ligadas ao oceano==. Também vale testar com pessoas muito curiosas ou com hiperfoco.')}
{lvbox('x','Fotos das peças do acervo, com o que observar em cada uma e dicas de como conduzir a apresentação com o material em mãos.')}'''.replace('{hl}',''),'Introdução')); P[-1]=hl(P[-1])
# ---------- ODS 14
ods=['Até 2025, prevenir e reduzir significativamente a poluição marinha de todos os tipos.','Até 2020, gerir de forma sustentável e proteger os ecossistemas marinhos e costeiros, respeitando os limites de resiliência, e tomar medidas para a sua restauração, a fim de assegurar oceanos saudáveis e produtivos.','Minimizar e enfrentar os impactos da acidificação dos oceanos, inclusive por meio do reforço da cooperação científica em todos os níveis.','Até 2020, regular a coleta e acabar com a sobrepesca, a pesca ilegal e as práticas de pesca destrutivas, implementando planos de gestão com base científica para restaurar populações de peixes no menor tempo possível.','Até 2020, conservar pelo menos 10% das zonas costeiras e marinhas.','Até 2020, proibir certas formas de subsídios à pesca que contribuem para a sobrecapacidade e a sobrepesca, e eliminar os subsídios que contribuam para a pesca ilegal.','Até 2030, aumentar os benefícios econômicos para os pequenos Estados insulares em desenvolvimento e os países menos desenvolvidos, a partir do uso sustentável dos recursos marinhos, inclusive por meio de uma gestão sustentável da pesca, da aquicultura e do turismo.','Aumentar o conhecimento científico, desenvolver capacidades de pesquisa e transferir tecnologia marinha, a fim de melhorar a saúde dos oceanos e aumentar a contribuição da biodiversidade marinha para o desenvolvimento dos países em desenvolvimento.','Proporcionar o acesso dos pescadores artesanais de pequena escala aos recursos marinhos e mercados.','Assegurar a conservação e o uso sustentável dos oceanos e de seus recursos pela implementação do direito internacional.']
P.append(plain('ODS 14: vida na água',f'''<p>Você já deve ter ouvido falar dos ODS, os Objetivos de Desenvolvimento Sustentável. Eles fazem parte da Agenda 2030, à qual aderiram, em 2015, os 193 países integrantes da Organização das Nações Unidas. Os ODS convocam diversos setores da sociedade (agentes governamentais, empresas, instituições e cidadãos) com o objetivo de criar um mundo mais justo, pacífico e sustentável, no qual meio ambiente, desenvolvimento econômico e bem-estar social estejam alinhados.</p>
<div class="box" style="margin:4mm 0"><p style="margin:0">Como PEAM, nossa missão está diretamente alinhada com o <b>ODS 14, vida na água</b>, que propõe a <mark>“conservação e uso sustentável dos oceanos, dos mares e dos recursos marinhos para o desenvolvimento sustentável”</mark>.</p></div>
<p>É interessante que, durante uma ação de educação ambiental, você vá além dos animais em si e tenha bagagem sobre o contexto global do cuidado com os oceanos. O ODS 14 se divide em metas que você deve conhecer:</p>
<div style="columns:2;column-gap:8mm;font-size:9.6pt;line-height:1.42">{''.join(f'<div style="display:flex;gap:3mm;margin-bottom:2.6mm;break-inside:avoid"><span class="sans" style="flex:none;width:6.4mm;height:6.4mm;border-radius:50%;background:{SKY};color:#fff;font-weight:800;font-size:8pt;display:flex;align-items:center;justify-content:center">{i}</span><span>{t}</span></div>' for i,t in enumerate(ods,1))}</div>''','Contexto'))
# ---------- EDUCAÇÃO AMBIENTAL
def tip(t,x): return f'<div class="card"><div class="dot" style="background:{SKY};color:#fff">✓</div><div><h3>{t}</h3><p>{x}</p></div></div>'
P.append(plain('Educação ambiental na prática',f'''<p>A Educação Ambiental é um aprendizado interdisciplinar essencial para a formação de cidadãos que respeitem, protejam e se integrem ao meio ambiente, e precisa ser estimulada desde cedo no ambiente escolar. Com a Política Nacional de Educação Ambiental (PNEA), Lei nº 9.795, de 27 de abril de 1999, ela passou a ser obrigatória em todos os níveis de ensino. A lei não exige uma “disciplina” própria: o tema deve ser abordado dentro de outras disciplinas ou de forma não formal, como é o caso das <mark>ações itinerantes do PEAM</mark>.</p>
{tip('Postura profissional','Ao entrar em um ambiente escolar, esteja uniformizado. Recomenda-se calça e sapato fechado. Coordenadores, professores e alunos estarão o tempo todo de olho em você.')}
{tip('É uma troca, não uma aula','Nunca apresente supondo que o público não sabe de nada. Quando menos se espera, aparece uma informação nova ou um relato de experiência que agrega ao momento.')}
{tip('Não invente respostas','Este guia contém muitas informações, mas sempre surgirão novas perguntas. Não há problema nenhum em dizer: “No momento não sei te dizer a resposta, mas vou pesquisar para a próxima vez”.')}
{tip('Deixe o público chegar à resposta','Quando vier o primeiro “o que é isso?”, você não precisa dizer o nome do animal e começar a dissertar sobre ele. Estimule as pessoas a chegar à resposta: elas se sentem mais motivadas a aprender e percebem que o conhecimento que trazem, seja de qual nível for, está sendo reconhecido.')}
{tip('Use a cultura popular','Sempre que possível, use filmes, comparações com o cotidiano, memes e até notícias recentes. Isso ajuda a criar um ambiente em que as pessoas se sentem confortáveis para tirar dúvidas.')}
{tip('Conecte com a sala de aula','Em contexto escolar, tente guiar a discussão pelas matérias ou assuntos que estão sendo tratados em sala. Você pode contar tanto com os alunos quanto com as professoras para saber o que foi visto recentemente.')}''','Antes de começar'))
# ---------- CAPÍTULOS
from content import C
def wc(items): return sum(len(re.sub(r'<[^>]+>','',t+' '+x).split()) for t,x in items)
def lvhead(k):
    n,name,col,who=LV[k]
    return f'<div style="display:flex;align-items:center;gap:4mm;background:{BLUE};color:#fff;border-radius:4mm;padding:3mm 5mm;margin:0 0 2mm"><div class="num" style="background:{col};width:11mm;height:11mm;font-size:16pt">{n}</div><div><h2 style="font-size:16pt;line-height:1">{name}</h2><div class="sans" style="font-size:8pt;color:#dbe7f8;margin-top:1mm">{who}</div></div></div>'
def figs2(items,intro=False,start=1):
    if len(items)<=3: return figs([(d['img'],d['t'],d['x'],d.get('marks')) for d in items],46 if intro else 58)
    hh=44 if len(items)>4 else 60
    o='<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm 7mm">'
    for i,d in enumerate(items,start):
        o+=f'<div style="break-inside:avoid"><div class="ph" style="position:relative"><img src="{IM}{d["img"]}" style="width:100%;height:{hh}mm;object-fit:cover;border-radius:3mm;display:block"><div class="tag">{i}</div>{marks(d.get("marks"))}</div><h3 style="font-size:1.05em;color:{BLUE};margin:2mm 0 .6mm">{d["t"]}</h3><p style="margin:0;font-size:.94em;line-height:1.4">{hl(d["x"])}</p></div>'
    return o+'</div>'
CH_START={}
for ch in C:
    CH_START.setdefault(ch['cap'],STATE['n']+1)
    STATE['run']=f"{ch['cap']} · {ch['grupo']}"
    prov=(f'<div class="sans" style="position:absolute;right:8mm;top:8mm;background:rgba(8,39,88,.6);color:#fff;font-size:6.6pt;border-radius:99px;padding:1.2mm 3mm">Foto: {ch["cred"]}</div>' if ch.get('cred') else '<div class="sans" style="position:absolute;right:8mm;top:8mm;background:rgba(242,111,113,.92);color:#fff;font-size:7.4pt;font-weight:700;letter-spacing:.06em;border-radius:99px;padding:1.6mm 3.4mm">FOTO PROVISÓRIA · A SUBSTITUIR</div>')
    P.append(f'''<section class="pg" style="background:{NAVY};color:#fff">
<img src="{IM}{ch['foto']}" style="position:absolute;left:0;top:0;width:100%;height:205mm;object-fit:cover;object-position:{ch.get('pos','50% 50%')}">{prov}
<svg viewBox="0 0 210 60" preserveAspectRatio="none" style="position:absolute;left:0;top:168mm;width:100%;height:60mm"><path d="M0 60V26c30-16 60-12 96-2s76 12 114-8v44z" fill="{SKY}" opacity=".6"/><path d="M0 60V36c34-14 66-8 100 0s72 8 110-8v32z" fill="{NAVY}"/></svg>
<div style="position:absolute;left:20mm;right:20mm;top:214mm">
<div class="sans" style="font-weight:700;font-size:10pt;letter-spacing:.14em;text-transform:uppercase;color:{YEL}">Capítulo {ch['cap']} · {ch['grupo']}</div>
<h1 style="font-size:58pt;line-height:1;margin-top:3mm">{ch['nome']}</h1>
<div style="display:flex;gap:3mm;margin-top:7mm">{''.join(f'<div class="sans" style="display:flex;align-items:center;gap:2mm;font-size:9pt;font-weight:600"><span style="width:7mm;height:7mm;border-radius:50%;background:{LV[k][2]};color:{NAVY};font-weight:800;display:flex;align-items:center;justify-content:center">{LV[k][0]}</span>{LV[k][1]}</div>' for k in [kk for kk in 'bma' if ch.get(kk)]+['x'])}</div>
</div><div class="foot" style="color:#b9c8e0"><span></span><span></span><span class="n">{STATE['n']+1:02d}</span></div></section>'''); STATE['n']+=1
    ks=[k for k in 'bma' if ch.get(k)]; i=0
    while i<len(ks):
        k=ks[i]
        if i+1<len(ks) and wc(ch[k])+wc(ch[ks[i+1]])<300:
            k2=ks[i+1]
            P.append(f'<section class="pg"><div style="position:absolute;left:0;top:0;width:100%;height:9mm;background:{BLUE}"></div><div class="sans" style="position:absolute;right:20mm;top:14mm;font-weight:700;font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:{BLUE};border:1.2px solid {BLUE};border-radius:99px;padding:1.4mm 3.6mm">{ch["nome"]}</div><div class="body fit" style="top:26mm">{lvhead(k)}{cards(k,ch[k])}<div style="height:5mm"></div>{lvhead(k2)}{cards(k2,ch[k2])}</div>{foot()}</section>'); i+=2
        else:
            P.append(level_page(k,ch['nome'],cards(k,ch[k]))); i+=1
    intro=f'<div class="box sans" style="font-size:.86em;line-height:1.45;margin-bottom:3mm"><b style="color:{BLUE}">Com a peça em mãos.</b> {hl(ch["x_intro"])}</div>' if ch.get('x_intro') else ''
    xs=ch['x']
    if len(xs)>6:
        h=(len(xs)+1)//2
        P.append(level_page('x',ch['nome'],intro+figs2(xs[:h],bool(intro))))
        P.append(level_page('x',ch['nome'],figs2(xs[h:],False,h+1)))
    else:
        P.append(level_page('x',ch['nome'],intro+figs2(xs,bool(intro))))
print('CH',CH_START)
exec(open('closing.py',encoding='utf-8').read())
html=f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Manual da Exposição Marinha Itinerante</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
open('out/piloto.html','w').write(html)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        await pg.goto('file://'+os.path.abspath('out/piloto.html')); await pg.wait_for_timeout(800)
        r=await pg.evaluate('''()=>[...document.querySelectorAll('.fit')].map(b=>{b.style.overflow='hidden';let f=10.2;b.style.fontSize=f+'pt';const a=[b.scrollHeight,b.clientHeight];while(f<13.4){b.style.fontSize=(f+0.2)+'pt';if(b.scrollHeight>b.clientHeight+1){b.style.fontSize=f+'pt';break}f+=0.2}b.style.overflow='visible';return [a,f]})''')
        print(r)
        await pg.pdf(path='out/Manual_Exposicao_Marinha_PEAM_parcial.pdf',prefer_css_page_size=True,print_background=True)
        await b.close()
asyncio.run(main()); print(len(P),'páginas')
