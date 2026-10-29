import random

RADIO_VISION = 2


class Escenario:

    def __init__(self, ancho: int, alto: int):
        self._ancho = ancho
        self._alto = alto
        self._enemigos = {}  # posicion (x, y) -> Enemigo
        self._objetos = {}  # posicion (x, y) -> Objeto
        self._zona_venta = None
        self._reservadas = set()
        self._celdas_visitadas = set()
        self._celdas_reveladas = set()
        self._obstaculos = set()

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
    def obstaculos(self) -> set:
        return self._obstaculos.copy()

    @property
    def zona_venta(self) -> tuple:
        return self._zona_venta

    def _posicion_libre_aleatoria(self) -> tuple:
        while True:
            pos = (random.randint(0, self._ancho - 1), random.randint(0, self._alto - 1))
            if pos not in self._enemigos and pos not in self._objetos and pos != self._zona_venta and pos not in self._reservadas and pos not in self._obstaculos:
                return pos

    def generar(self, zona_venta: tuple = None, reservadas: tuple = ()) -> None:
        # R4.1: generación del escenario con área explorable desconocida
        self._enemigos = {}
        self._objetos = {}
        self._celdas_visitadas = set()
        self._celdas_reveladas = set()
        self._obstaculos = set()
        self._reservadas = set(reservadas)
        self._zona_venta = zona_venta or (self._ancho // 2, self._alto // 2)  # R4.3: zona de venta

    def distribuir_enemigos(self, enemigos: list) -> None:
        for enemigo in enemigos:
            pos = self._posicion_libre_aleatoria()  # R4.2: ubicación aleatoria
            self._enemigos[pos] = enemigo

    def distribuir_objetos(self, objetos: list) -> None:
        for objeto in objetos:
            pos = self._posicion_libre_aleatoria()  # R4.2: ubicación aleatoria
            self._objetos[pos] = objeto

    def colocar_obstaculos(self, cantidad: int) -> None:
        # R3.4: bloques de código comentado que no se pueden atravesar caminando
        colocados = 0
        while colocados < cantidad:
            pos = self._posicion_libre_aleatoria()
            self._obstaculos.add(pos)
            if self._todo_conectado():
                colocados += 1
            else:
                self._obstaculos.discard(pos)

    def _todo_conectado(self) -> bool:
        libres = {(x, y) for x in range(self._ancho) for y in range(self._alto)} - self._obstaculos
        inicio = next(iter(libres))
        vistos, pendientes = {inicio}, [inicio]
        while pendientes:
            x, y = pendientes.pop()
            for vecino in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if vecino in libres and vecino not in vistos:
                    vistos.add(vecino)
                    pendientes.append(vecino)
        return vistos == libres

    def quitar_obstaculo(self, pos: tuple) -> None:
        self._obstaculos.discard(pos)

    def es_obstaculo(self, pos: tuple) -> bool:
        return pos in self._obstaculos

    def visitar(self, x: int, y: int) -> None:
        self._celdas_visitadas.add((x, y))
        for dx in range(-RADIO_VISION, RADIO_VISION + 1):
            for dy in range(-RADIO_VISION, RADIO_VISION + 1):
                self._celdas_reveladas.add((x + dx, y + dy))  # R4.1: lo demás sigue en la niebla

    def revelada(self, pos: tuple) -> bool:
        return pos in self._celdas_reveladas

    def porcentaje_explorado(self) -> float:
        total = self._ancho * self._alto - len(self._obstaculos)
        return len(self._celdas_visitadas) / total if total else 0.0

    def colocar_jefe(self, jefe, pos: tuple) -> None:
        self._enemigos.pop(pos, None)
        self._objetos.pop(pos, None)
        self._enemigos[pos] = jefe  # posición fija: el jefe no se mezcla con la distribución aleatoria

    def dentro(self, pos: tuple) -> bool:
        return 0 <= pos[0] < self._ancho and 0 <= pos[1] < self._alto

    def puede_ocupar(self, pos: tuple, vuela: bool = False) -> bool:
        # R10.2: los voladores pasan por encima de objetos y de la tienda; los terrestres no
        if not self.dentro(pos) or pos in self._enemigos:
            return False
        if vuela:
            return True
        return pos not in self._objetos and pos != self._zona_venta and pos not in self._obstaculos

    def mover_enemigo(self, desde: tuple, hasta: tuple) -> None:
        enemigo = self._enemigos.pop(desde)
        self._enemigos[hasta] = enemigo
        enemigo.mirar(hasta[0] - desde[0], hasta[1] - desde[1])

    def colocar_objeto(self, objeto, pos: tuple) -> None:
        self._objetos[pos] = objeto

    def quitar_enemigo(self, pos: tuple) -> None:
        self._enemigos.pop(pos, None)

    def quitar_objeto(self, pos: tuple) -> None:
        self._objetos.pop(pos, None)

    def en_zona_venta(self, x: int, y: int) -> bool:
        return (x, y) == self._zona_venta

    def a_dict(self) -> dict:
        lista = lambda celdas: [list(c) for c in sorted(celdas)]
        return {
            "ancho": self._ancho, "alto": self._alto,
            "zona_venta": list(self._zona_venta),
            "reservadas": lista(self._reservadas),
            "visitadas": lista(self._celdas_visitadas),
            "reveladas": lista(self._celdas_reveladas),
            "obstaculos": lista(self._obstaculos),
            "enemigos": [e.a_dict() | {"celda": list(p)} for p, e in self._enemigos.items()],
            "objetos": [o.a_dict() | {"celda": list(p)} for p, o in self._objetos.items()],
        }

    def restaurar(self, datos: dict) -> None:
        from models.fabrica import enemigo_desde_dict, objeto_desde_dict
        conjunto = lambda celdas: {tuple(c) for c in celdas}
        self._zona_venta = tuple(datos["zona_venta"])
        self._reservadas = conjunto(datos["reservadas"])
        self._celdas_visitadas = conjunto(datos["visitadas"])
        self._celdas_reveladas = conjunto(datos["reveladas"])
        self._obstaculos = conjunto(datos["obstaculos"])
        self._enemigos = {}
        for d in datos["enemigos"]:
            d = dict(d)
            celda = tuple(d.pop("celda"))
            self._enemigos[celda] = enemigo_desde_dict(d)
        self._objetos = {}
        for d in datos["objetos"]:
            d = dict(d)
            celda = tuple(d.pop("celda"))
            self._objetos[celda] = objeto_desde_dict(d)
