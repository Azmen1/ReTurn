PLAYER_BASE_STATS = {
	"hp": 30,
	"max_hp": 30,
	"atk": 6,
	"def_": 3,
	"speed": 4,
	"luck": 5,
	"level": 1,
	"xp": 0,
}

ENEMY_BASE_STATS = {
	"hp": 24,
	"max_hp": 24,
	"atk": 5,
	"def_": 2,
	"speed": 3,
	"luck": 2,
	"level": 1,
}

WAVE_TIER_SIZE = 5
TOTAL_WAVES = 20
TOTAL_TIERS = TOTAL_WAVES // WAVE_TIER_SIZE
ENCOUNTER_SEQUENCE = ("COMUM", "COMUM", "COMUM", "ELITE", "CHEFE")
INTERPOLATION_WAVES = (1, 6, 11, 16)
RECOVERY_PERCENT = 30
TARGET_MATCH_DURATION_MINUTES = (20, 30)

# The tier references are the midpoints of the original balancing ranges.
ENEMY_TIER_REFERENCES = {
	1: {"hp": 22, "atk": 4, "def_": 2, "speed": 2, "luck": 2},
	2: {"hp": 29, "atk": 7, "def_": 4, "speed": 4, "luck": 4},
	3: {"hp": 38, "atk": 10, "def_": 6, "speed": 6, "luck": 6},
	4: {"hp": 49, "atk": 14, "def_": 8, "speed": 8, "luck": 8},
}

ENCOUNTER_CATEGORY_MODIFIERS = {
	"COMUM": {"hp": 1.0, "atk": 1.0},
	"ELITE": {"hp": 1.25, "atk": 1.10},
	"CHEFE": {"hp": 1.60, "atk": 1.15},
}

ARCHETYPE_DEFINITIONS = {
	"BASICO": {"name": "BATEDOR", "hp": 1.00, "atk": 1.00, "def_": 1.00, "speed": 0},
	"BRUTO": {"name": "BRUTO", "hp": 1.20, "atk": 1.10, "def_": 0.75, "speed": -1},
	"GUARDIAO": {"name": "GUARDIAO", "hp": 1.00, "atk": 0.85, "def_": 1.35, "speed": -1},
	"DUELISTA": {"name": "DUELISTA", "hp": 0.75, "atk": 1.00, "def_": 0.75, "speed": 2},
}

COMMON_ARCHETYPES_BY_TIER = {
	1: ("BASICO", "BRUTO", ("BRUTO",)),
	2: ("GUARDIAO", "GUARDIAO", ("BASICO", "BRUTO")),
	3: ("DUELISTA", "DUELISTA", ("BRUTO", "GUARDIAO")),
	4: ("BRUTO", "GUARDIAO", ("DUELISTA",)),
}

ELITE_ARCHETYPE_BY_TIER = {1: "BRUTO", 2: "GUARDIAO", 3: "DUELISTA", 4: "DUELISTA"}

ELITE_NAMES = {
	"BRUTO": "BRUTO ELITE",
	"GUARDIAO": "GUARDIAO ELITE",
	"DUELISTA": "DUELISTA ELITE",
}

BOSS_DEFINITIONS = {
	5: {"name": "COLOSSO", "archetype": "BRUTO", "pattern": ("PREPARAR", "GOLPE_FORTE", "RECOMPOR", "ATACAR")},
	10: {"name": "SENTINELA", "archetype": "GUARDIAO", "pattern": ("DEFENDER", "ATACAR", "ATACAR", "ATACAR", "RECOMPOR")},
	15: {"name": "ESPADACHIM", "archetype": "DUELISTA", "pattern": ("ATACAR", "ATACAR", "ATACAR", "RECOMPOR")},
	20: {"name": "COMANDANTE", "archetype": "BASICO", "pattern": ("PREPARAR", "GOLPE_FORTE", "RECOMPOR", "DEFENDER", "ATACAR", "ATACAR", "ATACAR")},
}

PATTERNS = {
	"BASICO": ("ATACAR",),
	"BRUTO": ("PREPARAR", "GOLPE_FORTE", "RECOMPOR"),
	"GUARDIAO": ("DEFENDER", "ATACAR", "ATACAR"),
	"DUELISTA": ("ATACAR", "ATACAR", "RECOMPOR"),
}

ELITE_PATTERNS = {
	"BRUTO": ("ATACAR", "PREPARAR", "GOLPE_FORTE", "RECOMPOR"),
	"GUARDIAO": ("DEFENDER", "ATACAR", "DEFENDER", "ATACAR"),
	"DUELISTA": ("ATACAR", "ATACAR", "ATACAR", "RECOMPOR"),
}

LEVEL_UP_POINTS = 3

STAT_POINT_VALUE = {
	"hp": 5,
	"atk": 1,
	"def_": 1,
	"speed": 1,
	"luck": 1,
}

XP_BASE = 20
XP_GROWTH = 15

DEFESA_ESCALA = 10.0
MULTIPLICADOR_DEFENDER = 0.5
MULTIPLICADOR_CONTRA_ATAQUE = 1.5
MULTIPLICADOR_GOLPE_FORTE = 1.75
DANO_MINIMO = 1