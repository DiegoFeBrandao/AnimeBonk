# Co-op: tela de entrada e sala no fluxo do PokeBonk (2026-11-05)

Pedido do Diego (2026-11-05): não gostou do "Criar sala" da tela Cooperativo; o herói não deve ser escolhido antes, só
depois de criar a sala, onde se escolhe mapa, dificuldade e herói; copiar o fluxo do PokeBonk. O desenho das duas telas
foi aprovado por ele no artifact "Telas Co-op AnimeBonk" (cópia local do HTML no brief do lote). Só a **estrutura** vem do
PokeBonk; textos, nomes e arte são nossos.

## Como o PokeBonk faz (lido no cliente v0.9.13)

- "Criar sala" cria na hora, sem perguntar nada: sala privada, 4 vagas, último personagem usado.
- Dentro da sala: destino (mapa, modo, dificuldade) à esquerda, 4 cartões de jogador no centro, código/convite à direita,
  barra de estado embaixo com um único botão grande (líder: começar; demais: pronto / não pronto).
- Só o líder muda o destino; os outros veem só leitura. Opção que algum membro não desbloqueou trava o início e mostra o
  nome de quem falta.
- Personagem: troca dentro da sala, pelo próprio cartão, abrindo a tela normal de seleção e voltando.
- O líder pode abrir as vagas livres pro matchmaking, escolhendo dupla, trio ou esquadrão.
- Início: mínimo 2 jogadores, todos os não-líderes prontos (o líder conta como pronto), sem contagem regressiva.
- Não confirmado no PokeBonk (decisão nossa): quando o líder muda o destino, o pronto dos outros é zerado.

## Comportamento alvo

### Tela Co-op (entrada)

- Painel **With friends**: botão único "Create room" + legenda "You pick the map, difficulty and hero inside the room." +
  separador "or" + "Join with a code" (caixa de código e botão Join, comportamento de hoje).
- "Create room" cria a sala na hora: privada, tamanho 4, mapa padrão, modo clássico, primeira dificuldade, herói = o
  escolhido atual (`ctx.obterHeroi()`). Saem os seletores de dificuldade, tamanho e pública/privada desta tela.
- Painel **Quick match**: chips Any / Duo / Trio / Squad (selecionam) + botão "Find match" (busca com o chip escolhido) +
  "N searching now" (contagem de hoje).
- Sai o rodapé "Your hero" / "Change hero".

### Sala

- Cabeçalho "Room" + código no subtítulo; "Leave room" no canto superior direito.
- **Destination** (esquerda): legenda "You decide" (líder) ou "Decided by the host"; bloco com a cor e o nome do mapa;
  seletores Map, Mode e Difficulty com setas ‹ › (só o líder; os outros veem o valor sem setas). Regras de hoje continuam
  (mapas de `Config.MapasCoop`, modos de `Config.OrdemModos`, modo com dificuldade fixa mostra "(fixed)").
- **Your team · n/4** (centro): 4 cartões lado a lado. Cartão de jogador: imagem do herói, selos "Host" (líder), "You" e
  "Change" (só no próprio), estado "Ready" / "Choosing…", nome do herói, nome do jogador. Clicar no "Change" abre a tela
  de heróis e volta pra sala (fluxo de hoje do "Change hero"). Vaga vazia: "Free slot — Invite with the code"; com vagas
  abertas: "Searching… — Filling from Quick match"; vaga além do tamanho: "Closed".
- **Room code** (direita): código em destaque, ainda selecionável pra copiar. **Open slots**: Off / On + Duo / Trio /
  Squad, só o líder (tamanhos menores ou iguais ao número atual de membros ficam desabilitados); os outros leem "Only the
  host can open slots.". Corresponde aos campos `publica` e `tamanho` da sala, agora alteráveis depois de criada.
- **Barra de baixo**: uma bolinha por vaga (preenchida = ocupada, verde = pronto), "n of m ready" + motivo do bloqueio,
  resumo do destino e um único botão grande: líder "Start!", demais "I'm ready!" / "Not ready".
- **Regras de início** (validadas no servidor): 2 ou mais jogadores (`Config`), todos os não-líderes prontos (o líder não
  tem botão de pronto e conta como pronto), mapa e dificuldade desbloqueados por todos os membros. Quando falta
  desbloqueio, a sala mostra o nome de quem falta.
- **Pronto zerado**: quando o líder muda mapa, modo ou dificuldade, o servidor zera o pronto dos não-líderes.

## Fora do escopo (extras do PokeBonk não pedidos)

Filtros de modo/mapa/dificuldade no Quick match, convites e lista de amigos/clã, chat da sala, voltar ao menu sem sair da
sala, voltar todos pra mesma sala depois da partida, voto pra tirar líder e prazo do líder. Emblema de clã: adiado.

## Execução

Lote com agente implementador e agente revisor (só leitura), sem Play (quem testa é o Diego). Ledger em
`.superpowers/sdd/2026-11-05-coop-sala-redesign/`. Textos novos em inglês com pares pt-BR em `Shared/Localizacao/PtBr`
(replicar idêntico no place Partida se o `Shared` mudar).
