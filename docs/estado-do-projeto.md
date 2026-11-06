# Estado do projeto — AnimeBonk

Atualizado em 2026-11-03. Leia junto com `CLAUDE.md` (regras de trabalho) e
`docs/megabonk-referencia.md` (referência do jogo que inspira).

## Onde está o jogo

O código **não está neste repositório**: sem Rojo, todos os scripts vivem dentro dos
places no Roblox e são editados pelo MCP do Studio.

| Place | Nome no Studio | placeId | Papel |
|-------|----------------|---------|-------|
| Menu (inicial) | Menu | 108606222274512 | menus, seleção, co-op (etapa 5) |
| Partida | Partida | 108221889486707 | partida (etapa 1 em diante) |

Experiência (universe) **AnimeBonk**, GameId 10773718205 — renomeada pelo Diego em 2026-11-03
(antes aparecia como "Menu"). O nome do place inicial continua "Menu"; nada no código depende
de nome de place/experiência (só dos placeIds do `Config`).

Dono da experiência (conta pessoal ou grupo): _a definir_. Se for grupo, todo asset
(animação, malha, imagem, áudio, badge) precisa ser publicado em nome do grupo —
animação de outro dono não carrega ("Failed to load animation"). Lição do Table_Stories.

## Mapa dos scripts

### Place Partida (108221889486707) — etapa 1

- `Workspace/Mapa/Chao` (400×2×400, grama) e `Mapa/SpawnJogador` (invisível).
- `ReplicatedStorage/Shared`
  - `Types`, `Config` (todos os números da partida), `Remotes` (`get`/`getUnreliable`)
  - `Definicoes/Herois` e `Golpes` (ver etapa 3a abaixo — formato atual), `Inimigos`
    (Lanterna, Tanuki), `Pergaminhos` (Dano, VelAtaque, HpMax)
  - `Logica/Progressao` (curva de XP, dano por nível), `Logica/Cartas` (sorteio de
    cartas), `Logica/Dano` (multiplicadores, recarga, HP máx.)
- `ServerScriptService/Server`
  - `Server` (Script de entrada: cria remotes, bootstrap init/start)
  - `EstadoPartida` (emAndamento, pausadoPorCarta — fonte única de pausa/fim)
  - `Testes/TesteLogica` (rodar na barra de comando:
    `require(game.ServerScriptService.Server.Testes.TesteLogica)()`)
  - `Systems/HeroiSystem` (HP, XP, nível, golpes, pergaminhos; esconde o avatar)
  - `Systems/InimigoSystem` (inimigos como dados, grade espacial, snapshots em buffer)
  - `Systems/GolpeSystem` (golpes automáticos, projéteis como dados)
  - `Systems/XpSystem` (orbes de XP, coleta por proximidade)
  - `Systems/LevelUpSystem` (fila de ofertas, validação de `EscolherCarta`)
  - `Systems/PartidaSystem` (relógio, abates, vitória/derrota, `Reiniciar`)
- `StarterPlayer/StarterPlayerScripts/Client`
  - `Client` (LocalScript de entrada)
  - `Controllers/HeroiSpriteController`, `InimigoRenderController`,
    `EfeitosController`, `LevelUpController`, `HudController`, `FimController`
- Remotes (`ReplicatedStorage/Remotes`, criados pelo servidor): Snapshot (unreliable,
  dividido em pacotes de até 60 inimigos), InimigoMorreu, XpOrbs, EfeitoGolpe,
  EstadoHeroi, OfertaCartas (com `ofertaId`), EscolherCarta (`ofertaId, indice`),
  FimPartida, Relogio, Reiniciar, PartidaReiniciada.
- Visual ainda é placeholder (quadrados coloridos com letra) até a arte dos sprites.

### Place Partida — etapa 2 (zonas e chefes)

- `Workspace/Mapa/Zonas/{Vila, Bambuzal, Templo, Santuario}` — cada uma com `Chao`,
  `Spawn`, `Altar` (onde aparece o ProximityPrompt "Summon Guardian"), `Portal`
  (posição do portal), paredes invisíveis e `Decoracao` provisória. Áreas no eixo X:
  0, 600, 1200, 1800.
- `Shared/Definicoes/Zonas` (ordem e guardião de cada zona) e `Definicoes/Chefes`
  (Stone Komainu, Bamboo Ronin, Temple Tengu, Eclipse Oni — golpe em área com aviso,
  Oni invoca lacaios).
- `Server/Systems/ZonaSystem` — fase explorar → chefe → portal, timer de 10:00 por
  zona, Cerco Final, recompensa (cura + cartas extras), portal (todos dentro ou 10 s),
  vitória na saída do Santuário.
- `Server/Systems/ChefeSystem` — IA de golpe dos chefes (relógio próprio, pausa-safe).
- `Client/Controllers/ZonaHudController` (zona, objetivo, FINAL SIEGE, barra do chefe,
  contagem do portal, marcadores "!" e "↑"), `AvisoController` (círculo vermelho).
- Remotes novos: Zona, Chefe, Aviso.
- `workspace.Dinamico` (criado em runtime): portal ativo.

### Place Partida — etapa 3a (heróis, kits de 4 golpes, escolha de herói)

- `Shared/Definicoes/Herois`: Ryuga, Kaizo, Haruto com `classe`, `descricao`, `hpBase`,
  `velocidade`, `letra`/`cor` (sprite placeholder), `kit` de 4 golpes e `passiva` como dado
  (`furia` Ryuga, `armadura` Kaizo, `clones` Haruto). Ordem da tela em `Config.OrdemHerois`.
- `Shared/Definicoes/Golpes`: 12 golpes em 5 **formas** genéricas (`projetil` com
  leque/teleguiado/perfura/retorna, `cone`, `area`, `linha`, `cadeia`) — o `GolpeSystem`
  implementa cada forma uma vez, sem código por golpe. `Config.HpHeroiBase`/`VelocidadeHeroi`
  saíram (vivem no `HeroiDef`); `Config` ganhou `ArmaduraK`, `EvasaoMax`, `CloneDanoFrac`,
  `CloneRaioSpawn`, `CadeiaIntervalo`, `TeleporteRecuo`, `RateLimitEscolherHeroi`.
- `Logica/Dano`: `reducaoArmadura`, `evasao`, `bonusExtra` em `multiplicador`/`recarga`.
- `Server/Systems/HeroiSystem`: jogador começa **sem herói** (`heroiId = nil`, parado);
  `escolher(player, id)` (uma vez por partida), atributo `HeroiId` no Player (replica pros
  sprites), `escolheram()`, `bonusPassiva()`, evasão/armadura em `aplicarDano`.
- `Server/Systems/PartidaSystem`: `EstadoPartida.emAndamento` começa false; a partida
  **começa na primeira escolha** (`iniciar()`); Play Again volta todos pra tela de escolha;
  derrota só conta quem escolheu.
- `Server/Systems/GolpeSystem`: reescrito por forma; `usarDe(player, golpeId, origem,
  multDano)` e `ultimoGolpe(player)`; fila própria de ações agendadas (ticks/atraso/saltos)
  com relógio que congela na pausa e cancela na morte do dono/limparTudo.
- `Server/Systems/CloneSystem` (novo): clone do Haruto (1 por herói, nasce a cada
  `intervalo`, vive `duracao`, repete o último golpe com `CloneDanoFrac`).
- Cliente: `HeroiEscolhaController` (tela "Choose your hero", teclas 1/2/3),
  `CloneRenderController` (sprite translúcido em `workspace.ClonesVisual`),
  `HeroiSpriteController`/`HudController` leem letra/cor/nome do herói pelo atributo; HUD
  só aparece com herói; `EfeitosController` desenha por forma (cor do `GolpeDef`).
- Remotes novos: `EscolherHeroi` (cliente→servidor, string validada + rate-limit), `Clone`.
- `EfeitoGolpe` agora manda `{ golpe, ... }` por forma e os eventos `Fim`/`Volta`.
- Ledger: `.superpowers/sdd/2026-10-29-etapa3a-herois/progress.md`.
- Fora desta etapa: ultimates, despertares nv 20/40, fusão, golpes genéricos de elemento.

### Place Partida — etapa 3b (Pergaminhos, raridade, moedas, baús, mercador)

- `Shared/Definicoes/Pergaminhos`: 13 ids com `porNivel`/`descricao` — Power, Speed, Volley
  (+1 projétil/acerto/salto a cada 2 nv), Reach, Lasting, Critical, Vitality, Iron, Mending,
  Swift, Magnet, Wisdom e **Cursed Scroll** (`amaldicoado`, teto 5: +inimigos/+HP, +XP/+moedas).
  Ordem de sorteio em `Config.OrdemPergaminhos`.
- `Logica/Dano`: `nivel/mult/extra/flat/critico(perg, id)` — todo sistema lê stats por aí.
- `Logica/Cartas`: **raridade** por carta (`Config.RaridadePesos`); só muda quantos níveis a
  carta dá (`Config.RaridadeNiveis`: 1/1/2/2/3), respeitando o teto. Golpe novo é sempre comum.
- `HeroiSystem`: `moedas` (+ resumo), `ganharMoedas/gastarMoedas` (nunca negativo), regen
  (Mending), velocidade (Swift), armadura flat (Iron), XP × Wisdom × maldição,
  `recalcularStats` + evento `pergaminhoMudou`, `maldicaoTotal()`.
- `GolpeSystem`: Volley/Reach/Lasting aplicados por forma; crítico sorteado por uso.
- `XpSystem`: orbes com `tipo` (0 XP azul / 1 moeda dourada); chance `ChanceMoeda` nos comuns,
  `MoedasChefe` nos chefes; raio de coleta × Magnet.
- `ZonaSystem`: maldição (soma dos Cursed de todos) multiplica spawn/HP; ao iniciar a zona chama
  `BauSystem.gerar` e `MercadorSystem.gerar`; `encerrar` limpa os dois.
- `BauSystem` (novo): sorteia `BausPorZona` entre os marcadores estáticos
  `Zonas/<zona>/Baus/Bau1..6`; prompt "Open Chest" (custo sobe por zona e por baú aberto);
  abre → oferta extra de cartas (itens vêm na 3c). Baús em `workspace.BausAtivos`.
- `MercadorSystem` (novo): prompt "Trade" na Part estática `Zonas/<zona>/Mercador`; 3 itens por
  jogador e por zona (pergaminho +1, melhoria do golpe mais baixo, cura total), preço
  × 1.5^(zona−1); servidor guarda a oferta e valida `ComprarLoja(ofertaId, i)`.
- Cliente: `LevelUpController` (borda/faixa por raridade + descrição), `HudController`
  ("Coins: N"), `EfeitosController` (orbe dourada), `LojaController` (novo: painel do mercador,
  teclas 1/2/3, Esc/longe fecha).
- Remotes novos: `Loja`, `ComprarLoja`. `XpOrbs.criados` agora é `[id, x, z, tipo, ...]`.
- Ledger: `.superpowers/sdd/2026-10-29-etapa3b-pergaminhos-economia/progress.md`.
- **Não testado pelo Claude** (prompt não dispara via MCP): abrir baú, comprar na loja, Cursed
  Scroll em jogo — testar manualmente.

### Place Partida — etapa 3c (itens, status, reações)

- `Shared/Definicoes/Itens`: 22 itens com `raridade` (comum max 3 / incomum max 2 /
  lendário max 1), `letra` (ícone placeholder) e `efeito` tipado (`stat`, `aoAcertar`,
  `aoMatar`, `condicional`, `reviver`, `critMult`, `reacaoDano`). Lendários: Phoenix Feather
  (revive 1×), Dragon Scale (+40 armadura), Hunter's Mark (crit ×2.5), Storm Core (reações
  causam +50% do acerto em área).
- `Golpes.elemento` (Ki / Impacto / Vento por herói). `Logica/Dano.*` aceitam `bonus`
  (tabela por stat dos itens).
- `InimigoSystem`: status por slot (Burning, Wet, Stunned, Cursed, Slowed; chefes: duração
  × `ChefeResistenciaStatus`, Stunned ignorado), `aplicarStatus`, `danificar(id, dano,
  matador, elemento)` com **reações** (Tempest = Vento+Wet, Wildfire = Vento+Burning,
  Rupture = Ki+Stunned ×2, Steam = Burning+Wet → Slowed, Shatter = Impacto+Cursed → área);
  reação espalha status com `semReacao` (sem cadeia). Queimadura por tick com crédito do
  abate. Snapshot ganhou 1 byte de status (`TAM_ENTRADA 15`, 55 entradas/pacote).
- `ItemSystem` (novo): `dar/sortear/recalcular` → `e.bonus`, `e.aoAcertar`,
  `e.condicionais`; Rice Ball cura por abate. `BauSystem` dá item (70%) ou cartas.
- `HeroiSystem`: `itens` no estado/resumo, Phoenix Feather em `aplicarDano`, condicionais em
  `bonusPassiva`; `MercadorSystem` aplica desconto (`PrecoLoja`).
- Cliente: `ItemController` (toast "Found: …" + faixa de inventário), `InimigoRenderController`
  (contorno colorido por status), `EfeitosController` (disco da reação). Remotes: `Item`, `Reacao`.
- Ledger: `.superpowers/sdd/2026-10-29-etapa3c-itens-status-reacoes/progress.md`.
- **Não testado pelo Claude**: receber item, status/reações em jogo, revive (dependem do baú).

### Place Partida — etapa 4 (co-op no mesmo place)

- `Config` bloco "Co-op": `SpawnPorJogadorExtra`, `TetoPorJogadorExtra`, `ChefeHpPorJogadorExtra`
  (×(1 + k·(n−1))), `HpReviver 0.5`, `TempoReviver 3`, `RaioReviver 8`.
- `InimigoSystem.passo`: taxa e teto escalam pelos heróis vivos. `ZonaSystem.invocar`: vida do
  guardião escala por `#escolheram()`.
- `HeroiSystem`: herói que zera fica **caído** (`vivo=false`, atributo `Caido`, movimento
  travado) com ProximityPrompt "Revive" no `HumanoidRootPart` (segurar E 3 s);
  `HeroiSystem.reviver(alvo, por)` valida no servidor (aliado vivo, distância, partida rodando)
  → 50% HP + invuln; evento `reviveu`. Solo: caído = derrota na hora (nenhum vivo).
  `vivos()`/`escolheram()` reaproveitam uma tabela (chamador só itera na hora).
- `CloneSystem`: quem entra no meio recebe os clones ativos. `ZonaSystem`: maldição reaplicada
  quando alguém sai. Cliente: sprite do caído fica apagado.
- Fora (etapa 5+): sala com código, tela "End Match / Revive All" de 15 s, Segundo Fôlego pago.
- Ledger: `.superpowers/sdd/2026-10-29-etapa4-coop/progress.md`. **Testar com 2 clientes**
  (Test → Clients and Servers) — o Claude só testou solo.
- Revisão: prompt Revive mede o tempo segurando no servidor; `Config.ProtecaoCartas` = 5 s de
  invulnerabilidade ao abrir cartas no co-op; pausa das cartas conta `escolheram()`.

### Place Partida — etapa 5a (perfil persistente + Essência)

- `Shared/Logica/Perfil` (puro): `VERSAO = 1`, `novo()`, `migrar(dados)` (schema versionado,
  nunca perde Essência, descarta campos desconhecidos), `essenciaDaPartida` (nível×2 +
  abates/10 + 100 na vitória), `registrarFim`.
- `Server/Systems/PerfilSystem`: DataStore `"Perfil"`, chave `u<UserId>`; load no `PlayerAdded`
  com 3 tentativas (backoff 1/2/4 s); **se o load falhar o perfil fica só em memória e nunca é
  salvo** (não sobrescreve o remoto); save no `PlayerRemoving`, autosave (120 s, só sujos) e
  `BindToClose` (paralelo, espera ≤ 25 s e os saves em andamento); contador de revisão por
  jogador (`rev`/`revSalva`) em vez de flag; save via `UpdateAsync` com contador `gravacao`
  no perfil (nunca escreve por cima de um dado mais novo de outro servidor). Remote
  `Perfil` (s→c) manda o perfil ao carregar e no fim da partida.
- `PartidaSystem.terminar` registra o fim (só de quem escolheu herói) e manda
  `essenciaGanha/essenciaTotal` na `FimPartidaInfo`; `FimController` mostra "Essence +N (total T)".
- `Types.Perfil` é o schema; mudar = subir `VERSAO` + tratar em `migrar`.
- **No Studio** o DataStore só funciona com Game Settings → Security → "Enable Studio Access
  to API Services"; sem isso aparece o warn `[Perfil] ... só em memória` (esperado).
- Ledger: `.superpowers/sdd/2026-10-29-etapa5a-perfil-essencia/progress.md`.

### Place Menu — etapa 5b

- Place Menu (108606222274512). Mesmo bootstrap do Partida:
  - `ReplicatedStorage/Shared`: **cópias fiéis** de `Types`, `Config`, `Remotes`,
    `Definicoes/Herois`, `Golpes`, `Zonas`, `Chefes`, `Logica/Perfil` (conferidas por checksum).
  - `ServerScriptService/Server/Server` (cria remotes `Perfil`, `IrParaPartida`, `Menu`) +
    `Systems/PerfilSystem` (cópia fiel do Partida) + `Systems/MenuSystem` (novo).
  - `StarterPlayer/StarterPlayerScripts/Client/Client` + `Controllers/MenuController` (novo).
- **Layout segue o PokeBonk** (pedido do Diego, pra ele personalizar tela por tela): tela
  inicial (logo, Play grande + modos, atalhos, painel "Your profile" à direita) → seleção de
  herói (ficha à esquerda, lista à direita com trancados em cinza + cadeado + desafio, teclas
  1/2/3, Enter) → "Prepare match" (região, guardiões por zona, modo/dificuldade, recordes,
  Start). Atalhos sem sistema = apagados com "Coming soon". UI toda por `Instance.new`
  (`PlayerGui.MenuGui`).
- `MenuSystem`: `IrParaPartida(heroiId)` → rate-limit 1 s, string, herói existe, perfil
  carregado, `desbloqueios[heroiId]`; `PerfilSystem.salvarAgora` (recusa se o save falhar);
  `TeleportAsync(Config.PlaceIdPartida, {player}, options)` com `TeleportData = { heroiId }`;
  erro → warn + remote `Menu` `{ erro }`. No Studio: só warn + "Teleport only works in the
  published game".
- Partida (5b): `PartidaSystem` lê `GetJoinData().TeleportData.heroiId` no `PlayerAdded` e
  passa por `aoEscolherHeroi` (mesma validação do remote); `PerfilSystem.desbloquear(player,
  id)` e `salvarAgora(player)`; `ZonaSystem.avancar` (zona 1 → 2) libera **Kaizo**;
  `PartidaSystem.terminar("vitoria")` libera **Haruto**. `HeroiDef.desafio` = texto do desafio.
- **Replicar no Menu** qualquer mudança em `Types`, `Config`, `Remotes`, `Definicoes/Herois`,
  `Golpes`, `Zonas`, `Chefes`, `Dojo` (5c), `Ultimates` (6a), `Conquistas` (6b), `Tarefas` (6c),
  `Logica/Perfil`, `Logica/Conquistas` (6b), `Logica/Tarefas` (6c), `Localizacao/PtBr` (6c), `Definicoes/Emblemas` (7),
  `Logica/Cla` (7), `Definicoes/Dificuldades` (2026-10-30), `Definicoes/Inimigos` (Mobs), `Definicoes/Skins` (Skins), no bloco de
  tradução do `Server` (6c), em `Systems/PerfilSystem`, `Systems/RankingSystem` (6b), `Systems/ConfigSystem`
  (6b) e em `Client/Controllers/LocalizacaoController` (6c) do Partida.
- Ledger: `.superpowers/sdd/2026-10-29-etapa5b-menu/progress.md`. **Teleporte só testável
  publicado** (Menu → Partida com o herói; publicar os 2 places).
- `EscolherHeroi` exige desbloqueio fora do Studio (livre no Studio pra testar). Recusa
  (herói trancado / perfil carregando) avisa o cliente pelo remote `MensagemHeroi` (s→c,
  `Types.MensagemHeroi { texto }`), mostrado 3 s abaixo dos cartões no
  `HeroiEscolhaController`, que também mostra "LOCKED" nos trancados pelo remote `Perfil`
  (só fora do Studio). O herói do TeleportData espera Character **e** perfil
  (`Config.EsperaPersonagemTeleporte`). Menu: `teleportando` limpo na saída do jogador e
  por timeout (`Config.TimeoutTeleporte` = 30 s).

### Etapa 5c — Dojo de Treino (2 places)

- **Shared (idêntico nos 2 places, conferido por checksum):** `Types.Perfil` + `dojo: { [string]:
  number }` (schema **v2**); `Logica/Perfil`: `VERSAO = 2`, `novo()` com `dojo = {}`, `migrar`
  aceita v0/v1 (cria `dojo = {}`) e valida o dojo (só ids conhecidos, inteiro ≥ 0, limitado ao
  `nivelMax`), `custoDojo(nivel)` = `DojoCustoBase × (nivel+1)` (50…250), `comprarDojo(p, id)`
  (puro: valida e desconta). `Definicoes/Dojo` (novo): Forca/Power (Dano +2%), Vitalidade/
  Vitality (HpMax +3%), Agilidade/Swiftness (Velocidade +2%), Sabedoria/Wisdom (Xp +3%),
  Sorte/Fortune (Critico +1%), Ima/Magnet (Coleta +5%), 5 níveis. `Config`: `DojoCustoBase = 50`,
  `RateLimitComprarDojo = 0.5`, `OrdemDojo`, `TimeoutTeleporte`, `DuracaoMensagemHeroi`.
- **PerfilSystem (2 places, idêntico):** `marcarMudanca(player)` (rev += 1 e envia `Perfil`),
  `salvarAgora(player, motivo?)`, evento `PerfilSystem.carregou` (BindableEvent, player).
