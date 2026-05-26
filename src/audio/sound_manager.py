import winsound
import threading
import time


class SoundManager:

    def _beep(self, frecuencia, duracion):
        threading.Thread(
            target=winsound.Beep,
            args=(frecuencia, duracion),
            daemon=True
        ).start()

    def play(self, nombre):
        sonidos = {
            "golpe":    (440, 100),
            "especial": (660, 200),
            "error":    (200, 200),
        }
        if nombre in sonidos:
            freq, dur = sonidos[nombre]
            self._beep(freq, dur)

    def play_punto(self):
        def secuencia():
            winsound.Beep(523, 150)
            time.sleep(0.05)
            winsound.Beep(659, 250)
        threading.Thread(target=secuencia, daemon=True).start()