import os
from array import array

import pygame

from ui.sonido import FRECUENCIA_MUESTREO, _onda
from ui.texturas import ruta_asset

# Pistas de "15 Melodic RPG Chiptunes" de Aureolus_Omicron (CC0, OpenGameArt).
# Basta con descomprimir el zip de OGG en assets/musica/ con los nombres originales.
PISTAS = {
    "titulo": "rpgchip01_title_screen.ogg",
    "historia": "rpgchip02_bittersweet_story.ogg",
    "tienda": "rpgchip03_town.ogg",
    "mundo": "rpgchip08_castle_on_the_mountain.ogg",
    "jefe": "rpgchip12_the_evil_one.ogg",
    "derrota": "rpgchip15_game_over.ogg",
}
VOLUMEN = 0.5

# Melodía original de respaldo (cuando no hay OGG): frase heroica en Do mayor, (nota, tiempos)
NOTAS = {"C4": 262, "D4": 294, "E4": 330, "F4": 349, "G4": 392, "A4": 440, "B4": 494,
         "C5": 523, "D5": 587, "E5": 659, "G5": 784, "-": 0}
MELODIA_RESPALDO = [
    ("C5", 2), ("G4", 1), ("G4", 1), ("C5", 1), ("D5", 1), ("E5", 2),
    ("D5", 1), ("C5", 1), ("A4", 2), ("G4", 3), ("-", 1),
    ("A4", 2), ("F4", 1), ("A4", 1), ("C5", 1), ("D5", 1), ("E5", 2),
    ("G5", 2), ("E5", 1), ("D5", 1), ("C5", 3), ("-", 1),
]
TIEMPO = 0.16  # segundos por tiempo


def melodia_respaldo() -> array:
    muestras = array("h")
    for nota, tiempos in MELODIA_RESPALDO:
        frecuencia = NOTAS[nota]
        duracion = TIEMPO * tiempos
        if frecuencia == 0:
            muestras.extend([0] * int(FRECUENCIA_MUESTREO * duracion))
        else:
            muestras.extend(_onda(frecuencia, duracion, volumen=0.12))
    return muestras


class Musica:
    # Una sola pista sonando a la vez; cambiar a la misma pista no la reinicia

    def __init__(self):
        self._actual = None
        self._respaldo = None

    @property
    def actual(self) -> str:
        return self._actual

    def _mixer_listo(self) -> bool:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=FRECUENCIA_MUESTREO, size=-16, channels=1)
            return True
        except pygame.error:
            return False

    def reproducir(self, pista: str) -> None:
        if pista == self._actual:
            return
        self._actual = pista
        if not self._mixer_listo():
            return
        self._detener_respaldo()
        ruta = ruta_asset(os.path.join("musica", PISTAS.get(pista, "")))
        if os.path.isfile(ruta):
            try:
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.set_volume(VOLUMEN)
                pygame.mixer.music.play(loops=-1, fade_ms=600)
                return
            except pygame.error:
                pass
        pygame.mixer.music.stop()
        if pista == "titulo":
            self._tocar_respaldo()

    def _tocar_respaldo(self) -> None:
        try:
            if self._respaldo is None:
                muestras = melodia_respaldo()
                if pygame.mixer.get_init()[2] == 2:
                    estereo = array("h")
                    for m in muestras:
                        estereo.extend((m, m))
                    muestras = estereo
                self._respaldo = pygame.mixer.Sound(buffer=muestras.tobytes())
            self._respaldo.play(loops=-1)
        except pygame.error:
            self._respaldo = None

    def _detener_respaldo(self) -> None:
        if self._respaldo is not None:
            self._respaldo.stop()

    def detener(self) -> None:
        self._actual = None
        if self._mixer_listo():
            pygame.mixer.music.stop()
            self._detener_respaldo()
