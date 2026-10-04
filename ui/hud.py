import pygame

ALTURA_HUD = 70
COLOR_FONDO_HUD = (15, 16, 22)
COLOR_BARRA_VIDA_FONDO = (60, 20, 20)
COLOR_BARRA_VIDA = (60, 200, 90)
COLOR_TEXTO = (230, 230, 230)
COLOR_MENSAJE = (240, 210, 60)

_fuente = None
_fuente_mensaje = None


def inicializar_fuentes() -> None:
    global _fuente, _fuente_mensaje
    _fuente = pygame.font.SysFont("arial", 18)
    _fuente_mensaje = pygame.font.SysFont("arial", 16, italic=True)


def dibujar_hud(superficie, ancho_ventana: int, y_offset: int, personaje, mensaje: str = "") -> None:
    # R8.1: interfaz que muestra vida, inventario y nivel
    pygame.draw.rect(superficie, COLOR_FONDO_HUD, (0, y_offset, ancho_ventana, ALTURA_HUD))

    barra_x, barra_y, barra_ancho, barra_alto = 10, y_offset + 10, 180, 18
    pygame.draw.rect(superficie, COLOR_BARRA_VIDA_FONDO, (barra_x, barra_y, barra_ancho, barra_alto))
    proporcion = max(0, personaje.vida) / personaje.vida_maxima if personaje.vida_maxima else 0
    pygame.draw.rect(superficie, COLOR_BARRA_VIDA, (barra_x, barra_y, int(barra_ancho * proporcion), barra_alto))
    texto_vida = _fuente.render(f"Vida: {personaje.vida}/{personaje.vida_maxima}", True, COLOR_TEXTO)
    superficie.blit(texto_vida, (barra_x, barra_y + barra_alto + 2))

    info = f"Nivel {personaje.nivel}   Puntos de commit: {personaje.puntos_commit}   Inventario: {len(personaje.inventario)}"
    texto_info = _fuente.render(info, True, COLOR_TEXTO)
    superficie.blit(texto_info, (barra_x + barra_ancho + 20, barra_y))

    if mensaje:
        texto_mensaje = _fuente_mensaje.render(mensaje, True, COLOR_MENSAJE)  # R8.2: retroalimentación de acciones
        superficie.blit(texto_mensaje, (barra_x, y_offset + ALTURA_HUD - 24))


def dibujar_final(superficie, ancho_px: int, alto_px: int, resultado: str, mensaje: str) -> None:
    overlay = pygame.Surface((ancho_px, alto_px))
    overlay.set_alpha(210)
    overlay.fill((10, 10, 15))
    superficie.blit(overlay, (0, 0))

    gano = resultado == "victoria"
    titulo_texto = "¡VICTORIA!" if gano else "GAME OVER"
    titulo_color = (120, 230, 150) if gano else (230, 90, 90)

    fuente_grande = pygame.font.SysFont("arial", 32, bold=True)
    titulo = fuente_grande.render(titulo_texto, True, titulo_color)
    superficie.blit(titulo, titulo.get_rect(center=(ancho_px // 2, alto_px // 2 - 30)))

    texto = _fuente.render(mensaje, True, COLOR_TEXTO)
    superficie.blit(texto, texto.get_rect(center=(ancho_px // 2, alto_px // 2 + 15)))

    texto_salir = _fuente_mensaje.render("Presiona R para reiniciar o ESC para salir", True, COLOR_MENSAJE)
    superficie.blit(texto_salir, texto_salir.get_rect(center=(ancho_px // 2, alto_px // 2 + 50)))
