# Etapa 5a — Perfil persistente (DataStore) e Essência — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Cada jogador tem um perfil salvo (DataStore) com **Essência** (moeda permanente),
estatísticas e desbloqueios; o fim da partida dá Essência e a tela de fim mostra o ganho.
Base pro place de Menu (5b) e meta-progressão (Dojo, desbloqueios).

**Architecture:** `Shared/Logica/Perfil` (puro): schema versionado, `novo()`, `migrar()`,
`essenciaDaPartida()`. `Server/Systems/PerfilSystem`: carrega no `PlayerAdded` com retry/backoff,
cache em sessão, salva no `PlayerRemoving`, autosave e `BindToClose`; se o load falhar depois
das tentativas o perfil fica **somente em memória e nunca é salvo** (não sobrescreve dados
remotos). `PartidaSystem.terminar` registra o fim e manda `essenciaGanha/essenciaTotal` na
`FimPartidaInfo`. Remote `Perfil` (s→c) com o resumo pra HUD/menus.

**Spec:** §10 (meta-progressão), §12 (segurança), regra "Dados" do CLAUDE.md.

## Review Focus
1. Load falhou (DataStore off no Studio / erro) → jogo funciona, warn no Output, nada é salvo pra esse jogador.
2. Jogador sai durante o save do autosave → sem save duplo concorrente (fila/flag por jogador).
3. BindToClose salva todos os sujos com retry e dentro do tempo (≤ 30 s).
4. Perfil de versão antiga (ou campos faltando) → migra sem perder Essência.
5. Essência nunca negativa; valores do cliente nunca entram (só o servidor escreve).

### Task 1: Types, Logica/Perfil, Config
- `Types.Perfil = { versao, essencia, partidas, vitorias, melhorNivel, melhorAbates, melhorTempoVitoria: number?, desbloqueios: {[string]: boolean} }`; `FimPartidaInfo` + `essenciaGanha`, `essenciaTotal`.
- `Logica/Perfil`: `VERSAO = 1`, `novo()`, `migrar(dados)`, `essenciaDaPartida(resultado, nivel, abates)` = `nivel·EssenciaPorNivel + floor(abates/EssenciaPorAbates) + (vitoria ? EssenciaVitoria : 0)`.
- `Config`: `AutosaveIntervalo 120`, `DataStoreTentativas 3`, `EssenciaPorNivel 2`, `EssenciaPorAbates 10`, `EssenciaVitoria 100`.
- `TesteLogica`: migrar(nil) == novo; migrar({essencia=50}) mantém 50 e versao 1; essenciaDaPartida("vitoria", 10, 95) == 129.

### Task 2: PerfilSystem + PartidaSystem + FimController + remote `Perfil`