- **Menu:** `Systems/DojoSystem` — remote `ComprarDojo(id)` (c→s): rate-limit 0,5 s, string, id
  existe, perfil carregado, `Perfil.comprarDojo` (nível < máx., Essência suficiente) →
  `marcarMudanca` + `salvarAgora(player, "dojo")`; recusa → remote `Menu { erro }`.
  `MenuController`: atalho **Dojo** ligado à tela `TelaDojo` (Essência no topo, 6 linhas com
  nome, descrição, "Lv x/5", "N Essence"/MAX, botão Buy apagado quando não dá; Esc/Back).
- **Partida:** `ItemSystem.recalcular` soma `perfil.dojo[id] × porNivel` em `e.bonus[stat]` (a
  mesma tabela dos itens); `ItemSystem` chama `recalcular` em `HeroiSystem.escolheu` e em
  `PerfilSystem.carregou` (se o jogador já tem herói). `TesteLogica` cobre v1→v2, validação do
  dojo, custo e compra.
- Ledger: `.superpowers/sdd/2026-10-29-etapa5c-dojo/progress.md`.
- Revisão final 5c: `DojoSystem` recusa compra com teleporte em andamento
  (`MenuSystem.estaTeleportando`) e com perfil somente leitura (`PerfilSystem.podeSalvar`, nos 2
  places; liberado no Studio); Buy apagado enquanto o Start mostra "Teleporting...".
- **Publicar Menu e Partida sempre juntos** (schema do perfil: um Partida v1 lendo perfil v2
  não salva).

### Etapa 6a — ultimates e despertares

- **Shared (idêntico nos 2 places, checksum):** `Definicoes/Ultimates` (novo): `golpes` (9
  `GolpeDef` completos, ids `Ult...`) + `herois[id].versoes` (3 ids: base / nv 20 / nv 40) —
  Ryuga Ki Burst → Crimson Meteor → Celestial Beam; Kaizo Cannon Punch → Giant Fist Rain →
  Captain's Hammer; Haruto Thousand Clones Strike → Wolf Howl (atordoa) → Beast Unleashed.
  `Herois.despertares` (nv 20 / 40: Crimson/Celestial Aura, Spring/Storm Mode, Wolf Mantle/Beast
  Awakening; `cor`, `multDano` 1.15/1.3, `multHp` 1.15/1.3, `multVel` 1.05/1.1). `Golpes.GolpeDef`
  + `aplicaStatus?`. `Config`: `UltimateCargaPorDano 0.0008`, `RateLimitUltimate 0.5`,
  `IntervaloUltimate 0.25`. `Types.InfoUltimate { carga, name }`.
- **Partida servidor:** `Systems/UltimateSystem` (novo): carga 0..1 por dano causado
  (`InimigoSystem.danoCausado`, BindableEvent em cada `danificar` com matador; chefes contam);
  remote `UsarUltimate` (rate-limit, `rodando()`, vivo, carga cheia) usa a versão do despertar via
  `GolpeSystem.usarDef` (não vira "último golpe": o clone não copia); sem alvo não gasta a carga;
  envia `Ultimate` 4×/s só quando muda; `limparTudo` no `PartidaSystem.limparSistemas` (troca de
  zona mantém a carga). `HeroiSystem`: `despertar` 0/1/2 (`atualizarDespertar` no fim do
  `ganharXp`, `despertar(player)`), atributo `Despertar` no Player, `multHp` no HP máx.,
  `multVel` no WalkSpeed, `multDano − 1` no `bonusPassiva`; zera em `escolher`/`resetarTodos`.
  Remotes novos no `Server`: `UsarUltimate` (c→s), `Ultimate` (s→c).
- **Partida cliente:** `Controllers/UltimateController` (barra roxa acima do HP com nome + "[R]",
  pisca cheia, tecla R, botão touch "ULT"); `HeroiSpriteController` troca cor e põe aura
  (UIStroke grosso) pelo `Despertar`; `EfeitosController` procura o def em `Golpes` e depois em
  `Ultimates.golpes`.
- `TesteLogica`: 3 versões completas por herói, ids sem colisão, despertares nv 20/40 crescentes.
- Ledger: `.superpowers/sdd/2026-10-29-etapa6a-ultimates-despertares/progress.md`. Despertar
  não testado em Play (nível 20) — teste manual do Diego.
- Revisão final 6a: o dano da própria ultimate **não carrega** a ultimate (`GolpeSystem.usarDef(...,
  semCarga)` marca acertos/pendentes/projéteis; `InimigoSystem.danificar(..., semCarga)`); a carga conta
  só o dano efetivo (`min(dano, hp)`); BindableEvent `danoCausado` virou callback
  `InimigoSystem.aoDanoCausado`; rate-limit do servidor com folga de 0,1 s; Menu mostra os nomes das 3
  ultimates na ficha do herói.

### Etapa 6b — conquistas, ranking, configurações

- **Shared (idêntico nos 2 places, checksum):** `Types` + `Estatisticas`, `ConfigJogador`,
  `EstatisticasPartida`, `InfoConquista`, `EntradaRanking`, `InfoRanking`; `Perfil` **v3** com
  `estatisticas` (abatesTotal, chefesDerrotados, partidas, vitorias, nivelMax, abatesKi/Impacto/Vento),
  `conquistas { [id]: true }` e `config { musica, efeitos, mostrarDano, escalaHud }`. `Logica/Perfil`:
  `VERSAO = 3`, `configPadrao()` (0.7 / 0.8 / true / 1), `configValida(c)` (estrita, pro remote),
  `migrar` v2→v3 (semeia partidas/vitórias/nível máx. do histórico; config campo a campo).
  `Definicoes/Conquistas` (13: First Steps, Village Cleared → Kaizo, Region Champion → Haruto, Hunter
  I/II/III, Boss Slayer, Ki Master, Iron Fist, Wind Walker, Level 20/40, Veteran) e `Logica/Conquistas`
  (puro: `registrarPartida` 1× por partida, `avaliar` idempotente → Essência + desbloqueio). `Config`:
  `OrdemConquistas`, `DuracaoToastConquista`, `RankingTop 10`, `RankingCacheSegundos 60`,
  `RateLimitRanking 5`, `RankingTentativas 2`, `RateLimitSalvarConfig 1`, `EscalaHudMin/Max 0.6/1.4`,
  `PassoVolume`, `PassoEscalaHud`.
- **Servidor (idêntico nos 2 places):** `Systems/RankingSystem` — OrderedDataStores
  `MelhorTempoVitoria` (menor vence, só vitória) e `MaisAbates` (maior vence) via `UpdateAsync` (só grava
  se melhor), `registrar` (Partida, no fim), `top(nome)` com cache 60 s, remote `Ranking` (c→s nome,
  s→c `InfoRanking`, rate-limit 5 s por placar). `Systems/ConfigSystem` — remote `SalvarConfig` (validado)
  → `perfil.config` + `marcarMudanca`.
- **Partida:** `Systems/ConquistaSystem` (abates, abates por elemento do golpe que matou — 6º arg de
  `InimigoSystem.morreu` —, guardiões, zonas concluídas; `zonaConcluida` avalia na hora;
  `fimDaPartida` antes do `registrarFim`). Gatilhos antigos de desbloqueio (Kaizo no `ZonaSystem.avancar`,
  Haruto no `terminar`) **migrados para as conquistas**. Cliente: `ConquistaController` (toast
  "Achievement: X (+N Essence)", 4 s cada), `ConfigController` (Esc ou botão "Settings": música/efeitos/
  tamanho da HUD −/+, números de dano on/off; aplica em SoundGroups `Musica`/`Efeitos` se existirem e
  `UIScale EscalaConfig` na `HudGui`). Remotes novos: `Conquista`, `Ranking`, `SalvarConfig`.
- **Menu:** atalhos **Achievements** (`TelaConquistas`), **Leaderboard** (`TelaRanking`, abas Best time /
  Most KOs, nomes por `GetNameFromUserIdAsync`) e **Settings** (`TelaConfig`) ligados. Remotes novos:
  `Ranking`, `SalvarConfig`.
- Ledger: `.superpowers/sdd/2026-10-29-etapa6b-conquistas-ranking/progress.md`. Ranking só funciona
  publicado (ou com API Services no Studio); toast/desbloqueio por conquista não testados em Play.
- Revisão final 6b (corrigida na 6c): `PerfilSystem.travar/estaTravado` (2 places) — o `MenuSystem` aplica a
  config pendente, trava antes do save do teleporte e destrava em falha/timeout; `ConfigSystem` e `DojoSystem`
  recusam travado; `ConfigSystem` guarda o pedido dentro do rate-limit como pendente (aplica no fim da janela);
  `MenuController` envia a config do debounce antes do `IrParaPartida`; `ConquistaSystem` só soma partida com
  marcador (criado no `escolheu`); `GolpeSystem` roda ações agendadas em `pcall`; Storm Core não acerta o
  próprio alvo; `Logica/Perfil` migra estatísticas por lista explícita.

### Etapa 6c — tarefas diárias, tradução pt-BR, visual placeholder melhor

- **Shared (idêntico nos 2 places, checksum):** `Types` + `TarefaDoDia`, `TarefasPerfil`, `InfoTarefa`,
  `InfoTarefas`; `Perfil` **v4** com `tarefas { dia, lista, streak, ultimoDiaCompleto }` (`Logica/Perfil`:
  `VERSAO = 4`, `tarefasNovas()`, `migrar` v3→v4 cria vazio e valida ids/progresso). `Definicoes/Tarefas` (10:
  Defeat 300/1000 enemies, Open 2 chests, Win a run, Reach level 15/25, Use your ultimate 5 times, Defeat 2
  guardians, Collect 100 coins, Play 3 runs) e `Logica/Tarefas` (puro: `diaHoje` UTC, `numeroDia`,
  `sortear(userId, dia)` determinístico, `garantirDia(perfil, userId, dia)` — streak zera se pulou um dia —,
  `progredir` (1× por tarefa; "nivel" usa o máximo), `bonusStreak` = min(streak, 7) × 10, `infoPerfil`).
  `Config`: `TarefasPorDia`, `OrdemTarefas`, `EssenciaStreakPorDia`, `StreakMax`, `IntervaloTarefas`.
  `Localizacao/PtBr` (324 pares en→pt). `PerfilSystem.marcarMudanca(player, semEnviar?)`.
- **Servidor:** `Server` dos 2 places gera `ReplicatedStorage/Localizacao/PtBr` (LocalizationTable, `SetEntries`)
  no boot e cria o remote `Tarefa` (s→c). **Partida:** `Systems/TarefaSystem` (abates, guardiões, baús —
  `BauSystem.aoAbrirBau` —, ultimates — `UltimateSystem.aoUsarUltimate` —, moedas — `HeroiSystem.aoGanharMoedas` —,
  nível — `subiuNivel` —, partidas/vitória no `PartidaSystem.terminar`); conclusão → Essência + `marcarMudanca` +
  `Tarefa` com `concluidas`. **Menu:** `Systems/TarefaSystem` (garantirDia no `carregou` + envia `Tarefa`).
- **Cliente:** `LocalizacaoController` (2 places, idêntico) liga `AutoLocalize` + `RootLocalizationTable` em toda
  ScreenGui. Partida: `ConquistaController` mostra "Task complete: X (+N)" e o bônus de streak;
  `Util/SpriteComposto` (sombra, corpo, faixa, cabeça, letra) usado por `HeroiSpriteController`,
  `CloneRenderController` (pool simples de 2 visuais, revisão 6c) e `InimigoRenderController` (pool; guardiões 1,6× com contorno dourado);
  `EfeitosController` (brilho `ParticleEmitter` nas orbes, flash branco 0,2 s nas ultimates);
  `ZonaVisualController` (novo: Lighting + Atmosphere por zona). Menu: atalho **Daily Tasks** → `TelaTarefas`
  (3 tarefas, progresso, ✓, Essência, "Streak: N days").
- Ledger: `.superpowers/sdd/2026-10-29-etapa6c-tarefas-traducao-visual/progress.md`. Tradução não testada com o
  idioma pt-BR (usar emulação de idioma no Studio); conclusão de tarefa/streak não testadas em Play.

- Revisão final 6c (corrigida na 7): `Tarefas.garantirDia` ignora dia anterior ao do perfil e completa lista
  incompleta sem zerar; `MenuSystem` com token por tentativa de teleporte; textos dinâmicos traduzidos por
  `LocalizacaoController.formatar/traduzir` (PtBr com `key` e `{1}`; Translator pelo idioma do jogador); pcall
  nos callbacks de tarefa; render de inimigos só escreve quando hp/status mudam; orbes com ColorSequence
  cacheada; sprite de herói sem duplicado; config travada fica pendente até destravar; Menu revisa a virada do
  dia a cada 60 s; clones com pool de 2.

### Etapa 7 — clãs

- **Shared (idêntico nos 2 places, checksum):** `Types` + `ClaPerfil`, `EmblemaCla`, `EntradaCla`, `CargoCla`, `Cla`
  (registro: id, nome, sigla, emblema, descricao, lider, oficiais, membros em ordem de entrada, vagas, entrada,
  pedidos, convidados, pontos, criadoEm), `ResumoCla`, `MembroCla`, `InfoCla`, `ListaCla`, `MensagemCla`; `Perfil`
  **v5** com `cla { id?, sigla?, convites, pedidosFeitos }` (`Logica/Perfil`: `VERSAO = 5`, `claNovo()`, `migrar`
  v4→v5). `Logica/Cla` (puro: `nomeValido`, `siglaValida`, `descricaoValida`, `emblemaValido`, `pontosDaPartida` =
  abates/10 + guardiões×20 + 100 na vitória, `custoAmpliar`, `novo`, `cargo`, `adicionarMembro`, `removerMembro`
  com sucessão oficial mais antigo → membro mais antigo → dissolve, `promover`, `rebaixar`, `registrarPedido`).
  `Definicoes/Emblemas` (formas Circle/Shield/Diamond/Hexagon, símbolos ✿ 🐺 🔥 ~ ☾ ★, 8 cores). `Config`:
  `ClaCustoFundar 500`, `ClaVagasBase 30`, `ClaVagasMax 100`, `ClaCustoVaga 10`, `ClaVagasPorAmpliacao 10`,
  limites de texto/listas, `RateLimitClaFundar 10`, `RateLimitCla 1`, `ClaRankingCacheSegundos 60`.
- **Menu:** `Systems/ClaSystem` — DataStores `Clas` (registro, sempre `UpdateAsync` com as regras dentro),
  `ClasPorNome` (nome minúsculo → id; reserva com `UpdateAsync` que recusa se existe) e OrderedDataStore
  `PontosCla`. Remotes (criados no `Server`): `ClaFundar`, `ClaBuscar`, `ClaPedir`, `ClaCancelarPedido`, `ClaAceitar`,
  `ClaRecusar`, `ClaConvidar` (só jogador online no mesmo servidor), `ClaResponderConvite`, `ClaSair`, `ClaExpulsar`,
  `ClaPromover`, `ClaRebaixar`, `ClaMudarEntrada`, `ClaAmpliar`, `ClaRanking`, `ClaMeu` (c→s e s→c) e `ClaMensagem`
  (s→c). Filtro do Roblox obrigatório (falha = recusa). O registro do clã é a verdade; `perfil.cla` é cache
  reconciliado no `PerfilSystem.carregou`. `MenuController`: atalho **Clan** → `TelaClaBuscar`, `TelaClaMeu`,
  `TelaClaCriar` (editor de emblema), `TelaClaRanking`, `TelaClaInbox`; painel de perfil mostra "[SIGLA] Nome".
- **Partida:** `Systems/ClaPontosSystem` (guardiões do grupo por jogador; no `terminar` soma os pontos no clã via
  `UpdateAsync` só se ainda é membro, + `PontosCla`); `HudController` mostra "[SIGLA] Nome" pelo remote `Perfil`.
- Ledger: `.superpowers/sdd/2026-10-29-etapa7-clas/progress.md`. **Nada de clã com DataStore testado** (Studio sem
  API Services): testar publicado com 2 contas. Publicar Menu e Partida juntos (Partida v4 lendo perfil v5 não salva).
- **Correções da revisão final (2026-10-30):** `PerfilSystem.ocupar/estaOcupado` (nos 2 places) — ação de clã
  marca ocupado e o `MenuSystem` recusa o teleporte ("Finishing your clan action... try again."); fundar grava
  `perfil.cla.id` + save antes de criar o registro (falha → limpa e devolve a Essência) e join aberto grava
  `pedidosFeitos` antes; reserva de nome/criação idempotentes, nome de clã morto (registro dissolvido ou sem registro
  há mais de `ClaNomeOrfaoSegundos 300`) pode ser refundado; `apagarCla` com retry (nome → registro → ranking por
  último); escrita no perfil do alvo revalidada depois do yield; busca com texto 5 s (`RateLimitClaBuscar`), 1 por
  vez, `cacheBusca` com teto 50 (`ClaBuscaCacheMax`), `ListKeysAsync` sem chaves apagadas; limpar `pedidosFeitos`
  também tira o membro dos outros clãs; `ClaMeu` com cache de 5 s (`ClaMeuCacheSegundos`); cancelar pedido só sai
  do perfil se o clã registrou. Partida `ClaPontosSystem`: soma idempotente (`ultimaPartida[userId] = idPartida`) e
  ranking só com registro vivo. Chaves novas do `Config` replicadas nos 2 places.

### Polimento HUD (2026-10-30)

- **Shared (idêntico nos 2 places, checksum):** `Types.EstadoHeroiResumo` + `golpes { [id]: nível }` e
  `pergaminhos { [id]: nível }` (o `HeroiSystem` já manda junto com `itens`). `Config`: `NumerosDanoMax 40`,
  `NumeroDanoDuracao 0.6`, `NumeroDanoSubida 4`, `NumeroDanoAltura 3`.
- **Barra do Roblox:** HUDs (`HudGui`, `ZonaHudGui`, `ItensGui`, `UltimateGui`, `ConquistaGui`, `ConfigBotaoGui`,
  `BuildGui`) com `IgnoreGuiInset = false` (altura da barra pela API; botão Settings em Y = 8). Telas de fundo cheio
  seguem com `IgnoreGuiInset = true` e o conteúdo de topo usa `Client/Util/Inset.manterAbaixo` (novo: empurra só o
  que faltar pra ficar em `GetGuiInset().Y + 8`) — título da escolha de herói, "LEVEL UP!" e painel Settings.
- **Painel da build:** `Controllers/BuildController` (novo) — `BuildGui` na esquerda abaixo do retrato: golpes
  (até `SlotsGolpe`, letra + cor do golpe + "Lv N", ordem do kit), pergaminhos (até `SlotsPergaminho`, roxo + "Lv N")
  e a grade de itens (**saiu do `ItemController`**, que agora só faz o toast). Tooltip ao passar o mouse/tocar
  (golpe: nome, forma, elemento; pergaminho/item: descrição). Reconstrói só quando a assinatura de
  golpes/pergaminhos/itens muda; esconde sem herói e no Play Again.
- **Números de dano:** remote unreliable `DanoNumeros` (s→c, handler vazio no servidor). `InimigoSystem`: todo
  `aplicarDanoBruto` registra o dano agregado por inimigo no frame; 1× por Heartbeat manda buffer
  `[f32 x, f32 z, u32 dano, u8 flags]` (máx. 40) pra quem está a ≤ `RaioDesenho`; flags = crítico (bit 0) + reação
  1..5 (bits 1–3). `danificar(..., semCarga, critico)`: `GolpeSystem.usoCritico` (sorteado no `danoDe`, guardado em
  projéteis/agendados). Cliente `Controllers/DanoController` (novo): pool de 40 BillboardGui
  (`workspace.AncoraNumerosDano`), sobe e some em 0,6 s, crítico amarelo maior, reação na cor do disco; ignora
  com `mostrarDano` off (`ConfigController.atual()`).
- Ledger: `.superpowers/sdd/2026-10-30-hud-build-dano/progress.md`. Não testados pelo Claude: tooltip, grade de
  itens, cor de crítico/reação, celular.

### Polimento 2 (2026-10-30)

- **Shared (idêntico nos 2 places, checksum):** `Config`: `DuracaoMensagem 2` (substitui `DuracaoMensagemHeroi`),
  `EscalaTelaReferencia 900`, `EscalaTelaMin 0.6`, `EscalaTelaMax 1.3`, `RaioOcultarMarcador 12`. `Types.MensagemHeroi`
  + `chave?`/`args?`. `Localizacao/PtBr`: `msg.semMoedas` ("Not enough coins ({1} needed)"), "HP is already full",
  "No free scroll slot".
- **Escala da HUD:** `Client/Util/EscalaHud` (novo) — uma UIScale "EscalaHud" por ScreenGui (`HudGui`, `ZonaHudGui`,
  `BuildGui`, `UltimateGui`, `ItensGui`, `ConquistaGui`, `MensagemGui`) com escala da tela × "HUD size"; reaplica em
  ViewportSize. `ConfigController` só faz `EscalaHud.definirConfig` + `aplicar` (a UIScale `EscalaConfig` saiu).
- **Marcadores:** `ZonaHudController` ganhou "$" dourado por baú (`workspace.BausAtivos`, ChildAdded/ChildRemoved) e
  "M" roxo pro mercador da zona (posição `mercador` no remote `Zona`, que também manda `ativa`). Pool de marcadores;
  escondidos fora da partida e a ≤ 12 studs.
- **Avisos de recusa:** `BauSystem` (sem moedas) e `MercadorSystem` (sem moedas / HP cheio / nível máximo / slot
  cheio; reenvia a oferta) mandam o motivo pelo `MensagemHeroi`. `Controllers/MensagemController` (novo): toast
  `MensagemGui` no centro-baixo, 2 s, label único, `formatar` pra texto com número. A escolha de herói usa ele.
- **DisplayOrder:** Loja 9, Fim/Escolha 20, Itens 21, Conquista 22, Mensagem 23, LevelUp 25, Config 30.
- Ledger: `.superpowers/sdd/2026-10-30-polimento-2/progress.md`. Não testados pelo Claude: recusa real no baú/loja,
  esconder perto, "HUD size" no painel, celular.

### Dificuldades (2026-10-30)

