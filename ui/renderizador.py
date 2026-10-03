import pygame

TAMAÑO_CELDA = 48

COLOR_FONDO = (24, 26, 34)
COLOR_GRILLA = (40, 43, 54)
COLOR_PERSONAJE = (90, 160, 255)
COLOR_ENEMIGO_TERRESTRE = (220, 70, 70)
COLOR_ENEMIGO_VOLADOR = (230, 150, 50)
COLOR_TRAMPA = (160, 40, 40)
COLOR_TESORO = (240, 210, 60)
COLOR_ARMAMENTO = (120, 220, 160)
COLOR_ZONA_VENTA = (50, 90, 60)


def celda_a_pixel(x: int, y: int) -> tuple:
    return (x * TAMAÑO_CELDA, y * TAMAÑO_CELDA)


def dibujar_grilla(superficie, ancho: int, alto: int) -> None:
    superficie.fill(COLOR_FONDO)
    for x in range(ancho + 1):
        px = x * TAMAÑO_CELDA
        pygame.draw.line(superficie, COLOR_GRILLA, (px, 0), (px, alto * TAMAÑO_CELDA))
    for y in range(alto + 1):
        py = y * TAMAÑO_CELDA
        pygame.draw.line(superficie, COLOR_GRILLA, (0, py), (ancho * TAMAÑO_CELDA, py))


def dibujar_zona_venta(superficie, pos: tuple) -> None:
    px, py = celda_a_pixel(*pos)
    pygame.draw.rect(superficie, COLOR_ZONA_VENTA, (px, py, TAMAÑO_CELDA, TAMAÑO_CELDA))


def dibujar_personaje(superficie, pos: tuple) -> None:
    px, py = celda_a_pixel(*pos)
    centro = (px + TAMAÑO_CELDA // 2, py + TAMAÑO_CELDA // 2)
    pygame.draw.circle(superficie, COLOR_PERSONAJE, centro, TAMAÑO_CELDA // 2 - 4)


def dibujar_enemigo(superficie, pos: tuple, enemigo) -> None:
    px, py = celda_a_pixel(*pos)
    margen = 8
    rect = (px + margen, py + margen, TAMAÑO_CELDA - margen * 2, TAMAÑO_CELDA - margen * 2)
    if enemigo.tipo == "terrestre":
        pygame.draw.rect(superficie, COLOR_ENEMIGO_TERRESTRE, rect)
    else:
        centro = (px + TAMAÑO_CELDA // 2, py + TAMAÑO_CELDA // 2)
        puntos = [
            (centro[0], py + margen),
            (px + margen, py + TAMAÑO_CELDA - margen),
            (px + TAMAÑO_CELDA - margen, py + TAMAÑO_CELDA - margen),
        ]
        pygame.draw.polygon(superficie, COLOR_ENEMIGO_VOLADOR, puntos)


def dibujar_objeto(superficie, pos: tuple, objeto) -> None:
    px, py = celda_a_pixel(*pos)
    centro = (px + TAMAÑO_CELDA // 2, py + TAMAÑO_CELDA // 2)
    nombre_clase = type(objeto).__name__
    if nombre_clase == "Tesoro":
        pygame.draw.circle(superficie, COLOR_TESORO, centro, TAMAÑO_CELDA // 3)
    elif nombre_clase == "TrampaExplosiva":
        puntos = [
            (centro[0], py + 10),
            (px + TAMAÑO_CELDA - 10, centro[1]),
            (centro[0], py + TAMAÑO_CELDA - 10),
            (px + 10, centro[1]),
        ]
        pygame.draw.polygon(superficie, COLOR_TRAMPA, puntos)
    else:
        pygame.draw.rect(superficie, COLOR_ARMAMENTO, (px + 10, py + 10, TAMAÑO_CELDA - 20, TAMAÑO_CELDA - 20))
