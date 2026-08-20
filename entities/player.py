from data.balance import PLAYER_BASE_STATS

class Player:
	def __init__(self, stats=None):
		base_stats = PLAYER_BASE_STATS if stats is None else stats

		self.hp = base_stats["hp"]
		self.max_hp = base_stats["max_hp"]
		self.atk = base_stats["atk"]
		self.def_ = base_stats["def_"]
		self.speed = base_stats["speed"]
		self.luck = base_stats["luck"]
		self.level = base_stats["level"]
		self.xp = base_stats["xp"]
		self.inventory = []