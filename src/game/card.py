from game.enums import TipoGolpe


class Card:
    def __init__(
        self,
        nombre,
        tipo,
        efecto_base=0,
        es_especial=False,
        efecto_especial=0,
        restriccion_previa=None,
        valida_despues_de=None,
    ):
        self.nombre = nombre
        self.tipo = tipo
        self.efecto_base = efecto_base
        self.es_especial = es_especial
        self.efecto_especial = efecto_especial
        self.restriccion_previa = restriccion_previa or []
        self.valida_despues_de = valida_despues_de or []

    def efecto_real(self, ultima_carta, estado_pelota=None):
        base = self.efecto_especial if self.es_especial else self.efecto_base

        if ultima_carta and ultima_carta.nombre in self.restriccion_previa:
            return 0

        if self.nombre == "Chiquita con Pared" and estado_pelota is not None:
            from game.enums import EstadoPelota
            if estado_pelota in (EstadoPelota.ROJO, EstadoPelota.ROJO_PLUS):
                return -1
            return 1

        if self.nombre == "Bandeja" and ultima_carta is not None:
            if "Globo" in ultima_carta.nombre:
                return 1
            return 0

        if self.nombre == "A los Pies":
            return 1

        return base

    def es_valida_en_contexto(self, ultima_carta):
        if not self.valida_despues_de:
            return True
        if ultima_carta is None:
            return False
        return ultima_carta.nombre in self.valida_despues_de

    def __str__(self):
        if self.es_especial:
            return f"{self.nombre} (ESPECIAL {self.tipo.value})"
        return f"{self.nombre} ({self.tipo.value})"

    def __repr__(self):
        return f"{self.nombre} ({self.tipo.value})"