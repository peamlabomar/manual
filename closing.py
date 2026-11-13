# Fechamento do manual (executado dentro de build.py; usa plain, hl, P, STATE, cores)
PH='color:#b4530a'   # cor dos campos a confirmar
CL={}
def mark_start(k): CL[k]=STATE['n']+1
STATE['run']='Fechamento'

# ---------- CARTA DA COORDENAÇÃO
mark_start('carta')
P.append(plain('Para quem chega e para quem fica',f'''
<p class="lead">Querido educador, querida educadora ambiental,</p>
<p>Se este manual chegou às suas mãos, você agora faz parte do PEAM. E eu queria que você soubesse, logo de cara, uma coisa que eu repito sempre: o programa é feito pelas pessoas que passam por ele.</p>
<p>Cada visita, cada mesa montada numa escola, cada criança que toca pela primeira vez uma estrela-do-mar ou descobre que o golfinho respira pelo alto da cabeça só acontece porque alguém como você esteve ali. Esse encontro não sai de um roteiro decorado. Sai da escuta, da paciência e da coragem de dizer “não sei, mas vou descobrir”.</p>
<p>Este livro é a maior prova disso. Ele não foi escrito por um especialista distante: foi escrito por uma bolsista. A Maiara transformou a própria experiência nas ações em um material para preparar quem estava chegando. Pesquisou, escreveu, fotografou cada peça do acervo e pensou em como falar do mesmo animal com uma criança de cinco anos e com um estudante de biologia. Ver uma educadora em formação transformar a própria experiência em algo que vai formar tantas outras pessoas me enche de ==orgulho==.</p>
<p>É isso que eu espero de você também: que não seja só quem apresenta as peças, mas quem constrói o programa com a gente. Traga suas perguntas, suas ideias, seu jeito de explicar. Se descobrir uma curiosidade nova, anote. Se perceber que algo aqui pode ficar melhor, avise. Este manual está vivo, e as próximas edições também serão suas.</p>
<p>Obrigada por escolher cuidar do mar ensinando sobre ele. Boa jornada!</p>
<div class="sans" style="margin-top:7mm;line-height:1.4"><b style="color:{BLUE};font-size:1.05em">Ravena Sthefany Alves Nogueira</b><br>Coordenadora do Programa de Educação Ambiental Marinha (PEAM)<br>Instituto de Ciências do Mar (LABOMAR/UFC)</div>''','Carta da coordenação'))
P[-1]=hl(P[-1])

# ---------- CHECKLIST
def ck(items): return ''.join(f'<div style="display:flex;gap:3mm;padding:1.6mm 0;border-bottom:1px solid #e5ecf5;break-inside:avoid"><span style="flex:none;width:4.6mm;height:4.6mm;border:1.6px solid {BLUE};border-radius:1.2mm;margin-top:.9mm"></span><span>{hl(t)}</span></div>' for t in items)
def ckblock(n,col,tit,items): return f'<div style="margin-bottom:5mm;break-inside:avoid"><div class="sans" style="display:flex;align-items:center;gap:3mm;margin-bottom:1.5mm"><span style="width:8mm;height:8mm;border-radius:50%;background:{col};color:{NAVY};font-weight:800;display:flex;align-items:center;justify-content:center">{n}</span><b style="color:{BLUE};font-size:1.15em">{tit}</b></div>{ck(items)}</div>'
mark_start('checklist')
P.append(plain('Checklist do monitor',f'''<p>Uma lista rápida para conferir antes, durante e depois de cada ação. Vale imprimir, colar no caderno ou deixar salvo no celular.</p>
{ckblock(1,GREEN,'Antes de sair',[
'Combinei com a escola ou instituição o ==horário, o local e o número de pessoas==.',
'Sei a ==faixa etária== do público e, se for escola, o que a turma está vendo em sala.',
'Revisei neste manual os capítulos das ==peças que vão na exposição==.',
'Conferi as peças e as embalagens, e anotei o que está saindo do laboratório.',
'Estou uniformizado, de ==calça e sapato fechado==.',
'Levo pano ou toalha para forrar a mesa e algo para higienizar as mãos depois de tocar nas peças.'])}
{ckblock(2,YEL,'Durante a apresentação',[
'Monto a mesa com as ==peças mais frágeis longe da borda== e perto de mim.',
'Começo perguntando: “O que vocês acham que é isso?”. ==É uma troca, não uma aula==.',
'Ajusto o nível (Básico, Moderado ou Avançado) a cada grupo, e não à idade apenas.',
'Mostro como segurar cada peça antes de passar adiante. As mais delicadas, só eu manuseio.',
'==Não abro== frascos com animais conservados em líquido.',
'Se não souber uma resposta, digo que vou pesquisar e ==anoto a pergunta==.'])}
{ckblock(3,CORAL,'Depois',[
'Confiro se ==todas as peças voltaram== e guardo cada uma na sua embalagem.',
'Aviso a coordenação se alguma peça ==quebrou ou se perdeu==.',
'Registro o número de participantes, o público atendido e as perguntas que ficaram sem resposta.',
'Compartilho com a equipe o que funcionou e o que eu mudaria na próxima vez.'])}''','Apêndice'))

