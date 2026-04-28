# Archivo que contiene la clase principal del juego, que maneja la lógica del mismo
from game.ball import Ball
from game.player import Player
from data.cards_data import generar_cartas_especiales, generar_mazo_basico

# Clase principal del juego, que maneja la lógica del mismo
class Game:
    def __init__(self):
        self.jugador1 = Player("Jugador 1")
        self.jugador2 = Player("Jugador 2")
        self.ball = Ball()
        self.turno = self.jugador1
        self.mazo = generar_mazo_basico()
        self.historial = []

        self.ultima_carta = None  # 👈 YA lo habíamos agregado antes

        # 👇 NUEVO (marcador)
        self.puntos = {
            self.jugador1: 0,
            self.jugador2: 0
        }

        self.reparto_realizado = False  # Flag para controlar el reparto inicial

        self.repartir_cartas()

        self.juego_terminado = False  # Flag para controlar el fin del juego

        self.puntos_para_ganar = 7  # Puntos necesarios para ganar el juego

        from data.cards_data import generar_cartas_especiales

        self.jugador1.especiales = generar_cartas_especiales()
        self.jugador2.especiales = generar_cartas_especiales()

    # Método para repartir cartas a ambos jugadores al inicio del juego
    def repartir_cartas(self):
        for _ in range(10):
            if self.mazo:
                self.jugador1.mano.append(self.mazo.pop())
            if self.mazo:
                self.jugador2.mano.append(self.mazo.pop())

                
    # Método para cambiar el turno entre los jugadores
    def cambiar_turno(self):
        self.turno = (
            self.jugador2 if self.turno == self.jugador1 else self.jugador1
        )

    # Método para aplicar el efecto de una carta jugada, modificando el estado de la pelota
    def aplicar_carta(self, carta):
        if carta.es_especial:
            self.ball.aplicar_cambio(carta.efecto_especial)
        else:
            self.ball.aplicar_cambio(carta.efecto_base)

        self.historial.append(carta)

        if self.ball.estado.value == 2:
            self.sumar_punto(self.turno)

            if not self.juego_terminado:
                self.reiniciar_rally()

            return True # hubo punto

        return False # no hubo punto

    # Método para mostrar el estado actual del juego, incluyendo el estado de la pelota
    def mostrar_estado(self):
        print(self.ball)
        print("\nESPECIALES:")
        for i, carta in enumerate(self.turno.especiales):
            print(f"E{i}: {carta}")

    # Método para mostrar la mano del jugador actual y permitirle elegir una carta para jugar
    def mostrar_mano(self):
        print(f"\nTurno de {self.turno.nombre}")

        grupos = {
            "DEFENSIVO": [],
            "TRANSICION": [],
            "ATAQUE": []
        }

        for i, carta in enumerate(self.turno.mano):
            grupos[carta.tipo.name].append((i, carta))

        for tipo, cartas in grupos.items():
            if cartas:
                print(f"\n{tipo}:")
                for i, carta in cartas:
                    print(f"{i}: {carta}")

    # Método para manejar el turno de un jugador, mostrando su mano, permitiéndole elegir una carta y aplicando su efecto
    def jugar_turno(self):

        # CASO: sin cartas
        if len(self.jugador1.mano) == 0 and len(self.jugador2.mano) == 0:

            if self.ball.estado.value == 0:
                print("\nNo hay cartas, se reparten 3 nuevas\n")
                self.repartir_3_cartas()
                return
            else:
                print("No hay cartas y no se puede continuar el rally")

                # El punto es para el rival
                rival = self.jugador2 if self.turno == self.jugador1 else self.jugador1
                self.sumar_punto(rival)
                self.reiniciar_rally()
                return

        self.mostrar_mano()

        cartas_validas = self.obtener_cartas_validas()

        if not cartas_validas:
            print(f"{self.turno.nombre} no puede responder.")

            if self.ball.estado.value == 1:
                rival = self.jugador2 if self.turno == self.jugador1 else self.jugador1
                self.sumar_punto(rival)
                self.reiniciar_rally()
                return

            self.cambiar_turno()
            return
    
        while True:
            try:
               eleccion = input("Elegí una carta: ")

                # ESPECIAL
               if eleccion.startswith("E"):
                  idx = int(eleccion[1:])
                  carta = self.turno.especiales[idx]
                  es_especial = True

               else:
                  idx = int(eleccion)
                  carta = self.turno.mano[idx]
                  es_especial = False
    
               if not self.carta_valida(carta):
                  print("No podés jugar esa carta ahora.")
                  continue
              
                # recién acá eliminamos la carta
               if es_especial:
                  self.turno.especiales.pop(idx)
               else:
                  self.turno.mano.pop(idx)
    
               break
          
            except:
                print("Entrada inválida")
    
            print(f"{self.turno.nombre} juega {carta}")
    
            hubo_punto = self.aplicar_carta(carta)
            self.ultima_carta = carta
    
            self.mostrar_estado()
    
            if hubo_punto:
                return
    
            self.cambiar_turno()
    
    
    def carta_valida(self, carta):
        if self.ultima_carta is None:
            return True  # primera jugada libre

        tipo_anterior = self.ultima_carta.tipo
        tipo_actual = carta.tipo

        if tipo_anterior.name == "ATAQUE":
            return tipo_actual.name in ["DEFENSIVO", "TRANSICION"]

        if tipo_anterior.name == "DEFENSIVO":
            return tipo_actual.name in ["TRANSICION", "ATAQUE"]

        if tipo_anterior.name == "TRANSICION":
            return True

        return True
    
    def obtener_cartas_validas(self):
        return [c for c in self.turno.mano if self.carta_valida(c)]
    
    #funcion para repartir 3 cartas a cada jugador, se llama cuando se quedan sin cartas en la mano, para que el juego no se detenga
    def repartir_3_cartas(self):
        for _ in range(3):
            if self.mazo:
                self.jugador1.mano.append(self.mazo.pop())
            if self.mazo:
                self.jugador2.mano.append(self.mazo.pop())

        print("\nSe reparten 3 nuevas cartas a cada jugador\n")

    #Funcion para sumar puntos en cada ronda
    def sumar_punto(self, ganador):
        self.puntos[ganador] += 1

        print(f"\nPUNTO para {ganador.nombre}")
        print(f"Marcador: {self.jugador1.nombre} {self.puntos[self.jugador1]} - {self.jugador2.nombre} {self.puntos[self.jugador2]}")

        self.verificar_ganador()
        if self.juego_terminado:
            return

    #Reset del rally, se llama después de sumar puntos, para reiniciar la pelota y la última carta jugada
    def reiniciar_rally(self):
        from data.cards_data import generar_mazo_basico  # import local

        self.ball = Ball()
        self.ultima_carta = None

        # 🔥 REGENERAR MAZO
        self.mazo = generar_mazo_basico()

        # Limpiar manos
        self.jugador1.mano = []
        self.jugador2.mano = []

        # Repartir nuevas cartas
        self.repartir_cartas()

        print("\n--- Nuevo punto (cartas nuevas) ---\n")

    # Método para verificar si alguno de los jugadores ha alcanzado la condición de victoria (7 puntos con diferencia de 2)
    def verificar_ganador(self):
        p1 = self.puntos[self.jugador1]
        p2 = self.puntos[self.jugador2]

        if (p1 >= self.puntos_para_ganar or p2 >= self.puntos_para_ganar) and abs(p1 - p2) >= 2:
            ganador = self.jugador1 if p1 > p2 else self.jugador2
            print(f"\n🏆 GANADOR: {ganador.nombre}")
            self.juego_terminado = True