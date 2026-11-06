# Pool de golpes por desbloqueio + efeitos fiéis e bonitos — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** (1) Cada herói passa a ter **6 golpes** (hoje 4) e o pool de level-up vira
**global por desbloqueio**: os golpes de um herói só podem aparecer nas cartas de quem já
**desbloqueou aquele herói** no perfil (Megabonk: toda arma liberada entra no pool de
qualquer personagem). Quem joga com Ryuga e tem o Kaizo liberado pode receber "Rubber
Lash" nas cartas. (2) Cada golpe ganha um **visual próprio e fiel** ao que ele é (braço
elástico = cilindro que estica com rastro; clone = silhuetas; ki = esfera brilhante com
rastro e impacto; etc.), com partículas, luz, som e tremor leves, dentro dos pools do
`EfeitosController`. Pedido do Diego (2026-10-30): "efeitos dos poderes mais bonitos e fiéis
ao que eles são e colocar mais uma pool de poderes que nem o megabonk tem e só vai liberando
os poderes quando libera o personagem... caso não escolha [o herói], vai ter a chance de
aparecer"; "deixa bem bonito o jogo com efeitos, detalhes bonitos".

**Architecture:**
- `Definicoes/Golpes`: 18 golpes (6 × 3 heróis), cada um com `heroi: HeroiId` (dono),
  `inicial: boolean` (o 1º do kit, nunca entra no pool de outro herói), `forma`, `elemento`,
  números por nível, e um bloco `visual = { estilo, cor, cor2, tamanho, rastro, particulas,
  luz, som, impacto }` lido pelo `EfeitosController` — **estilos** (≤ 10, cada um uma função
  de desenho no cliente): `esfera`, `feixe`, `braco` (cilindro que estica da mão até o alvo e
  volta), `lamina` (arco/cone com corte), `onda` (anel que cresce), `chuva` (projéteis caem),
  `silhuetas` (cópias translúcidas do herói atacando), `cadeia` (raio que salta), `orbita`
  (orbes girando), `pilar` (coluna de luz). Nada por golpe no código: só dados + estilo.
- Pool de level-up (`LevelUpSystem`/`Logica/Cartas`): candidatos = golpes do herói atual +
  golpes não-iniciais dos heróis em `perfil.desbloqueios` (o servidor já carrega o perfil no
  Partida) − banidos; peso menor pra golpes de outro herói (`Config.PesoGolpeEmprestado 0,6`).
  Teto de 4 slots de golpe continua (`Config`), 5º/6º slot só por item/loja (se existir).
- Golpes novos (nomes nossos): Ryuga: "Ki Orbit" (orbita), "Rising Pillar" (pilar). Kaizo:
  "Rubber Lash" (braco, linha), "Anchor Drop" (chuva, área). Haruto: "Shadow Step Slash"
  (lamina, teleporta atrás), "Mirror Volley" (silhuetas disparando). Rebalancear só se um
  golpe novo quebrar (o Diego balanceia depois).
- Menu: ficha do herói lista os 6 golpes com o aviso "Unlock this hero to add their attacks
  to every run"; o Dojo/loja não muda.
- Juice geral da partida (Diego: "deixa bem bonito"): impacto com flash de cor no inimigo,
  faíscas por elemento, rastros nos projéteis, luz pontual breve nos golpes de área, tremor
  leve na ultimate, números de dano com cor por elemento e crítico maior. Tudo com os tetos
  do `Config` (partículas, luzes, Highlights) e pools já existentes.

**Spec:** §6 (combate), Megabonk §5 (armas no pool).

## Review Focus
1. Golpe de outro herói nunca aparece sem o desbloqueio no perfil; perfil só em memória (DataStore falhou) = só os do herói atual.
2. Pool com todos os heróis liberados ainda garante ≥ 1 golpe próprio nas 3 cartas até ter 2 golpes; `inicial` nunca entra emprestado.
3. Efeitos: zero alocação por frame nos estilos (pools de Parts/Beams/Attachments), teto de instâncias ativas, limpeza em `FimPartida`/`PartidaReiniciada`; 120 inimigos + 30 projéteis a ≥ 55 fps.
4. `Shared` idêntico nos 2 places (Golpes/Types/Config/PtBr).
5. Estilo `braco` e `silhuetas` com skin/evolução aplicadas (tinta/modelo do herói).

### Task 1: Definições (18 golpes + `visual`, `heroi`, `inicial`), Types, Config, PtBr nos 2 places + `TesteLogica` (pool por desbloqueio).
### Task 2 (Partida): `LevelUpSystem`/`Logica/Cartas` com pool por desbloqueio; `GolpeSystem` cobrindo os golpes novos com as formas existentes.
### Task 3 (Partida, cliente): 10 estilos no `EfeitosController` + juice de impacto/números/luz; Menu: ficha com 6 golpes.
### Task 4: teste em Play (cada golpe disparado e visto pelo contador de instâncias/efeitos; pool com 1 e com 3 heróis liberados) + revisão + docs.
