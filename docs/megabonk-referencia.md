# Megabonk — referência de mecânicas

Resumo tirado do wiki independente https://megabonk.org/ (288 páginas lidas em
2026-10-29; o site acompanha a versão **v1.0.69**, de julho/2026). Serve de base pra
comparar/inspirar o AnimeBonk — **não é spec do nosso jogo** e nada daqui deve ser
copiado literalmente (nomes, textos, personagens). Valores marcados pelo próprio wiki
como "comunidade"/"não confirmado" estão indicados com `~`.

Fora do escopo (o site também cobre, mas são outros jogos): PokeBonk, PokéSurvivor,
Azeroth Survivors, Survivor: Ace. Leaderboard, mods e páginas de save também foram
ignorados.

---

## 1. Ficha do jogo

| Campo | Valor |
|---|---|
| Gênero | Roguelike de sobrevivência 3D, "bullet heaven" (Vampire Survivors em 3D) |
| Dev / publisher | vedinad (solo) |
| Lançamento | 18/09/2025 (Steam) |
| Plataformas | Windows e Linux. Sem console/mobile oficial |
| Modo | **Só single-player** — sem co-op/online/local oficial (existem mods de multiplayer) |
| Sucesso | +1 milhão de cópias nas 2 primeiras semanas; pico de 117 mil jogadores simultâneos |
| Tom | Humor absurdo/meme (nomes como "Borgar", "Speed Boi", "Za Warudo", "Kevin") |

**Ideia central:** as armas atacam **sozinhas**. O jogador só controla **movimento**
(andar, pular, deslizar) e **decisões de upgrade**. "Ficar parado = morrer."
Movimento 3D livre com verticalidade (pulo, pulo duplo de alguns personagens, escalar
parede, bunny hop, slide com CTRL que dá i-frames).

---

## 2. Loop de uma partida (run)

1. Escolhe **personagem** (define passiva + arma inicial) → **mapa** → **tier**
   (dificuldade/nº de fases) → opcionalmente um **Challenge** (modificador).
2. Nasce no mapa gerado aleatoriamente; inimigos vêm em hordas crescentes.
3. Mata inimigos → caem **orbes de XP** (e ouro). Coletar XP → **level up** → escolhe 1
   entre 3 ofertas (arma nova, upgrade de arma, Tome novo ou upgrade de Tome).
4. Explora o mapa atrás de **baús** (custam ouro), **santuários** (shrines), **potes**
   quebráveis, **micro-ondas**, mercador, estátuas Moai e power-ups temporários.
5. Acha o **Portal do Chefe** (posição aleatória) e invoca o chefe quando quiser.
6. Aos **10:00** começa o **overtime / Final Swarm** (pressão máxima), quer o chefe
   tenha morrido ou não.
7. Mata o chefe → se o tier tiver mais fases, aparece o **portal da próxima fase**.
   Se não, fica no Final Swarm (sobreviver dá recompensas) até morrer/sair.
8. Fim da run → **Silver** (moeda permanente) entra na conta → gasta no menu em
   desbloqueios.

### Linha do tempo padrão de uma fase (Forest/Desert)

| Tempo | Evento |
|---|---|
| 0:00 | Fase começa. Explorar, pegar XP, procurar o portal do chefe |
| 3:00 | 1º mini-chefe |
| 4:00 | 1º evento de enxame (swarm) |
| 7:00 | 2º enxame |
| 8:00 | 2º mini-chefe |
| 10:00 | Overtime / Final Swarm |

- O portal do chefe já existe desde o início, em lugar aleatório; dá pra invocar cedo.
- Cada fase tem o próprio relógio (reinicia na próxima fase).
- **Final Swarm**: sobreviver 1 min desbloqueia um item, 2 min outro, 6 min um lendário.
  Multiplicador de Silver vai até **8×** (era 16×). Depois de 20 min os inimigos
  fantasma ficam mais rápidos e o limite de stun/freeze cai até zero — foi feito pra
  **matar runs infinitas** (antes havia runs de 5h+ com builds AFK).

### Tiers e fases

