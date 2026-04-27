from game.game import Game


def main():
    game = Game()

    print("=== INICIO DEL JUEGO ===")

    while True:
        game.jugar_turno()

        # condición de corte temporal
        if len(game.jugador1.mano) == 0 and len(game.jugador2.mano) == 0:
            print("Se terminaron las cartas")
            break

        #condicion para repartir 3 cartas a cada jugador cuando se quedan sin cartas en la mano, para que el juego no se detenga
        if (
            len(game.jugador1.mano) == 0 and
            len(game.jugador2.mano) == 0 and
            game.ball.estado.value == 0
        ):
            game.repartir_3_cartas()


if __name__ == "__main__":
    main()