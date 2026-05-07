from game.card import Card
from game.enums import TipoGolpe
import random


def generar_mazo_basico():
    cartas = [

        # ── DEFENSIVOS ──────────────────────────────────────────────
        Card("Dos Paredes", TipoGolpe.DEFENSIVO, efecto_base=-1,
             valida_despues_de=["Bandeja", "Vibora", "BandeVibora ★"]),

        Card("Defensa con Pared", TipoGolpe.DEFENSIVO, efecto_base=-1,
             valida_despues_de=["Volea", "Chiquita con Pared", "Bandeja", "Pasarla"]),

        Card("Defensa sin Pared", TipoGolpe.DEFENSIVO, efecto_base=-1,
             valida_despues_de=["Volea", "Chiquita con Pared", "Bandeja", "Pasarla"]),

        Card("Globo", TipoGolpe.DEFENSIVO, efecto_base=-1),

        Card("Recuperación Red", TipoGolpe.DEFENSIVO, efecto_base=-1,
             valida_despues_de=["Smash Kick", "Smash Plano Potencia",
                                "Smash Kick ★", "Smash Plano ★"]),

        Card("Recuperación x3", TipoGolpe.DEFENSIVO, efecto_base=-1,
             valida_despues_de=["Smash x3"]),

        Card("Chiquita con Pared", TipoGolpe.DEFENSIVO, efecto_base=-1),

        Card("Al Cuerpo", TipoGolpe.DEFENSIVO, efecto_base=-1),

        # ── TRANSICIÓN ───────────────────────────────────────────────
        Card("A los Pies", TipoGolpe.TRANSICION, efecto_base=0),

        Card("Bandeja", TipoGolpe.TRANSICION, efecto_base=0),

        Card("Pasarla", TipoGolpe.TRANSICION, efecto_base=0),

        # ── ATAQUE ───────────────────────────────────────────────────
        Card("Volea", TipoGolpe.ATAQUE, efecto_base=1,
             restriccion_previa=["Al Cuerpo"]),

        Card("Vibora", TipoGolpe.ATAQUE, efecto_base=1,
             restriccion_previa=["Globo", "Globo ★"]),

        Card("Smash x3", TipoGolpe.ATAQUE, efecto_base=1,
             restriccion_previa=["Globo", "Globo ★"]),

        Card("Rulo a la Reja", TipoGolpe.ATAQUE, efecto_base=1,
             restriccion_previa=["Globo", "Globo ★"]),

        Card("Gancho a la Reja", TipoGolpe.ATAQUE, efecto_base=1,
             restriccion_previa=["Globo", "Globo ★"]),

        Card("Smash Kick", TipoGolpe.ATAQUE, efecto_base=1,
             restriccion_previa=["Globo", "Globo ★"]),

        Card("Smash Plano Potencia", TipoGolpe.ATAQUE, efecto_base=1,
             restriccion_previa=["Globo", "Globo ★"]),

        Card("Kick x4", TipoGolpe.ATAQUE, efecto_base=1,
             restriccion_previa=["Globo", "Globo ★"]),

        Card("Dejada", TipoGolpe.ATAQUE, efecto_base=1,
             restriccion_previa=["Al Cuerpo"]),
    ]

    frecuencias = {
        "Globo": 3,
        "Volea": 3,
        "Smash x3": 3,
        "Bandeja": 3,
        "Pasarla": 2,
        "Defensa con Pared": 2,
        "Defensa sin Pared": 2,
        "Vibora": 2,
        "Smash Kick": 2,
        "Chiquita con Pared": 2,
        "Al Cuerpo": 2,
    }

    mazo = []
    for carta in cartas:
        copias = frecuencias.get(carta.nombre, 1)
        mazo.extend([carta] * copias)

    random.shuffle(mazo)
    return mazo