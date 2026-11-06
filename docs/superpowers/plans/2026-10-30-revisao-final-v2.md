# Revisão final v2 — revisar o que ficou sem revisão, jogar uma run inteira e corrigir — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Diego saiu e pediu "veja se tem algo a melhorar e melhore" (2026-10-30, fim do dia).
Três lotes do dia nunca passaram por revisor (**Menu redesign**, **Polimento UI v2**, **Co-op v2**),
e todo lote revisado até agora rendeu 1–5 achados importantes. Além disso ninguém jogou uma run
inteira depois da fase 2 procurando erro de console, estado preso ou texto errado. Este lote:
(1) revisa esses três lotes (código + 1 Play por place), (2) joga uma run solo inteira na Partida
atrás de erros, (3) corrige tudo que for Crítico/Importante nos 2 places, (4) replica o `Shared`.

**Architecture:** quatro agentes, no fluxo de sempre (ver memória `fluxo-lotes-agentes`):
- **A — revisor Partida** (só leitura + 1 Play no fim): Co-op v2 + Polimento UI v2.
- **B — revisor Menu** (só leitura + 1 Play no fim): Menu redesign + parte Menu do Co-op v2 e do
  Polimento UI v2 + conferir que I1–I3 da revisão de Co-op com salas foram mesmo corrigidos.
- **C — playtest Partida** (depois de A, porque Play atrapalha `script_read`): run solo completa,
  objetos/eventos um a um, derrota, vitória, Play Again; mede vazamento (instâncias/memória ao
  longo do tempo).
- **D — implementador** (Partida, depois Menu): corrige Crítico/Importante de A, B e C; Menor só se
  for barato; replica `Shared`; atualiza `docs/estado-do-projeto.md`.
A e B rodam em paralelo (places diferentes, nenhum escreve).

**Spec:** `docs/estado-do-projeto.md`, ledgers em `.superpowers/sdd/2026-10-30-{coop-v2,
polimento-ui-v2, menu-redesign}/progress.md`, planos dos três lotes.

## Review Focus
1. Troca de zona com jogador saindo/morrendo/caído no meio do teleporte; `Character` nil; vigia devolvendo alguém que acabou de ser teleportado.
2. Caído com prazo × End Match × pausa × Revive All × renascer na zona nova (prazo some? HP? invulnerável?).
3. Vazamentos: billboards/feixes/pings/marcadores de mapa quando o aliado sai; conexões por jogador em `PlayerRemoving`.
4. Remotes novos (`Ping`, `Equipe`, `RecargaGolpe`) validados e com rate-limit; `Qa` só com `IsStudio`.
5. Menu: pilha de navegação com herói trancado × Prepare × Start; telas reconstruídas sem duplicar conexões; `SalaSystem` após I1–I3.

### Task 1: A + B em paralelo → `review.md` nos ledgers de coop-v2 e menu-redesign.
### Task 2: C → `.superpowers/sdd/2026-10-30-revisao-final-v2/playtest.md`.
### Task 3: D corrige (Partida → Menu → Shared) → `progress.md` deste lote + docs.
