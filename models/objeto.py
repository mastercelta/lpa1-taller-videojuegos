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

    def a_dict(self) -> dict:
        # Autosave: cada subclase agrega sus propios datos (polimorfismo)
        return {"clase": type(self).__name__, "nombre": self._nombre, "descripcion": self._descripcion}

    @abstractmethod
    def describir(self) -> str:
        pass
