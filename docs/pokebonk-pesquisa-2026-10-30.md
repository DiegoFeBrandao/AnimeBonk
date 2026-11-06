# PokeBonk — pesquisa complementar (2026-10-30)

Complementa `docs/pokebonk-referencia.md`. Aqui só está o que **não** estava anotado lá
(nem no §9 de `docs/megabonk-referencia.md`). Organizado por onde entraria no AnimeBonk.
Os nomes originais (Pokémon, PokeBonk, Megabonk) aparecem **só pra identificar a
mecânica**: nada disso entra no jogo. O AnimeBonk segue com tema ninja/anime **original**.

## Fontes e confiabilidade

- **[C] Cliente do jogo, v0.8.80 (2026-10-30)**: `https://pokebonk.com/assets/main-BMSEb-pX-mvur4p6p.js`
  (2,4 MB de código + textos). O idioma-fonte do jogo é **espanhol**. Os textos citados
  abaixo eu traduzi; os números (custos, tempos, chances) foram lidos direto do código.
  É a fonte mais exata que existe hoje: números de código, não de jogo testado.
- **[D] Pacote de dados do cliente**: `https://pokebonk.com/assets/defineProperty-DFY2V380-mvur4p6p.js`
  (biomas, Laboratório, itens, conquistas, visuais e **changelog completo 0.5.0 → 0.8.80**).
- **[MB] Guia megabonk.org**: https://megabonk.org/pokebonk/ (maps, survival, team-survival,
  lab, unlocks, multiplayer, updates, evolution, items-vitamins).
- **[DX] Dexerto**: https://www.dexerto.com/pokemon/pokemon-fan-game-turns-kanto-into-megabonk-in-your-browser-3419791/
- **Não encontrado**: wiki no Fandom, subreddit próprio, guias no YouTube, Trello público.
  As buscas por "PokeBonk wiki/altars/survival/reddit/tips" só devolvem a Dexerto, a Digg
  e o megabonk.org. O Discord oficial existe (link no jogo), mas não é público pra leitura.
- **Correção do pedido**: o PokeBonk **não é um jogo de Roblox**. É um fan-game de
  navegador (pokebonk.com, three.js/WebGL), gratuito, **sem anúncios, sem compras e sem
  doações** [DX]. Por isso **não existe loja de Robux** (nem de dinheiro real) pra comparar.

---

## 1. Mapa e objetos da partida

### 1.1 Quantos objetos de cada tipo aparecem por zona [C]

Tabela de geração do mapa (`populate`). `×área` = o número escala com o tamanho do mapa
(`n × (0,5 + 0,5 × multiplicador de área)`). Os objetos são espalhados assim: o jogo sorteia
30 pontos e fica com o **mais longe** de outros objetos do mesmo tipo e de marcos do cenário.
O altar do guardião fica **na borda** (entre 55% e 97% do raio).

| Objeto (nome original → função) | Clássico | Sobrevivência |
|---|---|---|
| Altar de bênção (Unown) | 5 ×área | 3 ×área |
| Altar "mais difícil, mais espólio" (Gengar) | 1 | — |
| Altar de desafio | 2 ×área | 1 ×área |
| Altar maldito | 1 | 1 |
| Ruínas do Fóssil (poder ↔ HP máx.) | 1 | 1 |
| Grito de Rhydon (chefe mais forte ↔ mais espólio) | 1 | — |
| Altar de Porygon (troca um stat por outro) | 1 | 1 |
| Máquina de fusão (Bill) | 1 | 1 |
| Ninho com Ovo | 1 | 1 |
| Mercador fixo (Meowth) | 1 | — (visita periódica, ver §4) |
| Clonador de item (Ditto) | 1 | 2 |
| Esquecedor (Hypno) | 1 | 1 |
| NPC dorminhoco (Snorlax: bênção ou dinheiro) | 2 | 1 |
| Ímã de XP (Magnemite) | 2 | 1 |
| Caça-níqueis | 2 ×área | 1 ×área |
| Bola grátis | 3 ×área | 2 ×área |
| Bola amaldiçoada (emboscada) | 2 ×área | 1 ×área |
| Jaula (soltar um bicho) | 2 ×área | — |
| Frutinhas (cura) | 5 ×área | 4 ×área |
| Bola paga (baú) | 14 ×área | 8 ×área |
| Rocha de ouro | 14 ×área | 8 ×área |
| Cogumelo saltitante | 3 ×área (só em mapa com relevo) | idem |

- O item "Dowsing Machine" soma, a partir da zona seguinte, **+1 altar de bênção e +2
  baús por zona** (máx. 2 cópias). No co-op os extras vêm de uma semente separada.
