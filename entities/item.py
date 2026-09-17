class Item:
	def __init__(self, nome, tipo, valor=0, *, bonus_atk=0, bonus_defesa=0):
		self.nome = nome
		self.tipo = tipo
		self.valor = valor
		self.bonus_atk = int(bonus_atk)
		self.bonus_defesa = int(bonus_defesa)
		self.efeito = {
			"tipo": tipo,
			"valor": valor,
		}

	def __repr__(self):
		return f"Item(nome={self.nome!r}, tipo={self.tipo!r}, valor={self.valor!r})"
	