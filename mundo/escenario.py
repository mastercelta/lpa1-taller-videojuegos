import random


class Escenario:

    def __init__(self, ancho: int, alto: int):
        self._ancho = ancho
        self._alto = alto
        self._enemigos = {}  # posicion (x, y) -> Enemigo
        self._objetos = {}  # posicion (x, y) -> Objeto
        self._zona_venta = None
        self._celdas_visitadas = set()

    @property
    def ancho(self) -> int:
        return self._ancho

    @property
    def alto(self) -> int:
        return self._alto

    @property
    def enemigos(self) -> dict:
        return self._enemigos.copy()

    @property
    def objetos(self) -> dict:
        return self._objetos.copy()

    @property
    def zona_venta(self) -> tuple:
        return self._zona_venta

    def _posicion_libre_aleatoria(self) -> tuple:
        while True:
            pos = (random.randint(0, self._ancho - 1), random.randint(0, self._alto - 1))
            if pos not in self._enemigos and pos not in self._objetos and pos != self._zona_venta:
                return pos

    def generar(self, zona_venta: tuple = None) -> None:
        # R4.1: generación del escenario con área explorable desconocida
        self._enemigos = {}
        self._objetos = {}
        self._celdas_visitadas = set()
        self._zona_venta = zona_venta or (self._ancho // 2, self._alto // 2)  # R4.3: zona de venta

    def distribuir_enemigos(self, enemigos: list) -> None:
        for enemigo in enemigos:
            pos = self._posicion_libre_aleatoria()  # R4.2: ubicación aleatoria
            self._enemigos[pos] = enemigo

    def distribuir_objetos(self, objetos: list) -> None:
        for objeto in objetos:
            pos = self._posicion_libre_aleatoria()  # R4.2: ubicación aleatoria
            self._objetos[pos] = objeto

    def visitar(self, x: int, y: int) -> None:
        self._celdas_visitadas.add((x, y))

    def porcentaje_explorado(self) -> float:
        total = self._ancho * self._alto
        return len(self._celdas_visitadas) / total if total else 0.0

    def quitar_enemigo(self, pos: tuple) -> None:
        self._enemigos.pop(pos, None)

    def quitar_objeto(self, pos: tuple) -> None:
        self._objetos.pop(pos, None)

    def en_zona_venta(self, x: int, y: int) -> bool:
        return (x, y) == self._zona_venta
