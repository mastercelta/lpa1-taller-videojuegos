import pygame

from ui.estados.base import Estado

COLOR_TITULO = (240, 210, 60)
COLOR_OPCION = (210, 215, 225)
COLOR_SELECCION = (120, 230, 150)


class EstadoPausa(Estado):
    # Se dibuja encima de la partida pausada, que se conserva tal cual

    OPCIONES = ("Continuar", "Volver al menú")

    def __init__(self, aplicacion, estado_jugando):
        super().__init__(aplicacion)
        self._estado_jugando = estado_jugando
        self._seleccion = 0
        self._fuente_titulo = pygame.font.SysFont("arial", 34, bold=True)
        self._fuente_opcion = pygame.font.SysFont("arial", 24)

    def manejar_evento(self, evento) -> None:
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key in (pygame.K_UP, pygame.K_DOWN):
            self._seleccion = 1 - self._seleccion
        elif evento.key == pygame.K_ESCAPE:
            self.aplicacion.cambiar_estado(self._estado_jugando)
        elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            if self.OPCIONES[self._seleccion] == "Continuar":
                self.aplicacion.cambiar_estado(self._estado_jugando)
            else:
                from ui.estados.menu import EstadoMenu
                self.aplicacion.cambiar_estado(EstadoMenu(self.aplicacion))

    def dibujar(self, superficie) -> None:
        self._estado_jugando.dibujar(superficie)
        ancho, alto = superficie.get_size()
        velo = pygame.Surface((ancho, alto))
        velo.set_alpha(180)
        velo.fill((10, 10, 15))
        superficie.blit(velo, (0, 0))

        titulo = self._fuente_titulo.render("PAUSA", True, COLOR_TITULO)
        superficie.blit(titulo, titulo.get_rect(center=(ancho // 2, alto // 2 - 60)))
        for i, opcion in enumerate(self.OPCIONES):
            elegida = i == self._seleccion
            color = COLOR_SELECCION if elegida else COLOR_OPCION
            texto = self._fuente_opcion.render(f"> {opcion} <" if elegida else opcion, True, color)
            superficie.blit(texto, texto.get_rect(center=(ancho // 2, alto // 2 + i * 45)))
