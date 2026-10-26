from models.enemigo import Enemigo
from models.enemigo_bug import EnemigoNullPointer, EnemigoBucleInfinito, EnemigoVariableGlobal, EnemigoMemoryLeak, EnemigoJefe
from models.tesoro import Tesoro
from models.trampa_explosiva import TrampaExplosiva
from models.armamento import Armamento
from mundo.tienda import Tienda


def crear_enemigos() -> list:
    return [
        # Estos tres heredan su debilidad ("Debugger") de EnemigoBug sin redefinirla
        EnemigoNullPointer("NullPointer", vida=20, ataque=6, defensa=1, tipo="terrestre", experiencia_otorgada=20, puntos_commit_otorgados=15),
        EnemigoBucleInfinito("Bucle Infinito", vida=25, ataque=5, defensa=2, tipo="terrestre", experiencia_otorgada=25, puntos_commit_otorgados=20),
        EnemigoVariableGlobal("Variable Global", vida=18, ataque=7, defensa=0, tipo="terrestre", experiencia_otorgada=18, puntos_commit_otorgados=12),
        # Este sobreescribe DEBILIDAD ("Stack Trace") en vez de heredar la de EnemigoBug
        EnemigoMemoryLeak("Memory Leak", vida=15, ataque=4, defensa=0, tipo="volador", experiencia_otorgada=22, puntos_commit_otorgados=18),
    ]


def crear_objetos() -> list:
    return [
        Tesoro("Fragmento de código limpio", valor_monetario=30),
        Tesoro("Café", valor_monetario=15),
        TrampaExplosiva("SyntaxError", alcance_explosion=1, daño_explosion=12),
    ]


def crear_jefe() -> Enemigo:
    # También sobreescribe DEBILIDAD ("Refactorizador"): solo él es vulnerable a esa arma
    return EnemigoJefe("El Legacy Code", vida=80, ataque=12, defensa=4, tipo="terrestre",
                        experiencia_otorgada=200, puntos_commit_otorgados=100)


def crear_tienda() -> Tienda:
    return Tienda([
        Armamento("Debugger", aumento_ataque=5, aumento_defensa=2, precio_compra=50, precio_venta=20, nivel_requerido=1),
        Armamento("Stack Trace", aumento_ataque=10, aumento_defensa=3, precio_compra=120, precio_venta=50, nivel_requerido=3),
        Armamento("Refactorizador", aumento_ataque=20, aumento_defensa=8, precio_compra=250, precio_venta=100, nivel_requerido=5),
    ])
