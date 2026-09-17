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
TRANSITION_FRAMES = 20
TRANSITION_MIDDLE = TRANSITION_FRAMES // 2

class App:
	def __init__(self):
		self.player = Player()
		self.wave_number = 1
		self.state_classes = {
			MENU: lambda payload=None: MenuState(),
			BATTLE: lambda payload=None: BattleState(self.change_state, self.player, self.wave_number, self.advance_wave),
			GAME_OVER: lambda payload=None: GameOverState(),
			VICTORY: lambda payload=None: VictoryState(payload),
			LEVEL_UP: lambda payload=None: LevelUpState(self.change_state, self.player, payload),
		}
		self.current_state = self.state_classes[MENU](None)
		self.pending_state = None
		self.pending_payload = None
		self.transition_frame = 0

		pyxel.init(160, 120, title="ReTurn", display_scale=8)
		pyxel.run(self.update, self.draw)

	def change_state(self, state_name, payload=None):
		self.pending_state = state_name
		self.pending_payload = payload
		self.transition_frame = 1

	def advance_wave(self):
		self.wave_number += 1

	def update(self):
		if self.transition_frame:
			self.transition_frame += 1
			if self.transition_frame == TRANSITION_MIDDLE:
				self.current_state = self.state_classes[self.pending_state](self.pending_payload)
			if self.transition_frame >= TRANSITION_FRAMES:
				self.transition_frame = 0
				self.pending_state = None
				self.pending_payload = None
			return

		if isinstance(self.current_state, MenuState) and pyxel.btnp(pyxel.KEY_SPACE):
			if self.player.hp <= 0:
				self.player = Player()
				self.wave_number = 1
			self.change_state(BATTLE)

		if (isinstance(self.current_state, GameOverState) or isinstance(self.current_state, VictoryState)) and pyxel.btnp(pyxel.KEY_R):
			if isinstance(self.current_state, GameOverState):
				self.player = Player()
				self.wave_number = 1
			self.change_state(MENU)

		self.current_state.update()

	def draw(self):
		self.current_state.draw()
		if self.transition_frame:
			if self.transition_frame <= TRANSITION_MIDDLE:
				largura = 160 * self.transition_frame // TRANSITION_MIDDLE
			else:
				largura = 160 * (TRANSITION_FRAMES - self.transition_frame) // TRANSITION_MIDDLE
			pyxel.rect(0, 0, largura, 120, 0)


App()