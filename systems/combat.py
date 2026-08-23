from typing import Iterable, List, Any


def build_turn_order(combatants: Iterable[Any]) -> List[Any]:
	"""Return a new turn order list sorted by speed and luck (descending)."""
	return sorted(combatants, key=lambda entity: (entity.speed, entity.luck), reverse=True)


def aplicar_dano(alvo: Any, dano: int) -> int:
	"""Subtract damage from target HP without letting HP go below zero."""
	dano_aplicado = max(0, int(dano))
	alvo.hp = max(0, int(getattr(alvo, "hp", 0)) - dano_aplicado)
	return dano_aplicado


def calcular_dano(atacante: Any, alvo: Any) -> int:
	"""Apply damage to target HP using ATK and DEF, returning applied damage."""
	ataque = max(0, int(getattr(atacante, "atk", 0)))
	defesa = max(0, int(getattr(alvo, "def_", 0)))

	dano_recebido = int(ataque * (100 / (100 + defesa)))
	aplicar_dano(alvo, dano_recebido)
	return dano_recebido
