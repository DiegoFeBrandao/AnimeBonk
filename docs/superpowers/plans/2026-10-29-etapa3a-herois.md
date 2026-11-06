# Etapa 3a — Heróis Kaizo e Haruto, kits de 4 golpes, escolha de herói — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A partida passa a ter 3 heróis jogáveis (Ryuga, Kaizo, Haruto), cada um com
passiva própria e kit de 4 golpes que chegam por carta; o jogador escolhe o herói numa
tela simples ao entrar (e no Play Again) e a partida só começa depois da escolha.

**Architecture:** Golpes viram **dados por forma** (`projetil`, `cone`, `area`, `linha`,
`cadeia`) e o `GolpeSystem` implementa cada forma uma vez — nenhum `if golpe == "x"`.
Passivas são dados no `HeroiDef` (`furia`, `armadura`, `clones`) lidos por `HeroiSystem`/
`GolpeSystem`. Novo `CloneSystem` (servidor) cria o clone do Haruto, que dispara o último
golpe usado via `GolpeSystem.usarDe`. A escolha de herói é um remote validado; o
`PartidaSystem` só inicia a partida quando o primeiro jogador escolhe. Cliente ganha
`HeroiEscolhaController` e `CloneRenderController`; `EfeitosController` desenha por forma.

**Tech Stack:** igual às etapas 1–2 (Studio via MCP, Luau `--!strict`, sem Rojo/git).

**Spec:** `docs/superpowers/specs/2026-10-29-animebonk-design.md` §5 (heróis), §6
(combate — slots, golpes por carta, fórmulas), §13 item 3. Ultimates, despertares (nv 20/40),
fusão e golpes genéricos de elemento ficam **fora** desta sub-etapa (etapa 6).

## Global Constraints

- Mesmas das etapas 1–2: textos visíveis em inglês, IDs/comentários em português,
  `--!strict`, tabs, conteúdo como dado em `Shared/Definicoes`, servidor autoritativo,
  pool/sem alocação por frame, números no `Config`.
- Nomes de heróis fixados pelo Diego: **Ryuga, Kaizo, Haruto**. Golpes com nomes nossos
  (abaixo); nada de nomes/golpes de animes existentes.
- Fórmulas da spec §6: armadura = `a / (a + 45)`; evasão máx. 60%; recarga mínima 0,12 s;
  bônus da mesma origem somam, origens diferentes multiplicam.
- Diego autorizou o Claude a testar com Play nesta etapa (2026-10-29).
- Decisões do Diego (2026-10-29): etapa 3 dividida em 3a/3b/3c; tela simples de escolha
  no início; Ryuga ganha os 2 golpes que faltam.

## Review Focus

1. `EscolherHeroi` com id inválido, repetido, ou com o herói já escolhido na partida →
   ignorado (um herói por jogador por partida); ninguém consegue trocar no meio.
2. Ninguém escolheu ainda (ou jogador entrou e não escolheu) → nada spawna, timer parado,
   **derrota não dispara**, jogador sem herói não leva dano nem ganha XP.
3. Pausa das cartas, morte do herói ou Play Again no meio de um golpe com ticks/atraso
   (Ki Cannon, Explosive Tag, Spring Bullet) → ticks pendentes cancelam, nada acerta depois.
4. Clone do Haruto na morte do herói, na troca de zona e no Play Again → some do servidor
   e do cliente; não dispara.
5. Shuriken que volta com o herói andando/morto → retorna à posição atual (ou some se
   morreu) e **não acerta o mesmo inimigo duas vezes na mesma passagem**.

---

### Task 1: Definições, Config e Types

**Files:**
- Modify: `ReplicatedStorage/Shared/Definicoes/Herois`, `Definicoes/Golpes`, `Config`, `Types`
- Modify: `ServerScriptService/Server/Server` (lista de remotes)

**Produces:**
- `HeroiDef = { name, classe: string, descricao: string, hpBase: number, velocidade: number,
  letra: string, cor: Color3, golpeInicial: string, danoPorNivel: number, kit: { string },
  passiva: Passiva }` com
  `Passiva = { tipo: "furia", limiarHp: number, bonusDano: number, bonusVelAtaque: number }
  | { tipo: "armadura", porNivel: number }
  | { tipo: "clones", intervalo: number, duracao: number, evasaoPorNivel: number }`.
