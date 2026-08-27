import pyxel


class GameOverState:
	def update(self):
		if pyxel.btnp(pyxel.KEY_R):
			print("Reiniciando para MENU")

	def draw(self):
		pyxel.cls(2)
		pyxel.text(40, 56, "GAME OVER", 7)
		pyxel.text(26, 68, "Press R to restart", 6)


class VictoryState:
	def __init__(self, payload=None):
		payload = payload or {}
		self.xp = int(payload.get("xp", 0))
		self.itens = payload.get("itens", [])

	def update(self):
		if pyxel.btnp(pyxel.KEY_R):
			print("Reiniciando para MENU")

	def draw(self):
		pyxel.cls(3)
		pyxel.text(48, 56, "VITORIA", 7)
		pyxel.text(26, 68, f"XP GANHO: {self.xp}", 6)
		if self.itens:
			nomes = ", ".join(item.nome for item in self.itens)
			pyxel.text(8, 78, f"LOOT: {nomes}", 10)
		else:
			pyxel.text(8, 78, "LOOT: NENHUM", 5)
		pyxel.text(26, 98, "Press R to restart", 6)