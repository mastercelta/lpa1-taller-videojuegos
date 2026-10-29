import math
import random

import pygame

from ui import sprites
from ui.estados.base import Estado
from ui.texturas import cargar_png

DORADO = (250, 205, 70)
DORADO_OSCURO = (150, 95, 20)
VERDE_CODIGO = (90, 230, 140)
SIMBOLOS = ("{ }", "01", ";", "if", "()", "//", "[ ]", "def")
DURACION_FUNDIDO = 1.2


class EstadoTitulo(Estado):
    # Pantalla de título estilo Zelda: ilustración, logo y "Presiona Enter" antes del menú.
    # Si existen assets/titulo_fondo.png y assets/titulo_logo.png (Recraft) se usan esos.

    pista = "titulo"

    def __init__(self, aplicacion):
        super().__init__(aplicacion)
        ancho, alto = aplicacion.tamaño
        self._tiempo = 0.0
        self._fondo = cargar_png("titulo_fondo.png", (ancho, alto))
        self._logo = cargar_png("titulo_logo.png")
        azar = random.Random(3)
        self._estrellas = [(azar.random(), azar.random() * 0.55, azar.random()) for _ in range(90)]
        self._particulas = [[azar.random(), azar.random(), azar.choice(SIMBOLOS), 0.03 + azar.random() * 0.05]
                            for _ in range(14)]
        self._fuente_logo = pygame.font.SysFont("arial", 64, bold=True)
        self._fuente_sub = pygame.font.SysFont("arial", 22, italic=True)
        self._fuente_enter = pygame.font.SysFont("arial", 22, bold=True)
        self._fuente_codigo = pygame.font.SysFont("courier", 14, bold=True)
        self._fuente_pie = pygame.font.SysFont("arial", 13)

    def manejar_evento(self, evento) -> None:
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key == pygame.K_ESCAPE:
            self.aplicacion.salir()
        elif self._tiempo >= 0.4:
            from ui.estados.menu import EstadoMenu
            self.aplicacion.cambiar_estado(EstadoMenu(self.aplicacion))

    def actualizar(self, dt: float) -> None:
        self._tiempo += dt
        for p in self._particulas:
            p[1] -= p[3] * dt
            if p[1] < 0.45:
                p[1] = 1.0
                p[0] = random.random()

    def dibujar(self, superficie) -> None:
        ancho, alto = superficie.get_size()
        if self._fondo is not None:
            superficie.blit(self._fondo, (0, 0))
        else:
            self._dibujar_paisaje(superficie, ancho, alto)
        self._dibujar_particulas(superficie, ancho, alto)
        self._dibujar_logo(superficie, ancho, alto)

        if int(self._tiempo * 1.6) % 2 == 0 and self._tiempo > DURACION_FUNDIDO:
            enter = self._fuente_enter.render("PRESIONA ENTER", True, (240, 240, 240))
            sombra = self._fuente_enter.render("PRESIONA ENTER", True, (0, 0, 0))
            centro = (ancho // 2, int(alto * 0.80))
            superficie.blit(sombra, sombra.get_rect(center=(centro[0] + 2, centro[1] + 2)))
            superficie.blit(enter, enter.get_rect(center=centro))
        pie = self._fuente_pie.render("Taller 3 · POO · @mastercelta · música CC0: Aureolus_Omicron", True, (120, 125, 145))
        superficie.blit(pie, pie.get_rect(center=(ancho // 2, alto - 14)))

        if self._tiempo < DURACION_FUNDIDO:
            negro = pygame.Surface((ancho, alto))
            negro.fill((0, 0, 0))
            negro.set_alpha(int(255 * (1 - self._tiempo / DURACION_FUNDIDO)))
            superficie.blit(negro, (0, 0))

    def _dibujar_paisaje(self, superficie, ancho: int, alto: int) -> None:
        # cielo nocturno en degradado
        for y in range(alto):
            k = y / alto
            superficie.fill((int(8 + 20 * k), int(10 + 18 * k), int(30 + 30 * k)), (0, y, ancho, 1))
        for x, y, fase in self._estrellas:
            brillo = 90 + int(120 * abs(math.sin(self._tiempo * 1.3 + fase * 9)))
            superficie.set_at((int(x * ancho), int(y * alto)), (brillo, brillo, min(255, brillo + 30)))
        pygame.draw.circle(superficie, (240, 236, 205), (int(ancho * 0.12), int(alto * 0.40)), 26)
        pygame.draw.circle(superficie, (16, 18, 42), (int(ancho * 0.12) + 10, int(alto * 0.40) - 7), 23)

        # montañas lejanas
        horizonte = int(alto * 0.70)
        picos = [(0, horizonte), (0, horizonte - 60), (90, horizonte - 120), (180, horizonte - 50), (270, horizonte - 140),
                 (380, horizonte - 70), (470, horizonte - 130), (560, horizonte - 60), (ancho, horizonte - 100), (ancho, horizonte)]
        pygame.draw.polygon(superficie, (22, 26, 52), picos)

        # castillo del Legacy Code hecho de bloques de código
        self._dibujar_castillo(superficie, ancho // 2, horizonte)

        # suelo y camino
        pygame.draw.rect(superficie, (14, 30, 28), (0, horizonte, ancho, alto - horizonte))
        pygame.draw.polygon(superficie, (40, 52, 60), [(ancho // 2 - 18, horizonte), (ancho // 2 + 18, horizonte),
                                                       (ancho // 2 + 90, alto), (ancho // 2 - 90, alto)])
        # el estudiante y el pato de espaldas, mirando el castillo
        sprites.dibujar_estudiante(superficie, ancho // 2 - 30, int(alto * 0.84), "arriba", 0, False)
        pato_x, pato_y = ancho // 2 + 22, int(alto * 0.90)
        pygame.draw.ellipse(superficie, (250, 215, 60), (pato_x - 10, pato_y, 20, 11))
        pygame.draw.circle(superficie, (250, 215, 60), (pato_x + 5, pato_y - 2), 6)
        pygame.draw.polygon(superficie, (245, 140, 40), [(pato_x + 10, pato_y - 3), (pato_x + 15, pato_y - 1), (pato_x + 10, pato_y + 1)])

    def _dibujar_castillo(self, superficie, cx: int, base: int) -> None:
        bloque = (36, 40, 62)
        borde = (58, 64, 96)
        torres = [(-150, 120, 36), (-70, 170, 44), (0, 230, 56), (70, 170, 44), (150, 120, 36)]
        for dx, alto_torre, ancho_torre in torres:
            x = cx + dx - ancho_torre // 2
            pygame.draw.rect(superficie, bloque, (x, base - alto_torre, ancho_torre, alto_torre))
            pygame.draw.rect(superficie, borde, (x, base - alto_torre, ancho_torre, alto_torre), 2)
            for i in range(0, ancho_torre, 10):
                pygame.draw.rect(superficie, bloque, (x + i, base - alto_torre - 8, 6, 8))
            # ventanas con líneas de código que brillan
            for fila in range(alto_torre // 26):
                pulso = 0.5 + 0.5 * math.sin(self._tiempo * 2 + dx * 0.05 + fila)
                verde = (int(40 + 50 * pulso), int(120 + 110 * pulso), int(70 + 70 * pulso))
                largo = 8 + (fila * 7 + dx) % (ancho_torre - 16)
                pygame.draw.line(superficie, verde, (x + 6, base - alto_torre + 18 + fila * 26),
                                 (x + 6 + largo, base - alto_torre + 18 + fila * 26), 3)
        pygame.draw.rect(superficie, bloque, (cx - 190, base - 60, 380, 60))
        pygame.draw.rect(superficie, borde, (cx - 190, base - 60, 380, 60), 2)
        pygame.draw.rect(superficie, (12, 12, 20), (cx - 18, base - 44, 36, 44), border_top_left_radius=18, border_top_right_radius=18)
        ojo = 0.5 + 0.5 * math.sin(self._tiempo * 3)
        for lado in (-1, 1):
            pygame.draw.circle(superficie, (int(180 + 70 * ojo), 60, 50), (cx + lado * 7, base - 28), 3)

    def _dibujar_particulas(self, superficie, ancho: int, alto: int) -> None:
        for x, y, simbolo, _ in self._particulas:
            alfa = max(0, min(1, (y - 0.45) / 0.3))
            color = tuple(int(c * alfa) for c in VERDE_CODIGO)
            superficie.blit(self._fuente_codigo.render(simbolo, True, color), (x * ancho, y * alto))

    def _dibujar_logo(self, superficie, ancho: int, alto: int) -> None:
        flote = math.sin(self._tiempo * 1.5) * 4
        centro = (ancho // 2, int(alto * 0.17 + flote))
        if self._logo is not None:
            superficie.blit(self._logo, self._logo.get_rect(center=centro))
            return
        texto = "DEPURACIÓN"
        for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 4), (-3, 3), (3, 3)):
            borde = self._fuente_logo.render(texto, True, (25, 15, 5))
            superficie.blit(borde, borde.get_rect(center=(centro[0] + dx, centro[1] + dy)))
        sombra = self._fuente_logo.render(texto, True, DORADO_OSCURO)
        superficie.blit(sombra, sombra.get_rect(center=(centro[0], centro[1] + 2)))
        logo = self._fuente_logo.render(texto, True, DORADO)
        rect = logo.get_rect(center=centro)
        superficie.blit(logo, rect)
        # brillo que recorre las letras: una franja blanca recortada con la forma del texto
        franja = pygame.Surface(rect.size, pygame.SRCALPHA)
        x = (self._tiempo * 180) % (rect.width + 240) - 120
        pygame.draw.polygon(franja, (255, 255, 255, 140), [(x, 0), (x + 22, 0), (x - 4, rect.height), (x - 26, rect.height)])
        brillo = pygame.mask.from_surface(logo).to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))
        brillo.blit(franja, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        superficie.blit(brillo, rect)
        cursor = "|" if int(self._tiempo * 2) % 2 == 0 else " "
        sub = self._fuente_sub.render(f"— El Sueño del Programador —{cursor}", True, (190, 200, 225))
        superficie.blit(sub, sub.get_rect(center=(centro[0], centro[1] + 52)))
