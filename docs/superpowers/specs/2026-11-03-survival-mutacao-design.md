# Survival e Mutação do Dia — design (2026-11-03)

**Pedido do Diego**: "faz o resto; segue sempre o Megabonk e o PokeBonk, principalmente o PokeBonk, como eles funcionam".
Diego pulou as perguntas: tudo abaixo que não é regra explícita dele é **decisão minha (Claude)**, marcada [C]. Referências:
`docs/pokebonk-referencia.md` §3 (Sobrevivência), §5 (Mutação do Dia), §15; `docs/megabonk-referencia.md` (Final Swarm, tetos).

## Intenção
Dois modos novos no mesmo place Partida, escolhidos no Menu, que reaproveitam tudo da run Clássica (heróis, golpes, cartas,
itens, objetos, chefes, co-op no mesmo servidor):
- **Survival (Sobrevivência)**: run infinita numa zona só, com marcos de chefe por tempo, pactos (bônus + maldição) e ranking por
  tempo sobrevivido. Substitui o cartão "Survival · Coming soon" da Home.
- **Mutação do Dia (Daily Mutation)**: a run Clássica com uma regra modificadora que gira a cada 24 h (UTC), dificuldade fixa,
  mesma semente de objetos pra todos, ranking do dia por progresso e trilha de recompensa em Essência.

Não-objetivos (ficam pra depois): eventos de temporada, títulos/molduras/fundos de perfil, Survival em sala co-op pelo Menu
(salas continuam Clássico), tradução dos textos novos (lote de tradução no fim do projeto — textos em inglês).
Anti-objetivo: run infinita sem teto (Megabonk aprendeu: Noite Sem Fim precisa apertar até matar o jogador).

## Como o modo viaja (os dois modos)
- `Types.PedidoHeroi` e `Types.DadosTeleporte` ganham `modo: string?` (`"classico"` padrão, `"sobrevivencia"`, `"mutacao"`).
  `Shared/Definicoes/Modos` (dado): id, `name`, descrição curta, `dificuldadeFixa?`.
- Menu: `MenuSystem.aoIrParaPartida` valida o modo (existe; mutação força `Config.MutacaoDificuldade`) e põe no TeleportData.
- Partida: `PartidaSystem.heroiDoTeleporte`/`aoEscolherHeroi` validam; **quem começa a partida define o modo do servidor**
  (igual à dificuldade); quem entra depois segue o modo atual. `EstadoPartida.modo` + `EstadoPartida.defModo()`.
- `FimPartidaInfo.modo` pra tela de fim; remote `Zona` ganha `modo` e `mutacao` (id) pra HUD.
- Co-op no mesmo servidor funciona nos dois modos (sem mudança nas salas).

## Survival [C, seguindo PokeBonk §3]
- **Mapa**: só a zona 1 (Vila Shinobi), sem altar, sem portal, sem mini-chefe por tempo da zona. Relógio da zona **sobe**
  desde 0:00 (HUD mostra o tempo sobrevivido; "Zona 1/3" vira "Survival").
- **Marcos** (`Config.SurvivalMarcos`, segundos → chefe): 5:00 Great Toad Elder, 10:00 White Serpent, 15:00 Nine-Tailed Fox,
  30:00 Giant Slug, 45:00 Sealed Demon. Depois de 45:00, **Endless Night**: um guardião sorteado a cada 5 min. O chefe nasce
  perto do grupo (como o mini-chefe), com aviso "Milestone boss!" (remote `Evento`). Vida do chefe = vida da definição ×
  `ChefeHpMult` × multiplicador do marco (`Config.SurvivalMultHpMarcos` = { 1, 1.6, 2.4, 3.2, 4 }, depois +0.5 por chefe da
  Endless Night) × dificuldade × jogadores extras.
- **Pressão contínua**: comuns com vida ×(1 + `Config.SurvivalHpPorMinuto` × min) e spawn ×(1 + `Config.SurvivalSpawnPorMinuto`
  × min, teto `Config.SurvivalSpawnMax`); chance de elite +`Config.SurvivalElitePorMinuto`/min. Dificuldade escolhida (Normal/
  Difícil/Pesadelo) multiplica por cima. Endless Night: além disso, inimigos +10% de velocidade a cada 5 min (teto 1.6) —
  teto anti-run-infinita, à la Megabonk.
- **Pacto** depois de cada chefe de marco: lista de 3 pactos (`Shared/Definicoes/Pactos`, 10 pactos) pela UI de escolha que já
  existe (`EscolhaObjeto`/`EscolherObjeto`, título "Choose a pact"), **sem cancelar** (Cancel recusado: tem que escolher). Cada
  pacto = bônus forte no herói + maldição permanente na run. Exemplos: "Blood Oath: +40% damage / −30% max HP";
  "Iron Skin: +50% max HP / −20% move speed"; "Greed: ×2 coins / enemies +25% HP"; "Swift: +25% attack speed / enemies +15%
  speed"; "Magnet: +60% pickup range / −20% XP"; "Berserk: +30% crit / take +25% damage". Em co-op, cada jogador escolhe o seu;
  maldições de inimigo somam em `EstadoPartida.modificadores`. Bônus pelo `e.bonus` do herói (mesmas chaves do Dojo).