| Tier | Fases | Sequência | Libera com |
|---|---|---|---|
| 1 | 1 | Forest | já liberado |
| 2 | 2 | Forest → Desert (portal) | vencer Tier 1 |
| 3 | 3 | Forest → Desert → Chefe Final | vencer Tier 2 |

Não dá pra pular tier. Tier 1 não tem portal pós-chefe (a run acaba no Final Swarm).

---

## 3. Mapas

| Mapa | Tema / terreno | Inimigos típicos | Mecânica especial | Como libera |
|---|---|---|---|---|
| **Forest** | Floresta, morros, árvores, ruínas medievais; verticalidade e cobertura | Goblins, insetos, criaturas | Esconde segredos (jaula do macaco, arbusto suspeito, sapos) | Padrão |
| **Desert** | Plano, aberto, poucas ruínas, pouca cobertura | Escorpiões, cactos, "bolas de esqueleto", wisps | **Tempestade de areia** (visibilidade ~zero); **tornados** que levantam o jogador; desafio "chão é lava" | Chegar na fase 2 do Forest Tier 2 com um personagem específico |
| **Graveyard** | Cemitério + criptas | Esqueletos, fantasmas | **Cripta com contagem regressiva** (se zerar, chefe especial aparece); 4 chaves em caixões guardados; chefe na 2ª cripta; sala secreta | Cadeia de missão longa (personagem X no Desert T2, achar 4 túmulos, matar 4 fantasmas coloridos + chefe dourado) |

- Mapas **gerados aleatoriamente** a cada run (layout, baús, santuários, portal).
- Mapa em tela cheia com **névoa de guerra** (adicionado num patch).
- Objetos marcados no minimapa com ícones (santuário = losango verde etc.).

---

## 4. Personagens (21)

Cada personagem = **passiva que escala por nível** + **arma inicial**. Começa com 2
liberados; o resto é desbloqueado por objetivos e depois **comprado com Silver**.

| Personagem | Arquétipo | Passiva (escala por nível) | Arma inicial | Desbloqueio |
|---|---|---|---|---|
| Fox | Equilibrado, sorte | +1,5% Luck/nível | Fire Staff | Inicial |
| Sir Oofie | Tanque melee | +1% Armor/nível | Sword | Inicial |
| Megachad | Tanque "flex" | Ao "flexionar": imunidade, stun e +2,5% dano permanente | Aura | Damage Tome nv 7 |
| CL4NK | Robô crítico | +1% Crit Chance/nível | Revolver | Vencer Forest T1 |
| Ninja | Esquiva | +0,5% Evasion/nível; esquiva pode executar inimigo | Katana | Vencer Desert T1 + ter a Katana |
| Calcium | Velocidade | +0,75% dano/nível e dano extra por velocidade | Bone | Matar 1.000 esqueletos |
| Monke | Mobilidade | Escala parede, pulo alto, +2 HP/nível | Bananarang | Achar chave dourada e soltar da jaula no Forest |
| Robinette | Economia | +1% ouro/nível; dano escala com ouro carregado | Bow | Vencer Forest T2 |
| Vlad | Vampiro | +5% lifesteal base +1%/nível | Blood Magic | Vencer Desert T2 |
| Sir Chadwell | Amaldiçoado | +1% Curse (dificuldade)/nível | Corrupted Sword | Vencer Forest T3 |
| Ogre | Bruto | +1,5% dano/nível | Axe | Liberar Axe + matar 15.000 goblins |
| Amog | Veneno | +1% dano de veneno/nível; raio cresce | Poison Flask | Envenenar 50.000 inimigos |
| Athena | Espinhos | +2 Thorns/nível; mais dano com pouca vida | Aegis | Liberar Aegis + Thorns Tome |
| Bandit | Velocidade de ataque | +1% atk speed/nível | Dexecutioner | Matar mini-chefe secreto no Desert |
| Birdo | Aéreo | Planar + dano aéreo/nível | Tornado | Matar 100 inimigos com Tornado no ar (Desert) |
| Bush | Sniper | +1% crit dmg/nível; marca inimigos pra explodir | Sniper Rifle | Ter Sniper + achar e vencer o "arbusto suspeito" no Forest |
| Dicehead | Aposta/RNG | "Gamba": atributos aleatórios por nível | Dice | Completar 100 quests |
| Noelle | Gelo | +0,75% tamanho/nível, dano por inimigo congelado | Frostwalker | Duplicar item X 3× seguidas no micro-ondas |
| Roberto | Colecionador | Gera baú grátis periodicamente | Scythe | Matar chefe da cripta e comprar a Scythe |
| Spaceman | XP | +5% XP fixo +1,5%/nível | Black Hole | 6 challenges + liberar Black Hole |
| Tony McZoom | Elétrico | Carrega eletricidade andando; +2% alcance de coleta/nível | Wireless Dagger | 2 challenges + liberar Wireless Dagger |

