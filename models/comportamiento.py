from abc import ABC, abstractmethod


def distancia(a: tuple, b: tuple) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Comportamiento(ABC):
    # R10.2: cómo se mueve un enemigo. Cada estrategia decide el siguiente paso (dx, dy)
    # y el juego solo llama a decidir(), sin saber cuál es (polimorfismo).

    @abstractmethod
    def decidir(self, desde: tuple, jugador: tuple, puede_ir) -> tuple:
        pass


class Quieto(Comportamiento):
    # Guardia: no se mueve, espera a que el jugador llegue

    def decidir(self, desde: tuple, jugador: tuple, puede_ir) -> tuple:
        return (0, 0)


class Patrullar(Comportamiento):
    # Va y viene en línea recta; al chocar con algo da media vuelta

    def __init__(self, horizontal: bool = True):
        self._horizontal = horizontal
        self._sentido = 1

    def decidir(self, desde: tuple, jugador: tuple, puede_ir) -> tuple:
        for _ in range(2):
            paso = (self._sentido, 0) if self._horizontal else (0, self._sentido)
            destino = (desde[0] + paso[0], desde[1] + paso[1])
            if destino == jugador or puede_ir(destino):
                return paso
            self._sentido *= -1
        return (0, 0)


class Perseguir(Comportamiento):
    # Si el jugador está dentro del radio, se acerca un paso por el eje más largo

    def __init__(self, radio: int = 4):
        self._radio = radio

    @property
    def radio(self) -> int:
        return self._radio

    def decidir(self, desde: tuple, jugador: tuple, puede_ir) -> tuple:
        if distancia(desde, jugador) > self._radio:
            return (0, 0)
        dx = (jugador[0] > desde[0]) - (jugador[0] < desde[0])
        dy = (jugador[1] > desde[1]) - (jugador[1] < desde[1])
        opciones = [(dx, 0), (0, dy)] if abs(jugador[0] - desde[0]) >= abs(jugador[1] - desde[1]) else [(0, dy), (dx, 0)]
        for paso in opciones:
            if paso == (0, 0):
                continue
            destino = (desde[0] + paso[0], desde[1] + paso[1])
            if destino == jugador or puede_ir(destino):
                return paso
        return (0, 0)
