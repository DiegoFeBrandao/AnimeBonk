# HUD da run, cartas detalhadas, pausa, mapa com descoberta e evolução — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Levar a partida ao padrão das telas de referência do PokeBonk (só a **estrutura**;
arte/nomes nossos): `C:\Users\Diego\Desktop\pokebonk\20. em partida.png` (HUD), `21. up em
partida.png` (cartas de level-up), `22. pausa em partida.png` (pausa), `23. mapa no tab.png`
(mapa da zona no Tab) e `24. mapa grande pelas configurações ou M.png` (mapa grande em M com
lista "Discovered in this zone"). Mais a **evolução do herói** em 2 estágios com troca de
modelo e tela de evolução. Pedido do Diego (2026-10-30): "os itens quando aparece com
descrições, pular, bloquear e atualizar... mostrando dano e tudo mais"; "a pausa como mostra
as coisas bonitas"; "o mapa no TAB ou M que tem dois formatos e só vão aparecendo os ícones
do que você passou perto... para o coop libera também"; "pode ser sim essa evolução".

**Architecture (tudo cliente, salvo o marcado):**
- **HUD** (tela 20): canto sup. esq. retrato redondo + nome + elemento (chip) + "Lv N" +
  "Next form: Lv 20"; topo-centro: nome da zona, "Zone 1/4", dificuldade (chip), **timer
  da zona** grande, cronômetro total e recorde do mapa; linha abaixo: moedas, itens, abates;
  sup. dir. **minimapa redondo** (N/S/E/W, seta do jogador, ícones descobertos, inimigos
  como pontos); inf. esq. 4 slots de golpe (ícone, nível) + 4 slots de pergaminho menores
  + anel da ultimate com "R" e nome; barra de HP sob o herói (já existe) + anel de seleção;
  combo à direita. Contadores com rolagem (`Juice.contar`). Tudo abaixo do Inset.
- **Cartas de level-up** (tela 21): título "Level N!"; 3 cartas com cabeçalho na cor da
  raridade (chip "Attack"/"Common"… + "NEW"), ícone grande, nome, subtítulo ("New attack" /
  "New scroll" / "Scroll Lv 3 → 4"), chips de tags (elemento, forma), **descrição**,
  **números** (Damage, Cooldown, Range/Area, status %) e **antes → depois** em verde para
  pergaminhos/golpe que sobe; tecla [1][2][3]; botões **Reroll (N) F**, **Skip (N) X**, **Ban
  (N) Z** com contadores por run (`Config.RerollsPorRun 2`, `SkipsPorRun 5`, `BansPorRun 3`;
  Skip dá moedas pequenas; Ban remove a carta do pool da run) — **servidor** valida
  (`LevelUpSystem`: remotes `RerollCartas`, `PularCartas`, `BanirCarta`, rate-limit, contadores
  no estado do herói); chip "Vine Whip Lv 1" vira "selected build" resumido; linha "Affects"
  do lote de itens quando existir.
