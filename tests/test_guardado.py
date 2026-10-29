from models.armamento import Armamento
from models.enemigo_bug import EnemigoMemoryLeak
from models.fabrica import enemigo_desde_dict, objeto_desde_dict
from models.personaje import Personaje
from models.tesoro import Tesoro
from models.trampa_explosiva import TrampaExplosiva


def test_cada_objeto_vuelve_a_su_clase():
    for objeto in (Tesoro("Café", 15), TrampaExplosiva("SyntaxError", 1, 12), Armamento("Debugger", 5, 2, 50, 20, 1)):
        copia = objeto_desde_dict(objeto.a_dict())
        assert type(copia) is type(objeto)
        assert copia.a_dict() == objeto.a_dict()


def test_el_enemigo_conserva_clase_vida_y_debilidad():
    leak = EnemigoMemoryLeak("Memory Leak", vida=15, ataque=4, defensa=0, tipo="volador", x=3, y=2)
    leak.recibir_daño(10)
    copia = enemigo_desde_dict(leak.a_dict())
    assert isinstance(copia, EnemigoMemoryLeak)
    assert copia.vida == leak.vida and copia.posicion == (3, 2)
    assert copia.es_debil_contra("Stack Trace")


def test_el_personaje_conserva_progreso_e_inventario():
    p = Personaje("Estudiante")
    p.ganar_puntos_commit(80)
    p.ganar_experiencia(150)
    p.recolectar(TrampaExplosiva("SyntaxError", 1, 12))
    p.equipar(Armamento("Debugger", 5, 2, 50, 20, 1))
    copia = Personaje("x")
    copia.restaurar(p.a_dict())
    assert copia.a_dict() == p.a_dict()
