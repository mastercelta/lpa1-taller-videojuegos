import asyncio

import pygame

from mundo.guardado import Guardado
from ui.musica import Musica


class Aplicacion:
    # Máquina de estados: guarda el estado actual y cambia entre pantallas (R9.2)

    def __init__(self, tamaño: tuple, titulo: str, guardado: Guardado = None):
        self._tamaño = tamaño
        self._guardado = guardado or Guardado()
        self._musica = Musica()
        self._titulo = titulo
        self._estado = None
        self._ejecutando = False

    @property
    def tamaño(self) -> tuple:
        return self._tamaño

    @property
    def guardado(self) -> Guardado:
        return self._guardado

    @property
    def musica(self) -> Musica:
        return self._musica

    @property
    def estado(self):
        return self._estado

    @property
    def ejecutando(self) -> bool:
        return self._ejecutando

    def cambiar_estado(self, nuevo_estado) -> None:
        self._estado = nuevo_estado
        if nuevo_estado.pista:
            self._musica.reproducir(nuevo_estado.pista)

    def salir(self) -> None:
        self._ejecutando = False

    def procesar(self, eventos: list, dt: float, superficie) -> None:
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self._estado.al_cerrar()
                self.salir()
                return
            self._estado.manejar_evento(evento)
        self._estado.actualizar(dt)
        self._estado.dibujar(superficie)

    async def ejecutar(self, crear_estado_inicial) -> None:
        # async para que la versión web (pygbag) le devuelva el control al navegador en cada cuadro
        pygame.init()
        ventana = pygame.display.set_mode(self._tamaño)
        pygame.display.set_caption(self._titulo)
        reloj = pygame.time.Clock()
        self.cambiar_estado(crear_estado_inicial(self))
        self._ejecutando = True
        while self._ejecutando:
            dt = reloj.tick(60) / 1000
            self.procesar(pygame.event.get(), dt, ventana)
            pygame.display.flip()
            await asyncio.sleep(0)
        pygame.quit()
