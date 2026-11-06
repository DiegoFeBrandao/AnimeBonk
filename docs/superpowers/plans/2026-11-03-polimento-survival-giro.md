# Plano — Polimento Survival/Mutação + giro do herói + Endless Night (2026-11-03)

Contexto: lote Survival + Mutação do Dia (`docs/superpowers/plans/2026-11-03-survival-mutacao.md`) implementado, revisado e
corrigido em 2026-11-03 (`.superpowers/sdd/2026-11-03-survival-mutacao/review.md` e `fix-review.md`). Diego: "pode continuar
fazendo o game". Este lote fecha os menores que valem a pena, a pendência do Diego (giro do herói) e o aperto da Endless Night
previsto na spec (`docs/superpowers/specs/2026-11-03-survival-mutacao-design.md` §Survival) que não foi feito.

## Task 0 — menores das revisões (Partida salvo onde indicado Menu)
- **m1** `ObjetoSystem.gerar` (l.~546–555): na 1ª pedra, sortear sempre os 2 números do `rngPos` antes de decidir o tier pelo
  limiar da sorte → tiers iguais pra todos os grupos na Mutação.
- **m5** `PartidaSystem.terminar`/`FimPartidaInfo`: tela "SURVIVED" mostra o tempo do jogador (`tempoSurv`), não o `decorrido`
  da partida. Se `FimPartidaInfo` precisar de campo novo em `Types` (Shared), replicar no Menu.
- **m7** `Qa guardiao` no Survival: zerar/ajustar `marcoTipo` (ou mandar o tipo invocado) pra HUD mostrar o nome certo.
- **m8** `HeroiEscolhaController`: só manda `td.modo` se existir em `Definicoes/Modos`.
- **M1** `Logica/Perfil.migrar`: `mutacao.marcos` só aceita chaves de `Config.MutacaoPremios` (Shared → replicar no Menu).
- **M2** Relógio do servidor no cliente: `Telas/Mutacao` (Menu) e `MenuController.escolherModoRanking/escolherDiaRanking` usam
  `workspace:GetServerTimeNow()` em vez de `os.time()`. Se `Logica/Mutacao` ganhar parâmetro `agora: number?` (default
  `os.time()` no servidor), atualizar `TesteLogica` e replicar o Shared no Menu.
- **M4** `premiarMutacao`: só reseta os marcos quando `dia > pf.mutacao.dia`; se `dia < pf.mutacao.dia` (run que atravessou a
  meia-noite), não paga nem apaga.
- **M8** `PactoSystem.resolver`: rate-limit curto pra `indice = 0` (reabrir a lista), `Config.RateLimitReabrirPacto` (0.5 s).
- **M9** `MenuController.atualizarModo` (Menu): guardar a dificuldade escolhida antes de forçar Normal no modo fixo e devolver ao
  voltar pra clássico/Survival.
- **m6** `MenuSystem.aoIrParaPartida` (Menu): `ReserveServer` com `comRetry` (como o `SalaSystem`) e `saindoDaSala` só depois da
  reserva dar certo.
- Fora: M6 (design), M10 (tradução no fim), M11 (contagem de maldições — perguntar ao Diego), m2/m3 (resolvidos por M2 ou
  aceitáveis), m4 (borda da grade — aceitável; anotar).

## Task 1 — herói vira pro alvo ao atacar e desvira (pendência do Diego, PokeBonk)
- Só visual, no cliente. Ao disparar um golpe com alvo, o herói passa a encarar a direção do alvo por `Config.HeroiGiroDuracao`
  (0.35 s; renovado a cada disparo) e depois volta a encarar a direção do movimento (ou a última direção, parado).
- Fonte da direção: o `EfeitoGolpe` já leva origem/direção do golpe — confirmar o payload no `GolpeSystem`/`EfeitosController`.
  Se faltar, acrescentar `direcao` ao payload (em `Types`, Shared → replicar no Menu) sem mandar nada que o cliente não precise.
- Onde o herói "encara" hoje: `HeroiSpriteController` (sprite/modelo). Reaproveitar o mecanismo de virar pro movimento (flip do
  sprite ou rotação do modelo): o giro pro alvo é um override temporário dessa direção, com o mesmo tween/suavização.
- Golpes sem alvo (área ao redor) não giram. Clones de Haruto seguem o mesmo giro só se já seguem a direção do dono.
- Sem alocação por frame: um `alvoAte: number` + `direcaoAlvo: Vector3` por herói, lidos no laço que já existe.

## Task 2 — aperto da Endless Night (spec §Survival, M7)
- `Config.SurvivalElitePorMinuto` (0.01 = +1 pt de chance de elite por minuto, teto `SurvivalEliteMax` 0.5) aplicado na chance
  de elite dos comuns no Survival (onde o `InimigoSystem`/`DiretorSystem` decide elite).
- Endless Night (depois do último marco): velocidade dos comuns ×(1 + `SurvivalEndlessVelPasso` 0.10 a cada
  `SurvivalEndlessIntervalo`), teto `SurvivalEndlessVelMax` 1.6. Só comuns (chefes fora, coerente com I9).
- Aplicar em `ZonaSystem.aplicarMultiplicadores` (Survival) junto da curva de HP/spawn já existente; `Qa` ganha `endless` (pula
  pro início da Endless Night) se não existir.

## Teste (agente em Play; Diego confirma visual depois)
- Partida: `TesteLogica OK`; Survival com `Qa marco` ×5 (ou `endless`) → velocidade dos comuns sobe (print temporário removido);
  pacto `indice = 0` 3× rápido → só 1 reenvio; giro: disparar golpe com inimigo à direita enquanto anda pra esquerda → sprite
  encara a direita por ~0.35 s e volta. Mutação: 2 runs com `mutacao <id>` → tiers das pedras iguais.
- Menu: `TesteLogica OK`; tela Mutação usa `GetServerTimeNow`; `loadstring` no `MenuSystem` e `MenuController`.
