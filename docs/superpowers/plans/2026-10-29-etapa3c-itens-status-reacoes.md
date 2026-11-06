# Etapa 3c — Itens, status e reações — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Baús passam a dar itens (22, com raridade e teto por item); golpes têm elemento;
inimigos ganham status (Burning, Wet, Stunned, Cursed, Slowed) e reações entre status e
elemento (Tempest, Wildfire, Rupture, Steam, Shatter) com efeito visual.

**Architecture:** Status são arrays por slot no `InimigoSystem` (sem instâncias) e vão no
snapshot como 1 byte de bitmask (tint no cliente). Reações são decididas em
`InimigoSystem.danificar(id, dano, matador, elemento)` / `aplicarStatus`. Itens são dados
(`Definicoes/Itens`) com `efeito` tipado; `ItemSystem` (novo) recalcula no estado do herói um
`bonus` por stat, uma lista `aoAcertar` e `condicionais`; `Logica/Dano` aceita `bonus` opcional
e todos os sistemas que já leem pergaminhos passam a somar o bônus dos itens.

**Spec:** `docs/superpowers/specs/2026-10-29-animebonk-design.md` §6 (itens, elementos, reações,
status), §13 item 3. Lista de itens definida pelo Claude (autorizado pelo Diego nesta sessão).

## Global Constraints
Mesmas das etapas anteriores. Nomes em inglês nossos (nada de animes existentes).

## Review Focus
1. Reação em cadeia (Tempest espalha Wet → outro golpe de Vento → Tempest…) não pode explodir
   em loop no mesmo frame: espalhar status nunca dispara reação.
2. Status em chefe: duração × `ChefeResistenciaStatus`, Stunned ignorado.
3. Phoenix Feather revive só 1× por partida e zera no Play Again; não revive se a partida acabou.
4. Item no teto (`max`) não é sorteado nem dado; baú sem item possível cai na oferta de cartas.
5. Snapshot cresce 1 byte por entrada (15): cliente e servidor com o mesmo `TAM_ENTRADA`; pacote
   de 60 entradas continua < 900 bytes (6 + 60×15 = 906 → reduzir `SnapshotEntradasPorPacote` pra 55).

---

### Task 1: Definições (Itens, elemento nos golpes), Config, Types, Dano com bônus
- `Golpes`: campo `elemento: "Ki" | "Impacto" | "Vento"` (Ryuga Ki, Kaizo Impacto, Haruto Vento).
- `Definicoes/Itens` — `ItemDef = { name, descricao, raridade, max, letra, efeito }`, `efeito`:
  `{ tipo="stat", stat, valor }` · `{ tipo="aoAcertar", status, chance }` · `{ tipo="aoMatar", cura }`
  · `{ tipo="condicional", limiarHp, stat, valor }` · `{ tipo="reviver", fracHp }` · `{ tipo="critMult", valor }`
  · `{ tipo="reacaoDano", valor }`.
  Comuns (max 3): WarriorSash "Warrior Sash" +10% Dano · HourglassCharm "Hourglass Charm" +10% VelAtaque ·
  MonkBeads "Monk Beads" +10% Area · HawkFeather "Hawk Feather" +5% Critico · IronBento "Iron Bento" +10% HpMax ·
  SwiftSandals "Swift Sandals" +8% Velocidade · ScholarsBrush "Scholar's Brush" +15% Xp · LuckyCoin "Lucky Coin" +25% Moedas ·
  MagnetStone "Magnet Stone" +20% Coleta · RiceBall "Rice Ball" cura 2 HP por abate · SpiritLantern "Spirit Lantern" +0.5 HP/s Regen.
  Incomuns (max 2): EmberCharm "Ember Charm" 20% Burning · TidePearl "Tide Pearl" 20% Wet · FrostBell "Frost Bell" 20% Slowed ·
  ThunderDrum "Thunder Drum" 10% Stunned · ShadowIdol "Shadow Idol" 15% Cursed · PaperCrane "Paper Crane" +1 Projeteis ·
  MerchantSeal "Merchant's Seal" −20% PrecoLoja · OniMask "Oni Mask" +25% Dano abaixo de 50% HP.
  Lendários (max 1): PhoenixFeather "Phoenix Feather" revive 1× com 50% HP · DragonScale "Dragon Scale" +40 Armadura ·
  HuntersMark "Hunter's Mark" crítico ×2.5 · StormCore "Storm Core" reações causam +50% do acerto em área.
