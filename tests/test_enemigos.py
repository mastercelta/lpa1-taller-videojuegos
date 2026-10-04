import pytest

from combate.combate import Combate
from models.armamento import Armamento
from models.enemigo import Enemigo
from models.enemigo_bug import (EnemigoBug, EnemigoBucleInfinito, EnemigoJefe, EnemigoMemoryLeak,
                                EnemigoNullPointer, EnemigoVariableGlobal)
from models.entidad import Entidad
from models.objeto import Objeto
from models.personaje import Personaje


def crear(clase, tipo="terrestre"):
    return clase("E", vida=100, ataque=0, defensa=0, tipo=tipo)


def test_las_clases_abstractas_no_se_pueden_instanciar():
    with pytest.raises(TypeError):
        Entidad("x", 1, 1, 1)
    with pytest.raises(TypeError):
        Objeto("x")


def test_todos_los_enemigos_son_entidades():
    for clase in (EnemigoNullPointer, EnemigoBucleInfinito, EnemigoVariableGlobal, EnemigoMemoryLeak, EnemigoJefe):
        enemigo = crear(clase)
        assert isinstance(enemigo, EnemigoBug)
        assert isinstance(enemigo, Enemigo)
        assert isinstance(enemigo, Entidad)


def test_tres_subclases_heredan_la_misma_debilidad_sin_redefinirla():
    for clase in (EnemigoNullPointer, EnemigoBucleInfinito, EnemigoVariableGlobal):
        assert "DEBILIDAD" not in vars(clase)
        assert clase.DEBILIDAD == EnemigoBug.DEBILIDAD == "Debugger"


def test_dos_subclases_sobrescriben_la_debilidad():
    assert EnemigoMemoryLeak.DEBILIDAD == "Stack Trace"
    assert EnemigoJefe.DEBILIDAD == "Refactorizador"


def test_el_tipo_de_enemigo_solo_acepta_volador_o_terrestre():
    with pytest.raises(ValueError):
        Enemigo("x", vida=1, ataque=1, defensa=1, tipo="acuatico")


def test_explotar_la_debilidad_hace_un_50_por_ciento_mas_de_daño():
    sin_arma = Personaje("A")
    con_debugger = Personaje("B")
    con_debugger.equipar(Armamento("Debugger", 0, 0, 0, 0))
    assert Combate.atacar(sin_arma, crear(EnemigoNullPointer))["daño"] == 10
    resultado = Combate.atacar(con_debugger, crear(EnemigoNullPointer))
    assert resultado["daño"] == 15
    assert resultado["debilidad_explotada"] == "Debugger"


def test_un_arma_que_no_es_la_debilidad_no_da_bono():
    personaje = Personaje("A")
    personaje.equipar(Armamento("Stack Trace", 0, 0, 0, 0))
    assert Combate.atacar(personaje, crear(EnemigoNullPointer))["daño"] == 10
    assert Combate.atacar(personaje, crear(EnemigoMemoryLeak, "volador"))["debilidad_explotada"] == "Stack Trace"


def test_polimorfismo_describir_en_cada_clase():
    assert "Nivel" in Personaje("Ana").describir()
    assert "volador" in crear(EnemigoMemoryLeak, "volador").describir()
