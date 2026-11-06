# Menu "1000× mais legal" — redesign visual e telas que faltam — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Redesenhar o place **Menu** com identidade própria (hoje é a cópia estrutural do
PokeBonk com rótulos placeholder): fundo 3D vivo (herói escolhido em pose numa vila ninja
ao entardecer, câmera lenta orbitando, pétalas/vaga-lumes), painel lateral com botões
grandes animados, cartões com brilho por raridade, transições entre telas (slide + fade),
som de UI, e terminar as telas incompletas. Pedido do Diego (2026-10-30): "ainda tem um
monte de coisa no menu não pronta... queria deixar ele 1000x mais legal".

**Architecture:**
- Tema visual único (`Client/Util/Tema`: paleta — índigo escuro, vermelho carmim, dourado;
  fontes `GothamBlack`/`GothamMedium`; cantos 12 px; sombra; borda por raridade) usado por
  todos os controllers do Menu (e exportado pro Partida depois).
- **Cena 3D** em `Workspace/Cenario` (estática, criada em Edit: pátio de vila ninja com
  lanternas, torii, cerejeira, pedestal do herói) + `CenarioController` (câmera scriptable
  orbitando devagar, troca o modelo do herói ao selecionar, partículas).
- `MenuController` fatiado por tela (`Telas/Home`, `Telas/Herois`, `Telas/Preparar`,
  `Telas/Skins`, `Telas/Dojo`, `Telas/Conquistas`, `Telas/Ranking`, `Telas/Config`,
  `Telas/Tarefas`, `Telas/Cla*`) com um `Navegacao` comum (pilha, Back sempre no mesmo
  lugar abaixo do Inset, transições). Nada de lógica nova de servidor: só UI.
- Telas incompletas (listar na Task 1 por grep de "placeholder"/"TODO"/"Coming soon"):
  terminar com os dados que já existem (perfil, definições). O que depender de sistema
  inexistente fica como botão desabilitado com tooltip "Coming soon" e vai pro ledger.
- Juice: `Util/Juice` já tem botão/carta; acrescentar `transicaoTela`, `brilhoRaridade`,
  `contador`. Sons de clique/hover/confirm já existem em `Definicoes/Sons`.

**Spec:** §9 (menus), PokeBonk §7, §13–16 (estrutura).

## Review Focus
1. Back nunca fica sob os ícones do Roblox (Inset) em nenhuma tela, nem no celular.
2. Cena 3D: ≤ 400 instâncias, sem Highlights além do teto, sem vazamento de conexão ao trocar herói.
3. Transições não deixam telas invisíveis recebendo clique; Esc fecha a tela do topo.
4. Nenhum remote novo; nada de lógica que o servidor precise validar.
5. Textos em inglês, `AutoLocalize` ligado, nomes de jogador não traduzidos.

### Task 1: Levantamento (telas, placeholders, rótulos) + `Util/Tema` + `Navegacao`.
### Task 2: Cena 3D + `CenarioController` + Home nova.
### Task 3: Telas Heroes/Prepare/Skins/Dojo no tema novo (com evolução em 3 estágios se o lote HUD já existir).
### Task 4: Telas Achievements/Leaderboard/Settings/Daily Tasks/Clan no tema novo + telas incompletas.
### Task 5: teste em Play + revisão + docs.
