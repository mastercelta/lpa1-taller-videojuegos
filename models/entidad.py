import random
from abc import ABC, abstractmethod


class Entidad(ABC):

    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int, x: int = 0, y: int = 0):
        self._nombre = nombre
        self._vida_maxima = vida
        self._vida = vida
        self._ataque = ataque
        self._defensa = defensa
        self._x = x
        self._y = y

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def vida(self) -> int:
        return self._vida

    @property
    def vida_maxima(self) -> int:
        return self._vida_maxima

    @property
    def ataque(self) -> int:
        return self._ataque

    @ataque.setter
    def ataque(self, value: int) -> None:
        if value < 0:
            raise ValueError("El ataque no puede ser negativo")
        self._ataque = value

    @property
    def defensa(self) -> int:
        return self._defensa

    @defensa.setter
    def defensa(self, value: int) -> None:
        if value < 0:
            raise ValueError("La defensa no puede ser negativa")
        self._defensa = value

    @property
    def posicion(self) -> tuple:
        return (self._x, self._y)

    def mover(self, dx: int, dy: int) -> None:
        self._x += dx
        self._y += dy

    def esta_vivo(self) -> bool:
        return self._vida > 0

    def recibir_daño(self, cantidad: int) -> int:
        daño_real = max(0, cantidad - self.defensa)
        self._vida = max(0, self._vida - daño_real)
        return daño_real

    def curar(self, cantidad: int) -> None:
        self._vida = min(self._vida_maxima, self._vida + cantidad)

    def intentar_esquivar(self, probabilidad: float = 0.2) -> bool:
        return random.random() < probabilidad  # R3.4: esquivar obstáculos del escenario

    @abstractmethod
    def describir(self) -> str:
        pass
