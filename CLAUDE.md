# AnimeBonk — Regras do projeto

Jogo Roblox ("AnimeBonk") de sobrevivência roguelike 3D com tema anime, **inspirado no
gênero do Megabonk e do PokeBonk** (auto-ataque, hordas, level-up com escolhas, builds,
co-op). Desenvolvido
direto no Roblox Studio via MCP (sem Rojo). Regras trazidas do projeto `Table_Stories`
(2026-10-29) e adaptadas pra cá.

**Leia primeiro:** `docs/estado-do-projeto.md` (places, IDs, mapa dos scripts, status,
pendências). Referências dos jogos que inspiram: `docs/megabonk-referencia.md` e
`docs/pokebonk-referencia.md` (este é o modelo principal: co-op, sobrevivência, telas).
Design do AnimeBonk (quando existir): `docs/superpowers/specs/`.

## Como trabalhar comigo (fluxo)

- **Conversa sempre em português** (perguntas, resumos, comentários de código).
  Só os textos que aparecem no jogo são em inglês (ver "Textos do jogo").
- **Faça só o que eu pedi.** Se eu pedir X, implemente X — não implemente Y "de brinde"
  mesmo que pareça relacionado ou uma boa ideia.
- **Se você achar que vale a pena fazer algo além do pedido, comente comigo antes.**
  Não faça e me avise depois — pergunte antes de agir. Eu decido se quero ou não.
  Isso vale também pra ideias de design inspiradas no Megabonk: sugira, não implemente.
- **Não teste o jogo sozinho depois de implementar algo** (não dê Play pelo MCP, não
  tente simular gameplay, não gaste chamadas/tokens validando comportamento em runtime).
  Implemente a mudança, explique brevemente o que mudou e onde, e pare por aí.
  Eu mesmo testo no Studio e te conto o que aconteceu (erro, comportamento errado, etc).
  Exceção: ler o Output/console (`get_console_output`) quando eu pedir pra investigar
  um erro é ok.
- Se um pedido for ambíguo o suficiente pra eu ter que adivinhar escopo, pergunte antes
  de implementar em vez de assumir o caminho mais abrangente.

## Inspiração ≠ cópia

- Megabonk e PokeBonk são **referência de gênero e de mecânicas**, não algo a ser
  recriado. Personagens, armas, itens, mapas, chefes, nomes e visuais do AnimeBonk são
  **nossos**. Não reaproveitar nomes/textos/artes deles (ex.: "Tome", "Sir Oofie",
  Pokémon, "Liga", "Poké Bola", "Máquina do Bill").
- Tema anime **genérico/original**: nada de personagens, nomes, golpes ou visuais de
  animes existentes (Naruto, One Piece, etc.) — é propriedade de terceiros e o Roblox
  modera/derruba. Inspiração de estilo (arquétipos, poses, efeitos) pode; personagem de
  marca não.

## Fonte da verdade: o place no Studio

- Não usamos Rojo. Scripts, UI estática, mapa e decoração vivem **dentro do place**
  (`.rbxl` local / place publicado) e são criados/editados pelo MCP do Studio.
- Mudança feita pelo MCP só existe na sessão aberta do Studio até ser salva.
  Depois de qualquer alteração, avisar o usuário pra **salvar (Ctrl+S) ou publicar**.
- Antes de considerar uma tarefa pronta, pergunte: "isso está salvo no place, ou só
  existe na sessão aberta / só em runtime?" Coisas criadas durante o Play somem ao parar.
- **Backup = histórico de versões do Roblox.** Cada publicação do place gera uma versão
  restaurável no Creator Dashboard. Não há export de scripts nem git do código.
  Ao final de mudanças grandes, lembrar o usuário de **publicar** (não só Ctrl+S),
  porque só a publicação entra no histórico.

## Estrutura (no Studio)

