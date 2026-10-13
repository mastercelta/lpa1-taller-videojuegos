import pygame

from ui.estados.base import Estado

COLOR_FONDO = (18, 20, 28)
COLOR_TITULO = (120, 230, 150)
COLOR_TEXTO = (210, 215, 225)
COLOR_RESALTE = (240, 210, 60)

SECCIONES = [
    ("La historia", [
        "Te dormiste estudiando para el parcial de programación.",
        "Tu código roto cobró vida: cada error es un enemigo.",
        "Depúralo todo antes de que suene el despertador.",
    ]),
    ("Controles", [
        "Flechas: moverte   |   ESC: pausa",
        "Choca con un bug para atacarlo.",
        "R: reiniciar al terminar la partida.",
    ]),
    ("Las zonas", [
        "1. Valle de las Variables      (tipos de datos)",
        "2. Bosque de los Condicionales (if / else)",
        "3. Laberinto de los Bucles     (while / for)",
        "4. Castillo de los Objetos     (clases y herencia)",
    ]),
]


class EstadoComoJugar(Estado):

    def __init__(self, aplicacion):
        super().__init__(aplicacion)
        self._fuente_titulo = pygame.font.SysFont("arial", 30, bold=True)
        self._fuente_seccion = pygame.font.SysFont("arial", 20, bold=True)
        self._fuente_texto = pygame.font.SysFont("arial", 17)

    def manejar_evento(self, evento) -> None:
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
            from ui.estados.menu import EstadoMenu
            self.aplicacion.cambiar_estado(EstadoMenu(self.aplicacion))

    def dibujar(self, superficie) -> None:
        ancho, alto = superficie.get_size()
        superficie.fill(COLOR_FONDO)
        titulo = self._fuente_titulo.render("Cómo jugar", True, COLOR_TITULO)
        superficie.blit(titulo, titulo.get_rect(center=(ancho // 2, 40)))

        y = 85
        for nombre, lineas in SECCIONES:
            superficie.blit(self._fuente_seccion.render(nombre, True, COLOR_RESALTE), (40, y))
            y += 30
            for linea in lineas:
                superficie.blit(self._fuente_texto.render(linea, True, COLOR_TEXTO), (60, y))
                y += 24
            y += 14

        volver = self._fuente_texto.render("Enter o ESC para volver al menú", True, COLOR_RESALTE)
        superficie.blit(volver, volver.get_rect(center=(ancho // 2, alto - 25)))
