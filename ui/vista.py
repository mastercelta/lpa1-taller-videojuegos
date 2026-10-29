import math

from ui import hud
from ui import renderizador as r
from ui import sprites
from ui.texturas import Texturas

_texturas = Texturas()


def tamaño_ventana(juego) -> tuple:
    return (juego.ancho * r.TAMAÑO_CELDA, juego.alto * r.TAMAÑO_CELDA + hud.ALTURA_HUD)


def dibujar_juego(superficie, juego, animador=None) -> None:
    escenario = juego.escenario
    ancho_px = juego.ancho * r.TAMAÑO_CELDA
    alto_px_mapa = juego.alto * r.TAMAÑO_CELDA
    t = animador.tiempo if animador else 0.0

    def pixel(entidad, celda):
        if animador:
            return animador.posicion(entidad, celda)
        return (celda[0] * r.TAMAÑO_CELDA, celda[1] * r.TAMAÑO_CELDA)

    C = r.TAMAÑO_CELDA
    for x in range(juego.ancho):
        for y in range(juego.alto):
            superficie.blit(_texturas.piso(x, y), (x * C, y * C))
    zx, zy = escenario.zona_venta
    superficie.blit(_texturas.zona_venta(), (zx * C, zy * C))
    obstaculo = _texturas.obstaculo()
    for celda in escenario.obstaculos:
        if obstaculo is not None:
            superficie.blit(obstaculo, (celda[0] * C, celda[1] * C))
        else:
            sprites.dibujar_obstaculo(superficie, celda[0] * C, celda[1] * C)
    for celda, objeto in escenario.objetos.items():
        sprites.dibujar_objeto(superficie, celda[0] * r.TAMAÑO_CELDA, celda[1] * r.TAMAÑO_CELDA, objeto, t)

    # se dibuja de arriba hacia abajo para que quien está más abajo quede adelante
    personaje = juego.personaje
    actores = [(enemigo, celda) for celda, enemigo in escenario.enemigos.items() if escenario.revelada(celda)]
    actores.append((personaje, personaje.posicion))
    actores.sort(key=lambda par: pixel(*par)[1])
    for entidad, celda in actores:
        px, py = pixel(entidad, celda)
        nombre = f"estudiante_{personaje.direccion}" if entidad is personaje else type(entidad).__name__
        imagen = _texturas.sprite(nombre)
        if imagen is not None:
            flote = 2 * math.sin(t * 6) if getattr(entidad, "vuela", False) else 0
            superficie.blit(imagen, (px, py + flote))  # asset de Recraft
        elif entidad is personaje:
            caminando = animador.caminando(personaje) if animador else False
            sprites.dibujar_estudiante(superficie, px, py, personaje.direccion, t, caminando)
        else:
            sprites.dibujar_enemigo(superficie, px, py, entidad, t)

    # R4.1: lo que no se ha explorado queda tapado por la niebla
    for x in range(juego.ancho):
        for y in range(juego.alto):
            if not escenario.revelada((x, y)):
                sprites.dibujar_niebla(superficie, x * r.TAMAÑO_CELDA, y * r.TAMAÑO_CELDA, t)

    hud.dibujar_hud(superficie, ancho_px, alto_px_mapa, personaje, juego.mensaje)
    if juego.terminado:
        hud.dibujar_final(superficie, ancho_px, alto_px_mapa + hud.ALTURA_HUD, juego.resultado, juego.texto_final)
