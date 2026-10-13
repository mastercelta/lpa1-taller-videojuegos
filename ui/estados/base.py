from abc import ABC, abstractmethod


class Estado(ABC):
    # R9.2: cada pantalla del juego es un estado. La aplicación solo conoce esta interfaz
    # y le delega eventos, actualización y dibujo (polimorfismo).

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

    @abstractmethod
    def dibujar(self, superficie) -> None:
        pass