# ---------- O PÚBLICO SEMPRE PERGUNTA
FAQ=[
('Se uma água-viva me queimar, faço xixi em cima?','Não. Tire a pessoa da água, ==não use água doce nem gelo== (eles ativam os cnidócitos que ficaram na pele) e lave primeiro com ==água do mar== e depois com ==vinagre==, sem esfregar. Veja o capítulo Água-viva.'),
('Tubarão ataca gente?','Muito raramente: não fazemos parte da dieta deles. Em 2024, foram ==47 mordidas não provocadas== no mundo todo, 4 delas fatais. Nós matamos cerca de ==100 milhões de tubarões== por ano.'),
('Golfinho é peixe?','Não, é ==mamífero==: respira ar com pulmões, pelo alto da cabeça, e amamenta os filhotes. O mesmo vale para as baleias.'),
('Boto e golfinho são bichos diferentes?','Depende da região. O ==boto-cinza==, o mais comum no Ceará, é um golfinho; o nome muda de lugar para lugar.'),
('É verdade que o cavalo-marinho macho fica grávido?','É! A fêmea deposita os ovos numa bolsa na barriga do ==macho==, e é ele quem “dá à luz” os filhotes.'),
('Posso tirar a estrela-do-mar da água para tirar uma foto?','Melhor não. Ela respira pelas ==pápulas== da pele, e a exposição ao ar pode matá-la ==horas ou dias depois==, mesmo devolvida ao mar.'),
('Posso levar conchas ou bolachas-da-praia para casa?','O Ministério do Meio Ambiente orienta a ==não retirar== conchas da praia, e em áreas protegidas, como Jericoacoara, isso é proibido. A bolacha viva ==morre== fora do ambiente dela.'),
('Todo ouriço é venenoso?','Não. Existem espécies venenosas, mas não é o caso das que vivem no Ceará. Ainda assim, ==nunca pegue um ouriço sem proteção==: os espinhos machucam.'),
('E se eu pisar numa arraia?','Lave com soro e mergulhe a área em ==água quente (40 a 45 °C)==, o mais quente que der sem queimar. ==Não retire o esporão== se estiver preso e procure um hospital.'),
('Por que a tartaruga come plástico?','Porque ==sacolas plásticas== na água parecem ==águas-vivas==, um dos alimentos delas. O plástico se acumula no estômago, e o animal pode morrer de fome.'),
('A baleia solta água pelo nariz?','Não. O “esguicho” é o ar quente dos pulmões que ==condensa== ao sair pelo espiráculo, como a nossa respiração num dia frio.'),
('Como sei se a resposta deste guia ainda vale?','Ciência muda! Os números deste manual foram conferidos em 2026, e as fontes estão nas ==Referências==. Se encontrar algo novo, conte para a equipe.')]
def faq(items): return ''.join(f'<div style="padding:2.2mm 0;border-bottom:1px solid #dfe7f1;break-inside:avoid"><div class="sans" style="font-weight:700;color:{BLUE};margin-bottom:.6mm">“{q}”</div><div>{hl(a)}</div></div>' for q,a in items)
mark_start('faq')
P.append(plain('O público sempre pergunta…','<p>Algumas perguntas aparecem em quase toda ação. Aqui vão respostas curtas para ter na ponta da língua; os detalhes estão nos capítulos de cada animal.</p>'+faq(FAQ[:6]),'Apêndice'))
P.append(plain('O público sempre pergunta…',faq(FAQ[6:]),'Apêndice'))

# ---------- GLOSSÁRIO
G=[
('Ampolas de Lorenzini','Órgãos sensoriais no focinho de tubarões e arraias que captam os pequenos sinais elétricos produzidos por outros animais.'),
('Autotomia','Capacidade de soltar uma parte do corpo, como uma pata ou um braço, para escapar de um predador.'),
('Barbas','Placas flexíveis que as baleias-de-barbas têm no lugar dos dentes e usam como filtro para reter o alimento.'),
('Bioconstrutor','Organismo que forma estruturas usadas como base de um ecossistema, como corais e algumas esponjas nos recifes.'),
('Bioindicador','Espécie cuja presença, ausência ou condição indica a qualidade do ambiente.'),
('Branqueamento','Perda da cor de corais e esponjas quando, por estresse (como o calor), expulsam as algas que vivem em seus tecidos.'),
('Captura acidental','Animais pescados sem querer, quando o alvo da pesca era outra espécie. Também chamada de <i>bycatch</i>.'),
('Carcinicultura','Criação de camarões em cativeiro.'),
('Cnidócito','Célula dos cnidários (águas-vivas, caravelas, corais) que dispara uma estrutura com veneno, o nematocisto, ao ser tocada.'),
('Colônia','Conjunto de indivíduos ligados entre si que funcionam como um só organismo, como a caravela e os corais.'),
('Comensalismo','Relação em que uma espécie se beneficia de outra sem prejudicá-la.'),
('Cromatóforos','Células da pele de polvos e lulas que mudam de tamanho e permitem trocar de cor rapidamente.'),
('Defeso','Período em que a pesca ou a captura de uma espécie é proibida para proteger a reprodução.'),
('Ecolocalização','Uso de sons e de seus ecos para localizar objetos e presas, como fazem os golfinhos.'),
('Ectotérmico','Animal cuja temperatura do corpo depende do ambiente, como as tartarugas.'),
('Endêmico','Que só existe em uma determinada região.'),
('Endotérmico','Animal que produz o próprio calor e mantém a temperatura do corpo, como baleias e golfinhos.'),
('Espécie-chave','Espécie com papel tão importante que sua ausência altera todo o ecossistema.'),
('Espécie invasora','Espécie levada para fora da sua área de origem que se espalha e causa prejuízos ao novo ambiente.'),
('Espículas','Pequenas estruturas rígidas que formam o esqueleto das esponjas.'),
('Estuário','Encontro do rio com o mar, onde a água é salobra. Os manguezais ficam nesses ambientes.'),
('Exoesqueleto','Esqueleto externo, como a carapaça de caranguejos e lagostas, trocado durante a muda.'),
('Fendas branquiais','Aberturas por onde a água sai depois de passar pelas brânquias de tubarões e arraias.'),
('Filtrador','Animal que se alimenta retirando partículas e pequenos organismos da água.'),
('Gônadas','Órgãos que produzem as células reprodutivas (ovários e testículos).'),
('Lanterna de Aristóteles','Estrutura usada na alimentação de ouriços e bolachas-da-praia, com cinco dentes; é a “estrelinha” de dentro da bolacha.'),
('Madreporito','Placa porosa por onde a água do mar entra no sistema ambulacral dos equinodermos.'),
('Manguezal','Ambiente costeiro de transição entre a terra e o mar, berçário de muitas espécies.'),
('Medusa','Forma de vida livre e nadadora dos cnidários, com corpo em forma de sino.'),
('Muda','Troca do exoesqueleto que permite o crescimento dos crustáceos.'),
('Nácar','Camada brilhante na parte interna de algumas conchas; é o mesmo material das pérolas.'),
('Ovovivíparo','Animal cujos ovos se desenvolvem e eclodem dentro do corpo da mãe.'),
('Pápulas','Pequenas projeções na pele das estrelas-do-mar por onde ocorre a troca de gases.'),
('Pesca fantasma','Captura de animais por redes e outros equipamentos de pesca perdidos ou abandonados no mar.'),
('Pés ambulacrais','Pequenos “pés” cheios de água dos equinodermos, usados para se locomover, se fixar e capturar alimento.'),
('Petaloides','Estruturas em forma de flor na parte de cima das bolachas-da-praia, ligadas à respiração.'),
('Plâncton','Organismos que vivem à deriva na água, levados pelas correntes.'),
('Pleópodes','Pequenos apêndices sob o abdome dos crustáceos; nas fêmeas, seguram os ovos.'),
('Pneumatóforo','O “balão” cheio de gás que mantém a caravela na superfície.'),
('Pólipo','Forma fixa dos cnidários, com a boca e os tentáculos voltados para cima, como nos corais.'),
('Propulsão a jato','Movimento produzido ao expulsar água com força, como fazem polvos e lulas.'),
('Quelas','Pinças dos crustáceos.'),
('Séssil','Que vive fixo em um mesmo lugar, como as esponjas e os corais.'),
('Sistema ambulacral','Rede de canais cheios de água do mar que movimenta os pés ambulacrais dos equinodermos.'),
('Telômeros','Pontas dos cromossomos; a telomerase é a enzima que impede o seu encurtamento.'),
('Tetrodotoxina','Toxina muito potente presente no baiacu, capaz de causar paralisia.'),
('Vivíparo','Animal cujo filhote se desenvolve dentro do corpo da mãe e nasce já formado.'),
('Zona entremarés','Faixa do litoral que fica coberta na maré alta e descoberta na maré baixa.'),
('Zooxantelas','Algas microscópicas que vivem dentro dos tecidos dos corais e fornecem parte do seu alimento.'),
]
G.sort(key=lambda g:g[0].lower().replace('é','e'))
def glo(items): return '<div style="columns:2;column-gap:8mm">'+''.join(f'<div style="break-inside:avoid;margin-bottom:2.6mm"><b class="sans" style="color:{BLUE}">{t}</b><br><span style="font-size:.94em">{d}</span></div>' for t,d in items)+'</div>'
mark_start('glossario')
n=len(G); a=17; b=34
P.append(plain('Glossário','<p>Os termos técnicos que mais aparecem no manual, explicados de forma simples.</p>'+glo(G[:a]),'Pós-textual'))
P.append(plain('Glossário',glo(G[a:b]),'Pós-textual'))
P.append(plain('Glossário',glo(G[b:]),'Pós-textual'))

