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

ENEMY_STAT_RANGE_BY_TIER = {
	1: {"hp": (20, 24), "atk": (4, 5), "def_": (1, 2), "speed": (2, 3), "luck": (1, 2)},
	2: {"hp": (26, 32), "atk": (6, 8), "def_": (3, 4), "speed": (4, 5), "luck": (3, 4)},
	3: {"hp": (34, 42), "atk": (9, 11), "def_": (5, 6), "speed": (6, 7), "luck": (5, 6)},
	4: {"hp": (44, 54), "atk": (12, 15), "def_": (7, 9), "speed": (8, 9), "luck": (7, 9)},
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
DANO_MINIMO = 1