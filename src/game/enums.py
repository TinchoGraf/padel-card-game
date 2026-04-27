from enum import Enum

# Enums para el juego de padel
class TipoGolpe(Enum):
    DEFENSIVO = "defensivo"
    TRANSICION = "transicion"
    ATAQUE = "ataque"
    ESPECIAL = "especial"

# Enums para el estado de la pelota
class EstadoPelota(Enum):
    VERDE = -1
    AMARILLO = 0
    ROJO = 1
    ROJO_PLUS = 2