**Padrões de design que valem anotar:**
- Desbloqueio de personagem quase sempre ensina/força uma mecânica (ex.: "use o
  micro-ondas 3×", "mate 100 no ar", "ache o segredo no mapa").
- Personagens secretos escondidos no mapa (jaula, arbusto que é chefe, mini-chefe raro).
- Passiva **sempre escala com o nível da run** → todo personagem fica mais forte no tempo.

---

## 5. Armas (30)

Começa com **2 slots de arma** (3º e 4º slots são upgrades de loja). 7 armas vêm
liberadas por padrão. Arma sobe de nível pelas ofertas de level-up; cada upgrade rola
**linhas de atributo** (dano, quantidade, tamanho, duração, cooldown, crit, ricochete,
knockback...) e a raridade da oferta define quantas linhas/quanto valor.

| Arma | Tipo / comportamento | Desbloqueio (resumo) |
|---|---|---|
| Sword | Corte melee em arco à frente | Padrão (Sir Oofie) |
| Fire Staff | Bolas de fogo que explodem (área) | Padrão |
| Flamewalker | Deixa rastro de fogo ao andar (S-tier) | Padrão |
| Lightning Staff | Raios em inimigos próximos, ricocheteiam | Padrão |
| Chunkers | Pedras orbitando, knockback 360° | Padrão |
| Aura | Campo de dano constante em volta | Padrão/Megachad |
| Bow | Flechas, perfuração | Padrão/Robinette |
| Revolver | Rajada, forte em crit e ricochete | Matar 7.500 no total |
| Katana | Golpes rápidos melee | Ninja |
| Axe | Lâminas giratórias em arco/órbita (escala muito no late) | Objetivo |
| Bananarang | Bumerangue que vai e volta | Monke |
| Black Hole | Puxa e agrupa inimigos (controle) | Objetivo |
| Blood Magic | Pulso de sangue, dá Max HP ao matar | Vlad |
| Bone | Projétil que quica entre inimigos | Calcium |
| Corrupted Sword | Corte frente+trás, mais dano com pouca vida | Cursed Tome nv 20 antes de 10:00 |
| Dexecutioner | Golpe em linha perfurante, 2% de executar | Bandit |
| Dice | Dados; 6 = crítico acumulado | Dicehead |
| Dragon's Breath | Jato de fogo com mira automática | Matar 1.000 wisps com Fox no Desert |
| Frostwalker | Congela área ao redor, vira trilha de gelo | Congelar 1.000 inimigos |
| Hero Sword | Corte múltiplo + onda de corte à distância | Matar chefe **sem** itens, power-ups ou santuários |
| Mines | Minas de proximidade (controle de área) | 7.500 kills com Rocket |
| Poison Flask | Garrafa que vira nuvem de veneno | Amog |
| Scythe | Arco largo melee | Matar o chefe da cripta |
| Shotgun | Cone de chumbinhos, **mira manual** | Drop raro no Desert |
| Rocket (nome meme) | Míssil teleguiado explosivo | 15.000 kills com CL4NK |
| Sniper Rifle | Tiro perfurante, **mira manual**, mata chefe | Precision Tome nv 10 numa run |
| Space Noodle | Feixe que gruda num alvo e fere tudo entre | Vencer Desert T2 com Tony |
| Tornado | Knockback / controle | Carregar 5 santuários durante tempestade de areia |
| Wireless Dagger | Adagas teleguiadas | Tony |
| Aegis | Escudo que bloqueia (defensiva) | Bloquear 500 de dano com armor usando Sir Oofie |

**Famílias de arma** (útil pro nosso design): melee em arco · projétil reto · projétil
teleguiado · projétil que quica/perfura · órbita · aura/campo · rastro no chão ·
armadilha · controle (puxar/empurrar) · mira manual (exceção, alto risco/recompensa).

---

## 6. Tomes (23) — upgrades passivos de atributo

Tome = "livro" que entra num slot e sobe de nível pelas ofertas de level-up. Começa com
**2 slots de Tome** (3º e 4º via loja). Nível máximo ~99. Valores por nível (raridade
comum; ofertas raras dão mais):

| Tome | Atributo | Por nível | Desbloqueio |
|---|---|---|---|
| Damage | Dano (multiplicador) | ~+8% | Padrão |
| Cooldown | Velocidade de ataque | — | Padrão |
| Agility | Velocidade de movimento | +15% | Padrão |
| Health | Max HP | +25 | Padrão |
| Regen | Regen de HP | +40/min | Padrão |
| Shield | Escudo (recarrega após 5 s sem dano) | +25 | Padrão |
| Size | Tamanho de ataques | ~+10% | Padrão |
| Knockback | Empurrão (só armas que têm) | +20% | Padrão |
| Golden | Ganho de ouro | +12% | Padrão |
| Silver | Ganho de Silver (meta) | +12% | Padrão |
| Precision | Crit chance (>100% = Overcrit) | +7% | Padrão |
| Luck | Sorte (raridade das ofertas/baús) | +7% | Padrão |
| Quantity | +1 projétil | +1 | Disparar 5.000 projéteis |
| XP | Ganho de XP | +7% (era 9%) | Quebrar 20 potes numa run |
| Attraction | Raio de coleta | +75% | Usar santuário 8× |
| Armor | Redução de dano | +12% | 5.000 kills com Sir Oofie |
| Evasion | Esquiva (retornos decrescentes) | +10% interno | Objetivo |
| Duration | Duração de projéteis/efeitos | — | Objetivo |
| Projectile Speed | Velocidade de projétil | ~+15% | Objetivo |
| Thorns | Dano refletido | +15 | Bloquear 250 com Aegis |
| Bloody | Lifesteal | ~+10% | 12.500 kills |
| Cursed | **Dificuldade +3,5%/nível** (mais inimigos = mais XP/loot) | +3,5% | Matar chefe em < 5 min |
| Chaos | +1 atributo aleatório por nível | aleatório | Desafio extremo |

**"Santíssima Trindade" da comunidade:** XP Tome + Luck Tome + Cursed Tome → loop
exponencial (mais inimigos × mais XP × ofertas melhores). Mostra o valor de ter um
Tome de **risco/recompensa** que o jogador escolhe pegar.

---

## 7. Itens (~80) — passivos de inventário

Itens vêm de **baús**, mercador, estátuas Moai e chão. Não ocupam slot (empilham;
duplicatas somam). Raridades: **Common · Uncommon · Rare · Epic · Legendary** (cor na UI).
Muitos começam bloqueados e são liberados por objetivos ("mate 3.000 com a Sniper").

Agrupados por **função** (o que importa pro nosso design):

- **Atributo puro:** +10% dano; +8% atk speed; +25 Max HP; +15% velocidade; +10% crit;
  +10% sorte; +8% XP; +15% evasão; +45 regen; +1 projétil em todas as armas.
- **Condicional de dano:** +20% em inimigos perto; +20% em inimigos com >90% HP; +15%
  em elites/chefes; +50% no ar; mais dano quanto menos vida; dano escala com Max HP;
  dano cresce parado (até +100%); +0,1% dano por kill (até +100%); +2,5% dano por baú
  aberto.
- **On-hit (chance ao acertar):** envenenar (40%), queimar (15%), congelar (20%),
  raio/stun (25%), explosão grande com knockback (8%), 2% de "BONK" 20× dano, 1% de
  executar (e +1% dano permanente), arremessar inimigo pro alto.
- **On-kill:** almas teleguiadas, mísseis (20%), chance de dropar cura, +XP extra,
  +Max HP por kill (com teto).
- **On-damage-taken (ao apanhar):** espinhos, choque elétrico, nuvem de veneno,
  ganhar ouro, velocidade breve, refletir dano + invulnerabilidade curta, tempo lento +
  2× dano abaixo de 50% HP.
- **Economia:** +15% ouro de kill; ouro por metro andado; chave que abre baú de graça
  (10%); +2% sorte por baú aberto (mas baú fica 10% mais caro).
- **Meta-modificadores (lendários que mudam regras):** upgrade de arma ganha +1 linha
  de atributo; +1 rolagem de todo efeito on-hit; crit vira megacrit (4×); +10 níveis no
  teto de arma; +10 níveis no teto de Tome; **evita uma morte por run** (congela o
  tempo); overheal até 75% do Max HP.
- **Risco autoinfligido:** +7% dificuldade; 25% de socar a si mesmo (mas ativa efeitos
  on-hit) — item "piada" que virou combo meta.
- **Mapa/santuário:** santuário carrega 4% mais rápido e dá +7,5%; +2 santuários nas
  próximas fases e zona de cura; invocar fantasmas ao usar objetos.

---

## 8. Atributos (stats) e fórmulas

| Stat | Efeito |
|---|---|
| Max HP / HP Regen (por minuto) / Overheal | Vida, cura passiva, vida extra acima do máximo |
| Shield | Absorve antes do HP; recarrega após **5 s** sem dano. Um único golpe não atravessa escudo + HP (anti one-shot) |
| Armor | % de redução, aditivo com **retornos decrescentes** (nunca 100%) |
| Evasion | % de anular golpe, hiperbólico (nunca 100%) |
| Lifesteal | % de chance de roubar 1 HP por ataque; >100% = chance de 2 HP |
| Thorns | Dano devolvido a quem bate |
| Damage | Multiplicador (2.0× = 200%) |
| Attack Speed | Menos tempo entre ataques, global |
| Crit Chance / Crit Damage | >100% vira **Overcrit** (vários crits no mesmo golpe) |
| Projectile Count / Speed | Mais projéteis / mais rápidos |
| Size / Duration / Knockback | Só funcionam se a arma tem a propriedade |
| Luck | Raridade de ofertas, baús, santuários, Moai, mercador (não aumenta crit/proc) |
| XP Gain / Pickup Range | Ritmo de nível / raio de coleta |
| Difficulty (Curse) | Mais HP, dano, velocidade e quantidade de inimigos; mais XP/loot por minuto |
| Powerup Multiplier / Drop Chance | Duração/força de power-ups e chance relativa de cair |

**Faixas de dano (damage brackets):** bônus **dentro** da mesma faixa somam; faixas
**diferentes** multiplicam. Dano final = base × (1+Tome) × (1+passiva) × (1+itens
fixos) × (1+"Damage %" condicional) × (1+velocidade) × (1+elite) × (1+arma especial)
× megacrit. Consequência: espalhar bônus por faixas rende mais que empilhar numa só
(1,5×1,5 = 2,25 > 2,0).

**Proc coefficient:** só armas e **8 itens** disparam efeitos on-hit de outros itens;
a chance é multiplicada pelo coeficiente da fonte (arma = 1,0; alguns itens = 0,5).
Evita reação em cadeia infinita.

**Efeitos de status:**

| Efeito | Duração base | Detalhe |
|---|---|---|
| Poison | 5 s | Acumula; tick a cada 0,5 s; Duration = mais ticks |
| Burn | ~3 s | Tick a cada 1 s |
| Freeze | ~3 s | −70% velocidade (inimigo fica azul) |
| Stun | ~3 s | Para o inimigo (fica amarelo). Chefe atordoado ainda ataca |
| Bloodmark | — | Dano atrasado acumulado (barra vermelho-escuro); mata se passar da vida |

**Imunidade a CC escondida:** após 15 stuns/freezes o inimigo fica imune; depois de
20 min o limite cai até zero (anti stun-lock infinito).

---

## 9. Objetos do mapa (interações)

| Objeto | Como funciona |
|---|---|
| **Orbe de XP** | Cai ao matar; coleta por proximidade (raio = Attraction) |
| **Ouro** | Moeda da run (baús, mercador, micro-ondas) |
| **Baú** | Custa ouro, **preço sobe** a cada abertura; dá item |
| **Charge Shrine** (losango verde) | Ficar **dentro do círculo** até carregar enquanto apanha → escolher 1 de 3 bônus de atributo. Versão **dourada** dá bônus lendários |
| **Greed Shrine** | +5% dificuldade permanente na run em troca de recompensa econômica |
| **Boss Curse** (altar de sangue) | +1 cópia do chefe; se vencer, +1 baú |
| **Moai** | Oferta de itens/troca baseada em sorte |
| **Mercador ("Shady Guy")** | Loja de itens na fase; estoque rolado com a sorte na entrada |
| **Micro-ondas** | Duplica um item escolhido, custa ouro **e destrói outro item aleatório da mesma raridade**; usos por raridade: Common 3, Rare 2, Epic 2, Legendary 1, depois explode |
| **Potes** | Quebráveis, dão ouro/coisas; desbloqueios por quantidade |
| **Power-ups no chão** | Temporários: dano, velocidade, proteção, cura, utilidade |
| **Portal do Chefe** | Arco com caveira, posição aleatória, partículas de vento em volta; o jogador escolhe quando invocar |
| **Portal de fase** | Só aparece após o chefe, se o tier tiver mais fases |
| Segredos | Chave dourada + jaula, arbusto-chefe, sapos escondidos, sala secreta, item no topo de torre |

---

## 10. Chefes

| Chefe | Onde | Destaque |
|---|---|---|
| Mini-chefes | 3:00 e 8:00 de cada fase | Elites mais fortes |
| Chefe Forest T1 | Forest T1 | Tutorial: esferas vermelhas, padrões previsíveis, kitar em círculo (~100K HP) |
| Chefe Forest T2 | Forest T2 | Versão reforçada: mais dano, projéteis mais rápidos (~500K HP) |
| Chefe Forest T3 | Forest T3 | **Deleta todas as armas menos a inicial**; pilares de escudo + fases de cura (~18M HP) |
| Chefe do Desert | Desert | Multi-fase, lasers em área, invoca enxames |
| Chefe da cripta (temporizado) | Graveyard | Aparece se o contador da cripta zerar; vida enorme |
| Chefe da cripta final | Graveyard | Fim da rota das 4 chaves |
| Chefe Final | Tier 3 fase 3 | Cicla fogo/gelo/raio a cada 30 s, várias fases |
| Chefes secretos | Forest/Desert | Arbusto disfarçado, bandido, fantasmas coloridos + estátua dourada |

Ideia forte: **o jogador decide quando enfrentar o chefe** (portal) e pode **multiplicar
o chefe por mais loot** (altar).

---

## 11. Meta-progressão (entre runs)

- **Silver**: moeda permanente ganha na run (multiplicada pelo Final Swarm, challenges e
  Silver Tome). Usada pra **comprar** personagens, armas, itens e Tomes já destravados.
- Desbloqueio em **duas etapas**: cumprir o objetivo (achievement) → comprar com Silver.
- **Quests** (conquistas) cumulativas entre runs. Marcos de quests liberam upgrades de
  loja: 20 → Refresh (rerolar ofertas) · 25 → 3º slot de arma (50 Silver) · 30 → Skip ·
  35 → 3º slot de Tome · 40 → Banish (remover opção da run) · 45 → 4º slot de arma
  (125 Silver) · 55 → 4º slot de Tome.
- **Toggler** (após comprar 40 desbloqueios, custa 4 Silver): desativar conteúdo do pool
  antes da run. Motivo: **cada desbloqueio dilui o pool** e dificulta sinergias — o
  próprio wiki aconselha não desbloquear tudo de uma vez.
- **Challenges** (1 por run, ligados a mapa+tier, ficam fora do ranking): AFK (não se
  mexer até o Final Swarm, 1,5× Silver), Pacifist (sem armas, 2×), Fragile (sem tomar
  dano, 1,6×), Speedrunner (chefes em 6:00, 1,5×) e Speedrunner+ (4:15, 2×), Sem itens
  (1,5×), Chão é lava (1,5×). Primeira conclusão dá +1% Silver permanente.
- **Cosméticos** (zero atributo, comprados com Silver): 4 skins por personagem com
  modelo padrão de desbloqueio (matar o 1º chefe em < 6 min; 15.000 kills com o
  personagem; etc.) + 22 chapéus por conquistas (achar sapos escondidos, explodir 50
  micro-ondas...).
- **Leaderboards** (kills, tempo), com anti-cheat; runs com Challenge não contam.
- **Dificuldade escolhível**: mais dificuldade = mais XP/moedas, mais volatilidade.

---

## 12. Conselhos de jogo do wiki (revelam a curva pretendida)

- Prioridade de iniciante: **HP/Regen → velocidade → armor/escudo → dano**.
- Armas de área são mais fáceis no início; armas de mira manual são de especialista.
- Pegar XP cedo (snowball), pegar santuário quando a área está controlada.
- "Não pegue só dano"; "abra o baú agora se estiver apertado".
- Dificuldade/Curse só quando a build está estável.
- Personagens complexos (RNG, velocidade) não são pra iniciante.

---

## 13. Histórico de balanceamento (lições)

- **v1.0.7**: corrigido exploit de invencibilidade do item de autodano; reset do ranking.
- **v1.0.12**: XP Tome 9% → 7%; teto no item de executar (2.000% com 10 cópias);
  Final Swarm refeito pra acabar com runs de 5h+ (fantasmas, imunidade a CC);
  um personagem tinha 99% de uso no topo — rebalanceado pra 8 viáveis.
- **v1.0.17**: mapa com névoa de guerra, transparência de projéteis ajustável (acúmulo
  de efeitos cegava o jogador), coleta de dinheiro mais rápida no Final Swarm.
- **v1.0.49 (Natal)**: Silver removido dos santuários; cartão de crédito encarece baú;
  pote não afeta mais Tomes; Wizard's Hat.
- **v1.0.64 "H A T S"**: 21 chapéus cosméticos.
- **v1.0.69**: versão atual acompanhada.

Lições: escalonamento infinito precisa de **tetos** e de uma fase final que **termina**;
efeitos visuais acumulados atrapalham leitura (dar opção de transparência); itens de
autodano geram exploits; um personagem dominante mata a variedade.

---

## 14. O que levar pro AnimeBonk (pra discutir — não decidido)

Ideias **de gênero** que se aplicam bem ao Roblox; tudo com nomes/arte/tema próprios:

- Auto-ataque + movimento 3D com verticalidade (pulo duplo, dash/slide com i-frame) —
  o Roblox já dá física de personagem.
- Level-up com 3 ofertas (arma / upgrade de arma / "livro" de atributo), com raridade.
- Slots limitados (2 armas + 2 passivas no início) liberados por meta-progressão.
- Itens com funções claras (atributo, condicional, on-hit, on-kill, ao apanhar,
  economia, meta-regra), raridades e pool controlável (banir/desativar).
- Mapa com timer de 10 min, mini-chefes em horários fixos, portal do chefe sorteado e
  decisão de quando enfrentar.
- Santuários de risco (ficar no círculo), altar de "mais chefe = mais loot", baús com
  preço crescente, mercador, objeto de duplicar com custo.
- Fase final que encerra a run (evitar runs infinitas — ainda mais em servidor Roblox).
- Personagens = passiva que escala + arma inicial; desbloqueio por objetivo que ensina
  uma mecânica + compra com moeda permanente.
- Cosméticos por conquista (bom pra retenção no Roblox) sem afetar atributos.
- Diferencial possível no Roblox: **co-op** (o Megabonk é só solo) — impacta
  performance, escala de inimigos e servidor autoritativo; decidir cedo.
- Tema anime original: "golpes especiais" com efeitos exagerados, arquétipos (espadachim,
  ninja, mago, lutador, garota mágica), chefes estilo arco de anime.
