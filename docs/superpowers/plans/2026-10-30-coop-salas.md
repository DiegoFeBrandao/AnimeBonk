# Co-op com salas (código, matchmaking, servidor reservado) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Amigos conseguirem jogar juntos de propósito: no Menu, **criar sala** (escolhe
mapa/dificuldade, recebe código de 6 letras, convida), **entrar com código**, **matchmaking**
por tamanho (Any / Duo / Trio / Squad) com "N searching", lobby da sala (lista, pronto,
líder inicia), **teleporte em grupo** pra um servidor **reservado** da Partida, e na Partida
a tela **"End Match / Revive All"** (15 s) quando todos caem, mais a **pausa de equipe por
votação** (5 min por partida) e o **ranking cooperativo** por tamanho × dificuldade × mapa.
Pedido do Diego (2026-10-30): "Falando em coop e outros modos no MENU, o que falta para a
gente fazer?" — ele aceitou fechar o solo primeiro; este é o lote seguinte.

**Architecture:**
- **Salas** no Menu: `SalaSystem` (servidor do Menu) com estado em `MemoryStoreService`
  (`SortedMap "Salas"`: código → `{ lider, membros {userId}, mapa, dificuldade, tamanhoMax,
  publica, criadaEm, jobId }`, TTL 30 min) + `MessagingService` ("Salas") para sincronizar
  entre servidores do Menu; código de 6 letras A–Z sem ambíguas (sem I/O/0/1), sorteado até
  não colidir; remotes `SalaCriar`, `SalaEntrar(codigo)`, `SalaSair`, `SalaPronto(bool)`,
  `SalaIniciar`, `SalaConfig(mapa, dificuldade, publica)`, `SalaBuscar(tamanho)` (matchmaking:
  entra na 1ª sala pública com vaga do tamanho pedido ou cria uma), s→c `SalaEstado`.
  Validação: só o líder configura/inicia; tamanho ≤ 4; rate-limit 1 s (criar 10 s);
  textos nenhum (só código gerado). Expulsar membro = líder; líder sai → passa pro mais antigo.
- **Teleporte**: `TeleportService:ReserveServer(PlaceIdPartida)` → `TeleportAsync(place,
  membros, options{ReservedServerAccessCode, TeleportData = { sala = codigo, heroiId por
  jogador, dificuldade, mapa }})`; retry 3× com backoff; falha parcial = avisa a sala.
  Partida recebe `TeleportData.sala` → `PartidaSystem` espera até `Config.EsperaSala 20 s`
  pelos membros antes de começar (ou todos chegaram), mostra "Waiting for party N/M".
- **Partida co-op**: `End Match / Revive All` (todos caídos: timer 15 s; qualquer um pode
  pagar `Config.ReviveAllEssencia` em Essência para reviver todos com 50 % HP, 1× por
  partida; se ninguém pagar → fim); pausa de equipe por votação (`VotarPausa`: maioria
  simples, orçamento 5 min por partida, congela como a pausa solo); ranking cooperativo
  `OrderedDataStore("CoopTempo_<tamanho>_<dif>_<mapa>")` escrito no fim pelo servidor
  (melhor tempo de vitória do time; chave = jobId + lista de userIds ordenada).
- **Menu**: telas `Co-op` (Create room / Join with code / Quick match por tamanho),
  `Lobby` (código grande com botão copiar, lista de membros com herói/pronto, config do líder,
  Start), `Leaderboard` ganha abas Solo / Duo / Trio / Squad. Tudo no tema do redesign.
- Perfil: nada novo (schema v6).

**Spec:** §9 (menus), PokeBonk §4 (co-op), pesquisa §4/§5 (co-op: reanimar, pausa por votação; **não** existe "Revive All" pago no PokeBonk — o nosso usa Essência, decisão da spec).

## Review Focus
1. Dois jogadores entrando com o mesmo código no mesmo instante em servidores diferentes do Menu: contagem de vagas nunca passa do máximo (`UpdateAsync` no MemoryStore).
2. Líder cai/sai: sala continua com novo líder; sala vazia some; TTL expira; código reutilizado só depois de expirar.
3. Teleporte falha pra 1 membro: os outros chegam, a Partida espera 20 s e começa; o que falhou recebe mensagem e a sala continua no Menu.
4. `Revive All` cobra Essência 1×, nunca negativa, idempotente com 2 cliques; voto de pausa não ultrapassa 5 min; solo não vê nada disso.
5. Ranking coop só servidor, só vitória, chave estável; jogador sozinho em servidor reservado conta como Solo.

### Task 1: `SalaSystem` + remotes + `TesteLogica` (código, estado puro em `Logica/Sala`).
### Task 2: Teleporte em grupo (reservado) + espera na Partida (`PartidaSystem`, `TeleportData.sala`).
### Task 3: Partida — End Match / Revive All, pausa por votação, ranking coop.
### Task 4: Menu — telas Co-op / Lobby / abas do Leaderboard (tema novo).
### Task 5: teste (Studio: só lógica e UI; publicado com 2 contas: o Diego) + revisão + docs.
