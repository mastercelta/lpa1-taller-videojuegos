import pygame

from mundo.juego import Juego
from ui import hud, sprites
from ui.animador import Animador
from ui.estados.base import Estado
from ui.sonido import Sonidos
from ui.vista import dibujar_juego

TECLAS_MOVIMIENTO = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}
INTERVALO_AUTOSAVE = 5.0  # segundos entre guardados automáticos
RETARDO_INICIAL = 0.22  # pausa tras el primer paso antes de caminar seguido
REPETICION = 0.13  # segundos entre pasos con la tecla sostenida


class EstadoJugando(Estado):


    def __init__(self, aplicacion, juego: Juego = None):
        super().__init__(aplicacion)
        hud.inicializar_fuentes()
        sprites.inicializar_fuentes()
        self._juego = juego or Juego()
        self._animador = Animador()
        self._espera = 0.0
        self._sonidos = Sonidos()
        self._reloj_guardado = 0.0
        self.aplicacion.guardado.guardar(self._juego)

    @property
    def juego(self) -> Juego:
        return self._juego

    @property
    def pista(self) -> str:
        if self._juego.resultado == "derrota":
            return "derrota"
        return "jefe" if self._juego.jefe_avistado else "mundo"

    def _reiniciar(self) -> None:
        self._juego = Juego()
        self._animador = Animador()
        self.guardar()

    def guardar(self) -> None:
        # Autosave: se guarda solo, el jugador nunca tiene que acordarse
        self.aplicacion.guardado.guardar(self._juego)
        self._reloj_guardado = 0.0

    def al_cerrar(self) -> None:
        self.guardar()

    def manejar_evento(self, evento) -> None:
        if evento.type != pygame.KEYDOWN:
            return
        if self._juego.terminado:
            if evento.key == pygame.K_r:
                self._reiniciar()
            elif evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                from ui.estados.menu import EstadoMenu
                self.aplicacion.cambiar_estado(EstadoMenu(self.aplicacion))
            return
        if evento.key == pygame.K_ESCAPE:
            from ui.estados.pausa import EstadoPausa
            self.guardar()
            self.aplicacion.cambiar_estado(EstadoPausa(self.aplicacion, self))
        elif evento.key == pygame.K_SPACE:
            self._juego.activar_trampa()
        elif evento.key == pygame.K_t and self._juego.en_tienda:
            from ui.estados.tienda import EstadoTienda
            self.aplicacion.cambiar_estado(EstadoTienda(self.aplicacion, self))
        elif evento.key in TECLAS_MOVIMIENTO:
            self._juego.mover(*TECLAS_MOVIMIENTO[evento.key])
            self._espera = RETARDO_INICIAL

    def _tecla_sostenida(self):
        presionadas = pygame.key.get_pressed()
        for tecla, direccion in TECLAS_MOVIMIENTO.items():
            if presionadas[tecla]:
                return direccion
        return None

    def actualizar(self, dt: float) -> None:
        # R10.1: con la flecha sostenida el personaje sigue caminando
        direccion = self._tecla_sostenida()
        if direccion is None:
            self._espera = 0.0
        else:
            self._espera -= dt
            if self._espera <= 0:
                self._juego.mover(*direccion)
                self._espera = REPETICION
        self._juego.actualizar(dt)
        self._animador.actualizar(dt, self._juego)
        self.reproducir_eventos()
        self.aplicacion.musica.reproducir(self.pista)
        self._reloj_guardado += dt
        if self._reloj_guardado >= INTERVALO_AUTOSAVE:
            self.guardar()

    def reproducir_eventos(self) -> None:
        eventos = self._juego.tomar_eventos()
        for evento in eventos:
            self._sonidos.reproducir(evento)  # R8.2
        if eventos:
            self.guardar()

    def dibujar(self, superficie) -> None:
        dibujar_juego(superficie, self._juego, self._animador)
