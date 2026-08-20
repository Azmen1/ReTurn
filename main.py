import pyxel
from entities.enemy import Enemy
from entities.player import Player

MENU = "MENU"
BATTLE = "BATTLE"
GAME_OVER = "GAME_OVER"

class MenuState:
	def update(self):
		pass

	def draw(self):
		pyxel.cls(0)
		pyxel.text(52, 56, "MENU", 7)
		pyxel.text(22, 68, "Press SPACE for BATTLE", 6)


class BattleState:
	def __init__(self):
		self.player = Player()
		self.enemy = Enemy()

	def update(self):
		pass

	def draw(self):
		pyxel.cls(1)
		pyxel.text(56, 8, "BATTLE", 7)

		pyxel.text(8, 24, "PLAYER", 10)
		pyxel.text(8, 34, f"HP: {self.player.hp}", 7)
		pyxel.text(8, 42, f"ATK: {self.player.atk}", 7)
		pyxel.text(8, 50, f"DEF: {self.player.def_}", 7)
		pyxel.text(8, 58, f"SPD: {self.player.speed}", 7)

		pyxel.text(90, 24, "ENEMY", 8)
		pyxel.text(90, 34, f"HP: {self.enemy.hp}", 7)
		pyxel.text(90, 42, f"ATK: {self.enemy.atk}", 7)
		pyxel.text(90, 50, f"DEF: {self.enemy.def_}", 7)
		pyxel.text(90, 58, f"SPD: {self.enemy.speed}", 7)

class GameOverState:
	def update(self):
		pass

	def draw(self):
		pyxel.cls(2)
		pyxel.text(40, 56, "GAME OVER", 7)

class App:
	def __init__(self):
		self.states = {
			MENU: MenuState(),
			BATTLE: BattleState(),
			GAME_OVER: GameOverState(),
		}
		self.current_state = MENU

		pyxel.init(160, 120, title="ReTurn")
		pyxel.run(self.update, self.draw)

	def update(self):
		if self.current_state == MENU and pyxel.btnp(pyxel.KEY_SPACE):
			self.current_state = BATTLE

		self.states[self.current_state].update()

	def draw(self):
		self.states[self.current_state].draw()

App()