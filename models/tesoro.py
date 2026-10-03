from .objeto import Objeto


class Tesoro(Objeto):

    def __init__(self, nombre: str, valor_monetario: int, descripcion: str = ""):
        super().__init__(nombre, descripcion)
        self._valor_monetario = valor_monetario  # R2.2

    @property
    def valor_monetario(self) -> int:
        return self._valor_monetario

    def describir(self) -> str:
        return f"{self.nombre} - Valor: {self.valor_monetario} puntos de commit"
