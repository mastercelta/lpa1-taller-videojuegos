import os
import wave

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from ui import musica


def test_sin_archivos_suena_la_melodia_de_respaldo(tmp_path, monkeypatch):
    monkeypatch.setattr(musica, "ruta_asset", lambda nombre: str(tmp_path / nombre))
    pygame.init()
    m = musica.Musica()
    m.reproducir("titulo")
    assert m.actual == "titulo"
    assert len(musica.melodia_respaldo()) > 0
    m.detener()
    pygame.quit()


def test_si_existe_la_pista_se_carga_del_archivo(tmp_path, monkeypatch):
    (tmp_path / "musica").mkdir()
    with wave.open(str(tmp_path / "musica" / "pista.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(22050)
        w.writeframes(b"\x00\x00" * 2205)
    monkeypatch.setattr(musica, "ruta_asset", lambda nombre: str(tmp_path / nombre))
    monkeypatch.setitem(musica.PISTAS, "mundo", "pista.wav")
    pygame.init()
    m = musica.Musica()
    m.reproducir("mundo")
    assert m.actual == "mundo"
    m.reproducir("mundo")  # la misma pista no se reinicia
    assert m.actual == "mundo"
    m.detener()
    pygame.quit()
