from typing import Iterable, List, Any
from math import floor


from data.balance import (
    DANO_MINIMO,
    DEFESA_ESCALA,
    MULTIPLICADOR_CONTRA_ATAQUE,
    MULTIPLICADOR_DEFENDER,
)


def build_turn_order(combatants: Iterable[Any]) -> List[Any]:
    return sorted(
        combatants,
        key=lambda entity: (entity.speed, entity.luck),
        reverse=True,
    )


def obter_ataque_total(combatente: Any) -> int:
    equipamentos = getattr(combatente, "equipamentos", {})
    bonus = sum(getattr(item, "bonus_atk", 0) for item in equipamentos.values())
    return max(0, int(combatente.atk + bonus))


def obter_defesa_total(combatente: Any) -> int:
    equipamentos = getattr(combatente, "equipamentos", {})
    bonus = sum(getattr(item, "bonus_defesa", 0) for item in equipamentos.values())
    return max(0, int(combatente.def_ + bonus))


def aplicar_dano(alvo: Any, dano: int) -> int:
    """Retorna o HP efetivamente perdido, sem incluir excesso de dano."""
    hp_anterior = max(0, int(alvo.hp))
    dano_aplicado = min(hp_anterior, max(0, int(dano)))
    alvo.hp = hp_anterior - dano_aplicado
    return dano_aplicado


def calcular_dano_bruto(atacante: Any, alvo: Any) -> int:
    """Prevê o dano após mitigação, sem alterar HP nem consumir efeitos."""
    if atacante.hp <= 0 or alvo.hp <= 0:
        return 0

    ataque = obter_ataque_total(atacante)
    defesa = obter_defesa_total(alvo)
    if ataque == 0:
        return 0

    dano = ataque
    if getattr(atacante, "contra_ataque", False):
        dano *= MULTIPLICADOR_CONTRA_ATAQUE

    dano *= DEFESA_ESCALA / (DEFESA_ESCALA + defesa)

    if getattr(alvo, "defendendo", False):
        dano *= MULTIPLICADOR_DEFENDER

    # Arredonda uma única vez: 2.5 -> 3. Ataques positivos causam ao menos 1.
    return max(DANO_MINIMO, floor(dano + 0.5))


def calcular_dano(atacante: Any, alvo: Any) -> int:
    """Resolve um ataque completo e retorna o HP efetivamente removido."""
    dano = calcular_dano_bruto(atacante, alvo)
    if dano <= 0:
        return 0

    estava_defendendo = getattr(alvo, "defendendo", False)
    dano_aplicado = aplicar_dano(alvo, dano)

    # O bônus vale para um ataque e não se acumula.
    atacante.contra_ataque = False

    if estava_defendendo:
        # A guarda protege o próximo golpe, mesmo em outra rodada.
        alvo.defendendo = False
        alvo.contra_ataque = alvo.hp > 0

    return dano_aplicado