- Heróis (hpBase / velocidade / letra / cor):
  - **Ryuga** "Ki Fighter — Brawler" 150 / 18 / "R" / (70,130,255); passiva `furia`
    limiar 0,4, +0,3 dano, +0,2 vel. ataque; `danoPorNivel = 0.01`. Descrição (inglês):
    "Warrior's Blood: +1% damage per level. Below 40% HP: +30% damage, +20% attack speed."
    Kit: RajadaKi, ChuvaSocos, PassoInstantaneo, CanhaoKi.
  - **Kaizo** "Rubber Pirate — Tank" 190 / 16 / "K" / (255,200,40); passiva `armadura`
    2 por nível; `danoPorNivel = 0`. "Rubber Body: +2 armor per level." Kit:
    SocoEstilingue, MetralhadoraSocos, ChicotePerna, BalaMola.
  - **Haruto** "Clone Ninja — Summoner" 125 / 20 / "H" / (40,160,90); passiva `clones`
    intervalo 8, duração 6, evasão 0,005 por nível; `danoPorNivel = 0`. "Army of One:
    every 8 s a clone fights for 6 s, copying your last move. +0.5% evasion per level."
    Kit: ChuvaKunai, ShurikenVento, SeloExplosivo, LaminaVento.
- `GolpeDef = { name, nivelMin, forma: Forma, dano, recarga, alcance, cor: Color3,
  -- projetil: velocidade, raioAcerto, quantidade?, teleguiado?, perfura?, retorna?
  -- cone: anguloGraus, acertosPorUso
  -- area: raio, noAlvo?, atraso?, teleportar?
  -- linha: largura, ticks?, intervalo?
  -- cadeia: saltos, raioSalto }` com `Forma = "projetil" | "cone" | "area" | "linha" | "cadeia"`.
- Golpes (nível 1):

  | id | name | nivelMin | forma | dano | recarga | alcance | extras |
  |---|---|---|---|---|---|---|---|
  | RajadaKi | Ki Blast | 1 | projetil | 20 | 0.8 | 40 | vel 50, raioAcerto 2.5 |
  | ChuvaSocos | Punch Barrage | 2 | cone | 9 | 1.6 | 10 | 70°, 3 acertos |
  | PassoInstantaneo | Flash Step | 4 | area | 35 | 4.0 | 30 | raio 7, noAlvo, teleportar |
  | CanhaoKi | Ki Cannon | 7 | linha | 12 | 5.0 | 35 | largura 4, 6 ticks, 0.15 s |
  | SocoEstilingue | Slingshot Punch | 1 | linha | 22 | 1.0 | 25 | largura 3 |
  | MetralhadoraSocos | Gatling Fists | 2 | cone | 6 | 2.2 | 10 | 60°, 6 acertos |
  | ChicotePerna | Leg Whip | 4 | area | 30 | 3.0 | 12 | raio 12 (no herói) |
  | BalaMola | Spring Bullet | 7 | cadeia | 28 | 4.5 | 30 | 5 saltos, raioSalto 12 |
  | ChuvaKunai | Kunai Rain | 1 | projetil | 12 | 1.0 | 35 | vel 55, raioAcerto 2, qtd 3, teleguiado |
  | ShurikenVento | Wind Shuriken | 2 | projetil | 18 | 2.0 | 25 | vel 40, raioAcerto 3, perfura, retorna |
  | SeloExplosivo | Explosive Tag | 4 | area | 45 | 3.5 | 30 | raio 9, noAlvo, atraso 0.8 |
  | LaminaVento | Wind Blade | 7 | cone | 40 | 2.8 | 18 | 50°, 1 acerto |

  Cores: Ki amarelo-claro (255,230,90) · Impacto laranja (255,140,60) · Vento verde-água
  (120,255,200).
- `Config` novos: `ArmaduraK = 45`, `EvasaoMax = 0.6`, `CloneDanoFrac = 0.6`,
  `CloneRaioSpawn = 4`, `CadeiaIntervalo = 0.08`, `TeleporteRecuo = 3` (studs atrás do alvo),
  `RateLimitEscolherHeroi = 0.5`. `HpHeroiBase` e `VelocidadeHeroi` saem do `Config`
  (passam pro `HeroiDef`). Tudo é primeira versão: números de balanceamento são chute
  inicial, pra ajustar nos testes.
- `Types`: `HeroiId = "Ryuga" | "Kaizo" | "Haruto"`; `GolpeId` com os 12 ids;
  `EstadoHeroiResumo` ganha `heroiId: string?` (nil = ainda não escolheu);
  `InfoClone = { id: number, dono: number (UserId), x: number, z: number, ativo: boolean }`.
