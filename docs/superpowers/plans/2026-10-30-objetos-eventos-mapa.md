# Objetos interativos e eventos de partida ("diretor") — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Encher as zonas de **decisões pequenas** (objetos de uso único com troca
risco ↔ prêmio) e dar **ritmo** à partida com um diretor de eventos (hordas com banner,
mini-chefes com prazo, atmosfera, anti-campar). Baseado na pesquisa
`docs/pokebonk-pesquisa-2026-10-30.md` (§1 objetos por zona e números, §4 diretor, §7 ideias
1–25, 37–38). Nomes e visuais nossos (tema ninja). O Diego autorizou "os recomendados e o
que você tiver de ideia" (2026-10-30).

**Architecture:**
- **Objetos como dado**: `Definicoes/Objetos` (`{ id: { name, descricao, icone, porZona:
  {n1,n2,n3,n4}, custo?, prompt, regra: {...} } }`) + `ObjetoSystem` (servidor) que sorteia
  posições por zona (sobre `Alturas`, longe de pontos-chave e caminhos, nos platôs), cria o
  molde (`ReplicatedStorage/Moldes/Objetos/<id>`, estático no place) com ProximityPrompt e
  rótulo no mundo (preço / % carga), valida o uso (distância, moedas, 1 uso), aplica a regra
  e manda `ObjetoUsado` (s→c) pro feedback. Regras implementadas por **tipo** (≤ 12 tipos),
  nunca por id: `cargaBencao`, `modificadorRun`, `desafio`, `trocaHp`, `tambor`, `espelho`,
  `esquecer`, `clonarItem`, `sorte`, `cacaNiquel`, `jaula`, `bauVariante`, `coleta`, `mola`.
- **Objetos da v1 (nomes nossos):**
  1. **Chakra Stone** (cargaBencao, tiers common/rare/epic/golden: 8/14/22/35 s dentro do
     círculo; epic/golden chamam ondas; golden selado até 1:30 da zona e dá 4 cartas pra
     escolher 2). Usa o fluxo de cartas existente.
  2. **Greed Shrine** (+20 % dificuldade, +25 % XP e moedas pelo resto da run).
  3. **Challenge Totem** (anel de 8 + 3×zona inimigos, 2 elites; venceu = baú de raridade
     maior via `BauSystem.criarGratis` com `raridadeMin`).
  4. **Cursed Altar** (+15 % inimigos, +10 % dificuldade → 1 item raro na hora).
  5. **Sealed Ruins** (3 selos: item épico −15 % HP máx. / pergaminho lendário −20 % /
     companheiro espírito −25 %; 1 escolha).
  6. **War Drum** (até 3 batidas: guardião +25 % HP/dano por batida, +1 baú ao morrer).
  7. **Trade Mirror** (stat ↑ 20 % / stat ↓ 10 % de uma tabela de 10 pares, mostrada antes).
  8. **Forgetful Monk** (esquece 1 golpe ou pergaminho; devolve o slot).
  9. **Shadow Twin** (clona 1 item não-lendário, respeitando `max`).
  10. **Sleepy Cat** (50 %: bênção pequena; 50 %: moedas 15×zona; frase engraçada).
  11. **Festival Pachinko** (custo base 20, +8 % por giro; tabela: 777 1,8 % = lendário,
      moedas ×3, cura total, item comum, emboscada, maldição −5 % HP; segurar E).
  12. **Beast Cage** (20 + 10×zona moedas → meia barra de XP + conquista).
  13. **Cursed Chest** (grátis + emboscada + 5 % dificuldade).
  14. **Gold Vein** (bater 3× = moedas) e **Healing Berry** (cura 20 %).
  15. **Spring Mushroom** (mola que lança pra um platô; `BodyVelocity`/`AssemblyLinearVelocity`
      só no cliente dono, servidor valida distância).
  Quantidade por zona copiada da tabela da pesquisa (§1), ajustável no `Config`.
- **Diretor** (`DiretorSystem`, servidor): a cada 60–90 s sorteia 1 evento com banner
  (`AvisoController` grande): **Swarm** (anel de 40 fracos), **Stampede** (linha que
  atravessa a zona), **Flock** (voadores rápidos), **Rockfall** (círculos de aviso + dano);
  mini-chefes **Dominant** (dá bênção ao morrer) e **Summoner** (foge após 45 s); atmosfera
  por zona (névoa densa 30 s, tempestade com marcas de raio, eclipse 20 s com chance de skin
  rara ×3 no drop de Essência, **Golden Thief** que solta moedas a cada golpe e foge);
  **Siege** anti-campar (parado > 12 s = anel vermelho + inimigos com 50 % de resistência até
  andar 30 studs); **chefe cansa** (+5 % dano recebido a cada 20 s após 2 min); marcos de
  combo (10/25/50/100 → moedas/ímã/cura); 1º elite da zona solta baú grátis; **split de
  tempo** por zona contra o recorde (verde/vermelho); iluminação progressiva por zona
  (tarde → crepúsculo → noite) além do clima.
- **HUD**: carteira no topo com preço do próximo baú e do reroll em verde/vermelho (`Config`);
  rótulos no mundo (BillboardGui no molde) com preço/% de carga, desligáveis nas configurações.
- **Conquistas novas** (dado): 3 selos, 3 batidas, 777, 15 maldições, vencer com ≤ 3 itens.
- Replicar `Shared` (Objetos/Conquistas/Config/PtBr/Types) no Menu; o mapa com descoberta
  (lote HUD) lista esses objetos por `Definicoes/Objetos[id].icone`.

**Spec:** §6/§7; pesquisa §1, §4, §6, §7.

## Review Focus
1. Todo uso de objeto é validado no servidor (distância ≤ 12, 1 uso, moedas, cooldown) e o cliente só anima; pachinko com rate-limit e custo crescente no servidor.
2. Modificadores de run (ganância, maldição, tambor) somam no estado da partida e zeram no Play Again; no co-op valem pro time e o banner diz quem ativou.
3. Diretor nunca estoura o teto de vivos (hordas respeitam `Config`), nunca dispara durante cartas/chefe final/transição; Summoner some de verdade (sem XP) e Thief solta moedas com teto.
4. Objetos sorteados fora de obstáculos (raycast + distância de pontos-chave) e alcançáveis (platô acessível pelo flood-fill de `Alturas`).
5. Desempenho: moldes clonados uma vez por zona (≤ 30 por zona), rótulos só a < 80 studs, sem Heartbeat por objeto (um laço no `ObjetoSystem` a 4 Hz).

### Task 1: `Definicoes/Objetos` + Types + Config + Conquistas + PtBr nos 2 places; moldes estáticos em `ReplicatedStorage/Moldes/Objetos` (primitivas + ≤ 6 meshes gerados); `TesteLogica` (tabela do pachinko soma 100 %, pares do espelho).
### Task 2: `ObjetoSystem` (sorteio, prompts, 14 tipos de regra) + hooks em Bau/LevelUp/Item/Heroi/Chefe.
### Task 3: `DiretorSystem` (hordas, mini-chefes com prazo, atmosfera, siege, chefe cansa, marcos, split) + banners/visuais no cliente.
### Task 4: HUD carteira + rótulos no mundo + configurações.
### Task 5: teste em Play (cada objeto usado 1×, cada evento forçado por `Config` curto) + revisão + docs.