# ---------- PARA SABER MAIS
def sm(t,items): return f'<h3 class="sans" style="color:{BLUE};font-size:1.1em;margin:4mm 0 1.5mm">{t}</h3>'+''.join(f'<div style="padding:1.6mm 0;border-bottom:1px solid #e5ecf5"><b>{a}</b> {b}</div>' for a,b in items)
mark_start('saber')
P.append(plain('Para saber mais',f'''<p>Para continuar estudando e conferir informações novas, comece por aqui.</p>
{sm('Livros e materiais',[
('<i>Biologia marinha</i>.','PEREIRA, R. C.; SOARES-GOMES, A. (org.). 2. ed. Rio de Janeiro: Interciência, 2009. Referência em português para todos os grupos do manual.'),
('<i>Invertebrados</i>.','BRUSCA, R. C.; MOORE, W.; SHUSTER, S. M. 3. ed. Rio de Janeiro: Guanabara Koogan, 2018. Para aprofundar esponjas, cnidários, moluscos, equinodermos e crustáceos.'),
('<i>Cultura oceânica para todos</i>: kit pedagógico.','UNESCO, 2020. Ideias de atividades e os sete princípios da cultura oceânica, em português.')])}
{sm('Sites e aplicativos',[
('iNaturalist','(inaturalist.org): registre e identifique animais com fotos, com ajuda de especialistas.'),
('WoRMS','(marinespecies.org): nomes científicos atualizados de todas as espécies marinhas.'),
('FishBase','(fishbase.se): tamanho, distribuição e biologia de peixes, inclusive tubarões e arraias.'),
('ICMBio','(gov.br/icmbio): lista oficial de espécies ameaçadas e unidades de conservação do Brasil.'),
('International Shark Attack File','(floridamuseum.ufl.edu/shark-attacks): números anuais de incidentes com tubarões.')])}
''','Pós-textual'))