- `Config`: `ItemPesosRaridade = { comum 70, incomum 25, lendario 5 }`, `ChanceItemBau = 0.7`,
  `StatusQueimadoDuracao 3`, `StatusQueimadoFrac 0.15` (dano/s = fração do acerto), `IntervaloQueimadura 0.5`,
  `StatusMolhadoDuracao 4`, `StatusAtordoadoDuracao 1`, `StatusAmaldicoadoDuracao 5`, `StatusAmaldicoadoBonus 0.25`,
  `StatusLentoDuracao 3`, `StatusLentoFator 0.6`, `ChefeResistenciaStatus 0.3`, `ReacaoRaio 8`,
  `ReacaoRupturaMult 2`, `ReacaoEstilhacoFrac 0.6`, `SnapshotEntradasPorPacote 55`.
- `Types`: `Elemento`, `StatusId = "Queimado"|"Molhado"|"Atordoado"|"Amaldicoado"|"Lento"`, `InfoItem = { id, name, descricao, raridade, quantidade }`,
  `InfoReacao = { tipo, x, z }`, `EstadoHeroiResumo.itens: { [string]: number }`.
- `Dano`: `mult/extra/flat/critico` ganham `bonus: { [string]: number }?` (soma: `1 + porNivel*nv + bonus[id]`; critico usa `bonus.CritMult`).
- `Server`: remotes `Item`, `Reacao` (s→c).

### Task 2: Status e reações no InimigoSystem + snapshot + tint no cliente
- Arrays por slot: `queimadoAte/queimadoDps/queimadoDono`, `molhadoAte`, `atordoadoAte`, `amaldicoadoAte`, `lentoAte`; zerados em `spawnar`/`limparTudo`.
- `InimigoSystem.aplicarStatus(id, status, dono: Player?, dps: number?, semReacao: boolean?)` — chefes: duração × resistência, Stunned ignorado;
  Molhado sobre Queimado (ou vice-versa) = **Steam** (Slowed no alvo e no raio) quando `not semReacao`.
- `danificar(id, dano, matador, elemento?)`: Cursed → dano × (1+bonus); reações por elemento (uma por acerto, limpa o status gasto):
  Vento+Wet → **Tempest** (Wet+Stunned no raio, `semReacao`) · Vento+Burning → **Wildfire** (Burning no raio) ·
  Ki+Stunned → **Rupture** (dano × 2) · Impacto+Cursed → **Shatter** (`ReacaoEstilhacoFrac` × dano a todos no raio).
  StormCore do matador: +50% do dano do acerto em área. Reação manda `Reacao {tipo, x, z}` a todos.
  Depois do dano, itens `aoAcertar` do matador (`HeroiSystem.obter(matador).aoAcertar`) rolam status.
- `passo`: Stunned não anda; Slowed × fator; Burning tira `dps` a cada `IntervaloQueimadura` (mata com crédito pro `dono`).
- Snapshot: `TAM_ENTRADA 15`, u8 bitmask (1 burn, 2 wet, 4 stun, 8 curse, 16 slow) após o hp; `InimigoRenderController` lê o byte e
  pinta o `UIStroke` (laranja/azul/amarelo/roxo/ciano, nessa prioridade; sem status = cor original).
- `GolpeSystem`: toda chamada `danificar` passa `def.elemento`.
- `EfeitosController`: `Reacao` → disco colorido 0,4 s no chão (cor por tipo).

### Task 3: ItemSystem + HeroiSystem + consumidores de bônus
- `HeroiSystem.EstadoHeroi` ganha `itens`, `bonus`, `aoAcertar`, `condicionais`, `reviveuUsado`; resumo manda `itens`.
  `bonusPassiva` soma condicionais; `aplicarDano` usa `bonus.Armadura` e, ao morrer com `reviver` disponível, revive
  (`hp = fracHp × hpMax`, invuln 2 s, `reviveuUsado = true`). Regen/velocidade/HP/XP/moedas somam `bonus`.
- `ItemSystem` (novo): `dar(player, id): boolean` (respeita `max`, recalcula bônus, manda `Item`), `sortear(player, rng): string?`
  (pesos por raridade, exclui no teto), `recalcular(player)`; `start`: `InimigoSystem.morreu` → cura `bonus.CuraPorAbate` do matador.
- `GolpeSystem`/`CloneSystem`/`XpSystem`/`MercadorSystem` (preço × (1 + bonus.PrecoLoja)): passam `e.bonus` ao `Dano.*`.
- `BauSystem.abrir`: `ChanceItemBau` → `ItemSystem.sortear` + `dar`; senão (ou sem item possível) oferta de cartas.

### Task 4: Cliente — ItemController
- Toast "Found: <name>" (cor da raridade, 3 s) e faixa de inventário no canto inferior esquerdo
  (quadradinhos com `letra` e contagem), atualizada pelo `EstadoHeroi.itens`.

### Task 5: Teste em Play + revisão + docs
