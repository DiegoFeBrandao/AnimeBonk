# Etapa 3b — Pergaminhos completos, raridade, moedas, baús, mercador — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** As cartas ganham os 12 Pergaminhos da spec + Pergaminho Amaldiçoado e raridade;
inimigos soltam moedas; cada zona tem baús (custam moedas, dão cartas) e um mercador
(vende pergaminho, melhoria de golpe e cura).

**Architecture:** Pergaminhos viram dados com `porNivel`; `Logica/Dano` expõe
`mult/extra/flat/critico` por id e os sistemas leem só por aí. Raridade é sorteada por carta
(`Logica/Cartas`) e só muda quantos níveis a carta dá. Moedas são orbes do `XpSystem` com
`tipo`. Baús e mercador são spawnados em marcadores estáticos do place
(`Zonas/<zona>/Baus/BauN`, `Zonas/<zona>/Mercador`) por `BauSystem`/`MercadorSystem`, criados
por zona. Loja é uma oferta guardada no servidor; o cliente manda só o índice.

**Spec:** `docs/superpowers/specs/2026-10-29-animebonk-design.md` §4 item 3, §6 (Pergaminhos,
fórmulas), §13 item 3. Decisões de design desta etapa tomadas pelo Claude (autorizado pelo
Diego nesta sessão, 2026-10-29).

## Global Constraints

Mesmas das etapas 1–3a. Nomes em inglês nossos: Power/Speed/Volley/Reach/Lasting/Critical/
Vitality/Iron/Mending/Swift/Magnet/Wisdom/Cursed Scroll.

## Review Focus

1. Comprar no baú/loja sem moedas, com índice inválido, duas vezes seguidas, ou longe →
   recusado; moedas nunca ficam negativas.
2. Pergaminho Amaldiçoado muda spawn/HP imediatamente e o multiplicador some no Play Again.
3. Baús e mercador da zona anterior somem na troca de zona e no Play Again; prompt não fica
   pendurado.
4. Raridade lendária perto do nível máximo não ultrapassa o teto (nível 10 / golpe 8).
5. Moedas: orbe de moeda não dá XP; com teto de orbes, moeda soma na orbe mais antiga do mesmo tipo.

---

### Task 1: Definições, Config, Types, Dano, Cartas, remotes
- `Definicoes/Pergaminhos`: `{ name, descricao, porNivel, nivelMax?, amaldicoado? }` — 13 ids:
  Dano 0.10, VelAtaque 0.10, Projeteis 0.5 (inteiro: +1 a cada 2 níveis), Area 0.10,
  Duracao 0.10, Critico 0.04, HpMax 0.10, Armadura 4 (flat), Regen 0.3 (flat HP/s),
  Velocidade 0.05, Coleta 0.15, Xp 0.10, Amaldicoado 0.25 (nivelMax 5, amaldicoado).
- `Config`: `OrdemPergaminhos`, `RaridadePesos`, `RaridadeNiveis` (comum/incomum 1, raro/épico 2,
  lendário 3), `CriticoMult 1.75`, `CriticoMax 0.4`, `ChanceMoeda 0.4`, `MoedasComum 1`,
  `MoedasChefe 30`, `BausPorZona 3`, `CustoBauBase 20`, `CustoBauPorZona 15`, `CustoBauPorAberto 10`,
  `RaioBau 8`, `RaioMercador 10`, `PrecoLojaPergaminho 35`, `PrecoLojaGolpe 40`, `PrecoLojaCura 15`,
  `PrecoLojaMultZona 1.5`, `MaldicaoSpawn 0.25`, `MaldicaoHp 0.15`, `MaldicaoRecompensa 0.30`,
  `RateLimitLoja 0.25`.
- `Types`: `Raridade`, `Carta.raridade`, `CartaExibida.raridade/descricao`,
  `EstadoHeroiResumo.moedas`, `InfoLoja = { ofertaId, itens: { { tipo: "pergaminho"|"golpe"|"cura", id: string?, name, descricao, preco } } }`.
- `Logica/Dano`: `nivel(perg,id)`, `mult(perg,id)`, `extra(perg,id)` (floor), `flat(perg,id)`,
  `critico(perg, rng): number` (1 ou CriticoMult); `multiplicador/recarga/hpMax` passam a usar `mult`.
