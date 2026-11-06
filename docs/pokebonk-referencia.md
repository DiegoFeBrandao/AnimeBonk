# PokeBonk — referência de mecânicas e telas

Fontes: **78 capturas de tela** que o Diego tirou do jogo (pasta
`C:\Users\Diego\Desktop\pokebonk`, 2026-10-29, versão v0.8.77 beta) + ~40 páginas de guia
do PokeBonk em https://megabonk.org/pokebonk/ (lidas em 2026-10-29). Serve de base pra
comparar/inspirar o AnimeBonk — **não é spec do nosso jogo**; nada de Pokémon (nomes,
sprites, tipos com nome de marca) entra no AnimeBonk. Ver também
`docs/megabonk-referencia.md` (o jogo que o PokeBonk imita).

---

## 1. Ficha

| Campo | Valor |
|---|---|
| O que é | Fan-game gratuito de navegador (pokebonk.com), feito por "Charcher". "Megabonk com Pokémon" |
| Visual | **3D** (câmera em 3ª pessoa, FOV, pulo, terreno com relevo) com **sprites pixel art** (estilo Pokémon Mystery Dungeon) e cenário voxel/pixel |
| Plataformas | PC (teclado/mouse ou controle) e celular (controles de toque) |
| Modos | Clássico · Sobrevivência · **Cooperativo 2–4 (beta)** · Mutação do Dia · Evento de temporada |
| Idiomas | 10 (pt, en, es, fr, ja, zh-hans, zh-hant, ko, ru, automático) |
| Conta | Convidado (salvo no servidor, por dispositivo, apagado após 60 dias sem uso) ou conta registrada (obrigatória pro co-op) |
| Ritmo de updates | Muito rápido (vários patches por dia em out/2026); temporadas de ~2 semanas |
| Escala | Temporada 2: ~790 mil treinadores no ranking, 327 mil no evento, 271 procurando co-op no momento |

---

## 2. Loop do modo Clássico

1. **Escolher parceiro** na tela "A Liga" → "Eu escolho você!".
2. **Escolher região** (mapa) + **modo** (Clássico/Sobrevivência) + **dificuldade**
   (Normal ×1 Stardust · Difícil ×1,75 Stardust, inimigos +70% · Pesadelo ×2,5 Stardust,
   inimigos +160%, bloqueado até vencer o Difícil) + até **2 itens de Mochila** → Começar.
3. A região tem **3 zonas + santuário**. Em cada zona: matar hordas, subir de nível, pegar
   itens, achar o **altar do guardião** (marcado no mapa), invocar e derrotar o **guardião**
   (sorteado entre 3 possíveis por zona), pegar a **recompensa** (uma Poké Bola grande,
   seta + minimapa guiam), entrar no **portal** → próxima zona.
4. Zona 3 leva ao **Santuário** (lendário da região, ex.: Mew na floresta). Vencer e
   entrar na saída final = **vitória** da região.
5. Se a zona chegar a **10:00** começa o **Final Swarm** (pressão escala sem parar). Não é
   pra esperar: é punição por enrolar.
6. Fim → tela de resultado; Stardust e progresso de desafios entram na conta.
7. **Salvar e sair** pela pausa (exceto durante chefe/evento) e continuar depois.
8. **Contra o relógio**: medalhas por tempo de vitória (Bronze qualquer vitória · Prata
   < 24:00 · Ouro < 18:00 · Campeão < 13:30, na floresta normal).

### Regiões (temporada 2)

| Região | Tipos de inimigo | Libera com |
|---|---|---|
| Floresta Verde | planta, inseto, normal, voador, fada, veneno | padrão |
| Deserto Rochoso | terra, pedra, lutador, aço, fogo | vencer a Floresta |
| Costa da Tormenta | água, elétrico, voador, dragão, aço | vencer o Deserto |
| Geleira Celeste | gelo, água, psíquico, fada, dragão | vencer a Costa |
| Torre Lavender / Ilha Vulcão | — | "em breve" |

- Cada região tem chefes próprios com mecânica de arena (ex.: chefe elétrico com maré
  que inunda a arena; chefe de gelo que pode ser congelado pelo próprio raio).
