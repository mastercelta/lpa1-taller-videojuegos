import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from mundo.juego import Juego
from mundo.guardado import Guardado
from tests.test_guardado import AlmacenMemoria
from ui.aplicacion import Aplicacion
from ui.estados.base import Estado
from ui.estados.como_jugar import EstadoComoJugar
from ui.estados.jugando import EstadoJugando
from ui.estados.menu import EstadoMenu
from ui.estados.pausa import EstadoPausa
from ui.estados.tienda import EstadoTienda
from ui.vista import tamaño_ventana


@pytest.fixture
def app():
    pygame.init()
    aplicacion = Aplicacion(tamaño_ventana(Juego()), "test", Guardado(AlmacenMemoria()))
    aplicacion._ejecutando = True
    aplicacion.cambiar_estado(EstadoMenu(aplicacion))
    yield aplicacion
    pygame.quit()


def tecla(aplicacion, key):
    superficie = pygame.Surface(aplicacion.tamaño)
    aplicacion.procesar([pygame.event.Event(pygame.KEYDOWN, key=key)], 0.016, superficie)


def test_estado_es_abstracto():
    with pytest.raises(TypeError):
        Estado(None)


def test_todas_las_pantallas_son_estados(app):
    jugando = EstadoJugando(app)
    for estado in (EstadoMenu(app), EstadoComoJugar(app), jugando, EstadoPausa(app, jugando), EstadoTienda(app, jugando)):
        assert isinstance(estado, Estado)


def test_el_menu_navega_en_circulo(app):
    tecla(app, pygame.K_UP)
    assert app.estado.seleccion == len(EstadoMenu.OPCIONES) - 1
    tecla(app, pygame.K_DOWN)
    assert app.estado.seleccion == 0


def test_nueva_partida_entra_a_jugar(app):
    tecla(app, pygame.K_RETURN)
    assert isinstance(app.estado, EstadoJugando)


def test_como_jugar_y_volver(app):
    tecla(app, pygame.K_DOWN)
    tecla(app, pygame.K_RETURN)
    assert isinstance(app.estado, EstadoComoJugar)
    tecla(app, pygame.K_ESCAPE)
    assert isinstance(app.estado, EstadoMenu)


def test_salir_desde_el_menu(app):
    tecla(app, pygame.K_UP)
    tecla(app, pygame.K_RETURN)
    assert not app.ejecutando


def test_pausa_conserva_la_partida(app):
    tecla(app, pygame.K_RETURN)
    jugando = app.estado
    jugando.juego.mover(1, 0)
    posicion = jugando.juego.personaje.posicion
    tecla(app, pygame.K_ESCAPE)
    assert isinstance(app.estado, EstadoPausa)
    tecla(app, pygame.K_RETURN)
    assert app.estado is jugando
    assert jugando.juego.personaje.posicion == posicion


def test_desde_la_pausa_se_vuelve_al_menu(app):
    tecla(app, pygame.K_RETURN)
    tecla(app, pygame.K_ESCAPE)
    tecla(app, pygame.K_DOWN)
    tecla(app, pygame.K_RETURN)
    assert isinstance(app.estado, EstadoMenu)


def test_al_terminar_la_partida_enter_vuelve_al_menu(app):
    tecla(app, pygame.K_RETURN)
    app.estado.juego._resultado = "derrota"
    tecla(app, pygame.K_RETURN)
    assert isinstance(app.estado, EstadoMenu)


def test_la_tienda_compra_equipa_y_vuelve_a_la_partida(app):
    tecla(app, pygame.K_RETURN)
    jugando = app.estado
    juego = jugando.juego
    juego.personaje.mover(*juego.escenario.zona_venta)
    juego.personaje.ganar_puntos_commit(60)
    app.cambiar_estado(EstadoTienda(app, jugando))
    tecla(app, pygame.K_RETURN)
    assert juego.personaje.puntos_commit == 10
    tecla(app, pygame.K_RIGHT)
    ataque = juego.personaje.ataque
    tecla(app, pygame.K_RETURN)
    assert juego.personaje.ataque > ataque
    tecla(app, pygame.K_ESCAPE)
    assert app.estado is jugando


def test_la_t_abre_la_tienda_solo_en_la_zona_de_venta(app):
    tecla(app, pygame.K_RETURN)
    jugando = app.estado
    tecla(app, pygame.K_t)
    assert app.estado is jugando
    jugando.juego.personaje.mover(*jugando.juego.escenario.zona_venta)
    tecla(app, pygame.K_t)
    assert isinstance(app.estado, EstadoTienda)


def test_espacio_activa_la_trampa(app):
    from models.trampa_explosiva import TrampaExplosiva
    tecla(app, pygame.K_RETURN)
    juego = app.estado.juego
    juego.personaje.recolectar(TrampaExplosiva("SyntaxError", alcance_explosion=1, daño_explosion=12))
    tecla(app, pygame.K_SPACE)
    assert juego.trampas_en_inventario() == []


def test_hay_un_sonido_por_cada_evento():
    from ui.sonido import MELODIAS, Sonidos
    sonidos = Sonidos()
    for nombre in ("golpe", "daño", "esquivar", "derrotar", "recoger", "comprar", "error", "explosion", "victoria", "derrota"):
        assert nombre in MELODIAS
        sonidos.reproducir(nombre)


def test_autosave_y_continuar_desde_el_menu(app):
    assert app.estado.opciones[0] == "Nueva partida"
    tecla(app, pygame.K_RETURN)
    jugando = app.estado
    jugando.juego.mover(0, 1)
    jugando.juego.personaje.ganar_puntos_commit(33)
    tecla(app, pygame.K_ESCAPE)
    tecla(app, pygame.K_DOWN)
    tecla(app, pygame.K_RETURN)
    menu = app.estado
    assert menu.opciones[0] == "Continuar"
    tecla(app, pygame.K_RETURN)
    assert app.estado.juego.personaje.puntos_commit == 33


def test_cerrar_la_ventana_guarda_la_partida(app):
    tecla(app, pygame.K_RETURN)
    app.estado.juego.personaje.ganar_puntos_commit(12)
    superficie = pygame.Surface(app.tamaño)
    app.procesar([pygame.event.Event(pygame.QUIT)], 0.016, superficie)
    assert app.guardado.cargar().personaje.puntos_commit == 12
