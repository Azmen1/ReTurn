import random

from data.balance import ENEMY_STAT_RANGE_BY_TIER, WAVE_TIER_SIZE, XP_BASE, XP_GROWTH


def calcular_tier(wave_number: int) -> int:
	return (wave_number - 1) // WAVE_TIER_SIZE + 1


def gerar_stats_inimigo(tier: int) -> dict:
	tier_disponivel = min(max(1, tier), max(ENEMY_STAT_RANGE_BY_TIER))
	faixas = ENEMY_STAT_RANGE_BY_TIER[tier_disponivel]
	stats = {stat: random.randint(*faixa) for stat, faixa in faixas.items()}
	stats["max_hp"] = stats["hp"]
	stats["level"] = tier_disponivel
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