from data.balance import ENEMY_BASE_STATS

class Enemy:
	def __init__(self, stats=None):
		base_stats = ENEMY_BASE_STATS if stats is None else stats

		self.hp = base_stats["hp"]
		self.max_hp = base_stats["max_hp"]
		self.atk = base_stats["atk"]
		self.def_ = base_stats["def_"]
		self.speed = base_stats["speed"]
		self.luck = base_stats["luck"]
		self.level = base_stats["level"]

	def esta_vivo(self):
		return self.hp > 0

	def escolher_acao(self):
		return "atacar"