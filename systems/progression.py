import random
from math import floor

from data.balance import (
	ENCOUNTER_CATEGORY_MODIFIERS,
	ENCOUNTER_SEQUENCE,
	ENEMY_TIER_REFERENCES,
	INTERPOLATION_WAVES,
	ARCHETYPE_DEFINITIONS,
	BOSS_DEFINITIONS,
	COMMON_ARCHETYPES_BY_TIER,
	ELITE_ARCHETYPE_BY_TIER,
	ELITE_NAMES,
	ELITE_PATTERNS,
	PATTERNS,
	TOTAL_WAVES,
	WAVE_TIER_SIZE,
	XP_BASE,
	XP_GROWTH,
)


def calcular_tier(wave_number: int) -> int:
	return (wave_number - 1) // WAVE_TIER_SIZE + 1


def dados_encontro(wave_number: int, rng=None) -> dict:
	if not 1 <= wave_number <= TOTAL_WAVES:
		raise ValueError("A campanha padrao possui apenas 20 ondas")
	tier = calcular_tier(wave_number)
	position = (wave_number - 1) % WAVE_TIER_SIZE + 1
	category = ENCOUNTER_SEQUENCE[position - 1]
	rng = random if rng is None else rng
	if category == "CHEFE":
		boss = BOSS_DEFINITIONS[wave_number]
		archetype = boss["archetype"]
		name = boss["name"]
		pattern = boss["pattern"]
	elif category == "ELITE":
		archetype = ELITE_ARCHETYPE_BY_TIER[calcular_tier(wave_number)]
		name = ELITE_NAMES[archetype]
		pattern = ELITE_PATTERNS[archetype]
	else:
		candidates = COMMON_ARCHETYPES_BY_TIER[calcular_tier(wave_number)][position - 1]
		if isinstance(candidates, str):
			archetype = candidates
		else:
			archetype = rng.choice(candidates)
		name = ARCHETYPE_DEFINITIONS[archetype]["name"]
		pattern = PATTERNS[archetype]
	return {
		"wave": wave_number,
		"tier": tier,
		"position": position,
		"category": category,
		"archetype": archetype,
		"name": name,
		"pattern": pattern,
	}


def _interpolar(referencias: dict, wave_number: int) -> dict:
	marcos = INTERPOLATION_WAVES
	if wave_number >= marcos[-1]:
		return dict(referencias[16])
	for inicio, fim in zip(marcos, marcos[1:]):
		if inicio <= wave_number <= fim:
			fracao = (wave_number - inicio) / (fim - inicio)
			return {
				stat: referencias[inicio][stat] + (referencias[fim][stat] - referencias[inicio][stat]) * fracao
				for stat in referencias[inicio]
			}
	return dict(referencias[1])


def _referencias_por_onda() -> dict:
	return {wave: ENEMY_TIER_REFERENCES[calcular_tier(wave)] for wave in INTERPOLATION_WAVES}


def arredondar_atributo(valor: float, minimo: int) -> int:
	return max(minimo, int(floor(valor + 0.5)))


def gerar_encontro(wave_number: int, rng=None) -> dict:
	dados = dados_encontro(wave_number, rng)
	rng = random if rng is None else rng
	base = _interpolar(_referencias_por_onda(), wave_number)
	modificador = ENCOUNTER_CATEGORY_MODIFIERS[dados["category"]]
	arquetipo = ARCHETYPE_DEFINITIONS[dados["archetype"]]
	stats = {}
	for stat, valor in base.items():
		valor_modificado = valor * modificador.get(stat, 1.0)
		if stat == "speed":
			valor_modificado += arquetipo["speed"]
		else:
			valor_modificado *= arquetipo.get(stat, 1.0)
		limite = 1 if stat in ("hp", "atk", "speed") else 0
		stats[stat] = arredondar_atributo(valor_modificado, limite)
	stats["max_hp"] = stats["hp"]
	stats["level"] = dados["tier"]
	stats.update(dados)
	return stats


def xp_necessario(level: int) -> int:
	return XP_BASE + (level - 1) * XP_GROWTH


def verificar_level_up(player) -> int:
	#Sobe o player de nivel enquanto tiver XP suficiente. Retorna quantos niveis subiu.
	niveis_subidos = 0
	while player.xp >= xp_necessario(player.level):
		player.xp -= xp_necessario(player.level)
		player.level += 1
		niveis_subidos += 1
	return niveis_subidos