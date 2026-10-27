import pygame

from ui.estados.base import Estado

COLOR_TITULO = (240, 210, 60)
COLOR_TEXTO = (210, 215, 225)
COLOR_APAGADO = (110, 115, 125)
COLOR_SELECCION = (120, 230, 150)
COLOR_MENSAJE = (240, 210, 60)


class EstadoTienda(Estado):
    # R3.3, R4.3: se abre encima de la partida, que queda en pausa mientras se compra

    PESTAÑAS = ("Comprar", "Mi inventario")

    def __init__(self, aplicacion, estado_jugando):
        super().__init__(aplicacion)
        self._estado_jugando = estado_jugando
        self._pestaña = 0
        self._seleccion = 0
        self._aviso = "Flechas: elegir · Enter: comprar/equipar · V: vender · ESC: salir"
        self._fuente_titulo = pygame.font.SysFont("arial", 30, bold=True)
        self._fuente = pygame.font.SysFont("arial", 19)
        self._fuente_chica = pygame.font.SysFont("arial", 15, italic=True)

    @property
    def juego(self):
        return self._estado_jugando.juego

    @property
    def pestaña(self) -> str:
        return self.PESTAÑAS[self._pestaña]

    def elementos(self) -> list:
        if self._pestaña == 0:
            return self.juego.tienda.catalogo
        return self.juego.armas_en_inventario()

    def manejar_evento(self, evento) -> None:
        if evento.type != pygame.KEYDOWN:
            return
        elementos = self.elementos()
        if evento.key in (pygame.K_ESCAPE, pygame.K_t):
            self.aplicacion.cambiar_estado(self._estado_jugando)
        elif evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
            self._pestaña = 1 - self._pestaña
            self._seleccion = 0
        elif evento.key in (pygame.K_UP, pygame.K_DOWN) and elementos:
            paso = -1 if evento.key == pygame.K_UP else 1
            self._seleccion = (self._seleccion + paso) % len(elementos)
        elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE) and elementos:
            arma = elementos[self._seleccion]
            self._aviso = self.juego.comprar(arma) if self._pestaña == 0 else self.juego.equipar(arma)
        elif evento.key == pygame.K_v and self._pestaña == 1 and elementos:
            self._aviso = self.juego.vender(elementos[self._seleccion])
        self._seleccion = min(self._seleccion, max(0, len(self.elementos()) - 1))
        self._estado_jugando.reproducir_eventos()

    def dibujar(self, superficie) -> None:
        self._estado_jugando.dibujar(superficie)
        ancho, alto = superficie.get_size()
        velo = pygame.Surface((ancho, alto))
        velo.set_alpha(235)
        velo.fill((10, 10, 15))
        superficie.blit(velo, (0, 0))

        titulo = self._fuente_titulo.render("Tienda del Stack Overflow", True, COLOR_TITULO)
        superficie.blit(titulo, titulo.get_rect(center=(ancho // 2, 40)))
        personaje = self.juego.personaje
        datos = f"Puntos de commit: {personaje.puntos_commit}   Nivel: {personaje.nivel}   Ataque: {personaje.ataque}   Defensa: {personaje.defensa}"
        texto = self._fuente.render(datos, True, COLOR_TEXTO)
        superficie.blit(texto, texto.get_rect(center=(ancho // 2, 80)))

        for i, nombre in enumerate(self.PESTAÑAS):
            color = COLOR_SELECCION if i == self._pestaña else COLOR_APAGADO
            etiqueta = self._fuente.render(f"[ {nombre} ]" if i == self._pestaña else nombre, True, color)
            superficie.blit(etiqueta, etiqueta.get_rect(center=(ancho // 2 + (i * 2 - 1) * 120, 120)))

        elementos = self.elementos()
        if not elementos:
            vacio = self._fuente.render("No tienes armas en el inventario", True, COLOR_APAGADO)
            superficie.blit(vacio, vacio.get_rect(center=(ancho // 2, 170)))
        for i, arma in enumerate(elementos):
            elegida = i == self._seleccion
            bloqueada = self._pestaña == 0 and arma.nivel_requerido > personaje.nivel
            color = COLOR_SELECCION if elegida else (COLOR_APAGADO if bloqueada else COLOR_TEXTO)
            precio = f"{arma.precio_compra} pts" if self._pestaña == 0 else f"vende en {arma.precio_venta} pts"
            linea = f"{'> ' if elegida else '  '}{arma.nombre}  +{arma.aumento_ataque} atq  +{arma.aumento_defensa} def  ·  {precio}"
            if bloqueada:
                linea += f"  (nivel {arma.nivel_requerido})"
            superficie.blit(self._fuente.render(linea, True, color), (60, 160 + i * 34))

        aviso = self._fuente_chica.render(self._aviso, True, COLOR_MENSAJE)
        superficie.blit(aviso, aviso.get_rect(center=(ancho // 2, 320)))
