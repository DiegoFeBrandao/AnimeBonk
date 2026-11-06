# Etapa 6a — Ultimates (tecla R) e despertares (nv 20 / 40) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Cada herói tem uma **ultimate** (spec §5) que carrega com o dano causado e dispara
na tecla R (botão na HUD no mobile), com 3 versões (base / despertar 1 / despertar 2); nos
níveis 20 e 40 o herói **desperta**: stats sobem, o sprite muda de cor/aura e a ultimate
sobe de versão.

**Architecture:** Ultimates são dados em `Definicoes/Ultimates` (`{ [heroiId]: { versoes:
{ {name, forma, dano, raio/alcance/..., cor} ×3 } }`), reaproveitando as **formas** do
`GolpeSystem` (`area`, `linha`, `cadeia`, `projetil` com quantidade alta) via
`GolpeSystem.usarDe` com um `multDano` grande — nada de código por ultimate. `UltimateSystem`
(servidor): carga por jogador (`Config.UltimateCargaPorDano`, 0..1; chefes contam), remote
`UsarUltimate` (rate-limit, carga cheia, vivo, rodando), aplica a versão pelo despertar e zera a
carga; manda `Ultimate` (s→c) com a carga 4×/s (só quando muda). Despertares em
`Definicoes/Herois.despertares = { {nivel=20, name, cor, multDano, multHp, multVel}, {nivel=40, ...} }`
aplicados em `HeroiSystem.subiuNivel` (recalcularStats + atributo `Despertar` no Player → sprite
muda cor/aura no cliente; `bonusPassiva` soma o mult). HUD: barra da ultimate com "R" e nome;
botão touch.

**Spec:** §5 (ultimates e transformações de cada herói), §9 (HUD).

## Review Focus
1. Spam de R / R sem carga / R caído ou na pausa → ignorado; carga nunca passa de 1.
2. Despertar no mesmo frame da morte / Play Again → stats e atributo voltam ao normal.
3. Ultimate do clone não existe (clone não usa ultimate).
4. Carga persiste na troca de zona, zera no Play Again.
5. Mobile: botão na HUD dispara o mesmo remote.

### Task 1: Definições + Config (`UltimateCargaPorDano 0.0008`, `RateLimitUltimate 0.5`) + Types (`InfoUltimate = { carga, name }`) + remotes `UsarUltimate`/`Ultimate`.
  Ultimates (nomes nossos, spec §5): Ryuga "Ki Burst" → "Crimson Meteor" → "Celestial Beam";
  Kaizo "Cannon Punch" → "Giant Fist Rain" → "Captain's Hammer"; Haruto "Thousand Clones Strike"
  → "Wolf Howl" → "Beast Unleashed". Despertares: Ryuga "Crimson Aura"/"Celestial Aura", Kaizo
  "Spring Mode"/"Storm Mode", Haruto "Wolf Mantle"/"Beast Awakening".
### Task 2: UltimateSystem (servidor) + HeroiSystem despertares + `Despertar` no Player.
### Task 3: Cliente — `UltimateController` (barra + tecla R + botão touch), `HeroiSpriteController`
  (cor/aura por `Despertar`), `EfeitosController` (ultimate usa o visual da forma, com raio maior).
### Task 4: teste em Play (dar carga via Config temporário alto) + revisão + docs (+ replicar
  `Shared` no Menu: Herois/Config/Types/Ultimates).
