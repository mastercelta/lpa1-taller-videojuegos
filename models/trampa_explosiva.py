from .objeto import Objeto


class TrampaExplosiva(Objeto):

    def __init__(self, nombre: str, alcance_explosion: int, daño_explosion: int, descripcion: str = ""):
        super().__init__(nombre, descripcion)
        self._alcance_explosion = alcance_explosion  # R2.1
        self._daño_explosion = daño_explosion  # R2.1

    @property
    def alcance_explosion(self) -> int:
        return self._alcance_explosion

    @property
    def daño_explosion(self) -> int:
        return self._daño_explosion

    def explotar(self, objetivos: list) -> dict:
        resultados = {}
        for objetivo in objetivos:
            resultados[objetivo.nombre] = objetivo.recibir_daño(self.daño_explosion)  # R5.3: efecto especial
        return resultados

    def describir(self) -> str:
        return f"{self.nombre} - Alcance: {self.alcance_explosion} | Daño: {self.daño_explosion}"
