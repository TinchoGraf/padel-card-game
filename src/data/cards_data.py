# Archivo que contiene la función para generar el mazo básico de cartas del juego
from game.card import Card
from game.enums import TipoGolpe
import random

# Función para generar un mazo básico de cartas
def generar_mazo_basico():
    # Definimos un conjunto de cartas con diferentes tipos y efectos
    cartas = [
        Card("Volea", TipoGolpe.ATAQUE, +1),
        Card("Vibora", TipoGolpe.ATAQUE, +1),
        Card("Smash", TipoGolpe.ATAQUE, +1),
        Card("Globo", TipoGolpe.DEFENSIVO, -1),
        Card("Defensa simple", TipoGolpe.DEFENSIVO, -1),
        Card("Chiquita", TipoGolpe.TRANSICION, 0),
        Card("Bandeja", TipoGolpe.TRANSICION, 0),
    ]

    # duplicamos para tener mazo grande
    mazo = cartas * 5
    random.shuffle(mazo)

    return mazo