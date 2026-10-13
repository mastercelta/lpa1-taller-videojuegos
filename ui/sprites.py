import math

import pygame

from ui.renderizador import TAMAÑO_CELDA as C

# Sprites dibujados con formas mientras llegan los vectores definitivos (Recraft / Rive).
# Cada función recibe la esquina superior izquierda en píxeles, así se pueden animar
# posiciones intermedias entre celdas (movimiento fluido, R10.1).

PIEL = (240, 200, 160)
PELO = (60, 45, 40)
SUDADERA = (70, 130, 230)
PANTALON = (40, 50, 80)
BLANCO = (245, 245, 245)
NEGRO = (20, 20, 25)

_fuentes = {}


def _fuente(tamaño: int, negrita: bool = True):
    clave = (tamaño, negrita)
    if clave not in _fuentes:
        _fuentes[clave] = pygame.font.SysFont("arial", tamaño, bold=negrita)
    return _fuentes[clave]


def _sombra(superficie, cx: float, piso: float, ancho: int = 26) -> None:
    sombra = pygame.Surface((ancho, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 90), (0, 0, ancho, 8))
    superficie.blit(sombra, (cx - ancho / 2, piso - 4))


def _ojos(superficie, cx: float, cy: float, direccion: str, separacion: int = 5, radio: int = 3) -> None:
    dx = {"izquierda": -2, "derecha": 2}.get(direccion, 0)
    dy = {"arriba": -2, "abajo": 1}.get(direccion, 0)
    for lado in (-1, 1):
        x, y = cx + lado * separacion, cy
        pygame.draw.circle(superficie, BLANCO, (x, y), radio + 1)
        pygame.draw.circle(superficie, NEGRO, (x + dx, y + dy), radio - 1)


def dibujar_estudiante(superficie, px: float, py: float, direccion: str, t: float, caminando: bool) -> None:
    cx = px + C / 2
    paso = math.sin(t * 14) if caminando else 0
    rebote = abs(paso) * 2
    _sombra(superficie, cx, py + C - 4)

    # piernas: se alternan al caminar
    for lado in (-1, 1):
        alto = 8 + (paso * lado * 2 if caminando else 0)
        pygame.draw.rect(superficie, PANTALON, (cx + lado * 5 - 3, py + 34 - rebote, 6, max(4, alto)), border_radius=2)

    # cuerpo con mochila visible de espaldas
    pygame.draw.rect(superficie, SUDADERA, (cx - 11, py + 20 - rebote, 22, 17), border_radius=6)
    if direccion == "arriba":
        pygame.draw.rect(superficie, (200, 90, 60), (cx - 8, py + 22 - rebote, 16, 12), border_radius=4)

    # cabeza
    cabeza_y = py + 13 - rebote
    pygame.draw.circle(superficie, PIEL, (cx, cabeza_y), 10)
    if direccion == "arriba":
        pygame.draw.circle(superficie, PELO, (cx, cabeza_y), 10)
    else:
        pygame.draw.arc(superficie, PELO, (cx - 10, cabeza_y - 11, 20, 16), 0.1, math.pi - 0.1, 6)
        if direccion == "izquierda":
            pygame.draw.circle(superficie, NEGRO, (cx - 5, cabeza_y + 1), 2)
        elif direccion == "derecha":
            pygame.draw.circle(superficie, NEGRO, (cx + 5, cabeza_y + 1), 2)
        else:
            pygame.draw.circle(superficie, NEGRO, (cx - 4, cabeza_y + 1), 2)
            pygame.draw.circle(superficie, NEGRO, (cx + 4, cabeza_y + 1), 2)


def _null_pointer(superficie, px, py, direccion, t):
    # fantasma: una variable que apunta a la nada
    cx, flote = px + C / 2, math.sin(t * 3) * 2
    color = (175, 145, 235)
    _sombra(superficie, cx, py + C - 4, 22)
    pygame.draw.circle(superficie, color, (cx, py + 20 + flote), 14)
    pygame.draw.rect(superficie, color, (cx - 14, py + 20 + flote, 28, 14))
    for i in range(3):
        pygame.draw.circle(superficie, color, (cx - 9 + i * 9, py + 34 + flote), 5)
    _ojos(superficie, cx, py + 19 + flote, direccion)
    texto = _fuente(10).render("null", True, (90, 60, 150))
    superficie.blit(texto, texto.get_rect(center=(cx, py + 29 + flote)))


def _bucle_infinito(superficie, px, py, direccion, t):
    # anillo que gira sin parar
    cx, cy = px + C / 2, py + C / 2
    color = (235, 125, 60)
    _sombra(superficie, cx, py + C - 4, 24)
    giro = t * 4
    rect = (cx - 16, cy - 16, 32, 32)
    pygame.draw.arc(superficie, color, rect, giro, giro + 5.0, 5)
    punta = (cx + 16 * math.cos(giro), cy - 16 * math.sin(giro))
    pygame.draw.circle(superficie, (255, 200, 120), punta, 4)
    pygame.draw.circle(superficie, (60, 30, 20), (cx, cy), 9)
    _ojos(superficie, cx, cy, direccion, separacion=4, radio=2)


def _variable_global(superficie, px, py, direccion, t):
    # slime que se estira: se mete en todas partes
    cx = px + C / 2
    estira = math.sin(t * 5) * 3
    color = (95, 205, 125)
    _sombra(superficie, cx, py + C - 4, 30)
    pygame.draw.ellipse(superficie, color, (cx - 16 - estira, py + 16 + estira, 32 + estira * 2, 26 - estira))
    pygame.draw.ellipse(superficie, (150, 235, 170), (cx - 9, py + 20 + estira, 8, 5))
    _ojos(superficie, cx, py + 28, direccion)
    texto = _fuente(11).render("G", True, (30, 90, 50))
    superficie.blit(texto, texto.get_rect(center=(cx, py + 37)))


