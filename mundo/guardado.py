import json
import os
import sys
from abc import ABC, abstractmethod

CLAVE = "depuracion_partida"


class Almacen(ABC):
    # Strategy: dónde se guarda cambia según si el juego corre en el computador o en el navegador

    @abstractmethod
    def leer(self) -> str:
        pass

    @abstractmethod
    def escribir(self, texto: str) -> None:
        pass

    @abstractmethod
    def borrar(self) -> None:
        pass


class AlmacenArchivo(Almacen):

    def __init__(self, ruta: str):
        self._ruta = ruta

    def leer(self) -> str:
        if not os.path.exists(self._ruta):
            return ""
        with open(self._ruta, encoding="utf-8") as archivo:
            return archivo.read()

    def escribir(self, texto: str) -> None:
        with open(self._ruta, "w", encoding="utf-8") as archivo:
            archivo.write(texto)

    def borrar(self) -> None:
        if os.path.exists(self._ruta):
            os.remove(self._ruta)


class AlmacenNavegador(Almacen):
    # En la versión web (pygbag) se usa el localStorage del navegador

    def __init__(self):
        import platform
        self._storage = platform.window.localStorage

    def leer(self) -> str:
        return self._storage.getItem(CLAVE) or ""

    def escribir(self, texto: str) -> None:
        self._storage.setItem(CLAVE, texto)

    def borrar(self) -> None:
        self._storage.removeItem(CLAVE)


def almacen_por_defecto() -> Almacen:
    if sys.platform == "emscripten":
        return AlmacenNavegador()
    carpeta = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return AlmacenArchivo(os.path.join(carpeta, "partida_guardada.json"))


class Guardado:

    def __init__(self, almacen: Almacen = None):
        self._almacen = almacen or almacen_por_defecto()

    def guardar(self, juego) -> None:
        if juego.terminado:
            self.borrar()  # una partida terminada no se puede continuar
            return
        self._almacen.escribir(json.dumps(juego.a_dict(), ensure_ascii=False))

    def hay_partida(self) -> bool:
        return self.cargar() is not None

    def cargar(self):
        from mundo.juego import Juego
        texto = self._almacen.leer()
        if not texto:
            return None
        try:
            return Juego.desde_dict(json.loads(texto))
        except (ValueError, KeyError, TypeError):
            return None  # guardado viejo o dañado: se ignora

    def borrar(self) -> None:
        self._almacen.borrar()
