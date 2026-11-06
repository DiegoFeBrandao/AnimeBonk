# Etapa 1 — Partida mínima solo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** No place "Partida", um jogador com o Ryuga anda num chão aberto, inimigos em
sprite 2D vêm em hordas, os 2 golpes do Ryuga atacam sozinhos, matar dá XP, subir de
nível abre 3 cartas, e a partida termina em derrota (HP 0) ou vitória (sobreviver até o
timer zerar).

**Architecture:** Servidor autoritativo: inimigos, projéteis e orbes de XP existem só
como **dados** no servidor (sem Parts); o servidor resolve movimento, acerto, dano e XP e
manda snapshots compactos. O cliente só desenha (sprites em BillboardGui com pool) e
manda: índice da carta escolhida. Lógica pura (fórmulas, sorteio de cartas, curva de XP)
fica em módulos do `Shared` sem estado, pra poder ser reaproveitada nas etapas seguintes.

**Tech Stack:** Roblox Studio via MCP (`execute_luau` modo Edit, `multi_edit`,
`script_read`), Luau `--!strict`, RemoteEvent + UnreliableRemoteEvent. Sem Rojo, sem git
do código (regras do `CLAUDE.md`).

**Spec:** `docs/superpowers/specs/2026-10-29-animebonk-design.md` (seções 4, 5.1, 6, 8, 12,
13 item 1).

## Global Constraints

- Todo script começa com `--!strict`; indentação com tabs; sem `_G`.
- Estrutura: `ReplicatedStorage/Shared` (tipos, config, definições, lógica pura),
  `ServerScriptService/Server` (Script `Server` + `Systems/`), `StarterPlayer/
  StarterPlayerScripts/Client` (LocalScript `Client` + `Controllers/`). Cada sistema/
  controller é ModuleScript com `init()` e `start()`.
- Texto visível ao jogador em **inglês**; IDs, chaves, nomes de instância, logs e
  comentários em português. A tela mostra o campo `name`, nunca a chave interna.
- Números ajustáveis só no `Config`.
- Servidor decide dano, XP, cartas oferecidas, nível, morte e fim de partida. Cliente
  manda só o índice da carta; validar tipo, faixa e se há oferta pendente; rate-limit.
- Desconectar conexões ao terminar; loops por sistema (um Heartbeat por sistema, não um
  por inimigo); sem alocar tabelas novas por inimigo por frame no loop principal.
- **Não dar Play pelo MCP nem testar sozinho.** Cada task termina com um roteiro de teste
  manual pro Diego e o aviso de salvar (Ctrl+S). "Commit" deste plano = salvar o place.
- Heróis e inimigos em **sprite 2D** (nesta etapa: placeholders sem asset — Frame
  colorido com a inicial, até a arte existir).

## Review Focus

1. **Muitos inimigos** (teto atingido, 200 vivos) → o jogo não trava; snapshots só com
   inimigos dentro do raio de desenho do jogador. Teste no Task 4 (roteiro com
   `Config.InimigosMaxVivos` alto).
2. **Clique duplo / carta inválida** (índice fora de 1..3, sem oferta pendente, string)
   → ignorado sem erro; nível não sobe duas vezes. Teste no Task 6.
3. **Vários level-ups de uma vez** (matar muitos e ganhar 2+ níveis) → as ofertas ficam
   em fila e aparecem uma após a outra. Teste no Task 6.
4. **Jogador sai no meio da partida** → sistemas param de mirar nele, nada dá erro, o
   servidor encerra a partida se não sobrar ninguém. Teste no Task 7.
5. **Morte e vitória no mesmo frame** (HP chega a 0 quando o timer zera) → só um
   resultado é enviado (derrota tem prioridade). Teste no Task 7.

---

### Task 0: Preparar a experiência (Diego)

- [ ] **Step 1:** Diego cria o grupo do Roblox, a experiência (dona: o grupo) e o place
  **"Partida"**; abre no Studio e liga o MCP (Assistant → Manage MCP Servers → Enable).
- [ ] **Step 2:** Registrar grupo, universe e placeId em `docs/estado-do-projeto.md`.
- [ ] **Step 3:** No place: `Workspace/Mapa/Chao` — Part ancorada 400×2×400 studs em
  (0,0,0), material Grass, e `Workspace/Mapa/SpawnJogador` (SpawnLocation no centro).
  Criado pelo MCP no modo Edit (geometria estática fica salva no place).