- **Shared (idêntico nos 2 places, checksum):** `Definicoes/Dificuldades` (novo): `Normal` (x1 em tudo, sempre livre),
  `Dificil`/"Hard" (spawn 1.4, vida 1.5, dano de contato 1.3, Essência 1.5, pontos de clã 1.5; `requer = "vitoriaNormal"`) e
  `Pesadelo`/"Nightmare" (1.8 / 2.2 / 1.6 / 2.5 / 2.5; `requer = "vitoriaDificil"`), com `desafio` (texto do cadeado) e `cor`.
  `Config.OrdemDificuldades`, `Config.DificuldadePadrao = "Normal"`. `Types`: `DadosTeleporte.dificuldade?`,
  `FimPartidaInfo.dificuldade?`, `PedidoHeroi { heroiId, dificuldade? }`. `Logica/Perfil`: `essenciaDaPartida(..., mult?)`,
  `registrarFim(..., multEssencia?)`, `dificuldadeLiberada(p, id)`. `PerfilSystem.registrarFim(..., multEssencia?)`.
  `PtBr`: Nightmare, "🔒 Hard", desafios, "This difficulty is locked.", "Difficulty", "Set by the match in progress",
  "YOUR RECORDS" (substitui "YOUR RECORDS · NORMAL"), chaves `dif.essencia` e `dif.rotulo`.
- **Desbloqueio sem mudar o schema:** `perfil.desbloqueios["dif:<id>"]`; `PartidaSystem.terminar` na vitória libera toda
  dificuldade cujo `requer == "vitoria" .. <dificuldade da partida>` (`PerfilSystem.desbloquear`).
- **Menu:** "Prepare match" com 3 botões (trancado = cinza, "🔒 Hard", "Unlock: win on Normal"; clicar avisa o desafio); a
  escolhida vai no `IrParaPartida({ heroiId, dificuldade })` (string sozinha ainda aceita). `MenuSystem` valida existe +
  liberada no perfil e põe no `TeleportData`.
- **Partida:** `EstadoPartida.dificuldade` (+ `defDificuldade()`), fixada no `iniciar(dificuldade)` por quem começa a partida
  (co-op: quem entra depois segue a atual; Play Again volta à escolha). Fonte: `TeleportData.dificuldade` ou o seletor da tela
  "Choose your hero" (`HeroiEscolhaController`, 3 botões abaixo dos cartões, pré-seleciona a do TeleportData; com partida em
  andamento mostra só a dela). `EscolherHeroi` aceita `{ heroiId, dificuldade }` ou string (= Normal); dificuldade inexistente
  é ignorada, trancada recusa com "This difficulty is locked." (só fora do Studio, como o herói). Efeitos: `ZonaSystem`
  multiplica vida/spawn dos comuns e a vida do guardião; `InimigoSystem.definirZona(..., multDanoContato)` multiplica o dano de
  contato (comuns e chefes); Essência × `multEssencia`; `ClaPontosSystem.fimDaPartida(..., mult)` × `multPontosCla`. HUD:
  " · Hard"/" · Nightmare" ao lado do nome da zona (Normal não mostra, remote `Zona` manda `dificuldade`); tela de fim mostra
  "Difficulty: X".
- **Ranking:** continua 1 placar por estatística (todas as dificuldades juntas) — OrderedDataStore só guarda número.
- Ledger: `.superpowers/sdd/2026-10-30-dificuldade/progress.md`. Testado em Play pelo Claude: Nightmare no HUD, mais inimigos
  (15 vs 7 em ~25 s), `TesteLogica` OK, botões do Menu. Não testado: desbloqueio real (vitória com DataStore), TeleportData
  publicado, recusa de dificuldade trancada fora do Studio, co-op entrando com partida em andamento.

### Mobs (2026-10-30)

- **Shared (idêntico nos 2 places, cópia via HTTP + diff):** `Definicoes/Inimigos` (agora também no Menu) com 12 comuns
  como dado — `comportamento`, `zonas` (`zonas[1]` = zona "de casa"; nas outras o peso × `Config.PesoZonaSecundaria`),
  `peso`, `forma`, `elemento?`, `projetil?`, `explosao?`, `invoca?`, `ignoraSeparacao?`, `indice` único (u8). Vila: Lantern
  Ghost (perseguir, em todas as zonas), Rascal Tanuki, Paper Umbrella Sprite (rápido), River Kappa (atirador, Agua);
  Bambuzal: Bamboo Scarecrow (tanque), Snow Monkey (rápido), Will-o'-Wisp (explosivo, Fogo); Templo: Stone Pup (tanque),
  Hollow Monk (invocador → Lanterna), Tengu Crow (voador rápido, ignora separação); Santuário: Oni Grunt, Shade (atirador,
  Sombra) + todos os anteriores com peso baixo. `Definicoes/Chefes`: `forma?`, `ehMini?` e 4 mini-chefes (Umbrella Lord,
  Monkey King, Crow Captain, Oni General; índices 105–108, ~40% da vida do guardião). `Definicoes/Zonas.miniChefe`.
  `Herois`: Kaizo `passiva.refletir = 0.1` (descrição nova). `Types.InfoProjetilInimigo`, `Types.InfoChefe` (+`mini`).
  `Config` bloco "Mobs" (pesos, zigue-zague, tanque, atirador, `ProjeteisInimigosMax 150`, refletido, explosão, elite,
  mini-chefe); `ChanceTanuki` saiu. `PtBr`: 14 nomes + "Free" + descrição do Kaizo.
- **`InimigoSystem`** (reescrito): sorteio por zona pré-calculado em `definirZona(..., zonaId)`; comportamentos em `passo`
  (rápido = desvio senoidal perpendicular; tanque = sem empurrão e Slowed pela metade; atirador/invocador mantêm distância
  e recuam; explosivo arma a `raio + ExplosaoGatilho`, para, aviso e some sem crédito/XP); projéteis inimigos em arrays
  paralelos (acerto por raio; refletido pelo `HeroiSystem.chanceRefletir` volta × `RefletirMult` no inimigo mais próximo,
  crédito pro Kaizo); explosões avisadas (remote `Aviso` só pra quem está a ≤ RaioDesenho, dano ignora a invuln curta);
  elite (`ChanceElite` depois de `EliteTempoMin` da zona, só na horda): HP ×4, dano ×1.5, modificador veloz/blindado/
  regenera/explosivo-ao-morrer. Pausa das cartas cancela projéteis/explosões no ar. `morreu` ganhou `elite` (7º) e
  `mini` (8º); mini-chefe passa `ehChefe = false` (não conta como guardião em tarefas/conquistas/clã).
  Snapshot: **bit 32 do byte de status = elite** (TAM_ENTRADA continua 15).
- **Servidor:** `ZonaSystem` (mini-chefe 1× por zona aos `MiniChefeTempo` perto de um jogador, vida escala como o
  guardião; ao morrer → `BauSystem.criarGratis(x, z)`); `BauSystem.criarGratis` (prompt "Open Chest", "Free", não sobe o
  preço); `XpSystem` (elite XP ×5 + moeda garantida ×5; mini-chefe `MoedasMiniChefe` 20); `ChefeSystem` (barra prioriza o
  guardião, manda `mini`). Remote novo `ProjetilInimigo` (s→c, handler vazio no servidor).
- **Cliente:** `Util/SpriteComposto.forma(p, forma)` (fantasma/bicho/humanoide/voador; orelhas e asas pré-montadas);
  `InimigoRenderController` (forma por def, elite ×`EliteEscala` com contorno dourado grosso); `EfeitosController` (pool
  `projetilInimigo`: bola vermelha, amarela quando refletida); `ZonaHudController` (barra do mini-chefe mais estreita e
  laranja). Explosão = disco do `AvisoController`.
- `TesteLogica`: índices únicos, formas/comportamentos válidos, dados por comportamento, ≥ 3 tipos por zona, mini-chefe por
  zona mais fraco que o guardião, Kaizo reflete.
- Ledger: `.superpowers/sdd/2026-10-30-mobs/progress.md`. Testado em Play pelo Claude (Config temporário, restaurado): 5 letras
  diferentes na Vila, projéteis inimigos, avisos de explosão, elites, barra do Umbrella Lord, `TesteLogica` OK, console sem
  erro. Não testado: baú grátis (prompt), refletir do Kaizo visível, Bambuzal/Templo/Santuário reais, co-op.
- **Revisão final Mobs (corrigida no lote Skins):** discos de explosão em sincronia (`limpar` quando há explosão
  pendente; guardião morto cancela explosões; mini-chefe morto apaga só os impactos dele via `ChefeSystem.limparImpactosDe`
  e reenvia os demais); `agendarExplosao` devolve boolean; carga da ultimate com redução do blindado; lacaios dos chefes
  com teto por jogador e tipos em `Chefes.lacaiosTipos`.
