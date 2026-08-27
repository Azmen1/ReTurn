import pyxel
from entities.enemy import Enemy
from entities.player import Player
from systems.combat import build_turn_order, calcular_dano_bruto, aplicar_dano
from systems.loot import gerar_loot
from scenes.menu import MenuState
from scenes.battle import BattleState
from scenes.gamer_over import GameOverState, VictoryState
from scenes.level_up import LevelUpState

MENU = "MENU"
BATTLE = "BATTLE"
GAME_OVER = "GAME_OVER"
VICTORY = "VICTORY"
LEVEL_UP = "LEVEL_UP"

class App:
	def __init__(self):
		self.player = Player()
		self.state_classes = {
			MENU: lambda payload=None: MenuState(),
			BATTLE: lambda payload=None: BattleState(self.change_state, self.player),
			GAME_OVER: lambda payload=None: GameOverState(),
			VICTORY: lambda payload=None: VictoryState(payload),
			LEVEL_UP: lambda payload=None: LevelUpState(self.change_state, self.player, payload),
		}
		self.current_state = self.state_classes[MENU](None)

		pyxel.init(160, 120, title="ReTurn")
		pyxel.run(self.update, self.draw)

	def change_state(self, state_name, payload=None):
		self.current_state = self.state_classes[state_name](payload)

	def update(self):
		if isinstance(self.current_state, MenuState) and pyxel.btnp(pyxel.KEY_SPACE):
			if self.player.hp <= 0:
				self.player = Player()
			self.change_state(BATTLE)

		if (isinstance(self.current_state, GameOverState) or isinstance(self.current_state, VictoryState)) and pyxel.btnp(pyxel.KEY_R):
			if isinstance(self.current_state, GameOverState):
				self.player = Player()
			self.change_state(MENU)

		self.current_state.update()

	def draw(self):
		self.current_state.draw()


App()