Roteiro: abrir o place, ver o chão; Ctrl+S.

---

### Task 1: Base compartilhada (Types, Config, definições, Remotes) + bootstrap

**Files (Studio):**
- Create: `ReplicatedStorage/Shared/Types` (ModuleScript)
- Create: `ReplicatedStorage/Shared/Config`
- Create: `ReplicatedStorage/Shared/Definicoes/Herois` · `Definicoes/Golpes` ·
  `Definicoes/Inimigos` · `Definicoes/Pergaminhos`
- Create: `ReplicatedStorage/Shared/Remotes`
- Create: `ServerScriptService/Server/Server` (Script) e pasta `Systems`
- Create: `StarterPlayer/StarterPlayerScripts/Client/Client` (LocalScript) e pasta
  `Controllers`

**Interfaces:**
- Produces `Types`:
  - `export type GolpeId = "RajadaKi" | "ChuvaSocos"`
  - `export type PergaminhoId = "Dano" | "VelAtaque" | "HpMax"`
  - `export type Carta = { tipo: "golpeNovo" | "golpeNivel" | "pergaminho", id: string, nivelNovo: number }`
  - `export type InimigoSnapshot = { id: number, tipo: string, x: number, z: number, hpFrac: number }`
  - `export type Resultado = "vitoria" | "derrota"`
- Produces `Config` (valores desta etapa, decisão do Claude):
  `DuracaoPartida = 300` (s) · `InimigosMaxVivos = 120` · `RaioSpawnMin = 60` ·
  `RaioSpawnMax = 90` · `RaioDesenho = 120` · `SnapshotHz = 10` ·
  `SpawnPorSegundoInicial = 1.5` · `SpawnPorSegundoFinal = 8` ·
  `HpHeroiBase = 120` · `CuraPorSegundo = 0.4` · `InvulnAposDano = 0.5` ·
  `RaioColetaXp = 8` · `CartasPorOferta = 3` · `NivelMaxGolpe = 8` ·
  `SlotsGolpe = 3` · `SlotsPergaminho = 3` · `NivelMaxPergaminho = 10` ·
  `BonusPergaminhoPorNivel = 0.10` · `XpBase = 5` · `XpCrescimento = 1.18`.
- Produces `Definicoes/Herois.Ryuga = { name = "Ryuga", golpeInicial = "RajadaKi", danoPorNivel = 0.01, kit = {"RajadaKi","ChuvaSocos"} }`
  (passiva <40% HP fica pra etapa 3).
- Produces `Definicoes/Golpes`:
  - `RajadaKi = { name = "Ki Blast", nivelMin = 1, forma = "projetil", dano = 12, recarga = 0.9, alcance = 40, velocidade = 50, raioAcerto = 2.5 }`
  - `ChuvaSocos = { name = "Punch Barrage", nivelMin = 2, forma = "cone", dano = 9, recarga = 1.6, alcance = 10, anguloGraus = 70, acertosPorUso = 3 }`
  - `nivelMin` = nível do herói a partir do qual o golpe pode aparecer como carta (o
    golpe nunca libera sozinho — spec §6).
- Produces `Definicoes/Inimigos`:
  - `Lanterna = { name = "Lantern Ghost", hp = 20, velocidade = 9, danoContato = 8, xp = 1, raio = 2, cor = Color3.fromRGB(255,170,60) }`
  - `Tanuki = { name = "Rascal Tanuki", hp = 45, velocidade = 7, danoContato = 14, xp = 3, raio = 2.5, cor = Color3.fromRGB(150,100,60) }`
- Produces `Definicoes/Pergaminhos`: `Dano = { name = "Power Scroll" }`,
  `VelAtaque = { name = "Speed Scroll" }`, `HpMax = { name = "Vitality Scroll" }`
  (cada nível +10%).
