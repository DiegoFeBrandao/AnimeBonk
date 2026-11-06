# Polimento UI v2 — feedback do Diego após testar a fase 2 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Atender o feedback do Diego (2026-10-30, depois de testar): (1) **mapa do Tab/M
bonito** (imagem estática por zona com relevo sombreado, penhascos, água e caminhos, em vez
da grade de quadrados); (2) **minimapa** mostrando o mapa de verdade dentro do círculo, sem
fundo preto maior que ele; (3) **herói mais rápido** (velocidade de andar base +25 %);
(4) **imagens** para golpes, ultimates e pergaminhos (fim dos "KR[]"/"ET[]": o `[]` é um
glifo que a fonte não tem); (5) carta de **golpe sem a linha "Affects"** (só pergaminhos e
itens); (6) **barra do topo** (zona, timer, contadores) encostada no topo da tela;
(7) **ultimate redonda** com ícone e anel de carga; (8) **barra de recarga** em cada slot de
golpe (preenche até o próximo disparo, como no PokeBonk, sem números); (9) **teclas
desenhadas**: todo `[ENTER]`, `[E]`, `[F]`, `[Tab]`, `[M1]` no texto vira uma tecla desenhada
com o nome dentro (padrão do Table Stories, `Modulos/TextoComTeclas`), nos 2 places.
Ele gostou do Menu e da cena 3D: não mexer.

**Architecture:**
- **Imagens**: pipeline local → Roblox. Um servidor HTTP local (`python -m http.server` numa
  pasta do scratchpad) serve PNGs e `mcp__roblox-studio__upload_image` sobe por URL
  `http://localhost:<porta>/<arquivo>.png` e devolve `rbxassetid`. Os ids vão para
  `Definicoes/Golpes[id].icone`, `Ultimates[heroi].versoes[i].icone`, `Pergaminhos[id].icone`
  (campo já existe nos itens; criar nos demais), e para `Definicoes/Zonas[id].mapaImagem`.
  - Ícones: **folhas de sprites 3×3** (1024×1024, 9 ícones de 320 px com margem) geradas
    por `mcp__claude_ai_Canva__generate-image` (estilo: ícone de jogo anime/ninja, fundo
    transparente ou chapado escuro uniforme, traço grosso, cores vivas, sem texto), uma folha
    por grupo; no Roblox, `ImageRectOffset/ImageRectSize` seleciona o ícone. Se o Canva não
    responder, fallback: ícones vetoriais simples desenhados em Python/PIL (forma + cor do
    elemento + símbolo), mesma folha 3×3.
  - Mapas: decodificar a grade de `Shared/Mapa/Alturas` (base 64, 2 chars/amostra; ler o
    `Source` com `script_read` e decodificar em Python), gerar PNG 1024×1024 por zona com
    hillshade (luz NO), cor por altura (grama → verde claro no alto, mais escuro embaixo),
    faces > 25° em marrom/rocha, água (`Zonas.lagoas` + riachos) azul, caminhos entre
    pontos-chave em bege, borda fora das paredes escurecida, estilo "mapa de jogo" (traço nos
    degraus). Subir como asset; `MapaController` e minimapa usam `ImageLabel` com o asset;
    a grade de Frames vira fallback só se o asset falhar. Ícones por cima como hoje.
- **Minimapa**: `ImageLabel` circular (UICorner 1,0 + `ClipsDescendants`) mostrando o recorte
  do mapa ao redor do jogador (posição/rotação da imagem calculadas por frame, só a imagem),
  seta no centro, ícones descobertos e pontos de inimigo; sem Frame preto por fora; anel fino
  dourado; N/S/E/W.
- **Slots de golpe**: ícone + nível + **barra de recarga** (preenche da esquerda pra direita
  no tempo `cooldown / multVelAtaque`, reiniciada no evento de disparo que o cliente já recebe
  para desenhar o efeito; se não houver evento por golpe, acrescentar `golpeId` ao payload
  existente). Ultimate: círculo com ícone, anel de carga (`UIGradient` rotacionado ou 2
  meio-arcos), "R" como tecla desenhada.
- **Teclas**: `Client/Util/Teclas` nos 2 places: `desenhar(container, texto)` quebra o texto
  em runs e cria `TextLabel`s + keycaps (Frame com UICorner 6, fundo claro, sombra 2 px em
  baixo, UIStroke, texto `GothamBlack` 11–13, largura automática; mouse = ícone de mouse com
  botão destacado); aplicado em cartas (Reroll/Skip/Ban, 1–4), pausa (dicas), prompts de
  objeto/baú/mercador, HUD (R, Tab, M, P), tela de fim (Enter), Menu (Enter, Esc, Backspace).
- **Topo**: painel zona/timer/contadores com `Position.Y = Inset + 4` e altura menor; cartão
  do herói e minimapa alinhados no mesmo topo.
- `Config.VelocidadeBase` ×1,25 (e o que depender: velocidade de projétil inimigo não muda).

**Spec:** §9 (HUD); telas 20–24 do PokeBonk como referência de estrutura.

## Review Focus
1. Nenhum asset falhando no console (`rbxassetid` inválido = ícone em branco): fallback por letra ASCII quando `icone` vazio ou falhar.
2. Minimapa sem alocação por frame (só muda `Position`/`Rotation` da imagem).
3. Barra de recarga nunca dessincroniza mais de 1 disparo (reinicia em cada evento; com +VelAtaque recalcula).
4. Teclas desenhadas em celular: viram ícone de toque ou somem (sem "[E]" solto).
5. `Shared` idêntico nos 2 places; nada de upload de imagem de terceiros (tudo gerado aqui).

### Task 1: Pipeline de imagens (servidor local, Canva/PIL, upload) + mapas das 4 zonas + ícones (18 golpes, 9 ultimates, 24 pergaminhos) + campos `icone`/`mapaImagem` nos 2 places.
### Task 2: Mapa Tab/M e minimapa com imagem; topo; velocidade.
### Task 3: Slots com barra de recarga, ultimate redonda, cartas sem "Affects" em golpe, `Util/Teclas` nos 2 places aplicado em tudo.
### Task 4: teste em Play (ícones carregam, mapa aparece, barra de recarga bate com o disparo, teclas desenhadas, 844×390) + docs.
