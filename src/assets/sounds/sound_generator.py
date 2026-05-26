import wave
import struct
import math
import os

def generar_tono(filename, frecuencia, duracion, volumen=0.3, fade=True):
    sample_rate = 44100
    n_samples = int(sample_rate * duracion)
    
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        
        for i in range(n_samples):
            t = i / sample_rate
            sample = math.sin(2 * math.pi * frecuencia * t)
            
            # fade out
            if fade and i > n_samples * 0.7:
                sample *= 1 - (i - n_samples * 0.7) / (n_samples * 0.3)
            
            sample = int(sample * volumen * 32767)
            f.writeframes(struct.pack('<h', sample))

def generar_todos():
    base = os.path.dirname(__file__)
    
    # golpe normal — tono medio corto
    generar_tono(os.path.join(base, "golpe.wav"), frecuencia=440, duracion=0.15)
    
    # especial — tono más agudo y largo
    generar_tono(os.path.join(base, "especial.wav"), frecuencia=660, duracion=0.25)
    
    # punto — dos tonos ascendentes
    generar_tono(os.path.join(base, "punto.wav"), frecuencia=523, duracion=0.15)
    generar_tono(os.path.join(base, "punto2.wav"), frecuencia=659, duracion=0.2)
    
    # error — tono grave
    generar_tono(os.path.join(base, "error.wav"), frecuencia=200, duracion=0.2)

if __name__ == "__main__":
    generar_todos()
    print("Sonidos generados OK")