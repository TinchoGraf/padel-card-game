from game.enums import EstadoPelota

# Clase para representar la pelota y su estado
class Ball:
    # Inicialmente la pelota está en estado AMARILLO
    def __init__(self):
        self.estado = EstadoPelota.AMARILLO

    # Método para aplicar un cambio al estado de la pelota
    def aplicar_cambio(self, valor):
        nuevo_valor = self.estado.value + valor

        # Clamp entre -1 y 2
        nuevo_valor = max(-1, min(2, nuevo_valor))

        self.estado = EstadoPelota(nuevo_valor)

    # Representación de la pelota para impresión
    def __repr__(self):
        return f"Pelota: {self.estado.name}"