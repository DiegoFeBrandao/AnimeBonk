# Survival + Mutação do Dia — plano de implementação (2026-11-03)

Spec: `docs/superpowers/specs/2026-11-03-survival-mutacao-design.md`. Execução inline pelo Claude (agentes bloqueados pelo auto
mode); ledger em `.superpowers/sdd/2026-11-03-survival-mutacao/progress.md`. Studios: Partida `fc765721…`, Menu `ed644ca6…`.
Shared replicado nos 2 places a cada lote (conferir tamanho/hash).

## Lote 1 — o modo viaja (Shared + Menu + Partida)
1. `Shared/Definicoes/Modos` (novo): `classico`, `sobrevivencia`, `mutacao` com `name`, `descricao`, `dificuldadeFixa?`.
2. `Shared/Types`: `modo: string?` em `PedidoHeroi`, `DadosTeleporte`, `FimPartidaInfo`; `Zona` ganha `modo`/`mutacao`.
3. `Shared/Config`: `ModoPadrao = "classico"`, `MutacaoDificuldade = "Normal"` (+ chaves do Survival e Mutação já declaradas).
4. Partida: `EstadoPartida.modo` + `defModo()`; `PartidaSystem.aoEscolherHeroi`/`heroiDoTeleporte` validam `modo` (quem começa
   define; depois segue o atual); `iniciar(dificuldade, modo)`; `FimPartidaInfo.modo`.
5. Menu: `MenuSystem.aoIrParaPartida` valida `modo` e grava no TeleportData (mutação força a dificuldade fixa);
   `MenuController.modoSel` (+ `ctx.escolherModo`), Home: cartão Survival vira botão real, cartão "Daily Mutation" novo;
   Preparar: rótulo "Mode: …" e esconde dificuldade quando o modo tem `dificuldadeFixa`.
6. Qa: `modo <id> [mutacaoId]` (só antes de escolher herói).

## Lote 2 — Survival (Partida + ranking + Menu)
1. `ZonaSystem`: ramo Survival em `iniciarZona`/laço: sem altar/prompt/portal/mini por tempo; `restante` sobe (negativo desde o
   início → HUD "+"? não: campo novo `decorridoZona` no Relogio; HUD mostra tempo subindo e "Survival"); `aplicarMultiplicadores`
   com a curva do Survival; marcos (`Config.SurvivalMarcos`) → `ChefeSystem`/`InimigoSystem.spawnarChefe` perto do grupo com
   banner `Evento`; Endless Night; `HeroiSystem.renascerMortos` após cada chefe de marco.
2. `PactoSystem` (novo, Server/Systems): depois de cada chefe de marco, oferta de 3 pactos por jogador vivo via
   `EscolhaObjeto`/`EscolherObjeto` (compartilha o canal com o ObjetoSystem: registrar um resolvedor de oferta); aplica bônus
   (`e.bonus`) e maldições (`EstadoPartida.modificadores` / multiplicadores de inimigo). `Shared/Definicoes/Pactos` (10).
3. Fim: `PartidaSystem.terminar` em Survival → tela "SURVIVED" + Essência por minuto; `RankingSystem` placar `SurvivalTempo`
   (2 places) + aba no Menu (`Telas/Ranking`).
4. HUD: `HudController` (timer subindo, rótulo "Survival"), `ZonaHudController` (sem objetivo de altar/portal; "Next boss in
   M:SS"), `FimController` (título/tempo).
5. Qa: `marco` (força o próximo marco), `pacto` (lista).

## Lote 3 — Mutação do Dia
1. `Shared/Definicoes/Mutacoes` (7) + `Logica/Mutacao` (dia UTC → mutação; próximas N; segundos até girar) — puro, testável.
2. Partida: `EstadoPartida.mutacao`/`semente`; multiplicadores em `ZonaSystem.aplicarMultiplicadores` (HP/spawn/vel/dano/escala
   dos comuns; chefes ignoram), `HeroiSystem` (dano/HP do herói, moedas/XP via `modificadores`), `InimigoRenderController`
   (escala); `ObjetoSystem` com `Random.new(semente)`.
3. Ranking `Mutacao_<dia>` (valor zona×1e6 + abates) nos 2 places; Menu aba "Daily Mutation" (Hoje/Ontem).
4. Perfil v7 (`mutacao = { dia, marcos }`, migração) + `Config.MutacaoPremios`; prêmios no `PartidaSystem` ao trocar de zona /
   vencer, toast pelo remote `Conquista`.
5. Menu: tela `Mutacao` (nome, descrição, chips, "Rotates in", próximas 2, melhor de hoje, PLAY); Home cartão; HUD chip.
6. Qa: `modo mutacao <id>`.
7. `TesteLogica`: casos de `Logica/Mutacao` (rotação determinística, próximas, segundos) e `Perfil.migrar` v6→v7.

## Lote 4 — Teste em Play, ledger, docs
Run Survival até 2 marcos com `Qa marco`, pacto escolhido, fim "SURVIVED", ranking local; run Mutação com `Giant Wilds`, prêmio
de zona 2, ranking; TesteLogica OK nos 2 places; Output limpo; `estado-do-projeto.md` + memória.

## Pendências anotadas pelo Diego durante o lote (fazer depois)
- **Herói vira pro alvo ao atacar e desvira** (PokeBonk): o sprite/modelo do herói gira sozinho pra direção do golpe no disparo e
  volta pra direção do movimento depois (`HeroiSpriteController` / `GolpeSystem` manda direção do alvo no `EfeitoGolpe`).
