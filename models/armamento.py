from .objeto import Objeto


class Armamento(Objeto):

    def __init__(self, nombre: str, aumento_ataque: int, aumento_defensa: int,
                 precio_compra: int, precio_venta: int, nivel_requerido: int = 1, descripcion: str = ""):
        super().__init__(nombre, descripcion)
        self._aumento_ataque = aumento_ataque  # R2.3
        self._aumento_defensa = aumento_defensa  # R2.3
        self._precio_compra = precio_compra  # R2.3
        self._precio_venta = precio_venta  # R2.3
        self._nivel_requerido = nivel_requerido  # R6.3: acceso a nuevo equipamiento por nivel

    @property
    def aumento_ataque(self) -> int:
        return self._aumento_ataque

    @property
    def aumento_defensa(self) -> int:
        return self._aumento_defensa

    @property
    def precio_compra(self) -> int:
        return self._precio_compra

    @property
    def precio_venta(self) -> int:
        return self._precio_venta

    @property
    def nivel_requerido(self) -> int:
        return self._nivel_requerido

    def describir(self) -> str:
        return f"{self.nombre} - Atq +{self.aumento_ataque} / Def +{self.aumento_defensa} | Compra: {self.precio_compra} | Venta: {self.precio_venta} | Nivel req: {self.nivel_requerido}"
