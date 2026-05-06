from game.ball import Ball
from game.player import Player
from data.cards_data import generar_cartas_especiales, generar_mazo_basico


class Game:
    def __init__(self):
        self.jugador1 = Player("Jugador 1")
        self.jugador2 = Player("Jugador 2")
        self.ball = Ball()
        self.turno = self.jugador1
        self.mazo = generar_mazo_basico()
        self.historial = []

        self.ultima_carta = None

        self.puntos = {
            self.jugador1: 0,
            self.jugador2: 0
        }

        self.juego_terminado = False
        self.puntos_para_ganar = 7

        self.repartir_cartas()

        # especiales (1 y 1 por simplicidad ahora)
        self.jugador1.especiales = generar_cartas_especiales()[:2]
        self.jugador2.especiales = generar_cartas_especiales()[:2]

    # ---------------------------
    # CARTAS
    # ---------------------------

    def repartir_cartas(self):
        for _ in range(5):
            if self.mazo:
                self.jugador1.mano.append(self.mazo.pop())
            if self.mazo:
                self.jugador2.mano.append(self.mazo.pop())

    def repartir_3_cartas(self):
        for _ in range(3):
            if self.mazo:
                self.jugador1.mano.append(self.mazo.pop())
            if self.mazo:
                self.jugador2.mano.append(self.mazo.pop())

    # ---------------------------
    # TURNOS
    # ---------------------------

    def cambiar_turno(self):
        self.turno = (
            self.jugador2 if self.turno == self.jugador1 else self.jugador1
        )

    # ---------------------------
    # CORE GAMEPLAY
    # ---------------------------

    def aplicar_carta(self, carta):
        # aplicar efecto
        if carta.es_especial:
            self.ball.aplicar_cambio(carta.efecto_especial)
        else:
            self.ball.aplicar_cambio(carta.efecto_base)

        self.historial.append(carta)
        self.ultima_carta = carta

        # 🔴 ROJO_PLUS → punto
        if self.ball.fuerza >= 3:
            self.sumar_punto(self.turno)

            if not self.juego_terminado:
                self.reiniciar_rally()

            return True

        return False

    # ---------------------------
    # VALIDACIONES
    # ---------------------------

    def carta_valida(self, carta):
        # primera jugada
        if self.ultima_carta is None:
            return True

        # ROJO_PLUS → solo defensa especial
        if self.ball.fuerza >= 3:
            return carta.es_especial and carta.efecto_especial == -2

        tipo_anterior = self.ultima_carta.tipo.name
        tipo_actual = carta.tipo.name

        if carta.es_especial:
            return True

        if tipo_anterior == "ATAQUE":
            return tipo_actual in ["DEFENSIVO", "TRANSICION"]

        if tipo_anterior == "DEFENSIVO":
            return tipo_actual in ["TRANSICION", "ATAQUE"]

        if tipo_anterior == "TRANSICION":
            return True

        return True

    def obtener_cartas_validas(self):
        return [
            c for c in (self.turno.mano + self.turno.especiales)
            if self.carta_valida(c)
        ]

    # ---------------------------
    # JUGAR (para UI)
    # ---------------------------

    def jugar_carta(self, idx, es_especial=False):
        jugador = self.turno

        if es_especial:
            carta = jugador.especiales[idx]
        else:
            carta = jugador.mano[idx]

        if not self.carta_valida(carta):
            return "jugada_invalida"

        # remover carta
        if es_especial:
            jugador.especiales.pop(idx)
        else:
            jugador.mano.pop(idx)

        hubo_punto = self.aplicar_carta(carta)

        if hubo_punto:
            return "punto"

        # cambiar turno
        self.cambiar_turno()

        # verificar si el nuevo jugador puede jugar
        if not self.obtener_cartas_validas():
            rival = (
                self.jugador2 if self.turno == self.jugador1 else self.jugador1
            )

            self.sumar_punto(rival)

            if not self.juego_terminado:
                self.reiniciar_rally()

            return "sin_jugada"

        return "ok"

    # ---------------------------
    # PUNTOS
    # ---------------------------

    def sumar_punto(self, ganador):
        self.puntos[ganador] += 1

        print(f"\nPUNTO para {ganador.nombre}")
        print(
            f"Marcador: {self.jugador1.nombre} {self.puntos[self.jugador1]} - "
            f"{self.jugador2.nombre} {self.puntos[self.jugador2]}"
        )

        self.verificar_ganador()

    def verificar_ganador(self):
        p1 = self.puntos[self.jugador1]
        p2 = self.puntos[self.jugador2]

        if (
            (p1 >= self.puntos_para_ganar or p2 >= self.puntos_para_ganar)
            and abs(p1 - p2) >= 2
        ):
            ganador = self.jugador1 if p1 > p2 else self.jugador2
            print(f"\n🏆 GANADOR: {ganador.nombre}")
            self.juego_terminado = True

    # ---------------------------
    # RESET
    # ---------------------------

    def reiniciar_rally(self):
        self.ball = Ball()
        self.ultima_carta = None

        self.mazo = generar_mazo_basico()

        self.jugador1.mano = []
        self.jugador2.mano = []

        self.repartir_cartas()

        print("\n--- Nuevo punto ---\n")