- **Nota Kaizo (inspiração ≠ cópia, 2026-10-30):** saiu "Rubber Pirate"/"Rubber Body" e o amarelo; agora
  `classe = "Sea Rogue — Tank"`, passiva **Kinetic Guard** ("+2 armor per level; 10% chance to bounce enemy projectiles
  back."), cor `(40, 140, 160)`. Mecânica igual (`tipo = "armadura"`, `refletir = 0.1`).

### Skins (2026-10-30)

- **Shared (idêntico nos 2 places, checksum):** `Definicoes/Skins` (novo): 3 por herói — padrão grátis (`ordem = 1`, cor
  do `HeroiDef`) + 2 por Essência (`Config.SkinCusto = { 300, 600 }`): Ryuga Training Gi / Crimson Gi / Moonlit Gi; Kaizo
  Deck Hand / Storm Coat / Golden Captain; Haruto Shadow Scarf / Snow Scarf / Thunder Scarf (`id`, `heroiId`, `name`,
  `ordem`, `cor` = corpo, `corDetalhe` = faixa, `custo`). `Types.Perfil` **v6** + `skins { [skinId]: true }` e
  `skinAtiva { [heroiId]: skinId }`; `Logica/Perfil`: `VERSAO = 6`, `novo`/`migrar` garantem as padrão possuídas e
  equipadas, `skinDoHeroi`, `comprarSkin`, `equiparSkin`. `Config.RateLimitSkin 0.5`. `PtBr`: nomes + textos da tela.
- **Menu:** `Systems/SkinSystem` — remotes `ComprarSkin(id)` (rate-limit, id existe, perfil carregado, recusa
  teleportando/`estaTravado`/`estaOcupado`/somente leitura, Essência suficiente, não possui; comprar já equipa e salva)
  e `EquiparSkin(id)` (mesmas checagens + possui; só `marcarMudanca`). `MenuController`: aba **Skins** da lista de heróis
  (era "Coming soon") → `TelaSkins` com 3 cartões do herói selecionado (prévia = retrato recolorido + faixa, nome,
  "Owned"/preço, botão "Equipped"/"Equip"/"Buy N Essence"); Esc volta pros heróis.
- **Partida:** `HeroiSystem.escolher` põe o atributo `Skin` no Player (`Perfil.skinDoHeroi`), reaplica no
  `PerfilSystem.carregou` e limpa no `resetarTodos`; `HeroiSpriteController` e o retrato do `HudController` usam
  `cor`/`corDetalhe` da skin (se for do herói), senão o `HeroiDef`; despertar tem prioridade na cor do sprite.
- `TesteLogica`: VERSAO 6, migração v5→v6, skins apontam pra herói existente, 1 padrão por herói com custo 0 e sempre
  possuída, comprar/equipar, lacaios dos chefes existem.
- Ledger: `.superpowers/sdd/2026-10-30-skins/progress.md`. **Publicar Menu e Partida juntos** (Partida v5 lendo perfil
  v6 não salva). Não testado: compra com Essência real, skin vinda do perfil publicado, clone do Haruto (continua na cor
  do herói).

### Áudio placeholder (2026-10-30)

- **Shared (idêntico nos 2 places, checksum):** `Definicoes/Sons` (novo) `{ chave = assetId }` — 16 efeitos (acerto, critico,
  moeda, xp, levelUp, carta, bau, item, reacao, ultPronta, ultUso, chefe, vitoria, derrota, clique, hover) + 5 músicas
  (`musicaMenu`, `musicaVila/Bambuzal/Templo/Santuario` = "musica" .. ZonaDef.id); ids públicos da Creator Store (nomes no
  ledger). `Config` bloco Juice: `SomMaxPorSegundo 8`, `SomPoolPorChave 8`, `SomVolumePadrao 0.4`, `SomVolumes`,
  `MusicaVolume 0.35`, `MusicaFade 1`.
- **SoundService (2 places, salvo):** SoundGroups `Musica` (0.7) e `Efeitos` (0.8) — o ConfigController/MenuController aplicam
  o volume das configurações.
- **Client/Util/Som (idêntico nos 2 places):** pool de até 8 Sounds por chave em `SoundService/SonsJuice`, PlaybackSpeed
  0.95–1.05, rate-limit por chave, id 0 ignorado; `Som.musica(chave)` em loop com fade de 1 s.
- **Partida:** `Controllers/AudioController` — EfeitoGolpe → acerto; DanoNumeros com crítico → critico; EstadoHeroi do próprio
  herói (xp/moedas subindo) → xp/moeda; OfertaCartas → levelUp; Item → item; baú sumindo a ≤ 15 studs → bau; Reacao → reacao;
  Ultimate (carga chega a 1 / cai) → ultPronta/ultUso; Chefe novo → chefe; FimPartida → vitoria/derrota; Zona → música da
  zona. `LevelUpController` toca "carta" ao enviar a escolha.
- **Menu:** `Controllers/AudioController` — `musicaMenu` + hover/clique nos botões (via `Util/Juice`).
- Ledger: `.superpowers/sdd/2026-10-30-juice/progress.md`.

### Juice (2026-10-30)

- **Client/Util/Juice (idêntico nos 2 places):** `botao` (hover 1.05 + brilho UIStroke + som; clique 0.95 → elástico + som),
  `autoBotoes(PlayerGui)` (helper único: todo GuiButton ganha `Juice = true`; `SemJuice = true` exclui), `pop`, `tremer`
  (câmera, teto `Config.TremorCameraMax 0.6`), `flash`, `confete` (pool `ConfeteMax 40`), `contador`, `moedaVoando` (pool
  `MoedasVoandoMax 10`). `JuiceGui` DisplayOrder 40. `Config`: `TremorCriticoIntervalo 0.4`, `ComboJanela 2`, `ComboMinimo 3`.
- **Partida:** `JuiceController` (novo: autoBotoes, moeda voando até "Coins", despertar = flash + anel no chão),
  `ComboController` (novo: `ComboGui` "x12 COMBO" com cor/tamanho subindo, "NEW RECORD!", recorde na tela de fim),
  `LevelUpController` (cartas entram uma a uma com pop, borda por raridade, lendária pulsa com atributo `Pulso`, escolhida
  cresce e some, "LEVEL UP!" com pop + flash), `ItemController` (pop do toast + confete), `ZonaHudController` (chefe novo:
  pop + tremor), `UltimateController` (cheia: pop + borda/botão pulsando), `DanoController` (crítico: pop maior + tremor),
  `FimController` (escurece; vitória confete + flash dourado + Essência subindo; derrota flash vermelho; "Best combo: x{1}").
- **PtBr:** "COMBO", "RECORD", "NEW RECORD!", `combo.recorde`.
- Testado em Play pelo Claude: combo x36, cartas animadas, música da zona e do menu tocando, 21 ids carregam, 120/120 botões do
  Menu com Juice, `TesteLogica` OK, console sem erro. Não testado: carta lendária, hover/clique com mouse real, tremor/flash
  visual, baú, despertar, vitória/derrota, chefe, ultimate cheia, celular.
- **Réplica Shared/Util (Menu ↔ Partida):** `Config`, `Localizacao/PtBr`, `Definicoes/Sons`, `Client/Util/Som`, `Client/Util/Juice`.

### Arte (2026-10-30)

- **Modelos 3D (estáticos, salvos no place Partida):** `ReplicatedStorage/Modelos/{Herois,Inimigos,Chefes}/<chave>` — 3 heróis,
  12 inimigos comuns, 8 chefes/mini-chefes, gerados com `generate_mesh` (1 MeshPart texturizado cada, chibi low-poly). Cada um é
  um `Model` com PrimaryPart `Corpo` (anchored, sem colisão), pivô no pé (0,0,0), **frente = -Z (LookVector, padrão do
  Roblox)**, altura normalizada: inimigos/chefes = `raio × 2` da definição, heróis = `Config.AlturaHeroiModelo` (5,5).
  Atributos: `Altura`, `GiroY` (graus, corrige a frente sem mexer no código), `Voo` (studs acima do chão: Lanterna, Fogueira,
  Corvo, Sombra, Tengu, TenguMenor), `AssetGerado`. Pastas `Efeitos` e `Skins` vazias (reservadas).
- **Trocar um modelo:** gerar/importar o novo, deixar um `Model` com PrimaryPart (qualquer BasePart), mesmo nome da chave da
  definição, pivô no pé e altura certa (ou rodar a normalização do ledger), e pôr na pasta. Se ficar de costas, `GiroY = 180`.
  Sem modelo para uma chave → o cliente desenha uma bola na cor da definição e avisa no Output.
- **Inimigos (`InimigoRenderController`, reescrito):** pool de MeshParts por índice (clonados do molde), um loop de
  RenderStepped que interpola e move todos com `workspace:BulkMoveTo`, virados pra direção do movimento, pulinho ao andar,
  voadores flutuam. Barra de vida + bolinha de status num BillboardGui pequeno, ligado só ferido/com status (a textura do
  MeshPart ignora `Color`, então status não é tint). Elite = `Config.EliteEscala` + Highlight dourado; chefe = contorno dourado.
  Morte = encolhe 0,15 s + 4 partículas na cor. Custo medido no atributo `CustoMs` de `workspace.InimigosVisual`.
  Snapshot/protocolo iguais.
- **Heróis (`HeroiSpriteController`, reescrito):** clone do `Corpo` soldado (Weld) ao HumanoidRootPart (gira com o Humanoid,
  custo zero por frame). Skin paga = Highlight tingindo na cor da skin (contorno = `corDetalhe`), porque `generate_texture`
  falhou ("User is not authorized to access Asset"); se um dia existir `Modelos/Skins/<skinId>` com textura própria, ele é usado
  no lugar. Despertar = Highlight na cor + aura (`ParticleEmitter`); caído = translúcido 0,6. Expõe `molde()` e `parteDe()`.
  **Clones** (`CloneRenderController`) = mesmo modelo, transparência 0,5, pool de 2.
- **Utils novos (Partida):** `Client/Util/Particulas` (emissores pooled por tipo morte/impacto/reacao/faisca, só `Emit`, teto
  `Config.EfeitosParticulasMax` por segundo) e `Client/Util/Destaques` (pool de Highlights com teto `Config.HighlightsMax` 20,
  na pasta `workspace.Destaques`).
- **Efeitos (`EfeitosController`):** projétil com `Trail` + faíscas ao acertar; cone com faíscas; área com anel de choque
  expandindo + faíscas; linha com `Beam` + faíscas; cadeia com `Beam` curvo entre os pontos (teto 30); ultimate com 25 faíscas +
  contorno piscando 0,6 s no herói mais perto da origem; reação com partículas na cor.
- **Shared (idêntico nos 2 places, checksum):** `Config` + `AlturaHeroiModelo`, `HighlightsMax`, `EfeitosParticulasMax`,
  `ParticulasMorte`.
- **Menu:** `ReplicatedStorage/Modelos/Herois` (3 heróis recriados com `CreateMeshPartAsync`, mesmos MeshId/TextureID) +
  `Client/Util/RetratoModelo` (ViewportFrame estático, sem loop) na ficha do herói e no "Prepare match" (a letra some quando há
  modelo; herói trancado = silhueta escura). Cartões da lista continuam com o retrato de cor (prévias de skin viraram 3D na
  revisão geral, abaixo).
- **Ficou sprite/2D:** nada no jogo; `Util/SpriteComposto` ficou sem uso (pode apagar depois).
- Medido em Play (120 inimigos visíveis, Config temporário restaurado): loop de render 0,13–0,18 ms/frame, dt médio 8,3 ms,
  física 60. `TesteLogica` OK, console sem erro. Ledger: `.superpowers/sdd/2026-10-30-arte/progress.md` (+ montagens dos
  modelos). Não testado/visto: aparência no jogo (captura 3D do Studio sai preta), frente dos modelos, Beams da linha/cadeia,
  elite/chefe com Highlight, ultimate, Menu em Play.

### Mapa (2026-10-30)

- **Cenário estático das 4 zonas** em `Workspace/Mapa/Zonas/<zona>/Decoracao` (a provisória foi apagada), só primitivas
  (sem modelo gerado nem asset). `Chao` ganhou Material/Color por zona; posição/tamanho de Chao, Spawn, Altar, Portal, Baus,
  Mercador e paredes intactos. Caminhos finos sem colisão (y 0,1) Spawn→Portal→Altar + Spawn→Mercador.
- **Vila "Cherry Village"** (387 inst.): cerejeiras na borda e em 3 ilhas, 5 casas, cerca N/S, lanternas de pedra, riacho
  translúcido + ponte vermelha, pétalas (3 ParticleEmitters). **Bambuzal "Bamboo Grove"** (377): bambus densos na borda e em
  4 bosques, pedras musgosas, lanternas de papel. **Templo "Temple Ruins"** (282): torii vermelho na entrada, escadarias de 3
  degraus nas bordas N/S, pilares quebrados/caídos, 4 komainu, lajes, tochas com Fire. **Santuário "Eclipse Shrine"** (172):
  chão escuro, círculo ritual Neon roxo ao redor do Altar, torii preto atrás do Spawn, 8 pilares com fogo roxo, rochas e
  cristais, eclipse no céu (esfera + corona + Highlight, sem colisão). Total 1218.
- **Regras de colisão:** só tronco/caule/casa/rocha grande/pilar/degrau/pedestal/torii colidem; o resto é `CanCollide`,
  `CanQuery` e `CanTouch` false. Nada com colisão a < 20 studs de Altar/Portal/Mercador/Baús (12 do Spawn) nem a < 6 do eixo
  dos caminhos Spawn→Altar→Portal→Mercador→Baús. Altura máx. 27 (bambu). Testado em Play: 0 colisores num raio de 10 em
  todos os pontos-chave das 4 zonas, herói sem prender na Vila. Ledger: `.superpowers/sdd/2026-10-30-mapa/progress.md`.
- **Não visto:** aparência (sem captura); eclipse pode sumir na Atmosphere densa do Santuário.

### Correções da revisão geral (2026-10-30)

- **Partida (cliente):** `ComboController` conta `#lista // 3` (payload `[id, x, z, ...]`). `Util/Destaques`: `pegarComum`
  (elite/chefe/clone) para em `HighlightsMax - 4` (`RESERVA_HEROI` local); `esperarVaga(cb)` = fila atendida a cada vaga solta;
  `ativos()`. `HeroiSpriteController`: herói sem vaga entra na fila; caído = Corpo 0,6 + `FillTransparency` 0,9.
  `InimigoRenderController`: barra só em elite/chefe/mini-chefe ferido ou inimigo com status, `MaxDistance = RaioDesenho`;
  morte encolhe no próprio `RenderStepped` (sem Tween). `Util/Particulas`: emissor por cor (chave RGB, 12 por tipo, LRU; não
  repinta partícula viva), exporta `sequencia(cor)`. `EfeitosController`: ColorSequence em cache, registro `Voo` do herói
  reaproveitado por Part, `FimPartida`/`PartidaReiniciada` limpam também os projéteis do herói. `CloneRenderController`: tinta
  da skin (Highlight via `pegarComum`) e clone pendente até o `HeroiId` do dono chegar.
- **Partida (servidor):** `CloneSystem` reenvia os clones ativos no `PlayerAdded` e no 1º `CharacterAdded` de quem entra.
- **Menu + Partida (idênticos, hash conferido):** `Util/Som` pré-carrega todos os sons (Sounds temporários + `PreloadAsync`,
  em `task.spawn` no 1º require); `Util/Juice.botao` cancela os tweens e volta a escala 1 ao esconder (`Visible`) ou mudar de
  pai (`AncestryChanged`).
- **Menu:** prévia da skin = `RetratoModelo` 3D (`mostrar(quadro, heroiId, apagado?, skinId?, tinta?)`) tingido pelo
  `ImageColor3` do ViewportFrame (Highlight não desenha em ViewportFrame); `Modelos/Skins/<id>` usa o modelo próprio sem tinta.
- **Arte/IP:** Haruto regenerado (asset 73645924786640: faixa de pano com lua crescente, sem placa de metal) e trocado em
  `ReplicatedStorage/Modelos/Herois/Haruto` nos 2 places (mesmo PrimaryPart/pivô/atributos). Kaizo conferido: sem chapéu de
  palha nem cicatriz, mantido.
- Testado pelo Claude: combo x56 ≤ KOs 57, Highlights ≤ 2/20, 0 BillboardGuis ativos com 11 inimigos, reserva 16+4 e fila,
  `TesteLogica` OK, Menu com 3 prévias 3D; console limpo. Ledger: `.superpowers/sdd/2026-10-30-revisao-geral/progress.md`.
  **Salvar e publicar Menu e Partida juntos.**

### Mapa ninja (2026-10-30)

- **Zonas novas (só Partida):** mesmos ids, tema ninja original. `Vila` "Shinobi Village", `Bambuzal` "Forest of Trials",
  `Templo` "Fallen Fortress", `Santuario` "Sealed Shrine". Centros no X **0 / 4000 / 8000 / 12000** (Z = 0), 600×600
  (Santuário 320×320). `Definicoes/Zonas` ganhou `centroX`/`meiaLargura`; PtBr ganhou as 4 traduções.
- **Chão = Terrain** com relevo (−6..+8; platôs/crateras com rampa ≤ ~34°, riacho raso na Vila e na Floresta, pontos-chave
  achatados) e montanha/paredão (+42±16) em volta, fora das paredes invisíveis (±meia+1, 160 de altura). `Chao` de cada zona
  ficou invisível, sem colisão/query, em Y −40 (o `ZonaSystem` ainda lê Position/Size.X dele). Spawn/Altar/Portal/Mercador/
  Baús movidos (layout antigo ×2) e assentados no terreno; `Mapa/SpawnJogador` e `Config.PosicaoInicial` (−240, 2, 0) no
  Spawn da Vila.
- **`ReplicatedStorage/Shared/Mapa/Alturas`** (gerado por raycast no Terrain, passo 6, décimos de stud; **gerar de novo se o
  terreno mudar**): `em(zonaId, x, z)` bilinear sem alocar, `zonaEm(x)`, `y(x, z)`. Usam: `ZonaSystem` (portal ativo),
  `BauSystem.criarGratis`; cliente `InimigoRenderController`, `EfeitosController` (voos, orbes, efeitos de golpe/reação),
  `AvisoController`, `JuiceController`, `DanoController`, `CloneRenderController`. O servidor continua 2D (inimigos/projéteis/
  orbes só x/z). `HeroiSystem.teleportar` pede `RequestStreamAroundAsync` do destino (sem bloquear).
- **Cenário** (`Zonas/<zona>/Decoracao`, 1523 inst. no `Mapa`): 6 meshes gerados (árvore, casa, torre de vigia, estátua de
  guerreiro genérico, sapo de pedra, torii preto liso) clonados, sempre sem colisão + `Colisor` invisível (tronco/caixa/pilares).
  Vila: paliçada, casas, torres, campo de treino, lanternas, riacho + ponte. Floresta: árvores gigantes, troncos caídos,
  cogumelos, cabanas, sapos, vaga-lumes. Fortaleza: muralha em ruínas, muros partidos, estátuas, catapultas, fogo nas
  crateras, tochas, cinzas. Santuário: círculo do selo Neon, pilares com correntes até o Altar, torii pretos, fogo roxo,
  cristais, eclipse. Mesmas regras de colisão do mapa anterior; auditoria 0 violações.
- **Clima** (`ZonaVisualController`): Vila tarde dourada, Floresta verde enevoada, Fortaleza âmbar/cinza, Santuário igual.
- **Ritmo:** `DuracaoZona` 420 (7 min), `MiniChefeTempo` 210, `EliteTempoMin` 90.
- Testado pelo Claude em Play: 0 colisores num raio de 10 nos 40 pontos-chave, HRP estável sobre o terreno nas 4 zonas,
  inimigos com base entre 0 e 0,9 acima de `Alturas`, da Vila 0 Parts de outra zona a < 3000; console limpo.
  Ledger: `.superpowers/sdd/2026-10-30-mapa-ninja/progress.md`. **Salvar e publicar o Partida.**
- **Pendências:** `StreamingMinRadius`/`StreamOutBehavior`/`StreamingIntegrityMode` não são acessíveis pelo MCP → Diego ajustar
  à mão no Workspace (MinRadius 256; opcional Opportunistic e PauseOutsideLoadedArea). Textos antigos "Cherry Village"/
  "Eclipse Shrine"/"Shattered Cherry Valley" seguem em `Herois.desafio`, `Conquistas`, `Tarefas`, `Config.NomeRegiao/
  DescricaoRegiao` (compartilhados com o Menu; não mexidos). → **resolvido no lote Inimigos ninja.**
- **Não visto:** aparência (meshes gerados, terreno, água/ponte, eclipse, partículas), troca de zona pelo portal real com o
  streaming padrão, FPS.
- **Adendo 2 (1,5× + terraços, 2026-10-30):** zonas **900×900** (Santuário 480×480), centros iguais; `Chao`, paredes
  invisíveis (±meia+1), `Definicoes/Zonas.meiaLargura` 450/450/450/240 (idêntico no Menu), `Config.PosicaoInicial`
  (−360, 10, 0). Terreno refeito em **platôs em degraus**: 4 níveis (−6,5/0/6,5/13; Fortaleza −7/0/7/14), Santuário 2
  (0/6,5), paredões com face de rocha (Sandstone na Vila, Rock na Floresta, Basalt na Fortaleza e no Santuário; topo
  Grass/LeafyGrass/Ground/Slate), rampas largas (18–25 por zona, ≤ 33°) ligando todos os platôs, corredores dos caminhos
  suavizados (≤ 29°), ravina com riacho raso (Part translúcida, fundo −10, barranco ~29°) + 2–3 pontes de madeira **com
  colisão** onde os caminhos cruzam (Vila/Floresta/Fortaleza), 2–3 lagoas rasas por zona, montanha de borda +54±16 fora das
  paredes. Pontos-chave no layout antigo ×1,5, cada um num platô. `Shared/Mapa/Alturas` regerado (151×151, Santuário 81×81)
  e com **dados codificados em base 64 (2 caracteres por amostra)** — o CSV passava do limite de 200k do `Source`; API igual.
  Decoração reposicionada (×1,5, assentada no platô plano mais próximo) + grupos novos (árvores dos meshes, pedras, tocos,
  cogumelos, flores, arbustos, grama alta, troncos, cristais); paliçada/muralha/círculo do selo/pilares refeitos no tamanho
  novo. `Workspace/Mapa` = **2394** instâncias, 30 luzes, 12 emissores. Auditoria: 0 colisores a 10 dos pontos-chave, 0
  bloqueios nos raios da rota, flood-fill (passo 6, 35°) 100 % nas 4 zonas. Play: HRP estável nas 4 zonas, inimigos no chão,
  herói andou pela ponte da Vila. Ledger: seção "Adendo 2" do `progress.md`. **Salvar e publicar Partida e Menu.**

### Inimigos ninja (2026-10-30)

- **Bestiário novo (substitui os 12 comuns e 8 chefes antigos; modelos antigos apagados).** Ids em português, `name` em
  inglês, tudo dado em `Definicoes/Inimigos`/`Chefes` (Shared, idêntico nos 2 places).
  - Vila (Shinobi Village): Rogue Genin `GeninRenegado` (perseguir; também na Floresta/Fortaleza), Kunai Thrower
    `LancadorKunai` (atirador), Shield Bruiser `BrutamonteEscudo` (tanque), Smoke Runner `CorredorFumaca` (rápido), Paper
    Bomb Carrier `PortadorBomba` (explosivo).
  - Floresta (Forest of Trials): Leaf Hopper `SaltadorFolha` (rápido; também na Fortaleza), Vine Puppeteer `TitereiroVinhas`
    (**marionete** → Leaf Hoppers), Poison Moth `MariposaVeneno` (atirador voador), Bark Golem `GolemCasca` (tanque), Mirror
    Clone `CloneEspelho` (**clone** → 2× Mirror Copy `CopiaEspelho`, `soInvocado`, 25% do XP).
  - Fortaleza (Fallen Fortress): Armored Ashigaru `AshigaruBlindado` (tanque), Crossbow Sentinel `SentinelaBesta` (atirador),
    Shadow Stalker `EspreitadorSombra` (**teleporte**; também no Santuário), Siege Bomber `BombardeiroCerco` (explosivo),
    Warlord's Herald `ArautoSenhor` (invocador → Rogue Genin).
  - Santuário (Sealed Shrine): Sealed Wraith `EspectroSelado` (perseguir, fantasma), Masked Assassin `AssassinoMascarado`
    (teleporte), Cursed Monk `MongeAmaldicoado` (atirador), Chain Guardian `GuardiaoCorrente` (tanque), Seal Fragment
    `FragmentoSelo` (explosivo).
  - Números = tipo equivalente antigo (mesmo comportamento) × fator da zona (HP/dano/xp 1 / 1,6 / 2,5 / 3,5); `Zonas.multHp`
    continua por cima. **Balanceamento: Diego.**
- **Comportamentos novos (3):** `teleporte` (`InimigoDef.teleporte` {intervalo, distanciaMin}: reaparece 6–10 studs atrás do
  herói, preso na zona), `clone` (`InimigoDef.clone` {tipo, quantidade}: no 1º dano solta as cópias, dentro do teto de vivos),
  `marionete` (usa `invoca`; fica longe e as invocadas surgem num anel de `Config.MarioneteRaio` em volta do herói). Campo
  `soInvocado` (peso 0, fora do sorteio). Snapshot (15 bytes) e pool de render sem mudança.
- **Guardiões** (`ChefeDef.padroes`, único campo novo; rodízio a cada `golpeIntervalo`, aviso vermelho no chão
  `Config.ChefePadraoAviso` 0,8 s antes): Great Toad Elder `SapoAnciao` (Vila: língua em linha + pulo), White Serpent
  `SerpenteBranca` (Floresta: investida + poças de veneno + área), Nine-Tailed Fox `RaposaNoveCaudas` (Fortaleza: leque de 9
  projéteis + chuva de fogo + pulo), Giant Slug `LesmaGigante` (Santuário: lama em chuva que cura 4% + área). **Chefe final**
  Sealed Demon `DemonioSelado`: surge no lugar da Giant Slug quando ela cai (`Zonas.chefeFinal`, cura o grupo); fase 1 área +
  leque; fase 2 (≤ 66%) invoca Seal Fragments e fica mais rápido; fase 3 (≤ 33%) chuva de fogo roxo, mais rápido ainda
  (`Config.ChefeFaseLimites`/`ChefeFaseVelMult`). Só a morte dele abre o portal dourado. Mini-chefes = comuns grandes (mesmo
  mesh): Rogue Captain, Elder Bark Golem, Ashigaru Commander, Chain Warden.
- **Sistemas (Partida):** `ChefeSystem` (formas círculo/linha/leque, pulo/investida movem o chefe, fases), `InimigoSystem`
  (comportamentos novos + `prenderNaZona`, `moverPara`, `curar`, `definirMultVel`, `dispararProjetilLivre`), `ZonaSystem`
  (chefe final), `AvisoController` (aviso em faixa: `linha = true`). Menu: `MenuController` mostra o chefe final no card do
  Santuário (Prepare match).
- **Modelos:** 25 meshes gerados (`ReplicatedStorage/Modelos/Inimigos` 21, `Chefes` 9; assetIds no ledger), pivô no pé,
  altura = raio × 2, `GiroY` 0, `Voo` na mariposa/espectro/fragmento.
- **Correções da revisão do Mapa ninja (Task 0):** `HeroiSystem.teleportar` espera o streaming (pcall, 5 s) antes de mover em
  teleporte longo (thread por jogador; `posicao()` devolve o destino enquanto espera; golpe com teleporte continua
  instantâneo); renascer já ia pro `ZonaSystem.spawnAtual()` (via `ZonaSystem.acompanhar`) e agora com streaming;
  `InimigoRenderController`/`EfeitosController` usam `Alturas.em(zona do remote Zona)`; `CloneSystem` prende o clone na zona;
  textos: região **"Shinobi Lands"**, "Unlock: clear Shinobi Village", "Clear Shinobi Village (zone 1)…", "Clear the Sealed
  Shrine." (2 places, PtBr junto). `Config`/`Zonas`/PtBr do Menu, que o Mapa ninja tinha deixado pra trás, ficaram iguais aos
  do Partida (21 módulos do Shared conferidos por hash).
- `TesteLogica` cobre comportamentos/padrões/fases/ids/pesos. Testado em Play pelo Claude (gancho de teste temporário,
  removido): `TesteLogica: OK`, as 4 zonas (inimigos no chão, teleporte/clone/marionete/invocador rodando), os 4 guardiões e
  as 3 fases do chefe final com avisos, portal dourado no fim; console sem erro novo.
  Ledger: `.superpowers/sdd/2026-10-30-inimigos-ninja/progress.md`. **Salvar e publicar os 2 places.**
- **Pendências:** Marionete invoca muito (13 titereiros → ~66 invocações/min); lentidão da lama da lesma não existe (sem
  status no herói); teleporte sem efeito de "puff" (o render só desliza rápido); faixa de aviso é reta (no relevo forte pode
  ficar meio enterrada/flutuando). Nome "Paper Bomb Carrier" e "Rogue Genin" vêm do plano — o Diego decide se ficam (o
  modelo do Paper Bomb Carrier é um pote de fogos, sem selos de papel).
- **Não visto:** aparência e frente dos 25 modelos, leitura dos avisos em jogo, portal real/altar por prompt, co-op.

### Pool de itens e pergaminhos (2026-10-30)

- **Shared (idêntico nos 2 places, hash 28/28):** `Definicoes/Itens` com **83 itens** (comum 28 · incomum 22 · raro 16 ·
  épico 9 · lendário 8; `max` padrão 10/6/4/2/1 em `Config.ItemMaxPorRaridade`, sobrescrevível) e `Definicoes/Pergaminhos`
  com **24** (novos: Barrier/Escudo, Gale/VelProjetil, Mist/Evasao, Hex/ChanceStatus, Gold/Moedas, Fate/Sorte,
  Leech/RouboVida, Thorn/Espinhos, Overflow/Sobrecura, Challenge/Elites, Focus/CargaUltimate). `letra` placeholder +
  `icone?` (assetId; vazio = letra) nos dois. Nomes nossos, números portados do Megabonk §6–7 / PokeBonk §9–10 —
  **o Diego troca nome/ícone e balanceia**. Itens/Pergaminhos/Cartas/Dano/Progressao/Afeta/Exibicao passaram a existir
  também no Shared do Menu (sem uso lá).
- **Tipos de efeito** (`Itens.Efeito`, resolvidos por tipo em `ItemSystem`/`InimigoSystem`/`HeroiSystem`/`GolpeSystem`):
  `stat`, `escudo`, `aoAcertar` (status), `aoAcertarDano` (explosão, raio em cadeia, bonk ×20, executar), `aoMatar`
  (cura, moeda, míssil teleguiado, XP, +HP máx. com teto), `aoApanhar` (espinhos, veneno = dano + Burning em área, moeda,
  velocidade 3 s, invulnerável), `condicional` (HP baixo), `statCondicional` (perto/longe/vida alta/elite-chefe/parado/
  por abate/por baú), `economia` (chave de baú, sorte por baú, preço da loja), `meta` (+1 carta na oferta, rolagem
  extra, megacrit ×4, teto de golpe 10, teto de pergaminho 12, sobrecura 75 %, evitar 1 morte, +dificuldade),
  `reviver`, `critMult`, `reacaoDano`. Listas pré-montadas por jogador no `ItemSystem.recalcular` (sem alocação por acerto).
- **Stats novos do herói** (`HeroiSystem.recalcularStats` → `e.derivados`): evasão (com a do Haruto, teto 60 %),
  escudo (recarrega 25 %/s após 5 s sem dano), roubo de vida, espinhos (dano no inimigo do contato), sobrecura (cura
  além do máx. vira HP extra até 75 %, decai 2 %/s), chance de status (× chances ao acertar), duração (× status),
  velocidade de projétil, sorte, elites (+chance de elite e +XP), carga da ultimate. Resumo manda `escudo`/`sobrecura`
  (a HUD ainda não desenha).
- **Sorte:** `Cartas.pesosComSorte` (peso × (1 + sorte × `Config.SortePorRaridade`)) na raridade das cartas, dos itens
  de baú e da loja — nunca no conteúdo. Testado no `TesteLogica` (10 k sorteios, 2 %).
- **"Affects":** `Logica/Afeta` (puro) diz se um efeito/pergaminho muda cada golpe equipado; o servidor manda `afeta` +
  `equipados` na carta (`LevelUpSystem`), na loja (`MercadorSystem`, recalculado a cada envio) e no toast do item
  (`ItemSystem.dar`, calculado ao aplicar). Cliente: `Client/Util/CartaUI` (novo) desenha a carta parecida com a do
  PokeBonk (cabeçalho na cor da raridade, chips, ícone, números antes → depois em verde, chips por golpe ✓/✗ com nome
  ao passar o mouse); usada pelo `LevelUpController` e pelo `LojaController`. `ItemController` mostra "Affects: …" no toast.
- **Loja:** +2 itens sorteados (preço por raridade em `Config.PrecoLojaItem` × zona × desconto). **Baú:** custo por
  jogador, Skeleton Key, contagem pra itens "por baú".
- Ledger: `.superpowers/sdd/2026-10-30-itens-pool/progress.md`. Testado em Play pelo Claude (gancho temporário,
  removido): `TesteLogica: OK`, 3 level-ups com raridade/números/Affects, loja (comprou 2 itens), baú pelo prompt,
  escudo, explosão, +HP por abate, velocidade ao apanhar, 4 cartas, morte evitada, Affects recalculado ao trocar golpe.
- **Pendências:** nomes/ícones/balanceamento dos 83 itens (Diego); textos novos não estão na `Localizacao/PtBr`
  (ficam em inglês no pt-BR); míssil usa o visual do Ki Blast e escala com o nível dele; HUD não mostra escudo/sobrecura;
  layout final da carta vem no lote da HUD (o texto pode ficar pequeno no celular).
- **Não visto:** espinhos/veneno no contato, sobrecura acumulando, bonk/executar/raio em cadeia, Skeleton Key, megacrit,
  carta lendária/5 raridades na tela, celular.
- **Lembrete: salvar e publicar os 2 places juntos** (Shared mudou nos dois).

### QA no Studio

- `Server/Systems/QaSystem` (Partida) cria a RemoteFunction `ReplicatedStorage.Remotes.Qa` **só no Studio**
  (`RunService:IsStudio()`); fora do Studio o remote nem existe e o handler confere de novo. Uso no datamodel Client:
  `game.ReplicatedStorage.Remotes.Qa:InvokeServer("moedas 500")` → devolve um texto ("ok …" / "erro: …").
- Comandos (validados por tabela: inteiros ≥ 1, ids `[%w_]` ≤ 40): `moedas n`, `xp n`, `item id`, `pergaminho id`,
  `golpe id [nivel]`, `soGolpe id` (fica só com esse golpe), `nivel n`, `zona n` (mesma rota do portal), `guardiao`,
  `avancar` (fecha a zona como se o guardião caísse: cura, oferta extra, portal), `objeto id` (usa o objeto `id` mais
  próximo como se o prompt tivesse sido acionado, pagando, sem checar distância; `ChakraStoneDourada` força a pedra
  dourada), `objetos` (lista os objetos da zona com distância), `evento id` (força um evento do diretor: Swarm, Stampede,
  Flock, Rockfall, Dominant, Summoner, Fog, Storm, Eclipse, Thief, Siege), `matarChefe` (mata guardião/mini com drops e
  mostra o hpMax), `invulneravel 0|1`, `matarTodos` (comuns; chefes ficam), `spawn n` (até o teto de vivos),
  `desbloquear heroiId` (tabela de QA no `PerfilSystem`, nunca no perfil), `confiar 0|1` (perfil em memória vale pro pool
  de golpes), `cartas n` (sorteia n ofertas e conta por herói dono), `estado` (inclui moedas, itens, modificadores da run,
  batidas do tambor e `bonusRun`).
- Ganchos usados: `HeroiSystem.qaInvulneraveis`, `InimigoSystem.qaMatarComuns/qaSpawnar/qaMatarChefes`, `ZonaSystem.qaIrPara/
  qaGuardiao/qaAvancar/zonaIdAtual`, `PerfilSystem.qaConfiar/qaDesbloquear`, `GolpeSystem.contarProjeteis`,
  `ObjetoSystem.qaUsar/qaListar`, `DiretorSystem.qaEvento`.

### Golpes: pool por desbloqueio e efeitos (2026-10-30)

- **Shared (idêntico nos 2 places, 29/29 por `Source`):** `Definicoes/Golpes` com **18 golpes** (6 por herói, `heroi`,
  `inicial`, bloco `visual` com `estilo`/`cor`/`cor2`/`tamanho`/`rastro`/`particulas`/`luz`/`som`/`impacto`);
  `Definicoes/GolpesInternos` (novo: `ItemMissil` do Spirit Wisp); `Herois.kit` com 6; `Logica/Cartas` (pool por
  desbloqueio); `Config` (`PesoGolpeEmprestado 0.6`, `GolpesProprioAte 2`, `EfeitosPartsMax 220`, `LuzesEfeitoMax 8`,
  `SilhuetasMax 8`, `FlashAcertoDuracao 0.12`, `TremorUltimate 0.35`); `PtBr` (+8).
- **Golpes e estilos** (nv mín.):
  - Ryuga (Ki): Ki Blast `esfera` (1) · Punch Barrage `braco` (2) · Flash Step `silhuetas` (4) · **Ki Orbit** `orbita`
    (5, área que segue o herói, 3 orbes, 10 ticks) · Ki Cannon `feixe` (7) · **Rising Pillar** `pilar` (9).
  - Kaizo (Impacto): Slingshot Punch `braco` (1) · Gatling Fists `braco` (2) · Leg Whip `onda` (4) · **Coil Lash**
    `braco` (5, linha com 2 chicotadas) · Spring Bullet `cadeia` (7) · **Anchor Drop** `chuva` (9).
  - Haruto (Vento): Kunai Rain `lamina` (1) · Wind Shuriken `lamina` (2) · Explosive Tag `onda` (4) · **Shadow Step
    Slash** `lamina` (5, cone que teleporta atrás do alvo) · Wind Blade `lamina` (7) · **Mirror Volley** `silhuetas` (9).
  - "Rubber Lash" do plano virou **Coil Lash** (nome lembrava obra existente).
- **Pool de level-up:** kit do herói + golpes **não-iniciais** dos heróis desbloqueados no perfil (peso 0,6), sorteio
  ponderado sem reposição; até ter 2 golpes, toda oferta traz ≥ 1 golpe do próprio herói. Perfil só em memória
  (DataStore falhou / Studio) = só o kit do herói (`PerfilSystem.desbloqueiosConfiaveis`). Carta emprestada mostra o
  nome do herói dono nas tags. Mecânicas novas só com dado nas formas existentes (`segue`/`orbita` em `area`,
  `teleportaAtras` em `cone`); nenhuma forma nova.
- **Efeitos (cliente):** `EfeitosController` reescrito com os 10 estilos (pools por tipo, tetos do `Config`, braço e
  silhuetas na tinta da skin/despertar via `HeroiSpriteController.tintaDe`, ultimate com tremor leve só pra quem usou,
  limpeza no fim/Play Again, atributos `Ativas/PicoAtivas/Luzes/Silhuetas` em `workspace.Efeitos`). Flash de acerto no
  inimigo (`InimigoRenderController.piscar`: pulo de tamanho + cor) a partir do `DanoNumeros`, que agora tem 17 bytes
  (+id do inimigo, bits 4..5 = elemento); números com cor por elemento e crítico maior.
- **Menu:** ficha do herói com os 6 golpes (2×3) e "Unlock this hero to add their attacks to every run" no trancado.
- **Correções da revisão dos itens (Task 0):** míssil do Spirit Wisp com dano fixo 15 e quantidade fixa (M1); execute
  ignora a blindagem do elite (M2); prompt do baú mostra o preço real por jogador ("N–M coins" no co-op) (M3); cache de
  elites/dificuldade recalculado quando alguém sai (M4); roubo de vida só em golpe (M5); TesteLogica cobre sorte
  negativa/nula (M7).
- Testado em Play pelo Claude: `TesteLogica: OK`; os 18 golpes disparando 5 s cada (pico 54 Parts de efeito, ≤ 2 luzes,
  ≤ 4 silhuetas, volta a 0); pool só do Ryuga sem perfil confiável e com os 3 liberados (10 emprestados, nenhum
  inicial); 100–125 inimigos + até 31 projéteis a 120 fps médios; comandos de QA. Console sem erro novo.
  Ledger: `.superpowers/sdd/2026-10-30-golpes-pool-efeitos/progress.md`.
- **Pendências:** balanceamento dos golpes novos; ultimates sem `visual` próprio (estilo padrão da forma); cartão da
  escolha de herói da Partida lista 6 nomes num texto só; `Config.SlotsGolpe` continua 3.
- **Não visto:** aparência dos efeitos (captura do Studio sai preta), flash no inimigo texturizado, tremor da ultimate,
  silhueta com skin/despertar, ficha do Menu em Play, tag de herói na carta, pool com perfil real (DataStore), celular.
- **Lembrete: salvar e publicar os 2 places juntos** (Shared mudou nos dois; `DanoNumeros` mudou de formato).

### Objetos e eventos de mapa (2026-10-30)

- **Shared (idêntico nos 2 places, 30/30 por hash + `ConfigSystem`):** `Definicoes/Objetos` (novo) com **16 objetos** em
  **14 tipos de regra** (`icone` letra placeholder + `categoria` pro mapa com descoberta), `Config` (bloco "Objetos
  interativos e eventos de partida" + 5 em `OrdemConquistas`), `Types` (payloads `ObjetoUsadoInfo`/`EscolhaObjetoInfo`/
  `EventoInfo`/`CarteiraInfo`, campos opcionais da partida, `ConfigJogador.rotulosMundo?`), `Conquistas` (tipos `naPartida`
  e `vitoriaPoucosItens`), `Logica/Perfil` (`rotulosMundo` opcional, **perfil continua v6**), `PtBr` (+63).
- **Objetos** (Vila / Floresta / Fortaleza / Santuário; teto `Config.ObjetosMaxPorZona` 30): Chakra Stone 4/4/4/2 (carrega
  por presença; comum/raro/épico/dourado 8/14/22/35 s, % no rótulo, épica/dourada com feixe e ondas, dourada selada até
  1:30 e dá 4 cartas pra escolher 2), Greed Shrine 1/1/1/0 (+20 % dificuldade, +25 % XP e moedas), Cursed Altar 1/1/1/1
  (+15 % inimigos, +10 % dificuldade → item raro), Challenge Totem 2/2/2/1 (anel 8 + 3 × zona com 2 elites, 90 s → baú roxo
  com item ≥ raro), Sealed Ruins 1/1/1/0 (−15/−20/−25 % HP máx.: item épico / +3 níveis num pergaminho / Spirit Wisp),
  War Drum 1/1/1/0 (até 3 batidas: guardião +25 % HP e dano e +1 baú por batida), Trade Mirror 1/1/1/0 (1 de 10 pares
  +20 %/−10 %, mostrado no prompt), Forgetful Monk 1/1/1/1 (esquece 1 golpe ou pergaminho), Shadow Twin 1/1/1/1 (clona item
  não lendário), Sleepy Cat 2/2/2/1 (50 %: +1 nível num pergaminho; senão 15 × zona moedas), Festival Pachinko 2/2/2/1
  (20 × 1,08^giros, segurar E; 777 1,8 % = lendário), Beast Cage 2/2/2/0 (20 + 10 × zona → meia barra de XP), Cursed Chest
  2/2/2/1 (grátis: 1–2 itens + emboscada de 12 + 5 % dificuldade), Gold Vein 4/4/4/3 (3 toques de moedas), Healing Berry
  3/3/3/2 (cura 20 %), Spring Mushroom 2/2/2/1 (impulso só no cliente dono).
- **Sistemas (Partida):** `ObjetoSystem` (novo: sorteio sobre `Alturas` com flood-fill a partir do Spawn, plano, ≥ 25 dos
  pontos-chave, ≥ 8 dos caminhos, raycast no Terrain sem água/colisor; prompts + rótulos; validação de distância ≤ 12, usos,
  moedas, rate-limit; listas com `EscolhaObjeto`/`EscolherObjeto`; laço único a 4 Hz; carteira); `DiretorSystem` (novo:
  evento a cada 60–90 s, 1º aos 50 s, nunca com cartas abertas/fora da fase explorar; Swarm, Stampede, Flock, Rockfall,
  Dominant, Summoner, Fog, Storm, Eclipse, Golden Thief; Siege anti-campar; chefe cansado; marcos de combo 10/25/50/100;
  1º elite da zona solta baú; split de tempo por zona). Ganchos em `EstadoPartida` (`modificadores` da run + `tamborBatidas`,
  zeram no início/Play Again), `ZonaSystem`, `HeroiSystem` (`bonusRun`), `ItemSystem`, `BauSystem`, `LevelUpSystem`
  (`ofertaEspecial`), `InimigoSystem`, `XpSystem`, `ChefeSystem`, `ConquistaSystem`, `PartidaSystem`. Remotes novos:
  `ObjetoUsado`, `EscolhaObjeto`, `EscolherObjeto`, `Evento`, `Carteira`.
- **Moldes:** `ReplicatedStorage/Moldes/Objetos/<id>` (Partida), 16 Models de primitivas (89 Parts), sem colisão; 0 meshes.
- **Cliente:** `ObjetoController` (carteira no topo-centro com o preço do baú em verde/vermelho, rótulos no mundo
  liga/desliga e preço colorido, texto/som/confete do uso, mola, lista de escolha), `DiretorController` (banner, anel do Siege,
  split verde/vermelho), `ZonaVisualController` (hora do dia por zona: tarde → crepúsculo → noite, e atmosfera temporária
  Fog/Storm/Eclipse), `ConfigController` (linha "World labels").
- **Conquistas novas:** Seal Breaker (3 selos numa run), Thunder Drummer (3 batidas + guardião), Lucky 777, Walking Curse
  (15 maldições numa run), Empty Pockets (vencer com ≤ 3 itens).
- **Correções da revisão dos golpes (Task 0):** I1 desbloqueio de QA numa tabela à parte do `PerfilSystem` (nunca vai pro
  DataStore); I2 míssil do Spirit Wisp com `danoFixo` de verdade (sem Cond*/reações/Storm Core); m1 troca de zona limpa os
  efeitos do cliente; m2 `spawn` do QA respeita o teto de vivos.
- Testado em Play pelo Claude via `Qa`: `TesteLogica: OK`; 30 objetos na Vila, todos com Terrain embaixo, 0 colisores,
  dentro do flood-fill; os 16 objetos usados com efeito conferido no `estado`; os 11 eventos forçados sem passar do teto;
  tambor 2× → guardião com 1,5× HP e +2 baús; split ao atravessar o portal; diretor automático disparou aos 50 s. Console
  sem erro novo. Ledger: `.superpowers/sdd/2026-10-30-objetos-eventos-mapa/progress.md`.
- **Pendências:** balanceamento e nomes (Diego); Eclipse "skin rara ×3" é só uma flag (não existe drop de skin); split sem
  recorde no perfil (melhor tempo só da sessão do servidor, o schema não mudou); carteira sem reroll (não existe reroll de
  loja ainda); moldes de primitivas (trocar por mesh quando quiser).
- **Não visto:** aparência dos moldes, rótulos, banner, carteira (pode encostar na HUD do topo), anel do Siege, névoa/
  tempestade/eclipse; prompt real (E) de cada objeto, segurar E no pachinko, mola no relevo; co-op; celular.
- **Lembrete: salvar e publicar os 2 places juntos** (Shared e `ConfigSystem` mudaram nos dois; moldes só no Partida).

### HUD, cartas, pausa, mapa e evolução (2026-10-30)

- **Correções da revisão dos objetos (Task 0):** I1 `ObjetoSystem.abrirOferta` não reabre lista do mesmo objeto e só protege
  1× por objeto/jogador; I2 `DiretorSystem.passoSiege` zera o tempo de quem tem carta (`LevelUpSystem.temAberta`) ou lista de
  objeto (`ObjetoSystem.temOferta`) aberta; m1 `zerarZona` zera combo e marcos; m2 Golden Thief/minis do diretor não contam
  como 1º elite; m3 herói caído solta o pachinko; m4 a 2ª escolha da oferta dupla é sorteada de novo; m8 QA `objeto` responde
  "recusado: <motivo>" (`usar` devolve o motivo).
- **Shared (idêntico nos 2 places, hash 30/30):** `Config` (Rerolls/Skips/BansPorRun 2/5/3, `SkipMoedasPorZona`, rate-limits,
  `RaioDescoberta 60`, `DescobertaHz`, `MinimapaAlcance`, `MapaGradeMax`, `MapaFaceGraus`, `EvolucaoTelaDuracao`,
  `EvolucaoInvulneravel`, `DpsJanela`), `Types` (`DescobertaInfo`, `OfertaCartasInfo`, `RelogioInfo`), `Herois.despertares[i]`
  com `modelo`/`nomeForma`, `Zonas.lagoas` (100 retângulos de água), `Logica/Cartas` (`banidos`), `Logica/Exibicao`
  (Cooldown/Range nas cartas de golpe + `descricaoGolpe`).
- **Remotes novos:** `RerollCartas(ofertaId)`, `PularCartas(ofertaId)`, `BanirCarta(ofertaId, indice)`, `Pausar("pausar" |
  "retomar" | "desistir" | "reiniciar")` (c→s, validados e com rate-limit) e `Descoberto` (s→c). `DanoNumeros` passou de 17 pra
  **18 bytes** (+u8 fonte do dano: golpe na ordem alfabética de `Golpes`, 253 outro, 254 ultimate, 0 = de outro jogador).
  `Relogio` ganhou `total`; `EstadoHeroi` leva `bonus` quando os stats mudam; `workspace.Pausado` (atributo) = pausa do menu.
- **Servidor (Partida):** `LevelUpSystem` (Reroll/Skip/Ban com contadores no estado do herói, zeram no Play Again; Ban não tira
  o último golpe possível; fila de níveis pro título da oferta); `PartidaSystem.pausar` (só solo, usa o mesmo flag das cartas:
  inimigos/projéteis/relógio/diretor congelam; Give up/Restart só solo); `EstadoPartida.cartaAberta/menuPausado`;
  `DescobertaSystem` (novo, 2 Hz, descobre a < 60 studs de qualquer herói vivo, manda a todos, lista inteira pra quem entra);
  `InimigoSystem.fonteDano` + `GolpeSystem` (dano por golpe); `HeroiSystem` (contadores, `qaEvoluir`, invulnerável ao evoluir);
  `BauSystem` (atributo `Gratis`).
- **Cliente (Partida):** `HudController` (cartão do herói com retrato 3D/elemento/Lv/"Next form", painel da zona com
  timer/total/recorde, moedas/itens/abates com rolagem, HP com escudo e sobrecura), `BuildController` (slots embaixo à
  esquerda), `UltimateController` (anel com R), `LevelUpController` + `Util/CartaUI` (cartas detalhadas, Reroll F / Skip X /
  Ban Z, modo compacto no celular, texto ≥ 11 px, dica por toque), `PausaController` (novo; P, Esc via menu do Roblox, botão
  "II"), `MapaController` (novo; minimapa, Tab, M) + `Util/MapaChao`, `EvolucaoController` (novo), `Util/UiKit` (novo),
  `HeroiSpriteController` (modelo da forma), `LojaController` (tela baixa), `ConfigController` (sem o botão fixo; abre pela
  pausa), reposicionamentos em `ZonaHud/Objeto/Diretor/Item/Conquista/Combo`.
- **Modelos:** `ReplicatedStorage/Modelos/Herois/{Ryuga,Kaizo,Haruto}_{2,3}` (generate_mesh, 2 places). **Menu:** ficha do herói
  com "FORMS" (3 retratos, Lv 1/20/40).
- **QA novo:** `evoluir`, `pausar 0|1`, `descobrirTudo`; `estado` mostra pausa, contadores, banidos, despertar e descobertos.
- Testado pelo Claude em Play (detalhes e medidas 1341×650 / 844×390 no ledger
  `.superpowers/sdd/2026-10-30-hud-run-evolucao/progress.md`): `TesteLogica: OK`; HUD abaixo do Inset sem sobreposição;
  Reroll/Skip/Ban com recusa no fim; pausa congela (inimigos e tempo iguais em 3 s) e retoma; 33 descobertos → 19 tipos na
  lista do M; Tab sem travar o movimento; evolução 2× troca o modelo; `zona 2` zera o mapa; 120 inimigos a 120 fps; console
  sem erro novo.
- **Pendências:** liberar **EditableImage** (Experience Settings → Security) pra o chão do mapa virar imagem também no minimapa
  (hoje: grade de 900 Frames no Tab/M e minimapa com fundo liso); textos novos fora da `Localizacao/PtBr`; textos pequenos da
  HUD no celular (escala 0,6); a carta de golpe mostra recarga/alcance base (sem pergaminhos); DPS/dano por golpe é aproximado
  (remote unreliable, teto de 40 números/frame perto do herói); nomes/visual das 6 formas (Diego).
- **Não visto:** aparência (captura sai preta) de HUD, cartas, pausa, mapa, tela de evolução e dos 6 modelos; co-op (pausa só
  painel, faixa de evolução dos outros, Siege com carta aberta); celular de verdade (medidas por aproximação); loja com 5
  cartas; Esc fora do Studio.
- **Correções da revisão (só Partida, sem mudança no Shared):** **relógio da partida** `EstadoPartida.tempoPartida()`
  (avançado pelo `PartidaSystem` no PreSimulation só com `rodando()`; nunca zera). **Regra pra sistemas futuros: prazo de
  jogo (invulnerabilidade, buff breve, desafio, espera no mapa, recarga por tempo) usa `tempoPartida()` ou desconta `dt` no
  Heartbeat que só roda com `rodando()`; `os.clock()` só pra rate-limit de remote, retry/DataStore e input.** Já usam:
  `HeroiSystem` (invuln de evolução/dano/reviver/proteções, velocidade breve, parado, escudo), `ObjetoSystem` (prazo do
  totem, espera fora da chakra stone). Pausa: `"retomar"` sem rate-limit e `"pausar"` na janela fica pendente (I1); a pausa do
  menu congela projéteis/explosões/impactos (cancelar só com carta aberta), cliente congela voos (`EfeitosController`) e
  discos (`AvisoController`) por `workspace.Pausado` (I2); `terminar` desliga a pausa. "EVOLVED!" espera as cartas fecharem e
  some no Play Again. `Client/Util/DanoPacote` (18 bytes) no `AudioController`/`DanoController`. Mapa: trava de cálculo no
  `MapaChao`, descobertos por zona, PlayerList do Roblox desligada (Tab = mapa), Tab/M/P ignorados digitando. `Juice.contador`
  cancela o anterior; reroll evita repetir cartas; `DescobertaSystem` sem `GetChildren`; DPS da pausa ignora o tempo pausado.
  QA `estado` mostra `relogio`, `invuln`, `projIni/explIni/impactos` e `desafio`. Detalhes e testes no ledger.
- **Lembrete: salvar e publicar os 2 places juntos** (Shared, modelos e Menu mudaram nos dois).

### Menu redesign (2026-10-30)

- **Só no place Menu** (Shared intocado). Plano `plans/2026-10-30-menu-redesign.md`, ledger
  `.superpowers/sdd/2026-10-30-menu-redesign/progress.md`.
- **Estrutura nova (cliente):** `Client/Util/Tema` (paleta índigo/carmim/dourado, GothamBlack/GothamMedium, cantos 12,
  painel translúcido com gradiente, `sombra`, `bordaRaridade`, `titulo`, `semTraducao`); `Client/Util/Navegacao` (pilha
  com a Home na base, Back único em x 6 px / inset + 8, Esc e Backspace voltam, slide + véu, só a tela do topo visível,
  abas do clã trocam no lugar); `Util/Juice` + `transicaoTela`, `brilhoRaridade` (**só no Menu**: copiar pro Partida);
  `Controllers/CenarioController` (novo); `Controllers/Telas/` (Folder, fora do bootstrap): `Home`, `Herois` (novas),
  `Preparar`, `Dojo`, `Skins`, `Conquistas`, `Tarefas`, `Ranking`, `Config`, `Cla` (movidas do MenuController; cada uma
  `construir(ctx)`). `MenuController` (~980 linhas) segue dono de estado, remotes e `atualizar*` e monta o `ctx`.
- **Cena 3D:** `Workspace/Cenario` (Model Persistent, 181 instâncias, 11 luzes) a 3000 studs no X: pátio de pedra,
  pedestal com anel dourado, torii, 6 lanternas de pedra, 2 cerejeiras com pétalas, bambuzal, 4 casas com lanternas de
  papel, montanhas, vaga-lumes. Lighting do Menu no entardecer (+ `ColorCorrection` `CorMenu`, DOF). O controller
  balança a câmera em arco (±18°, 26 s), põe o herói selecionado no pedestal (forma da ficha / skin; trancado em
  silhueta) com flash, e enquadra por tela (centro em Heroes/Skins, direita no resto).
- **Home:** logo, PLAY grande com brilho, Co-op ("Rooms coming soon") e Survival apagados, 8 atalhos (Heroes, Dojo,
  Skins, Achievements, Daily Tasks, Leaderboard, Clan, Settings), barra com avatar/nome/Essência/heróis, cartão de
  sequência diária (abre Daily Tasks), recordes e placa do herói. **Heroes:** ficha com rolagem (retrato, classe,
  elemento, 3 formas clicáveis, stats base → na partida com Dojo e dica, passiva, 6 golpes com números e cadeado,
  3 ultimates, partidas) + grade com silhueta, desafio e barra/“Next”. **Prepare:** prévia translúcida, 4 zonas com
  miniatura e guardião, dificuldade, recordes, Start grande.
- **Coming soon / pendências:** co-op com salas, Survival, regiões 2–4, estatísticas por herói, nível de conta;
  textos novos fora da `Localizacao/PtBr`; Juice novo e Tema no Partida.
- **Não visto:** aparência (captura sai preta), celular real (medidas por cálculo), Esc fora do Studio (abre também o
  menu do Roblox), compra/equipar com perfil real, partículas.
- **Lembrete: salvar (Ctrl+S) e publicar o Menu** (cena, Lighting e scripts novos só existem na sessão até salvar).

### Co-op com salas (2026-10-30)

- Plano `plans/2026-10-30-coop-salas.md`, ledger `.superpowers/sdd/2026-10-30-coop-salas/progress.md` (decisões).
- **Task 0:** `ObjetoSystem.usar` não diz mais "recusado" quando o Challenge Totem começa o desafio (e não devolve
  o preço); `Util/Juice` idêntico nos 2 places (Menu ganhou o `contador` com cancelamento; Partida ganhou
  `transicaoTela`/`brilhoRaridade`); `Util/Tema` copiado pro Partida.
- **Shared (idêntico nos 2 places: 31 ModuleScripts em comum com hash igual; `Mapa.Alturas` existe só no Partida;
  `Util/Juice`/`Tema` ficam em `Client/Util`, não no Shared):** `Logica/Sala` (novo, puro: código de 6 letras A–Z sem I/O e sem
  dígitos, vagas, líder → mais antigo, pronto, config só do líder, sala vazia = "fechada" até o TTL, `valida`, nomes
  e chave do ranking coop); `Config` bloco "Co-op com salas" (`SalaTTL 1800`, `RateLimitSalaCriar 10`,
  `RateLimitSala 1`, `SalaTentativas 3`, `SalaBuscaMax 50`, `SalaTeleporteTimeout 40`, `EsperaSala 20`,
  `FimEquipeSegundos 15`, `ReviveAllEssencia 100`, `PausaEquipeSegundos 300`, `RateLimitCoop 0.5`, `MapasCoop`,
  `MapaPadrao`, `NomesMapa`); `Types` (`DadosTeleporte` + `sala/mapa/membros/herois`, `EntradaRanking.userIds?`,
  `SalaInfo`, `SalaEstadoInfo`, `EsperaSalaInfo`, `FimEquipeInfo`, `PausaEquipeInfo`). Também idênticos:
  `Systems/RankingSystem` (placares `CoopTempo_<n>_<dif>_<mapa>`, `registrar(..., semTempo?)`, `registrarCoop`) e
  `Testes/TesteSala`. **Perfil continua v6** (a v6 veio das skins; o co-op não mudou o schema, então não há migração).
- **Menu:** `Systems/SalaSystem` (novo) — MemoryStore SortedMap `Salas` (código → sala, `UpdateAsync` com a regra
  dentro: vagas nunca passam do máximo) + `SalasAbertas` (índice do matchmaking) + MessagingService `Salas`
  (sincroniza os servidores do Menu; teleporte publicado com o código do servidor reservado). Remotes c→s
  `SalaCriar {heroiId, dificuldade, mapa, tamanho, publica}`, `SalaEntrar {codigo, heroiId}`, `SalaSair`,
  `SalaPronto {pronto, heroiId?}`, `SalaIniciar`, `SalaConfig {mapa?, dificuldade?, publica?, tamanho?}`,
  `SalaBuscar {tamanho 0|2|3|4, heroiId, contar?}`; s→c `SalaEstado {sala?, foraDeSala?, aviso?, buscando?}`.
  `MenuSystem.prepararTeleporte/liberarTeleporte/marcarTeleportAsync/aoSairDaSala` (jogar solo tira da sala).
  `Testes/TesteLogica` (novo, roda o `TesteSala`). Cliente: `Telas/Coop` (telas "coop" e "lobby"), botão Co-op
  da Home ligado, Leaderboard com abas Solo/Duo/Trio/Squad (grupo: sub-aba por dificuldade).
- **Fluxo:** Home → Co-op → Create room (dificuldade/tamanho/pública) | Join with code | Quick match (entra na sala
  pública mais cheia do tamanho ou cria uma; "N searching" = jogadores esperando em salas abertas) → Lobby (código
  selecionável, membros com herói/pronto, config do líder, Ready/Start/Leave/Change hero) → líder Start →
  `ReserveServer` + `TeleportAsync` por servidor do Menu (retry 3×) com `TeleportData { sala, dificuldade, mapa,
  membros, herois }` → Partida espera até 20 s ("Waiting for party N/M") → partida.
- **Partida:** `Systems/CoopSystem` (novo): espera da sala (só em servidor reservado), End Match / Revive All (15 s,
  jogo congelado; Revive All cobra 100 Essência de quem clicou, 1× por partida, idempotente, nunca negativa;
  End Match = voto, todos → fim; tempo esgotado → fim), pausa por votação (maioria simples, 300 s por partida,
  qualquer um retoma), ranking coop no fim (vitória com 2+ heróis vai só pro `CoopTempo_*`). Remotes c→s
  `ReviveAll`, `EncerrarPartida`, `VotarPausa(bool)`; s→c `EsperaSala`, `FimEquipe`, `PausaEquipe`.
  `EstadoPartida.equipePausada/decisaoEquipe` (entram no `pausadoPorCarta`), `HeroiSystem.reviverTodos`,
  ganchos no `PartidaSystem` (espera, dificuldade da sala, derrota, terminar/iniciar/Play Again). Cliente:
  `CoopController` (novo) e botão "Team pause" no painel de pausa do co-op (no lugar de Give up/Restart).
  QA: `coop n`, `cairTodos`, `votarPausa 0|1`, `essencia n`, `coopEstado`.
- **Testado pelo Claude (Studio):** os 2 `TesteLogica` OK; Partida via `Qa` (espera 1/2 → começa aos 20 s, voto solo
  ignorado, End Match 15 s, Revive All 3 cliques → cobra 1×, fim por tempo); Menu por remote/clique (criar, config,
  Start no Studio volta pro lobby com aviso, contagem, sair, código inválido/inexistente, quick match, telas
  Lobby/Co-op/Leaderboard). MemoryStore e MessagingService responderam no Studio (o caminho de falha com aviso
  amigável não foi exercitado em runtime).
- **Só o Diego testa (publicado, 2 contas):** criar sala numa conta e entrar com o código na outra (inclusive em
  servidores diferentes do Menu); pronto/config/Start → os dois no mesmo servidor reservado; teleporte falhando pra
  um; quick match Duo nas duas contas; End Match/Revive All com 2 caídos (Essência real), voto de pausa 2/2 e Resume;
  vitória em Duo aparecendo na aba Duo do Leaderboard; aparência das telas novas e no celular.
- **Correções da revisão (2026-10-30, ledger `.superpowers/sdd/2026-10-30-traducao-final/progress.md`):**
  I1 — `Logica/Sala` ganhou `inicio: string?` (`marcarIniciando(sala, inicio?)` grava, `voltarLobby` limpa, `valida`
  aceita); `SalaSystem.iniciarSala` gera um GUID e o timeout de 40 s confere `estado == "iniciando"` + esse id (antes
  conferia `versao`, que muda a cada membro que teleporta e sai). I2 — `aoEntrar` entra na sala nova primeiro e só
  então sai da antiga (`sairDeCodigo`): código errado/cheio não expulsa. I3 — `desfazerSeSaiu`: se o jogador saiu do
  jogo durante o `UpdateAsync` de criar/entrar, é tirado da sala e `salaDe` não é gravado; `PlayerRemoving` limpa
  `salaDe` mesmo se a gravação falhar. m1 — `sairDaSala` só limpa `salaDe` depois de gravar (falha → mantém, avisa e
  devolve false; criar/quick match param). m2 — `comTrava(..., silencioso)`: `SalaBuscar{contar}` com ação em andamento
  é ignorado sem "Please wait...". QA só no Studio: atributo `QaPrenderInicio = true` no módulo `SalaSystem` (em Play)
  deixa o Start "iniciando" pra testar o timeout. Testado em Play: código errado não tira da sala; contagem silenciosa;
  sala presa em "iniciando" com versão alterada volta pro lobby aos 40 s.
- **Pendências:** expulsar membro (fora da lista de remotes decidida); só 1 mapa (`ShinobiLands`); ranking coop só
  mostra o mapa padrão. (Textos: ver "Tradução pt-BR dos lotes de 2026-10-30".)
- **Lembrete: salvar (Ctrl+S) e publicar os 2 places JUNTOS** (Shared, RankingSystem e Juice mudaram nos dois).

### Tradução pt-BR dos lotes de 2026-10-30

- Ledger `.superpowers/sdd/2026-10-30-traducao-final/progress.md` (contagem por origem e lista do que ficou em inglês).
- `Shared/Localizacao/PtBr` (idêntico nos 2 places): 583 → 1070 pares (468 novos: itens 141, pergaminhos 23,
  formas/golpes/rótulos de `Exibicao` 32, objetos/eventos 72, HUD/cartas/pausa/mapa 61, co-op Partida 13, co-op Menu +
  menu redesign + clã/skins 77, chaves dinâmicas 49). A `LocalizationTable` gerada no boot fica com 1064 entradas
  (dedup por `key`/`en`); `SetEntries` continua idempotente, sem lotes. "Forest of Trials" agora é "Floresta das
  Provações".
- Textos com número/nome passaram a usar `LocalizacaoController.formatar` (chaves `zona.*`, `hud.*`, `lv.n`,
  `golpe.nivel`, `levelup.*`, `pausa.*`, `coop.*`, `evolucao.outro`, `split.*`, `item.*`, `carta.*`, `home.*`) e
  `traduzir` pros nomes dentro deles. Partida: `ZonaHudController`, `PausaController`, `LevelUpController`,
  `CoopController`, `HudController`, `EvolucaoController`, `ItemController`, `DiretorController`, `BuildController`,
  `Util/CartaUI`. Menu: `Telas/Coop`, `Telas/Home`.
- Ficam em inglês (precisam refatorar o payload/montagem): descrição gerada dos golpes (`Logica/Exibicao`), avisos
  montados no servidor do `ObjetoSystem`/`DiretorSystem`/`BauSystem`/`MercadorSystem`, rodapés da loja, decomposição
  de atributos na tela Heróis do Menu e sufixos antigos do Menu (lista completa no ledger).
- Testado em Play (Partida): tabela com 1064 entradas, `GetTranslator("pt-br")` traduz as amostras e as chaves.
  Falta o Diego ver as telas com o idioma pt-BR (emulação de idioma no Studio ou conta em português).
- **Lembrete: salvar (Ctrl+S) e publicar os 2 places JUNTOS** (`Shared/Localizacao/PtBr` e `Logica/Sala` mudaram nos dois).

### Polimento UI v2 (2026-10-30)

- Feedback do Diego depois de jogar. Plano `plans/2026-10-30-polimento-ui-v2.md`, ledger
  `.superpowers/sdd/2026-10-30-polimento-ui-v2/progress.md` (assetIds, decisões, medidas).
- **Shared (idêntico nos 2 places, 31/31 por hash):** `Definicoes/Golpes` (tipo `IconeRect`; `icone` + `iconeRect` nos 18),
  `Definicoes/Ultimates` (idem nas 9), `Definicoes/Pergaminhos` (idem nos 25), `Definicoes/Zonas.mapaImagem` (4),
  `Config.MultVelocidadeHeroi = 1.25`, `Types.InfoUltimate.id?`, `Itens` (letras ASCII no Phoenix Feather/Fate's Bell).
- **Imagens:** mapas 1024² por zona (relevo de `Mapa/Alturas` com sombra do noroeste, material do Terrain, penhascos com
  traço, lagoas/riacho, trilhas a partir do Mercador, vinheta) e 6 folhas 3×3 de ícones (3 heróis com 6 golpes + 3
  ultimates; pergaminhos em 3 folhas). O Canva não estava conectado: ícones desenhados em Python/PIL (medalhão na cor
  do elemento + símbolo). PNGs, geradores e dados de entrada em `arte/polimento-ui-v2/`.
  **Como gerar/subir de novo:** (1) se o terreno mudar, regerar `Mapa/Alturas` e mandar o `Source` + material por
  amostra pro `recebidos/` (POST pro `ferramentas/receptor.py` na 8766 com `HttpEnabled` ligado só durante o
  `execute_luau` em Edit); (2) `python -I ferramentas/gerar_mapas.py` / `gerar_icones.py`; (3) servir `imagens/` com
  `python -m http.server 8765` e chamar `upload_image` com `http://localhost:8765/<arquivo>.png`; (4) gravar os ids nas
  `Definicoes` (2 places).
- **Partida (cliente):** `Util/Icone` (novo: imagem recortada da folha + letra/sigla de reserva se não houver asset ou
  se o asset falhar), `Util/Teclas` (novo, igual no Menu: "[E]", "[ENTER]", "[Tab]", "[M1]"… viram tecla desenhada;
  sem teclado a tecla some), `Util/MapaChao` (usa `mapaImagem`; grade/EditableImage só se o asset não carregar),
  `MapaController` (minimapa encostado no topo, anel dourado, seta desenhada, dica Tab/M), `HudController` (topo a 4 px
  da borda onde a barra do Roblox não tem botão — `Inset.livre()`; cartão do herói à direita dos botões),
  `BuildController` (ícones + **barra de recarga** por slot, reinicia no remote novo `RecargaGolpe`),
  `UltimateController` (círculo com ícone, anel de carga horário, tecla R), `Util/CartaUI` (ícone pela definição,
  carta de golpe sem "Affects", rodapé com tecla), `LevelUpController`/`PausaController`/`LojaController`/
  `ConfigController`/`FimController` (Enter = Play Again)/`HeroiEscolhaController` com teclas desenhadas; glifos fora
  da fonte trocados por ASCII (lista no ledger).
- **Partida (servidor):** `GolpeSystem` manda `RecargaGolpe(golpeId, segundos)` (UnreliableRemoteEvent) ao dono a cada
  disparo; `UltimateSystem` manda `id`; `HeroiSystem` aplica `Config.MultVelocidadeHeroi`.
- **Menu:** `Util/Teclas` + Shared; teclas desenhadas nos cabeçalhos (Esc Back / Enter Start), no PLAY, na grade de heróis
  e nos botões Start/Choose hero; ícones dos golpes/ultimates na ficha do herói. Resto do Menu intocado.
- Testado pelo Claude em Play: barra de recarga 13 eventos = 13 reinícios; topo a 4 px; ultimate quadrada com canto
  (1, 0); carta de golpe sem "Affects" e de pergaminho com; 11 teclas na pausa; WalkSpeed 18,9 → 23,625; Menu sem erro.
- **Pendência principal: as 10 imagens ainda não carregam** (ContentProvider "Failure"): o place é do grupo e os assets
  foram enviados pelo usuário Alucard26. Diego: no Creator Dashboard dar permissão de uso dessas imagens à experiência
  (ids no ledger) ou subir os PNGs pelo grupo e trocar os ids. Até lá: letras/siglas nos ícones e grade no mapa.
- **Não visto:** aparência (captura sai preta), mapa com a imagem carregada, celular real.
- **Lembrete: salvar (Ctrl+S) e publicar os 2 places JUNTOS** (Shared mudou nos dois; Util/Teclas novo nos dois).

### Co-op v2 (2026-10-30)

- Correções do teste em dupla + caído com prazo + ping. Ledger `.superpowers/sdd/2026-10-30-coop-v2/progress.md`
  (causa raiz com linhas, tabela dos 16 moldes, testes).
- **Bug "ficamos no mapa 1":** golpe com teleporte (Shadow Step / Instant Step) chamava `HeroiSystem.teleportar` durante
  a espera do streaming da troca de zona e reiniciava o teleporte longo (seq novo) — no publicado, com streaming lento, a
  troca nunca terminava. Agora: `teleportar` com prazo total `Config.TeleporteZonaTimeout` (6 s, move mesmo se o
  streaming falhar); golpe usa `HeroiSystem.teleportarGolpe` (só curto e nunca com teleporte pendente); `ZonaSystem`
  troca o estado e teleporta antes de limpar/gerar (cada passo em pcall), `avancar` protegido; **vigia** a cada 1 s
  devolve ao Spawn quem estiver fora da zona atual.
- **Regras novas:** caído no co-op tem `Config.TempoCaido` 60 s (relógio da partida) pra ser revivido (segurar E); zerou
  = **morto** até a zona seguinte (renasce no Spawn com HP cheio); Revive All traz mortos também; todos caídos/mortos =
  End Match. Solo igual a antes. **Ping G**: toque = "I'm here", segurar = roda (Help! / I'm here / Need backup),
  rate-limit 1 s, marcador 3D + minimapa + som por 4 s.
- **Novos:** `Server/Systems/EquipeSystem` (remotes `Equipe` s→c a 4 Hz quando muda, `Ping`), `Client/Controllers/
  EquipeController` (painel da equipe à esquerda, nome+HP sobre o aliado, setas no mapa, feixe e bússola do caído, tela
  cinza DOWN/DEAD), `PingController`. `MapaController.marcador/tirarMarcador`. Shared: `Config` (bloco "Co-op v2"),
  `Types` (`EquipeMembro`, `EquipeInfo`, `PingInfo`) — idênticos nos 2 places.
- **Objetos deitados/afundados:** pivô dos 16 moldes (`Base.PivotOffset`) em pé, na base, Y do chão; 6 estavam deitados
  (Chakra Stone, Shadow Twin, Challenge Totem, Sleepy Cat, Spring Mushroom, Forgetful Monk) e vários afundados (Pachinko 3).
- **Menu:** herói trancado só fica na ficha de Heroes/Skins; saindo dela volta o último desbloqueado (`MenuController`).
- QA novo: `cair`, `morrer`, `prazoCaido n`, `portal`, `fecharCartas`, `aliadoFake v|c|m|off`, `ping tipo`, `equipe`.
- **Diego testa em dupla (publicado):** passar de zona com os dois (principalmente com Haruto/Shadow Step); nome/HP sobre
  o amigo, painel à esquerda e seta no minimapa; cair → feixe, bússola no outro, contador 60→0, "DEAD" e renascer na zona
  seguinte; reviver segurando E; G tocado/segurado e o ping aparecendo pro amigo; objetos em pé; Menu com herói trancado.
- **Lembrete: salvar (Ctrl+S) e publicar os 2 places JUNTOS** (Shared mudou nos dois; moldes e sistemas no Partida;
  `MenuController` no Menu).

### Menu — botão Back fora dos ícones do Roblox (2026-10-30)

- `Client/Util/Inset` criado no Menu (cópia do Partida). `MenuController.cabecalho()`: Back na margem esquerda
  (x 0,006) com `Inset.manterAbaixo`; faixa do título anda pra direita se `GuiService.TopbarInset` a cobrir
  (`manterADireitaDaBarra`, local). `construirInicio`: Idioma, Treasures, Shop e BarraPerfil com `manterAbaixo`.
  Não testado em Play (UI só monta em Play). Ledger: `.superpowers/sdd/2026-10-30-menu-voltar/progress.md`.

### Fase 2 — conteúdo (planos escritos em 2026-10-30, ordem combinada com o Diego)

1. `plans/2026-10-30-mapa-ninja.md` — relevo (Terrain + grade `Shared/Mapa/Alturas`), zonas a 4000 studs, cenário ninja.
2. `plans/2026-10-30-inimigos-ninja.md` — 16–20 mobs, guardiões folclóricos (raposa, sapo, cobra, lesma), chefe final.
3. `plans/2026-10-30-itens-pool.md` — ~80 itens / ~24 pergaminhos, 5 raridades, linha "Affects" por golpe equipado.
4. `plans/2026-10-30-hud-run-evolucao.md` — prateleira de itens, contadores, baú/mercador, pausa, evolução com modelo.
5. `plans/2026-10-30-golpes-pool-efeitos.md` — 6 golpes por herói, pool global por desbloqueio de herói, 10 estilos visuais.
6. `plans/2026-10-30-objetos-eventos-mapa.md` — 15 objetos de uso único (risco ↔ prêmio), diretor de hordas/eventos, carteira.
7. `plans/2026-10-30-menu-redesign.md` — tema, cena 3D, telas por arquivo, telas incompletas.
8. Depois: co-op com salas (código, matchmaking, servidor reservado, End Match/Revive All), Sobrevivência, Mutação do Dia.
   Regra do tema: ninja **original** (folclore ok; nomes/visuais de obras existentes não).
   Pesquisa complementar do PokeBonk (2026-10-30): `docs/pokebonk-pesquisa-2026-10-30.md` (ideias pra entrar nos lotes).
   Ordem autorizada pelo Diego em 2026-10-30 ("faça os recomendados e o que vc tiver de ideia e no final vc me conta").

## Status

- 2026-10-29: projeto iniciado. Regras copiadas/adaptadas do Table_Stories
  (`CLAUDE.md`) e referência completa do Megabonk anotada (`docs/megabonk-referencia.md`).
- 2026-10-29: referência do PokeBonk anotada (`docs/pokebonk-referencia.md`) a partir das
  78 telas do Diego (`C:\Users\Diego\Desktop\pokebonk`) + guias do megabonk.org/pokebonk.
  O Diego quer o AnimeBonk parecido com o PokeBonk (co-op + sobrevivência).

- 2026-10-29: design da v1 aprovado: `docs/superpowers/specs/2026-10-29-animebonk-design.md`
  (nome AnimeBonk; heróis Ryuga, Kaizo, Haruto em sprite 2D; sem lobby, só menus; co-op
  2–4; reviver pago; inglês + pt-BR; clãs na etapa 7).

## Revisão final v2 (2026-10-30, fim do dia — INTERROMPIDA, retomar primeiro)

Pedido do Diego ao sair: "veja se tem algo a melhorar e melhore". Plano `docs/superpowers/plans/2026-10-30-revisao-final-v2.md`;
ledger `.superpowers/sdd/2026-10-30-revisao-final-v2/progress.md` (tem o detalhe de tudo abaixo).
- **Revisões feitas** (nada crítico): Partida `.superpowers/sdd/2026-10-30-coop-v2/review.md` (2 importantes: seta do aliado
  não mudava de cor; ping repetido mantinha ícone antigo; 8 menores), Menu `.superpowers/sdd/2026-10-30-menu-redesign/review.md`
  (1 importante: herói da sala ≠ herói mostrado; 6 menores; I1–I3 da revisão de salas confirmados corrigidos).
- **Playtest** de run inteira (vitória + derrota + Play Again + co-op simulado): `.superpowers/sdd/2026-10-30-revisao-final-v2/playtest.md`.
  Sem erro de console nem vazamento. 1 importante (HUD segurava nível/moedas/itens da run anterior após Play Again), 5 menores
  (tradução pt-BR pela metade, tela de fim sem botão Menu/moedas, "Essence +N (total T)" não fecha, clique no herói durante
  "Waiting for party" não vale, Ryuga parado morre em 32 s).
- **Menu: 7 correções feitas** (I1 herói × sala, m1 timeout em todos os servidores, m2 aviso ao falhar saída, m3 Perfil novo
  com trancado, m4 skin de herói trancado recusada "Unlock the hero first.", m5 `TesteSala` com id de início, m6 `Util/Inset`
  igual ao Partida). Testado em Play, `TesteLogica OK`.
- **Partida: implementador interrompido no meio (Diego precisou sair)**. Pelo código (grep "Revisão v2"/"Revisão final v2"),
  **feitos**: `MapaController.marcador` repinta cor/letra; `Config.InvulnRenascer` 9 s no `renascerMortos`; bússola do caído
  sem alocação por frame; `PingController` limpa marcas no `PlayerRemoving`/Play Again; `BuildController` barra de recarga
  só congela com cartas no solo; `Config.VigiaFolgaXZ`/`VigiaYMinimo` na vigia; `EquipeController` usa
  `LocalizacaoController.texto/formatar` pros estados (chaves `equipe.caido`, `equipe.caidoTitulo`, "Down", "Dead", "DOWN",
  "DEAD" — **ainda não existem no `PtBr`**, fallback em inglês); `HudController.redesenharTudo` após Play Again/troca de herói;
  `LocalizacaoController` do Partida agora traduz à mão todo TextLabel/TextButton do PlayerGui (dicionário en→pt da tabela)
  porque a tradução automática do motor não trocava o texto; `Types.FimPartidaInfo` ganhou `essenciaExtra`/`moedas` (o
  servidor já preenche? **conferir** `PartidaSystem`/`PerfilSystem`); `CoopController` aceita escolha de herói durante a espera.
  Todos esses scripts passam no `loadstring` (sintaxe ok). **Não feitos**: botão "Menu" na tela de fim + "Coins: N" (remote
  `VoltarMenu` com `TeleportAsync` pro Menu), tela de fim usando `essenciaExtra` (checar se o cliente mostra), pares novos no
  `PtBr` (os 6 do caído + "Hero locked", "Unlock the hero first.", "Could not leave your previous room." + os textos que o
  playtest viu em inglês: "Level up!", nomes de golpe no slot/carta, "Giant Slug", "Final zone", "DEFEAT"...), copiar
  `Testes/TesteSala` do Menu pro Partida, m6/m8 da revisão (decididos: não fazer).
- **Shared conferido idêntico nos 2 places** (31 módulos, hash) depois de eu copiar à mão `Config` (3 chaves) e `Types`
  (2 campos) pro Menu. **Divergência de propósito**: `Client/Controllers/LocalizacaoController` (Partida 6455 chars com a
  tradução manual; Menu 3926 chars, versão antiga, que no Menu funciona) — decidir amanhã se copia pro Menu.
- `HttpEnabled = false` nos 2. Nada salvo: **Ctrl+S nos 2 places** antes de fechar o Studio (todo o dia 30 está só na sessão).

### Retomada 2026-11-03 — lote CONCLUÍDO (detalhe no ledger `.superpowers/sdd/2026-10-30-revisao-final-v2/progress.md`)

- O Studio fechou sem salvar no dia 30, mas os **arquivos de recuperação automática** dos 2 places tinham tudo (conferido por grep).
  Diego publicou os dois por "Publish to Roblox As → Update existing" (recuperados vêm com PlaceId 0).
- Itens "Não feitos" fechados (inline, sem agente — o auto mode recusou o Agent por causa do hook do `context-mode`):
  tela de fim com botão **Menu** (remote `VoltarMenu` → `PartidaSystem.aoVoltarMenu`: só fora de partida, rate-limit
  `Config.RateLimitVoltarMenu`, `salvarAgora` + `TeleportAsync(Config.PlaceIdMenu)`), "· Coins N" e Essência com
  "bonus +E"/"spent E" (`essenciaExtra` = total − Essência ao entrar na run − prêmio; `essenciaInicio` no `PartidaSystem`);
  `PtBr` +9 pares (caído, skins, salas) idêntico nos 2; `TesteSala` do Menu copiado pro Partida. `TesteLogica OK`, tela de fim
  conferida em Play (Coins 57, bonus +20 da conquista da 1ª run), 1 warn esperado do teleporte no Studio.
- **Decisão**: `LocalizacaoController` novo fica só no Partida (Menu segue com o antigo). `Util/Inset` idêntico nos 2 (2250 chars).
- **Pendente**: Diego salvar/publicar os 2 places; testar publicado o Partida→Menu (perfil chega salvo?); passar um revisor
  neste lote quando o fluxo de agentes voltar; "An ally can revive you (hold E near you)"/"You return in the next zone" sem PtBr.
- **Anotações do Diego (2026-11-03, inline; detalhe no mesmo ledger)**: herói do Menu com os pés no pedestal
  (`CenarioController`: pivô dos moldes é no centro → compensa pela bbox); Esc fecha o mercador mesmo "processado"
  (`LojaController` + guarda `fechouHaPouco` no `PausaController`); "Affects:" sem letra preta (`ItemController` espelha
  `TextTransparency` no `UIStroke`); `Config.ChefeHpMult = 10` em `InimigoSystem.spawnarChefe` (guardiões/chefe final, minis não;
  só vida); relógio da zona passa de 0:00 e mostra "+M:SS" (`ZonaSystem.restante` negativo + `HudController.textoDoTimer`; o
  Cerco Final já escala spawn ×3 e vida +25%/min); rótulo dos objetos `AlwaysOnTop` (% da Chakra Stone); orbes voam até quem
  coletou (`XpSystem.coletores` + `EfeitosController.voosOrbe`, `Config.OrbeVoo*`). `Config` 24251 chars nos 2 places.
- **Revisão + playtest de 2026-11-03** (`.superpowers/sdd/2026-10-30-revisao-final-v2/review-2026-11-03.md` e
  `.superpowers/sdd/2026-11-03-playtest/`): revisor achou 2 importantes (coletores desalinhados no teto de orbes; VoltarMenu sem
  travar o perfil) — corrigidos (`XpSystem`, `PartidaSystem.aoVoltarMenu` com token/trava/TeleportInitFailed/aviso s→c,
  `FimController` reabilita pelo aviso). Playtest inline: run inteira até a vitória, derrota, Play Again, Kaizo nv 20/40, pausa, mapa,
  objetos, salas no Menu — 0 importantes; HP "173 / 172" corrigido (`HudController` ceil nos dois). Pendente: Diego salvar/publicar
  os 2; briefs de playtest prontos pra rodar com agentes quando o auto mode permitir. **Decisão do Diego (2026-11-03)**: co-op já
  foi testado com um amigo antes; testes de teleporte (Partida→Menu, salas publicadas) ficam pra depois.

### Survival + Mutação do Dia (2026-11-03, inline; spec `docs/superpowers/specs/2026-11-03-survival-mutacao-design.md`,
ledger `.superpowers/sdd/2026-11-03-survival-mutacao/progress.md`)

- **Modo** viaja em `PedidoHeroi`/`DadosTeleporte.modo` (`Definicoes/Modos`: classico, sobrevivencia, mutacao); quem começa a
  partida fixa `EstadoPartida.modo`. Home: PLAY (clássico) + cartões Co-op / Survival / Daily Mutation; Prepare mostra o modo.
- **Survival**: Vila infinita sem altar/portal, relógio subindo, chefes nos marcos 5/10/15/30/45 min (`Config.Survival*`) e
  Endless Night; pressão por minuto; depois de cada chefe de marco, **pacto** obrigatório (`Definicoes/Pactos`, `PactoSystem`
  pela UI `EscolhaObjeto`); fim "SURVIVED", Essência por minuto, placar `SurvivalTempo` (aba no Leaderboard). Qa `marco`.
- **Mutação do Dia**: `Definicoes/Mutacoes` (7) + `Logica/Mutacao` (rotação por dia UTC), dificuldade fixa Normal, semente fixa
  de objetos/baús, placar `Mutacao_<dia>` (zona×1e6+abates; Leaderboard modo "Mutation" Hoje/Ontem), trilha de prêmios 1×/dia
  (`Config.MutacaoPremios`, **perfil v7** `mutacao`), tela "Daily Mutation" no Menu, chip na HUD. Qa `mutacao <id>`.
- Testado em Play nos 2 places (ver ledger). Publicado pelo Diego em 2026-11-03 (perfil v7 no ar).
- **Revisão (2026-11-03, agentes)**: 9 importantes + 11 menores (`review.md`); os 9 + M3/M5 corrigidos e re-revisados
  (`fix-review.md`: 0 importantes). Destaques: nome do chefe de marco na HUD, Play Again mantém o modo (`modoTeleporte`),
  semente do dia só no posicionamento (`Random` local em `ObjetoSystem`/`BauSystem.gerar`; sorteios de resultado aleatórios),
  ranking só aceita `Mutacao_<hoje|ontem>` + `Config.RateLimitRankingJogador`, tempo individual no Survival (`inicioSurvival`),
  solo Survival/Mutação em **servidor reservado** (`MenuSystem`), caídos levantam no marco (`renascerMortos(true)`) e recebem
  pacto, raio dos comuns × escala da mutação, mutação não mexe nos chefes, QA não grava placar, sala força clássico.

### Polimento Survival/Mutação + giro do herói + Endless Night (2026-11-03, agentes; plano
`docs/superpowers/plans/2026-11-03-polimento-survival-giro.md`, ledger `.superpowers/sdd/2026-11-03-polimento-survival-giro/`)

- **Giro do herói (PokeBonk)**: `GolpeSystem` manda `uid` (+ `gdx/gdz` no 1º projétil do leque) nos golpes do herói com alvo
  (`usarDef(..., semGiro)`; míssil ao matar do `ItemSystem` passa `semGiro`); `EfeitosController.aoEfeito` → `HeroiSpriteController.
  encarar(player, dx, dz)`; `passoGiros` no RenderStepped existente gira o C0 da solda e volta após `Config.HeroiGiroDuracao`
  (0.35). Sem suavização (Humanoid vira o personagem) — Diego avaliar visualmente.
- **Endless Night / elite**: `Config.SurvivalElitePorMinuto` 0.01 (teto `SurvivalEliteMax` 0.5) via `InimigoSystem.definirEliteExtra`;
  velocidade dos comuns ×1.1 aos 45:00 e +0.1 a cada 5 min (`SurvivalEndlessVelPasso`, teto `SurvivalEndlessVelMax` 1.6) em
  `ZonaSystem.multVelEndless`; chefes fora. Qa `endless`.
- **Menores fechados**: tiers das pedras iguais na Mutação; tela SURVIVED com tempo do jogador; `premiarMutacao` não repaga na
  virada de dia; `PactoSystem` reabrir com rate-limit (`RateLimitReabrirPacto` 0.5, reenvio agendado, nunca descarta);
  `Logica/Perfil.migrar` filtra marcos; Menu com `GetServerTimeNow`; `atualizarModo` devolve a dificuldade; `ReserveServer` com
  `comRetry` e saída da sala só após sucesso; `HeroiEscolhaController` filtra `td.modo`.
- Revisão: 2 importantes (pacto sumindo no rate-limit; míssil girava o herói) corrigidos; re-revisão em `review-2.md`.
- **Shared**: `Config` (26742) e `Logica/Perfil` (13434) idênticos nos 2 places. **Nada salvo** até o Diego publicar.
- **Decisão do Diego (2026-11-03)**: no Survival só o relógio decide marcos e Endless Night (PokeBonk) — `ZonaSystem.
  proximoHorarioMarco()` põe os guardiões da Endless Night numa grade absoluta (45:00 + k×5 min); matar o chefe não adianta nada.
  Limite: um chefe de marco por vez (se o anterior vive além do horário, o próximo nasce logo que ele morre).
- Menores abertos (decisão do Diego): pacto não pausa o jogo (M6); contagem de maldições só conta as de inimigo (M11); `noRaio` não cobre a borda extra dos gigantes na grade; `qaEndless` pula o
  5º marco; tradução dos textos novos no lote final.

### R1 — menores abertos + modos em sala co-op + prioridade de chefe (2026-11-03, agentes; plano
`docs/superpowers/plans/2026-11-03-restante-r1-coop-modos.md`, ledger `.superpowers/sdd/2026-11-03-restante-r1-coop-modos/`)