- Produces `Remotes.get(nome: string): RemoteEvent` e
  `Remotes.getUnreliable(nome: string): UnreliableRemoteEvent` — servidor cria na
  pasta `ReplicatedStorage/Remotes` na primeira chamada; cliente usa `WaitForChild`.
  Nomes usados no plano: `"Snapshot"` (unreliable), `"InimigoMorreu"`, `"XpOrbs"`,
  `"EfeitoGolpe"`, `"EstadoHeroi"`, `"OfertaCartas"`, `"EscolherCarta"`,
  `"FimPartida"`, `"Relogio"`.
- Produces bootstrap: `Server` e `Client` fazem `require` de todo ModuleScript em
  `Systems`/`Controllers`, chamam todos os `init()` e depois todos os `start()`, com
  `pcall` + `warn("[Server] falha em <nome>: ...")` por módulo.

- [ ] **Step 1:** Criar os módulos acima pelo MCP (`execute_luau` modo Edit).
- [ ] **Step 2:** Criar `Server` e `Client` com o bootstrap de duas fases.
- [ ] **Step 3:** Avisar Diego pra salvar. Roteiro: dar Play; Output sem erros e com
  `[Server] 0 sistemas iniciados` / `[Client] 0 controllers iniciados`.

---

### Task 2: Lógica pura (progressão, cartas, dano)

**Files:**
- Create: `ReplicatedStorage/Shared/Logica/Progressao`
- Create: `ReplicatedStorage/Shared/Logica/Cartas`
- Create: `ReplicatedStorage/Shared/Logica/Dano`

**Interfaces:**
- Produces `Progressao.xpParaProximo(nivel: number): number` =
  `math.floor(Config.XpBase * Config.XpCrescimento ^ (nivel - 1) + 0.5)`.
- Produces `Progressao.danoGolpe(base: number, nivelGolpe: number): number` — linear
  de `base` no nv 1 a `2 * base` no nv `Config.NivelMaxGolpe`.
- Produces `Cartas.gerar(estado: { nivelHeroi: number, golpes: {[string]: number}, pergaminhos: {[string]: number}, kit: {string} }, rng: Random): {Carta}`
  — monta a lista de candidatos válidos (golpe do kit que não tem, com
  `nivelMin <= nivelHeroi`, e há slot livre;
  golpe que tem abaixo do nível máx.; pergaminho novo se há slot; pergaminho abaixo do
  nível máx.), embaralha com `rng` e devolve até `Config.CartasPorOferta` sem repetir
  `id`. Lista vazia se não houver candidato.
- Produces `Dano.multiplicador(pergaminhos: {[string]: number}, nivelHeroi: number, danoPorNivel: number): number`
  = `(1 + 0.10 * nivel(Dano)) * (1 + danoPorNivel * (nivelHeroi - 1))` (origens
  diferentes multiplicam — spec §6).
- Produces `Dano.recarga(base: number, pergaminhos): number` =
  `math.max(0.12, base / (1 + 0.10 * nivel(VelAtaque)))`.
- Produces `Dano.hpMax(base: number, pergaminhos): number` = `base * (1 + 0.10 * nivel(HpMax))`.

- [ ] **Step 1:** Criar os 3 módulos.
- [ ] **Step 2:** Criar `ServerScriptService/Server/Testes/TesteLogica` (ModuleScript,
  **não** carregado pelo bootstrap) com asserções que o Diego pode rodar na barra de
  comando do Studio (`require(game.ServerScriptService.Server.Testes.TesteLogica)()`):
  - `xpParaProximo(1) == 5`, `xpParaProximo(2) == 6`
  - `danoGolpe(12, 1) == 12`, `danoGolpe(12, 8) == 24`
  - `Cartas.gerar` com `nivelHeroi = 2`, `golpes = {RajadaKi=1}`, `pergaminhos = {}`
    devolve 3 cartas sem `id` repetido; com `nivelHeroi = 1` nenhuma carta é
    `golpeNovo` de `ChuvaSocos`; com tudo no máximo e slots cheios devolve `{}`
  - `Dano.recarga(0.9, {VelAtaque = 100}) == 0.12`
- [ ] **Step 3:** Avisar pra salvar. Roteiro: rodar o comando acima; imprime
  `TesteLogica: OK`.

---

### Task 3: Herói do jogador (estado no servidor + sprite no cliente)

**Files:**
- Create: `Server/Systems/HeroiSystem`
- Create: `Client/Controllers/HeroiSpriteController`

