import pygame

from ui.estados.base import Estado

COLOR_FONDO = (18, 20, 28)
COLOR_TITULO = (120, 230, 150)
COLOR_SUBTITULO = (150, 160, 180)
COLOR_OPCION = (210, 215, 225)
COLOR_SELECCION = (240, 210, 60)
COLOR_CODIGO = (40, 46, 60)

LINEAS_DE_FONDO = [
    "while not despierto:",
    "    depurar(codigo)",
    "if bug is None:",
    "    raise NullPointer",
    "for zona in mundo:",
    "    zona.explorar()",
    "class LegacyCode(Bug):",
    "    pass  # nadie sabe",
]


class EstadoMenu(Estado):
    # R9.1: pantalla principal navegable con teclado

    OPCIONES = ("Nueva partida", "Cómo jugar", "Salir")

    def __init__(self, aplicacion):
        super().__init__(aplicacion)
        self._seleccion = 0
        self._partida = aplicacion.guardado.cargar()
        self._opciones = (("Continuar",) if self._partida else ()) + self.OPCIONES
        self._fuente_titulo = pygame.font.SysFont("arial", 40, bold=True)
        self._fuente_sub = pygame.font.SysFont("arial", 18, italic=True)
        self._fuente_opcion = pygame.font.SysFont("arial", 26)
        self._fuente_codigo = pygame.font.SysFont("courier", 18)

    @property
    def seleccion(self) -> int:
        return self._seleccion

    @property
    def opciones(self) -> tuple:
        return self._opciones

    def manejar_evento(self, evento) -> None:
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key == pygame.K_UP:
            self._seleccion = (self._seleccion - 1) % len(self._opciones)
        elif evento.key == pygame.K_DOWN:
            self._seleccion = (self._seleccion + 1) % len(self._opciones)
        elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self._elegir()
        elif evento.key == pygame.K_ESCAPE:
            self.aplicacion.salir()

    def _elegir(self) -> None:
        from ui.estados.como_jugar import EstadoComoJugar
        from ui.estados.jugando import EstadoJugando

        opcion = self._opciones[self._seleccion]
        if opcion == "Continuar":
            self.aplicacion.cambiar_estado(EstadoJugando(self.aplicacion, self._partida))
        elif opcion == "Nueva partida":
            self.aplicacion.cambiar_estado(EstadoJugando(self.aplicacion))
        elif opcion == "Cómo jugar":
            self.aplicacion.cambiar_estado(EstadoComoJugar(self.aplicacion))
        else:
            self.aplicacion.salir()

    def dibujar(self, superficie) -> None:
        ancho, alto = superficie.get_size()
        superficie.fill(COLOR_FONDO)

        # el código de fondo se reparte en dos esquinas, lejos del título y de las opciones
        mitad = len(LINEAS_DE_FONDO) // 2
        for i, linea in enumerate(LINEAS_DE_FONDO[:mitad]):
            texto = self._fuente_codigo.render(linea, True, COLOR_CODIGO)
            superficie.blit(texto, (20, 15 + i * 22))
        for i, linea in enumerate(LINEAS_DE_FONDO[mitad:]):
            texto = self._fuente_codigo.render(linea, True, COLOR_CODIGO)
            superficie.blit(texto, (ancho - texto.get_width() - 20, alto - 150 + i * 22))

        titulo = self._fuente_titulo.render("Depuración", True, COLOR_TITULO)
        superficie.blit(titulo, titulo.get_rect(center=(ancho // 2, alto // 4)))
        sub = self._fuente_sub.render("El Sueño del Programador", True, COLOR_SUBTITULO)
        superficie.blit(sub, sub.get_rect(center=(ancho // 2, alto // 4 + 40)))

        for i, opcion in enumerate(self._opciones):
            elegida = i == self._seleccion
            texto = f"> {opcion} <" if elegida else opcion
            color = COLOR_SELECCION if elegida else COLOR_OPCION
            render = self._fuente_opcion.render(texto, True, color)
            superficie.blit(render, render.get_rect(center=(ancho // 2, alto // 2 + 20 + i * 50)))

        ayuda = self._fuente_sub.render("Flechas para elegir, Enter para confirmar", True, COLOR_SUBTITULO)
        superficie.blit(ayuda, ayuda.get_rect(center=(ancho // 2, alto - 30)))
