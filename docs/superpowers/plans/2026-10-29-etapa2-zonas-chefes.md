# Etapa 2 — Zonas, guardiões, portal, santuário — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A partida vira a região "Vale das Cerejeiras Partidas": 3 zonas + Santuário.
Em cada zona o jogador acha o altar, invoca o guardião, vence, ganha a recompensa e
entra no portal; no Santuário vence o chefe final e entra na saída = VICTORY. Cada zona
tem 10:00; ao zerar começa o **Cerco Final** (pressão crescente).

**Architecture:** Novo `ZonaSystem` (servidor) é dono da progressão (zona atual, fase,
timer, altar, portal) e decide a vitória. Chefes são inimigos do `InimigoSystem` com
flag de chefe (vida grande, não contam no teto) + IA de ataque no novo `ChefeSystem`
(golpe em área com aviso no chão). Geometria das zonas é estática no place (regra do
`CLAUDE.md`), com marcadores de spawn/altar/portal. Cliente ganha `ZonaHudController`
(nome da zona, objetivo, barra do chefe, contagem do portal) e `AvisoController`
(círculo vermelho no chão antes do golpe do chefe).

**Tech Stack:** igual à etapa 1 (Studio via MCP, Luau `--!strict`).

**Spec:** `docs/superpowers/specs/2026-10-29-animebonk-design.md` §4, §7, §13 item 2.

## Global Constraints

- Mesmas da etapa 1 (`docs/superpowers/plans/2026-10-29-etapa1-partida-minima.md`).
- Guardiões e chefe final são **originais**, de folclore japonês genérico (domínio
  público): Komainu de pedra, Ronin de bambu, Tengu do templo, Oni do Eclipse.
- Diego autorizou o Claude a testar com Play nesta etapa (2026-10-29).

## Review Focus

1. Jogador morre com o portal aberto / durante a contagem → derrota normal, portal não
   teleporta morto (solo).
2. Invocar o guardião duas vezes (prompt spam / dois jogadores) → só 1 chefe.
3. Chefe morre no mesmo frame em que o timer da zona zera → recompensa + portal; o
   Cerco Final para de valer ao trocar de zona.
4. Play Again no meio da zona 3 → volta à zona 1 limpa (sem chefe, altar, portal ou
   aviso pendurado).
5. Golpe em área do chefe com o jogador saindo do círculo → não leva dano.

---

### Task 1: Mapa das 4 áreas (estático)

- Áreas lado a lado no eixo X, cada uma com chão próprio (cor/material diferentes),
  `Spawn` (Part invisível), `Altar` (Part com marcador) e `Portal` (posição do portal):
  - `Zonas/Vila` centro (0,0), 300×300, grama clara — guardião Komainu.
  - `Zonas/Bambuzal` centro (600,0), 300×300, grama escura + "bambus" (cilindros
    verdes) — guardião Ronin.
  - `Zonas/Templo` centro (1200,0), 300×300, pedra + escadas/plataformas — Tengu.
  - `Zonas/Santuario` centro (1800,0), 160×160, pedra escura + tochas — Oni do Eclipse.
- Cada área é cercada por paredes invisíveis (impede sair do chão).
- O `Mapa/Chao` da etapa 1 vira o chão da Vila (reaproveitado, redimensionado).
- Decoração mínima de placeholder (cerejeiras = tronco + copa rosa) só na Vila.

### Task 2: Definições e Config

- `Definicoes/Zonas` (lista ordenada): `{ id, name, guardiao, multHp, final? }` —
  Vila "Cherry Village" Komainu ×1; Bambuzal "Bamboo Grove" Ronin ×1.6; Templo
  "Temple Ruins" Tengu ×2.4; Santuario "Eclipse Shrine" OniEclipse ×3.2, `final = true`.