**Interfaces:**
- Produces `HeroiSystem.obter(player: Player): EstadoHeroi?` onde
  `EstadoHeroi = { heroiId: string, nivel: number, xp: number, hp: number, hpMax: number, golpes: {[string]: number}, pergaminhos: {[string]: number}, invulnAte: number, vivo: boolean }`.
- Produces `HeroiSystem.posicao(player: Player): Vector3?` (do HumanoidRootPart).
- Produces `HeroiSystem.aplicarDano(player: Player, quantidade: number)` — respeita
  `invulnAte`; HP 0 → `vivo = false` e dispara o sinal `HeroiSystem.morreu` (BindableEvent
  interno, `.Event:Connect(fn(player))`).
- Produces `HeroiSystem.ganharXp(player: Player, quantidade: number)` — soma XP, sobe
  níveis (pode subir vários) e dispara `HeroiSystem.subiuNivel` uma vez por nível.
- Produces `HeroiSystem.vivos(): {Player}`.
- Envia `EstadoHeroi` resumido pelo remote `"EstadoHeroi"` ao dono quando muda
  (`{nivel, xp, xpProx, hp, hpMax}`), no máximo 10×/s.
- Ao entrar: estado inicial Ryuga, golpe `RajadaKi` nv 1, HP `Config.HpHeroiBase`;
  regen `Config.CuraPorSegundo`/s.
- Cliente: deixa o avatar invisível (`LocalTransparencyModifier = 1` em todas as partes
  e acessórios, reaplicado em `CharacterAdded`; pros outros jogadores o servidor zera
  a transparência via `Transparency = 1` nas partes) e põe um BillboardGui 6×8 studs no
  HumanoidRootPart com Frame azul e texto "R" — placeholder do sprite.

- [ ] **Step 1:** Criar `HeroiSystem`.
- [ ] **Step 2:** Criar `HeroiSpriteController`.
- [ ] **Step 3:** Avisar pra salvar. Roteiro: Play → o boneco some e aparece o quadrado
  azul "R" que anda com WASD; Output sem erros.

---

### Task 4: Inimigos (simulação no servidor, desenho no cliente)

**Files:**
- Create: `Server/Systems/InimigoSystem`
- Create: `Client/Controllers/InimigoRenderController`

**Interfaces:**
- Consumes: `HeroiSystem.vivos`, `HeroiSystem.posicao`, `HeroiSystem.aplicarDano`,
  `Definicoes/Inimigos`, `Config`.
- Produces `InimigoSystem.noRaio(centro: Vector3, raio: number): {number}` (ids).
- Produces `InimigoSystem.posicao(id: number): Vector3?`.
- Produces `InimigoSystem.danificar(id: number, dano: number, donoAtaque: Player)` —
  HP 0 → remove, envia `"InimigoMorreu"` `{id, x, z}` a todos e dispara
  `InimigoSystem.morreu` (`fn(id, tipo, posicao, matador)`).
- Produces `InimigoSystem.pausar(on: boolean)` e `InimigoSystem.limparTudo()`.
- Simulação (um Heartbeat): spawn em anel `[RaioSpawnMin, RaioSpawnMax]` em volta de um
  herói vivo aleatório; taxa interpola de `SpawnPorSegundoInicial` a
  `SpawnPorSegundoFinal` ao longo de `DuracaoPartida`; 75% Lanterna / 25% Tanuki; teto
  `InimigosMaxVivos`. Cada inimigo anda em linha reta no plano XZ até o herói vivo mais
  próximo; separação simples (empurra quem está a menos de `raio*2` de outro, checando
  só vizinhos via grade espacial de células de 10 studs). Contato (distância <
  `raio + 2`) → `aplicarDano(danoContato)`.
- Estado guardado em arrays paralelos por índice (id, tipo, x, z, hp), reaproveitados —
  sem criar tabela por inimigo por frame.
- Snapshot a `SnapshotHz`: pra cada jogador, `UnreliableRemoteEvent "Snapshot"` com os
  inimigos dentro de `RaioDesenho`, codificados num `buffer` (por inimigo: u32 id,
  u8 tipoIndex, f32 x, f32 z, u8 hpFrac*255).