def _memory_leak(superficie, px, py, direccion, t):
    # gota voladora que va perdiendo memoria
    cx, altura = px + C / 2, 6 + math.sin(t * 6) * 3
    color = (85, 175, 235)
    _sombra(superficie, cx, py + C - 4, 16)
    aleteo = abs(math.sin(t * 18)) * 8
    for lado in (-1, 1):
        ala = [(cx + lado * 8, py + 20 - altura), (cx + lado * 20, py + 12 - altura - aleteo), (cx + lado * 18, py + 24 - altura)]
        pygame.draw.polygon(superficie, (200, 225, 245), ala)
    gota = [(cx, py + 4 - altura), (cx - 11, py + 22 - altura), (cx + 11, py + 22 - altura)]
    pygame.draw.polygon(superficie, color, gota)
    pygame.draw.circle(superficie, color, (cx, py + 24 - altura), 11)
    _ojos(superficie, cx, py + 23 - altura, direccion, separacion=4, radio=2)
    goteo = (t * 30) % 14
    pygame.draw.circle(superficie, color, (cx + 2, py + 36 - altura + goteo), 2)


def _legacy_code(superficie, px, py, direccion, t):
    # jefe: bloque de espagueti sin comentarios
    cx = px + C / 2
    pulso = math.sin(t * 2.5) * 2
    _sombra(superficie, cx, py + C - 2, 40)
    cuerpo = pygame.Rect(px + 3 - pulso, py + 3 - pulso, C - 6 + pulso * 2, C - 8 + pulso * 2)
    pygame.draw.rect(superficie, (130, 55, 45), cuerpo, border_radius=8)
    for i in range(4):
        y = cuerpo.top + 8 + i * 9
        puntos = [(cuerpo.left + 4 + k * 5, y + math.sin(t * 3 + k + i) * 3) for k in range(8)]
        pygame.draw.lines(superficie, (235, 200, 90), False, puntos, 2)
    for lado in (-1, 1):
        ojo = (cx + lado * 9, py + 18)
        pygame.draw.circle(superficie, (255, 230, 120), ojo, 5)
        pygame.draw.circle(superficie, (180, 20, 20), ojo, 2)
        pygame.draw.line(superficie, NEGRO, (cx + lado * 4, py + 10), (cx + lado * 14, py + 13), 3)


def _enemigo_generico(superficie, px, py, enemigo, t):
    cx = px + C / 2
    color = (220, 70, 70) if enemigo.tipo == "terrestre" else (230, 150, 50)
    _sombra(superficie, cx, py + C - 4)
    pygame.draw.rect(superficie, color, (px + 10, py + 12, C - 20, C - 20), border_radius=6)
    _ojos(superficie, cx, py + 22, enemigo.direccion)


DIBUJOS_ENEMIGOS = {
    "EnemigoNullPointer": _null_pointer,
    "EnemigoBucleInfinito": _bucle_infinito,
    "EnemigoVariableGlobal": _variable_global,
    "EnemigoMemoryLeak": _memory_leak,
    "EnemigoJefe": _legacy_code,
}


def dibujar_enemigo(superficie, px: float, py: float, enemigo, t: float) -> None:
    dibujo = DIBUJOS_ENEMIGOS.get(type(enemigo).__name__)
    if dibujo is None:
        _enemigo_generico(superficie, px, py, enemigo, t)
    else:
        dibujo(superficie, px, py, enemigo.direccion, t)


def dibujar_objeto(superficie, px: float, py: float, objeto, t: float) -> None:
    cx, cy = px + C / 2, py + C / 2
    clase = type(objeto).__name__
    flote = math.sin(t * 3) * 2
    if clase == "Tesoro" and "Café" in objeto.nombre:
        pygame.draw.rect(superficie, (235, 235, 225), (cx - 9, cy - 6 + flote, 18, 16), border_radius=3)
        pygame.draw.arc(superficie, (235, 235, 225), (cx + 5, cy - 3 + flote, 9, 9), -1.6, 1.6, 2)
        pygame.draw.rect(superficie, (110, 70, 40), (cx - 7, cy - 4 + flote, 14, 4))
        for i in (-3, 3):
            pygame.draw.line(superficie, (200, 200, 200), (cx + i, cy - 14 + flote), (cx + i + 2, cy - 9 + flote), 1)
    elif clase == "Tesoro":
        pygame.draw.circle(superficie, (240, 200, 50), (cx, cy + flote), 12)
        pygame.draw.circle(superficie, (255, 230, 120), (cx, cy + flote), 12, 2)
        texto = _fuente(12).render("{ }", True, (150, 110, 20))
        superficie.blit(texto, texto.get_rect(center=(cx, cy + flote)))
    elif clase == "TrampaExplosiva":
        brillo = 120 + int(80 * abs(math.sin(t * 4)))
        puntos = [(cx, py + 10), (px + C - 10, cy), (cx, py + C - 10), (px + 10, cy)]
        pygame.draw.polygon(superficie, (brillo, 40, 40), puntos)
        texto = _fuente(16).render("!", True, (255, 220, 120))
        superficie.blit(texto, texto.get_rect(center=(cx, cy)))
    else:
        pygame.draw.rect(superficie, (120, 220, 160), (px + 12, py + 12 + flote, C - 24, C - 24), border_radius=4)
