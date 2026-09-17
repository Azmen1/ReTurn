import pyxel
from entities.enemy import Enemy
from entities.player import Player
from systems.combat import build_turn_order, calcular_dano, obter_ataque_total, obter_defesa_total
from systems.loot import gerar_loot
from systems.progression import calcular_tier, gerar_stats_inimigo, verificar_level_up

VICTORY = "VICTORY"
GAME_OVER = "GAME_OVER"
LEVEL_UP = "LEVEL_UP"
MENU = "MENU"

class BattleState:
	def __init__(self, change_state, player, wave_number=1, advance_wave=None):
		self.player = player
		self.wave_number = wave_number
		self.advance_wave = advance_wave
		self.enemy = Enemy(gerar_stats_inimigo(calcular_tier(wave_number)))
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
		self.damage_numbers = []
		self.player.defendendo = False
		self.player.contra_ataque = False

	def update(self):
		self.atualizar_numeros_dano()

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
		if self.player.esta_vivo() and self.enemy.esta_vivo():
			self.registrar_log("SPACE: NEXT ROUND")

	def executar_ataque(self, atacante, alvo, nomes):
		contra_ataque = getattr(atacante, "contra_ataque", False)
		bloqueou = getattr(alvo, "defendendo", False)
		dano = calcular_dano(atacante, alvo)
		self.adicionar_numero_dano(alvo, dano)

		verbo = "contra-atacou" if contra_ataque and dano > 0 else "atacou"
		self.registrar_log(f"{nomes[atacante]} {verbo} {nomes[alvo]} ({dano})")
		if bloqueou and dano > 0 and alvo.esta_vivo():
			self.registrar_log(f"{nomes[alvo]}: CONTRA-ATAQUE PRONTO")

		if not alvo.esta_vivo():
			self.registrar_log(f"{nomes[alvo]} DERROTADO")

	def adicionar_numero_dano(self, alvo, dano):
		x = 36 if alvo is self.player else 118
		y = 25 if alvo is self.player else 25
		self.damage_numbers.append({"x": x, "y": y, "valor": dano, "tempo": 30})

	def atualizar_numeros_dano(self):
		for numero in self.damage_numbers:
			numero["y"] -= 1
			numero["tempo"] -= 1
		self.damage_numbers = [numero for numero in self.damage_numbers if numero["tempo"] > 0]

	def update_player_action_menu(self):
		row = self.selected_action // 2
		column = self.selected_action % 2

		if pyxel.btnp(pyxel.KEY_UP):
			row = (row - 1) % 2

		if pyxel.btnp(pyxel.KEY_DOWN):
			row = (row + 1) % 2

		if pyxel.btnp(pyxel.KEY_LEFT):
			column = (column - 1) % 2

		if pyxel.btnp(pyxel.KEY_RIGHT):
			column = (column + 1) % 2

		self.selected_action = row * 2 + column

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
			self.player.defendendo = True
			self.registrar_log("PLAYER entrou em DEFESA")
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

	def calcular_chance_fuga(self):
		enemy_speed = max(1, self.enemy.speed)
		speed_ratio = self.player.speed / enemy_speed
		speed_bonus = int((speed_ratio - 1.0) * 25)
		luck_bonus = (self.player.luck - self.enemy.luck) * 3
		chance = 30 + speed_bonus + luck_bonus
		return max(10, min(90, chance))

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
		item = self.player.inventory[index]

		if item.tipo in self.player.equipamento:
			anterior = self.player.equipamento[item.tipo]
			self.player.inventory.pop(index)
			self.player.equipamento[item.tipo] = item
			if anterior is not None:
				self.player.inventory.pop(index)
			self.registrar_log(f"PLAYER equipou {item.nome}")

		elif item.tipo == "cura":
			cura = min(max(0, int(item.valor)), self.player.max_hp - self.player.hp)
			if cura <= 0:
				self.registrar_log("SEM HP PARA RECUPERAR")
				return
			self.player.inventory.pop(index)
			self.player.hp += cura
			self.registrar_log(f"PLAYER usou {item.nome} (+{cura} HP)")
		else:
			self.registrar_log("ITEM NAO UTILIZAVEL")
			return

		self.waiting_item_menu = False
		self.consumir_turno_player()

	def consumir_turno_player(self):
		self.waiting_player_action = False
		self.waiting_item_menu = False
		self.turn_index += 1
		self.processar_fila_turnos()

	def ir_para_vitoria(self):
		primeira_vitoria = not self.victory_resolved
		payload = self.resolver_recompensa_vitoria()
		if primeira_vitoria and self.advance_wave is not None:
			self.advance_wave()

		niveis_subidos = verificar_level_up(self.player)
		if niveis_subidos > 0:
			self.change_state(LEVEL_UP, {"niveis_pendentes": niveis_subidos})
			return

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

	def desenhar_barra_hp(self, x, y, largura, hp, max_hp, cor):
		proporcao = max(0, min(1, hp / max_hp))
		pyxel.rect(x, y, largura, 6, 0)
		pyxel.rect(x, y, int(largura * proporcao), 6, cor)
		pyxel.rectb(x, y, largura, 6, 7)

	def draw(self):
		pyxel.cls(1)
		pyxel.text(56, 8, "BATTLE", 7)
		pyxel.text(112, 8, f"ONDA: {self.wave_number}", 10)
		if not self.round_active and not self.waiting_player_action:
			pyxel.text(8, 14, "SPACE: NEXT ROUND", 6)
		else:
			pyxel.text(8, 14, "ARROWS + ENTER/Z", 6)

		pyxel.text(8, 24, "PLAYER", 10)
		self.desenhar_barra_hp(8, 32, 55, self.player.hp, self.player.max_hp, 11)
		pyxel.text(8, 41, f"HP: {self.player.hp}/{self.player.max_hp}", 7)
		pyxel.text(8, 49, f"ATK: {self.player.atk}", 7)
		pyxel.text(8, 57, f"DEF: {self.player.def_}", 7)
		pyxel.text(8, 65, f"SPD: {self.player.speed}", 7)

		pyxel.text(90, 24, "ENEMY", 8)
		self.desenhar_barra_hp(90, 32, 55, self.enemy.hp, self.enemy.max_hp, 8)
		pyxel.text(90, 41, f"HP: {self.enemy.hp}/{self.enemy.max_hp}", 7)
		pyxel.text(90, 49, f"ATK: {self.enemy.atk}", 7)
		pyxel.text(90, 57, f"DEF: {self.enemy.def_}", 7)
		pyxel.text(90, 65, f"SPD: {self.enemy.speed}", 7)

		for numero in self.damage_numbers:
			pyxel.text(numero["x"], numero["y"], f"-{numero['valor']}", 8)

		for idx, line in enumerate(self.battle_log[-4:]):
			pyxel.text(8, 78 + idx * 8, line, 7)

		if self.waiting_player_action:
			if self.waiting_item_menu:
				pyxel.rect(4, 68, 152, 48, 0)
				pyxel.rectb(4, 68, 152, 48, 7)
				pyxel.text(70, 72, "ITENS", 10)
				if not self.player.inventory:
					pyxel.text(68, 88, "(VAZIO)", 5)
				else:
					for idx, item in enumerate(self.player.inventory[:3]):
						cursor = ">" if idx == self.selected_item_index else " "
						color = 10 if idx == self.selected_item_index else 7
						y = 82 + idx * 9
						pyxel.rectb(12, y, 136, 8, color)
						pyxel.text(17, y + 1, f"{cursor}{item.nome} ({item.valor})", color)
				pyxel.text(58, 110, "ESC/X: VOLTAR", 6)
			else:
				pyxel.rect(4, 68, 152, 48, 0)
				pyxel.rectb(4, 68, 152, 48, 7)
				pyxel.text(72, 72, "ACAO", 10)
				for idx, option in enumerate(self.action_options):
					color = 10 if idx == self.selected_action else 7
					column = idx % 2
					row = idx // 2
					x = 10 + column * 75
					y = 80 + row * 18
					pyxel.rectb(x, y, 68, 15, color)
					pyxel.text(x + 5, y + 4, option, color)