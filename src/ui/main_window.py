import tkinter as tk


def color_por_tipo(tipo):
    if tipo == "DEFENSIVO":
        return "#4CAF50"  # verde
    elif tipo == "TRANSICION":
        return "#FFC107"  # amarillo
    elif tipo == "ATAQUE":
        return "#F44336"  # rojo
    return "white"

class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Padel Card Game")

        # Tamaño de la ventana
        self.root.geometry("600x400")

        # Label del estado de la pelota
        self.label_pelota = tk.Label(
            self.root,
            text="Pelota: AMARILLO",
            font=("Arial", 16)
        )
        self.label_pelota.pack(pady=20)

        # Label del turno
        self.label_turno = tk.Label(
            self.root,
            text="Turno: Jugador 1",
            font=("Arial", 14)
        )
        self.label_turno.pack(pady=10)

        # Frame para cartas (botones)
        self.frame_cartas = tk.Frame(self.root)
        self.frame_cartas.pack(pady=20)

        def color_por_tipo(tipo):
            if tipo == "DEFENSIVO":
                return "#4CAF50"
            elif tipo == "TRANSICION":
                return "#FFC107"
            elif tipo == "ATAQUE":
                return "#F44336"
            return "white"


        cartas_demo = [
            ("Globo", "DEFENSIVO", -1),
            ("Defensa", "DEFENSIVO", -1),
            ("Chiquita", "TRANSICION", 0),
            ("Bandeja", "TRANSICION", 0),
            ("Volea", "ATAQUE", +1),
]

        for i, (nombre_carta, tipo_carta, efecto) in enumerate(cartas_demo):
            color = color_por_tipo(tipo_carta)

            # contenedor externo (simula borde redondeado)
            outer = tk.Frame(
                self.frame_cartas,
                bg="black"
            )
            outer.grid(row=0, column=i, padx=12, pady=5)

            # carta interna
            carta_frame = tk.Frame(
                outer,
                width=100,
                height=150,
                bg=color
            )
            carta_frame.pack(padx=2, pady=2)
            carta_frame.pack_propagate(False)

            # nombre
            nombre = tk.Label(
                carta_frame,
                text=nombre_carta.upper(),
                font=("Arial", 10, "bold"),
                bg=color
            )
            nombre.pack(pady=10)

            # tipo
            tipo = tk.Label(
                carta_frame,
                text=tipo_carta,
                font=("Arial", 9),
                bg=color
            )
            tipo.pack()

            # efecto (🔥 nuevo)
            efecto_texto = f"{efecto:+}"  # muestra +1 / -1

            efecto_label = tk.Label(
                carta_frame,
                text=efecto_texto,
                font=("Arial", 14, "bold"),
                bg=color
            )
            efecto_label.pack(side="bottom", pady=10)

            # click
            def on_click(idx=i):
                print(f"Click en {nombre_carta}")

            carta_frame.bind("<Button-1>", lambda e, idx=i: on_click(idx))

        
        def on_click(idx=i):
            print(f"Click en {nombre_carta}")

            carta_frame.bind("<Button-1>", lambda e, idx=i: on_click(idx))

    def run(self):
        self.root.mainloop()