- `Server`: remotes novos `"EscolherHeroi"` (cliente→servidor) e `"Clone"` (servidor→cliente,
  handler vazio).

- [ ] Editar as 4 definições/Config/Types e o `Server` conforme acima.
- [ ] Verificar em modo Edit: `require` de `Herois`, `Golpes`, `Config`, `Types` sem erro.

### Task 2: Fórmulas das passivas + TesteLogica

**Files:**
- Modify: `Shared/Logica/Dano`, `Server/Testes/TesteLogica`

**Produces:**
- `Dano.reducaoArmadura(armadura: number): number` = `armadura / (armadura + Config.ArmaduraK)`.
- `Dano.evasao(nivelHeroi: number, porNivel: number): number` = `min(Config.EvasaoMax, porNivel * nivelHeroi)`.
- `Dano.multiplicador(pergaminhos, nivelHeroi, danoPorNivel, bonusExtra: number?)` —
  `bonusExtra` (fúria) multiplica como origem própria: `* (1 + bonusExtra)`.
- `Dano.recarga(base, pergaminhos, bonusExtra: number?)` — divide por `(1 + bonusExtra)`
  além do pergaminho, mantendo `RecargaMinima`.

- [ ] Implementar as 4 funções (as duas existentes ganham o parâmetro opcional).
- [ ] `TesteLogica`: adicionar asserts — `reducaoArmadura(45) == 0.5`; `evasao(200, 0.005) == 0.6`;
  `multiplicador({}, 1, 0, 0.3) == 1.3`; `recarga(1.0, {}, 0.2) == 1/1.2`;
  `Cartas.gerar` com kit do Kaizo no nv 1 só oferece `SocoEstilingue` nível 2 (golpe inicial já
  no slot) — e com kit do Haruto no nv 7 oferece os 4 golpes como candidatos.
- [ ] Rodar `require(game.ServerScriptService.Server.Testes.TesteLogica)()` em Edit → "TesteLogica: OK".

### Task 3: Escolha de herói e início da partida (servidor)

**Files:**
- Modify: `Server/EstadoPartida`, `Server/Systems/HeroiSystem`, `Server/Systems/PartidaSystem`
- Verificar: `ZonaSystem`, `InimigoSystem`, `XpSystem`, `LevelUpSystem` só agem com `EstadoPartida.rodando()` e sobre `HeroiSystem.vivos()` (já é assim; se algum usar `todos()` pra spawn/dano, trocar).

**Consumes:** `HeroiDef` (Task 1), `Dano` (Task 2).
**Produces:**
- `EstadoHeroi.heroiId: string?` (nil até escolher). `novoEstado()` começa sem herói, `vivo = false`.
- `HeroiSystem.escolher(player, heroiId): boolean` — só se `heroiId == nil` e id existe em
  `Herois`; define hp/hpMax = `hpBase`, `golpes = { [golpeInicial] = 1 }`, `vivo = true`,
  `player:SetAttribute("HeroiId", heroiId)`, destrava movimento com `velocidade` do herói,
  marca sujo; dispara `HeroiSystem.escolheu` (BindableEvent `fn(player)`).
- `HeroiSystem.vivos()` exige `heroiId ~= nil`. `aplicarDano`/`ganharXp` ignoram sem herói.
- `aplicarDano`: antes de descontar, evasão (`rng:NextNumber() < Dano.evasao(...)` só pra
  passiva `clones`) e armadura (`quantidade * (1 - Dano.reducaoArmadura(porNivel * nivel))`
  só pra passiva `armadura`). Golpes avisados de chefe passam pela armadura mas **não** pela evasão.
- `HeroiSystem.bonusPassiva(player): (number, number)` → `(bonusDano, bonusVelAtaque)`;
  fúria ativa quando `hp / hpMax < limiarHp`, senão `(0, 0)`.
- `recalcularHpMax` usa `Herois[heroiId].hpBase`; `resetarTodos` volta ao estado sem herói
  (`heroiId = nil`, atributo nil, movimento travado, teleporte pro `Config.PosicaoInicial`).
- `EstadoHeroiResumo` enviado inclui `heroiId`.
- `EstadoPartida.emAndamento` começa **false**. `PartidaSystem`: remote `EscolherHeroi`
  (rate-limit `RateLimitEscolherHeroi`, payload string) → `HeroiSystem.escolher`; na
  **primeira** escolha com `emAndamento == false` → `iniciar()` (= `reiniciar()` sem o
  `resetarTodos`, zera relógio/abates, `ZonaSystem.reiniciar()`, `emAndamento = true`).
  `aoPedirReinicio` → `reiniciar()` volta todos pra **sem herói** e `emAndamento = false`;
  `PartidaReiniciada` continua indo a todos (cliente reabre a escolha). Derrota só é
  checada com `emAndamento`.