# ---------- REFERÊNCIAS
R={
'Introdução':[
'BRASIL. Lei nº 9.795, de 27 de abril de 1999. Dispõe sobre a educação ambiental, institui a Política Nacional de Educação Ambiental e dá outras providências. <i>Diário Oficial da União</i>, Brasília, DF, 28 abr. 1999.',
'NAÇÕES UNIDAS BRASIL. <i>Objetivo de Desenvolvimento Sustentável 14</i>: vida na água. Brasília: ONU Brasil. Disponível em: https://brasil.un.org/pt-br/sdgs/14.',
'UNESCO. <i>Cultura oceânica para todos</i>: kit pedagógico. Paris: Comissão Oceanográfica Intergovernamental, 2020.'],
'Esponjas':[
'JOCHUM, K. P. <i>et al.</i> Siliceous deep-sea sponge <i>Monorhaphis chuni</i>: a potential paleoclimate archive in ancient animals. <i>Chemical Geology</i>, v. 300–301, p. 143–151, 2012.'],
'Equinodermos':[
'ANIMAL DIVERSITY WEB. <i>Asteroidea</i>: sea stars. Ann Arbor: University of Michigan. Disponível em: https://animaldiversity.org/accounts/Asteroidea/.',
'CARNEIRO, L. S.; CERQUEIRA, W. R. P. Informações sobre o ouriço-do-mar <i>Echinometra lucunter</i> (Linnaeus, 1758) (Echinodermata: Echinoidea) para o litoral de Salvador e adjacências. <i>Sitientibus Série Ciências Biológicas</i>, Feira de Santana, 2008.'],
'Crustáceos':[
'ESTADO atual das exportações de lagostas no Brasil. <i>Research, Society and Development</i>, [2020]. Disponível em: https://rsdjournal.org/rsd/article/download/5804/4843.',
'IBAMA. <i>Plano de gestão da lagosta</i>. Brasília: IBAMA, 2006. Disponível em: https://www.gov.br/icmbio/pt-br/assuntos/centros-de-pesquisa/biodiversidade-marinha-do-sudeste-e-sul/acervo-digital/trabalhos-tecnicos/pub_2006_plano_gestao_lagosta-1.pdf.',
'IBGE. <i>Produção da Pecuária Municipal 2024</i>. Rio de Janeiro: IBGE, 2025.',
'KLAPPER, W. <i>et al.</i> Longevity of lobsters is linked to ubiquitous telomerase expression. <i>FEBS Letters</i>, v. 439, n. 1–2, p. 143–146, 1998.',
'MYERS, R. A.; WORM, B. Rapid worldwide depletion of predatory fish communities. <i>Nature</i>, v. 423, p. 280–283, 2003.',
'NOAA FISHERIES. <i>Fun facts about luscious lobsters</i>. Disponível em: https://www.fisheries.noaa.gov.',
'OCEANA BRASIL. <i>Lagosta</i>. Brasília: Oceana, [s.d.]. Folheto.',
'VOGT, G. A compilation of longevity data in decapod crustaceans. <i>Nauplius</i>, v. 27, e2019011, 2019.',
'Portaria Interministerial MPA/MMA nº 11, de 2024, que estabelece limite de captura para as lagostas-vermelha e verde.',
'Calendário de defeso do caranguejo-uçá 2024/2025 (portaria interministerial), conforme divulgado em O Imparcial, dez. 2024.'],
'Mamíferos marinhos':[
'CABALLERO, S. <i>et al.</i> Taxonomic status of the genus <i>Sotalia</i>: species level ranking for “tucuxi” (<i>Sotalia fluviatilis</i>) and “costero” (<i>Sotalia guianensis</i>) dolphins. <i>Marine Mammal Science</i>, v. 23, n. 2, p. 358–386, 2007.',
'FAHLMAN, A. <i>et al.</i> Conditioned variation in heart rate during static breath-holds in the bottlenose dolphin (<i>Tursiops truncatus</i>). <i>Frontiers in Physiology</i>, v. 11, 604018, 2020.',
'LYAMIN, O. I. <i>et al.</i> Cetacean sleep: an unusual form of mammalian sleep. <i>Neuroscience & Biobehavioral Reviews</i>, v. 32, n. 8, p. 1451–1484, 2008.',
'NOAA FISHERIES. <i>Humpback whale</i>. Disponível em: https://www.fisheries.noaa.gov/species/humpback-whale.',
'NATIONAL PARK SERVICE; MOTE MARINE LABORATORY; NOAA MARINE DEBRIS PROGRAM. <i>Decomposition times of marine debris</i>. Processado por Our World in Data, 2018.'],
'Tartarugas marinhas':[
'OLIVE RIDLEY PROJECT. <i>Can sea turtles breathe underwater?</i> Disponível em: https://oliveridleyproject.org.'],
'Peixes cartilaginosos':[
'AFONSO, A. S. <i>et al.</i> Evasive mating behaviour by female nurse sharks, <i>Ginglymostoma cirratum</i> (Bonnaterre, 1788), in an equatorial insular breeding ground. <i>Neotropical Ichthyology</i>, v. 14, n. 4, e160103, 2016.',
'FLORIDA MUSEUM OF NATURAL HISTORY. <i>International Shark Attack File</i>: yearly worldwide summary 2024. Gainesville: University of Florida, 2025.',
'MARTIN, R. A. <i>Speed of sharks</i>; <i>Teeth of the white shark</i>. ReefQuest Centre for Shark Research. Disponível em: https://www.elasmo-research.org.',
'MEDLINEPLUS. <i>Stingray</i>. Bethesda: U.S. National Library of Medicine. Disponível em: https://medlineplus.gov/ency/article/002853.htm.',
'WORM, B. <i>et al.</i> Global catches, exploitation rates, and rebuilding options for sharks. <i>Marine Policy</i>, v. 40, p. 194–204, 2013.',
'Mortes por ataques de cães no Brasil em 2023 (dados do Ministério da Saúde), conforme SBT News.'],
}
def refs(groups): return ''.join(f'<h3 class="sans" style="color:{BLUE};font-size:1.05em;margin:3.6mm 0 1.4mm">{g}</h3>'+''.join(f'<p style="margin:0 0 1.8mm;padding-left:5mm;text-indent:-5mm;font-size:.9em;line-height:1.38">{r}</p>' for r in R[g]) for g in groups)
mark_start('refs')
P.append(plain('Referências','<p style="font-size:.92em">Fontes consultadas na revisão técnica desta edição, organizadas pelo capítulo em que são usadas. Acesso aos endereços eletrônicos em novembro de 2026.</p>'+refs(['Introdução','Esponjas','Equinodermos','Crustáceos']),'Pós-textual'))
P.append(plain('Referências',refs(['Mamíferos marinhos','Tartarugas marinhas','Peixes cartilaginosos']),'Pós-textual'))

