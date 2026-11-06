# Mapas 2 e 3 — "Corsair Tides" (piratas) e "Warrior's Summit" (guerreiros de ki) — Design (2026-11-03)

**Aprovado pelo Diego em 2026-11-03** ("escreva e faça, está tudo aprovado"): mapa 1 = Shinobi Lands (ninja), mapa 2 = clima de
piratas (inspiração One Piece), mapa 3 = clima de guerreiros de ki (inspiração Dragon Ball). Regra do `CLAUDE.md`: arquétipo sim,
marca não — nenhum nome de personagem, golpe, lugar ou termo registrado dessas obras; tudo abaixo é nosso. Dúvidas de mecânica:
seguir o PokeBonk (`docs/pokebonk-referencia.md` §Regiões: 3 zonas + santuário, libera vencendo a anterior, chefes próprios,
clima por região, sala escolhe mapa, ranking por mapa). Decisões marcadas [C] são do Claude.

## Conceito comum (vale pros 3 mapas)
- **"Região" no código = "mapa" pro Diego.** `Shared/Definicoes/Regioes` (novo): `{ id, name, descricao, ordem, zonas = {4 ids},
  desbloqueio = { tipo = "vencerRegiao", regiao = <id anterior> } | nil, clima = { bonus = elemento, malus = elemento } | nil,
  multHp, multDano, cor }`. `ShinobiLands` fica como está (padrão, sem desbloqueio, sem clima). `Zonas[id]` ganha `regiao`.
- **Posições no MESMO place Partida** [C]: mapa 2 em X 20000 / 24000 / 28000 / 32000; mapa 3 em X 40000 / 44000 / 48000 / 52000
  (Z = 0). Zonas 1–3 de 900×900, zona 4 de 480×480, como no mapa 1. Streaming já isola.
- **Clima** (PokeBonk): golpes do elemento `bonus` +30% de dano, do `malus` −25% (`Config.ClimaBonus/ClimaMalus`), aplicado no
  cálculo de dano do `GolpeSystem` pelo elemento do golpe; HUD mostra o chip do clima ao lado da zona. Mapa 1 sem clima.
- **Desbloqueio**: mapa 2 ao vencer o mapa 1 em qualquer dificuldade [C] (perfil ganha `regioesVencidas { [id]: true }`, perfil
  **v9**, migração: `ShinobiLands` = true se `estatisticas.vitorias > 0`); mapa 3 ao vencer o mapa 2. Mapa trancado aparece no
  Prepare com cadeado e "Unlock: clear <mapa anterior>".
- **Escolha**: Prepare match ganha seletor de mapa (cartões com nome, 4 zonas, guardiões, cadeado); sala co-op: o líder escolhe o
  mapa (mesmo padrão do modo/dificuldade, `SalaInfo.regiao`); `TeleportData.regiao`, `PedidoHeroi.regiao` validados no servidor;
  quem começa fixa `EstadoPartida.regiao`; quem entra segue. **Survival e Mutação do Dia continuam no mapa 1** nesta etapa [C].
- **Rankings** por mapa: placares existentes mantêm o nome pro mapa 1; os outros ganham sufixo `_<regiaoId>` (`MelhorTempo_CorsairTides`,
  `CoopTempo_...`, `MaisAbates_...`); Leaderboard ganha seletor de mapa.
- **Conquistas** novas por mapa: "Tide Breaker" (vencer o mapa 2), "Summit Champion" (vencer o mapa 3), "Fruit Taster" (comer 10
  frutas), "Full Charge" (50 golpes carregados).
- **Mini-chefes** = 4 comuns grandes por mapa (como hoje). **Guardião** 1 por zona + **chefe final** na zona 4 (3 fases), padrões
  com as formas que já existem (linha, leque, área, pulo/investida, invocar, chuva).
- **Objetos/baús/mercador** iguais ao mapa 1 (o `ObjetoSystem` sorteia por zona); cada mapa ganha **1 objeto próprio** (abaixo).
- Textos em inglês; ids em português; PtBr fica pro lote de tradução.

## Mapa 2 — **Corsair Tides** (piratas) · clima: bonus **Vento**, malus **Ki** [C] · HP ×2,2 / dano ×1,8 [C]
| # | id | Nome | Cenário | Guardião (padrões) |
|---|---|---|---|---|
| 1 | `Porto` | Driftwood Harbor | porto de madeira, docas, tavernas, barris, gaivotas, pôr do sol | **Dreadnought Captain** — salva de canhão (leque 7), âncora (área), investida |
| 2 | `Naufragios` | Shipwreck Graveyard | cascos encalhados, bancos de areia, névoa, correntes, caranguejos | **Drowned Kraken** — tentáculos (2 linhas), tinta (área grande), invoca Barnacle Crabs |
| 3 | `Recife` | Stormreach Reef | recife, mar bravo, raios, rochas pretas, chuva | **Thunder Leviathan** — mergulho (linha), chuva de raios, área elétrica, pulo |
| 4 | `Bastiao` | Admiral's Bastion (480×480) | fortaleza da marinha, canhões, bandeiras, farol | **Iron Admiral** (guardião) → chefe final **Tide Emperor** (fase 1 canhões em leque + área; fase 2 ≤ 66% invoca Ironclad Marines e acelera; fase 3 ≤ 33% chuva de canhão + redemoinho em área) |

Comuns (5 por zona; comportamentos existentes: perseguir, rápido, tanque, atirador, explosivo, invocador, marionete, clone,
teleporte; `soInvocado` onde indicado):
- Harbor: Deck Swab (perseguir), Musket Buccaneer (atirador), Barrel Brute (tanque), Rigging Monkey (rápido), Powder Keg Runner (explosivo).
- Graveyard: Drowned Sailor (perseguir, fantasma/voo baixo), Barnacle Crab (tanque, `soInvocado` pelo Kraken também no sorteio normal),
  Siren Caller (marionete → Drowned Sailors), Wreck Wisp (clone → 2 Wreck Echoes `soInvocado`), Harpoon Ghost (atirador).
