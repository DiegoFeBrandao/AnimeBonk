# Pool grande de itens e pergaminhos (+ "afeta o seu golpe") — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Subir de 22 itens / 13 pergaminhos para **~80 itens** e **~24 pergaminhos**, com
**5 raridades** (comum · incomum · raro · épico · lendário) e efeitos novos, com os stats
portados das referências (Megabonk §6–7, PokeBonk §9–10 em `docs/`), nomes e ícones
placeholder nossos (o Diego troca nome/ícone depois). Na **carta/oferta** (level-up, baú,
loja) mostrar se o item/pergaminho **afeta cada golpe equipado** do jogador ("Affects: Ki
Blast ✓ · Paper Crane ✗"). Pedido do Diego (2026-10-30): "uma pool grande de itens (os itens
pode pegar do pokebonk ou do megabonk e colocar aqui) eu falo dos status dele, eaí a gente
troca a foto e o nome"; "No item quando aparecer para mim, coloque se ele afeta ou não aquela
skill que eu estou utilizando".

**Architecture:**
- `Definicoes/Itens` continua **dado**; `RaridadeItem` vira `Types.Raridade` (5 níveis);
  `max` por raridade (comum 10 · incomum 6 · raro 4 · épico 2 · lendário 1), sobrescrevível.
- `Efeito` ganha variantes novas, todas resolvidas em `ItemSystem`/`Logica/Dano`/`GolpeSystem`
  sem `if item == "x"`: `statCondicional` (perto/longe, inimigo > 90 % HP, elite/chefe,
  parado, por abate até teto, por baú aberto), `aoAcertarDano` (chance de explosão/raio/
  bonk ×20/executar < X %), `aoMatar` (cura, moeda, míssil, XP extra, +HpMax até teto),
  `aoApanhar` (espinhos, veneno em área, moeda, velocidade breve, invulnerável curto),
  `economia` (chave 10 % baú grátis, +sorte por baú, preço), `meta` (+1 linha na carta,
  +1 rolagem on-hit, megacrit ×4, +teto de nível de golpe/pergaminho, overheal, 1 morte
  evitada por run, +dificuldade % como risco), `escudo` (recarrega após 5 s sem dano).
- Sorte (`Luck`) influencia raridade das cartas e dos baús (`Logica/Cartas` já tem raridade:
  acrescentar peso por sorte).
- **"Afeta o seu golpe"**: cada efeito declara `afeta` implicitamente pelo stat
  (`Projeteis`/`VelProjetil`/`Ricochete` → formas `projetil`/`cadeia`; `Area` → `area`/`cone`;
  `Duracao` → golpes com duração; `Dano`/`Critico`/`VelAtaque` → todos; status on-hit →
  todos; elemento → só golpes daquele elemento). `Logica/Afeta.golpe(def, golpeDef): boolean`
  puro, testado no `TesteLogica`. `CartaExibida`/`ItemLoja`/baú recebem `afeta: {GolpeId}`
  **calculado no servidor** a partir dos golpes equipados; o cliente só desenha ✓/✗ por golpe
  (ícone pequeno do golpe + cor). Vale para pergaminhos também.
- Pergaminhos novos (vitaminas do PokeBonk): dano físico/especial não existe aqui → usar
  Dano, VelAtaque, Armadura, Escudo, Velocidade, HpMax, Projeteis, Critico, VelProjetil,
  Evasao, ChanceStatus, Area, Duracao, Regen, Moedas, Xp, Sorte, RouboVida, Coleta,
  Espinhos, Sobrecura, Elites (+elites, +XP), Maldito (+inimigos/+XP, risco). Nível 1→10,
  ganho por raridade da carta (já existe `ganho`).
- Ícones: `letra` placeholder continua; acrescentar `icone: string?` (assetId) que, quando
  vazio, cai no placeholder. Diego preenche.
- Replicar `Shared` no Menu (Itens/Pergaminhos/Types/Logica) — o Menu mostra coleção/arquivo?
  Não na v1: só replicar os módulos pra manter os dois `Shared` iguais.

**Spec:** §6 (combate), referências §6–7 (Megabonk) e §9–10 (PokeBonk).

## Review Focus
1. Nenhum efeito novo confia no cliente; `afeta` vem do servidor e bate com os golpes equipados no momento da oferta (troca de golpe entre oferta e escolha → recalcular ao aplicar, não ao exibir).
2. Tetos: `max` por item respeitado em baú, loja e carta; "1 morte evitada" só 1× por run; overheal nunca passa do teto; `+dificuldade` não zera recompensa.
3. Desempenho: efeitos on-hit/on-kill sem alocação por acerto (tabelas pré-montadas por jogador em `ItemSystem.recalcular`).
4. Sorte muda só a raridade, nunca o conteúdo; distribuições testadas no `TesteLogica` (10 k sorteios, tolerância 2 %).
5. Texto da carta cabe na UI com 5 raridades e a linha "Affects" (mobile incluso).

### Task 1: Types/Definicoes (Itens ~80, Pergaminhos ~24, raridades, `icone?`, `afeta` em `CartaExibida`/`ItemLoja`) + `Logica/Afeta` + `Logica/Cartas` com sorte + `TesteLogica`, nos 2 places.
### Task 2 (Partida): ItemSystem/GolpeSystem/Logica.Dano/LevelUpSystem/BauSystem/MercadorSystem resolvendo os efeitos novos e preenchendo `afeta`.
### Task 3 (Partida, cliente): carta/loja/baú com cor das 5 raridades, linha "Affects" com ✓/✗ por golpe equipado, tooltip; ItemController lista com contagem ×N.
### Task 4: teste em Play (pegar 10 itens de tipos diferentes, loja, baú lendário, afeta correto ao trocar golpe) + revisão + docs.