- **Clima** por região (chuva, sol, tempestade de areia, granizo): +30% num tipo, −25% em
  outro.
- Objetos especiais no mapa: altares, jaulas (soltar dá pesquisa), lápides, "Máquina do
  Bill" (fusão), loja do Meowth (mercador), frutas, Poké Bolas de item espalhadas.

---

## 3. Modo Sobrevivência

- **Infinito**: hordas + marcos. Ranking por tempo sobrevivido (desempate por abates).
- Marcos na floresta: guardiões aos **5:00 e 10:00**, lendário aos **15:00** e **30:00**,
  chefe final aos **45:00** e daí começa a "Noite Sem Fim" (pressão contínua).
- Depois de cada chefe de marco: escolher um **pacto** = bônus forte **+ maldição**
  (custo permanente na run). Decisão de risco acumulado.
- **Sobrevivência em equipe** (co-op): chefe compartilhado **a cada 4 min**; quem caiu
  volta depois do próximo chefe; ranking de equipe por tempo; Máquina de fusão recarrega
  11 min após o uso.

---

## 4. Cooperativo (2–4 jogadores, beta)

- **Com amigos**: criar sala (criada na hora, sem escolher nada antes; mapa, modo, dificuldade
  e personagem são escolhidos dentro dela, e de lá se convida) ou entrar com **código de 4
  letras/números** (sem I, L, O, 0, 1 — corrigido em 2026-11-05, cliente v0.9.13). Painel de
  convites. Detalhe das telas: `docs/superpowers/plans/2026-11-05-coop-sala-redesign.md`.
- **Procurar partida** (matchmaking): filtros de modo (Clássico/Sobrevivência), equipe
  (Qualquer/Dupla/Trio/Esquadrão), mapa, dificuldade. Mostra quantos estão procurando.
- Regras na tela "Como se joga":
  - **Uma horda para cada um** — cada jogador tem a própria horda; se ficarem juntos, as
    hordas se somam.
  - **Chefes de todos** — guardião e lendário são compartilhados e têm mais vida.
  - **Ninguém fica para trás** — caiu → companheiro reanima segurando E ao lado.
- Roda de sinais (G / L3) pra marcar local/perigo; líder da sala com coroa (passa se
  ficar inativo, "Ainda aí?").
- Escolhas de level-up não pausam o mundo; proteção de 5 s por nível (máx. 10 s)
  enquanto escolhe.
- **Classificação cooperativa** por Dupla/Trio/Esquadrão × dificuldade × mapa. Cada
  entrada abre: abates da equipe, tempo, data, e por jogador: Pokémon e nível, abates,
  dano, % dos abates da equipe, golpes, itens, botões "Ficha" e "Ver o build".
- Config própria: "Ataques dos colegas" Completos / Simplificados / Ocultos (dano conta
  igual) — pra não poluir a tela.
- Exige conta registrada.

---

## 5. Mutação do Dia (modo diário)

- Regra modificadora **rotativa a cada 24 h** (timer na tela), dificuldade fixa.
  Ex. "Selvagens Dynamax": inimigos 2× tamanho e 2× HP, batem +50%, 15% mais lentos;
  chefes não mudam.
- **Mesmo mapa e mesma semente pra todos**, sem Mochila → ranking justo.
- Conta a **melhor partida do dia** (até onde chegou; empate = abates). Ranking Hoje /
  Ontem / Há 2 dias.
- **Trilha de recompensa** por progresso: Zona 1 → Zona 2 (+60 Stardust) → Zona 3
  (título) → Santuário (moldura) → Vitória (fundo de perfil).
