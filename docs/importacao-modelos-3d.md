# Importação dos modelos 3D (Claude Design → Roblox)

Combinado em 2026-11-26. O Diego criou no Claude Design objetos 3D (baús, recursos, chakra stones,
estruturas) e personagens com animações e VFX. Nada foi importado ainda.

## O que existe do lado do Diego

- **Objetos**: a maioria tem animação própria (ex.: baú com `Closed` e `Open`).
- **Personagens**: `Idle`, `Walk`, `BasicAttack`, `Hit`, `Skill1`, `Skill2`, `Skill3`, `Ultimate`, `Victory`.
- **VFX**: detalhes de efeito por skill.
- O Claude Design oferece download em **GLB** ou **OBJ**. Decisão: **GLB** (OBJ não leva esqueleto,
  animação nem textura embutida), um GLB por modelo com todas as animações dentro.

## Regras do Roblox conferidas na documentação (2026-11-26)

- Cada malha: no máximo **20.000 triângulos**.
- Rig: no máximo 4 ossos por vértice; osso raiz em 0,0,0 e sem influência; ossos com escala 1 e rotação 0.
- **Uma animação por arquivo importado** ("single track"): os clipes do GLB precisam ser separados
  antes de importar (dá pra fazer no Blender).
- Cor só de material (sem textura) costuma se perder na importação (peça chega cinza): pedir cor em
  textura embutida.
- Animação em glTF/GLB: a página do 3D Importer lista como suportada; a de especificações só cita FBX.
  **Não testado.** Se não entrar, converter GLB → FBX no Blender.
- VFX (partículas, brilhos, rastros) não atravessam a importação: são refeitos no jogo a partir da ficha.
- Upload cria asset permanente (só apaga pelo Creator Dashboard).

## Próximo passo

1. Diego pede a exportação ao Claude Design com o prompt abaixo.
2. Baixar primeiro **um baú e um personagem** e importar só esses dois, pra validar cor, rig e
   animação antes de gerar o resto.
3. Se o Claude Design não entregar animação em osso nos objetos: tampa como peça separada com pivô
   na dobradiça e a abertura feita no jogo.

## Prompt para o Claude Design

```
Preciso exportar os modelos e personagens que você criou para importar no Roblox Studio.
Siga estas regras e, se alguma não for possível, me avise qual e por quê em vez de adaptar em silêncio.

FORMATO
- Um arquivo .glb por modelo (objeto ou personagem), com texturas embutidas e TODAS as animações daquele modelo dentro.
- Nada de câmeras, luzes ou objetos auxiliares dentro dos arquivos.

CORES
- Não deixe cor só como cor do material. Converta (bake) todas as cores para uma textura de cor base (PNG, até 1024x1024) com UV, embutida no arquivo.
- Se houver normal/roughness/metalness/emissivo, embuta também; efeitos procedurais ou de shader precisam virar textura.
- Um material por malha, sempre que possível.

GEOMETRIA
- Cada malha com no máximo 20.000 triângulos (se passar, divida em partes nomeadas Nome_Part1, Nome_Part2...).
- Malhas fechadas, com volume, sem faces de espessura zero, normais para fora.
- Transformações aplicadas (escala 1, rotação 0), pivô na base do objeto, no centro.
- Unidades em metros, eixo Y para cima, frente do modelo virada para -Z.
- Nome único e descritivo para cada malha, material e osso, sem acento nem espaço.

RIG (personagens e objetos animados)
- Toda animação precisa estar em OSSOS. Se algo foi animado movendo a peça direto, por código ou por shader, converta para esqueleto com keyframes.
- Objetos animados: um esqueleto simples, um osso por parte móvel (ex.: baú = raiz + osso da tampa, com o osso na dobradiça), cada parte 100% presa ao seu osso.
- Um esqueleto só por modelo, osso raiz na origem (0,0,0), sem vértices influenciados pela raiz.
- Ossos com escala 1 e rotação 0 na pose de descanso (personagens em T-pose ou A-pose).
- No máximo 4 ossos influenciando cada vértice.

ANIMAÇÕES
- Cada animação como um CLIPE SEPARADO E NOMEADO dentro do .glb (não uma linha do tempo única com tudo emendado).
  Personagem: Idle, Walk, BasicAttack, Hit, Skill1, Skill2, Skill3, Ultimate, Victory.
  Baú e similares: Closed, Open (e outras que existirem).
- Todo clipe começa no tempo 0 e anima todos os ossos que ele usa (sem depender da pose deixada por outro clipe).
- Animação "assada" em keyframes nos ossos (bake): sem IK, constraints, drivers ou morph targets/shape keys.
- 30 fps. Idle, Walk e Closed em loop perfeito (primeiro e último frame iguais).
- Animações no lugar: o modelo não sai da origem (sem deslocamento da raiz), nem no Walk nem nas skills.

VFX (não vão no arquivo; serão refeitos no Roblox)
- Não inclua partículas, brilhos, rastros ou projéteis nos arquivos.
- Para cada skill/ultimate/objeto, escreva uma ficha: nome, cada efeito que aparece, cores em hex, forma e tamanho aproximado em metros,
  de onde nasce (qual osso ou ponto), para onde vai, quanto dura, em que segundo da animação começa e termina.
- Se algum efeito usa imagem (textura de fumaça, faísca, símbolo), exporte cada uma como PNG com fundo transparente.
- Informe também, para cada ataque e skill, o segundo exato do "impacto" (momento em que o golpe acerta).

LISTA DE CONFERÊNCIA (manifest.json ou .txt na raiz)
Para cada arquivo: nome das malhas, triângulos de cada uma, tamanho em metros (largura/altura/profundidade), materiais com a cor principal em hex,
lista de ossos e, para cada clipe de animação, nome, duração em segundos, se é loop e o segundo do impacto.

ENTREGA
Um .zip com pastas: objetos/, personagens/, vfx/ (fichas e PNGs) e o manifesto na raiz.
```
