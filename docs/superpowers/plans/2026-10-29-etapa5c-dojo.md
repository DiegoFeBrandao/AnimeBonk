# Etapa 5c — Dojo de Treino (melhorias permanentes com Essência) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** No Menu, a tela **Dojo** vende melhorias permanentes pequenas com Essência
(spec §10): Power (+2% dano/nível), Vitality (+3% HP máx.), Swiftness (+2% velocidade),
Wisdom (+3% XP), Fortune (+1% crítico), Magnet (+5% coleta) — 5 níveis cada; custo
`DojoCustoBase × (nível+1)` (50, 100, 150, 200, 250). No Partida, os níveis do Dojo entram
como bônus no herói desde o início da partida.

**Architecture:** `Types.Perfil` ganha `dojo: { [string]: number }` (schema **v2**:
`Perfil.VERSAO = 2`, `migrar` cria `dojo = {}` quando falta). `Definicoes/Dojo` (dado:
`{ name, descricao, stat, porNivel, nivelMax }`). Menu: `DojoSystem` com remote
`ComprarDojo(id)` (rate-limit, id existe, nível < max, Essência suficiente → desconta,
sobe nível, `rev += 1`, `PerfilSystem.salvarAgora`, envia `Perfil`). Partida:
`ItemSystem.recalcular` soma os bônus do Dojo (`PerfilSystem.obter(player).dojo`) na mesma
tabela `e.bonus` (stats já entendidos por `Logica/Dano`: Dano, HpMax, Velocidade, Xp,
Critico, Coleta) — e é chamado em `HeroiSystem.escolheu`. `Shared` replicado nos 2 places.

## Review Focus
1. Comprar sem Essência / nível máx. / id inválido / spam → recusado; Essência nunca negativa.
2. Perfil v1 salvo (sem `dojo`) → migra pra v2 sem perder nada; servidor v1 lendo v2 → não salva (regra da 5a).
3. Bônus do Dojo aplicado já no nível 1 da partida (HP máx. visível na HUD) e não some ao pegar item.
4. Compra enquanto o perfil ainda carrega → recusada com mensagem.
5. Dojo visível no Menu com níveis e preços corretos; botão desabilitado quando não dá pra comprar.

### Task 1: Shared (Types v2, Logica/Perfil migrar, Definicoes/Dojo, Config.DojoCustoBase 50) nos 2 places + TesteLogica (migrar v1→v2).
### Task 2 (Menu): DojoSystem + tela Dojo no MenuController (lista das 6 melhorias: nome, descrição, nível x/5, preço, botão Buy; teclas opcionais).
### Task 3 (Partida): ItemSystem.recalcular soma Dojo; chamar em HeroiSystem.escolheu; PerfilSystem.obter já existe.
### Task 4: teste em Play nos 2 places + revisão + docs.
