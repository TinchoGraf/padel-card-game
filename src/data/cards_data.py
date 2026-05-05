from game.card import Card
from game.enums import TipoGolpe
import random


def generar_mazo_basico():
    cartas = [
        Card("Volea", TipoGolpe.ATAQUE, +1),
        Card("Vibora", TipoGolpe.ATAQUE, +1),
        Card("Smash", TipoGolpe.ATAQUE, +1),
        Card("Globo", TipoGolpe.DEFENSIVO, -1),
        Card("Defensa simple", TipoGolpe.DEFENSIVO, -1),
        Card("Chiquita", TipoGolpe.TRANSICION, 0),
        Card("Bandeja", TipoGolpe.TRANSICION, 0),
    ]

    mazo = cartas * 3  # 🔽 antes 5 → ahora menos cartas
    random.shuffle(mazo)

    return mazo


def generar_cartas_especiales():
    return [
        Card("Defensa PRO", TipoGolpe.DEFENSIVO, es_especial=True, efecto_especial=-2),
        Card("Ataque PRO", TipoGolpe.ATAQUE, es_especial=True, efecto_especial=2),
    ]