- `ReplicatedStorage/Shared` — ModuleScripts de tipos, config, utilitários puros (sem estado de jogo)
- `ServerScriptService/Server` — Script de entrada + sistemas autoritativos (`Systems/`)
- `StarterPlayer/StarterPlayerScripts/Client` — LocalScript de entrada + controllers de
  UI/input/render (`Controllers/`)
- Sistemas/controllers são ModuleScripts que seguem o bootstrap de duas fases: exportam
  `init()` e `start()`, carregados pelos scripts de entrada (`Server` / `Client`).
  Não crie outro mecanismo de bootstrap paralelo nem Scripts soltos espalhados pelo place.
- Se o jogo tiver mais de um place (ex.: lobby + partida), o `Shared` existe em cada um:
  mudança num `Shared` precisa ser replicada no outro (registrar em `estado-do-projeto.md`).

## Scripts pelo MCP

- Scripts (`Script`, `LocalScript`, `ModuleScript`) são criados e editados pelo MCP
  do Studio (`execute_luau` no modo Edit para criar/definir `Source`, `multi_edit` para
  editar, `script_read`/`script_grep`/`script_search` para ler e procurar).
- Sempre ler o script atual antes de editar — nunca sobrescrever `Source` inteiro
  sem ter visto o conteúdo.
- Nunca criar/editar scripts com o Studio em Play (a mudança se perde ao parar).

## Mapa / cenário (geometria estática)

- Peças de mapa/cenário (chão, terreno, ruínas, decoração, santuários fixos) **não** são
  criadas por script em runtime. São criadas direto no Workspace pelo MCP (`execute_luau`
  no modo Edit, `insert_asset`, `generate_procedural_model`, etc.) e ficam salvas no place.
- Exceção natural do gênero: o que é **sorteado por partida** (posição de baús,
  santuários, portal do chefe, inimigos, drops) é spawnado por script a partir de
  pontos/modelos-molde que ficam salvos no place.
- Se o usuário já ajustou algo à mão no Studio, não mexer na posição/tamanho daquilo
  sem combinar antes.

## MCP do Roblox Studio

- Conectado no Claude Code (escopo user). Pra funcionar, no Studio:
  Assistant → … → Manage MCP Servers → Enable Studio as MCP server.
- Usado para tudo: scripts, mapa, decoração, UI estática. Depois avisar pra salvar (Ctrl+S).

## Textos do jogo

- Todo texto visível ao jogador (UI, avisos, prompts, nomes de personagens/armas/itens/
  mapas/chefes) é em **inglês** — idioma de origem pra tradução automática do Roblox.
- Continuam em português: IDs internos, chaves de config, nomes de instância/pasta,
  logs e comentários. A tela usa um campo `name` de exibição, nunca a chave interna.

## Luau / estilo

- Todo script novo começa com `--!strict`.
- Tabs para indentação, sem exceções manuais.
- Tipos que cruzam a fronteira cliente/servidor (payload de remotes, schema de
  perfil) vivem em `ReplicatedStorage/Shared/Types` — as duas pontas usam o mesmo tipo.
- Sem `_G` ou globais soltas — compartilhar estado via ModuleScripts.
- UIs dinâmicas são montadas pelos Controllers via `Instance.new`; UIs estáticas podem
  ficar no place (StarterGui), criadas pelo MCP.
- Conteúdo do jogo (armas, itens, personagens, inimigos, upgrades) é **dado**, em
  ModuleScripts de definição no `Shared` (uma tabela por entidade, chave interna em
  português/código + `name` em inglês). Sistemas leem as definições; não espalhar
  `if arma == "x"` pelo código.

## Segurança (servidor autoritativo)

- Todo RemoteEvent/RemoteFunction é validado no servidor: tipo, formato e
  plausibilidade do payload. Nunca confie em valor vindo do cliente (moeda, XP,
  posição, dano, acerto, item escolhido, quantidade, resultado de sorteio).
- Cliente só *pede* uma ação; quem decide o resultado é o servidor
  (dano e acerto das armas, drop de XP/ouro, ofertas de level-up, sorteio de baú/
  santuário, compra na loja, desbloqueios).
