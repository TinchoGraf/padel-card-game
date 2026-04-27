from game.game import Game


def main():
    game = Game()

    print("=== INICIO DEL JUEGO ===")

    while not game.juego_terminado:
        game.jugar_turno()

        # condición de corte temporal
        if len(game.jugador1.mano) == 0 and len(game.jugador2.mano) == 0:
            print("Se terminaron las cartas")
            break


if __name__ == "__main__":
    main()