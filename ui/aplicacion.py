import pygame


class Aplicacion:
    # Máquina de estados: guarda el estado actual y cambia entre pantallas (R9.2)

    def __init__(self, tamaño: tuple, titulo: str):
        self._tamaño = tamaño
        self._titulo = titulo
        self._estado = None
        self._ejecutando = False

    @property
    def tamaño(self) -> tuple:
        return self._tamaño

    @property
    def estado(self):
        return self._estado

    @property
    def ejecutando(self) -> bool:
        return self._ejecutando

    def cambiar_estado(self, nuevo_estado) -> None:
        self._estado = nuevo_estado

    def salir(self) -> None:
        self._ejecutando = False

    def procesar(self, eventos: list, dt: float, superficie) -> None:
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.salir()
                return
            self._estado.manejar_evento(evento)
        self._estado.actualizar(dt)
        self._estado.dibujar(superficie)

    def ejecutar(self, crear_estado_inicial) -> None:
        pygame.init()
        ventana = pygame.display.set_mode(self._tamaño)
        pygame.display.set_caption(self._titulo)
        reloj = pygame.time.Clock()
        self._estado = crear_estado_inicial(self)
        self._ejecutando = True
        while self._ejecutando:
            dt = reloj.tick(60) / 1000
            self.procesar(pygame.event.get(), dt, ventana)
            pygame.display.flip()
        pygame.quit()