- **Primeiro elite da zona solta uma bola grátis** (aviso: "O primeiro elite da zona solta
  uma Poké Ball grátis!").

### 1.2 O que cada objeto faz (regras exatas) [C]

**Altar de bênção (Unown)**, o "Charge Shrine" do PokeBonk, com **5 tiers**:

| Tier | Carga (s) | Raio | Esvazia fora (s) | Ofertas / escolhas | Ondas de inimigos | Selado |
|---|---|---|---|---|---|---|
| Comum (ciano) | 8 | 6 | 6 | 3 / 1 | não | não |
| Raro (verde) | 14 | 5,5 | 5 | 3 / 1 (mín. raro) | não | não |
| Épico (roxo) | 22 | 5 | 4 | 3 / 1 (mín. épico) | 4 ondas | não |
| Dourado | 35 | 4,5 | 3 | **4 / 2** (mín. lendário) | 6 ondas | **selado até 1:30 da zona** ("Selado · desperta em N s") |
| Fragmento de cometa (azul, só Sobrevivência) | 10 | 6,5 | 3 | 3 / 1 | 2 ondas | dura 60 s e some |

- Tempo de carga × (1 + 0,25 × (zona − 1)): zona 3 carrega 50% mais devagar.
- Fica **ancorado** (a horda empurra menos) enquanto carrega. Sair um pouco não zera:
  depois de 1,2 s fora começa a esvaziar.
- Sorteio dos tiers por zona: ~15% épico (se houver ≥ 4 altares), ~30% raro, resto comum;
  chance de o primeiro virar **dourado** = mín(30%, 20% × √sorte).
- Épico/dourado têm **feixe de luz** visível de longe (beacon) e chamam ondas ("Os Unown
  chamam a horda! Aguente dentro do círculo").
- Co-op: vários jogadores no círculo carregam mais rápido (+60% por pessoa extra) e
  a bênção vale **pra todos** ("{nome} completou um altar! A bênção é de todos").
- Item "Secret Key": carrega 30% mais rápido e esvazia na metade da velocidade.
- A pausa tem uma aba **"Altares"**: o que cada altar deu, zona por zona, e o total (v0.8.52).

**Altar "mais difícil, mais espólio" (Gengar)**: uso único. **+20% dificuldade** pelo resto
da partida em troca de **+25% XP e +25% dinheiro**. Tem conquista por usar.

**Altar de desafio**: invoca um anel de **8 + 3 × zona** inimigos da mesma espécie em volta
do altar (os primeiros **1 + zona/2** são elite). Rótulo flutuante "Faltam N". Vencer →
"Desafio superado! Uma bola especial te espera no altar" (baú de raridade maior).

**Altar maldito**: uso único. **+15% inimigos e +10% dificuldade** pelo resto da partida
→ ganha **um item raro** na hora. Conquista "sofra 15 maldições numa partida".

**Ruínas do Fóssil**: reviver **um** de 3 fósseis, cada um custa **HP máx. permanente**:
- Fóssil A (−15% HP máx.): escolher entre **2 itens épicos ou melhores**.
- Fóssil B (−20% HP máx.): **bênção ancestral** (lendária ×1,5).
- Fóssil C (−25% HP máx.): um **companheiro** (pterossauro) luta com você o resto da partida.
- Conquista: reviver os 3 fósseis (em partidas diferentes).

**Grito de Rhydon**: só antes de invocar o guardião. Até **3 gritos**; cada grito deixa
o guardião com +% HP, +% dano e mais escoltas elite, e ao vencê-lo ele solta **+1 bola
especial por grito**. Depois que o guardião acorda: "Rhydon não responde". Conquista
"vencer um mapa após dar os 3 gritos de uma zona".

**Altar de Porygon (troca de stat)**: uma vez. Mostra cartas "um stat sobe / outro desce"
pelo resto da partida. Pares possíveis: dano +30%/−15%, vel. ataque +25%/−12%,
HP máx. +25%/−15%, velocidade +20%/−10%, crítico +15/−8 pontos, área +30%/−15%,
XP +40%/−20%, regeneração +2,5/−40%, armadura +20/−25%, duração +40%/−20%.

**Ninho com Ovo**: pega o ovo (só um por vez), ele **flutua orbitando você** e treme cada
vez mais. **Choca depois de 200 / 300 / 400 abates** (zona 1/2/3) → nasce um aliado
(espécie da horda da região) que luta com você; se o time de aliados estiver cheio, ele
"se despede e deixa um presente" (item).

**Clonador (Ditto)**: copia **um item seu** (não copia item que já está no máximo).

**Esquecedor (Hypno)**: esquece um **golpe ou vitamina** (libera o espaço pra outra build).
Não some depois de usado.

**NPC dorminhoco (Snorlax)**: frase aleatória engraçada; chance = mín(85%, 50% × sorte) de
dar uma **bênção**, senão dá dinheiro (máx(30 × zona, metade do preço do baú)).

**Ímã (Magnemite)**: puxa **toda** a XP do mapa por 5 s.

**Frutinhas**: cura 50% do HP (uso único; o arbusto fica apagado).

**Rocha de ouro** ("Golpe Rocha"): interagir quebra → dinheiro (6–14 × fator da zona),
15% × sorte de soltar power-up (cura, ímã ou bomba). Conta pra conquista.

**Jaula**: custa **20 + 10 × zona** de dinheiro. Solta um bicho da horda da região:
**+25 de pesquisa** da família dele (coleção) e **+50% da barra de XP** atual.

**Bola grátis**: abre de graça (tem feixe de luz azul que aparece de longe).
**Bola paga**: preço base 18 × curva que sobe **por baú comprado**; abre e deixa **escolher
1 de 3 itens** (desde v0.7.0). Itens "Big Nugget" baixam o preço até −40%.
**Bola amaldiçoada**: grátis, mas: 1 ou 2 itens (40% × sorte de vir 2), **+5% dificuldade**
permanente e **emboscada de fantasmas** (4 + 2 × zona, o primeiro é elite): "Era uma
armadilha!". Rótulo: "Abrir Poké Ball amaldiçoada (grátis... certeza?)".

**Caça-níqueis**: custo = máx(5, 40 × fator da zona × **1,08^giros** × desconto). Segurar
E gira sem parar e junta os prêmios numa bandeja (v0.8.61). Tabela (sorte aumenta só os bons):

| Resultado | Chance base | Efeito |
|---|---|---|
| 777 (jackpot) | 1,8% | 3 itens, um épico ou melhor (conquista própria) |
| Ícone do mascote | 5% | 1 item raro |
| Frutinha | 9% | cura 25% + 1 item |
| Moeda | 10% | devolve 2,5× o apostado |
| Bomba-viva (Voltorb) | 6% | solta 3 + zona inimigos explosivos em volta |
| Fantasma (Gengar) | 6% (com limite por partida) | maldição: +5% inimigos e +5% dificuldade |
| Nada | resto | rolos mostram combinação perdedora, com "quase" (2 iguais) frequente |

**Cogumelo saltitante**: pad de pulo (raio 1,4) apontado pra um alvo; só nos mapas com relevo.

**Máquina de fusão (Bill)**: uma fusão por máquina, escolhendo entre os pares prontos;
mostra tipo, físico/especial e números **antes** de fundir (v0.8.14). Solta faíscas
quando há par pronto (dá pra ver de longe). Na Torre aparece a cada 3 andares; no
co-op de Sobrevivência recarrega em 11 min.

**Tempos de regeneração na Sobrevivência** (objetos voltam depois de usados, v0.5.0):
altar 200 s · desafio 240 s · Snorlax 240 s · rocha 180 s · Ditto 150 s · ímã 150 s ·
frutinha 120 s · máquina de fusão no co-op 660 s.

### 1.3 Rótulos e marcadores dos objetos [C]

- Cada objeto tem um **rótulo flutuante** que aparece perto (6 m; NPCs a 18 m) e vai
  sumindo com a distância: altar mostra **% de carga** com a cor do tier; baú/jaula/
  caça-níqueis mostram o **preço em verde (dá pra pagar) ou vermelho**; desafio mostra
  "Faltam N"; altar dourado mostra "Selado · desperta em N s".
- Ícones do mapa com anel colorido e legenda: "Altar (bênção)", "Altar mais difícil, mais
  espólio", "Ditto (clona um item)", "Hypno (esquece golpes)", "Snorlax (bênção ou ₽)",
  "Ruínas (poder em troca de HP máx.)", "Rhydon (guardião mais forte, mais bolas)",
  "Porygon (troca um stat por outro)", "Ninho (choca lutando)", "Máquina (funde dois
  golpes no nível máx.)", "Caça-níqueis (aposta por itens)".

### 1.4 Eventos de mapa (diretor de hordas) [C]

**Hordas com aviso grande (banner)**, sorteadas em rodízio (embaralha as 4, usa todas
antes de repetir):
- **Enxame**: anel de 40 (zona 1, antes de 5 min) ou 46 + 12 × zona inimigos a 26 m
  em volta, com 60% do HP normal.
- **Estouro de manada**: manada correndo em linha ("saia do caminho").
- **Revoada**: bando voador cruzando o céu.
- **Chuva de rochas**: círculos marcados no chão; quem estiver dentro leva dano; algumas
  rochas viram inimigos.

**Inimigos especiais (minichefes)**:
- **Alfa** ("um X gigante e furioso apareceu"): forma evoluída, mais forte; capturável
  como apoio.
- **Dominante** (totem): aura poderosa, chama a própria espécie. Ao vencer: **bênção**,
  bola grátis e 10 moedas. Não dá pra salvar a partida com ele vivo.
- **Invocador**: fica parado chamando reforços e **vai embora** se você demorar
  ("encontre-o antes que vá embora"). Ao vencer: todos os lacaios desmaiam junto + doce
  raro (sobe 1 nível) + 8 moedas.

**Eventos de atmosfera** (um de cada por partida, sem chefe vivo):

| Evento | Duração | Regra |
|---|---|---|
| Névoa espectral | 45 s | visão curtíssima, fantasmas na névoa |
| Tempestade elétrica | 40 s | raios caem em marcas amarelas no chão |
| Eclipse | 40 s | escurece, saem inimigos noturnos (+12% elite) e **chance de shiny** |
| Mascote dourado (Meowth) | 25 s | inimigo que **solta moedas a cada golpe** e foge se não morrer; morto = chuva de 30 moedas ("Dia de Pagamento!") |

**Eventos e perigos por região** [C][D]:
- **Floresta**: clima limpo/limpo/chuva nas zonas 1/2/3.
- **Deserto**: limpo / **tempestade de areia** / **sol**.
- **Costa da Tormenta**: **maré** que sobe e inunda as praias (água te freia; platôs e
  ilhotas de para-raios ficam secos) e, ao baixar, **deixa pérolas na areia**; **tromba
  d'água** que te arremessa por cima da horda; chefe com **mar eletrificado**; **para-raios**
  que absorvem o golpe do chefe.
- **Geleira Celeste**: **granizo** (dano e congela inimigos aos poucos), **nevasca** (vento
  te empurra, visão baixa, abrigue-se atrás de rochas), **lagos de gelo que escorregam**,
  chefe "frio absoluto" (ir pros setores de borda dourada), chefe congelável com o próprio raio.
- **Torre (evento)**: névoa. **Ilha Vulcão** (anunciada): rios de lava e **cinzas**.
- Cada região tem **3 guardiões possíveis por zona**, **4 Dominantes possíveis por zona** e
  **2 Invocadores por zona**, todos diferentes por região [D].

**"Dia e noite" por zona** [D]: cada região muda a iluminação/céu a cada zona (ex.:
Floresta zona 2 "Tarde dourada", zona 3 "Crepúsculo" com vaga-lumes; Deserto "Calima" →
"Ocaso"; Costa "Pôr do sol tropical" → "Noite de tempestade"; Geleira "Tarde gelada" →
"Aurora"). É progressão visual que mostra que a run está avançando. O santuário tem céu,
névoa e **música própria** (escala/bpm definidos por região).

**Mudança de clima no meio da zona**: aviso "O clima muda: {clima}!"; clima dá +30% a
certos tipos e −25% a outros. Golpes de clima existem (o jogador muda o clima).

**Anti-campar ("Cerco!")** [C]: se você fica parado ou num raio pequeno por muito tempo,
aparece um anel vermelho e os inimigos **resistem aos seus golpes** ("Se você não se
mexer, os selvagens resistem. Saia do círculo!"); acima de 45 s parado ainda chegam
bandos. Mexer quebra o cerco.

**Enxame final** (zona passou de 10:00): spawns ×6 e elites extras sem parar, banner
"ENXAME FINAL! Você não deveria continuar aqui...".

**Ritmo de spawn** [C]: teto de inimigos vivos = (10 + 0,65 t + 4,5 (t/60)²) × (1 + 0,6 ×
(zona−1)) × fator da dificuldade; até 1.800 spawns/s. Fase da zona: "Fase 2: a horda
evolui (chegam formas evoluídas)", "Fase 3: as formas finais saem pra caçar".

**Tempo de chefe**: guardiões e lendários que duram demais **se cansam e recebem cada
vez mais dano** (v0.5.2) — anti-luta-infinita.

---

## 2. Personagens

- **Evolução por nível na partida** [MB]: os iniciais evoluem nos níveis **24 e 41/44**;
  um personagem com várias evoluções abre **menu de escolha de ramo**. O cliente calcula
  os limiares a partir dos dados da espécie, com exceções por personagem.
- **Regra exata dos kits compartilhados** [C]: "Os membros da sua Liga que **compartilham
  tipo** com ele **ensinam os ataques desse tipo ou do tipo Normal**." A ficha mostra
  "Ensinado por" e "Ninguém da sua Liga ensina nada ainda". A **fusão de assinatura** (2
  golpes do kit de um membro) vale mesmo se você aprendeu os golpes por kit compartilhado.
- **Depois de aprender tudo** [C]: banner "Treinamento! Você já aprendeu tudo: cada nível
  agora dá um bônus pequeno e permanente" (decresce, mínimo 1/3 do primeiro).
- **Vínculo dos aliados** [C]: aliados (Alfas de apoio) ganham **Vínculo** por abates; cada
  nível de vínculo = **+10% de dano** ("{nome} confia mais em você! Vínculo 2 (+20% dano)").
- **Shiny** [C][D]:
  - Shiny normal + **"shiny clássico"** (raríssimo, brilho dourado) que desbloqueia o
    visual da linha inteira.
  - Lendários têm **chance de shiny por conta que sobe a cada tentativa** até garantir
    (v0.8.77) — "pity timer".
  - Capturar um 2º shiny na mesma partida: você escolhe **qual soltar** (limite de vagas).
- **Desafios de desbloqueio** [MB]: contadores cumulativos ou "numa partida só", ex.:
  dormir 1.500/4.000/8.000 inimigos (cumulativo), dormir 1.500 numa partida, queimar
  6.000 (cumulativo) ou 6.000/8.000 numa partida, curar 7.000 HP numa partida. Conta
  **inimigos distintos** afetados, não golpes. Iniciais: "complete 2 partidas".
  Depois do desafio, o personagem aparece no mapa num **"Encontro selvagem"** com seta na
  tela; lendários entram só de enfraquecer.
- **Visuais com shader** [D] (Guarda-roupa, maestrias): Game Boy (4 tons), Magma, Cristal,
  Metal, Holográfico, Sombra, Galáxia, Neon, Estátua, **Tinta (pincelada no papel)**,
  Chama, Aurora, Brasa viva, Selva viva, Maré profunda. Cada um é um efeito de material
  sobre o mesmo sprite: muito conteúdo cosmético com pouca arte nova.
- **Passivas de habilidade com mecânica de movimento** [C]: várias passivas mexem no
  movimento: levitar (planar segurando pulo e **subir paredes**), +1 pulo, dano extra no
  ar (+25%), bônus com clima (com chuva +30% velocidade), botar ovo de cura a cada 10 s,
  baga que nasce do lado a cada 15 s, pêndulo que faz dormir 3 inimigos a cada 7 s,
  inimigos derrotados com 12% de explodir.

---

## 3. Golpes, vitaminas e itens

### 3.1 Golpes [C][MB]
- Taxonomia de formas já está na referência. Novidades achadas:
  - Ultimates e golpes de fusão têm **"Maturidade"** (versão mais forte com o nível).
  - Exemplos de comportamento descritos: jaula de raios (prende o grupo 1,1 s e o raio cai
    no fim); caixa de cristal (paredes invisíveis prendem e explodem); chuva de ovos;
    cogumelos que nascem onde o projétil cai e soltam esporos de sono; 12 cometas que
    racham o chão; coroa de 3 anéis de lâminas giratórias; socos que perseguem e ficam
    mais fortes quanto **menos vida** você tem.
  - **Golpes de clima e de potencialização não podem ser fundidos**; fusões já feitas
    também não.
  - Golpe "Metrônomo" e a mutação do mesmo nome trocam golpes aleatoriamente.
- **Fusão-glitch** (qualquer par que não bate receita) tem conquista própria ("Falha na
  máquina").

### 3.2 Vitaminas — nada novo além da referência (26, níveis 1–10/12).

### 3.3 Itens com efeito ativo ou que mudam regra [D]

| Raridade | Item (original) | Efeito |
|---|---|---|
| Comum | Soda Pop | ao **deslizar**, onda de bolhas que causa dano e molha |
| Comum | Berry Juice | 5% por abate de curar 2% |
| Incomum | Old Rod (vara) | a cada 9 s pesca um peixe que cai num inimigo e molha; às vezes vem um peixe-dragão (conquista) |
| Incomum | Secret Key | altares carregam 30% mais rápido |
| Incomum | Gold Teeth | mercador, reroll e caça-níqueis −8% (até −24%) |
| Incomum | Smoke Ball | 25% ao apanhar de ficar invisível 1,5 s |
| Raro | Dowsing Machine | +1 altar e +2 baús por zona |
| Raro | Razor Fang | executa inimigos (não chefes) abaixo de 8% HP |
| Raro | Iron Ball | ao cair de um pulo, onda sísmica que cresce com a armadura |
| Raro | Guard Spec | a cada 14 s bloqueia o próximo golpe inteiro |
| Raro | Bicycle | +1% dano a cada 2% de velocidade extra |
| Épico | Focus Sash | sobrevive a um golpe letal **uma vez por fase** |
| Épico | Thunder/Fire/Ice/Leaf Stone | crítico solta raio; queimados explodem; congelados estilhaçam; abates soltam redemoinho de folhas que cura |
| Épico | Electirizer | a cada 2,5 s raio em 3 inimigos |
| Épico | Griseous Orb | 12% dos abates deixam sombra que explode e amaldiçoa |
| Épico | Reaper Cloth | +1% dano a cada 100 abates (até +30%) |
| Épico | Silph Scope | a cada 6 s marca o inimigo mais forte: +40% dano recebido |
| Épico | Rage Candy Bar | até +60% dano com ≤ 25% HP, −25% cura |
| Épico | Revive | revive 1× com 35% |
| Épico | Max Ether | vitaminas até nível 12 |
| Lendário | Max Revive | revive 1× com 60% (até 3) |
| Lendário | Rainbow Wing | **1× por zona**, ao cair renasce em chamas com 50% HP, 3 s invulnerável e explosão de fogo |
| Lendário | TM Case | golpes até nível 10, fusões até ★6 |
| Lendário | Poké Flute | ultimate +25% mais rápida; ao lançar, recarrega todos os golpes e +30% vel. ataque 6 s |
| Lendário | Adamant Orb | ao apanhar, **para o tempo** dos inimigos próximos 3 s (cada 20 s) |
| Lendário | Lustrous Orb | a cada 8 s abre uma fenda que puxa inimigos e explode |
| Lendário | Sun Stone | a cada 6 s raio solar no inimigo mais forte |
| Lendário | Silver Wing | a cada 5 s rajada de vento que empurra quem está em volta |
| Lendário | Master Ball | +25% dano e captura garantida nos encontros |
| Lendário | Rare Candy | sobe 2 níveis na hora + 5% dano |

- **Item no plano de build**: até 6 itens marcados "No seu plano" aparecem destacados nos
  baús e na loja (v0.8.44).
- Pokédex tem aba de itens: o que faz, se está desbloqueado ou arquivado.

### 3.4 Power-ups no chão [C]
XP em **4 tamanhos** de doce (valor ≥ 4, ≥ 12, ≥ 40), moeda, cura (25%), **ímã** (puxa toda a
XP), **bomba** (limpa a tela), **repelente**, **doce raro** (+1 nível), **chave de baú** e 5
"MTs" temporários: dano, velocidade, defesa, paralisia em volta, **chuva de moedas**.
Pegar outro MT só **renova a duração** (não soma). Stat "Power-ups" multiplica chance,
encurta espera e alonga duração.

### 3.5 Sequência de abates (streak) [C]
Janela de **3 s** entre abates. Marcos **10, 25, 50, 100, 150, 200, 300, 400, 500, 750, 1000**:
cada marco paga dinheiro; a partir de 25 também **ímã de XP**; a partir de 50 também
**cura 15%** ("Sequência ×50! +X ₽ · ímã · +15% HP"). "Melhor sequência" vai pra pausa e
pro fim de partida.

---

## 4. Partida

### 4.1 Clássico
- Tela de entrada da zona: "Região · Zona n/3" + título ("Sobreviver!", "Zona profunda",
  "Covil lendário") + linha da dificuldade ("Difícil: mais inimigos, mais rápidos e mais
  elites; os chefes avisam menos" / "Pesadelo: hordas maiores, **elites que explodem ao
  morrer** e chefes sem piedade") [C].
- **Split por zona**: ao trocar de zona aparece o tempo da zona e a diferença pro seu
  recorde ("Primeiro tempo" / −0:12 em verde / +0:30) [C].
- Depois de vencer o guardião: **o mapa marca tudo que falta pegar**; recompensas do chefe
  caem longe do portal e o portal **pede confirmação** se você deixou alguma pra trás
  (v0.8.17).
- **Música**: 4 temas sorteados por partida; chefes lendários têm tema próprio.

### 4.2 Sobrevivência (o que faltava) [C][D]
- Mapa "aberto", objetos **se regeneram** (tempos no §1.2).
- **Visita do mercador**: chega aos 3:30 e depois a cada 5 min, fica **45 s** ("O mercador
  veio com a loja! Vai embora em 45 s").
- **Suprimentos do céu**: a cada 55–75 s caem bolas e itens.
- **Cometas** a cada ~150 s: fragmento-altar azul que dura 60 s, carrega em 10 s e chama
  2 ondas.
- **Portal de migração** aos **11:00**: "Atravesse em N s pra chegar a terras novas, com
  tudo pra descobrir" → mapa novo, a horda vem junto.
- **Terreno hostil**: lama, espinheiro, areia movediça, chão em chamas.
- **Feridas profundas**: a partir de certo ponto você **cura menos a cada minuto**.
- **Noite Sem Fim** (solo, 45:00): cada minuto os inimigos ficam mais fortes, elites
  contínuos. **Cataclismo** e **Apocalipse** (equipe): timer na tela "Cataclismo em 3:12".
- **Pactos** (escolher 1 depois de cada chefe de marco, pode recusar; cada pacto até 1–2×):

| Pacto | Bônus | Maldição |
|---|---|---|
| da Horda | 1 item épico ou melhor | +25% inimigos |
| de Ferro | 1 item lendário | inimigos +35% HP |
| de Fúria | +25% dano | inimigos +25% dano |
| do Vento | +15% velocidade e +1 pulo | inimigos +12% velocidade |
| de Elite | +30% XP e +20 sorte | o dobro de elites |
| da Lua | sobe 3 níveis na hora | um Alfa a cada 90 s (era 150 s) |
| Ganancioso | dinheiro na hora e +30% dinheiro | baús +50% mais caros |
| de Cristal | +40% dano crítico e +10% crítico | −20% HP máx. |
| Espinhoso | +1 espaço de vitamina | −30% cura |

- Conquista "Noite sem fim": vencer o chefe do minuto 45.

### 4.3 Mutação do Dia (exemplos com regra) [MB][C][D]
- **Metrônomo** (Pesadelo): a cada 30 s um golpe (não o 1º, não fusão) vira outro aleatório
  da Liga inteira, mesmo nível. HUD mostra "golpe velho → golpe novo".
- **Selvagens gigantes** (Dynamax): 2× tamanho e HP, +50% dano, 15% mais lentos.
- **Febre de Doces** e **Cristal**: nomes confirmados no calendário; regras exatas
  **não encontradas** (as mutações vêm do servidor, não estão no cliente).
- Stardust 1×/dia: 60 (zona 2) + 60 (zona 3) + 60 (santuário) + 120 (vitória) = 300.
  Premiações permanentes: título (zona 3), moldura (santuário), fundo de perfil (vitória);
  4 fundos = título "Rei das Mutações". Splash na entrada com medalha, nome e regra.

### 4.4 Evento de temporada (Torre) — conquistas novas [D]
"Calme o fantasma no andar 6", "Vença o chefe no andar 7", "Chegue ao andar 15 / 25"
(Além), "Passe o andar 4 sem acender vela", "Revele 300 fantasmas com o visor",
"Sobreviva a 10 travessuras das lápides". Na Torre **não dá pra salvar**. Travessuras das
lápides: maldição (+6% dificuldade), emboscada, roubo de dinheiro, ou prêmio.

### 4.5 Dificuldades
Já na referência (×1 / ×1,75 / ×2,5 Stardust). Extra [C]: o Pesadelo faz **elites
explodirem ao morrer**; o Difícil reduz o **aviso** dos golpes de chefe.

### 4.6 Tela de fim de partida [C]
- Cabeçalho: "Você sobreviveu {tempo}" / "Sua equipe aguentou {tempo}" / "Chegou ao andar N".
- Números: Tempo, Abates, Dano, Pontos; **Stardust** ganho; Bonkoins ("pras roletas").
- Blocos: **Sua partida** (melhor sequência, reações, evoluções, golpes recebidos, pactos,
  marcos, lendários) · **Dano por golpe** · **Capturados!** (com aviso "se une à sua Liga"
  e o visual shiny ganho) · **Alfas que te acompanharam** · **Tarefas completadas** (resgatar
  na aba) · **Pokédex**: espécies, quantas novas, "NOVO", abates por espécie ·
  **Caderno de pesquisa**: famílias completadas ("já pode usar como avatar") ·
  **Classificação**: "Novo recorde!", "Você entrou no top N", "Ultrapassou {nome} · agora
  você é #N", "Fora do top N" · co-op: dano por jogador e a equipe.
- Atalhos: **Enter = jogar de novo**, Esc = menu.
- "Partidas de menos de 1 minuto" não entram no histórico/ranking (mas contam progresso).

### 4.7 Segundo fôlego / reviver [C][D][MB]
- **Laboratório "Reviver"** (4.250 Stardust): começa toda partida com um Max Revive.
- Itens: Revive (35%), Max Revive (60%, até 3), Rainbow Wing (1×/zona), Focus Sash
  (1×/fase). HUD: "Reviver disponível: N"; banner "Você foi derrotado e volta à luta · mais
  N na mochila".
- **Co-op**: caído, companheiro segura E ao lado ("[E] Segure pra reanimar {nome}"),
  janela de **60 s** (v0.8.45); quem reanima vê barra; aviso "estavam te reanimando: não
  deixe ele se afastar". Na Sobrevivência em equipe: quem não foi reanimado **volta
  quando a equipe vence o próximo chefe**. Caído **não causa dano**.
- **"End Match / Revive All" pago: não encontrado** (não existe; o jogo não tem compras).
- **Pausa de equipe** (v0.8.77): P pede pausa, todos aceitam, **5 min de pausa por
  partida**, retoma quando todos votam.
- **Bolha do level-up no co-op** (v0.8.77): reserva de **45 s**, +15 s por nível (máx. 90),
  recarrega devagar; reroll/banir/pular não gastam.

---

## 5. Menu e meta

### 5.1 Laboratório — lista completa e preços [D][MB]
| Melhoria | Efeito | Níveis | Custo |
|---|---|---|---|
| 4º golpe | 3 → 4 slots | 1 | 1.275 |
| Espaços de vitamina | +1 por nível | 2 | 1.020 → 2.550 |
| Atualizar (reroll) | +1 uso | 6 | 100 → 550 (1.665 total) |
| Pular | +1 uso (dá dinheiro) | 6 | 70 → 365 (1.110) |
| Banir | +1 uso | 6 | 130 → 685 (2.085) |
| Quarta opção | 4 cartas no level-up | 1 | 2.550 |
| Treino / Resistência | +4% dano / +8 HP por nível | 8 | 85 → 895 (2.920) |
| Agilidade | +2,5% velocidade | 6 | 100 → 655 (1.880) |
| Estudo, Comércio, Fortuna, Magnetismo, Restos, Couraça, Precisão, Celeridade, Expansão | XP, dinheiro, sorte, coleta, regen, armadura, crítico, vel. ataque, área | vários | curva parecida |
| **Sintonia** | ultimate carrega +4% por nível | — | — |
| **Reviver** | começa com Max Revive | 1 | 4.250 |
| **Pesquisa** | +25% progresso do caderno por nível | — | — |
| **Equipe de apoio** | +1 vaga de Alfa (2 → 3) | — | — |
| **Arquivo** | +5 vagas por nível (+1 a cada 2 itens desbloqueados) | — | — |
| **Mochila grande** | leva 3 itens pra partida (em vez de 2) | 1 | — |

Dica do próprio jogo: "comece pelo 4º golpe, depois reparta entre Atualizar, Pular e o
Treino". Total: 24 melhorias, 111 níveis.

### 5.2 Conquistas de desafio (lista exata) [D]
Minimalista (≤ 3 itens), Sem vitaminas, Intocável (≤ 20 golpes), Por um fio (< 10% HP),
Asceta (Pesadelo ≤ 3 itens), Espelho de gelo (congelar o chefe com o próprio raio), Rhydon
furioso (3 gritos), Assinatura própria (fusão de assinatura do inicial), Paleontólogo (3
fósseis), Toda a Liga, Colecionador de itens, Jackpot (777), Maldição (15 numa partida),
**"Bonk!"** (finalizar chefe com o golpe de 4% ×8 do item-piada), "Viu chegar" (morrer pra
um chefe específico), Falha na máquina (fusão-glitch), "Fisgou algo!" (pescar o peixe
raro), Mel (+1 Alfa por zona). Todas giram em torno de **objetos do mapa** e **builds
extremas** — barato de fazer e gera história.

### 5.3 Social, ranking e outros [C][D]
- **Chat da sala** com frases rápidas e balão sobre o cartão (some ao começar) (v0.8.29).
- **Roda de sinais** (G): Aqui!, No chefe!, Olha isso!, No portal!, Valeu!, Esperem!,
  Cuidado!, Ajuda! — cada um se posiciona sozinho.
- Matchmaking: líder com **60 s** pra começar (caiu pra **30 s** na v0.8.85, conferido em 2026-11-05), senão perde a liderança; aviso aos 20 s;
  busca solo cancela após 3 min parado; prioriza a sua região.
- Ranking: perseguir **cada rival um por um** (#50, #49...) em vez de saltos; "Tope da
  tabela: 6 h" na Sobrevivência; títulos por personagem ("Mestre de X", "Lenda de X").
- Clãs: requisitos de entrada (personagens, vitórias, idade da conta, posição), aba
  **Guia** (regras do líder), liderança passa sozinha após 7 dias offline, comunicado
  fixado 7 dias (1 por hora), recompensas por estrela de missão (até 2.000 Stardust +
  item; 3ª estrela 1 Bonkoin), vitória na rivalidade (1.500 + 2 Bonkoins + bola mestre),
  3 molduras de clã com título, prêmio de temporada pra quem fez ≥ 500 pontos e ≥ 1/4 da
  média.
- **Anti-cheat público**: notas de versão listam contas suspensas, denúncias revisadas e
  **suspensões injustas revertidas** (transparência = confiança no ranking).
- **Recuperação**: se a partida não chega a começar, os itens de Mochila gastos voltam
  horas depois.
- **Tarefas**: base já tem; extra: streak paga de 11 a 40 Stardust conforme os dias.
- **Loja de Robux/dinheiro**: não existe (ver "Fontes").

### 5.4 Configurações extras (não estavam na referência) [C]
Limite de FPS (sem limite/30/60/90/120/144), brilho dos efeitos, reduzir clarões,
"doces discretos" (sem rastro ao coletar), coleta simples, ocultar itens do canto, tema
claro/escuro/automático (dark mode em toda a HUD), som no iPhone mesmo no silencioso,
zona morta do controle, tecla de pausa remapeável, aviso quando o navegador está sem
aceleração de hardware (baixa a qualidade sozinho).

---

## 6. HUD e UX [C][D]

- **Carteira no topo-centro**: dinheiro grande e, na mesma linha, **o preço atual do baú,
  do caça-níqueis e do reroll do mercador**, cada um em verde se dá pra pagar (v0.8.60).
- **Ovo orbitando** o personagem, tremendo perto de chocar.
- **Rótulos no mundo** com % de carga/preço (ver §1.3).
- **Toasts** curtos pra quase tudo ("Rocha!", "Ímã! Você puxa todos os doces", "Doce raro!
  Sobe de nível"); **banners** grandes só pra eventos (enxame, alfa, chefe, mutação).
- **Tela de carregamento** com barra "Inimigos prontos N/total", dica aleatória (6 dicas:
  ultimate, baús com E, deslizar, altar, mercador, guardião abre o portal) e botão
  "Começar já" se a conexão estiver lenta.
- **Mapa**: só mostra o que você **já viu de perto**, exceto altar do guardião, santuário e
  portal; segurar **Tab** mostra o mapa **sem pausar**; M abre o grande com zoom (roda/
  pinça/botões) e marcadores; minimapa com **norte pra cima** opcional e pontos cardeais;
  no co-op o **mapa é compartilhado** (o que um descobre aparece pra todos).
- **Captura**: animação com "Vai, bola!", 3 balançadas (pips acendendo) e "Pegou!" /
  "Ah, não! Escapou!".
- **Pausa**: aba **Altares**, lista do que foi **banido**, tabela de **fusões**, DPS por
  golpe e da ultimate, botão **"Preso"/"Atascado"** (desprende o personagem).
- **Salvar e sair**: lembra o mapa explorado; avisa se a partida foi salva em outro
  aparelho; ao voltar pergunta **continuar** ou **finalizar ficando com o conquistado**.
  Não salva durante chefe, evento, Dominante ou Invocador.
- **H** esconde ataques e números (só naquela partida, e com aviso fixo na tela).
- Atalhos de level-up: **F/X/Z** reroll/pular/banir (antes eram R/S/B e davam clique sem
  querer andando pra trás — a mudança é uma lição de UX).
- Aviso de **versão nova** com botão "Recarregar / Mais tarde"; formulário de bug com
  "anexar dados técnicos" (navegador, versão, partida, FPS, conexão).
- **Números grandes** com K/M/B/T/Q.

---

## 7. Ideias pra adicionar no AnimeBonk

Legenda: **[F]** fácil (reaproveita sistema que já existe: baús, mercador, cartas,
status, co-op, Essência, conquistas) · **[L]** lote novo. Nomes abaixo são **sugestões
originais** de tema ninja, não do PokeBonk. Nada disso está decidido: é cardápio pra o
Diego escolher.

1. **[mapa] Pedra de Chakra com tiers (comum/raro/épico/dourado)** [L] — círculo que
   carrega ficando dentro e dá carta de bênção; épico/dourado chamam ondas e o dourado
   só "desperta" aos 1:30. *Por quê*: decisão de risco + feixe de luz que chama de longe.
2. **[mapa] Santuário da Ganância (+20% dificuldade, +25% XP e moedas)** [F] — só um
   modificador no `Config` + prompt. *Por quê*: "aposta" voluntária, sensação de controle.
3. **[mapa] Totem do Desafio** [F] — anel de 8 + 3 × zona inimigos (alguns elite);
   venceu = baú de raridade maior. Reaproveita spawn de mobs e `BauSystem.criarGratis`.
4. **[mapa] Altar Amaldiçoado** [F] — +15% inimigos/+10% dificuldade → item raro na hora.
5. **[mapa] Ruínas Seladas (poder ↔ HP máx.)** [L] — 3 selos: item épico (−15% HP),
   bênção lendária (−20%), companheiro invocado (−25%). *Por quê*: a escolha mais
   memorável do PokeBonk; dá conquista "abrir os 3 selos".
6. **[mapa] Tambor de Guerra (3 batidas)** [F] — cada batida deixa o guardião mais forte e
   +1 baú quando ele morrer. *Por quê*: dificuldade opcional que paga.
7. **[mapa] Espelho de Troca (stat ↑ / stat ↓)** [F] — usa a mesma tabela de 10 pares.
8. **[mapa] Ninho com Ovo de espírito** [L] — ovo orbita o herói e choca após 200/300/400
   abates num aliado. *Por quê*: meta de curto prazo visível o tempo todo.
9. **[mapa] Monge Esquecedor** [F] — esquece um golpe ou pergaminho pra trocar a build.
10. **[mapa] Gêmeo de Sombra (clona 1 item)** [F] — reaproveita inventário de itens.
11. **[mapa] Gato dorminhoco (bênção ou moedas)** [F] — frases engraçadas + sorte decide.
12. **[mapa] Caça-níqueis do festival (pachinko)** [L] — custo +8% por giro, tabela com
    777/moedas/cura/emboscada/maldição, segurar E pra girar. *Por quê*: dopamina pura,
    sumidouro de moedas no fim da zona.
13. **[mapa] Jaula com animal preso** [F] — paga 20 + 10 × zona, ganha meia barra de XP e
    progresso de coleção.
14. **[mapa] Baú amaldiçoado (grátis + emboscada + 5% dificuldade)** [F] — variante do baú.
15. **[mapa] Rocha de ouro e frutinha de cura** [F] — objetos baratos que enchem o mapa de
    decisões pequenas.
16. **[mapa] Cogumelo/mola de pulo** [F] — pad que lança pra platôs (já temos relevo).
17. **[partida] Rodízio de hordas com banner (enxame em anel, manada em linha, revoada,
    chuva de pedras com círculos)** [L] — *Por quê*: quebra a monotonia a cada ~1–2 min.
18. **[partida] Minichefes Dominante e Invocador** [L] — o Invocador **vai embora** se você
    demorar; Dominante dá bênção. *Por quê*: caça com prazo.
19. **[partida] Eventos de atmosfera (névoa, tempestade com marcas, eclipse com chance de
    skin rara, ladrão dourado que solta moedas a cada golpe)** [L].
20. **[partida] Cerco anti-campar** [F] — anel vermelho e resistência se ficar parado.
    *Por quê*: mantém o ritmo do gênero.
21. **[partida] Sequência de abates com marcos (10/25/50/100…)** [F] — moedas, ímã, cura.
    *Por quê*: feedback constante; o contador já existe na ideia de HUD.
22. **[partida] Primeiro elite da zona solta baú grátis** [F].
23. **[partida] Chefe que se cansa (dano recebido sobe com o tempo)** [F] — evita luta
    eterna em build fraca.
24. **[partida] Iluminação por zona (tarde → crepúsculo → noite) + música do santuário**
    [F] — só `Lighting` por zona. *Por quê*: sensação de progresso sem conteúdo novo.
25. **[partida] Split de tempo por zona vs recorde** [F] — popup verde/vermelho.
26. **[partida] Sobrevivência com objetos que se regeneram, mercador visitante (45 s),
    suprimentos do céu, portal de migração aos 11:00 e pactos** [L] — usar a tabela de
    9 pactos como base de números.
27. **[partida] Reviver: Laboratório "começa com 1 reviver" + item 1× por zona que renasce
    explodindo** [F] — encaixa no "reviver pago" da spec com Essência.
28. **[partida] Pausa de equipe por votação (5 min por partida)** [F] — co-op.
29. **[partida] Reserva de bolha no level-up do co-op (45 s +15/nível, máx. 90)** [F].
30. **[personagem] Vínculo do aliado (+10% dano por nível, por abates)** [L].
31. **[personagem] "Treinamento" pós-kit completo (bônus pequeno permanente por nível)** [F].
32. **[personagem] Pity de skin rara (chance sobe a cada tentativa)** [F] — anti-frustração.
33. **[personagem] Visuais por shader (tinta sumi-ê, pedra, neon, chama, sombra)** [L] —
    muitos cosméticos com a mesma malha. *Por quê*: maestria vira visual sem arte nova.
34. **[menu] Conquistas de desafio ligadas a objetos do mapa** (3 selos, 3 batidas, 777,
    15 maldições, ≤ 3 itens) [F] — já temos sistema de conquistas.
35. **[menu] Laboratório: Sintonia (ultimate), Mochila grande, Equipe de apoio, Pesquisa**
    [F] — linhas novas na mesma loja de Essência.
36. **[menu] Tela de fim com "ultrapassou {nome}, agora você é #N" e Enter = jogar de novo**
    [F]. *Por quê*: rival concreto puxa a próxima partida.
37. **[HUD] Carteira com preço do próximo baú/reroll em verde/vermelho** [F].
38. **[HUD] Rótulos no mundo com % de carga e preço; Tab = mapa sem pausar; mapa só do
    que foi visto, compartilhado no co-op** [L].
39. **[HUD] Dicas na tela de carregamento + aba "Altares" na pausa** [F].
40. **[menu] Mutação do Dia com recompensa 1×/dia por zona e prêmios permanentes** [L] —
    já está no plano da etapa 7.

---

## Resumo das descobertas mais valiosas

1. O cliente público do PokeBonk (v0.8.80) tem **todos os números**: custos, tempos,
   chances e a tabela de quantos objetos aparecem por zona — base pronta pra balancear.
2. São **~20 tipos de objeto de mapa**, todos de uso único e com troca clara (risco ↔ prêmio).
3. O altar de carga tem **5 tiers** (8/14/22/35 s, ondas no épico/dourado, dourado selado até 1:30).
4. "Poder ↔ HP máx." (3 fósseis: −15/−20/−25%) e "chefe mais forte ↔ +1 baú por grito"
   são as escolhas mais marcantes.
5. O caça-níqueis tem uma tabela de prêmios e um custo que **sobe 8% por giro**: é um sumidouro de moedas.
6. O diretor alterna **4 hordas com banner**, **2 minichefes** (um deles foge) e **4 eventos de atmosfera**.
7. Existe um **anti-campar ("Cerco")** e o chefe que demora **fica cansado**: ritmo forçado sem frustrar.
8. A Sobrevivência tem **9 pactos** com números, mercador que visita, cometas, migração aos 11:00 e objetos que se regeneram.
9. O reviver vem do Laboratório (4.250), de itens (35%/60%) e de um item 1×/zona. No co-op há reanimar com E em 60 s e uma pausa de equipe por votação. **Não existe** "Revive All" pago.
10. O PokeBonk **não é de Roblox** e **não tem loja paga**. A loja de Robux do AnimeBonk vai precisar de outra referência.