- **Pacto pausa como a carta**: `EstadoPartida.pactoAberto` → `pausadoPorCarta` (só solo, como a carta); `InimigoSystem`/
  `ChefeSystem` cancelam projéteis/explosões/discos. **Maldições**: todo pacto com maldição conta em `modificadores.maldicoes`
  e na conquista "Walking Curse". **Borda da grade**: `InimigoSystem.bordaMutacao` em `noRaio`.
- **Prioridade de chefe**: `Config.PrioridadeChefe` (true) / `PrioridadeChefeRaioFrac` (0.8); `InimigoSystem.alvoGolpe` (contador
  `vivosChefesPrio`: guardião/marco/final, mini fora) usado pelo `GolpeSystem` em projétil, cone, área no alvo, linha e cadeia.
- **Modo na sala co-op**: `Logica/Sala.modo?` (ausente = clássico), `Types.SalaInfo.modo`, `Config.OrdemModos`; mesmo remote
  `SalaConfig` da dificuldade (líder, rate-limit, `UpdateAsync` + `propagar`); `Telas/Coop` botão "Mode: X" cicla Classic/Survival/
  Daily Mutation, Mutação = "Normal (fixed)"; TeleportData do grupo leva `modo`; Partida `CoopSystem.modoSala()` manda em sala
  (`difSala` no clássico/Survival); Qa `coopModo <n> <modo>`. Ranking coop `CoopTempo` só grava vitória no Clássico sem mutação.
