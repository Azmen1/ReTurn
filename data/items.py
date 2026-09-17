WEAPON_ITEMS = {
	"espada_curta": {
		"nome": "Espada Curta",
		"tipo": "arma",
		"valor": 0,
		"bonus_atk": 3,
	},
	"machado": {
		"nome": "Machado",
		"tipo": "arma",
		"valor": 0,
		"bonus_atk": 6,
	},
}

ARMOR_ITEMS = {
	"colete": {
		"nome": "Colete",
		"tipo": "armadura",
		"valor": 0,
		"bonus_defesa": 2,
	},
	"armadura_ferro": {
		"nome": "Armadura de Ferro",
		"tipo": "armadura",
		"valor": 0,
		"bonus_defesa": 5,
	},
}

CONSUMABLE_ITEMS = {
	"pocao": {
		"nome": "Pocao de Cura",
		"tipo": "cura",
		"valor": 10,
	},
	"pocao_grande": {
		"nome": "Pocao Grande",
		"tipo": "cura",
		"valor": 20,
	},
	"tonico_forca": {
		"nome": "Tonico de Forca",
		"tipo": "buff_atk",
		"valor": 3,
	},
	"elixir_defesa": {
		"nome": "Elixir de Defesa",
		"tipo": "buff_defesa",
		"valor": 3,
	},
}

TOTEM_ITEMS = {
	"totem_vitalidade": {
		"nome": "Totem da Vitalidade",
		"tipo": "totem",
		"valor": 15,
		"habilidade": "cura",
	},
	"totem_furia": {
		"nome": "Totem da Furia",
		"tipo": "totem",
		"valor": 5,
		"habilidade": "buff_atk",
	},
}

ITEMS = {
	**WEAPON_ITEMS,
	**ARMOR_ITEMS,
	**CONSUMABLE_ITEMS,
	**TOTEM_ITEMS,
}
