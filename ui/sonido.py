import math
from array import array

import pygame

FRECUENCIA_MUESTREO = 22050

# R8.2: cada evento del juego tiene un sonido corto generado por código (sin archivos de audio)
# nombre -> lista de (frecuencia en Hz, duración en segundos); frecuencia 0 es ruido
MELODIAS = {
    "golpe": [(220, 0.06), (160, 0.06)],
    "daño": [(140, 0.12)],
    "esquivar": [(660, 0.04), (880, 0.05)],
    "derrotar": [(523, 0.07), (659, 0.07), (784, 0.1)],
    "recoger": [(880, 0.05), (1175, 0.08)],
    "comprar": [(784, 0.06), (1047, 0.1)],
    "error": [(200, 0.08), (150, 0.1)],
    "explosion": [(0, 0.3)],
    "victoria": [(523, 0.12), (659, 0.12), (784, 0.12), (1047, 0.3)],
    "derrota": [(392, 0.18), (330, 0.18), (262, 0.4)],
}


def _onda(frecuencia: float, duracion: float, volumen: float = 0.35) -> array:
    total = int(FRECUENCIA_MUESTREO * duracion)
    muestras = array("h")
    semilla = 12345
    for i in range(total):
        desvanecer = 1 - i / total
        if frecuencia == 0:
            semilla = (semilla * 1103515245 + 12345) & 0x7FFFFFFF
            valor = (semilla / 0x7FFFFFFF) * 2 - 1
        else:
            valor = 1.0 if math.sin(2 * math.pi * frecuencia * i / FRECUENCIA_MUESTREO) >= 0 else -1.0
        muestras.append(int(valor * volumen * desvanecer * 32767))
    return muestras


class Sonidos:

    def __init__(self):
        self._sonidos = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=FRECUENCIA_MUESTREO, size=-16, channels=1)
            canales = pygame.mixer.get_init()[2]
            for nombre, notas in MELODIAS.items():
                muestras = array("h")
                for frecuencia, duracion in notas:
                    muestras.extend(_onda(frecuencia, duracion))
                if canales == 2:
                    estereo = array("h")
                    for m in muestras:
                        estereo.extend((m, m))
                    muestras = estereo
                self._sonidos[nombre] = pygame.mixer.Sound(buffer=muestras.tobytes())
        except pygame.error:
            self._sonidos = {}  # sin tarjeta de sonido el juego sigue funcionando en silencio

    @property
    def disponibles(self) -> bool:
        return bool(self._sonidos)

    def reproducir(self, nombre: str) -> None:
        sonido = self._sonidos.get(nombre)
        if sonido is not None:
            sonido.play()