- Revisão: 0 importantes, 8 menores (3 fechados na Task 0 do R2). `Shared` e `TesteSala` idênticos nos 2 places. **Nada salvo**.

### R2 — estatísticas por herói + nível de conta, perfil v8 (2026-11-03, agentes; plano
`docs/superpowers/plans/2026-11-03-restante-r2-stats-nivel-conta.md`, ledger `.superpowers/sdd/2026-11-03-restante-r2-stats-nivel-conta/`)

- **Shared**: `Types` (`EstatisticasHeroi`, `ContaPerfil`, `Perfil.porHeroi`/`conta`, `FimPartidaInfo.contaXp/contaNivel/contaSubiu`,
  `InfoConquista.texto?`), `Config.Conta*` (XpBase 100, XpPorNivel 50, XpPorMinuto 2, XpPorAbates 25, XpSemente 30,
  EssenciaPorNivel 10, NivelMax 100), `Logica/Perfil` **VERSAO 8** (migração v7→v8: porHeroi validado, `conta.xp` semeado por
  partidas 1×), `Logica/Conta` (novo, puro: `xpParaSubir`, `nivel`, `progresso`, `xpDaPartida`).
- **Partida**: `PartidaSystem.registrarConta` no `terminar` (stats do herói: partidas/vitórias/abates/tempo/melhorNivel/melhorZona
  clássico+mutação/melhorSurvival; XP de conta; nível subiu → +Essência e toast "Account level N! +E Essence" com `texto` direto na
  fila do `ConquistaController`); `FimController` "Account XP +N · Level L (· Level up!)"; Qa `conta [xp]`; `TesteLogica` v8 + Conta.
