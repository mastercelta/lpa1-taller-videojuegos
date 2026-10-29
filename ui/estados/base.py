from abc import ABC, abstractmethod


class Estado(ABC):
    # R9.2: cada pantalla del juego es un estado. La aplicación solo conoce esta interfaz
    # y le delega eventos, actualización y dibujo (polimorfismo).

    pista = None  # música de la pantalla; None deja sonando la que venía

    def __init__(self, aplicacion):
        self._aplicacion = aplicacion

    @property
    def aplicacion(self):
        return self._aplicacion

    @abstractmethod
    def manejar_evento(self, evento) -> None:
        pass

    def actualizar(self, dt: float) -> None:
        pass

    def al_cerrar(self) -> None:
        pass  # la ventana se cierra; los estados con partida la guardan

    @abstractmethod
    def dibujar(self, superficie) -> None:
        pass