- Cliente: pool de BillboardGui (cria sob demanda, nunca destrói, esconde quando sai
  do snapshot) ancorados em Attachments numa Part invisível ancorada no chão; interpola
  posição entre snapshots; Frame com a cor do tipo + inicial; barra de vida só se
  `hpFrac < 1`; ao receber `"InimigoMorreu"` esconde e toca um "pop" (escala 1→0 em
  0,15 s via TweenService).

- [ ] **Step 1:** Criar `InimigoSystem`.
- [ ] **Step 2:** Criar `InimigoRenderController`.
- [ ] **Step 3:** Avisar pra salvar. Roteiro: Play → quadrados laranja e marrons
  aparecem em volta e perseguem; encostar tira HP (ver no Output por enquanto); com
  `Config.InimigosMaxVivos = 200` o jogo segue liso (Review Focus 1).

---

### Task 5: Golpes automáticos do Ryuga + XP

**Files:**
- Create: `Server/Systems/GolpeSystem`
- Create: `Server/Systems/XpSystem`
- Create: `Client/Controllers/EfeitosController`

**Interfaces:**
- Consumes: `HeroiSystem.obter/posicao/ganharXp`, `InimigoSystem.noRaio/posicao/
  danificar/morreu`, `Logica/Dano`, `Logica/Progressao`, `Definicoes/Golpes`.
- `GolpeSystem` (Heartbeat): por jogador vivo e por golpe que ele tem, quando a recarga
  (`Dano.recarga`) vence:
  - `RajadaKi`: alvo = inimigo mais próximo dentro de `alcance`; cria projétil como dado
    (origem, direção, velocidade); a cada passo checa inimigos em `raioAcerto`; acerta o
    primeiro e some (ou some ao passar do alcance). Envia `"EfeitoGolpe"` a todos
    `{golpe="RajadaKi", ox, oz, dx, dz}` uma vez no disparo (cliente anima sozinho).
  - `ChuvaSocos`: direção = inimigo mais próximo; acerta todos os inimigos dentro de
    `alcance` e do cone `anguloGraus`, `acertosPorUso` vezes com 0,1 s entre acertos.
    Envia `"EfeitoGolpe"` `{golpe="ChuvaSocos", ox, oz, dx, dz}`.
  - Dano = `Progressao.danoGolpe(base, nivel) * Dano.multiplicador(...)`.
- `XpSystem`: em `InimigoSystem.morreu`, cria orbe (dado) com `xp` do tipo na posição;
  a cada 0,1 s, orbe a menos de `Config.RaioColetaXp` de um herói vivo → `ganharXp`.
  Envia ao cliente `"XpOrbs"` `{criados = {{id,x,z}}, removidos = {id}}` em lote a cada
  0,1 s.
- `EfeitosController`: projétil = Part neon amarela pequena (pool) que voa no cliente;
  cone = flash semi-transparente em leque por 0,15 s; orbes = esferas azuis pequenas
  (pool) que somem ao receber `removidos`.

- [ ] **Step 1:** Criar `GolpeSystem`.
- [ ] **Step 2:** Criar `XpSystem`.
- [ ] **Step 3:** Criar `EfeitosController`.
- [ ] **Step 4:** Avisar pra salvar. Roteiro: Play → bolinhas amarelas saem sozinhas no
  inimigo mais próximo e matam; cai orbe azul; andar perto coleta (Output mostra
  `nivel`/`xp`).

---

### Task 6: Level-up com cartas

**Files:**
- Create: `Server/Systems/LevelUpSystem`
- Create: `Client/Controllers/LevelUpController`

**Interfaces:**
- Consumes: `HeroiSystem.subiuNivel/obter`, `Logica/Cartas.gerar`, `Definicoes/*` (pro
  `name` exibido).
- `LevelUpSystem`: fila de ofertas pendentes por jogador. Em `subiuNivel` enfileira; se
  não há oferta aberta, gera (`Cartas.gerar` com `Random` do servidor), guarda e envia
  `"OfertaCartas"` `{cartas = {{tipo, id, nivelNovo, name}}}`. Se `gerar` devolver
  vazio, descarta e passa pra próxima. **Solo: pausa a partida** (`InimigoSystem.
  pausar(true)` e GolpeSystem/XpSystem/relógio param) enquanto a oferta está aberta.
