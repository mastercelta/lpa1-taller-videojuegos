from abc import ABC, abstractmethod


class Objeto(ABC):

    def __init__(self, nombre: str, descripcion: str = ""):
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @abstractmethod
    def describir(self) -> str:
        pass
