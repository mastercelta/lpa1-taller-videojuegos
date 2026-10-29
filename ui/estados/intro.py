import math
import random

import pygame

from mundo.historia import INTRO, JEFE, NARRADOR, PATO
from ui import sprites
from ui.estados.base import Estado

VELOCIDAD_TEXTO = 45  # letras por segundo, efecto máquina de escribir
COLOR_FONDO = (10, 11, 18)
COLOR_TEXTO = (225, 228, 238)
COLOR_AYUDA = (130, 136, 155)
COLORES_HABLANTE = {NARRADOR: (150, 160, 190), PATO: (250, 215, 60), JEFE: (230, 110, 80)}


class EstadoIntro(Estado):
    # Escena de diálogos antes de la partida: Enter avanza, ESC la salta

    def __init__(self, aplicacion, dialogos: list = None):
        super().__init__(aplicacion)
        self._dialogos = dialogos or INTRO
        self._indice = 0
        self._letras = 0.0
        self._tiempo = 0.0
        azar = random.Random(7)
        self._estrellas = [(azar.random(), azar.random(), azar.random()) for _ in range(70)]
        self._fuente_nombre = pygame.font.SysFont("arial", 20, bold=True)
        self._fuente_texto = pygame.font.SysFont("arial", 19)
        self._fuente_ayuda = pygame.font.SysFont("arial", 14, italic=True)

    @property
    def indice(self) -> int:
        return self._indice

    def _texto_actual(self) -> str:
        return self._dialogos[self._indice][1]

    def _terminado_de_escribir(self) -> bool:
        return self._letras >= len(self._texto_actual())

    def _empezar_partida(self) -> None:
        from ui.estados.jugando import EstadoJugando
        self.aplicacion.cambiar_estado(EstadoJugando(self.aplicacion))

    def manejar_evento(self, evento) -> None:
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key == pygame.K_ESCAPE:
            self._empezar_partida()
        elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            if not self._terminado_de_escribir():
                self._letras = len(self._texto_actual())
            elif self._indice + 1 < len(self._dialogos):
                self._indice += 1
                self._letras = 0
            else:
                self._empezar_partida()

    def actualizar(self, dt: float) -> None:
        self._tiempo += dt
        self._letras = min(len(self._texto_actual()), self._letras + VELOCIDAD_TEXTO * dt)

    def dibujar(self, superficie) -> None:
        ancho, alto = superficie.get_size()
        superficie.fill(COLOR_FONDO)
        for x, y, fase in self._estrellas:
            brillo = 60 + int(70 * abs(math.sin(self._tiempo * 1.5 + fase * 6)))
            superficie.set_at((int(x * ancho), int(y * alto * 0.6)), (brillo, brillo, brillo + 30))

        hablante, texto = self._dialogos[self._indice]
        self._dibujar_retrato(superficie, hablante, ancho // 2, int(alto * 0.33))

        caja = pygame.Rect(30, alto - 200, ancho - 60, 160)
        pygame.draw.rect(superficie, (22, 25, 36), caja, border_radius=10)
        pygame.draw.rect(superficie, COLORES_HABLANTE[hablante], caja, 2, border_radius=10)
        nombre = self._fuente_nombre.render(hablante, True, COLORES_HABLANTE[hablante])
        superficie.blit(nombre, (caja.x + 18, caja.y + 12))

        visible = texto[:int(self._letras)]
        for i, linea in enumerate(_partir(visible, self._fuente_texto, caja.width - 36)):
            superficie.blit(self._fuente_texto.render(linea, True, COLOR_TEXTO), (caja.x + 18, caja.y + 46 + i * 26))

        pista = "Enter: continuar   ·   ESC: saltar"
        if self._terminado_de_escribir() and int(self._tiempo * 2) % 2 == 0:
            pista = "▼  " + pista
        ayuda = self._fuente_ayuda.render(f"{pista}   ·   {self._indice + 1}/{len(self._dialogos)}", True, COLOR_AYUDA)
        superficie.blit(ayuda, ayuda.get_rect(bottomright=(caja.right - 12, caja.bottom - 8)))

    def _dibujar_retrato(self, superficie, hablante: str, cx: int, cy: int) -> None:
        flote = math.sin(self._tiempo * 2) * 4
        if hablante == PATO:
            _dibujar_pato(superficie, cx, cy + flote)
        elif hablante == JEFE:
            lienzo = pygame.Surface((48, 48), pygame.SRCALPHA)
            sprites.DIBUJOS_ENEMIGOS["EnemigoJefe"](lienzo, 0, 0, "abajo", self._tiempo)
            grande = pygame.transform.scale(lienzo, (144, 144))
            superficie.blit(grande, grande.get_rect(center=(cx, cy + flote)))
        else:
            # luna y reloj: la noche antes del parcial
            pygame.draw.circle(superficie, (235, 232, 200), (cx, cy), 46)
            pygame.draw.circle(superficie, COLOR_FONDO, (cx + 20, cy - 12), 42)
            reloj = self._fuente_nombre.render("03:07", True, (235, 90, 90))
            superficie.blit(reloj, reloj.get_rect(center=(cx - 10, cy + 70)))


def _dibujar_pato(superficie, cx: float, cy: float) -> None:
    amarillo, sombra = (250, 215, 60), (215, 175, 40)
    pygame.draw.ellipse(superficie, sombra, (cx - 58, cy - 2, 116, 66))
    pygame.draw.ellipse(superficie, amarillo, (cx - 56, cy - 6, 112, 62))
    pygame.draw.circle(superficie, amarillo, (cx + 22, cy - 26), 32)
    pygame.draw.polygon(superficie, (245, 140, 40), [(cx + 48, cy - 30), (cx + 78, cy - 22), (cx + 48, cy - 14)])
    pygame.draw.circle(superficie, (255, 255, 255), (cx + 30, cy - 36), 9)
    pygame.draw.circle(superficie, (20, 20, 25), (cx + 33, cy - 36), 5)
    pygame.draw.arc(superficie, sombra, (cx - 40, cy + 4, 50, 30), 3.4, 5.6, 4)


def _partir(texto: str, fuente, ancho_max: int) -> list:
    lineas, actual = [], ""
    for palabra in texto.split(" "):
        prueba = f"{actual} {palabra}".strip()
        if fuente.size(prueba)[0] <= ancho_max:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas
