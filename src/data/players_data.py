import copy
from game.card import Card
from game.enums import TipoGolpe


JUGADORES = {
    "Tapia": {
        "nombre": "Tapia",
        "posicion": "reves",
        "bonus_golpe": "Smash Kick",
        "especiales": [
            Card("Smash Kick ★", TipoGolpe.ATAQUE,
                 es_especial=True, efecto_especial=2),
            Card("Salida por la Puerta ★", TipoGolpe.DEFENSIVO,
                 es_especial=True, efecto_especial=-2),
        ],
    },
    "Coello": {
        "nombre": "Coello",
        "posicion": "drive",
        "bonus_golpe": "Smash Plano Potencia",
        "especiales": [
            Card("Smash Plano ★", TipoGolpe.ATAQUE,
                 es_especial=True, efecto_especial=2),
            Card("Chiquita ★", TipoGolpe.TRANSICION,
                 es_especial=True, efecto_especial=-1),
        ],
    },
    "Galán": {
        "nombre": "Galán",
        "posicion": "reves",
        "bonus_golpe": "Smash Kick",
        "especiales": [
            Card("Smash Kick ★", TipoGolpe.ATAQUE,
                 es_especial=True, efecto_especial=2),
            Card("Recuperación Red ★", TipoGolpe.DEFENSIVO,
                 es_especial=True, efecto_especial=-2,
                 valida_despues_de=["Smash x3", "Smash Kick",
                                    "Smash Plano Potencia",
                                    "Smash Kick ★", "Smash Plano ★"]),
        ],
    },
    "Chingotto": {
        "nombre": "Chingotto",
        "posicion": "drive",
        "bonus_golpe": "Vibora",
        "especiales": [
            Card("BandeVibora ★", TipoGolpe.ATAQUE,
                 es_especial=True, efecto_especial=2),
            Card("Globo ★", TipoGolpe.DEFENSIVO,
                 es_especial=True, efecto_especial=-2),
        ],
    },
}