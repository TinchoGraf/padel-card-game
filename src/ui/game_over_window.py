import tkinter as tk


class GameOverWindow:
    def __init__(self, root, ganador_nombre, puntos, on_rematch, on_quit):
        self.root = root
        self.on_rematch = on_rematch
        self.on_quit = on_quit

        # overlay oscuro encima de todo
        self.overlay = tk.Frame(root, bg="black")
        self.overlay.place(x=0, y=0, width=1100, height=700)
        self.overlay.configure(bg="#000000")

        # panel central
        panel = tk.Frame(
            self.overlay,
            bg="#1e1e2e",
            highlightbackground="#4CAF50",
            highlightthickness=3,
            padx=40,
            pady=40
        )
        panel.place(relx=0.5, rely=0.5, anchor="center")

        # trofeo
        tk.Label(
            panel,
            text="🏆",
            font=("Arial", 48),
            bg="#1e1e2e"
        ).pack(pady=(0, 10))

        # ganador
        tk.Label(
            panel,
            text="¡GANADOR!",
            font=("Arial", 14),
            fg="#aaaaaa",
            bg="#1e1e2e"
        ).pack()

        tk.Label(
            panel,
            text=ganador_nombre,
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#1e1e2e"
        ).pack(pady=(5, 15))

        # marcador final
        p1_nombre, p1_pts, p2_nombre, p2_pts = puntos
        tk.Label(
            panel,
            text=f"{p1_nombre}   {p1_pts} — {p2_pts}   {p2_nombre}",
            font=("Arial", 13),
            fg="#cccccc",
            bg="#1e1e2e"
        ).pack(pady=(0, 25))

        # botones
        frame_btns = tk.Frame(panel, bg="#1e1e2e")
        frame_btns.pack()

        tk.Button(
            frame_btns,
            text="▶  Jugar de nuevo",
            font=("Arial", 12, "bold"),
            bg="#4CAF50", fg="white",
            padx=20, pady=8,
            cursor="hand2",
            command=self._rematch
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            frame_btns,
            text="✕  Salir",
            font=("Arial", 12),
            bg="#c0392b", fg="white",
            padx=20, pady=8,
            cursor="hand2",
            command=self._quit
        ).grid(row=0, column=1, padx=10)

    def _rematch(self):
        self.overlay.destroy()
        self.on_rematch()

    def _quit(self):
        self.root.destroy()