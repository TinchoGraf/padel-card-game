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

        self.puntos_para_ganar = 7
        self.juego_terminado = False

        self.log = ""

        self.repartir_cartas()

        self.jugador1.especiales = generar_cartas_especiales()
        self.jugador2.especiales = generar_cartas_especiales()

    def repartir_cartas(self):
        for _ in range(5):
            if self.mazo:
                self.jugador1.mano.append(self.mazo.pop())
            if self.mazo:
                self.jugador2.mano.append(self.mazo.pop())

    def cambiar_turno(self):
        self.turno = (
            self.jugador2 if self.turno == self.jugador1 else self.jugador1
        )

    # 🔴 NUEVO: chequeo automático
    def puede_jugar(self):
        jugador = self.turno

        # especiales válidas
        especiales_validas = [
            c for c in jugador.especiales if self.carta_valida(c)
        ]

        normales_validas = [
            c for c in jugador.mano if self.carta_valida(c)
        ]

        return len(especiales_validas) > 0 or len(normales_validas) > 0

    # 🔴 NUEVO: resolver turno si no puede jugar
    def resolver_turno_si_bloqueado(self):
        if self.puede_jugar():
            return False  # puede jugar

        rival = (
            self.jugador2 if self.turno == self.jugador1 else self.jugador1
        )

        self.log = f"{self.turno.nombre} no puede jugar → PUNTO para {rival.nombre}"

        self.sumar_punto(rival)

        if not self.juego_terminado:
            self.reiniciar_rally()

        return True  # se resolvió automáticamente

    def aplicar_carta(self, carta):
        if carta.es_especial:
            self.ball.aplicar_cambio(carta.efecto_especial)
        else:
            self.ball.aplicar_cambio(carta.efecto_base)

        self.historial.append(carta)
        self.ultima_carta = carta

        # 🔴 ROJO_PLUS
        if self.ball.estado.name == "ROJO_PLUS":
            self.sumar_punto(self.turno)

            if not self.juego_terminado:
                self.reiniciar_rally()

            return True

        return False

    def carta_valida(self, carta):
        # primera jugada libre
        if self.ultima_carta is None:
            return True
    
        tipo_anterior = self.ultima_carta.tipo.name
        tipo_actual = carta.tipo.name
    
        # 🔴 CASO CRÍTICO: pelota en ROJO
        if self.ball.estado.name == "ROJO":
            # solo puede defender o transicionar
            if carta.es_especial:
                # solo defensa especial
                return carta.efecto_especial < 0
            return tipo_actual in ["DEFENSIVO", "TRANSICION"]
    
        # 🔴🔥 ROJO_PLUS → solo defensa especial
        if self.ball.estado.name == "ROJO_PLUS":
            return carta.es_especial and carta.efecto_especial < 0
    
        # 🟡 Lógica normal
        if tipo_anterior == "ATAQUE":
            return tipo_actual in ["DEFENSIVO", "TRANSICION"]
    
        if tipo_anterior == "DEFENSIVO":
            return tipo_actual in ["TRANSICION", "ATAQUE"]
    
        if tipo_anterior == "TRANSICION":
            return True
    
        return True

    def sumar_punto(self, ganador):
        self.puntos[ganador] += 1

        self.log = f"PUNTO para {ganador.nombre}\nMarcador: {self.puntos[self.jugador1]} - {self.puntos[self.jugador2]}"

        self.verificar_ganador()

    def reiniciar_rally(self):
        self.ball = Ball()
        self.ultima_carta = None

        self.mazo = generar_mazo_basico()

        self.jugador1.mano = []
        self.jugador2.mano = []

        self.repartir_cartas()

    def verificar_ganador(self):
        p1 = self.puntos[self.jugador1]
        p2 = self.puntos[self.jugador2]

        if (p1 >= self.puntos_para_ganar or p2 >= self.puntos_para_ganar) and abs(p1 - p2) >= 2:
            ganador = self.jugador1 if p1 > p2 else self.jugador2
            self.log = f"🏆 GANADOR: {ganador.nombre}"
            self.juego_terminado = True