import tkinter as tk
from game.game import Game

def color_por_tipo(tipo, es_especial=False, es_valida=True):
    if not es_valida:
        return "#BDBDBD"

    if es_especial:
        return "#9C27B0"

    if tipo == "DEFENSIVO":
        return "#4CAF50"
    elif tipo == "TRANSICION":
        return "#FFC107"
    elif tipo == "ATAQUE":
        return "#F44336"

    return "white"


class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Padel Card Game")
        self.root.geometry("900x550")

        self.game = Game()

        self.label_mensaje = tk.Label(self.root, text="", font=("Arial", 12, "bold"), fg="blue")
        self.label_mensaje.pack(pady=5)

        self.label_info = tk.Label(self.root, text="", font=("Arial", 14))
        self.label_info.pack()

        self.canvas = tk.Canvas(self.root, width=100, height=100)
        self.canvas.pack(pady=10)

        self.label_turno = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_turno.pack(pady=5)

        self.frame_cartas = tk.Frame(self.root)
        self.frame_cartas.pack(pady=20)

        self.actualizar_ui()

    def dibujar_pelota(self):
        self.canvas.delete("all")

        estado = self.game.ball.estado.name

        color = {
            "AMARILLO": "yellow",
            "VERDE": "green",
            "ROJO": "red",
            "ROJO_PLUS": "darkred"
        }.get(estado, "gray")

        self.canvas.create_oval(20, 20, 80, 80, fill=color)

    def actualizar_ui(self):
        self.dibujar_pelota()

        p1 = self.game.puntos[self.game.jugador1]
        p2 = self.game.puntos[self.game.jugador2]

        self.label_info.config(
            text=f"Marcador: {p1} - {p2} | Pelota: {self.game.ball.estado.name}"
        )

        self.label_turno.config(
            text=f"Turno: {self.game.turno.nombre}"
        )

        self.render_cartas()

    def render_cartas(self):
        for widget in self.frame_cartas.winfo_children():
            widget.destroy()

        jugador = self.game.turno

        orden = {"DEFENSIVO": 0, "TRANSICION": 1, "ATAQUE": 2}

        cartas_ordenadas = sorted(
            list(enumerate(jugador.mano)),
            key=lambda x: orden[x[1].tipo.name]
        )

        # normales
        for col, (idx, carta) in enumerate(cartas_ordenadas):
            es_valida = self.game.carta_valida(carta)

            self.crear_carta(col, carta, idx, False, es_valida)

        # especiales
        offset = len(cartas_ordenadas) + 1

        for i, carta in enumerate(jugador.especiales):
            es_valida = self.game.carta_valida(carta)

            self.crear_carta(offset + i, carta, i, True, es_valida)

    def crear_carta(self, col, carta, idx, es_especial, es_valida):
        tipo = carta.tipo.name
        nombre = carta.nombre

        efecto = carta.efecto_especial if es_especial else carta.efecto_base

        color = color_por_tipo(tipo, es_especial, es_valida)

        outer = tk.Frame(self.frame_cartas, bg="black")
        outer.grid(row=0, column=col, padx=10, pady=5)

        carta_frame = tk.Frame(outer, width=100, height=150, bg=color)
        carta_frame.pack(padx=2, pady=2)
        carta_frame.pack_propagate(False)

        tk.Label(carta_frame, text=nombre.upper(), font=("Arial", 10, "bold"), bg=color).pack(pady=10)
        tk.Label(carta_frame, text=("ESPECIAL" if es_especial else tipo), bg=color).pack()
        tk.Label(carta_frame, text=f"{efecto:+}", font=("Arial", 14, "bold"), bg=color).pack(side="bottom", pady=10)

        if es_valida:
            if es_especial:
                carta_frame.bind("<Button-1>", lambda e, i=idx: self.jugar_especial(i))
            else:
                carta_frame.bind("<Button-1>", lambda e, i=idx: self.jugar_normal(i))

    def hay_jugada_valida(self):
        jugador = self.game.turno

        return any(self.game.carta_valida(c) for c in jugador.mano) or \
               any(self.game.carta_valida(c) for c in jugador.especiales)

    def jugar_normal(self, idx):
        jugador = self.game.turno

        if idx >= len(jugador.mano):
            return

        carta = jugador.mano.pop(idx)

        hubo_punto = self.game.aplicar_carta(carta)

        if hubo_punto:
            self.label_mensaje.config(text=f"PUNTO para {jugador.nombre}")
        else:
            self.game.cambiar_turno()

            if not self.hay_jugada_valida():
                self.label_mensaje.config(text="No podés responder → punto rival")

                rival = self.game.jugador2 if self.game.turno == self.game.jugador1 else self.game.jugador1
                self.game.sumar_punto(rival)
                self.game.reiniciar_rally()

        self.actualizar_ui()

    def jugar_especial(self, idx):
        jugador = self.game.turno

        if idx >= len(jugador.especiales):
            return

        carta = jugador.especiales.pop(idx)

        hubo_punto = self.game.aplicar_carta(carta)

        if hubo_punto:
            self.label_mensaje.config(text=f"PUNTO para {jugador.nombre}")
        else:
            self.game.cambiar_turno()

            if not self.hay_jugada_valida():
                self.label_mensaje.config(text="No podés responder → punto rival")

                rival = self.game.jugador2 if self.game.turno == self.game.jugador1 else self.game.jugador1
                self.game.sumar_punto(rival)
                self.game.reiniciar_rally()

        self.actualizar_ui()

    def run(self):
        self.root.mainloop()