import random

from data.items import ARMOR_ITEMS, CONSUMABLE_ITEMS, TOTEM_ITEMS, WEAPON_ITEMS
from entities.item import Item


def gerar_loot(enemy, player=None):
	"""Generate consumable drops and XP from a defeated enemy.

	Returns:
		tuple[list[Item], int]: (dropped_items, xp_reward)
	"""
	nivel = int(getattr(enemy, "level", 1))
	luck = int(getattr(player if player is not None else enemy, "luck", 0))
	atk = int(getattr(enemy, "atk", 0))
	defesa = int(getattr(enemy, "def_", 0))

	# XP scales primarily with level, with a small influence from combat stats.
	xp = max(1, 8 + (nivel * 4) + atk + (defesa // 2))

	itens = []

	# Base drop chance grows with enemy level and luck.
	chance_pocao = min(85, 35 + (nivel * 8) + (luck * 3))
	if random.randint(1, 100) <= chance_pocao:
		itens.append(Item(**CONSUMABLE_ITEMS["pocao"]))

	# Higher-level enemies can drop an extra potion.
	chance_extra = min(40, max(0, (nivel - 2) * 12))
	if random.randint(1, 100) <= chance_extra:
		itens.append(Item(**CONSUMABLE_ITEMS["pocao_grande"]))

	# Equipamentos e totens aparecem com mais frequencia em ondas maiores.
	chance_equipamento = min(55, 10 + (nivel * 8) + (luck * 2))
	if random.randint(1, 100) <= chance_equipamento:
		catalogo = WEAPON_ITEMS if random.randint(0, 1) == 0 else ARMOR_ITEMS
		itens.append(Item(**random.choice(list(catalogo.values()))))

	chance_totem = min(35, max(0, (nivel - 1) * 8 + luck))
	if random.randint(1, 100) <= chance_totem:
		itens.append(Item(**random.choice(list(TOTEM_ITEMS.values()))))

	return itens, xp
