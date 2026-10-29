import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from ui import texturas
from ui.renderizador import TAMAÑO_CELDA


def test_sin_assets_se_generan_por_codigo(tmp_path, monkeypatch):
    monkeypatch.setattr(texturas, "CARPETA_ASSETS", str(tmp_path))
    t = texturas.Texturas()
    assert t.piso(0, 0).get_size() == (TAMAÑO_CELDA, TAMAÑO_CELDA)
    assert t.zona_venta() is not None
    assert t.sprite("EnemigoNullPointer") is None


def test_un_png_en_assets_reemplaza_el_dibujo(tmp_path, monkeypatch):
    monkeypatch.setattr(texturas, "CARPETA_ASSETS", str(tmp_path))
    (tmp_path / "sprites").mkdir()
    imagen = pygame.Surface((100, 100))
    imagen.fill((255, 0, 0))
    pygame.image.save(imagen, str(tmp_path / "sprites" / "EnemigoNullPointer.png"))
    sprite = texturas.Texturas().sprite("EnemigoNullPointer")
    assert sprite.get_size() == (TAMAÑO_CELDA, TAMAÑO_CELDA)
    assert sprite.get_at((10, 10))[:3] == (255, 0, 0)
