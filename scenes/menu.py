import pyxel

class MenuState:
	def update(self):
		pass

	def draw(self):
		pyxel.cls(0)
		pyxel.text(52, 56, "MENU", 7)
		pyxel.text(22, 68, "Press SPACE for BATTLE", 6)