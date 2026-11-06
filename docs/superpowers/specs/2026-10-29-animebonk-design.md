# AnimeBonk — design da primeira versão (v1)

Data: 2026-10-29. Status: **aprovado pelo Diego (2026-10-29)** — nome do jogo fica
**AnimeBonk**; heróis **Ryuga**, **Kaizo** e **Haruto**; heróis em **2D** (sprite).
Limites do reviver pago (1 de cada por partida) e ícone no ranking ficam como decisão do
Claude até o Diego dizer o contrário.
Tudo aqui é proposta do Claude (o Diego pediu "pode propor tudo"), exceto o que está
marcado como **[Diego]**. Perguntas que o Claude faria e a resposta assumida estão na
seção 14.

Referências: `docs/pokebonk-referencia.md` (modelo de layout/menus e de co-op) e
`docs/megabonk-referencia.md` (modelo de gênero). Regras de trabalho: `CLAUDE.md`.

---

## 1. Intenção

- **[Diego]** Jogo Roblox de sobrevivência roguelike 3D com **tema anime**, no estilo do
  PokeBonk/Megabonk: auto-ataque, hordas, level-up com cartas, build, chefes, **co-op**.
- **[Diego]** Gostou muito do **layout e dos menus do PokeBonk**.
- **[Diego]** Primeiros 3 heróis **inspirados** em três protagonistas de anime famosos
  (lutador de energia, pirata elástico, ninja de clones), com nomes próprios. Resto vem
  depois.
- **[Diego]** Inimigos (e possivelmente heróis) como **sprites 2D dentro do mundo 3D**,
  como no PokeBonk, pra ficar leve no Roblox.
- **[Diego]** (revisão 2026-10-29) Heróis **mais parecidos com os animes** — mesmo tipo
  de poder, mesma "energia" de personagem. Experiência dono: **grupo novo do Roblox**.
  **Sem lobby 3D por enquanto** (só menus, como o PokeBonk). **Clãs** entram no jogo.
  **Segundo fôlego e "Reviver todos" pagos**. Jogo **em inglês com tradução pra
  português**.

### Até onde dá pra ir no "parecido" (regra de design)

Pode ficar igual: **o tipo de poder e a personalidade** — lutador que dispara rajadas e
raio de energia, voa, se teletransporta e se transforma em estágios com aura; pirata
de corpo elástico, socos esticados, alegre e comilão; ninja barulhento que faz clones,
usa kunai/shuriken e tem uma fera selada dentro de si. Isso é arquétipo de shonen.

Não pode ficar igual (é o que identifica o personagem e dá derrubada por direito
autoral): **nome parecido, rosto/cabelo/roupa/cores característicos e nome/pose dos
golpes famosos**. Concretamente fora: cabelo preto espetado + roupa laranja e azul,
cabelo dourado na transformação, chapéu de palha, cicatriz embaixo do olho, colete
vermelho aberto, cabelo loiro + roupa laranja + bandana com símbolo de vila, raposa de
nove caudas, bigodes no rosto, e os nomes/poses de golpe conhecidos (mãos em concha na
cintura, "Gomu Gomu", esfera azul girando na palma, "Gear", "Rasen-"). Mesmo cuidado com
menus: mesma organização (cards, abas, ficha completa), identidade visual nossa.

## 2. Objetivos, não-objetivos, anti-objetivos

**Objetivos da v1**
- Uma partida clássica completa, **solo e co-op 2–4**, divertida do começo ao fim.
- 3 heróis bem diferentes de jogar.
- Menus no estilo do PokeBonk: seleção com ficha completa, preparação de partida, pausa
  com estatísticas, glossário.
- Leve: rodar liso em celular com 4 jogadores e ~200 inimigos na tela.
- Progresso salvo (moeda permanente, desbloqueios, recordes).

**Não-objetivos da v1 (vêm em atualizações)**
- Sobrevivência infinita, Mutação do Dia, eventos sazonais, temporadas, roleta,
  caderno de coleção, guarda-roupa, matchmaking público, mais mapas, lobby 3D.
