# Plano R1 — menores abertos + Survival/Mutação em sala co-op + prioridade de chefe (2026-11-03)

Diego: "continua fazendo o restante" (decisões de design delegadas ao Claude, seguindo PokeBonk/Megabonk). Contexto: lotes
`docs/superpowers/plans/2026-11-03-survival-mutacao.md` e `2026-11-03-polimento-survival-giro.md` (ledgers em
`.superpowers/sdd/2026-11-03-*`). Regiões 2–4 ficam de fora (mapa/arte do Diego). R2 (estatísticas por herói + nível de conta)
é o lote seguinte, separado.

## Task 0 — menores abertos (Partida)
- **M6 pacto pausa como as cartas**: a oferta de pacto (`PactoSystem`) usa o MESMO mecanismo de pausa das cartas de level-up
  (`EstadoPartida.pausadoPorCarta` / o que o `LevelUpSystem` faz, inclusive a regra de co-op — ler antes como a carta trata
  vários jogadores). Enquanto a lista está aberta, o jogo pausa pra quem tem lista aberta do mesmo jeito que a carta; a proteção
  de 8 s (`SurvivalPactoProtecao`) continua como está. Oferta nova com lista aberta: a nova substitui (já é assim) — ok.
- **M11 maldições**: `PactoSystem.aplicar` conta `maldicoes += 1` pra QUALQUER pacto com maldição (herói ou inimigo). Conferir o
  texto da conquista relacionada em `Definicoes/Conquistas` (deve dizer "pacts with a curse"/equivalente; ajustar se precisar).
- **m4 borda da grade**: `InimigoSystem.noRaio` percorre as células cobrindo `raio + borda extra` dos comuns escalados (Giant Wilds),
  como já faz o teste de acerto. Sem alocação nova por chamada.
- **qaEndless** fica como está.

## Task 1 — Survival e Mutação em sala co-op pelo Menu (Menu + Partida)
Hoje as salas são sempre Clássico (spec de 2026-11-03 deixou de fora; `PartidaSystem` força `classico` em sala — M5). PokeBonk
tem co-op nos modos, então:
- **Menu / sala**: o **líder** escolhe o modo da sala (Classic / Survival / Daily Mutation) no Lobby, ao lado da dificuldade
  (mesmo padrão de UI/remote/validação da dificuldade da sala: `SalaSystem` + `Telas/Coop`). Padrão Classic. Mutação força
  Normal (botões de dificuldade escondidos, como no Prepare). O estado da sala (`Types.SalaEstado`, se existir) ganha `modo`;
  validar contra `Definicoes/Modos` no servidor; rate-limit igual ao da dificuldade. Lobby mostra "Mode: X" pra todos.
- **Teleporte em grupo**: `TeleportData.modo` = modo da sala (hoje já leva dificuldade). Survival/Mutação já usam servidor
  reservado no solo; o grupo já vai pra servidor reservado — conferir que o modo chega junto.
- **Partida**: `PartidaSystem.aoEscolherHeroi` em sala (M5) passa a usar o **modo da sala** vindo do TeleportData (guardado em
  `CoopSystem.guardarEscolha`/estado da sala), ignorando o modo do cliente como hoje; `difSala` só no clássico e no Survival
  (Mutação = `Config.MutacaoDificuldade`). Quem começa fixa `EstadoPartida.modo`, como já é.
- **Rankings/prêmios em grupo**: Survival grava `SurvivalTempo` por jogador (tempo individual, já existe); Mutação grava
  `Mutacao_<dia>` e paga a trilha por jogador, igual ao solo. Nada de placar de grupo novo.
- Tirar "Survival em sala co-op" dos não-objetivos da spec (anotar no ledger; a spec não precisa ser editada).

## Task 2 — prioridade de alvo no chefe (Partida; ideia anotada em `estado-do-projeto.md`)
- `Config.PrioridadeChefe = true` e `Config.PrioridadeChefeRaioFrac = 0.8`: ao escolher alvo de um golpe (onde o `GolpeSystem`
  pega o inimigo mais próximo), se houver guardião/chefe de marco/chefe final (`ehChefe`, mini-chefe fora) a até
  `alcance × PrioridadeChefeRaioFrac`, ele vira o alvo; senão, o mais próximo como hoje. Vale pra golpes com alvo único e pro
  centro do leque/cone; golpes de área ao redor não mudam. Clones seguem a mesma regra. `false` desliga tudo (comportamento atual).
- Sem alocação por disparo: reaproveitar `InimigoSystem.infoChefes()`/lista de chefes vivos que já existe.

## Teste (agente em Play; co-op real é do Diego)
- Partida: `TesteLogica OK`; Survival `Qa marco` + `matarChefe` → lista de pacto abre e o jogo pausa (inimigos parados, relógio
  parado) até escolher; `Qa` com mutação Giant Wilds → comum gigante na borda da célula é atingido; com guardião vivo a 0.8 do
  alcance e um comum mais perto, o golpe mira o guardião; `PrioridadeChefe=false` temporário → volta ao mais próximo (restaurar).
- Menu: `TesteLogica (Menu) OK` (TesteSala: modo da sala validado/propagado; copiar o `TesteSala` pro Partida se mudar —
  cabeçalho "IDÊNTICO nos places"); `SalaCriar` → `SalaModo "sobrevivencia"` pelo líder → `SalaEstado.modo`; membro tentando →
  recusado; Mutação → dificuldade Normal fixa.
