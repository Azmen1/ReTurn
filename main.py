import pyxel
from entities.enemy import Enemy
from entities.player import Player
from systems.combat import build_turn_order, calcular_dano

MENU = "MENU"
BATTLE = "BATTLE"
GAME_OVER = "GAME_OVER"
VICTORY = "VICTORY"

class MenuState:
	def update(self):
		pass

	def draw(self):
		pyxel.cls(0)
		pyxel.text(52, 56, "MENU", 7)
		pyxel.text(22, 68, "Press SPACE for BATTLE", 6)


class BattleState:
	def __init__(self, change_state):
		self.player = Player()
		self.enemy = Enemy()
		self.change_state = change_state
		self.round_number = 0
		self.battle_log = ["SPACE: NEXT ROUND"]

	def update(self):
		if self.enemy.hp <= 0:
			self.change_state(VICTORY)
			return

		if self.player.hp <= 0:
			self.change_state(GAME_OVER)
			return

		if not self.player.esta_vivo() or not self.enemy.esta_vivo():
			return

		if pyxel.btnp(pyxel.KEY_SPACE):
			self.executar_rodada()

	def executar_rodada(self):
		self.round_number += 1
		turn_order = build_turn_order([self.player, self.enemy])

		nomes = {
			self.player: "PLAYER",
			self.enemy: "ENEMY",
		}
		ordem = " -> ".join(nomes[combatente] for combatente in turn_order)
		self.battle_log = [f"ROUND {self.round_number}", f"ORDER: {ordem}"]
		print(f"[ROUND {self.round_number}] ORDER: {ordem}")

		for combatente in turn_order:
			if not combatente.esta_vivo():
				continue

			alvo = self.enemy if combatente is self.player else self.player
			if not alvo.esta_vivo():
				break

			dano = calcular_dano(combatente, alvo)
			acao = f"{nomes[combatente]} atacou {nomes[alvo]} ({dano})"
			self.battle_log.append(acao)
			print(acao)

			if not alvo.esta_vivo():
				derrotado = f"{nomes[alvo]} DERROTADO"
				self.battle_log.append(derrotado)
				print(derrotado)
				break

	def draw(self):
		pyxel.cls(1)
		pyxel.text(56, 8, "BATTLE", 7)
		pyxel.text(8, 14, "SPACE: NEXT ROUND", 6)

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

		for idx, line in enumerate(self.battle_log[-4:]):
			pyxel.text(8, 78 + idx * 8, line, 7)

class GameOverState:
	def update(self):
		if pyxel.btnp(pyxel.KEY_R):
			print("Reiniciando para MENU")

	def draw(self):
		pyxel.cls(2)
		pyxel.text(40, 56, "GAME OVER", 7)
		pyxel.text(26, 68, "Press R to restart", 6)


class VictoryState:
	def update(self):
		if pyxel.btnp(pyxel.KEY_R):
			print("Reiniciando para MENU")

	def draw(self):
		pyxel.cls(3)
		pyxel.text(48, 56, "VITORIA", 7)
		pyxel.text(26, 68, "Press R to restart", 6)

class App:
	def __init__(self):
		self.state_classes = {
			MENU: lambda: MenuState(),
			BATTLE: lambda: BattleState(self.change_state),
			GAME_OVER: lambda: GameOverState(),
			VICTORY: lambda: VictoryState(),
		}
		self.current_state = self.state_classes[MENU]()

		pyxel.init(160, 120, title="ReTurn")
		pyxel.run(self.update, self.draw)

	def change_state(self, state_name):
		self.current_state = self.state_classes[state_name]()

	def update(self):
		if isinstance(self.current_state, MenuState) and pyxel.btnp(pyxel.KEY_SPACE):
			self.change_state(BATTLE)

		if (isinstance(self.current_state, GameOverState) or isinstance(self.current_state, VictoryState)) and pyxel.btnp(pyxel.KEY_R):
			self.change_state(MENU)

		self.current_state.update()

	def draw(self):
		self.current_state.draw()

App()