- **Clãs**: entram no jogo **[Diego]**, numa etapa logo depois da v1 (ver seção 16).

**Anti-objetivos (se acontecer, falhou mesmo funcionando)**
- Herói que qualquer um olha e diz "é o Goku com outro nome".
- Lag/travamento com muitos inimigos ou derrubada do servidor no co-op.
- Pagar pra ganhar (Robux comprando poder).
- Tela poluída a ponto de não ver o próprio personagem.

## 3. Estrutura no Roblox

- **2 places na mesma experiência**:
  - **Menu** **[Diego: sem lobby 3D por enquanto]**: o jogador entra direto numa tela de
    menus em tela cheia (estilo PokeBonk) com um cenário animado de fundo; não vê outros
    jogadores andando. Aqui ficam seleção de herói, preparar partida, co-op (sala com
    código), clã, laboratório, loja, conquistas, tarefas, ranking e configurações.
  - **Partida** (servidor reservado com `ReserveServer` + `TeleportService`): 1 grupo de
    1–4 jogadores por servidor.
- Grupo: "Criar sala" gera **código de 4 dígitos**; amigos entram com o código ou
  convite; o líder escolhe mapa e dificuldade. Solo = sala de 1.
- Estrutura de código segue o `CLAUDE.md` (Shared / Server/Systems / Client/Controllers,
  `init()`/`start()`).

## 4. Loop de uma partida (modo Clássico)

1. Menu → herói → **Preparar partida** (mapa, dificuldade, "Mochila" de consumíveis) →
   Começar → teleporte.
2. Mapa com **3 zonas + Santuário** (chefe final). Cada zona é uma área do mesmo mapa,
   separada por portais/barreiras.
3. Em cada zona: hordas crescentes; matar dá **orbes de XP** e **moedas**; level-up
   oferece **3 cartas**; explorar acha **baús** (custam moedas), **santuários de bênção**
   (ficar no círculo carregando), **mercador** e o **altar do guardião**.
4. Jogador invoca o **guardião** quando quiser (sorteado entre 3 por zona). Ao vencer,
   cai a **recompensa** (baú especial) e abre o **portal** pra próxima zona.
5. Timer de **10:00 por zona**: ao zerar começa o **Cerco Final** (pressão sem fim) —
   punição por enrolar, não condição de vitória.
6. Santuário: chefe final da região. Vencer e entrar na saída = **vitória**.
7. Tela de resultado (abates, dano, tempo, build) → moeda permanente → volta ao lobby.

**Co-op** (regras do gênero que funcionam bem):
- Cada jogador tem a **própria horda** (spawn em volta de cada um); juntos, somam.
- **Guardiões e chefes são do grupo** e têm vida escalada pelo nº de jogadores.
- Caiu → fica caído; aliado **revive segurando E** ao lado (3 s). Todos caídos = derrota.
- XP e moedas: cada um pega o seu (coleta individual) — evita briga; ofertas de level-up
  são individuais e **não pausam** o jogo no co-op (5 s de proteção ao abrir as cartas).
- Portal só avança quando todos os vivos entram (ou contagem de 10 s após o primeiro).

## 5. Os 3 heróis da v1

Todos: passiva que escala por nível, **kit de 4 golpes** que libera por nível (inicial,
nv 2, nv 4, nv 7), **2 despertares** durante a partida (nv 20 e nv 40: visual muda,
stats sobem, golpes ganham efeito), **ultimate** (tecla R) que carrega com dano causado,
com 3 versões (base / despertar 1 / despertar 2).

> Revisão 2026-10-29: o Diego não gostou da 1ª versão (muito diferente dos animes).
> Esta versão mantém **poderes e personalidade** dos arquétipos e muda só o que
> identifica o personagem (ver regra na seção 1). **Nomes definidos pelo Diego: Ryuga,
> Kaizo, Haruto.** Nomes exibidos no jogo em inglês.

