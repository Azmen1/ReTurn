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
		self.wave = base_stats.get("wave")
		self.tier = base_stats.get("tier", self.level)
		self.position = base_stats.get("position")
		self.category = base_stats.get("category", "COMUM")
		self.archetype = base_stats.get("archetype", "BASICO")
		self.name = base_stats.get("name", "INIMIGO")
		self.pattern = tuple(base_stats.get("pattern", ("ATACAR",)))
		self.pattern_index = 0
		self.preparado = False
		self.defendendo = False
		self.contra_ataque = False

	def esta_vivo(self):
		return self.hp > 0

	def escolher_acao(self):
		return self.pattern[self.pattern_index % len(self.pattern)]

	def registrar_acao(self, acao):
		if acao == "PREPARAR":
			self.preparado = True
		elif acao == "GOLPE_FORTE":
			self.preparado = False
		self.pattern_index = (self.pattern_index + 1) % len(self.pattern)

	def recompor(self):
		self.defendendo = False
	