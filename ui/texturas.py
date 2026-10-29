import os
import random

import pygame

from ui.renderizador import TAMAÑO_CELDA as C

CARPETA_ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
VARIANTES_PISO = 4

# Si existe un PNG con este nombre en assets/ (por ejemplo, hecho en Recraft) se usa ese;
# si no, se genera la textura por código. Así el juego siempre funciona.
ARCHIVOS = {
    "piso": "piso_{}.png",
    "zona_venta": "zona_venta.png",
    "obstaculo": "obstaculo.png",
}


def ruta_asset(nombre: str) -> str:
    return os.path.join(CARPETA_ASSETS, nombre)


def cargar_png(nombre: str, tamaño: tuple = None):
    ruta = ruta_asset(nombre)
    if not os.path.exists(ruta):
        return None
    imagen = pygame.image.load(ruta)
    if pygame.display.get_surface() is not None:
        imagen = imagen.convert_alpha()
    if tamaño and imagen.get_size() != tamaño:
        imagen = pygame.transform.smoothscale(imagen, tamaño)
    return imagen


class Texturas:
    # Guarda en caché cada textura la primera vez que se pide

    def __init__(self):
        self._cache = {}

    def _obtener(self, clave: str, crear):
        if clave not in self._cache:
            self._cache[clave] = crear()
        return self._cache[clave]

    def piso(self, x: int, y: int):
        variante = (x * 7 + y * 13 + x * y) % VARIANTES_PISO
        return self._obtener(f"piso_{variante}", lambda: cargar_png(ARCHIVOS["piso"].format(variante), (C, C))
                             or _piso_circuito(variante))

    def zona_venta(self):
        return self._obtener("zona_venta", lambda: cargar_png(ARCHIVOS["zona_venta"], (C, C)) or _alfombra_tienda())

    def obstaculo(self):
        return self._obtener("obstaculo", lambda: cargar_png(ARCHIVOS["obstaculo"], (C, C)))

    def luz(self):
        return self._obtener("luz", crear_luz)

    def sprite(self, nombre: str):
        # sprites/<Clase>.png, por ejemplo sprites/EnemigoNullPointer.png o sprites/estudiante_abajo.png
        return self._obtener(f"sprite_{nombre}", lambda: cargar_png(os.path.join("sprites", f"{nombre}.png"), (C, C)))


def _piso_circuito(variante: int):
    # baldosa oscura con pistas de circuito impreso: el "suelo" del mundo del código
    azar = random.Random(variante * 97 + 11)
    tile = pygame.Surface((C, C))
    tile.fill((26, 29, 38))
    for _ in range(40):
        tono = azar.randint(22, 34)
        tile.set_at((azar.randrange(C), azar.randrange(C)), (tono, tono + 3, tono + 10))
    pista = (31, 44, 52)
    brillo = (48, 78, 86)
    for _ in range(1 + variante % 2):
        x, y = azar.randrange(6, C - 6), azar.randrange(6, C - 6)
        largo = azar.randrange(10, 24)
        if azar.random() < 0.5:
            fin = (min(C - 3, x + largo), y)
            codo = (fin[0], min(C - 3, y + azar.randrange(6, 14)))
        else:
            fin = (x, min(C - 3, y + largo))
            codo = (min(C - 3, x + azar.randrange(6, 14)), fin[1])
        pygame.draw.line(tile, pista, (x, y), fin, 2)
        pygame.draw.line(tile, pista, fin, codo, 2)
        pygame.draw.circle(tile, brillo, (x, y), 2)
        pygame.draw.circle(tile, brillo, codo, 2)
    pygame.draw.rect(tile, (33, 37, 48), (0, 0, C, C), 1)
    pygame.draw.line(tile, (20, 22, 30), (0, C - 1), (C, C - 1))
    return tile


def _alfombra_tienda():
    tile = pygame.Surface((C, C))
    tile.fill((38, 74, 52))
    pygame.draw.rect(tile, (230, 140, 50), (3, 3, C - 6, C - 6), 2, border_radius=4)
    for i in range(3):
        pygame.draw.line(tile, (210, 120, 40), (12, 16 + i * 8), (C - 12, 16 + i * 8), 3)
    pygame.draw.rect(tile, (28, 56, 40), (0, 0, C, C), 1)
    return tile


def crear_luz(radio: int = 240, oscuridad: int = 150):
    # sombra alrededor del jugador: transparente en el centro y oscura hacia los bordes
    pequeña = pygame.Surface((64, 64), pygame.SRCALPHA)
    for x in range(64):
        for y in range(64):
            d = min(1.0, ((x - 31.5) ** 2 + (y - 31.5) ** 2) ** 0.5 / 32)
            pequeña.set_at((x, y), (5, 6, 12, int(oscuridad * d ** 1.6)))
    return pygame.transform.smoothscale(pequeña, (radio * 2, radio * 2))
