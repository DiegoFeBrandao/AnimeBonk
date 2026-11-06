# Inimigos ninja (16–20 tipos, elites, mini-chefes, 4 guardiões novos) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Trocar o bestiário atual (yokai/vila de cerejeiras) por um bestiário **ninja
original** que combine com o mapa do lote `2026-10-30-mapa-ninja` (Shinobi Village →
Forest of Trials → Fallen Fortress → Sealed Shrine): 16–20 inimigos comuns (4–5 por zona),
elites e mini-chefes reaproveitando os 6 comportamentos que já existem, e **4 guardiões +
chefe final** com arte nossa inspirada em folclore (raposa de nove caudas, sapo gigante,
cobra branca, lesma gigante, demônio selado). Pedido do Diego (2026-10-30): "primeira run e
mobs vão ser ninjas"; "os boss podem ser por exemplo monstros que nem a 9 caudas, gamabunta"
— sem nomes/visuais da obra (regra do `CLAUDE.md`), só o arquétipo folclórico.

**Architecture:**
- Tudo **dado** em `Definicoes/Inimigos` e `Definicoes/Chefes` (comportamentos existentes:
  perseguir, rápido, tanque, atirador, explosivo, invocador). Comportamentos novos só se
  caberem como dado: `teleporte` (some e reaparece atrás do jogador a cada N s), `clone`
  (ao levar dano divide em 2 cópias fracas), `marionete` (invocador que fica longe). Máx. 3
  comportamentos novos, cada um com seu campo no `InimigoDef` e um bloco no `InimigoSystem`.
- Lista proposta (nomes em inglês, ids em português):
  - Village: Rogue Genin (perseguir), Kunai Thrower (atirador), Shield Bruiser (tanque),
    Smoke Runner (rápido), Paper Bomb Carrier (explosivo).
  - Forest: Leaf Hopper (rápido), Vine Puppeteer (invocador/marionete), Poison Moth
    (atirador, aplica Amaldicoado), Bark Golem (tanque), Mirror Clone (clone).
  - Fortress: Armored Ashigaru (tanque), Crossbow Sentinel (atirador), Shadow Stalker
    (teleporte), Siege Bomber (explosivo), Warlord's Herald (invocador).
  - Shrine: Sealed Wraith (perseguir, fantasma), Masked Assassin (teleporte), Cursed
    Monk (atirador), Chain Guardian (tanque), Seal Fragment (explosivo).
- Guardiões (1 por zona, sorteável entre 2 no futuro): **Great Toad Elder** (sapo gigante,
  língua em linha + pulo em área), **White Serpent** (cobra, investida + veneno), **Nine-
  Tailed Fox** (raposa, 9 projéteis em leque + fogo), **Giant Slug** (lesma, lama que
  atrasa + regen). Chefe final: **Sealed Demon** (demônio selado do santuário, 3 fases).
  Mini-chefes por zona = versões elite grandes dos comuns (já existe).
- Modelos 3D por `generate_mesh` (reaproveitar o pipeline do lote arte: `ReplicatedStorage/
  Modelos/Inimigos|Chefes/<id>`, atributos `GiroY`, pivô no pé); fallback = recolorir um
  modelo existente. Elites continuam com aura.
- Balanceamento inicial: copiar os números dos tipos equivalentes atuais e escalar por zona
  (HP ×1 / ×1,6 / ×2,5 / ×3,5), dano por zona idem; o Diego ajusta depois.
- Replicar `Definicoes/Inimigos`/`Chefes` no Menu (tela Prepare match mostra guardiões).

**Spec:** §7 (inimigos), referências Megabonk §10 (chefes), PokeBonk §2.

## Review Focus
1. Comportamentos novos não quebram o snapshot binário (15 bytes) nem o pool de render.
2. `clone` não explode a contagem (teto de inimigos vivos do `Config` respeitado; clones não dão XP cheio).
3. `teleporte` nunca cai fora da zona/dentro de obstáculo (usa `Alturas.em` e o limite da zona).
4. Guardiões com 2–3 padrões de ataque legíveis (aviso no chão antes do golpe) e barra/nome corretos.
5. Nenhum nome/visual identificável de obra existente.

### Task 1: Definições (inimigos, chefes, zonas → lista de tipos) nos 2 places + `TesteLogica` (pesos por zona somam, ids únicos).
### Task 2 (Partida): comportamentos novos no `InimigoSystem` (teleporte, clone, marionete) + padrões dos guardiões no `ChefeSystem`.
### Task 3: modelos 3D (≤ 25 meshes) + render/efeitos (avisos no chão, projéteis novos).
### Task 4: teste em Play por zona + revisão + docs.
