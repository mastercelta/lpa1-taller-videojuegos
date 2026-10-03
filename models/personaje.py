from .entidad import Entidad


class Personaje(Entidad):

    def __init__(self, nombre: str, vida: int = 100, ataque: int = 10, defensa: int = 5, x: int = 0, y: int = 0):
        super().__init__(nombre, vida, ataque, defensa, x, y)
        self._nivel = 1
        self._experiencia = 0
        self._experiencia_siguiente_nivel = 100
        self._inventario = []
        self._puntos_commit = 0
        self._armamento_equipado = []

    @property
    def nivel(self) -> int:
        return self._nivel

    @property
    def experiencia(self) -> int:
        return self._experiencia

    @property
    def inventario(self) -> list:
        return self._inventario.copy()

    @property
    def puntos_commit(self) -> int:
        return self._puntos_commit

    def recolectar(self, objeto) -> None:
        self._inventario.append(objeto)  # R3.2: recolección de objetos

    def quitar_del_inventario(self, objeto) -> bool:
        if objeto in self._inventario:
            self._inventario.remove(objeto)
            return True
        return False

    def ganar_puntos_commit(self, cantidad: int) -> None:
        self._puntos_commit += cantidad

    def gastar_puntos_commit(self, cantidad: int) -> bool:
        if cantidad > self._puntos_commit:
            return False
        self._puntos_commit -= cantidad
        return True

    def ganar_experiencia(self, cantidad: int) -> bool:
        self._experiencia += cantidad  # R6.1: experiencia al derrotar enemigos o recolectar objetos
        subio_nivel = False
        while self._experiencia >= self._experiencia_siguiente_nivel:
            self._experiencia -= self._experiencia_siguiente_nivel
            self._subir_nivel()
            subio_nivel = True
        return subio_nivel

    def _subir_nivel(self) -> None:
        self._nivel += 1
        self._vida_maxima += 20  # R6.2: mejora de atributos al subir de nivel
        self._vida = self._vida_maxima
        self.ataque += 5
        self.defensa += 2
        self._experiencia_siguiente_nivel = int(self._experiencia_siguiente_nivel * 1.3)

    def nombres_armas_equipadas(self) -> list:
        return [a.nombre for a in self._armamento_equipado]

    def equipar(self, armamento) -> None:
        self._armamento_equipado.append(armamento)  # R6.3: acceso a nuevo equipamiento
        self.ataque += armamento.aumento_ataque
        self.defensa += armamento.aumento_defensa
        if armamento in self._inventario:
            self._inventario.remove(armamento)

    def describir(self) -> str:
        return f"{self.nombre} - Nivel {self.nivel} | Vida: {self.vida}/{self.vida_maxima} | Ataque: {self.ataque} | Defensa: {self.defensa}"