- Reef: Storm Gull (rápido, voo), Thunder Eel (teleporte), Coral Hulk (tanque), Lightning Caster (atirador), Reef Mine (explosivo).
- Bastion: Ironclad Marine (tanque; também `soInvocado` pelo Emperor), Navy Sharpshooter (atirador), Shadow Corsair (teleporte),
  Cannon Loader (explosivo), Bosun Herald (invocador → Ironclad Marines).
- Mini-chefes: Harbor Boss (Barrel Brute), Crab King (Barnacle Crab), Storm Captain (Coral Hulk), Marine Commander (Ironclad Marine).
- **Objeto próprio: Tide Fruit** (`FrutaEstranha`, 2 por zona, prompt "Eat"): poder aleatório por `Config.FrutaDuracao` (45 s),
  1 por vez, chip na HUD: *Slick Skin* (evasão +20% + HP máx. +15%), *Ember Knuckle* (+35% dano Ki), *Tide Step* (+30% velocidade
  + coleta +50%). Dados em `Definicoes/Frutas`; reaproveita `bonusRun` temporário (aplicar/reverter) e o `ObjetoSystem`.
  (Nomes trocados em 2026-11-04 após revisão: "Strange Fruit"/"Rubber Body"/"Flame Fist" juntos lembravam One Piece; chaves
  internas continuam as mesmas.)

## Mapa 3 — **Warrior's Summit** (guerreiros de ki) · clima: bonus **Ki**, malus **Vento** [C] · HP ×3,6 / dano ×2,8 [C]
| # | id | Nome | Cenário | Guardião (padrões) |
|---|---|---|---|---|
| 1 | `Torneio` | Tournament City | cidade com arena, arquibancadas, lanternas, bandeirolas | **Grand Champion** — combo de socos (linha ×3), onda de choque (área), investida |
| 2 | `Deserto` | Wasteland of Invaders | deserto com naves caídas, crateras, mesas de pedra | **Invader Vanguard** — rajadas de energia (leque), bombardeio (chuva), invoca Scout Drones |
| 3 | `Planeta` | Crimson Planet | céu vermelho, água verde, rochas flutuantes, cristais | **Tyrant's Enforcer** — feixe (linha longa), área de ki, pulo, acelera a 50% |
| 4 | `Arena` | Sky Arena (480×480) | arena nas nuvens, pilares, raios de luz | **Golden Tyrant** (guardião) → chefe final **Tyrant Ascended** (fase 1 feixes + área; fase 2 ≤ 66% "transforma": cor muda, velocidade e dano ×1,3, invoca Elite Guards; fase 3 ≤ 33% chuva de esferas de ki + feixe gigante) |

- Comuns: Tournament City: Street Brawler (perseguir), Ki Archer (atirador), Iron Wrestler (tanque), Sprint Fighter (rápido),
  Firework Monk (explosivo). Wasteland: Scout Drone (rápido, voo, `soInvocado` + sorteio), Invader Trooper (atirador), Armored
  Crawler (tanque), Mirage Fighter (clone → 2 Afterimages), Signal Officer (invocador → Scout Drones). Crimson Planet: Blink Assassin
  (teleporte), Plasma Gunner (atirador), Crystal Golem (tanque), Energy Leech (perseguir), Unstable Core (explosivo). Sky Arena:
  Elite Guard (tanque; `soInvocado` pelo chefe também no sorteio), Ki Sniper (atirador), Phantom Duelist (teleporte), Overcharged
  Zealot (explosivo), Herald of the Tyrant (invocador → Elite Guards).
- Mini-chefes: Pit Champion, Crawler Alpha, Golem Colossus, Guard Captain.
- **Mecânica própria: Energy Charge** [C]: herói parado por `Config.CargaTempo` (1,5 s) acumula "carga" (aura dourada no sprite,
  anel na HUD); o próximo golpe sai com `Config.CargaMultDano` (×2) e consome a carga. Servidor decide (posição parada ≥ tempo),
  cliente só desenha. Vale só no mapa 3 (`Regioes.mecanica = "carga"`), ou em todos se ficar bom [C: só no mapa 3 por enquanto].

## Lotes (cada um com implementador + revisor; Diego testa e publica depois)
- **M2-A1** (Shared + Partida): `Regioes`, zonas/inimigos/chefes do mapa 2 como dados, clima, `EstadoPartida.regiao`, ZonaSystem
  por região, teleporte/pedido com `regiao`, perfil v9 (`regioesVencidas`), rankings com sufixo, conquistas novas, Qa `regiao`,
  **mapa provisório** (chão plano + Spawn/Altar/Portal/Mercador/Baús nos centros novos, `Alturas` plano), render com modelo
  provisório (recolor do equivalente do mapa 1) pra tudo rodar antes da arte. `TesteLogica`.
- **M2-A2** (Menu): seletor de mapa no Prepare, sala com mapa, Leaderboard por mapa, cadeado/desbloqueio, réplica do Shared.
- **M2-B** (Partida): terreno + cenário das 4 zonas (meshes gerados ≤ 6 por mapa + primitivas), `Alturas` regerado, auditoria.
- **M2-C** (Partida): modelos dos 20 comuns + 4 guardiões + chefe final (meshes gerados), mini-chefes.
- **M2-D**: Strange Fruit + revisão geral do mapa 2 + playtest.
- **M3-A…D**: idem pro mapa 3 (Energy Charge no D).
- **Final**: lote de tradução pt-BR (todos os textos novos do projeto) + playtest final nos 2 places.
