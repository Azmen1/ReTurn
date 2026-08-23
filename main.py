import pyxel
from entities.enemy import Enemy
from entities.player import Player
from systems.combat import build_turn_order, calcular_dano_bruto, aplicar_dano
from systems.loot import gerar_loot

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
	def __init__(self, change_state, player):
		self.player = player
		self.enemy = Enemy()
		self.change_state = change_state
		self.round_number = 0
		self.battle_log = ["SPACE: NEXT ROUND"]
		self.turn_order = []
		self.turn_index = 0
		self.round_active = False
		self.waiting_player_action = False
		self.waiting_item_menu = False
		self.action_options = ["ATACAR", "ITEM", "DEFENDER", "FUGIR"]
		self.selected_action = 0
		self.selected_item_index = 0
		self.victory_resolved = False
		self.player.defendendo = False

	def update(self):
		if self.enemy.hp <= 0:
			self.ir_para_vitoria()
			return

		if self.player.hp <= 0:
			self.change_state(GAME_OVER)
			return

		if not self.player.esta_vivo() or not self.enemy.esta_vivo():
			return

		if self.waiting_player_action:
			if self.waiting_item_menu:
				self.update_item_menu()
				return
			self.update_player_action_menu()
			return

		if pyxel.btnp(pyxel.KEY_SPACE) and not self.round_active:
			self.iniciar_rodada()

	def iniciar_rodada(self):
		self.round_number += 1
		self.turn_order = build_turn_order([self.player, self.enemy])
		self.turn_index = 0
		self.round_active = True
		self.player.defendendo = False

		nomes = {
			self.player: "PLAYER",
			self.enemy: "ENEMY",
		}
		ordem = " -> ".join(nomes[combatente] for combatente in self.turn_order)
		self.battle_log = [f"ROUND {self.round_number}", f"ORDER: {ordem}"]
		print(f"[ROUND {self.round_number}] ORDER: {ordem}")
		self.processar_fila_turnos()

	def processar_fila_turnos(self):
		nomes = {
			self.player: "PLAYER",
			self.enemy: "ENEMY",
		}

		while self.round_active and self.turn_index < len(self.turn_order):
			combatente = self.turn_order[self.turn_index]

			if not combatente.esta_vivo():
				self.turn_index += 1
				continue

			alvo = self.enemy if combatente is self.player else self.player
			if not alvo.esta_vivo():
				break

			if combatente is self.player:
				# Defense never carries to a fresh player decision point.
				self.player.defendendo = False
				self.waiting_player_action = True
				self.selected_action = 0
				self.registrar_log("ESCOLHA A ACAO")
				return

			self.executar_ataque(combatente, alvo, nomes)
			if not self.player.esta_vivo():
				self.round_active = False
				self.waiting_player_action = False
				self.change_state(GAME_OVER)
				return

			if not self.enemy.esta_vivo():
				self.round_active = False
				self.waiting_player_action = False
				self.ir_para_vitoria()
				return

			self.turn_index += 1

		self.round_active = False
		self.player.defendendo = False
		if self.player.esta_vivo() and self.enemy.esta_vivo():
			self.registrar_log("SPACE: NEXT ROUND")

	def executar_ataque(self, atacante, alvo, nomes):
		reduzir_defesa = atacante is self.enemy and alvo is self.player and self.player.defendendo
		dano = calcular_dano_bruto(atacante, alvo)

		if reduzir_defesa:
			dano = dano // 2
			self.player.defendendo = False

		dano = aplicar_dano(alvo, dano)

		acao = f"{nomes[atacante]} atacou {nomes[alvo]} ({dano})"
		self.registrar_log(acao)

		if not alvo.esta_vivo():
			self.registrar_log(f"{nomes[alvo]} DERROTADO")

	def update_player_action_menu(self):
		if pyxel.btnp(pyxel.KEY_UP):
			self.selected_action = (self.selected_action - 1) % len(self.action_options)

		if pyxel.btnp(pyxel.KEY_DOWN):
			self.selected_action = (self.selected_action + 1) % len(self.action_options)

		confirmou = (
			pyxel.btnp(pyxel.KEY_RETURN)
			or pyxel.btnp(pyxel.KEY_KP_ENTER)
			or pyxel.btnp(pyxel.KEY_Z)
			or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
		)
		if confirmou:
			self.executar_acao_player(self.selected_action)

	def update_item_menu(self):
		if not self.player.inventory:
			if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.KEY_X):
				self.waiting_item_menu = False
			if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
				self.registrar_log("INVENTARIO VAZIO")
				self.waiting_item_menu = False
			return

		if pyxel.btnp(pyxel.KEY_UP):
			self.selected_item_index = (self.selected_item_index - 1) % len(self.player.inventory)

		if pyxel.btnp(pyxel.KEY_DOWN):
			self.selected_item_index = (self.selected_item_index + 1) % len(self.player.inventory)

		cancelou = pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.KEY_X)
		if cancelou:
			self.waiting_item_menu = False
			return

		confirmou = (
			pyxel.btnp(pyxel.KEY_RETURN)
			or pyxel.btnp(pyxel.KEY_KP_ENTER)
			or pyxel.btnp(pyxel.KEY_Z)
			or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
		)
		if confirmou:
			self.usar_item_selecionado()

	def executar_acao_player(self, action_index):
		nomes = {
			self.player: "PLAYER",
			self.enemy: "ENEMY",
		}

		if action_index == 0:  # ATACAR
			self.executar_ataque(self.player, self.enemy, nomes)
			if not self.enemy.esta_vivo():
				self.waiting_player_action = False
				self.round_active = False
				self.ir_para_vitoria()
				return
		elif action_index == 1:  # ITEM
			self.abrir_menu_itens()
			return
		elif action_index == 2:  # DEFENDER
			if self.inimigo_ainda_age_nesta_rodada():
				self.player.defendendo = True
				self.registrar_log("PLAYER entrou em DEFESA")
			else:
				self.player.defendendo = False
				self.registrar_log("DEFESA sem alvo nesta rodada")
		elif action_index == 3:  # FUGIR
			chance = self.calcular_chance_fuga()
			sucesso = pyxel.rndi(1, 100) <= chance
			if sucesso:
				self.registrar_log(f"PLAYER conseguiu FUGIR ({chance}%)")
				self.change_state(MENU)
				return
			self.registrar_log(f"PLAYER falhou ao FUGIR ({chance}%)")

		self.consumir_turno_player()

	def registrar_log(self, mensagem):
		self.battle_log.append(mensagem)
		print(mensagem)

	def acao_desabilitada(self, action_index):
		return False

	def calcular_chance_fuga(self):
		enemy_speed = max(1, self.enemy.speed)
		speed_ratio = self.player.speed / enemy_speed
		speed_bonus = int((speed_ratio - 1.0) * 25)
		luck_bonus = (self.player.luck - self.enemy.luck) * 3
		chance = 30 + speed_bonus + luck_bonus
		return max(10, min(90, chance))

	def inimigo_ainda_age_nesta_rodada(self):
		for i in range(self.turn_index + 1, len(self.turn_order)):
			if self.turn_order[i] is self.enemy and self.enemy.esta_vivo():
				return True
		return False

	def abrir_menu_itens(self):
		self.waiting_item_menu = True
		self.selected_item_index = 0
		if self.player.inventory:
			self.registrar_log("ESCOLHA UM ITEM")
		else:
			self.registrar_log("INVENTARIO VAZIO")

	def usar_item_selecionado(self):
		if not self.player.inventory:
			self.waiting_item_menu = False
			return

		index = self.selected_item_index % len(self.player.inventory)
		item = self.player.inventory.pop(index)
		self.waiting_item_menu = False

		if item.tipo == "cura":
			cura = min(int(item.valor), self.player.max_hp - self.player.hp)
			self.player.hp += cura
			self.registrar_log(f"PLAYER usou {item.nome} (+{cura} HP)")
		else:
			self.registrar_log(f"PLAYER usou {item.nome}")

		self.consumir_turno_player()

	def consumir_turno_player(self):
		self.waiting_player_action = False
		self.waiting_item_menu = False
		self.turn_index += 1
		self.processar_fila_turnos()

	def ir_para_vitoria(self):
		payload = self.resolver_recompensa_vitoria()
		self.change_state(VICTORY, payload)

	def resolver_recompensa_vitoria(self):
		if self.victory_resolved:
			return {"itens": [], "xp": 0}

		itens, xp = gerar_loot(self.enemy)
		self.player.inventory.extend(itens)
		self.player.xp += xp
		self.victory_resolved = True

		for item in itens:
			self.registrar_log(f"LOOT: {item.nome}")
		self.registrar_log(f"XP +{xp}")

		return {"itens": itens, "xp": xp}

	def draw(self):
		pyxel.cls(1)
		pyxel.text(56, 8, "BATTLE", 7)
		if not self.round_active and not self.waiting_player_action:
			pyxel.text(8, 14, "SPACE: NEXT ROUND", 6)
		else:
			pyxel.text(8, 14, "UP/DOWN + ENTER/Z", 6)

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

		if self.waiting_player_action:
			if self.waiting_item_menu:
				pyxel.text(94, 70, "ITENS", 10)
				if not self.player.inventory:
					pyxel.text(90, 80, "(VAZIO)", 5)
					pyxel.text(72, 96, "ESC/X: VOLTAR", 6)
				else:
					for idx, item in enumerate(self.player.inventory):
						cursor = ">" if idx == self.selected_item_index else " "
						color = 10 if idx == self.selected_item_index else 7
						pyxel.text(66, 80 + idx * 8, f"{cursor} {item.nome} ({item.valor})", color)
					pyxel.text(64, 112, "ESC/X: VOLTAR", 6)
			else:
				pyxel.text(94, 70, "ACAO", 10)
				for idx, option in enumerate(self.action_options):
					cursor = ">" if idx == self.selected_action else " "
					color = 10 if idx == self.selected_action else 7
					pyxel.text(90, 80 + idx * 8, f"{cursor} {option}", color)

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

class App:
	def __init__(self):
		self.player = Player()
		self.state_classes = {
			MENU: lambda payload=None: MenuState(),
			BATTLE: lambda payload=None: BattleState(self.change_state, self.player),
			GAME_OVER: lambda payload=None: GameOverState(),
			VICTORY: lambda payload=None: VictoryState(payload),
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

if __name__ == "__main__":
	App()