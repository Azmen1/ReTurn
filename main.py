import pyxel
import time
import json
import os
from entities.enemy import Enemy
from entities.player import Player
from systems.combat import build_turn_order, calcular_dano_bruto, aplicar_dano
from systems.loot import gerar_loot
from scenes.menu import MenuState
from scenes.battle import BattleState
from scenes.gamer_over import GameOverState, VictoryState, WaveCompleteState
from scenes.level_up import LevelUpState
from data.balance import RECOVERY_PERCENT, TOTAL_WAVES, WAVE_TIER_SIZE

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
		self.batalha_suspensa = None
		self.match_log = []
		self.waves_won = 0
		self.campaign_completed = False
		self.match_closed = False
		self.last_match_summary = None
		self.match_started_at = time.monotonic()
		self.state_classes = {
			MENU: lambda payload=None: MenuState(),
			BATTLE: self.criar_batalha,
			GAME_OVER: lambda payload=None: GameOverState(),
			VICTORY: lambda payload=None: VictoryState(payload),
			LEVEL_UP: lambda payload=None: LevelUpState(self.change_state, self.player, payload),
			"WAVE_COMPLETE": self.criar_resultado_onda,
		}
		self.current_state = self.state_classes[MENU](None)
		self.pending_state = None
		self.pending_payload = None
		self.transition_frame = 0

		pyxel.init(160, 120, title="ReTurn", display_scale=8)
		pyxel.run(self.update, self.draw)

	def criar_batalha(self, payload=None):
		if self.batalha_suspensa is not None:
			batalha = self.batalha_suspensa
			self.batalha_suspensa = None
			return batalha
		if self.campaign_completed:
			return VictoryState(self.last_match_summary)
		return BattleState(
			self.change_state,
			self.player,
			self.wave_number,
			self.finalizar_onda,
			finish_battle=self.registrar_derrota,
		)

	def criar_resultado_onda(self, payload=None):
		payload = payload or {}
		if not payload.get("finalizado"):
			self.finalizar_onda(payload, transicionar=False)
		if payload.get("campanha_concluida"):
			return VictoryState(payload)
		return WaveCompleteState(self.change_state, payload)

	def change_state(self, state_name, payload=None):
		if state_name == MENU and isinstance(payload, dict):
			self.batalha_suspensa = payload.get("batalha_suspensa")
		self.pending_state = state_name
		self.pending_payload = payload
		self.transition_frame = 1

	def finalizar_onda(self, payload, transicionar=True):
		if self.campaign_completed or payload.get("wave") != self.wave_number or payload.get("finalizado"):
			return
		self.match_log.append({
			"wave": payload["wave"],
			"tier": payload["encounter"]["tier"],
			"category": payload["encounter"]["category"],
			"archetype": payload["encounter"]["archetype"],
			"pattern": payload["encounter"]["pattern"],
			"result": "VITORIA",
			"actions": payload.get("player_actions", 0),
			"offensive_actions": payload.get("offensive_actions", 0),
			"damage_received": payload.get("damage_received", 0),
			"entry_hp": payload.get("entry_hp"),
			"exit_hp": payload.get("exit_hp"),
		})
		self.waves_won += 1
		if self.wave_number == TOTAL_WAVES:
			self.campaign_completed = True
			payload["campanha_concluida"] = True
			payload["duration_seconds"] = round(time.monotonic() - self.match_started_at, 1)
			payload["match_log"] = self.match_log
			payload["finalizado"] = True
			self.encerrar_partida("VITORIA", self.wave_number)
			if transicionar:
				self.change_state(VICTORY, payload)
			return
		if self.wave_number % WAVE_TIER_SIZE == 0:
			antes = self.player.hp
			cura = (self.player.max_hp * RECOVERY_PERCENT + 99) // 100
			self.player.hp = min(self.player.max_hp, self.player.hp + cura)
			payload["hp_recovered"] = self.player.hp - antes
		self.wave_number += 1
		payload["finalizado"] = True
		if transicionar:
			self.change_state("WAVE_COMPLETE", payload)

	def registrar_derrota(self, battle):
		if self.match_closed:
			return
		self.match_log.append({
			"wave": battle.wave_number,
			"tier": battle.enemy.tier,
			"category": battle.enemy.category,
			"archetype": battle.enemy.archetype,
			"pattern": list(battle.enemy.pattern),
			"result": "DERROTA",
			"actions": battle.player_actions,
			"offensive_actions": battle.offensive_actions,
			"damage_received": battle.damage_received,
			"entry_hp": battle.entry_hp,
			"exit_hp": max(0, battle.player.hp),
		})
		self.encerrar_partida("DERROTA", battle.wave_number)
		self.change_state(GAME_OVER)

	def encerrar_partida(self, result, final_wave):
		if self.match_closed:
			return
		self.match_closed = True
		self.last_match_summary = {
			"result": result,
			"final_wave": final_wave,
			"waves_won": self.waves_won,
			"duration_seconds": round(time.monotonic() - self.match_started_at, 1),
			"encounters": list(self.match_log),
		}
		self.salvar_partida(self.last_match_summary)

	def salvar_partida(self, summary):
		path = os.path.join(os.path.dirname(__file__), "data", "matches.json")
		try:
			os.makedirs(os.path.dirname(path), exist_ok=True)
			try:
				with open(path, "r", encoding="utf-8") as arquivo:
					historico = json.load(arquivo)
			except (FileNotFoundError, json.JSONDecodeError):
				historico = []
			historico.append(summary)
			with open(path, "w", encoding="utf-8") as arquivo:
				json.dump(historico, arquivo, ensure_ascii=False, indent=2)
		except (OSError, TypeError) as erro:
			print(f"Nao foi possivel salvar o registro da partida: {erro}")

	def reiniciar_partida(self):
		self.player = Player()
		self.wave_number = 1
		self.batalha_suspensa = None
		self.match_log = []
		self.waves_won = 0
		self.campaign_completed = False
		self.match_closed = False
		self.last_match_summary = None
		self.match_started_at = time.monotonic()

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
			if self.batalha_suspensa is None:
				self.reiniciar_partida()
			self.change_state(BATTLE)

		if (isinstance(self.current_state, GameOverState) or isinstance(self.current_state, VictoryState)) and pyxel.btnp(pyxel.KEY_SPACE):
			if isinstance(self.current_state, (GameOverState, VictoryState)):
				self.reiniciar_partida()
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


if __name__ == "__main__":
	App()