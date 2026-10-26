from .comportamiento import Patrullar, Perseguir
from .entidad import Entidad

TIPOS_VALIDOS = ("terrestre", "volador")


class Enemigo(Entidad):

    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int, tipo: str,
                 experiencia_otorgada: int = 10, puntos_commit_otorgados: int = 5, x: int = 0, y: int = 0):
        super().__init__(nombre, vida, ataque, defensa, x, y)
        if tipo not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido: {tipo}. Debe ser uno de {TIPOS_VALIDOS}")
        self._tipo = tipo  # R1.2: tipo "volador" o "terrestre"
        self._experiencia_otorgada = experiencia_otorgada
        self._puntos_commit_otorgados = puntos_commit_otorgados
        self._comportamiento = self.comportamiento_por_defecto()  # R10.2

    def comportamiento_por_defecto(self):
        # Los terrestres patrullan; los voladores persiguen al jugador cercano.
        # Una subclase puede sobrescribir este método para cambiar cómo se mueve.
        if self._tipo == "volador":
            return Perseguir(radio=4)
        return Patrullar(horizontal=True)

    @property
    def comportamiento(self):
        return self._comportamiento

    @comportamiento.setter
    def comportamiento(self, valor) -> None:
        self._comportamiento = valor

    @property
    def vuela(self) -> bool:
        return self._tipo == "volador"

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def experiencia_otorgada(self) -> int:
        return self._experiencia_otorgada

    @property
    def puntos_commit_otorgados(self) -> int:
        return self._puntos_commit_otorgados

    def describir(self) -> str:
        return f"{self.nombre} ({self.tipo}) - Vida: {self.vida}/{self.vida_maxima} | Ataque: {self.ataque} | Defensa: {self.defensa}"
