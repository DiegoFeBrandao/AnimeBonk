# Etapa 5b — Place de Menu — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** O jogador entra no place **Menu** (placeId 108606222274512), vê sua Essência e
estatísticas, escolhe o herói (Ryuga liberado; Kaizo/Haruto trancados até o desbloqueio) e
aperta **Play**, que o teleporta pro place **Partida** (108221889486707) já com o herói
escolhido (sem a tela "Choose your hero").

**Architecture:** O Menu tem o mesmo bootstrap (`Server`/`Client` em duas fases) e uma cópia
fiel do `Shared` necessário (`Types`, `Config`, `Remotes`, `Definicoes/Herois`,
`Definicoes/Golpes`, `Logica/Perfil`) + `PerfilSystem` copiado do Partida (mesmo DataStore
`"Perfil"`, mesma chave `u<UserId>`). `MenuSystem` (servidor) recebe `IrParaPartida(heroiId)`,
valida (herói existe e está em `perfil.desbloqueios`), salva o perfil e teleporta com
`TeleportService:TeleportAsync(108221889486707, {player}, options)` com `TeleportData =
{ heroiId = ... }`. No Partida, `PartidaSystem` lê `player:GetJoinData().TeleportData.heroiId`
no `PlayerAdded`/`escolheu` e escolhe automaticamente (mesma validação do remote).

**Spec:** §9 (menus), §10 (desbloqueios), §13 item 5.

## Global Constraints
- Mesmas regras (CLAUDE.md). Textos em inglês. `--!strict`. Mudança no `Shared` do Partida tem
  que ser replicada no Menu (registrar em `estado-do-projeto.md`).
- TeleportService não funciona no Studio: testar o teleporte só publicado. No Studio o botão
  Play mostra "Teleport only works in the published game" (warn no Output).

## Review Focus
1. `IrParaPartida` com herói inválido/trancado → recusado; rate-limit.
2. Perfil ainda carregando ao apertar Play → espera/recusa, nunca teleporta sem salvar.
3. TeleportData forjado (jogador entra direto no Partida sem passar pelo Menu) → `heroiId` é só
   um pedido: validado como o remote; se inválido, cai na tela "Choose your hero".
4. Kaizo/Haruto trancados mostram o desafio de desbloqueio ("Win Cherry Village" / "Defeat 2,000
   enemies") — os desbloqueios em si entram com conquistas (etapa 6); por enquanto
   `perfil.desbloqueios` só tem Ryuga, e o Partida libera Kaizo ao vencer a zona 1 e Haruto ao
   vencer a região (registrar em `PerfilSystem.registrarFim`/`ZonaSystem`).
5. Menu sem DataStore (Studio) → tela funciona com perfil em memória (warn).

### Task 1 (Menu): replicar Shared + bootstrap + PerfilSystem
### Task 2 (Menu): MenuSystem (remote `IrParaPartida`, validação, teleporte) + MenuController
  (tela: título "AnimeBonk", Essence/partidas/vitórias, 3 cartões de herói com estado
  locked/unlocked e o desafio, botão Play)
### Task 3 (Partida): auto-escolha por TeleportData; desbloqueio de Kaizo (vencer zona 1 = passar
  pelo portal da Vila) e Haruto (vitória) gravado no perfil; replicar no Menu o que mudar no Shared.
### Task 4: teste em Play nos dois places (sem teleporte) + revisão + docs