- `Definicoes/Chefes` (`indice` ≥ 101 pro snapshot):
  - Komainu "Stone Komainu" hp 900, vel 8, contato 15, raio 6, golpe raio 12 dano 25
    aviso 1,0 s a cada 4 s.
  - Ronin "Bamboo Ronin" hp 1600, vel 11, contato 18, raio 5, golpe raio 10 dano 30
    aviso 0,8 s a cada 3,5 s.
  - Tengu "Temple Tengu" hp 2400, vel 10, contato 20, raio 6, golpe raio 14 dano 32
    aviso 0,9 s a cada 3 s.
  - OniEclipse "Eclipse Oni" hp 5000, vel 9, contato 25, raio 8, golpe raio 16 dano 40
    aviso 1,0 s a cada 3 s; invoca 6 lacaios a cada 12 s.
- `Config`: `DuracaoZona = 600`, `CercoMultSpawn = 3`, `CercoHpPorMinuto = 0.25`,
  `ContagemPortal = 10`, `RaioPortal = 8`, `RaioAltar = 10`, `ChefeHz = 5`.
- `Types`: `InfoZona = { indice, total, name, fase, restante, cerco }`,
  `InfoChefe = { name, hpFrac }?`, `Aviso = { x, z, raio, atraso }`.

### Task 3: InimigoSystem com chefes e zona

- `InimigoSystem.spawnarChefe(tipo: string, x: number, z: number, multHp: number): number`
  (chefe não conta no teto, usa `Definicoes/Chefes`).
- `InimigoSystem.definirZona(centro: Vector3, meiaLargura: number, multHp: number, multSpawn: number)`
  — spawn preso aos limites da zona; inimigos comuns nascem com `hp * multHp`.
- `InimigoSystem.infoChefes(): { {id, tipo, hpFrac} }`; `morreu` passa a informar
  `ehChefe` (5º argumento).
- Snapshot e render aceitam índices de chefe; cliente desenha chefes maiores.

### Task 4: ZonaSystem + ChefeSystem (servidor)

- `ZonaSystem`: fases `explorar → chefe → portal → (próxima zona | vitoria)`. Altar com
  ProximityPrompt "Summon Guardian" (só em `explorar`, debounce). Ao vencer o guardião:
  recompensa = cura total + uma oferta extra de cartas; abre o portal (prompt "Enter
  Portal"); com todos os vivos a ≤ `RaioPortal` **ou** 10 s após o primeiro entrar →
  limpa inimigos/orbes/projéteis, teleporta pro `Spawn` da próxima zona, timer reinicia.
  Zona final: chefe morto → portal "Exit" → `PartidaSystem.terminar("vitoria")`.
  Timer da zona só corre com `EstadoPartida.rodando()`; ao zerar liga o Cerco Final
  (spawn ×`CercoMultSpawn`, HP dos comuns +25%/min). Envia `"Zona"` (InfoZona) 4×/s.
- `ChefeSystem`: a cada `intervalo`, escolhe o herói vivo mais próximo do chefe, manda
  `"Aviso"` a todos e, após `aviso` s, aplica dano a quem estiver no raio (posição no
  momento do impacto). Oni invoca lacaios. Envia `"Chefe"` (InfoChefe) 5×/s.
- `PartidaSystem`: remove a vitória por timer; expõe `terminar(resultado)`; reinício
  volta tudo à zona 1 (`ZonaSystem.reiniciar()`).

### Task 5: Cliente (HUD da zona, barra do chefe, avisos, marcadores)

- `ZonaHudController`: "Zone 1/3 — Cherry Village" (Santuário: "Final — Eclipse
  Shrine"), objetivo ("Find the Guardian altar" / "Defeat the Guardian" / "Enter the
  portal" / "Defeat the Eclipse Oni"), timer da zona (vermelho + "FINAL SIEGE" no
  Cerco), barra do chefe com nome, contagem do portal.
- O timer da HUD da etapa 1 passa a mostrar o timer da zona.
- `AvisoController`: disco vermelho translúcido no chão que enche em `atraso` s.
- Marcadores: BillboardGui sempre visível sobre o altar e o portal (ícone + distância).

### Task 6: Teste com Play + revisão

- Roteiro automatizado (cliente via MCP): invocar o guardião da Vila com
  `Config` temporário de HP baixo, conferir recompensa, portal e troca de zona; derrota
  com portal aberto; Play Again no meio. Depois revisão independente e correções.
