from ui.renderizador import TAMAÑO_CELDA


class Animador:
    # R10.1: guarda una posición visual en píxeles por entidad y la acerca suavemente
    # a su celda real, para que el movimiento se vea fluido aunque la lógica sea por celdas.

    SUAVIDAD = 14.0  # más alto = llega más rápido a la celda destino

    def __init__(self):
        self._posiciones = {}
        self._en_movimiento = set()
        self._tiempo = 0.0

    @property
    def tiempo(self) -> float:
        return self._tiempo

    def actualizar(self, dt: float, juego) -> None:
        self._tiempo += dt
        objetivos = {juego.personaje: juego.personaje.posicion}
        for celda, enemigo in juego.escenario.enemigos.items():
            objetivos[enemigo] = celda

        factor = min(1.0, dt * self.SUAVIDAD)
        nuevas = {}
        self._en_movimiento = set()
        for entidad, celda in objetivos.items():
            destino = (celda[0] * TAMAÑO_CELDA, celda[1] * TAMAÑO_CELDA)
            actual = self._posiciones.get(entidad, destino)
            x = actual[0] + (destino[0] - actual[0]) * factor
            y = actual[1] + (destino[1] - actual[1]) * factor
            if abs(destino[0] - x) < 0.5 and abs(destino[1] - y) < 0.5:
                x, y = destino
            else:
                self._en_movimiento.add(entidad)
            nuevas[entidad] = (x, y)
        self._posiciones = nuevas

    def posicion(self, entidad, celda: tuple) -> tuple:
        return self._posiciones.get(entidad, (celda[0] * TAMAÑO_CELDA, celda[1] * TAMAÑO_CELDA))

    def caminando(self, entidad) -> bool:
        return entidad in self._en_movimiento
