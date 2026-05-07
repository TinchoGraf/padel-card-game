class Player:
    def __init__(self, nombre, posicion="drive"):
        self.nombre = nombre
        self.posicion = posicion
        self.mano = []
        self.especiales = []
        self.bonus_golpes = []

    def jugar_carta(self, index):
        return self.mano.pop(index)

    def __repr__(self):
        return self.nombre