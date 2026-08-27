from data.balance import XP_BASE, XP_GROWTH


def xp_necessario(level: int) -> int:
	return XP_BASE + (level - 1) * XP_GROWTH


def verificar_level_up(player) -> int:
	"""Sobe o player de nivel enquanto tiver XP suficiente. Retorna quantos niveis subiu."""
	niveis_subidos = 0
	while player.xp >= xp_necessario(player.level):
		player.xp -= xp_necessario(player.level)
		player.level += 1
		niveis_subidos += 1
	return niveis_subidos