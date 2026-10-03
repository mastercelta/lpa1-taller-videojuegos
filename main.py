import pygame

from models.personaje import Personaje
from models.enemigo import Enemigo
from models.tesoro import Tesoro
from models.trampa_explosiva import TrampaExplosiva
from models.armamento import Armamento
from mundo.escenario import Escenario
from mundo.tienda import Tienda
from combate.combate import Combate
from ui import renderizador as r
from ui import hud


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


def manejar_interacciones(personaje, escenario, tienda) -> str:
    pos = personaje.posicion
    mensaje = ""

    enemigo = escenario.enemigos.get(pos)
    if enemigo is not None:
        for resultado in Combate.resolver_combate_enemigo(personaje, enemigo):
            print(f"{resultado['atacante']} ataca a {resultado['defensor']}: {resultado['daño']} de daño")
        if not enemigo.esta_vivo():
            escenario.quitar_enemigo(pos)
            personaje.ganar_puntos_commit(enemigo.puntos_commit_otorgados)
            subio = personaje.ganar_experiencia(enemigo.experiencia_otorgada)  # R6.1
            mensaje = f"Derrotaste a {enemigo.nombre} (+{enemigo.experiencia_otorgada} XP, +{enemigo.puntos_commit_otorgados} pts)"
            if subio:
                mensaje = f"¡Subiste a nivel {personaje.nivel}!"
        else:
            mensaje = f"Combate contra {enemigo.nombre}: vida {enemigo.vida}/{enemigo.vida_maxima}"

    objeto = escenario.objetos.get(pos)
    if objeto is not None:
        if isinstance(objeto, Tesoro):
            personaje.ganar_puntos_commit(objeto.valor_monetario)  # R3.2
            mensaje = f"Recogiste {objeto.nombre}: +{objeto.valor_monetario} puntos de commit"
        else:
            personaje.recolectar(objeto)  # R3.2
            mensaje = f"Recogiste {objeto.nombre}"
        escenario.quitar_objeto(pos)

    if escenario.en_zona_venta(*pos):
        mensaje = "Zona de venta: " + ", ".join(a.nombre for a in tienda.catalogo_para_nivel(personaje.nivel))

    return mensaje


def main() -> None:
    pygame.init()
    ancho, alto = 14, 10
    escenario = Escenario(ancho, alto)
    escenario.generar()
    escenario.distribuir_enemigos(crear_enemigos())
    escenario.distribuir_objetos(crear_objetos())

    personaje = Personaje("Estudiante", x=0, y=0)
    tienda = crear_tienda()

    alto_px_mapa = alto * r.TAMAÑO_CELDA
    ventana = pygame.display.set_mode((ancho * r.TAMAÑO_CELDA, alto_px_mapa + hud.ALTURA_HUD))
    pygame.display.set_caption("Depuración: El Sueño del Programador")
    hud.inicializar_fuentes()
    reloj = pygame.time.Clock()
    mensaje_actual = "Muévete con las flechas. Explora, combate y sube de nivel."

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if evento.key == pygame.K_UP:
                    dy = -1
                elif evento.key == pygame.K_DOWN:
                    dy = 1
                elif evento.key == pygame.K_LEFT:
                    dx = -1
                elif evento.key == pygame.K_RIGHT:
                    dx = 1
                elif evento.key == pygame.K_ESCAPE:
                    ejecutando = False

                if dx or dy:
                    nuevo_x = max(0, min(ancho - 1, personaje.posicion[0] + dx))
                    nuevo_y = max(0, min(alto - 1, personaje.posicion[1] + dy))
                    personaje.mover(nuevo_x - personaje.posicion[0], nuevo_y - personaje.posicion[1])
                    escenario.visitar(*personaje.posicion)
                    resultado = manejar_interacciones(personaje, escenario, tienda)
                    if resultado:
                        mensaje_actual = resultado  # R8.2: retroalimentación de la última acción

        r.dibujar_grilla(ventana, ancho, alto)
        r.dibujar_zona_venta(ventana, escenario.zona_venta)
        for pos, objeto in escenario.objetos.items():
            r.dibujar_objeto(ventana, pos, objeto)
        for pos, enemigo in escenario.enemigos.items():
            r.dibujar_enemigo(ventana, pos, enemigo)
        r.dibujar_personaje(ventana, personaje.posicion)
        hud.dibujar_hud(ventana, ancho * r.TAMAÑO_CELDA, alto_px_mapa, personaje, mensaje_actual)

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