- **Menu**: Home "Lv N" + barra de progresso sob o nome (evento `Perfil`); `Telas/Herois` bloco "MY STATS" 4×2 do herói
  selecionado (Runs, Wins, KOs, Time played, Best level, Best zone, Best survival).
- Task 0 do R1: proteção do pacto só em co-op; comentário de maldições em `Types`; `TesteSala` +3 casos.
- Revisão: 0 importantes, 7 menores (tradução no lote final; Essência de nível no "bonus"; linha "Account XP" apertada).
- **Perfil v8: publicar os 2 places JUNTOS.** Nada salvo.

### R3 — menores acumulados (2026-11-03, agente; ledger `.superpowers/sdd/2026-11-03-restante-r3-menores/`)

- `InimigoSystem`: `raioMaxChefe` (8, calculado 1× das definições) + contador `vivosChefes` (inclui mini); `noRaio`/`maisProximoXZ`
  só alargam a varredura quando há chefe vivo (bug antigo: chefe na célula vizinha escapava de golpes de área). `FimController`:
  linhas da conta/Essência/Combo/Play Again descidas ~0.01; "Level up! +E Essence" na linha da conta e `extra` sem a Essência de
  nível. `QaSystem.conta` recusa inf/negativo. `Testes/TestePerfilConta` (novo, idêntico nos 2 places; `TesteLogica` dos 2 chama).
  Menu `Telas/Home`: "Lv N" com largura 0.14 e fonte mínima 11 px.
- Não feitos (decisão do Diego): quick match mostrar o modo (não há lista de salas; exigiria payload novo); botões do Room settings
  ≥ 36 px no celular (painel de 156 px não cabe 5 botões — refazer o painel).
- **Playtest 2 (agentes, `.superpowers/sdd/2026-11-03-playtest-2/`)**: Menu 0 importantes/2 menores; Partida 1 importante/5 menores.
  Corrigido: tela de fim (detalhes em caixa 0.6×0.07, texto "Time · KOs · Lv · Coins", sem sobreposição em nenhuma proporção);
  HUD do Survival mostra "Best survival m:ss" (`porHeroi.melhorSurvival`); `Qa mutacao` sobrevive ao Restart de run não-mutação;
  `formatarTempo` do Menu em h:mm:ss ≥ 1 h; ranking Mutation usa "Shrine" (`Zonas.final`) na zona 4. Os "+2 de Essência" no
  Survival eram a run anterior encerrada pelo Restart (não é bug). Textos novos em inglês listados nos relatórios (lote de tradução).
- Proposta da Região 2 (não implementada, aguarda o Diego): `docs/superpowers/specs/2026-11-03-regiao-2-proposta.md`.

## Mapas 2 e 3 (2026-11-04, agentes; spec `docs/superpowers/specs/2026-11-03-mapas-2-3-piratas-ki.md`)

Decisão do Diego (2026-11-03): mapa 1 ninja, **mapa 2 piratas** (clima One Piece), **mapa 3 guerreiros de ki** (clima Dragon Ball),
nomes/visuais nossos. "Região" no código = mapa. Claude segue sozinho até o jogo ficar pronto; PokeBonk como referência.

### Mapa 2 — Corsair Tides (lotes M2-A1/A2/B/C/D, ledgers `.superpowers/sdd/2026-11-03-mapa2-*`)
- **Dados/sistemas (A1)**: `Definicoes/Regioes` (ShinobiLands, CorsairTides: 4 zonas, desbloqueio = vencer o anterior, clima Vento
  +30%/Ki −25%, HP ×2,2/dano ×1,8), `Logica/Regiao`, `Zonas` com `regiao`/`nomeCurto` + `Porto`/`Naufragios`/`Recife`/`Bastiao`
  (X 20000/24000/28000/32000), 21 comuns (idx 22–42) + 9 chefes (110–118; Tide Emperor 3 fases), perfil **v9** (`regioesVencidas`,
  contadores `frutas`/`golpesCarregados`), conquistas Tide Breaker/Summit Champion/Fruit Taster/Full Charge, `EstadoPartida.regiao`,
  ZonaSystem por região, clima em `GolpeSystem.danoDe`, placares `_<regiao>`, Qa `regiao`/`regioes`.
- **Menu (A2)**: Prepare com cartões de mapa (cadeado "Unlock: clear …"; Survival/Mutação = "Shinobi Lands only"), sala com mapa
  (campo `mapa` da `Logica/Sala`, só líder e liberado), Leaderboard com coluna MAP, mapa ≠ padrão no solo em servidor reservado.
- **Terreno/cenário (B)**: Terrain em platôs (receita do Adendo 2), mar como Part, 6 meshes (casco, barril, palmeira, canhão, rocha
  com coral, farol), 1745 instâncias, climas por zona no `ZonaVisualController`, `Alturas` com filho `Alturas/CorsairTides` (limite
  de 200k do Source). Auditoria: 0 colisores, flood-fill 100%.
