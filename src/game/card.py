from game.enums import TipoGolpe

# Clase para representar una carta de golpe
class Card:
    def __init__(self, nombre, tipo, efecto_base):
        self.nombre = nombre
        self.tipo = tipo
        self.efecto_base = efecto_base  # -1, 0, +1
    
    # Representación de la carta para impresión
    def __repr__(self):
        return f"{self.nombre} ({self.tipo.value})"