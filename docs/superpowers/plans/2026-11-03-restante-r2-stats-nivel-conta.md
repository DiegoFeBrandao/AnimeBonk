# Plano R2 — estatísticas por herói + nível de conta (perfil v8) (2026-11-03)

Diego: "continua fazendo o restante". Itens "coming soon" do Menu desde 2026-10-30 (`estado-do-projeto.md` l.~983) e da spec
de design (ficha do herói: "minhas estatísticas com o herói"). Decisões de design do Claude, marcadas [C]. Roda DEPOIS do R1
(`2026-11-03-restante-r1-coop-modos.md`): mesmos places, não paralelizar.

## Shared (idêntico nos 2 places)
- `Types.Perfil` **v8**: `porHeroi: { [heroiId]: EstatisticasHeroi }` com `EstatisticasHeroi = { partidas, vitorias, abates,
  tempo (s), melhorNivel, melhorZona, melhorSurvival (s) }` e `conta: { xp: number }`. `Logica/Perfil`: `VERSAO = 8`,
  `estatisticasHeroiNova()`, `contaNova()`, `migrar` v7→v8 (porHeroi vazio; [C] `conta.xp = estatisticas.partidas ×
  Config.ContaXpSemente` pra veterano não voltar ao nível 1; validar chaves de `porHeroi` contra `Definicoes/Herois` e campos
  numéricos ≥ 0).
- `Logica/Conta` (novo, puro): `xpParaSubir(nivel)` = `Config.ContaXpBase + Config.ContaXpPorNivel × (nivel − 1)` [C];
  `nivel(xp)` e `progresso(xp) → (nivel, xpNoNivel, xpParaProximo)`; `xpDaPartida(info)` = `essenciaBase + floor(tempo/60) ×
  Config.ContaXpPorMinuto + floor(abates / Config.ContaXpPorAbates)` [C]. Teto de nível `Config.ContaNivelMax` (100).
- `Config`: `ContaXpBase 100`, `ContaXpPorNivel 50`, `ContaXpPorMinuto 2`, `ContaXpPorAbates 25`, `ContaXpSemente 30`,
  `ContaEssenciaPorNivel 10`, `ContaNivelMax 100`.
- `Types.FimPartidaInfo` ganha `contaXp: number` (ganho), `contaNivel: number` (depois), `contaSubiu: number` (níveis ganhos).

## Partida
- `PartidaSystem.terminar` (por jogador com herói): atualiza `porHeroi[heroiId]` (partidas +1, vitorias se vitória, abates e
  tempo individual da run — Survival usa `inicioSurvival`; melhorNivel; melhorZona só clássico/mutação; melhorSurvival só
  Survival); `conta.xp += xpDaPartida`; se o nível subiu: Essência `+ContaEssenciaPorNivel × níveis` somada ao perfil e toast
  pelo remote `Conquista` ("Account level N! +E Essence", mesmo padrão do `premiarMutacao`); `FimPartidaInfo.contaXp/
  contaNivel/contaSubiu`. QA (`qaMutacao`) não muda nada aqui (stats contam normalmente).
- `FimController`: linha "Account XP +N · Level L" (e "Level up!" quando `contaSubiu > 0`). Inglês, `AutoLocalize = false`
  como as linhas vizinhas.
- `TesteLogica`: migração v7→v8 (semente, porHeroi vazio, chave inválida descartada), `Logica/Conta` (nivel(0) = 1, limites,
  progresso, teto), `xpDaPartida` com valores conhecidos. Checagens "VERSAO == 7" → 8.

## Menu
- `BarraPerfil` (`Telas/Home`): "Lv N" + barra fina de progresso ao lado da Essência (usa `Logica/Conta.progresso`). Atualiza no
  evento `Perfil`.
- Ficha do herói (`Telas/Herois`): o campo "partidas" vira bloco **"My stats"**: Runs, Wins, KOs, Time played (h:mm), Best level,
  Best zone, Best survival (mm:ss ou "—"). Lê `perfil.porHeroi[heroiId]` (vazio → zeros/"—").
- Placa do herói na Home: se mostrar "partidas", trocar pra `porHeroi[escolhido].partidas` (senão deixar).
- `Server/Systems/PerfilSystem`/`MenuSystem`: nada muda além do `Logica/Perfil` novo (migração roda no load).

## Publicação
- Perfil v8: **os 2 places precisam ser publicados juntos** (Partida v7 lendo v8 não salva — proteção já existente).

## Teste (agente em Play)
- Partida: `TesteLogica OK`; run curta (`desistir` após matar algo) → Output com o `FimPartidaInfo` (contaXp > 0), perfil
  `porHeroi[Ryuga].partidas = 1`; run com XP forçado perto do limite (Qa `conta <xp>` novo, só Studio) → toast de nível + Essência.
- Menu: `TesteLogica (Menu) OK`; barra "Lv N" visível com perfil v8 (medidas por `AbsolutePosition`, sem sobrepor Essência);
  ficha do herói com o bloco "My stats"; `loadstring` nos scripts tocados; Shared idêntico (`#Source`).