- `travarMovimento` usa `Herois[heroiId].velocidade` (sem herói: travado).

- [ ] Implementar HeroiSystem/EstadoPartida/PartidaSystem conforme acima.
- [ ] Conferir por grep que nenhum sistema usa `Config.HpHeroiBase`/`Config.VelocidadeHeroi`
  (ambos removidos na Task 1).

### Task 4: GolpeSystem por forma + fúria

**Files:**
- Modify: `Server/Systems/GolpeSystem`

**Consumes:** `GolpeDef` (Task 1), `Dano` (Task 2), `HeroiSystem.bonusPassiva` (Task 3),
`InimigoSystem.noRaio/maisProximo/maisProximoXZ/posicao/danificar/existe`,
`HeroiSystem.teleportar`.
**Produces:**
- `GolpeSystem.usarDe(player: Player, golpeId: string, origem: Vector3, multDano: number): boolean`
  — usado pelo loop do herói (`multDano = 1`) e pelo `CloneSystem`. Tabela
  `USAR: { [Forma]: (Player, GolpeDef, string, Vector3, number) -> boolean }`, uma função por forma:
  - `projetil`: `quantidade` projéteis (ângulo de leque de 15° entre eles quando > 1);
    `teleguiado` corrige direção a cada passo pro inimigo mais próximo em `raioAcerto * 4`;
    `perfura` não some no acerto (lista `acertados` por projétil, sem repetir);
    `retorna` ao fim do alcance inverte pro herói (posição atual) e some ao chegar a ≤ 2 studs
    ou se o herói morreu; `acertados` é zerada na virada.
  - `cone`: generaliza `usarChuvaSocos` (acertos espaçados por `Config.IntervaloChuvaSocos`,
    cancelados por `epoca`/pausa — mantém o comportamento atual).
  - `area`: centro = herói, ou `noAlvo` = posição do inimigo mais próximo em `alcance` (sem
    alvo → false); `atraso` agenda o impacto (época/pausa cancelam); `teleportar` move o
    herói para `alvo - direção * TeleporteRecuo` antes do impacto.
  - `linha`: segmento `alcance` × `largura` na direção do inimigo mais próximo; `ticks`
    repetem o acerto a cada `intervalo` (direção fixa no primeiro tick; época/pausa cancelam).
  - `cadeia`: começa no mais próximo em `alcance`, pula `saltos` vezes pro mais próximo
    não acertado em `raioSalto`, um salto a cada `CadeiaIntervalo`.
- Dano final = `Progressao.danoGolpe(def.dano, nível) * Dano.multiplicador(perg, nivel,
  danoPorNivel, bonusDano) * multDano`; recarga = `Dano.recarga(def.recarga, perg, bonusVelAtaque)`.
- Efeito ao cliente (`EfeitoGolpe`): sempre `{ golpe, forma, cor, ox, oz, dx, dz, ... }` com os
  campos da forma (`pid`/`velocidade`/`alcance` em projétil; `alcance`/`acertos` em cone;
  `x, z, raio, atraso` em area; `alcance, largura, ticks, intervalo` em linha;
  `pontos = {x1,z1,x2,z2,...}` em cadeia). `"Fim"` continua pros projéteis.
- `limparTudo` também zera impactos/ticks pendentes (fila própria em vez de `task.delay`,
  como o `ChefeSystem`).

- [ ] Reescrever o GolpeSystem com as 5 formas e `usarDe`; manter `limparTudo/init/start`.
- [ ] Em Edit, `require` do módulo sem erro; grep confirma que não sobrou `Golpes.RajadaKi`/
  `Golpes.ChuvaSocos` hardcoded.

### Task 5: CloneSystem (Haruto)

**Files:**
- Create: `Server/Systems/CloneSystem`
- Modify: `Server/Systems/GolpeSystem` (registra `ultimoGolpe[player]` em `usarDe` quando
  `multDano == 1`), `Server/Systems/PartidaSystem` (`limparSistemas` chama `CloneSystem.limparTudo`),
  `Server/Systems/ZonaSystem` (troca de zona chama `CloneSystem.limparTudo`).

