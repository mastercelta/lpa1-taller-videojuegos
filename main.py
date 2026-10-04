import pygame

from mundo.juego import Juego
from ui import hud
from ui.vista import dibujar_juego, tamaño_ventana

TECLAS_MOVIMIENTO = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def main() -> None:
    pygame.init()
    juego = Juego()
    ventana = pygame.display.set_mode(tamaño_ventana(juego))
    pygame.display.set_caption("Depuración: El Sueño del Programador")
    hud.inicializar_fuentes()
    reloj = pygame.time.Clock()

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_r and juego.terminado:
                    juego = Juego()
                elif evento.key in TECLAS_MOVIMIENTO:
                    juego.mover(*TECLAS_MOVIMIENTO[evento.key])

        dibujar_juego(ventana, juego)
        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