- **Fim**: só por derrota (todos caídos/mortos) ou Give up. Tela de fim: título "SURVIVED" com o tempo grande em vez de
  DEFEAT; "Essence +N" = `Perfil.essenciaDaPartida("derrota", …)` + `Config.SurvivalEssenciaPorMinuto` × min (teto 60 min);
  ranking **`SurvivalTempo`** (OrderedDataStore, segundos inteiros, maior melhor; desempate não implementado — Roblox só ordena
  um número). Co-op: quem caiu volta depois do próximo chefe de marco (`HeroiSystem.renascerMortos`).
- **Menu**: cartão "Survival" da Home vira botão real (`modoSel = "sobrevivencia"`) → tela de heróis → Preparar (mostra "Mode:
  Survival", dificuldade escolhível) → Começar. Ranking: aba "Survival" no Solo (Best time survived).
- **QA**: `Qa modo sobrevivencia` antes de escolher herói; `Qa marco` força o próximo marco agora.

## Mutação do Dia [C, seguindo PokeBonk §5]
- **Rotação**: `dia = floor(os.time() / 86400)` (UTC); mutação = `Mutacoes.ordem[(dia % n) + 1]`. Dificuldade fixa
  `Config.MutacaoDificuldade = "Normal"`. Mapa Clássico inteiro (4 zonas + chefe final).
- **Mutações** (`Shared/Definicoes/Mutacoes`, 7, dado): id, `name`, `descricao`, efeitos opcionais: `multHpInimigos`,
  `multDanoInimigos`, `multSpawn`, `multVelInimigos`, `escalaInimigos` (tamanho do sprite), `multDanoHeroi`, `multHpHeroi`,
  `multMoedas`, `multXp`, `chefesIgnoram` (padrão true: guardiões não mudam). Lista inicial: Giant Wilds (×2 tamanho, ×2 HP,
  +50% dano, −15% vel), Glass Cannon (herói ×2 dano, ×0.5 HP), Swarm Night (spawn ×2, HP ×0.6), Golden Hour (moedas ×3,
  XP ×0.7), Speed Demons (vel +40%, HP ×0.7), Thick Skin (inimigos dano ×0.6, HP ×1.6), Scholar's Day (XP ×1.6, moedas ×0.5).
- **Semente fixa**: `EstadoPartida.semente = dia` → `ObjetoSystem` e sorteio de baús/tier das pedras usam `Random.new(dia)`
  (mesmo mapa pra todos no dia). Inimigos/cartas continuam aleatórios (PokeBonk também não fixa tudo).
- **Ranking do dia**: OrderedDataStore **`Mutacao_<dia>`**, valor = `zonaAlcancada × 1_000_000 + min(abates, 999_999)`
  (vitória = zona 5). Grava a melhor do dia (OrderedDataStore `UpdateAsync` só sobe). Menu: aba "Daily Mutation" (Hoje / Ontem).
- **Trilha de recompensa** (uma vez por dia, perfil **v7**: `mutacao = { dia: number, marcos: { [string]: boolean } }`, zera
  quando o dia muda): Zona 2 +30, Zona 3 +60, Santuário +100, Vitória +200 Essência (`Config.MutacaoPremios`). Toast
  "Daily Mutation: Zone 2 reached (+30 Essence)" pelo remote `Conquista` (mesmo caminho dos toasts).
- **Menu**: cartão novo "Daily Mutation" na Home (3º da fila Co-op / Survival / Daily Mutation) → tela `Mutacao`: nome e
  descrição da mutação de hoje, efeitos em chips, "Rotates in HH:MM", próximas 2 ("Tomorrow: …", "In 2 days: …"), melhor
  resultado de hoje (perfil), PLAY (→ heróis → Preparar sem botões de dificuldade, "Mode: Daily Mutation · Normal").
  HUD da Partida: chip da mutação ao lado do nome da zona.
- **QA**: `Qa modo mutacao [id]` força a mutação antes de escolher herói.

## Restrições
- Tudo é dado em `Shared/Definicoes` + `Config`; sistemas leem definições (sem `if modo == …` espalhado além do ponto de entrada).
- Servidor autoritativo: modo/mutação/pacto validados no servidor; o cliente só pede índice.
- `Shared` idêntico nos 2 places (Types, Config, Definicoes/Modos, Mutacoes, Pactos, Logica/Perfil v7 com migração).
- Pool/tetos existentes valem (`InimigosMaxVivos`, projéteis); Survival não cria sistema novo de spawn.
- Textos em inglês; PtBr só no lote final.

## O que fica pro implementador decidir
Posições exatas dos novos elementos de UI (seguir Tema/UiKit), números finos dos pactos/mutações (ficam no Config/Definicoes),
onde o chefe de marco nasce (reaproveitar `invocarMini`), ordem de aplicação dos multiplicadores no `aplicarMultiplicadores`.
