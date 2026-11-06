# Etapa 6c — Tarefas diárias, tradução pt-BR e visual placeholder melhor — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** (1) **Tarefas diárias**: 3 tarefas por dia (sorteadas de uma lista, ex.: "Defeat 300
enemies", "Open 2 chests", "Win a run", "Reach level 15", "Use your ultimate 5 times") com
Essência e **sequência** (streak: dias seguidos completando as 3 → bônus crescente, cap 7).
(2) **Tradução pt-BR**: tabela de localização (`LocalizationTable` em `ReplicatedStorage/
Localizacao`) com todos os textos visíveis em inglês → pt-BR, usando `LocalizationService`
automática (textos já em inglês como fonte) + `AutoLocalize` ligado nas GUIs. (3) **Visual
placeholder melhor** sem arte externa: sprites dos heróis/inimigos viram formas compostas
(corpo + cabeça + cor de destaque + sombra no chão), orbes/efeitos com `ParticleEmitter`
simples, chão das zonas com texturas built-in e névoa/iluminação por zona (`Lighting`
ajustado por zona no cliente). Nada de assets de terceiros.

**Architecture:** Tarefas: `Definicoes/Tarefas` (dado), `perfil.tarefas = { dia: string
("YYYY-MM-DD" UTC), lista: { {id, progresso, feita} ×3 }, streak: number, ultimoDiaCompleto:
string }` (schema **v4**); `TarefaSystem` (Partida) acumula progresso pelos mesmos hooks das
conquistas e, no `terminar`, grava/concede; sorteio diário por `os.date("!%Y-%m-%d")` com
seed = userId + dia; Menu mostra "Daily Tasks" (lista + streak). Tradução: módulo
`Shared/Localizacao/PtBr` (lista `{ en, pt }`) gera a `LocalizationTable` no boot do servidor
se faltar (idempotente), `LocalizationService` com `Localization table` apontando pra ela;
GUIs criadas por `Instance.new` com `AutoLocalize = true`. Visual: `HeroiSpriteController`/
`InimigoRenderController` montam o sprite composto; `ZonaVisualController` (cliente) troca
`Lighting` (cor do ambiente/névoa) ao receber `Zona`.

**Spec:** §9 (menus), §10 (tarefas diárias), §11.1 (idioma), §8 (visual).

## Review Focus
1. Tarefas do dia trocam à meia-noite UTC sem perder progresso do dia corrente; streak zera se pular 1 dia.
2. Progresso de tarefa só do servidor; Essência nunca negativa; mesma tarefa não concede 2×.
3. Perfil v3 → v4 migra; Partida v3 lendo v4 não salva (regra 5a).
4. Tradução: textos dinâmicos (`string.format`) usam `TranslationService`/placeholders e não quebram; `AutoLocalize` não traduz nomes de jogadores.
5. Sprites compostos continuam no pool (sem criar/destruir por frame) e o snapshot não muda.

### Task 1: Shared v4 + Definicoes/Tarefas + Logica/Tarefas (sorteio, progresso, streak) nos 2 places + TesteLogica.
### Task 2 (Partida): TarefaSystem + hooks + toast; (Menu): tela "Daily Tasks" com streak.
### Task 3: Localização (tabela pt-BR gerada do módulo; AutoLocalize nas GUIs dos 2 places).
### Task 4: Visual placeholder composto (heróis, inimigos, chefes maiores), partículas em orbes/ultimates, Lighting por zona.
### Task 5: teste em Play nos 2 places + revisão + docs.
