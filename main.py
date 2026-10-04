import pygame

from models.personaje import Personaje
from models.enemigo import Enemigo
from models.enemigo_bug import EnemigoNullPointer, EnemigoBucleInfinito, EnemigoVariableGlobal, EnemigoMemoryLeak, EnemigoJefe
from models.tesoro import Tesoro
from models.trampa_explosiva import TrampaExplosiva
from models.armamento import Armamento
from mundo.escenario import Escenario
from mundo.tienda import Tienda
from mundo.contenido import crear_enemigos, crear_objetos, crear_jefe, crear_tienda
from combate.combate import Combate
from mundo.victoria import verificar_victoria
from ui import renderizador as r
from ui import hud


def manejar_interacciones(personaje, escenario, tienda) -> str:
    pos = personaje.posicion
    mensaje = ""

    enemigo = escenario.enemigos.get(pos)
    if enemigo is not None:
        for resultado in Combate.resolver_combate_enemigo(personaje, enemigo):
            extra = f" ¡debilidad explotada con {resultado['debilidad_explotada']}!" if resultado["debilidad_explotada"] else ""
            print(f"{resultado['atacante']} ataca a {resultado['defensor']}: {resultado['daño']} de daño{extra}")
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

    jefe = crear_jefe()
    escenario.colocar_jefe(jefe, (ancho - 1, alto - 1))  # posición fija: encuentro final reconocible

    personaje = Personaje("Estudiante", x=0, y=0)
    tienda = crear_tienda()

    alto_px_mapa = alto * r.TAMAÑO_CELDA
    ventana = pygame.display.set_mode((ancho * r.TAMAÑO_CELDA, alto_px_mapa + hud.ALTURA_HUD))
    pygame.display.set_caption("Depuración: El Sueño del Programador")
    hud.inicializar_fuentes()
    reloj = pygame.time.Clock()
    mensaje_actual = "Muévete con las flechas. Explora, combate y sube de nivel."
    mensaje_victoria = ""

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

                if not mensaje_victoria and (dx or dy):
                    nuevo_x = max(0, min(ancho - 1, personaje.posicion[0] + dx))
                    nuevo_y = max(0, min(alto - 1, personaje.posicion[1] + dy))
                    personaje.mover(nuevo_x - personaje.posicion[0], nuevo_y - personaje.posicion[1])
                    escenario.visitar(*personaje.posicion)
                    resultado = manejar_interacciones(personaje, escenario, tienda)
                    if resultado:
                        mensaje_actual = resultado  # R8.2: retroalimentación de la última acción
                    mensaje_victoria = verificar_victoria(personaje, escenario, jefe)  # R7.1, R7.2, R7.3

        r.dibujar_grilla(ventana, ancho, alto)
        r.dibujar_zona_venta(ventana, escenario.zona_venta)
        for pos, objeto in escenario.objetos.items():
            r.dibujar_objeto(ventana, pos, objeto)
        for pos, enemigo in escenario.enemigos.items():
            r.dibujar_enemigo(ventana, pos, enemigo)
        r.dibujar_personaje(ventana, personaje.posicion)
        hud.dibujar_hud(ventana, ancho * r.TAMAÑO_CELDA, alto_px_mapa, personaje, mensaje_actual)
        if mensaje_victoria:
            hud.dibujar_victoria(ventana, ancho * r.TAMAÑO_CELDA, alto_px_mapa + hud.ALTURA_HUD, mensaje_victoria)

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
