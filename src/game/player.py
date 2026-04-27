# Clase para representar a un jugador
class Player:

    # Inicialización del jugador con un nombre y una mano vacía
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []

    # Método para jugar una carta de la mano, removiéndola de la misma
    def jugar_carta(self, index):
        return self.mano.pop(index)

    # Representación del jugador para impresión
    def __repr__(self):
        return self.nombre