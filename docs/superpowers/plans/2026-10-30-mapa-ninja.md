# Mapa ninja (relevo, zonas isoladas, cenário rico) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Trocar o mapa atual (4 quadrados planos de 300 studs enfileirados a 600 de
distância, visíveis uns dos outros) por 4 zonas **grandes, com relevo e cenário denso** no
tema **ninja original** (sem nomes/visuais de obras existentes), **isoladas** entre si
(não se vê a próxima zona), mantendo toda a lógica de zona/chefe/baú/mercador funcionando.
Pedido do Diego (2026-10-30): "ele tem relevo, tem objetos nele, árvores, estruturas, é bem
bacana. tente fazer do mesmo jeito"; "quando eu estou no primeiro mapa eu consigo ver o
segundo, não deveria dar para ver".

**Architecture:**
- Mesmos 4 ids de zona (`Vila`, `Bambuzal`, `Templo`, `Santuario`) — só muda `name`,
  tema, geometria e posições. Zonas afastadas **4000 studs** no X (0 / 4000 / 8000 / 12000)
  + `StreamingEnabled` com `StreamingTargetRadius` ≤ 1200 + névoa/Atmosphere por zona +
  borda natural (penhascos/muralha/árvores altas) = nunca se vê a próxima zona.
- Chão = **Terrain** (relevo suave: colinas até ±10 studs, platôs com rampas, riacho raso
  caminhável, lama/pedra/grama por zona) gerado em modo Edit por script (fica salvo no
  place). Zonas de 600×600 (Santuário 320×320). `Chao` vira parte invisível fina sob o
  terreno só se algum sistema depender dela (checar por grep); senão apagar.
- **Grade de alturas** `ReplicatedStorage/Shared/Mapa/Alturas` (ModuleScript gerado por
  script em Edit depois do terreno: por zona `{ x0, z0, passo = 6, colunas, linhas,
  dados }` + `Alturas.em(zonaId, x, z): number` com interpolação bilinear). Servidor usa
  pra Y de inimigos, projéteis inimigos, orbes, baús sorteados; cliente usa pra Y de render.
  Replicar o módulo no Menu só se o Menu o exigir (hoje não).
- Cenário por zona em `Workspace/Mapa/Zonas/<zona>/Decoracao`, **primitivas + no máx. 6
  meshes gerados reutilizados por clone** (árvore ninja, casa, torre de vigia, estátua,
  sapo de pedra, torii) — se a geração falhar ou demorar, só primitivas. Mesmas regras de
  colisão do lote anterior (só tronco/casa/rocha/pilar/muralha colidem; nada colidível a
  < 20 studs de Altar/Portal/Mercador/Baús, < 12 do Spawn, < 6 do eixo dos caminhos).
- Temas (nomes nossos): Vila → **"Shinobi Village"** (vila ninja de madeira com muralha,
  torre, campo de treino com alvos, lanternas, ponte sobre riacho); Bambuzal → **"Forest of
  Trials"** (árvores gigantes, troncos caídos, cogumelos, cabanas de treino, névoa);
  Templo → **"Fallen Fortress"** (fortaleza em ruínas, crateras, muralhas partidas,
  estátuas de guerreiros, catapultas quebradas, fogo); Santuario → **"Sealed Shrine"**
  (santuário do selo: círculo de selo gigante no chão, correntes, torii pretos, eclipse
  mantido).
- Ritmo da run de ~30 min: `Config` de duração de zona / mini-chefe ajustado pra 7 min
  por zona (4 zonas ≈ 28 min + chefe final). Só os números, sem mudar sistemas.

**Spec:** `docs/superpowers/specs/2026-10-29-animebonk-design.md` §7 (substituído por
este plano no tema), `docs/megabonk-referencia.md` §3, `docs/pokebonk-referencia.md`
(linha 17: terreno com relevo).

## Review Focus
1. Nenhum ponto-chave (Spawn, Altar, Portal, Mercador, Baús) dentro de terreno/obstáculo;
   herói não prende em 0 colisores a 10 studs; rampas ≤ 35°.
2. Inimigos/orbes/projéteis nunca flutuam nem afundam (Y pela grade); desempenho igual ao
   anterior (grade sem alocação por frame; `Alturas.em` sem criar tabelas).
3. Da Vila não se vê nenhuma outra zona (streaming + névoa + borda); teleporte entre zonas
   continua funcionando; co-op e `ZonaSystem` com os novos centros.
4. Sem nomes/visuais identificáveis de obras existentes.
5. Instâncias totais ≤ 2500 no `Mapa`; StreamingEnabled não quebra o render pool nem os
   marcadores (`ZonaHudController`).

### Task 1: Levantamento — grep de tudo que lê `Chao`, posições de zona (`Definicoes/Zonas`), Y fixo (`Y = 0`, `,0,`, `Vector3.new(x, 0`), `Config` de tempos de zona; ledger com a lista.
### Task 2: Terreno + grade de alturas (Edit): script gera terreno das 4 zonas nos novos centros, move Spawn/Altar/Portal/Mercador/Baús pros novos pontos (sobre o terreno), gera `Shared/Mapa/Alturas`; sistemas passam a usar `Alturas.em`.
### Task 3: Isolamento — `Definicoes/Zonas` com novos centros/tamanhos/nomes, Streaming (`StreamingTargetRadius`, `StreamingMinRadius`), névoa/Atmosphere/Lighting por zona no `ZonaVisualController`, borda natural.
### Task 4: Cenário das 4 zonas (meshes gerados ≤ 6 + primitivas), caminhos, iluminação, partículas (folhas, vaga-lumes, cinzas, selo).
## Adendo 2 (pedido do Diego, 2026-10-30, depois do lote): "mais relevo maior e aumentar eles tipo 1.5x"
- Zonas **900×900** (Santuário 480×480), centros mantidos (0/4000/8000/12000, cabe com folga).
- Relevo mais forte, **no estilo da referência** (`C:\Users\Diego\Desktop\pokebonk\20. em partida.png`): o chão é feito de
  **terraços/platôs em degraus** (3–4 níveis, 5–8 studs entre níveis, até ±15 no total) separados por **paredões de rocha
  visíveis** (Terrain Rock/Sandstone nas faces, grama no topo), ligados por rampas largas ≤ 35° e por passagens naturais;
  ravinas/vales entre platôs com riacho raso (Part translúcida) e ponte de madeira; montanhas altas (≥ 40) no horizonte
  da borda. Decoração densa como na referência: árvores de 2–3 tipos, pedras, tocos, cogumelos, flores, arbustos,
  gramas altas, troncos caídos, cada um em grupos naturais. O Diego disse (2026-10-30): "está fraco sim o relevo, precisa
  aumentar".
- Regenerar Terrain + `Shared/Mapa/Alturas` (passo 6 → 150×150 por zona), reassentar Spawn/Altar/Portal/Mercador/Baús
  (layout ×1,5 do atual), paredes invisíveis e `Chao` (tamanho novo), `Definicoes/Zonas.meiaLargura`, caminhos.
- Decoração: **reposicionar e densificar ~1,5×** (teto 2500 em `Workspace/Mapa` continua), mesmas regras de colisão e auditoria.
- `StreamingMinRadius` já está em 256 (Diego ajustou à mão). Executar **depois** do lote de inimigos (mesmo place).

### Task 5: `Config` ritmo 30 min; teste em Play (0 colisores nos pontos-chave, herói andando entre colinas, inimigos no chão, outra zona invisível); ledger + `docs/estado-do-projeto.md` (seção "Mapa ninja").
