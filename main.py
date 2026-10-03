import pygame

from models.personaje import Personaje
from models.enemigo import Enemigo
from models.tesoro import Tesoro
from models.trampa_explosiva import TrampaExplosiva
from models.armamento import Armamento
from mundo.escenario import Escenario
from mundo.tienda import Tienda
from ui import renderizador as r


def crear_enemigos() -> list:
    return [
        Enemigo("NullPointer", vida=20, ataque=6, defensa=1, tipo="terrestre", experiencia_otorgada=20, puntos_commit_otorgados=15),
        Enemigo("Bucle Infinito", vida=25, ataque=5, defensa=2, tipo="terrestre", experiencia_otorgada=25, puntos_commit_otorgados=20),
        Enemigo("Variable Global", vida=18, ataque=7, defensa=0, tipo="terrestre", experiencia_otorgada=18, puntos_commit_otorgados=12),
        Enemigo("Memory Leak", vida=15, ataque=4, defensa=0, tipo="volador", experiencia_otorgada=22, puntos_commit_otorgados=18),
    ]


def crear_objetos() -> list:
    return [
        Tesoro("Fragmento de código limpio", valor_monetario=30),
        Tesoro("Café", valor_monetario=15),
        TrampaExplosiva("SyntaxError", alcance_explosion=1, daño_explosion=12),
    ]


def crear_tienda() -> Tienda:
    return Tienda([
        Armamento("Debugger", aumento_ataque=5, aumento_defensa=2, precio_compra=50, precio_venta=20, nivel_requerido=1),
        Armamento("Stack Trace", aumento_ataque=10, aumento_defensa=3, precio_compra=120, precio_venta=50, nivel_requerido=3),
        Armamento("Refactorizador", aumento_ataque=20, aumento_defensa=8, precio_compra=250, precio_venta=100, nivel_requerido=5),
    ])


def main() -> None:
    pygame.init()
    ancho, alto = 14, 10
    escenario = Escenario(ancho, alto)
    escenario.generar()
    escenario.distribuir_enemigos(crear_enemigos())
    escenario.distribuir_objetos(crear_objetos())

    personaje = Personaje("Estudiante", x=0, y=0)
    tienda = crear_tienda()

    ventana = pygame.display.set_mode((ancho * r.TAMAÑO_CELDA, alto * r.TAMAÑO_CELDA))
    pygame.display.set_caption("Depuración: El Sueño del Programador")
    reloj = pygame.time.Clock()

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        r.dibujar_grilla(ventana, ancho, alto)
        r.dibujar_zona_venta(ventana, escenario.zona_venta)
        for pos, objeto in escenario.objetos.items():
            r.dibujar_objeto(ventana, pos, objeto)
        for pos, enemigo in escenario.enemigos.items():
            r.dibujar_enemigo(ventana, pos, enemigo)
        r.dibujar_personaje(ventana, personaje.posicion)

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
