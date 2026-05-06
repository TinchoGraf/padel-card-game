import tkinter as tk
from game.game import Game


class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Padel Card Game")
        self.root.geometry("900x500")

        self.game = Game()

        # ------------------------
        # UI SUPERIOR
        # ------------------------

        self.label_pelota = tk.Label(self.root, font=("Arial", 14))
        self.label_pelota.pack(pady=5)

        # círculo pelota
        self.canvas = tk.Canvas(self.root, width=50, height=50, highlightthickness=0)
        self.canvas.pack()

        # barra fuerza
        self.barra = tk.Canvas(self.root, width=200, height=20, bg="lightgray", highlightthickness=0)
        self.barra.pack(pady=5)

        # marcador
        self.label_score = tk.Label(self.root, font=("Arial", 12, "bold"))
        self.label_score.pack()

        # turno
        self.label_turno = tk.Label(self.root, font=("Arial", 11))
        self.label_turno.pack(pady=5)

        # mensajes
        self.label_mensaje = tk.Label(self.root, font=("Arial", 11), fg="red")
        self.label_mensaje.pack(pady=5)

        # ------------------------
        # CARTAS
        # ------------------------

        self.frame_cartas = tk.Frame(self.root)
        self.frame_cartas.pack(pady=20)

        self.actualizar_ui()

    # ------------------------
    # COLORES
    # ------------------------

    def color_por_tipo(self, tipo):
        if tipo == "DEFENSIVO":
            return "#4CAF50"
        elif tipo == "TRANSICION":
            return "#FFC107"
        elif tipo == "ATAQUE":
            return "#F44336"
        return "white"

    def color_pelota(self):
        estado = self.game.ball.estado.name

        if estado == "VERDE":
            return "green"
        elif estado == "AMARILLO":
            return "gold"
        elif estado == "ROJO":
            return "red"
        return "black"

    # ------------------------
    # ACTUALIZAR UI
    # ------------------------

    def actualizar_ui(self):
        estado = self.game.ball.estado.name
        fuerza = getattr(self.game.ball, "fuerza", 1)

        self.label_pelota.config(text=f"Pelota: {estado} (Fuerza {fuerza})")

        # dibujar pelota
        self.canvas.delete("all")
        self.canvas.create_oval(5, 5, 45, 45, fill=self.color_pelota())

        # barra fuerza
        self.barra.delete("all")
        self.barra.create_rectangle(0, 0, fuerza * 50, 20, fill="orange")

        # marcador
        p1 = self.game.puntos[self.game.jugador1]
        p2 = self.game.puntos[self.game.jugador2]

        self.label_score.config(
            text=f"{self.game.jugador1.nombre} {p1} - {p2} {self.game.jugador2.nombre}"
        )

        # turno
        self.label_turno.config(text=f"Turno: {self.game.turno.nombre}")

        # render cartas
        self.render_cartas()

    # ------------------------
    # RENDER CARTAS
    # ------------------------

    def render_cartas(self):
        for widget in self.frame_cartas.winfo_children():
            widget.destroy()

        jugador = self.game.turno

        # ordenar
        normales = sorted(
            jugador.mano,
            key=lambda c: (
                0 if c.tipo.name == "DEFENSIVO" else
                1 if c.tipo.name == "TRANSICION" else
                2
            )
        )

        cartas = normales + jugador.especiales

        for i, carta in enumerate(cartas):
            tipo = carta.tipo.name
            nombre = carta.nombre
            efecto = carta.efecto_especial if carta.es_especial else carta.efecto_base

            color = self.color_por_tipo(tipo)

            outer = tk.Frame(self.frame_cartas, bg="white")
            outer.grid(row=0, column=i, padx=10, pady=10)

            carta_frame = tk.Frame(
                outer,
                width=110,
                height=160,
                bg="white",
                highlightbackground=color,
                highlightthickness=2
            )
            carta_frame.pack()
            carta_frame.pack_propagate(False)

            # estrella especial
            if carta.es_especial:
                tk.Label(
                    carta_frame,
                    text="★",
                    fg="gold",
                    bg="white",
                    font=("Arial", 12, "bold")
                ).place(relx=0.95, rely=0.05, anchor="ne")

            # nombre
            tk.Label(
                carta_frame,
                text=nombre.upper(),
                font=("Arial", 9, "bold"),
                bg="white"
            ).pack(pady=(10, 5))

            # tipo
            tk.Label(
                carta_frame,
                text=tipo,
                font=("Arial", 8),
                fg="gray",
                bg="white"
            ).pack()

            # efecto
            tk.Label(
                carta_frame,
                text=f"{efecto:+}",
                font=("Arial", 14, "bold"),
                bg="white"
            ).pack(side="bottom", pady=10)

            # ------------------------
            # HOVER
            # ------------------------

            def on_enter(e, parent=outer, frame=carta_frame):
                parent.grid_configure(pady=2)
                frame.config(highlightthickness=4)

            def on_leave(e, parent=outer, frame=carta_frame):
                parent.grid_configure(pady=10)
                frame.config(highlightthickness=2)

            carta_frame.bind("<Enter>", on_enter)
            carta_frame.bind("<Leave>", on_leave)

            # ------------------------
            # CLICK
            # ------------------------

            if i < len(normales):
                carta_frame.bind(
                    "<Button-1>",
                    lambda e, idx=i: self.jugar_carta(idx, False)
                )
            else:
                carta_frame.bind(
                    "<Button-1>",
                    lambda e, idx=i - len(normales): self.jugar_carta(idx, True)
                )

    # ------------------------
    # JUGAR CARTA
    # ------------------------

    def jugar_carta(self, idx, es_especial):
        jugador = self.game.turno

        try:
            if es_especial:
                carta = jugador.especiales[idx]
                jugador.especiales.pop(idx)
            else:
                carta = jugador.mano[idx]
                jugador.mano.pop(idx)
        except IndexError:
            return

        # validar
        if not self.game.carta_valida(carta):
            self.label_mensaje.config(text="No podés jugar esa carta")
            return

        self.label_mensaje.config(text="")

        hubo_punto = self.game.aplicar_carta(carta)

        if not hubo_punto:
            self.game.cambiar_turno()

        self.actualizar_ui()

    # ------------------------
    # RUN
    # ------------------------

    def run(self):
        self.root.mainloop()