- Calendário mostra as próximas mutações ("Febre de Doces amanhã", "Metronome em 2
  dias", "Cristal em 4 dias") + meta "Rei das Mutações: 0 de 4 vitórias".

---

## 6. Evento de temporada (ex.: "A Noite da Torre Lavender", Halloween)

- Modo próprio com duração limitada (timer), **moeda do evento** (Velas).
- Regras: subir uma torre **andar por andar**, 3 ondas por andar abrem a escada;
  fantasmas invisíveis quase imunes até um **pulso de revelação**; **acender velas** pra
  enxergar no escuro; lápides com "travessura ou gostosura" (aleatório bom/ruim);
  escolher uma **Oferenda** por andar (modificador); mini-chefe no 6º, chefe no 7º;
  depois **andares infinitos** onde cada maldição aceita dá mais Velas.
- Abas: Jogar · **Livro de Velas** (trilha de recompensas 50 → 2500 velas: títulos,
  Stardust, itens, visuais/fantasias) · Conquistas do evento · Classificação
  (treinadores e clãs; andar alcançado → ondas → menor tempo; pódio) · Prêmios (top 100
  coroa, top 25 título, top 10 visual, nº 1 exclusivo; clãs top 10 ganham emblema).
- "Cada partida soma velas: muitas no modo evento e algumas nos outros" → evento puxa
  o jogador mesmo nos modos normais.
- O fundo animado de todos os menus muda pro tema do evento.

---

## 7. Personagem jogável ("parceiro" da Liga)

Tela **"A Liga"** (seleção), com tudo que importa numa ficha só:

- Nº, **classe** (ex.: Defensor, Assalto Ígneo, Feiticeira Ígnea, Radar), raridade
  (Comum/Incomum...), tipo(s), favoritar (até 6 favoritos).
- **Evolui durante a partida** por nível (ex.: nv 24 → nv 44). Visual e golpes mudam.
- **Vitórias por dificuldade** (Normal/Difícil/Pesadelo).
- **Estatísticas base** (HP, Ataque, Defesa, Atq. Esp., Def. Esp., Velocidade) →
  convertidas em **"Na partida"**: HP máx., Armadura, Evasão, Velocidade ×, Dano físico ×,
  Dano especial ×, Regeneração/s, Chance crít. Tooltip em cada stat explicando.
- **Passiva de classe** (ex.: "+15 armadura +20 escudo; abaixo de 40% HP +40% dano").
- **Kit de ataques**: 4 golpes próprios que liberam por nível (inicial, nv 2, nv 4, nv 7),
  cada um com forma, físico/especial, dano, recarga, alcance, % de status.
- **Ultimate (tecla R)**: 3 versões (uma por estágio de evolução), barra que carrega,
  com "pausa de imagem"/retrato ao lançar (desligável).
- **Tipos**: fraco contra (×1,35), resiste (×0,80), eficaz contra.
- **Kits compartilhados**: aprende golpes de outros membros da Liga do mesmo tipo
  → **colecionar personagens aumenta o pool de golpes** de todos.
- Estatísticas pessoais com o personagem: partidas, vitórias, recorde de abates, nível máx.
- Botões **Ataques** (lista completa) e **Plano** (plano de build).
- Lista à direita: abas Todos / Na minha Liga / Shiny / Guarda-roupa, busca, filtro por
  tipo, **Aleatório**; bloqueados aparecem como silhueta "???" com barra do desafio.

### Como entra um personagem novo na Liga (79 no total)

1. Cumprir o **desafio** dele (ex.: "Queime 6.000 inimigos"), progresso salvo entre
   partidas. Classe e kit ficam ocultos até entrar.
2. Ele **aparece selvagem na próxima partida** (banner/marcador).
3. **Enfraquecer** e **capturar** (lançar a bola perto, janela de 10 s antes de fugir).
- Lendários elegíveis entram só de enfraquecer (a bola serve pro shiny).
- "Começar do zero" na conta: escolher o parceiro inicial de novo (1× por semana).

---

## 8. Ataques (o "arsenal")

- **Slots de ataque** limitados (3 no início; 4º slot comprado no Laboratório; o plano
  fala em até 6). Ataques disparam sozinhos; mira **automática** (mais próximo) ou
  **manual** (direção da câmera), tecla Q alterna; clique direito fixa alvo.
- Fontes de golpe oferecidas no level-up:
  - **Kit próprio** (aparece mais que os outros).
  - **Linha evolutiva** (35% de chance de ser oferecido, se houver slot livre; alguns só
    a partir do nível X).
  - **Ao evoluir** (golpes novos liberados pela evolução).
  - **Kits de outros membros da Liga** do mesmo tipo (ou Normal) — "ensinado por X".
- 493 golpes catalogados (246 físicos). Ficha do golpe: poder, dano por golpe, DPS,
  recarga, alcance, velocidade, % de status, crítico, roubo de vida.
- **Nível do golpe 1 → 8**: só subir de nível dobra o dano (gráfico de barras na ficha).
  **A cada nível, 2 melhorias aleatórias** (3 se a carta for épica/lendária) de uma lista
  por golpe, que escalam de comum a lendário: Dano +22%→+46%, Recarga −8%→−17%,
  Quantidade +1→+2, Perfuração +1→+2, Velocidade +15%→+32%, Crítico +5%→+11%,
  Ricochetes +1→+2.
- Ficha mostra **"O que melhora"**: quais stats e **quais itens** afetam aquele golpe
  (e destaca os que você já tem).
- **Formas de ataque** (taxonomia exibida no glossário):
  - Projéteis: projétil, esfera explosiva, bomba em parábola, rajada, teleguiado,
    bumerangue, drenagem (rouba vida).
  - Raios e cones: raio contínuo (atravessa), cone, onda.
  - Área: onda de choque, corrente (salta), impacto celeste, meteoro, armadilha, vórtice,
    aura, órbita, giro, investida, golpe em arco.
  - Potencializador (buff).
- **Fusões** (na Máquina do Bill, objeto do mapa): 2 golpes **no nível máximo** viram um
  golpe novo, que ocupa o slot do primeiro e **libera o outro slot**. Tipo e
  físico/especial próprios; nível ★1–★5; nunca funde de novo. Categorias:
  - **Assinatura** — 2 golpes do kit do mesmo personagem (1 por personagem).
  - **Reação** — um golpe de cada tipo de uma reação elemental.
  - **Fusão de tipo** — 2 golpes do mesmo tipo.
  - **Falha na máquina** — qualquer outro par vira uma fusão-glitch aleatória (easter egg).
  - Cards de fusão explicam "como funciona" (sub-partes: cone, vórtice, zona persistente)
    e "quais melhorias o afetam".

---

## 9. Vitaminas (os "Tomes" do PokeBonk)

- Melhorias de **stat** escolhidas no level-up. **Espaços limitados** (3 no início, +
  espaços comprados no Laboratório; build de topo tinha 5).
- **Nível 1 → 10** (12 com item raro). Cada nível soma conforme a **raridade da carta**:
  Comum +10% · Incomum +12% · Raro +14,5% · Épico +17,5% · Lendário +21%.
- 26 vitaminas: dano físico, dano especial, armadura, escudo regenerável, velocidade de
  movimento, HP máx., projéteis, velocidade de ataque, crítico, velocidade de projétil,
  evasão, chance de status, área, duração, regeneração, dinheiro, experiência, sorte,
  roubo de vida, alcance de coleta, espinhos, sobrecura, surgimento de elites, power-ups
  e **"Incenso Maldito"** (mais inimigos e mais fortes, +XP — a "Cursed Tome").

---

## 10. Itens

- **126 itens** com raridade (Comum · Incomum · Raro · Épico · Lendário — cor da borda).
  Vêm de **Poké Bolas espalhadas pelo mapa** (abrir) e da **loja do mercador** na partida.
- **Sem limite de slots** (uma build de topo tinha 177 itens), mas cada item tem
  **"máximo por partida"** (lendários geralmente 1; comuns até ×10).
- Item precisa ser **comprado no Laboratório** com Stardust pra entrar no pool
  (ex.: lendário 2.800). **Arquivo**: itens que você tira do pool; cada 2 itens
  desbloqueados dão +1 espaço no Arquivo (até 59).
- Exemplos de efeitos: +15% dano e "ao apanhar, para o tempo dos inimigos próximos por
  3 s (a cada 20 s)"; +X% dano de um tipo; shiny garantido; começar 2 níveis acima...
- Itens que soltam ataques próprios (raios, explosões) têm dano base que sobe por nível
  e por cópia, mas **não provocam reações**.

---

## 11. Atributos e fórmulas (do glossário do jogo)

- Regra geral: **bônus da mesma origem somam; de origens diferentes multiplicam.**
- Armadura: redução = armadura / (armadura + 45).
- Evasão máx. 60%. Crítico ×1,75 (megacrítico existe acima de 100%).
- Velocidade de ataque: recarga real = recarga / vel.; mínimo 0,12 s (fusões 0,6 s);
  excedente não acelera.
- Projéteis extras não afetam auras/ondas.
- **STAB** (golpe do mesmo tipo do personagem) +25%. Eficácia ×2 / ×0,5 / ×0 (imune).
- Inimigos especiais: Elite, **Alfa**, Totem, Guardião, Lendário, Dominante (mais vida;
  "dano em elites" vale contra todos eles).
- Tabela final de stats na build (≈ 34 atributos): Área, Dinheiro, Sorte, Dano de queda,
  Armadura, HP máx., Regen, Dano, Espinhos, Experiência, Evasão, Cura, Power-ups, Dano
  especial, Duração, Chance de megacrítico, Sobrecura, Dano físico, Roubo de vida,
  Velocidade, Vel. projétil, Escudo, Chance crít., Dano crítico, Surgimento de elites,
  Pulos extras, Altura do pulo, Vel. de ataque, Dano em elites, Alcance de coleta,
  Projéteis, Chance de status, Dano de status, Dano super efetivo.
- Nível do personagem **sem teto** (ranking mostra nível 3.000+ em runs longas de co-op).

### Status (chefes resistem: duram menos e não travam)

| Status | Efeito |
|---|---|
| Queimado | 3 s, 30% do golpe por segundo |
| Envenenado | acumula até 10 cargas, dano cresce por carga |
| Paralisado | metade da velocidade, às vezes para 3 s |
| Congelado | 3 cargas de gelo = congela 1,6 s e +20% dano recebido; se Molhado, congela na hora |
| Dormindo | parado 3 s; próximo golpe ×1,8 e acorda |
| Confuso | 3 s andando sem controle, pode ferir outros inimigos |
| Molhado | 5 s; prepara reação elétrica e congelamento |
| Amaldiçoado | 4 s, +25% de dano recebido |
| Bloqueio de cura | 6 s sem cura, perde metade do escudo |
| Encantado | 3 s, −40% dano e para de atacar |
| Enraizado | 2 s, 65% mais lento |
| Atordoado | parado meio segundo |

### Reações elementais (golpe acerta inimigo que já tem um status → multiplica o dano)

| Reação | Combinação | Efeito |
|---|---|---|
| Eletrocutado | Molhado + Elétrico | salta até 12 molhados a 9 m, 60% paralisa, ×1,5 |
| Vapor | Queimado + Água | nuvem que confunde e enraíza, ×1,4 |
| Incêndio | Queimado + Planta/Voador | espalha queimadura 7 m, ×1,3 |
| Destruição | Congelado + Lutador/Pedra/Aço | quebra o gelo ×2,6 com estilhaços |
| Gás venenoso | Envenenado + Fogo | explode 10% por carga |
| Pesadelo | Dormindo + Fantasma/Sombrio | ×1,7 e cura |
| Colapso mental | Paralisado + Psíquico | ×1,6 ou confunde |
| Fúria dracônica | Encantado + Dragão | ×2 |

Têm um pequeno cooldown por golpe. Conquistas contam reações feitas (50/1k/10k).

---

## 12. Ajudantes na partida

- **Alfas de apoio**: Alfa derrotado pode ser capturado com uma bola especial; luta ao
  seu lado **só naquela partida** e dá bônus pelo tipo dele (normal +10% dinheiro, fogo
  +15% dano de status, água +15% cura, planta +0,5 HP/s, elétrico +5% vel. ataque, gelo
  +10% duração, lutador +10% dano em elites, veneno +12% chance de status, terra +4
  armadura, voador +5% velocidade, psíquico +8% XP, inseto +1 coleta, pedra +15 HP,
  fantasma +3% evasão, dragão +5% dano, sombrio +4% crit, aço +8% área, fada +8 sorte).
  Slots limitados (até 4 + 1 shiny com upgrades). Não entra na Liga.
- **Mochila** (consumíveis pré-partida, leva até 2, gastos ao começar; guarda até 9 de
  cada): começar 2 níveis acima; +25% XP; +50% dinheiro; +1 Alfa por zona; shiny
  garantido na zona 1; primeira captura garantida.

---

## 13. Meta-progressão e moedas

| Moeda | Onde ganha | Pra que serve |
|---|---|---|
| **Pokédólares** (in-run) | inimigos, pular ofertas | loja do mercador na partida |
| **Stardust / Poeira Estelar** (permanente) | fim de partida (× dificuldade), tarefas, conquistas, ranking, clã | Laboratório, loja da Mochila, criar/ampliar clã |
| **Bonkoins** | guardiões e chefes largam às vezes; missões de clã | roleta "Tesouros" |
| Moeda de evento (Velas) | partidas (muito no modo evento) | trilha do evento |

### Laboratório ("gaste seu Stardust")

- **Treinamento** (stats permanentes, níveis com custo crescente): +4% dano/nv (8 nv),
  +8 HP/nv, +2,5% velocidade, +5% XP, +8% dinheiro, +5 sorte, +0,6 coleta, +0,2 regen,
  +2 armadura, +1% crítico, +2% vel. ataque, +3% área. Contador "Melhorias 10/111 níveis
  (23 ao alcance)".
- **Equipe da partida** (espaços, opções e ferramentas): 4º slot de ataque, +espaços de
  vitamina, **Atualizar** (reroll de ofertas, +1 uso/nível), **Pular** (skip, dá
  dinheiro), **Banir** (remove opção pelo resto da partida), **Quarta opção** (level-up
  oferece 4 cartas).
- **Itens**: comprar itens pro pool ("73/126 no seu pool, 53 prontos").

### Loja (Stardust → itens de Mochila)

- Preço **sobe a cada cópia comprada no dia**, limite diário por item, reset 00:00 UTC.

### Tesouros (roleta)

- Uma roleta por personagem ("Tesouros de Charmander 0/10"). Gasta Bonkoins por giro;
  **sem repetição** (10 prêmios, 10 giros garantem tudo). Grande prêmio = visual +
  moldura épica + título. Tem botão **Probabilidades** (transparência).

---

## 14. Coleção e cosméticos

- **Pokédex** (151): vistos / capturados / shiny / famílias capturadas; ficha com dados,
  stats, linha evolutiva, "Ver todos os golpes (49)", "Plano de build". Abas também pra
  Ataques (493), Vitaminas (26) e Itens (126) — a Pokédex é a **enciclopédia completa**
  do jogo.
- **Caderno de pesquisa**: cada inimigo derrotado soma "pesquisa" na família dele
  (Alfas, chefes e jaulas somam mais). Família completa → vira **avatar**. Completar N
  famílias de um tipo → **moldura de tipo** (18). **Marcos do pesquisador** (5/15/30/45
  famílias) → avatares de personagens humanos; 60 → moldura especial.
- **Guarda-roupa** (visuais, só estéticos, 4 por personagem): Normal · Shiny · Shiny
  clássico (raríssimo) · Maestria I (épico) · Maestria II (lendário) — maestrias por
  feitos específicos com aquele personagem (vencer em < 14 min, vencer Pesadelo com a
  evolução final, aplicar 20.000 status...).
- **Perfil**: avatar + moldura + **título** + **fundo**; aparece em rankings e na ficha.
  Origens: ranking de temporada, caderno, eventos, tesouros, conquistas.
- **Ficha de treinador** (perfil público): tag do clã, data de entrada, posição global,
  favorito mais jogado, stats de carreira (partidas, vitórias, abates, tempo jogado,
  guardiões, lendários, Alfas, nível máx., Liga x/79, Pokédex, shinies, medalhas de tempo),
  favoritos, **recordes por região** (abates e contra o relógio, cada um com link pro
  build), vitrine de insígnias de temporada. Botões: adicionar amigo, copiar link,
  denunciar.

---

## 15. Engajamento diário e metas

- **Tarefas do dia** (3: fácil/média/difícil — ex.: sobreviver 8 min, chegar à zona 2,
  derrotar 2 guardiões) + **prêmio do dia** (Stardust + item de Mochila) + **sequência**
  (streak de dias).
- **Tarefas da semana** (3 categorias: Constância, Façanha, Desafio) com **Trocar**
  (reroll de tarefa) + prêmio da semana.
- **Conquistas** (228), em abas: Progresso (abates 100→1M, capturas, guardiões,
  lendários, reações, nível, tempo), Dificuldade (vencer cada mapa no Difícil/Pesadelo,
  medalhas de tempo), Desafios (≤3 itens, sem vitaminas, ≤20 golpes recebidos, vencer
  com < 10% HP, Pesadelo com ≤3 itens), Coleção, Temporada, Sobrevivência (10/30/60 min),
  Visuais, **Segredos** (ocultas "???"). Resgate manual com "Resgatar tudo"; algumas dão
  **título**.

---

## 16. Social

- **Classificação** ("recordes do servidor, validados contra trapaças"):
  Treinadores / Clãs / Cooperativo; Abates (Global = soma da melhor partida de cada
  região; ou por região), Por personagem, Sobrevivência (tempo), Contra o relógio.
  Esta temporada / Histórico. Pódio top 3 + tabela com "distância até o 1º". Barra fixa
  "Sua temporada". **Cartão da temporada** no HUD da partida: sua posição e o rival que
  você persegue ("faltam 2,9M pra entrar no top 50").
- **Prêmios de temporada** (top 100): #1 1500 Stardust, #2–3 900, top 10 500, top 25 300,
  top 50 180, top 100 100 + insígnias que liberam molduras e avatares exclusivos.
- **Clãs** (30 a 200 membros): fundar custa 2000 Stardust (nome, sigla, emblema
  desenhado). Partidas válidas somam pontos de clã (mais no Difícil/Pesadelo). Entrada
  aberta / por solicitação / só convite; líder e oficiais. Qualquer membro amplia vagas
  (+10 com Stardust). **Missões semanais** (3, com 3 estrelas) + **rivalidade** contra clã
  do mesmo tamanho. Clã sobe de nível (até 30) e libera enfeites de emblema. **Mural**
  com reações rápidas. Top 50 de clãs ganha prêmios (membro precisa ter contribuído).
  Sigla aparece antes do nome em todo lugar.
- **Amigos** (até 100): adicionar por nome ou link da ficha; status online; convidar pro
  clã/co-op.
- **Caixa de entrada**: convites de clã (expiram em 7 dias), pedidos de amizade (30
  dias), mensagens da equipe, resultados de temporada, decisões de "partida em revisão"
  (anti-cheat). Avisos guardados 60 dias.
- **Notícias** dentro do jogo (AVISO / ATUALIZAÇÃO / NOVIDADE, fixados).

---

## 17. HUD da partida e pausa

- **HUD**: retrato + nome + tipo + nível + próximo estágio de evolução (canto sup. esq.);
  centro-topo: região, zona x/3, dificuldade, **timer regressivo da zona (10:00)**,
  cronômetro total, recorde do mapa, contadores (dinheiro, itens, abates); minimapa
  redondo com ícones (sup. dir.); **cartão da temporada**; barra de HP sob o personagem
  + anel de seleção; slots de ataque (inf. esq.) com ícone e nível; ultimate com anel de
  recarga e tecla R; 3 slots pequenos de vitamina.
- **Pausa** (completa, solo): tempo, abates, dano, dano/s, dinheiro, melhor sequência;
  HP e XP; **Ataques** (cada golpe com dano total, % do dano, DPS dos últimos 7 s),
  botões "A conseguir" / Fusões / Altares; **Itens** e **Vitaminas x/3**;
  **Estatísticas** (Ataque / Defesa / Utilidade, verde = melhor que a base, tooltip);
  glossário; dicas de teclas; botões Desistir / Salvar e sair / Reiniciar / Mapa grande /
  **"Preso"** (destravar personagem) / Configurações / **Relatar** (bug) / Continuar.
- Primeiras 3 partidas: dicas curtas na primeira vez que vê cada objeto.
- Telas novas têm **tutorial guiado** em passos ("Passo 1 de 5", Pular/Voltar/Próximo).

---

## 18. Configurações (referência de acessibilidade e desempenho)

- **Som**: geral, música, efeitos, gritos, silenciar em segundo plano.
- **Gráficos**: qualidade, economia de bateria (30 fps), limite de FPS, tremor de tela +
  intensidade, opacidade dos efeitos / dos **meus** ataques, ocultar meus ataques,
  **inimigos desenhados** (todos / próximos 30 m / muito próximos 18 m — os outros
  existem mas não renderizam), XP discreto, efeitos de coleta simples, ataques dos
  colegas, brilho/bloom, **reduzir clarões** (fotossensibilidade), mostrar FPS.
- **Controles**: toque/teclado automático, mira auto/manual, sensibilidade, inverter Y,
  FOV, distância da câmera, ultimate automática, ultimate sem interrupções, controle de
  console com guia de botões.
- **Teclas** remapeáveis (inclui botões do mouse): WASD, Espaço pulo (segurar = planar se
  voa), Shift deslizar (no ar: mergulho), E interagir, R ultimate, Q mira, clique dir.
  fixar alvo, T avanço automático, M mapa, Y ultimate automática, H ocultar ataques e
  números, P pausa, F/X/Z reroll/pular/banir no level-up.
- **Interface**: tema, tamanho e opacidade da UI, opacidade das barras de chefe, vida dos
  chefes em HP ou %, minimapa (tamanho, marcas, norte pra cima), avisos grandes,
  cartão da temporada, contador de sequência, números de dano, textos flutuantes ("É super
  efetivo!"), **"sem janela se não houver escolha"** (level-up com 1 opção aplica sozinho),
  dicas das primeiras partidas.
- **Conta**: trocar nome (1×/30 dias), senha, começar do zero (1×/7 dias), apagar conta.

---

## 19. Megabonk × PokeBonk (o que o PokeBonk mudou)

| Tema | Megabonk | PokeBonk |
|---|---|---|
| Multiplayer | só solo | co-op 2–4 + matchmaking + clãs + ranking de equipe |
| Plataforma | Steam | navegador + celular |
| Estrutura do mapa | 1 mapa por fase, 10 min, portal do chefe | 3 zonas + santuário por região, guardião por zona |
| Personagem | passiva + 1 arma inicial | passiva + **kit de 4 golpes por nível + evolução + ultimate (R)** |
| Arsenal | armas + Tomes + itens | golpes (com fusões) + vitaminas + itens + Alfas de apoio |
| Elementos | poucos status | **18 tipos, vantagem/resistência, 12 status, 8 reações** |
| Coleção | desbloqueio por objetivo | desbloqueio por desafio **+ captura na partida** |
| Retenção | quests, challenges | tarefas diárias/semanais com streak, mutação do dia, eventos sazonais, temporadas, roleta, caderno de pesquisa |
| Transparência | wiki externo | **glossário, fichas e números dentro do jogo** (DPS, fórmulas, o que melhora cada golpe) |

---

## 20. O que levar pro AnimeBonk (pra discutir — não decidido)

- **Co-op** com "uma horda por jogador" e "chefe compartilhado com mais vida", reviver
  segurando E. Combina muito com Roblox (servidor já é multiplayer).
- **Personagem com kit que libera por nível + "despertar"/transformação** no meio da run
  (o equivalente anime da evolução) + **ultimate com retrato/pausa de imagem** —
  muito "anime".
- **Elementos + reações** (ex.: molhado + raio) dão profundidade sem precisar de muitos
  itens.
- **Fusão de golpes** no nível máximo (técnica combinada / golpe conjunto).
- **Coleção que alimenta o pool** (personagem novo ensina golpes pros outros do mesmo
  elemento) — torna desbloquear sempre útil.
- Desbloqueio por **desafio → aparece no mapa → derrotar/recrutar** na partida.
- **Mutação do dia com semente fixa** e **evento sazonal com moeda própria e trilha**.
- **Tarefas diárias/semanais com streak**, temporadas com prêmios, clãs com missões e
  rivalidade.
- **Glossário e fichas dentro do jogo**, pausa com estatísticas completas, "o que
  melhora este golpe".
- Opções de desempenho essenciais pro Roblox/celular: **inimigos desenhados só por
  perto**, ocultar/opacidade dos próprios ataques e dos colegas, efeitos simples.
- Cuidado: o PokeBonk é **enorme** (79 personagens, 493 golpes, 126 itens). Pro AnimeBonk,
  começar pequeno e crescer por temporada.