- **Modelos (C)**: 30/30 meshes gerados (assetIds no ledger; `KrakenAfogado` gerado no M2-D, asset 94294798480004).
- **Revisão A1/A2**: 2 importantes (semente do mapa 1 em todo load; "Village Cleared" no Porto) + 7 menores → corrigidos no M2-D.
- **M2-D**: Strange Fruit (`Definicoes/Frutas`, objeto `FrutaEstranha` com `regioes = {CorsairTides}`, 2 por zona fora do teto,
  molde `Moldes/Objetos/FrutaEstranha`; `FrutaSystem` novo: poder de 45 s no relógio da partida, chip na HUD, aura no sprite pelo
  atributo `Fruta`, Flame Fist ×1,35 Ki no `GolpeSystem.danoDe`; Rubber Body `imunePushback` sem efeito — não existe empurrão no herói)
  + correções I1/I2/m1–m4, Qa `danoChefe <frac>`/`fruta <id>`/`frutas` (Partida) e `Qa` mínimo no Menu (`vencer`/`essencia`/`perfil`),
  música do mapa 2 (`Sons.musicaPorto/...`, AudioController por id), contorno do chefe por fase (`Config.ChefeFaseCores`),
  `Regioes.multXp` (mapa 2 ×1,5 no XP dos comuns), Deck Swab só Porto / Thunder Eel só Recife. Ledger `2026-11-03-mapa2-d-fruta-revisao`.

- **Revisão M2-D**: 1 importante (nomes "Strange Fruit"/"Rubber Body"/"Flame Fist" juntos lembravam One Piece → exibição vira
  "Tide Fruit"/"Slick Skin"/"Ember Knuckle", chaves internas iguais; spec atualizada) + 5 menores → Task 0 do M3-D.

### Mapa 3 — Warrior's Summit (lotes M3-A1/A2/B/C/D, ledgers `.superpowers/sdd/2026-11-04-mapa3-*`)
- **Dados/sistemas (A1)**: `Regioes.WarriorsSummit` (ordem 3, libera vencendo CorsairTides, clima Ki +30%/Vento −25%, HP ×3,6/dano ×2,8,
  multXp 2, `mecanica = "carga"`), zonas `Torneio`/`Deserto`/`Planeta`/`Arena` (X 40000/44000/48000/52000), 21 comuns (idx 43–63),
  9 chefes (119–127; Tyrant Ascended 3 fases), campo novo `Chefes.furia { vida, multVel, multDano }` aplicado no `ChefeSystem`
  (Enforcer 50% vel ×1,3; Tyrant Ascended 66% vel/dano ×1,3 = "transformação"), `Alturas` com 12 zonas, "Summit Champion" possível.
  Testado até a vitória. Revisão A1: 0 importantes / 5 menores → M3-D.
- **Menu (A2)**: Shared replicado (hash), 3 cartões no Prepare (+ "Coming soon"), miniaturas 🥊🏜️🪐🏟️, sala/Leaderboard já por `Regioes`.
- **Terreno/cenário (B)**: Terrain em platôs (Torneio com ringue/arquibancadas, Deserto com mesas/naves caídas, Planeta com lagoas
  verdes/rochas flutuantes, Arena como disco nas nuvens), 6 meshes, `Alturas/WarriorsSummit` (filho), 1676 instâncias
  (`Mapa` = 5983), climas por zona. Auditoria: 0 colisores, flood-fill ≥ 99,6%.
- **Modelos (C)**: 30/30 meshes gerados (lotes de 3 por "Too Many Requests"); assetIds no ledger.
- **M3-D**: Energy Charge (`Config.Carga*`, estado no `HeroiSystem`, consumo só no golpe automático do herói no `GolpeSystem`, aura +
  barra + "Charged!" no cliente, Qa `carga`), fúria também no dano de contato + sinal laranja, frutas renomeadas (Tide Fruit / Slick Skin
  {Evasao 0.20, HpMax 0.15} / Ember Knuckle / Tide Step), músicas placeholder do mapa 3, luzes do Torneio 12, Unstable Core terrestre.
  Revisão: 0 importantes / 5 menores (m1 corrigido inline). Shared idêntico nos 2 places (42 módulos).
- **Tradução pt-BR final** (`.superpowers/sdd/2026-11-04-traducao-final/`): `PtBr` 1079 → **1344 pares** (+265: mapas 2/3, frutas,
  carga, Survival/pactos/mutações, stats/conquistas, textos fixos, placeholders `{1}`, dicas de teclas), idêntico nos 2 places; textos
  montados com poucos valores viraram pares fixos (pacto/fruta/mapa novo = par novo); controllers só na montagem do texto. **Sobrou em
  inglês**: textos fixos do Menu dependem da tradução automática do Roblox (controller antigo — decisão do Diego), avisos montados no
  servidor (`ObjetoSystem`/`DiretorSystem`/`BauSystem`/`MercadorSystem`), descrição gerada dos golpes, "ULT"/"DPS"/"HP"/"EXP"/"BETA",
  itens "+8% XP", decimais com ponto. Conferir no publicado com conta em português.
- **Playtest final** (`2026-11-04-playtest-final/`): Partida 0 importantes / 5 menores; Menu 0 importantes / 4 menores — todos de texto
  ou QA. **Ajustes finais** (`2026-11-04-ajustes-finais/`): `qaRegiao` consumido no Survival/Mutação, +47 pares no `PtBr` (1391; carta,
  pausa, 13 descrições geradas de golpes, telas do Menu), `CartaUI`/`PausaController`/`MenuController`/`Home`/`Herois` traduzindo na
  montagem, "Best zone" em chip duplo legível, decimais com vírgula na tela Mutação; Afterimage e toast do pacto confirmados ok.

### Pausa com loja e lista de objeto abertas (2026-11-04, agentes; ledger `.superpowers/sdd/2026-11-04-pausa-loja-objetos/`)

- Decisão do Diego: como no PokeBonk, abrir a **loja do mercador** ou a **lista de escolha de objeto** congela o jogo **no solo**
  (co-op não pausa; baú não tem tela; mapa grande/configurações ficam sem pausa).
- `EstadoPartida.lojaAberta`/`escolhaAberta` somados em `atualizarPausa()`; `MercadorSystem` com `abertas[player]` (separado de
  `ofertas`), remote novo **`FecharLoja`** (c→s, sem payload, sem rate-limit), `aoComprar` com `emAndamento` + exige `abertas`;
  `ObjetoSystem` com `atualizarPausa()`/`fecharOfertas()`, proteção `ObjetoProtecaoEscolha` só no co-op; `InimigoSystem`/`ChefeSystem`
  cancelam pendências com os flags novos; `PartidaSystem` zera; Qa `loja`/`pausa`. Cliente: `LojaController.fechar(avisarServidor)`,
  Esc fecha a lista de objeto (`ObjetoController`), `PausaController` não abre por cima. `Shared` intacto (Menu não mudou).
- Revisão: 0 importantes / 4 menores, todos corrigidos. **Nada salvo** (só Partida mudou).

### Menores finais + Menu com tradução nova + Room settings (2026-11-04, agentes)

- **Menores finais (Partida)** (`.superpowers/sdd/2026-11-04-menores-finais/`): triagem de 73 menores das revisões de 11-03/04
  (`pendencias.md`): 59 já fechados, 2 corrigidos (`PactoSystem.oferecer` zera reenvio pendente da oferta anterior; `TesteLogica`
  +3 checks da carga), **9 pra decisão do Diego** (lista com recomendação no ledger: Endless aos 45:00 junto do marco 5, giro sem
  suavização, Time played de quem entra no meio, vitória no mapa 2/3 conta pra desbloqueios, teste da fúria, Golden Tyrant vel 7,
  ×2 da carga em golpes com ticks, teleporte zera carga, luzes Porto/Planeta). Revisão 0 importantes.
- **Menu** (`.superpowers/sdd/2026-11-04-menu-traducao-lobby/`): decisão do Diego (revoga a de 11-03) — o Menu usa o
  `LocalizacaoController` novo (cópia byte a byte do Partida; traduz todo TextLabel/TextButton por dicionário + `formatar`); textos
  fixos de todas as telas em pt-BR (sobra: nomes próprios, teclas desenhadas, placeholders de TextBox do Clã); `PtBr` +1 par (PLAY),
  idêntico nos 2 places (1392 pares). **Room settings** refeito (`Telas/Coop`): botões 36,6 px em 844×390 / 60,9 px em 1625×650.
  Ranking: troca rápida de aba agenda 1 reenvio por placar em vez de perder o pedido (`MenuController.pedirRanking`). Revisão
  0 importantes / 5 menores (1 aplicado). Não feito (decisão): Quick match mostrar o modo.

### Tarde de 2026-11-04 — menores do Menu, loja em pt-BR, playtest de regressão (agentes)

- **Menu** (`.superpowers/sdd/2026-11-04-menu-menores/`): reenvio do ranking prioriza a aba visível; título/dica do Room settings
  com piso 18/12 px; placeholders das TextBox do Clã traduzidos (`Telas/Cla.traduzirPlaceholders`).
- **Loja em pt-BR** (`2026-11-04-loja-ptbr/`): `LojaController.traduzirItem` (nome "+1", "Move level N → M", preço, SOLD) +
  9 pares no `PtBr` (1401; "Close", "<Raridade> item"), idêntico nos 2 places.
- **Playtest de regressão** (`2026-11-04-playtest-regressao/`): Partida 0 importantes / 5 menores (botão II por cima da loja →
  corrigido no `PausaController`; loja em inglês → lote acima); Menu 0 importantes / 4 menores, todas as telas em pt-BR sem resíduo.
- Warn a conferir no publicado: `[Icone] asset não carregou: rbxassetid://138913147755289`.

### Anotações do Diego de 2026-11-05 (inline, só o place Menu; `Shared` intocado)

- **Título das telas reto**: `MenuController.cabecalho` — `faixa.Rotation` de -1 pra 0.
- **Ranking**: no bloco que pinta as abas (`MenuController`, ~l. 823–846) o botão selecionado ganha `ZIndex = 2` (os outros 1)
  nas 5 filas (placar, mapa, modo, dificuldade, dia), pra ficar por cima dos vizinhos.
- **Cartão Daily Mutation da Home**: o zoom do hover (UIScale do `Juice`) refazia a quebra de linha do texto
  (`TextScaled` + `TextWrapped`). `Telas/Home` ganhou `linhasFixas`: o rótulo original fica escondido (recebe a tradução) e
  um espelho sem `TextWrapped` mostra o texto com quebra fixa (título e sub do cartão).
- **Emblema de clã: ADIADO pelo Diego (2026-11-05)**. Sem desenho livre (desenho compartilhado é "free-form user creation"
  na política do Roblox e restringe a idade do público). Quando houver mais personagens, o emblema vai usar a carinha dos
  nossos personagens, como no PokeBonk; o Diego vai criar os modelos próprios dos personagens mais tarde.

### Co-op: tela de entrada e sala no fluxo do PokeBonk (2026-11-05, agentes; plano `docs/superpowers/plans/2026-11-05-coop-sala-redesign.md`,
ledger e revisão em `.superpowers/sdd/2026-11-05-coop-sala-redesign/`)

Desenho aprovado pelo Diego (artifact "Telas Co-op AnimeBonk"). Implementado e revisado por leitura; **nada rodou em Play e
nada está salvo** — o Diego testa, dá Ctrl+S e publica os 2 places juntos (o `Shared` mudou nos dois).

- **Tela Co-op** (`Telas/Coop.construirCoop`): "With friends" (Create room cria na hora + Join with a code) e "Quick match"
  (chips Any/Duo/Trio/Squad + Find match + "N searching now"). Saiu o rodapé Your hero / Change hero.
- **Sala** (`Telas/Coop.construirLobby`): Destination (mapa, modo, dificuldade com setas, só o líder), Your team (4 cartões
  com retrato, selos Host/You/Change, Ready/Choosing…), Room code + Open slots (Off/On, Duo/Trio/Squad), barra de baixo com
  um botão só (líder Start!, demais I'm ready!/Not ready) e o motivo do bloqueio.
- **Servidor** (`SalaSystem`): `SalaCriar` só usa `heroiId` (sala nasce privada, `Sala.MAX` vagas, destino padrão);
  `SalaIniciar` exige `Config.SalaMinJogadores` (2). `Logica/Sala.configurar` só zera o pronto quando muda mapa, modo ou
  dificuldade (vagas não zeram). `PtBr` ganhou 30 pares e 6 chaves. `TesteSala` atualizado (não executado).
- **Pós-revisão (inline)**: `Telas/Coop.pedir` virou janela por remote com reenvio do último pedido (cliques dentro do
  rate-limit do servidor não somem mais); Create room dentro dos 10 s avisa "Please wait a moment."; a contagem do Quick
  match marca a janela do `SalaBuscar` pra não derrubar o Find match.
- **Não feito**: cadeado por membro (mapa/dificuldade que um convidado não desbloqueou travar o início e mostrar o nome).
  As salas ficam no MemoryStore e os membros podem estar em outros servidores do Menu; continua valendo o perfil do líder.
  Precisa gravar os desbloqueios de cada membro na sala (`Logica/Sala` + `Types` nos 2 places) — decisão do Diego.
- **Menores abertos da revisão** (`review.md`): sala expirada deixa a tela presa (anterior ao lote); pronto zerado quando o
  líder reenvia o mesmo valor; controles inativos ainda animam no clique; alvos de toque pequenos no celular ("Change");
  busca de nome repetida; lacunas no `TesteSala`.

## Como retomar (atualizado em 2026-11-04, madrugada — JOGO "PRONTO" v1 com 3 mapas)

- **Primeiro**: Ctrl+S e publicar os 2 places JUNTOS (Shared mudou muito nos dois; perfil **v9**; mapas 2 e 3, PtBr 1401 pares;
  pausa com loja/lista de objeto no Partida; Menu com tradução nova + Room settings).
  Nada do que foi feito em 2026-11-03/04 está salvo até isso.
- **O que o Diego precisa testar no publicado** (o MCP não alcança): prompts E (altar, baú, mercador, Tide Fruit "Eat", Revive),
  teleportes reais (Menu→Partida nos 3 mapas e modos; servidor reservado pra Survival/Mutação/mapas 2–3; Partida→Menu), sala com 2
  contas (modo/mapa do líder, cadeado), AutoLocalize dos textos fixos do Menu com conta em português, aparência (terreno, cenário e
  modelos dos mapas 2 e 3 — frente dos modelos: ajustar `GiroY` se vier de lado; emojis das miniaturas do Prepare), áudio das músicas
  placeholder, FPS nos mapas novos, celular.
- **Decisões/balanceamento do Diego** (tudo em `Config`/`Definicoes`): multiplicadores dos mapas 2/3 (HP ×2,2/×3,6, dano ×1,8/×2,8,
  XP ×1,5/×2), frutas (2 por zona, 45 s), Energy Charge (1,5 s, ×2; golpes que teleportam zeram a carga), Endless Night, prioridade de
  chefe, nomes/ícones de itens e dos 42 inimigos/18 chefes novos, músicas definitivas, luzes do Porto (24) e Planeta (16).
- **Menores abertos** (listados nos `review.md`/`playtest-*.md` de 2026-11-03/04): nenhum importante aberto.
- **Como o código está organizado agora**: `Definicoes/Regioes` (3 mapas: zonas, clima, multiplicadores, desbloqueio, mecânica),
  `Logica/Regiao`, `Zonas` com `regiao`, `Mapa/Alturas` + filhos por mapa, `FrutaSystem`, Energy Charge no `HeroiSystem`/`GolpeSystem`,
  Qa (Partida: `regiao`, `regioes`, `danoChefe`, `fruta`, `frutas`, `carga`, `endless`, `marco`, `mutacao`, `conta`, `coopModo`…;
  Menu: `vencer`, `essencia`, `perfil`).

### Histórico anterior (parado em 2026-10-29)

- Etapas 1 e 2 **concluídas, revisadas e testadas em Play** no place Partida
  (108221889486707). Ledgers com decisões e ajustes menores pendentes:
  `.superpowers/sdd/2026-10-29-etapa1-partida-minima/progress.md` e
  `.superpowers/sdd/2026-10-29-etapa2-zonas-chefes/progress.md`.
- 2026-10-29: etapa 3 dividida em 3a/3b/3c (decisão do Diego). **Etapa 3a implementada**
  (heróis Kaizo e Haruto, kit de 4 golpes pros 3, tela de escolha de herói) — plano
  `docs/superpowers/plans/2026-10-29-etapa3a-herois.md`, testada em Play pelo Claude.
- 2026-10-29: **etapa 3b implementada** (Pergaminhos completos + Cursed, raridade, moedas,
  baús, mercador) — plano `docs/superpowers/plans/2026-10-29-etapa3b-pergaminhos-economia.md`.
  Diego autorizou o Claude a decidir design sem perguntar nesta sessão.
- 2026-10-29: **etapa 3c implementada** (22 itens, status, reações, elemento nos golpes) —
  plano `docs/superpowers/plans/2026-10-29-etapa3c-itens-status-reacoes.md`. Etapa 3 completa.
- 2026-10-29: **etapa 4 (co-op no place Partida) implementada** — hordas/teto/chefe por
  jogador, caído + reviver segurando E, minors de co-op. Plano
  `docs/superpowers/plans/2026-10-29-etapa4-coop.md`. Só testada solo pelo Claude.
- 2026-10-29: **etapa 5a implementada** (perfil DataStore + Essência) — plano
  `docs/superpowers/plans/2026-10-29-etapa5a-perfil-essencia.md`.
- 2026-10-29: **etapa 5b implementada** (place Menu com layout do PokeBonk, seleção de herói
  com desbloqueios, teleporte Menu → Partida com o herói, Kaizo/Haruto desbloqueáveis) —
  plano `docs/superpowers/plans/2026-10-29-etapa5b-menu.md`. Teleporte não testado (só
  publicado).
- 2026-10-29: **etapa 5c implementada** (Dojo de Treino: 6 melhorias permanentes com Essência
  no Menu, bônus aplicados no herói no Partida; perfil schema v2) + correções da revisão final
  da 5b — plano `docs/superpowers/plans/2026-10-29-etapa5c-dojo.md`. Compra com Essência real
  não testada no Studio (perfil em memória com 0 Essência).
- 2026-10-29: **etapa 6a implementada** (ultimates na tecla R/botão touch com 3 versões, despertares
  nv 20/40 com cor/aura e stats) + correções da revisão final da 5c (Dojo recusa compra durante
  teleporte e com perfil somente leitura) — plano
  `docs/superpowers/plans/2026-10-29-etapa6a-ultimates-despertares.md`.
- 2026-10-29: **etapa 6b implementada** (13 conquistas com Essência e desbloqueio de Kaizo/Haruto,
  ranking OrderedDataStore no Menu, tela de configurações no Menu e no Partida; perfil schema v3) +
  correções da revisão final da 6a (ultimate não recarrega a si mesma, callback direto) — plano
  `docs/superpowers/plans/2026-10-29-etapa6b-conquistas-ranking.md`. **Publicar Menu e Partida juntos**
  (Partida v2 lendo perfil v3 não salva).
- 2026-10-29: **etapa 6c implementada** (tarefas diárias com streak, tradução pt-BR automática, sprites
  compostos/partículas/clima por zona; perfil schema v4) + correções da revisão final da 6b (perfil travado
  no teleporte, config pendente no rate-limit) — plano
  `docs/superpowers/plans/2026-10-29-etapa6c-tarefas-traducao-visual.md`. **Publicar Menu e Partida juntos**
  (Partida v3 lendo perfil v4 não salva).
- 2026-10-29: **etapa 7 implementada** (clãs: fundar com Essência, nome/sigla/emblema, entrada aberta/pedido/convite,
  cargos, pontos de clã no fim da partida, ranking e 5 telas no Menu; perfil schema v5) + correções da revisão final
  da 6c — plano `docs/superpowers/plans/2026-10-29-etapa7-clas.md`. **Publicar Menu e Partida juntos.**
- 2026-10-30: **modo de dificuldade** (Normal/Hard/Nightmare, desbloqueio por vitória, seletor no Menu e no Partida).
- 2026-10-30: **skins** (3 por herói, compra/equipar no Menu, cor no Partida; perfil schema v6) + correções da revisão
  final do lote Mobs + Kaizo renomeado (Sea Rogue / Kinetic Guard). **Publicar Menu e Partida juntos.**
- 2026-10-30: **áudio placeholder + juice** (sons da Creator Store por id, SoundGroups, música por zona, feedback visual em
  botões/cartas/combo/fim). **Publicar Menu e Partida juntos** (Shared mudou nos 2).
- **Próximo passo:** roadmap v1 implementado; falta arte final (sprites; áudio definitivo no lugar dos placeholders) e
  os testes manuais/publicados listados (teleporte, DataStore, clãs com 2 contas, tradução pt-BR, prompts).
- **Pendente do Diego ao voltar**: salvar/publicar os places Partida **e Menu** (testar o
  teleporte Menu → Partida publicado); testar manualmente
  baú, mercador, itens/status/reações, co-op com 2 clientes, Essência na tela de fim;
  ligar "Enable Studio Access to API Services" pra testar o DataStore no Studio.
- Ideia anotada (não decidida): golpes com prioridade de alvo no chefe quando ele
  estiver no alcance (hoje miram o inimigo mais próximo).
- Ajustes menores adiados pra etapa de co-op: alocações por frame (`HeroiSystem.vivos()`,
  `InimigoSystem.infoChefes()`, `XpSystem.coletar`), teto/spawn por jogador, herói
  caído recebendo snapshot/oferta.
- Diego autorizou o Claude a testar com Play nas etapas (2026-10-29).
- Studio: abrir os places com uma conta que tenha permissão de edição na experiência
  e ligar o MCP (Assistant → Manage MCP Servers → Enable Studio as MCP server).

## Pendências anotadas

- Etapa 1 implementada (2026-10-29) no place Partida, revisada e corrigida; falta o
  teste manual do Diego. 12 ajustes menores anotados em
  `.superpowers/sdd/2026-10-29-etapa1-partida-minima/progress.md` (linhas "minor").
- Criar o grupo do Roblox e a experiência (2 places: Menu e Partida) e registrar IDs aqui.
- Criar o(s) place(s) e registrar placeIds aqui.
- FEITO 2026-11-05: repositório privado `DiegoFeBrandao/AnimeBonk` (documentação e arte; o código segue nos places),
  pro desenvolvimento em dupla. Sem hook de auto-push: as regras de pull antes de mexer e push ao fim de cada feature
  estão no `CLAUDE.md` (seção Git / GitHub).