- Escolha de upgrade: o servidor gera as opções e guarda; o cliente só manda o índice
  escolhido, que é validado contra as opções guardadas.
- Rate-limit em remotes que o cliente pode chamar repetidamente.

## Performance (crítico neste gênero: centenas de inimigos e projéteis)

- Sempre desconectar `Connection`s de `RunService`/eventos quando o objeto que
  as criou é destruído — conexão pendurada é vazamento de memória.
- Evitar alocação por frame em loops de `RunService.Heartbeat/RenderStepped`.
- Inimigos/projéteis/orbes de XP: usar **pool** (reaproveitar instâncias) em vez de
  criar/destruir toda hora; um loop central por sistema, não um script por inimigo.
- Teto de inimigos vivos e de projéteis configurável no `Config`.
- O ModuleScript `Config` guarda valores ajustáveis; não hardcode números mágicos
  espalhados pelo código.

## Dados (DataStore)

- Autosave + save em `BindToClose`, nunca só um dos dois.
- Sempre com retry/backoff em chamadas de DataStore — nunca falha silenciosa.
- Mudança de schema de perfil (em `Types`) precisa de versionamento e migração,
  não substituição direta do formato antigo.

## Git / GitHub

- O projeto é desenvolvido em dupla (Diego + um amigo) com repositório no GitHub
  (2026-11-05: o Diego vai criar o repositório). Enquanto a pasta não for um repositório git
  com remote configurado, as duas regras abaixo não se aplicam: avisar o Diego em vez de
  criar o repositório por conta própria.
- O repositório guarda só o que existe em arquivo (`CLAUDE.md`, `docs/`, `arte/`, config).
  O código, a UI e o mapa continuam vivendo nos places e **não** vão pro GitHub.
- **Antes de mexer em qualquer coisa** (início de sessão ou de tarefa): conferir se o GitHub
  tem algo novo (`git fetch` + `git status`) e, se tiver, dar `git pull` antes de ler a
  documentação ou alterar arquivos, pra trabalhar em cima da versão atualizada. Se o pull
  der conflito ou houver mudança local que o impeça, parar e avisar o Diego.
- **Ao terminar uma feature** (ou um conjunto de mudanças acumuladas): fazer commit e
  `git push` sozinho, sem pedir confirmação. Não subir a cada alteração pequena — juntar e
  subir quando a feature estiver concluída. Sempre `git pull` antes do `git push`; push
  direto no branch principal, sem PR.
- Conta pessoal **DiegoFeBrandao** no `gh` (não a `Diegobrandao-aramis` do trabalho),
  commits focados no "porquê", sem `.rbxl*`.
- Ao mudar algo relevante no jogo (script novo, place novo, etapa concluída), atualizar
  `docs/estado-do-projeto.md`.

## CI / GitHub Actions

- **Não usar GitHub Actions.** Nenhum workflow de CI/CD deve ser criado, mantido ou
  executado no repositório.

## Economia de contexto

- Testes: quem testa sou eu, manualmente. Não rode Play nem testes para conferir o
  trabalho; entregue um roteiro de teste manual curto e objetivo no final.
- Capturas de tela: não tire capturas por conta própria. Só tire quando eu pedir
  explicitamente, ou quando a tarefa depender de uma decisão visual minha (ex.: prévia
  de um ícone ou modelo novo). Para conferir posições e tamanhos, use os números
  (Position, Size, distâncias).
- Leitura de scripts: não leia scripts grandes inteiros. Primeiro procure pelo nome da
  função ou trecho e leia só as partes necessárias. Leia o arquivo inteiro só se for
  indispensável e diga por quê.
- Consultas ao Studio pelo MCP: faça só as necessárias e evite repetir consultas cujo
  resultado já está na conversa.
- Respostas: seja direto. Resumo do que mudou, lista linha a linha só para scripts do
  Diego, e o roteiro de teste.
