# Etapa 6b — Conquistas, ranking e configurações — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Conquistas (~12 na v1) com recompensa em Essência e desbloqueios por desafio
(Kaizo/Haruto passam a vir de conquistas), ranking (melhor tempo de vitória e mais abates,
`OrderedDataStore`) visível no Menu, e tela de configurações (volume de música/efeitos,
mostrar dano, tamanho da HUD) salva no perfil.

**Architecture:** `Definicoes/Conquistas` (dado: `{ id: { name, descricao, essencia,
desbloqueia: heroiId?, condicao: { tipo, valor } } }`); contadores acumulados no perfil
(`estatisticas: { abatesTotal, abatesPorElemento, vitorias, chefesDerrotados, partidas,
nivelMax }`, schema **v3**). `ConquistaSystem` (Partida) acumula durante a partida e, no
`terminar`, avalia e concede (Essência + `desbloqueios`), mandando `Conquista` (s→c) pro
toast. Ranking: `RankingSystem` (Partida) grava em `OrderedDataStore("MelhorTempo")` e
`("MaisAbates")` no fim; Menu lê top 10 (`GetSortedAsync`) com cache de 60 s e mostra na
tela "Leaderboard" (hoje placeholder). Configurações: `perfil.config = { musica, efeitos,
mostrarDano, escalaHud }` (v3), tela no Menu e no Partida (Esc), aplicadas no cliente.

**Spec:** §9, §10 (conquistas, classificação), §6/§9 (configurações).

## Review Focus
1. Conquista concedida 1× só (idempotente), mesmo com 2 fins de partida rápidos / Play Again.
2. Ranking: só o servidor escreve; tempo de vitória menor substitui, abates maior substitui; sem escrita em derrota pro tempo.
3. Perfil v2 → v3 migra (`estatisticas`/`config` criados) sem perder Dojo/Essência; Partida antigo lendo v3 não salva (regra 5a).
4. Configurações aplicadas ao entrar (antes do perfil chegar usa padrão) e persistem.
5. Desbloqueio de Kaizo/Haruto continua funcionando (migrar os gatilhos atuais de ZonaSystem/PartidaSystem para conquistas; perfis que já têm o desbloqueio mantêm).

### Task 1: Shared v3 (Types, Perfil, Definicoes/Conquistas, Config) nos 2 places + TesteLogica.
### Task 2 (Partida): ConquistaSystem + RankingSystem + hooks (morreu, terminar, avancar) + ConquistaController (toast) + ConfigController (Esc).
### Task 3 (Menu): telas "Achievements", "Leaderboard", "Settings" ligadas aos atalhos.
### Task 4: teste em Play nos 2 places + revisão + docs.
