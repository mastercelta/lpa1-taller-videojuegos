import pygame

from mundo.juego import Juego
from ui import hud
from ui.estados.base import Estado
from ui.vista import dibujar_juego

TECLAS_MOVIMIENTO = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


class EstadoJugando(Estado):

    def __init__(self, aplicacion, juego: Juego = None):
        super().__init__(aplicacion)
        hud.inicializar_fuentes()
        self._juego = juego or Juego()

    @property
    def juego(self) -> Juego:
        return self._juego

    def manejar_evento(self, evento) -> None:
        if evento.type != pygame.KEYDOWN:
            return
        if self._juego.terminado:
            if evento.key == pygame.K_r:
                self._juego = Juego()
            elif evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                from ui.estados.menu import EstadoMenu
                self.aplicacion.cambiar_estado(EstadoMenu(self.aplicacion))
            return
        if evento.key == pygame.K_ESCAPE:
            from ui.estados.pausa import EstadoPausa
            self.aplicacion.cambiar_estado(EstadoPausa(self.aplicacion, self))
        elif evento.key in TECLAS_MOVIMIENTO:
            self._juego.mover(*TECLAS_MOVIMIENTO[evento.key])

    def dibujar(self, superficie) -> None:
        dibujar_juego(superficie, self._juego)