### 5.1 Lutador de Ki — nome de trabalho **Ryuga** (opções: Ryuga, Daigo, Kenta)
- **Poder/personalidade (arquétipo)**: artista marcial alegre e meio ingênuo, vive pra
  achar alguém mais forte que ele; treina até cair no sono em qualquer lugar. Dispara rajadas de ki, raio de energia
  carregado, se teletransporta e **se transforma em estágios com aura**.
- **Visual (nosso)**: cabelo castanho-avermelhado espetado pra trás, gi **branco** com
  faixa preta, munhequeiras vermelhas, cicatriz no queixo, botas de treino.
- **Transformações**: nv 20 **Aura Carmesim** (aura vermelha flamejante, olhos vermelhos,
  reflexos vermelhos no cabelo) → nv 40 **Aura Celestial** (aura prata-branca com raios,
  cabelo prateado).
- **Elemento**: Ki. **Classe**: Brigão.
- **Passiva — "Sangue de Guerreiro"**: +1% dano por nível; com menos de 40% de HP,
  +30% dano e +20% velocidade de ataque (fica mais forte apanhando).
- **Kit**: Rajada de Ki (projéteis no mais próximo) · Chuva de Socos (rajada em cone na
  frente) · Passo Instantâneo (some e reaparece atrás de um inimigo com um chute em
  área) · Canhão de Ki (raio contínuo carregado; pose: um braço estendido segurando o
  pulso com a outra mão).
- **Ultimate**: Explosão de Ki (base) → Meteoro Carmesim (sobe no ar e despenca num
  impacto enorme) → Raio Celestial (raio gigante disparado do céu pra baixo).

### 5.2 Pirata elástico — nome de trabalho **Kaizo** (opções: Kaizo, Rikimaru, Joe)
- **Poder/personalidade (arquétipo)**: capitão pirata de **corpo elástico**,
  escandaloso e sem noção de perigo; quer ter o navio mais rápido dos sete mares e
  coleciona bússolas quebradas. Socos e chutes que esticam, rajadas de socos, se
  arremessa como estilingue.
- **Visual (nosso)**: cabelo verde-água bagunçado, **bandana amarela** com uma caveira
  sorridente própria, regata listrada azul e branca (marinheiro), casaco de capitão
  azul-marinho jogado nos ombros, bermuda e sandálias, curativo no nariz.
- **Transformações**: nv 20 **Modo Mola** (braços e pernas com espirais douradas,
  velocidade e ataque muito mais rápidos) → nv 40 **Modo Tempestade** (corpo carregado
  de relâmpagos, cada soco dá choque em cadeia).
- **Elemento**: Impacto. **Classe**: Tanque/brigão.
- **Passiva — "Corpo de Borracha"**: +2 armadura por nível; **imune a empurrão**;
  projéteis inimigos têm 10% de chance de quicar de volta.
- **Kit**: Soco Estilingue (braço estica em linha e volta, perfura) · Metralhadora de
  Socos (rajada em cone) · Chicote de Perna (chute esticado em arco 360°) · Bala de
  Mola (se arremessa e quica entre inimigos).
- **Ultimate**: Soco Canhão (base) → Chuva de Punhos Gigantes → Martelo do Capitão
  (punhos enormes martelam a área inteira).

### 5.3 Ninja de clones — nome de trabalho **Haruto** (opções: Haruto, Sora, Kenji)
- **Poder/personalidade (arquétipo)**: ninja confiante e brincalhão, teimoso, que adora
  pregar peças nos mestres; fez um **pacto com um espírito lobo** que o acompanha. Faz
  **clones**, usa kunai e shuriken, e técnicas de vento.
- **Visual (nosso)**: cabelo **azul-escuro** espetado, macacão **verde-escuro** com
  detalhes amarelos, **cachecol vermelho** comprido, faixa na testa com símbolo de **lua
  crescente** (nosso clã), luvas sem dedos, bolsa de kunais na perna.
- **Espírito parceiro**: um **lobo de trovão** (não raposa, não selado no corpo).
- **Transformações**: nv 20 **Manto do Lobo** (aura azul-elétrica em forma de lobo,
  olhos amarelos) → nv 40 **Despertar da Fera** (lobo gigante de trovão luta junto).