- **Pausa** (tela 22, Esc): cabeçalho (retrato, nome, chips, HP/EXP barras, "PAUSE · zona ·
  dificuldade") + tiles (Time, KOs, Damage, DPS, Coins, Best combo); 3 colunas **Attacks**
  (passiva + cada golpe com nível, tags, Damage/Cooldown/Range, status %, descrição, barra
  de % do dano total, dano total, DPS 15 s), **Items** (lista com ícone ×N, "Scrolls x/4"),
  **Stats** (Attack / Defense / Utility, verde = acima da base, tooltip); rodapé com dicas de
  tecla; botões Give up / Restart / Big map / Settings / Continue. Dano por golpe: o
  servidor já tem o acerto — `DanoController` recebe `golpeId` no payload de dano (ver se já
  vem; se não, acrescentar 1 byte/entrada) e acumula no cliente. **Solo:** pausa de verdade
  (servidor congela a partida se só há 1 jogador: `PartidaSystem.pausar` + remote, rate-limit)
  ; **co-op:** só o painel.
- **Mapa da zona** (telas 23/24): `MapaController`. Imagem do chão = **grade de cores**
  gerada no cliente a partir de `Alturas` (verde por altura, marrom nas faces > 25°, azul nas
  lagoas marcadas em `Zonas.lagoas`) desenhada uma vez por zona em Frames de 6×6 (150×150 =
  22 500 frames é demais → usar `EditableImage` se disponível no cliente; senão grade 30×30 de
  Frames coloridos, 900 frames, criados uma vez e reutilizados). **Tab** segura = quadrado no
  centro com N/S/E/W, seta do jogador, ícones; **M** = tela grande com zoom +/−/1:1, arrasto,
  lista "Discovered in this zone" com contagem por tipo e legenda. **Descoberta**: ícone só
  aparece depois de algum jogador passar a < `Config.RaioDescoberta 60` studs; exceções
  sempre visíveis: altar do guardião, portal (quando ativo), mercador. **Servidor** decide a
  descoberta (`DescobertaSystem`: checa a cada 0,5 s a distância de cada jogador a cada
  objeto da zona, manda `Descoberto {tipo, id, x, z}` a **todos** — co-op compartilha) e o
  cliente só desenha; minimapa reaproveita a mesma lista. Objetos: baús (pagos/grátis),
  mercador, altar, portal, mini-chefe, jaulas/altares extras quando existirem. Marcas do
  jogador (até 3, locais) opcional, só se sobrar tempo.
- **Evolução**: `Herois.despertares[i]` ganha `modelo` e `name`; `HeroiSpriteController`
  troca o modelo com flash branco + "EVOLVED! Ryuga → Crimson Ryuga" 1,5 s; modelos por
  `generate_mesh` (3 heróis × 2 estágios), fallback = modelo base com tinta/aura; Menu mostra
  os 3 estágios na ficha do herói. Co-op vê a evolução dos outros (atributo `Despertar` já
  replica).

**Spec:** §9 (HUD, pausa), PokeBonk §7, §17; referências visuais acima.

**Pendência herdada da revisão dos itens (I1):** a `CartaUI` atual fica ilegível no celular
(844×390: descrição com 6 px por linha, chip "Affects" de 15×14 px, dica só por `MouseEnter`).
A carta nova deste lote precisa de modo compacto para tela baixa (ou 2 linhas de cartas),
`UITextSizeConstraint.MinTextSize ≥ 11`, dica também por `Activated`, e a loja com 5 cartas
idem. Medir em 1341×650 e 844×390.

## Review Focus
1. Reroll/Skip/Ban: só o servidor conta; sem carta pendente → ignorado; Ban não remove o último golpe possível; contadores zeram no Play Again.
2. Descoberta vem só do servidor; objeto sorteado depois (mini-chefe, baú grátis) entra na lista; co-op: entrou tarde recebe a lista inteira.
3. Mapa: nada por frame além da seta/pontos (ícones só mudam por evento); 900 frames no máximo por zona; Tab não trava o input de movimento.
4. Pausa solo congela inimigos/projéteis/timer no servidor e o cliente para de prever; despausa sem salto; co-op nunca congela.
5. Evolução no mesmo frame da morte / Play Again volta ao modelo base; prateleira e cartas cabem no celular.

### Task 1: HUD (topo, retrato, slots, minimapa vazio, contadores) + Inset.
### Task 2: Cartas de level-up detalhadas + Reroll/Skip/Ban (servidor + cliente) + `TesteLogica`.
### Task 3: Pausa completa (+ pausa real em solo) + dano por golpe.
### Task 4: `DescobertaSystem` + `MapaController` (Tab, M, minimapa com ícones) + `Zonas.lagoas`.
### Task 5: Evolução (definições, 6 modelos, troca, tela) nos 2 places.
### Task 6: teste em Play + revisão + docs.
