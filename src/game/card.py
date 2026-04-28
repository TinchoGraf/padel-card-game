from game.enums import TipoGolpe

class Card:
    def __init__(self, nombre, tipo, efecto_base=0, es_especial=False, efecto_especial=0):
        self.nombre = nombre
        self.tipo = tipo
        self.efecto_base = efecto_base
        self.es_especial = es_especial
        self.efecto_especial = efecto_especial

    def __str__(self):
        if self.es_especial:
            return f"{self.nombre} (ESPECIAL {self.tipo.value})"
        return f"{self.nombre} ({self.tipo.value})"

    def __repr__(self):
        return f"{self.nombre} ({self.tipo.value})"