- **Elemento**: Vento. **Classe**: Invocador/assassino.
- **Passiva — "Exército de Um"**: a cada 8 s cria um **clone** que luta por 6 s
  copiando o último golpe (máx. 1 clone, +1 por transformação); +0,5% evasão por nível.
- **Kit**: Chuva de Kunai (projéteis teleguiados) · Shuriken de Vento (shuriken
  gigante que vai e volta) · Selo Explosivo (kunai com selo que explode no chão) ·
  Lâmina de Vento (onda cortante em cone).
- **Ultimate**: Ataque dos Mil Clones (base) → Uivo do Lobo (onda de trovão em círculo)
  → Fera Libertada (o lobo gigante atravessa a tela).

## 6. Sistemas de combate

- **Slots**: 3 de golpe (4º via meta-progressão) + 3 de **Pergaminhos** (cartas de
  atributo, o nosso "Tome/vitamina"; 4º via meta) + itens sem limite (com teto por item).
- **Cartas de level-up** (3 opções; raridade Comum/Incomum/Raro/Épico/Lendário):
  golpe novo · subir nível de golpe · Pergaminho novo/subir · (itens só por baú/mercador).
- **Golpe nv 1 → 8**: dano dobra até o nv 8; cada nível sorteia 2 melhorias (3 em
  épico/lendário) de uma lista do golpe (dano, recarga, quantidade, perfuração,
  velocidade, crítico, ricochete, área, duração).
- **[Diego] Golpes chegam por carta**, como no Megabonk/PokeBonk: o herói começa só com
  o golpe inicial; os outros golpes do kit **não liberam sozinhos** — a partir do nível
  mínimo de cada um (nv 2, 4, 7) passam a poder aparecer nas cartas de level-up e o
  jogador escolhe se pega.
- **Fontes de golpe**: kit próprio (mais frequente) + **golpes genéricos de elemento**
  (pool compartilhado; cada herói desbloqueado acrescenta golpes do elemento dele ao pool
  de todos).
- **Fusão (Técnica Combinada)**: dois golpes nv 8 + um "Altar de Fusão" no mapa →
  golpe novo, libera um slot. v1: só **fusão de assinatura** (2 golpes do kit do mesmo
  herói, 1 por herói) e **fusão de elemento** (2 golpes do mesmo elemento).
- **Pergaminhos v1 (12)**: Dano, Vel. de ataque, Projéteis, Área, Duração, Crítico,
  HP máx., Armadura, Regeneração, Velocidade, Coleta, XP. Nível 1–10; cada nível +10%
  (comum) a +21% (lendário). + **Pergaminho Amaldiçoado** (mais inimigos e mais fortes,
  mais XP/moedas) como escolha de risco.
- **Itens v1 (~24)**: mistura de atributo, condicional, ao acertar, ao matar, ao apanhar,
  economia, e 3–4 lendários que mudam regras. Lista detalhada fica pro plano.
- **Elementos v1 (6)**: Ki, Impacto, Vento (heróis) + Fogo, Água, Sombra (inimigos e
  itens; heróis futuros). Sem tabela de vantagem/resistência na v1 (simplifica);
  **reações** sim:
  - Molhado + Vento = **Tempestade** (espalha Molhado e paralisa); Queimado + Vento =
    **Incêndio** (espalha queimadura);
  - Atordoado + Ki = **Ruptura** (dano ×2); Queimado + Água = **Vapor** (confunde/lento);
  - Amaldiçoado + Impacto = **Estilhaço** (explode em área).
- **Status v1**: Queimado, Molhado, Atordoado, Amaldiçoado, Lento. Chefes resistem.
- **Fórmulas**: bônus da mesma origem somam, origens diferentes multiplicam; armadura =
  a/(a+45); evasão máx. 60%; crítico ×1,75; recarga mínima 0,12 s. Tudo no `Config`.

## 7. Mapa da v1 — "Vale das Cerejeiras Partidas"

