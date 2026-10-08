import pyxel


class GameOverState:
	def update(self):
		if pyxel.btnp(pyxel.KEY_SPACE):
			print("Reiniciando para MENU")

	def draw(self):
		pyxel.cls(2)
		pyxel.text(40, 56, "GAME OVER", 7)
		pyxel.text(22, 68, "Press SPACE to restart", 6)


class WaveCompleteState:
	def __init__(self, change_state, payload=None):
		self.change_state = change_state
		self.payload = payload or {}
		self.loot_page = 0
		self.items_per_page = 3

	def update(self):
		itens = self.payload.get("itens", [])
		max_page = max(0, (len(itens) - 1) // self.items_per_page)
		if pyxel.btnp(pyxel.KEY_LEFT):
			self.loot_page = max(0, self.loot_page - 1)
		if pyxel.btnp(pyxel.KEY_RIGHT):
			self.loot_page = min(max_page, self.loot_page + 1)
		if pyxel.btnp(pyxel.KEY_SPACE):
			self.change_state("BATTLE")

	def draw(self):
		pyxel.cls(3)
		wave = self.payload.get("wave", 0)
		pyxel.text(42, 28, f"ONDA {wave} VENCIDA", 7)
		pyxel.text(18, 42, f"XP: +{self.payload.get('xp', 0)}", 6)
		pyxel.text(18, 52, f"ACOES: {self.payload.get('player_actions', 0)}", 6)
		if self.payload.get("hp_recovered", 0):
			pyxel.text(18, 62, f"HP RECUPERADO: +{self.payload['hp_recovered']}", 10)
		itens = self.payload.get("itens", [])
		inicio = self.loot_page * self.items_per_page
		pagina = itens[inicio:inicio + self.items_per_page]
		pyxel.text(18, 72, "LOOT:", 10)
		if pagina:
			for indice, item in enumerate(pagina):
				pyxel.text(42, 72 + indice * 8, item.nome[:19], 7)
			if len(itens) > self.items_per_page:
				pyxel.text(122, 72, f"{self.loot_page + 1}/{(len(itens) - 1) // self.items_per_page + 1}", 6)
		else:
			pyxel.text(42, 72, "NENHUM", 5)
		pyxel.text(24, 108, "SPACE: PROXIMA ONDA", 6)


class VictoryState:
	def __init__(self, payload=None):
		payload = payload or {}
		self.payload = payload
		self.xp = int(payload.get("xp", 0))
		self.itens = payload.get("itens", [])
		self.loot_page = 0
		self.items_per_page = 3

	def update(self):
		max_page = max(0, (len(self.itens) - 1) // self.items_per_page)
		if pyxel.btnp(pyxel.KEY_LEFT):
			self.loot_page = max(0, self.loot_page - 1)
		if pyxel.btnp(pyxel.KEY_RIGHT):
			self.loot_page = min(max_page, self.loot_page + 1)
		if pyxel.btnp(pyxel.KEY_SPACE):
			print("Reiniciando para MENU")

	def draw(self):
		pyxel.cls(3)
		pyxel.text(48, 56, "VITORIA", 7)
		pyxel.text(26, 68, f"XP GANHO: {self.xp}", 6)
		inicio = self.loot_page * self.items_per_page
		pagina = self.itens[inicio:inicio + self.items_per_page]
		pyxel.text(8, 78, "LOOT:", 10)
		if pagina:
			for indice, item in enumerate(pagina):
				pyxel.text(38, 78 + indice * 8, item.nome[:20], 10)
			if len(self.itens) > self.items_per_page:
				pyxel.text(126, 78, f"{self.loot_page + 1}/{(len(self.itens) - 1) // self.items_per_page + 1}", 6)
		else:
			pyxel.text(38, 78, "NENHUM", 5)
		if self.payload.get("duration_seconds") is not None:
			pyxel.text(8, 104, f"DURACAO: {self.payload['duration_seconds']}s", 6)
		pyxel.text(22, 112, "Press SPACE to restart", 6)