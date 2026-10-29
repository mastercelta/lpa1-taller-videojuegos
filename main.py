import asyncio

from mundo.juego import Juego
from ui.aplicacion import Aplicacion
from ui.estados.menu import EstadoMenu
from ui.vista import tamaño_ventana


async def main() -> None:
    aplicacion = Aplicacion(tamaño_ventana(Juego()), "Depuración: El Sueño del Programador")
    await aplicacion.ejecutar(EstadoMenu)  # R9.1: el juego inicia en la pantalla principal


if __name__ == "__main__":
    asyncio.run(main())
