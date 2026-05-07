import tkinter as tk
from data.players_data import JUGADORES


class PlayerSelectWindow:
    def __init__(self, root, on_confirm):
        self.root = root
        self.on_confirm = on_confirm

        drives = [j for j in JUGADORES.values() if j["posicion"] == "drive"]
        reves  = [j for j in JUGADORES.values() if j["posicion"] == "reves"]

        self.seleccion = {
            "j1": {"drive": tk.StringVar(), "reves": tk.StringVar()},
            "j2": {"drive": tk.StringVar(), "reves": tk.StringVar()},
        }

        frame = tk.Frame(root, padx=30, pady=20)
        frame.pack(fill="both", expand=True)
        self.frame = frame

        tk.Label(frame, text="🎾 Elegí tu pareja",
                 font=("Arial", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )

        for col, (jk, label) in enumerate([("j1", "Jugador 1"), ("j2", "Jugador 2")]):
            tk.Label(frame, text=label,
                     font=("Arial", 13, "bold")).grid(row=1, column=col, pady=(0, 10))

            tk.Label(frame, text="Drive:",
                     font=("Arial", 11, "underline")).grid(
                row=2, column=col, sticky="w", padx=20
            )
            for i, j in enumerate(drives):
                tk.Radiobutton(
                    frame,
                    text=f"{j['nombre']}   (+1 en {j['bonus_golpe']})",
                    variable=self.seleccion[jk]["drive"],
                    value=j["nombre"],
                    font=("Arial", 10),
                    command=self._check_completo
                ).grid(row=3 + i, column=col, sticky="w", padx=35)

            offset = 3 + len(drives) + 2

            tk.Label(frame, text="Revés:",
                     font=("Arial", 11, "underline")).grid(
                row=offset, column=col, sticky="w", padx=20, pady=(10, 0)
            )
            for i, j in enumerate(reves):
                tk.Radiobutton(
                    frame,
                    text=f"{j['nombre']}   (+1 en {j['bonus_golpe']})",
                    variable=self.seleccion[jk]["reves"],
                    value=j["nombre"],
                    font=("Arial", 10),
                    command=self._check_completo
                ).grid(row=offset + 1 + i, column=col, sticky="w", padx=35)

        self.btn = tk.Button(
            frame,
            text="▶  Comenzar",
            font=("Arial", 12, "bold"),
            bg="#4CAF50", fg="white",
            state="disabled",
            command=self._confirmar
        )
        self.btn.grid(row=20, column=0, columnspan=2, pady=25)

        self.label_error = tk.Label(frame, text="", fg="red", font=("Arial", 10))
        self.label_error.grid(row=21, column=0, columnspan=2)

    def _check_completo(self):
        completo = all(
            self.seleccion[jk][pos].get()
            for jk in ["j1", "j2"]
            for pos in ["drive", "reves"]
        )
        self.btn.config(state="normal" if completo else "disabled")

    def _confirmar(self):
        j1_d = self.seleccion["j1"]["drive"].get()
        j1_r = self.seleccion["j1"]["reves"].get()
        j2_d = self.seleccion["j2"]["drive"].get()
        j2_r = self.seleccion["j2"]["reves"].get()

        conflicto = set([j1_d, j1_r]) & set([j2_d, j2_r])
        if conflicto:
            self.label_error.config(
                text=f"⚠  {', '.join(conflicto)} no puede estar en las dos parejas"
            )
            return

        self.frame.destroy()
        self.on_confirm(
            {"drive": JUGADORES[j1_d], "reves": JUGADORES[j1_r]},
            {"drive": JUGADORES[j2_d], "reves": JUGADORES[j2_r]},
        )