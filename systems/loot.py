import random

from data.items import CONSUMABLE_ITEMS
from entities.item import Item


def gerar_loot(enemy):
	"""Generate consumable drops and XP from a defeated enemy.

	Returns:
		tuple[list[Item], int]: (dropped_items, xp_reward)
	"""
	nivel = int(getattr(enemy, "level", 1))
	luck = int(getattr(enemy, "luck", 0))
	atk = int(getattr(enemy, "atk", 0))
	defesa = int(getattr(enemy, "def_", 0))

	# XP scales primarily with level, with a small influence from combat stats.
	xp = max(1, 8 + (nivel * 4) + atk + (defesa // 2))

	itens = []
	pocao_data = CONSUMABLE_ITEMS["pocao"]

	# Base drop chance grows with enemy level and luck.
	chance_pocao = min(85, 35 + (nivel * 8) + (luck * 3))
	if random.randint(1, 100) <= chance_pocao:
		itens.append(Item(**pocao_data))

	# Higher-level enemies can drop an extra potion.
	chance_extra = min(40, max(0, (nivel - 2) * 12))
	if random.randint(1, 100) <= chance_extra:
		itens.append(Item(**pocao_data))

	return itens, xp