**Consumes:** `HeroiSystem.vivos/obter/posicao/morreu`, `GolpeSystem.usarDe`,
`GolpeSystem.ultimoGolpe(player): string?`.
**Produces:**
- Um clone por herói com passiva `clones`: a cada `intervalo` s (relógio só anda com
  `rodando()`), nasce a `CloneRaioSpawn` studs do herói, vive `duracao` s, parado; a cada
  frame usa `GolpeSystem.usarDe(player, ultimoGolpe, posClone, Config.CloneDanoFrac)` com
  recarga própria. Sem último golpe → usa o `golpeInicial`.
- Remote `"Clone"` (`InfoClone`) ao nascer (`ativo = true`) e ao sumir (`ativo = false`).
- `CloneSystem.limparTudo()` remove todos (manda `ativo = false`). Herói morto/removido → clone some.
- Golpes `area` com `teleportar` **não** teleportam quando usados pelo clone (`multDano ~= 1`
  ⇒ `teleportar` ignorado; documentar no GolpeSystem).

- [ ] Criar CloneSystem e as 3 ligações; `require` em Edit sem erro.

### Task 6: Cliente — escolha, sprites por herói, HUD, efeitos por forma, clones

**Files:**
- Create: `Client/Controllers/HeroiEscolhaController`, `Client/Controllers/CloneRenderController`
- Modify: `Client/Controllers/HeroiSpriteController`, `HudController`, `EfeitosController`,
  `FimController` (Play Again), `LevelUpController` (sem mudança esperada).

- `HeroiEscolhaController`: ScreenGui `EscolhaHeroiGui` (UIScale como a HUD) com título
  "Choose your hero" e 3 cartões (nome, `classe`, `descricao`, nomes dos 4 golpes do kit,
  atalho `[1] [2] [3]`), lidos de `Definicoes/Herois` na ordem Ryuga, Kaizo, Haruto. Clique ou
  tecla → `EscolherHeroi:FireServer(heroiId)`; cartões desabilitam por 1 s após o envio; a
  tela some quando `EstadoHeroi.heroiId ~= nil`; reabre em `PartidaReiniciada`. Enquanto
  aberta, a HUD fica escondida.
- `HeroiSpriteController`: letra/cor de `Herois[player:GetAttribute("HeroiId")]`;
  `GetAttributeChangedSignal("HeroiId")` recria o sprite (atributo nil = sem sprite).
- `HudController`: `Nome` = `Herois[heroiId].name` ao receber `EstadoHeroi`; HUD só visível
  com herói escolhido.
- `EfeitosController`: desenha por `info.forma` com `info.cor` — projétil (bola; `retorna`
  só muda a direção, mesmo pid), cone (leque), area (disco no chão com `atraso` enchendo e
  flash no impacto; teleporte = flash na origem e no destino), linha (barra fina do
  comprimento `alcance`, piscando por tick), cadeia (segmentos entre `pontos`, 0,3 s).
  Pools por tipo de Part (`projetil`, `cone`, `disco`, `barra`, `segmento`).
- `CloneRenderController`: BillboardGui translúcido (letra "H", 50% de transparência) numa
  Part invisível em `workspace.Dinamico` por clone; some em `ativo = false`.
- `FimController`: Play Again continua igual; a escolha reabre pelo `PartidaReiniciada`.

- [ ] Implementar os 2 controllers novos e os ajustes; `require` dos controllers em Edit sem erro.

### Task 7: Teste em Play + revisão

- [ ] Roteiro automatizado (MCP): boot sem erro; tela de escolha aparece; nada spawna antes de
  escolher; escolher Kaizo por tecla → HUD "Kaizo", HP 190, Slingshot Punch acertando em
  linha; subir até nv 7 com `Config` temporário de XP alto e pegar os 4 golpes pelas cartas;
  repetir com Haruto (clone aparece a cada 8 s, some após 6 s; shuriken vai e volta; selo
  explode com atraso); Ryuga com HP < 40% → recarga menor (log); Play Again → volta pra
  escolha, sem clone/projétil/disco sobrando; escolher outro herói na 2ª partida.
- [ ] Revisão independente (subagent) com foco nos 5 itens do Review Focus; corrigir
  Critical/Important; registrar Minor no ledger `.superpowers/sdd/2026-10-29-etapa3a-herois/progress.md`.
- [ ] Atualizar `docs/estado-do-projeto.md` (mapa dos scripts, remotes novos, status) e lembrar
  o Diego de **publicar**.