- Tema anime clássico: vila de montanha com cerejeiras, templo, ponte, floresta de bambu.
- Zona 1 Vila (aberta, fácil) → Zona 2 Bambuzal (corredores, emboscadas) → Zona 3
  Ruínas do Templo (verticalidade, escadas) → **Santuário**: chefe final "Oni do Eclipse".
- 3 guardiões possíveis por zona (sorteados) — v1 pode começar com 1 por zona e crescer.
- Inimigos v1 (~8 tipos): yokais/espíritos e bandidos — lanterna-fantasma, tanuki
  travesso, ninja renegado, samurai de palha, kappa, corvo-tengu pequeno, golem de pedra,
  espírito de raposa **não** (evitar referência a raposa de nove caudas).
- Geometria estática no place (regra do `CLAUDE.md`); pontos de spawn/baús/altares como
  marcadores no mapa, sorteados por script.
- Dificuldades: Normal ×1, Difícil (inimigos +70%, ×1,75 moeda), Pesadelo (+160%, ×2,5,
  libera vencendo o Difícil).

## 8. Visual e desempenho (decisões técnicas)

- **Inimigos = sprites 2D**: o servidor simula inimigos **como dados** (posição, vida,
  estado) sem Parts físicas; envia snapshots compactos ~10×/s; cada cliente desenha os
  inimigos próximos com **sprites sempre virados pra câmera** (pool de quads/
  BillboardGui com sprite sheet animado: andar, atacar, levar dano, morrer).
  "Inimigos desenhados" configurável (todos / próximos / muito próximos), como no
  PokeBonk.
- **Projéteis/efeitos**: simulados no cliente pra visual; **dano decidido no servidor**
  (servidor calcula acerto pelas posições que ele mesmo simula).
- **Heróis** **[Diego: 2D]**: sprite 2D animado (andar, atacar, levar dano, cair,
  pose de ultimate, 1 conjunto por transformação), com o personagem Roblox invisível por
  baixo pra física/movimento.
- **Mundo**: 3D low-poly colorido; câmera 3ª pessoa alta (ajustável), FOV e distância
  nas configurações.
- **Arte dos sprites**: criada por nós (gerador de imagem + ajuste) e enviada como asset
  do dono da experiência. Pipeline a definir no plano.
- Tetos no `Config`: inimigos vivos por jogador, projéteis, partículas.

## 9. Menus (layout inspirado no PokeBonk, identidade nossa)

- **Tela inicial**: botão grande JOGAR (modo Clássico), Co-op (criar sala/entrar com
  código), atalhos: Heróis, Laboratório, Loja, Conquistas, Tarefas, Classificação,
  Configurações. Moedas no topo.
- **Seleção de herói ("Dojo")**: ficha completa — retrato animado, classe, elemento,
  despertares por nível, stats base → stats na partida (com tooltip), passiva, kit de
  golpes com números, ultimates, minhas estatísticas com o herói; grade de heróis à
  direita (bloqueados = silhueta + desafio).
- **Preparar partida**: mapa, guardiões por zona, dificuldade, recordes, Mochila,
  Começar.
- **HUD**: retrato/nível/despertar, timer da zona, abates/moedas, minimapa, barra de HP,
  slots de golpe e Pergaminho, ultimate com anel de recarga, marcadores de aliados.
- **Pausa**: tempo/abates/dano/DPS; golpes com dano por golpe; itens; Pergaminhos;
  estatísticas completas (verde = acima da base); glossário; Desistir/Configurações/
  Continuar (no co-op a pausa não para o jogo).
- **Glossário** dentro do jogo (stats, status, reações, formas de golpe, fusões).
- **Configurações v1**: som, gráficos (qualidade, inimigos desenhados, opacidade dos
  meus ataques e dos aliados, tremor de tela, reduzir clarões), controles (mira
  automática/manual), interface (tamanho, números de dano), toque/teclado/controle.
- Paleta e estilo próprios (ex.: tons de tinta/papel japonês, cantos com pincelada) —
  definir com mockups antes de construir.

## 10. Meta-progressão (v1 enxuta)

