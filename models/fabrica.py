from .armamento import Armamento
from .enemigo import Enemigo
from .enemigo_bug import EnemigoNullPointer, EnemigoBucleInfinito, EnemigoVariableGlobal, EnemigoMemoryLeak, EnemigoJefe
from .tesoro import Tesoro
from .trampa_explosiva import TrampaExplosiva

# Autosave: a partir del nombre de la clase guardado se vuelve a crear el objeto correcto
OBJETOS = {c.__name__: c for c in (Tesoro, TrampaExplosiva, Armamento)}
ENEMIGOS = {c.__name__: c for c in (Enemigo, EnemigoNullPointer, EnemigoBucleInfinito,
                                    EnemigoVariableGlobal, EnemigoMemoryLeak, EnemigoJefe)}


def objeto_desde_dict(datos: dict):
    datos = dict(datos)
    clase = OBJETOS[datos.pop("clase")]
    return clase(**datos)


def enemigo_desde_dict(datos: dict):
    clase = ENEMIGOS[datos["clase"]]
    enemigo = clase(datos["nombre"], vida=datos["vida_maxima"], ataque=datos["ataque"], defensa=datos["defensa"],
                    tipo=datos["tipo"], experiencia_otorgada=datos["experiencia_otorgada"],
                    puntos_commit_otorgados=datos["puntos_commit_otorgados"])
    enemigo.restaurar(datos)
    return enemigo
