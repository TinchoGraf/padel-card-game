import copy
from game.ball import Ball
from game.player import Player
from data.cards_data import generar_mazo_basico


class Game:
    def __init__(self):
        self.jugador1 = Player("Jugador 1")
        self.jugador2 = Player("Jugador 2")
        self.ball = Ball()
        self.turno = self.jugador1
        self.mazo = generar_mazo_basico()
        self.historial = []
        self.ultima_carta = None
        self.puntos = {self.jugador1: 0, self.jugador2: 0}
        self.juego_terminado = False
        self.puntos_para_ganar = 7

    def iniciar_con_seleccion(self, sel_j1, sel_j2):
        def aplicar(player, sel):
            player.bonus_golpes = [
                sel["drive"]["bonus_golpe"],
                sel["reves"]["bonus_golpe"],
            ]
            player.especiales = (
                copy.deepcopy(sel["drive"]["especiales"]) +
                copy.deepcopy(sel["reves"]["especiales"])
            )
        aplicar(self.jugador1, sel_j1)
        aplicar(self.jugador2, sel_j2)
        self.repartir_cartas()

    # ── CARTAS ──────────────────────────────────────────────────────

    def repartir_cartas(self):
        for _ in range(5):
            if self.mazo:
                self.jugador1.mano.append(self.mazo.pop())
            if self.mazo:
                self.jugador2.mano.append(self.mazo.pop())

    # ── TURNOS ──────────────────────────────────────────────────────

    def cambiar_turno(self):
        self.turno = (
            self.jugador2 if self.turno == self.jugador1 else self.jugador1
        )

    # ── VALIDACIÓN ──────────────────────────────────────────────────

    def carta_valida(self, carta):
        if self.ultima_carta is None:
            return True

        if carta.valida_despues_de and not carta.es_valida_en_contexto(self.ultima_carta):
            return False

        if self.ball.estado.value >= 3:
            return carta.es_especial and carta.efecto_especial <= -2

        # BandeVibora: solo Dos Paredes la defiende
        if (
            self.ultima_carta.nombre == "BandeVibora ★"
            and carta.tipo.name == "DEFENSIVO"
            and not carta.es_especial
        ):
            return carta.nombre == "Dos Paredes"

        tipo_anterior = self.ultima_carta.tipo.name
        tipo_actual = carta.tipo.name

        # DESPUÉS — las especiales respetan el flujo de tipos
        if carta.es_especial:
            if tipo_anterior == "ATAQUE":
                return carta.tipo.name in ["DEFENSIVO", "TRANSICION"]
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

    # ── GAMEPLAY ────────────────────────────────────────────────────

    def aplicar_carta(self, carta):
        efecto = carta.efecto_real(self.ultima_carta, self.ball.estado)

        if carta.nombre.replace(" ★", "") in self.turno.bonus_golpes:
            efecto += 1

        self.ball.aplicar_cambio(efecto)
        self.historial.append(carta)
        self.ultima_carta = carta

        if self.ball.estado.value >= 3:
            self.sumar_punto(self.turno)
            if not self.juego_terminado:
                self.reiniciar_rally()
            return True

        return False

    def jugar_carta(self, idx, es_especial=False):
        jugador = self.turno
        carta = jugador.especiales[idx] if es_especial else jugador.mano[idx]

        if not self.carta_valida(carta):
            return "jugada_invalida"

        if es_especial:
            jugador.especiales.pop(idx)
        else:
            jugador.mano.pop(idx)

        hubo_punto = self.aplicar_carta(carta)

        if hubo_punto:
            return "punto"

        self.cambiar_turno()

        if not self.obtener_cartas_validas():
            rival = self.jugador2 if self.turno == self.jugador1 else self.jugador1
            self.sumar_punto(rival)
            if not self.juego_terminado:
                self.reiniciar_rally()
            return "sin_jugada"

        return "ok"

    # ── PUNTOS ──────────────────────────────────────────────────────

    def sumar_punto(self, ganador):
        self.puntos[ganador] += 1
        self.verificar_ganador()

    def verificar_ganador(self):
        p1 = self.puntos[self.jugador1]
        p2 = self.puntos[self.jugador2]
        if (
            (p1 >= self.puntos_para_ganar or p2 >= self.puntos_para_ganar)
            and abs(p1 - p2) >= 2
        ):
            ganador = self.jugador1 if p1 > p2 else self.jugador2
            print(f"🏆 GANADOR: {ganador.nombre}")
            self.juego_terminado = True

    # ── RESET ───────────────────────────────────────────────────────

    def reiniciar_rally(self):
        self.ball = Ball()
        self.ultima_carta = None
        self.mazo = generar_mazo_basico()
        self.jugador1.mano = []
        self.jugador2.mano = []
        self.repartir_cartas()