- **Moedas** (na partida): baús, mercador. **Essência** (permanente): fim da partida ×
  dificuldade, conquistas, tarefas.
- **Laboratório → "Dojo de Treino"**: melhorias permanentes pequenas (dano, HP,
  velocidade, XP, sorte, coleta) + ferramentas (Rerolar, Pular, Banir, 4º slot de golpe,
  4º slot de Pergaminho, 4ª carta).
- **Desbloqueios**: Ryuga liberado; Kaizo e Haruto por **desafio** (ex.: vencer a
  região no Normal; derrotar 2.000 inimigos com golpes de Ki...). Itens entram no pool
  comprando com Essência.
- **Conquistas** (~30) e **tarefas diárias** (3 + prêmio + sequência).
- **Classificação** v1: melhor tempo de vitória e mais abates (solo e grupo), via
  OrderedDataStore.
- DataStore com retry, autosave + BindToClose, schema versionado (regra do `CLAUDE.md`).

## 11. Monetização

- **[Diego] Segundo Fôlego (pago)**: quando o jogador cai, aparece a oferta de levantar
  na hora com HP parcial e alguns segundos de invulnerabilidade (Developer Product em
  Robux). Proposta do Claude: limite de **1 por partida** por jogador.
- **[Diego] Tela de "todos caíram" (15 s)**: quando o grupo inteiro cai, aparece contagem
  de **15 s** com dois botões: **"End Match"** (finalizar, vai pro resultado) e
  **"Revive All"** (pago: revive o grupo todo). Se o tempo zerar sem escolha =
  finalizar. No co-op, qualquer jogador pode pagar o "Revive All" pra todos.
  Proposta do Claude: limite de **1 "Revive All" por partida**; o servidor confirma a
  compra (`ProcessReceipt`) antes de reviver; o jogo fica **pausado pra todos** durante
  os 15 s.
- Proposta do Claude pra manter o ranking justo: partidas que usaram reviver pago
  aparecem com um ícone no ranking (ou ficam num ranking separado) — decidir.
- Resto proposto pelo Claude: **cosméticos** (visuais alternativos de herói, efeitos de
  ultimate, molduras/títulos) e VIP com +espaço de Mochila. Heróis **não** vendidos por
  Robux (desbloqueio jogando).

## 11.1 Idioma

- **[Diego]** Jogo **em inglês** (idioma de origem) com **tradução pra português**.
- Proposta do Claude: tradução pt-BR feita por nós numa tabela de localização do Roblox
  (não depender só da tradução automática, que erra nomes de golpes); demais idiomas
  pela tradução automática do Roblox.

## 12. Segurança

- Servidor decide tudo: dano, XP, moedas, cartas oferecidas, sorteios, compras, reviver.
- Cliente manda só: input de movimento (Roblox já replica), índice da carta escolhida,
  interações (com checagem de distância), escolha de mira.
- Rate-limit e validação em todos os remotes (regra do `CLAUDE.md`).

## 13. Ordem sugerida de construção (o plano detalha)

1. Partida mínima solo: 1 herói (Ryuga), inimigos sprite simulados no servidor, XP,
   level-up com cartas, 2 golpes, morte/vitória numa zona.
2. Zonas + guardião + portal + santuário + timer/Cerco Final.
3. Kaizo e Haruto, Pergaminhos, itens, baús, mercador, status e reações.
4. Co-op (sala com código, hordas por jogador, chefe escalado, reviver segurando E,
   tela de 15 s "End Match / Revive All", Segundo Fôlego pago).
5. Place de menu + menus completos + DataStore + meta-progressão.
6. Polimento visual (sprites finais, efeitos, ultimates), configurações, conquistas,
   tarefas, ranking, tradução pt-BR.
7. Clãs (seção 16).

---

## 14. Perguntas que eu faria (e a resposta que assumi)

1. **Qual o nome final do jogo?** → **[Diego]** AnimeBonk.
2. **Os 3 heróis estão no ponto certo?** → **[Diego]** queria mais parecido; revisado na
   seção 5 (mesmo poder e "vibe", visual e nomes nossos). Falta escolher os nomes.
