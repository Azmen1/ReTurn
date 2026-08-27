import pyxel
from data.balance import LEVEL_UP_POINTS, STAT_POINT_VALUE

STATS_DISPONIVEIS = ["hp", "atk", "def_", "speed", "luck"]
LABELS = {"hp": "HP", "atk": "ATK", "def_": "DEF", "speed": "SPD", "luck": "LUCK"}

MENU = "MENU"
LEVEL_UP = "LEVEL_UP"


class LevelUpState:
	def __init__(self, change_state, player, payload=None):
		payload = payload or {}
		self.change_state = change_state
		self.player = player
		self.niveis_pendentes = int(payload.get("niveis_pendentes", 1))
		self.pontos_restantes = LEVEL_UP_POINTS
		self.selecionado = 0
		self.distribuido = {stat: 0 for stat in STATS_DISPONIVEIS}

	def update(self):
		if pyxel.btnp(pyxel.KEY_UP):
			self.selecionado = (self.selecionado - 1) % len(STATS_DISPONIVEIS)
		if pyxel.btnp(pyxel.KEY_DOWN):
			self.selecionado = (self.selecionado + 1) % len(STATS_DISPONIVEIS)

		stat = STATS_DISPONIVEIS[self.selecionado]

		if pyxel.btnp(pyxel.KEY_RIGHT) and self.pontos_restantes > 0:
			self.distribuido[stat] += 1
			self.pontos_restantes -= 1

		if pyxel.btnp(pyxel.KEY_LEFT) and self.distribuido[stat] > 0:
			self.distribuido[stat] -= 1
			self.pontos_restantes += 1

		confirmou = (
			pyxel.btnp(pyxel.KEY_RETURN)
			or pyxel.btnp(pyxel.KEY_KP_ENTER)
			or pyxel.btnp(pyxel.KEY_Z)
			or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
		)
		if confirmou and self.pontos_restantes == 0:
			self.aplicar_pontos()
			self.avancar()

	def aplicar_pontos(self):
		for stat, pontos in self.distribuido.items():
			if pontos == 0:
				continue
			incremento = pontos * STAT_POINT_VALUE[stat]
			if stat == "hp":
				self.player.max_hp += incremento
				self.player.hp += incremento
			else:
				setattr(self.player, stat, getattr(self.player, stat) + incremento)

	def avancar(self):
		restantes = self.niveis_pendentes - 1
		if restantes > 0:
			self.change_state(LEVEL_UP, {"niveis_pendentes": restantes})
			return
		self.change_state(MENU)

	def draw(self):
		pyxel.cls(4)
		pyxel.text(36, 8, f"LEVEL UP! Nivel {self.player.level}", 7)
		pyxel.text(8, 20, f"Pontos restantes: {self.pontos_restantes}", 10)

		for idx, stat in enumerate(STATS_DISPONIVEIS):
			cursor = ">" if idx == self.selecionado else " "
			cor = 10 if idx == self.selecionado else 7
			pyxel.text(8, 36 + idx * 10, f"{cursor} {LABELS[stat]}: +{self.distribuido[stat]}", cor)

		pyxel.text(8, 100, "LEFT/RIGHT: ajustar", 6)
		pyxel.text(8, 108, "ENTER/Z: confirmar", 6)