- `Logica/Cartas`: candidatos com os 13 pergaminhos (ordem `Config.OrdemPergaminhos`, teto
  `nivelMax or NivelMaxPergaminho`); raridade sorteada por carta; `nivelNovo = min(teto, atual + RaridadeNiveis[raridade])`;
  golpeNovo sempre comum/nível 1.
- `Server`: remotes `Loja` (s→c) e `ComprarLoja` (c→s).
- `TesteLogica`: mult/extra/flat/critico, raridade respeita teto, Cursed teto 5.

### Task 2: Marcadores no mapa (estático)
- Em cada `Zonas/<zona>`: Folder `Baus` com 6 Parts invisíveis `Bau1..Bau6` espalhados pelo
  chão (longe do spawn), e Part `Mercador` (bloco roxo 4×6×4 com BillboardGui "Merchant").

### Task 3: Servidor — stats, moedas, maldição
- `HeroiSystem`: `moedas` no estado (+ resumo), `ganharMoedas`, `gastarMoedas(player, n): boolean`,
  regen (`flat Regen`), velocidade (`mult Velocidade` no WalkSpeed), armadura flat extra,
  XP × `mult Xp` × (1 + MaldicaoRecompensa·nível Amaldicoado), `recalcularStats(player)` (HP máx + velocidade),
  evento `pergaminhoMudou(player)`, `maldicaoTotal()`.
- `LevelUpSystem.aplicar`: aplica `nivelNovo`, chama `recalcularStats` e dispara `pergaminhoMudou`;
  cartas exibidas levam `raridade` e `descricao`.
- `GolpeSystem`: Projeteis (`extra`) soma em quantidade/acertosPorUso/saltos; Area (`mult`) em
  raio/largura/alcance de cone/raioAcerto; Duracao (`mult`) em ticks; crítico por acerto (`Dano.critico`).
- `CloneSystem`: duração × `mult Duracao`.
- `XpSystem`: orbe com `tipo` (0 xp / 1 moeda); ao morrer: orbe de XP + (chance) orbe de moeda
  (`MoedasComum`, chefe `MoedasChefe`, × maldição); coleta usa raio × `mult Coleta` do jogador;
  `criados = [id, x, z, tipo, ...]`.
- `ZonaSystem.aplicarMultiplicadores`: × (1 + MaldicaoSpawn·m) e (1 + MaldicaoHp·m); reaplica em
  `pergaminhoMudou`; `iniciarZona` chama `BauSystem.gerar(modelo, indice)` e `MercadorSystem.gerar(modelo, indice)`;
  `encerrar`/`limparTudo` limpam os dois.

### Task 4: BauSystem e MercadorSystem (servidor)
- `BauSystem.gerar(modelo, indiceZona)`: sorteia `BausPorZona` marcadores, cria Part (baú) em
  `workspace.Dinamico` com ProximityPrompt "Open Chest" / ObjectText "N coins"; custo =
  `CustoBauBase + CustoBauPorZona·(indice−1) + CustoBauPorAberto·abertosNaZona`; ao abrir (distância
  checada, `gastarMoedas`): remove o baú, `LevelUpSystem.ofertaExtra(player)`; `limparTudo`.
- `MercadorSystem.gerar(modelo, indiceZona)`: prompt "Trade" no `Mercador`; por jogador e por zona,
  3 itens: pergaminho aleatório +1 (preço), melhoria do golpe mais baixo (preço), cura total
  (preço) × `PrecoLojaMultZona^(indice−1)`; `Loja` manda `InfoLoja`; `ComprarLoja(ofertaId, i)` valida
  (rate-limit, oferta, índice, distância, moedas), aplica, marca item vendido e reenvia; `limparTudo`.

### Task 5: Cliente
- `LevelUpController`: borda/faixa por raridade (comum cinza, incomum verde, raro azul, épico roxo,
  lendário dourado; faixa "RARE SCROLL" etc.), linha de `descricao`.
- `HudController`: "Coins: N" ao lado dos abates.
- `EfeitosController`: orbe de moeda dourada (tipo 1).
- `LojaController` (novo): painel com os 3 itens (nome, descrição, preço, `[1][2][3]`), "Close [Esc]";
  item vendido fica apagado; fecha ao andar longe (Loja com `itens = {}`) ou Esc.

### Task 6: Teste em Play + revisão + docs