# ---------- SOBRE A AUTORA
mark_start('autora')
P.append(plain('Sobre a autora',f'''<div style="display:flex;gap:7mm;align-items:flex-start">
<img src="{IM}autora_maiara.jpg" style="flex:none;width:48mm;height:58mm;border-radius:4mm;object-fit:cover;object-position:50% 50%;border:1.5px solid {SKY}">
<div>
<p class="lead" style="margin-top:0">Maiara Maia Borges</p>
<p>É bióloga formada pela Universidade Federal do Ceará (UFC) e mestranda no Instituto Oceanográfico da Universidade de São Paulo (IO-USP). Foi bolsista do Programa de Educação Ambiental Marinha (PEAM), no Instituto de Ciências do Mar (LABOMAR/UFC), onde atuou como educadora ambiental na Exposição Marinha Itinerante.</p>
</div></div>
<p>Este manual nasceu da sua vivência nas ações do programa. Ao perceber, na prática, o que um educador precisa saber diante de cada público, Maiara reuniu o conhecimento científico sobre a fauna marinha e a escuta de quem ensina, e ==fotografou cada peça do acervo== que aparece nas páginas de Material.</p>
<p>Em sua trajetória, ciência e arte nunca estiveram separadas. O mesmo olhar atento que a levou à biologia se expressa na ==fotografia de natureza== e no ==trabalho artesanal==, linguagens pelas quais ela traduz em forma, cor e delicadeza o encantamento pela vida. É dessa sensibilidade que vem o cuidado presente em cada página deste livro: a convicção de que conhecer também é uma forma de afeto, e de que só se protege aquilo que se aprende a admirar.</p>
<div class="box sans" style="margin-top:6mm;font-size:.9em"><b style="color:{BLUE}">Acompanhe o trabalho dela:</b> @naturartista_273 (fotografia de natureza) · @holistica_artesanatos (ateliê)</div>''','Pós-textual'))
P[-1]=hl(P[-1])

