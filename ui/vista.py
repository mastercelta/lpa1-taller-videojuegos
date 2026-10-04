from ui import hud
from ui import renderizador as r


def tamaño_ventana(juego) -> tuple:
    return (juego.ancho * r.TAMAÑO_CELDA, juego.alto * r.TAMAÑO_CELDA + hud.ALTURA_HUD)


def dibujar_juego(superficie, juego) -> None:
    escenario = juego.escenario
    ancho_px = juego.ancho * r.TAMAÑO_CELDA
    alto_px_mapa = juego.alto * r.TAMAÑO_CELDA

    r.dibujar_grilla(superficie, juego.ancho, juego.alto)
    r.dibujar_zona_venta(superficie, escenario.zona_venta)
    for pos, objeto in escenario.objetos.items():
        r.dibujar_objeto(superficie, pos, objeto)
    for pos, enemigo in escenario.enemigos.items():
        r.dibujar_enemigo(superficie, pos, enemigo)
    r.dibujar_personaje(superficie, juego.personaje.posicion)
    hud.dibujar_hud(superficie, ancho_px, alto_px_mapa, juego.personaje, juego.mensaje)
    if juego.terminado:
        hud.dibujar_final(superficie, ancho_px, alto_px_mapa + hud.ALTURA_HUD, juego.resultado, juego.texto_final)