3. **Heróis em 2D (sprite) ou 3D?** → **[Diego]** 2D sprite, igual aos inimigos.
4. **Quem faz a arte (sprites, ícones)?** → Assumi geração por IA + ajustes, publicados
   pelo dono da experiência. Você desenha ou tem alguém?
5. **Celular é prioridade?** → Assumi que sim (público Roblox) — UI e desempenho pensados
   pra celular desde o início.
6. **Co-op já na primeira versão?** → Assumi que sim (é o diferencial que você citou),
   mas construído depois do solo funcionar.
7. **Lobby 3D ou só menu?** → **[Diego]** só menu, como o PokeBonk, por enquanto.
8. **Dono da experiência: conta pessoal ou grupo?** → **[Diego]** grupo novo do Roblox.
9. **Vai monetizar? Como?** → **[Diego]** Segundo Fôlego e Revive All pagos; resto
   cosmético (seção 11).
10. **Público-alvo/idade?** → Assumi 10–16 anos, violência estilizada sem sangue.
11. **Tamanho da partida** → Assumi ~25–35 min pra vencer a região (3 zonas de ~8 min).
12. **Quanto tempo/ritmo de desenvolvimento?** → Sem prazo assumido; v1 em etapas
    (seção 13), você testa cada etapa.
13. **Mapa da v1 é tema japonês?** → Assumi vila/templo japonês (combina com anime).

## 15. Ideias extras que achei legais (não estão na v1, só sugestão)

- **Golpe conjunto no co-op**: dois heróis com ultimate cheia perto um do outro →
  aparece prompt de **Ultimate Combinada** (animação dupla). Muito "anime".
- **Rival da run**: um "herói rival" NPC aparece em uma zona aleatória, luta contra você
  e, se perder, larga um item raro (vibe de rival de shonen).
- **Abertura de anime**: ao começar a partida, uma "abertura" de 3 s com os retratos do
  grupo e o nome do mapa estilo título de episódio ("Episódio 1: O Vale das Cerejeiras").
- **Placar de "episódios"**: cada vitória vira um episódio no perfil, com título gerado
  pela run ("O dia em que Mako derrotou 3.000 yokais").
- ~~Despertar no limite~~ → virou o **Segundo Fôlego pago** (seção 11) **[Diego]**.
  Sugestão: quando usar, tocar fala + zoom no herói (o momento clichê de anime).
- **Lobby como vila** (pra quando houver lobby): a vila do mapa 1 em paz, com NPCs que
  são os lojistas/menus.
- **Sazonal**: eventos como "Festival de Verão" (fogos, yukata como visual) e
  "Noite dos Yokais" (Halloween).

## 16. Clãs (etapa 7, depois da v1) **[Diego]**

Modelo: o sistema de clãs do PokeBonk (ver `docs/pokebonk-referencia.md` §16).
Proposta do Claude pra nossa versão:
- **Fundar**: custa Essência; nome + sigla (até 4 letras, aparece antes do nome nos
  rankings e no perfil) + emblema montado com peças (forma, símbolo, cor).
- **Membros**: começa com 30 vagas, ampliável até 100 (Roblox: DataStore por clã com
  lista de membros; filtro de texto obrigatório do Roblox em nome/sigla/descrição).
- **Entrada**: aberta / por pedido (líder ou oficial aceita) / só convite. Cargos:
  líder, oficial, membro.
- **Pontos de clã**: cada partida válida de um membro soma (abates, guardiões, chefes,
  vitórias; mais no Difícil/Pesadelo).
- **Ranking de clãs** por temporada; top clãs ganham Essência e enfeites de emblema.
- **Missões semanais do clã** (3) — ideia pra uma segunda fase dos clãs, junto com
  rivalidade entre clãs e mural de conversa (o mural precisa usar o filtro de chat do
  Roblox).
- Telas: Buscar clã (filtros aberto/com pedido), Meu clã (membros, pontos, cargos),
  Ranking de clãs, caixa de entrada pra convites e pedidos.
