import tkinter as tk
from ui.player_select_window import PlayerSelectWindow


class GameUI:

    # ── INIT ────────────────────────────────────────────────────────

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Padel Card Game")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)
        self.game = None

        PlayerSelectWindow(self.root, self._iniciar_juego)

    def _iniciar_juego(self, seleccion_j1, seleccion_j2):
        from game.game import Game
        self.game = Game()
        self.game.iniciar_con_seleccion(seleccion_j1, seleccion_j2)
        self._build_ui()
        self.actualizar_ui()

    # ── BUILD UI ────────────────────────────────────────────────────

    def _build_ui(self):
        # canvas de fondo (cancha)
        self.bg_canvas = tk.Canvas(
            self.root, width=1100, height=700,
            highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0)
        self._dibujar_cancha()

        # ── ZONA RIVAL (arriba) ──────────────────────────────────────
        self.frame_rival = tk.Frame(self.bg_canvas, bg="#1e1e2e")
        self.frame_rival.place(x=0, y=10, width=1100, height=170)

        # ── ZONA CENTRAL (info + semáforo) ───────────────────────────
        self.frame_centro = tk.Frame(self.bg_canvas, bg="#1e1e2e")
        self.frame_centro.place(x=0, y=190, width=1100, height=130)

        self.label_turno = tk.Label(
            self.frame_centro,
            font=("Arial", 12, "bold"),
            bg="#1e1e2e", fg="white"
        )
        self.label_turno.pack(pady=(5, 0))

        # semáforo pelota
        frame_semaforo = tk.Frame(self.frame_centro, bg="#1e1e2e")
        frame_semaforo.pack(pady=5)

        self.label_pelota = tk.Label(
            frame_semaforo,
            font=("Arial", 11),
            bg="#1e1e2e", fg="white"
        )
        self.label_pelota.pack(side="left", padx=(0, 10))

        self.canvas_pelota = tk.Canvas(
            frame_semaforo, width=40, height=40,
            bg="#1e1e2e", highlightthickness=0
        )
        self.canvas_pelota.pack(side="left")

        # marcador
        self.label_score = tk.Label(
            self.frame_centro,
            font=("Arial", 13, "bold"),
            bg="#1e1e2e", fg="white"
        )
        self.label_score.pack()

        # mensaje error
        self.label_mensaje = tk.Label(
            self.frame_centro,
            font=("Arial", 10),
            bg="#1e1e2e", fg="#ffcc00"
        )
        self.label_mensaje.pack()

        # ── ZONA JUGADOR ACTIVO (abajo) ──────────────────────────────
        self.frame_cartas = tk.Frame(self.bg_canvas, bg="#1e1e2e")
        self.frame_cartas.place(x=0, y=330, width=1100, height=360)

    # ── CANCHA ──────────────────────────────────────────────────────

    def _dibujar_cancha(self):
        c = self.bg_canvas
        W, H = 1100, 700

        # fondo oscuro neutro, no distrae
        c.create_rectangle(0, 0, W, H, fill="#1e1e2e", outline="")

        # línea de red sutil en el centro
        mid_y = H // 2
        c.create_line(80, mid_y, W - 80, mid_y, fill="#3a3a5c", width=2)

        # borde de cancha muy suave
        c.create_rectangle(80, 40, W - 80, H - 40,
                           outline="#2e2e4e", width=1)

    # ── COLORES ─────────────────────────────────────────────────────

    def color_por_tipo(self, tipo):
        return {
            "DEFENSIVO": "#4CAF50",
            "TRANSICION": "#FFC107",
            "ATAQUE": "#F44336",
        }.get(tipo, "white")

    def color_pelota(self):
        estado = self.game.ball.estado.name
        return {
            "VERDE": "#00cc44",
            "AMARILLO": "gold",
            "ROJO": "#cc2200",
            "ROJO_PLUS": "#880000",
        }.get(estado, "white")

    # ── ACTUALIZAR UI ───────────────────────────────────────────────

    def actualizar_ui(self):
        estado = self.game.ball.estado.name
        fuerza = getattr(self.game.ball, "fuerza", 1)

        self.label_pelota.config(text=f"Pelota: {estado}  (fuerza {fuerza})")

        self.canvas_pelota.delete("all")
        self.canvas_pelota.create_oval(
            4, 4, 36, 36, fill=self.color_pelota(), outline=""
        )

        p1 = self.game.puntos[self.game.jugador1]
        p2 = self.game.puntos[self.game.jugador2]
        self.label_score.config(
            text=f"{self.game.jugador1.nombre}  {p1} — {p2}  {self.game.jugador2.nombre}"
        )

        self.label_turno.config(
            text=f"Turno de: {self.game.turno.nombre}"
        )

        # ── NUEVO: chequear si el jugador activo tiene jugadas posibles ──
        if not self.game.obtener_cartas_validas():
            rival = (
                self.game.jugador2
                if self.game.turno == self.game.jugador1
                else self.game.jugador1
            )
            self.game.sumar_punto(rival)
            if not self.game.juego_terminado:
                self.game.reiniciar_rally()
            self.label_mensaje.config(
                text=f"Sin jugadas — punto para {rival.nombre}"
            )

        self.render_cartas()

    # ── RENDER CARTAS ───────────────────────────────────────────────

    def render_cartas(self):
        for w in self.frame_rival.winfo_children():
            w.destroy()
        for w in self.frame_cartas.winfo_children():
            w.destroy()

        jugador_activo = self.game.turno
        jugador_rival = (
            self.game.jugador2
            if jugador_activo == self.game.jugador1
            else self.game.jugador1
        )

        # cartas del rival (dorso, arriba)
        self._render_dorsos(jugador_rival)

        # cartas del jugador activo (frente, abajo)
        normales = sorted(
            jugador_activo.mano,
            key=lambda c: (
                0 if c.tipo.name == "DEFENSIVO" else
                1 if c.tipo.name == "TRANSICION" else 2
            )
        )
        cartas = normales + jugador_activo.especiales

        frame_inner = tk.Frame(self.frame_cartas, bg="#1e1e2e")
        frame_inner.pack(expand=True)

        for i, carta in enumerate(cartas):
            es_especial = carta.es_especial
            idx = i - len(normales) if es_especial else i
            self._render_carta_frente(
                frame_inner, carta, i, idx, es_especial, len(normales)
            )

    def _render_dorsos(self, jugador_rival):
        total = len(jugador_rival.mano) + len(jugador_rival.especiales)

        frame_inner = tk.Frame(self.frame_rival, bg="#1e1e2e")
        frame_inner.pack(expand=True)

        for i in range(total):
            es_especial_slot = i >= len(jugador_rival.mano)

            outer = tk.Frame(frame_inner, bg="#1e1e2e")
            outer.grid(row=0, column=i, padx=6)

            dorso = tk.Frame(
                outer,
                width=90, height=130,
                bg="#1a3a5c",
                highlightbackground="#aaaaaa",
                highlightthickness=2
            )
            dorso.pack()
            dorso.pack_propagate(False)

            # estrella si es especial
            if es_especial_slot:
                tk.Label(
                    dorso, text="★",
                    fg="gold", bg="#1a3a5c",
                    font=("Arial", 10, "bold")
                ).place(relx=0.95, rely=0.05, anchor="ne")

            tk.Label(
                dorso,
                text="PADEL\nCARD\nGAME",
                font=("Arial", 9, "bold"),
                fg="#aaaacc",
                bg="#1a3a5c",
                justify="center"
            ).place(relx=0.5, rely=0.5, anchor="center")

    def _render_carta_frente(self, parent, carta, col, idx, es_especial, n_normales):
        tipo = carta.tipo.name
        nombre = carta.nombre
        efecto = carta.efecto_especial if es_especial else carta.efecto_base
        color = self.color_por_tipo(tipo)

        valida = self.game.carta_valida(carta)

        outer = tk.Frame(parent, bg="#1e1e2e")
        outer.grid(row=0, column=col, padx=6, pady=10)

        carta_frame = tk.Frame(
            outer,
            width=100, height=150,
            bg="white" if valida else "#cccccc",
            highlightbackground=color if valida else "#999999",
            highlightthickness=2
        )
        carta_frame.pack()
        carta_frame.pack_propagate(False)

        # estrella especial
        if es_especial:
            tk.Label(
                carta_frame, text="★",
                fg="gold",
                bg="white" if valida else "#cccccc",
                font=("Arial", 11, "bold")
            ).place(relx=0.95, rely=0.05, anchor="ne")

        # nombre
        tk.Label(
            carta_frame,
            text=nombre.upper(),
            font=("Arial", 8, "bold"),
            bg="white" if valida else "#cccccc",
            wraplength=85,
            justify="center"
        ).pack(pady=(12, 3))

        # tipo
        tk.Label(
            carta_frame,
            text=tipo,
            font=("Arial", 7),
            fg="gray",
            bg="white" if valida else "#cccccc"
        ).pack()

        # efecto
        tk.Label(
            carta_frame,
            text=f"{efecto:+}",
            font=("Arial", 13, "bold"),
            bg="white" if valida else "#cccccc",
            fg=color
        ).pack(side="bottom", pady=8)

        # hover y click solo si es válida
        if valida:
            def on_enter(e, f=carta_frame, c=color):
                f.config(highlightthickness=4)

            def on_leave(e, f=carta_frame):
                f.config(highlightthickness=2)

            carta_frame.bind("<Enter>", on_enter)
            carta_frame.bind("<Leave>", on_leave)

            carta_frame.bind(
                "<Button-1>",
                lambda e, i=idx, esp=es_especial: self.jugar_carta(i, esp)
            )

    # ── JUGAR CARTA ─────────────────────────────────────────────────

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

        self.label_mensaje.config(text="")

        hubo_punto = self.game.aplicar_carta(carta)

        if not hubo_punto:
            self.game.cambiar_turno()

        self.actualizar_ui()

    # ── RUN ─────────────────────────────────────────────────────────

    def run(self):
        self.root.mainloop()