from game.enums import EstadoPelota

class Ball:
    def __init__(self):
        self.estado = EstadoPelota.AMARILLO
        self.fuerza = 1  # nueva mecánica visual

    def aplicar_cambio(self, valor):
        # actualizar estado correctamente
        nuevo_valor = self.estado.value + valor

        # clamp entre 0 y 3
        nuevo_valor = max(0, min(3, nuevo_valor))

        self.estado = EstadoPelota(nuevo_valor)

        # actualizar fuerza (para barra visual)
        if valor > 0:
            self.fuerza += valor
        elif valor < 0:
            self.fuerza = max(1, self.fuerza + valor)

    def __repr__(self):
        return f"Pelota: {self.estado.name} (Fuerza {self.fuerza})"