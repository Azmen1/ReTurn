class Item:
	def __init__(self, nome, tipo, valor):
		self.nome = nome
		self.tipo = tipo
		self.valor = valor
		self.efeito = {
			"tipo": tipo,
			"valor": valor,
		}

	def __repr__(self):
		return f"Item(nome={self.nome!r}, tipo={self.tipo!r}, valor={self.valor!r})"