- `"EscolherCarta"` (cliente → servidor) recebe `indice`: valida `typeof(indice) ==
  "number"`, inteiro, `1 <= indice <= #oferta`, há oferta aberta; rate-limit 1 por
  0,25 s. Aplica: `golpeNovo` → `golpes[id] = 1`; `golpeNivel` → `+1`; `pergaminho` →
  `+1` (e `HpMax` recalcula `hpMax`, curando a diferença). Fecha a oferta, despausa se
  a fila está vazia, senão abre a próxima.
- `LevelUpController`: ScreenGui com título "LEVEL UP!" e 3 cards (nome, "NEW" ou
  "Lv X → Y", cor por tipo); clique ou teclas 1/2/3 enviam o índice; desabilita os
  cards após o clique até nova oferta (Review Focus 2).

- [ ] **Step 1:** Criar `LevelUpSystem`.
- [ ] **Step 2:** Criar `LevelUpController`.
- [ ] **Step 3:** Avisar pra salvar. Roteiro: Play → ao subir de nível o jogo pausa e
  aparecem 3 cartas em inglês; escolher "Punch Barrage" → o Ryuga passa a soltar o
  cone; clicar duas vezes rápido não aplica duas cartas (Review Focus 2); matar muitos
  e ganhar 2 níveis → duas ofertas seguidas (Review Focus 3).

---

### Task 7: Relógio, HUD, fim de partida

**Files:**
- Create: `Server/Systems/PartidaSystem`
- Create: `Client/Controllers/HudController`
- Create: `Client/Controllers/FimController`

**Interfaces:**
- Consumes: `HeroiSystem.morreu/vivos`, `InimigoSystem.pausar/limparTudo`, pausa do
  `LevelUpSystem` (expor `LevelUpSystem.pausado(): boolean`).
- `PartidaSystem`: relógio regressivo `Config.DuracaoPartida` que não corre enquanto
  `LevelUpSystem.pausado()`; envia `"Relogio"` `{restante}` 1×/s; conta abates por
  jogador (via `InimigoSystem.morreu`). Fim:
  - todos os heróis mortos → `derrota`;
  - relógio 0 com alguém vivo → `vitoria`;
  - checar derrota antes de vitória no mesmo tick (Review Focus 5); enviar `"FimPartida"`
    uma única vez `{resultado, tempo, abates, nivel}`; pausar tudo e `limparTudo()`.
  - `Players.PlayerRemoving`: remove o jogador dos sistemas (cada sistema escuta e limpa
    o seu estado); se não sobrou ninguém, encerra sem enviar nada (Review Focus 4).
- `HudController`: canto sup. esq. retrato placeholder + "Ryuga" + "Lv N"; barra de HP
  sob o centro; barra de XP no topo; timer `MM:SS` no topo central; abates; tudo com
  `UIScale` pra celular.
- `FimController`: tela cheia "VICTORY" ou "DEFEAT", tempo, abates, nível e botão
  "Play Again" (reinicia: `TeleportService` não existe ainda nesta etapa → botão pede ao
  servidor `"Reiniciar"`; servidor reseta estados e o relógio). Adicionar `"Reiniciar"`
  à lista de Remotes, com rate-limit e só aceito após `FimPartida`.

- [ ] **Step 1:** Criar `PartidaSystem`.
- [ ] **Step 2:** Criar `HudController`.
- [ ] **Step 3:** Criar `FimController`.
- [ ] **Step 4:** Atualizar `docs/estado-do-projeto.md` (mapa dos scripts, status da
  etapa 1) e avisar pra **publicar** o place.
- [ ] **Step 5:** Roteiro final pro Diego:
  1. Play → HUD com HP, XP, nível, timer 05:00 contando.
  2. Ficar parado no meio dos inimigos → HP cai → tela "DEFEAT" com estatísticas.
  3. "Play Again" → tudo recomeça.
  4. Mudar `Config.DuracaoPartida = 30` e sobreviver → "VICTORY".
  5. Abrir level-up perto do fim → o timer para enquanto as cartas estão abertas.
  6. Sair do jogo no meio (Stop) → Output sem erros.