# ---------- QUARTA CAPA
P.append(f'''<section class="pg" style="background:{NAVY};color:#fff">
<svg viewBox="0 0 210 297" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">
<path d="M0 0h210v70c-40 22-80 4-118 18S30 104 0 92z" fill="{BLUE}"/>
<path d="M0 232c44-18 76 2 112-8s66-26 98-14v87H0z" fill="{SKY}" opacity=".5"/>
<path d="M0 258c50-14 84 6 120-4s60-18 90-10v53H0z" fill="{SKY}"/>
<circle cx="28" cy="40" r="16" fill="none" stroke="{YEL}" stroke-width="6"/></svg>
<div style="position:absolute;left:24mm;right:24mm;top:96mm">
<div class="sans" style="font-weight:700;font-size:10pt;letter-spacing:.14em;text-transform:uppercase;color:{YEL}">Manual da Exposição Marinha Itinerante</div>
<p style="font-size:14pt;line-height:1.5;margin-top:6mm">Como apresentar uma estrela-do-mar para uma criança de cinco anos? E para um estudante de biologia? Este guia prepara os educadores ambientais do PEAM para mostrar ==25 animais== do acervo da exposição itinerante, com curiosidades em até três níveis de profundidade e dicas para conduzir a conversa com cada peça em mãos.</p>
<p class="sans" style="font-size:10.5pt;color:#dbe7f8;margin-top:6mm">Escrito e fotografado por uma bolsista do programa, é um convite para conhecer, respeitar e cuidar da vida no mar.</p>
</div>
<div style="position:absolute;left:24mm;bottom:20mm;display:flex;flex-direction:column-reverse;align-items:flex-start;gap:3mm">
<div style="background:#fff;border-radius:3mm;padding:3mm 4mm;display:flex;gap:5mm;align-items:center"><img src="{AS}peam-horizontal.png" style="height:10mm"><img src="{AS}labomar.png" style="height:10mm"><img src="{AS}ufc.png" style="height:10mm"></div>
<div class="sans" style="font-size:8pt;color:{NAVY};font-weight:700">CC BY-NC-ND 4.0 · Distribuição gratuita · Venda proibida</div></div>
<div style="position:absolute;right:24mm;bottom:20mm;width:42mm;height:24mm;background:#fff;border-radius:2mm;display:flex;align-items:center;justify-content:center;font-family:Inter;font-size:7.6pt;{PH};text-align:center">[código de barras<br>do ISBN]</div>
</section>''')
P[-1]=hl(P[-1]); STATE['n']+=1
print('CL',CL)
