import pytest

from models.comportamiento import Comportamiento, Patrullar, Perseguir, Quieto
from models.enemigo import Enemigo
from models.enemigo_bug import EnemigoJefe, EnemigoNullPointer
from mundo.juego import INTERVALO_ENEMIGOS, Juego


def libre_5x5(pos):
    return 0 <= pos[0] < 5 and 0 <= pos[1] < 5


def test_comportamiento_es_abstracto():
    with pytest.raises(TypeError):
        Comportamiento()


def test_quieto_no_se_mueve():
    assert Quieto().decidir((2, 2), (3, 2), libre_5x5) == (0, 0)


def test_patrullar_da_media_vuelta_en_el_borde():
    patrulla = Patrullar(horizontal=True)
    assert patrulla.decidir((3, 0), (0, 4), libre_5x5) == (1, 0)
    assert patrulla.decidir((4, 0), (0, 4), libre_5x5) == (-1, 0)


def test_patrullar_vertical():
    assert Patrullar(horizontal=False).decidir((2, 2), (0, 0), libre_5x5) == (0, 1)


def test_perseguir_se_acerca_si_estas_cerca():
    assert Perseguir(radio=4).decidir((4, 2), (1, 2), libre_5x5) == (-1, 0)


def test_perseguir_te_ignora_si_estas_lejos():
    assert Perseguir(radio=2).decidir((4, 4), (0, 0), libre_5x5) == (0, 0)


def test_comportamiento_segun_tipo():
    terrestre = Enemigo("t", vida=1, ataque=1, defensa=0, tipo="terrestre")
    volador = Enemigo("v", vida=1, ataque=1, defensa=0, tipo="volador")
    assert isinstance(terrestre.comportamiento, Patrullar)
    assert isinstance(volador.comportamiento, Perseguir)
    assert volador.vuela and not terrestre.vuela


def test_el_jefe_sobrescribe_su_comportamiento():
    jefe = EnemigoJefe("j", vida=1, ataque=1, defensa=0, tipo="terrestre")
    bug = EnemigoNullPointer("b", vida=1, ataque=1, defensa=0, tipo="terrestre")
    assert isinstance(jefe.comportamiento, Quieto)
    assert isinstance(bug.comportamiento, Patrullar)


def juego_con(enemigo, pos):
    juego = Juego()
    for p in list(juego.escenario.enemigos):
        juego.escenario.quitar_enemigo(p)
    for p in list(juego.escenario.objetos):
        juego.escenario.quitar_objeto(p)
    juego.escenario.colocar_jefe(enemigo, pos)
    return juego


def test_los_enemigos_se_mueven_con_el_tiempo():
    enemigo = Enemigo("t", vida=10, ataque=1, defensa=0, tipo="terrestre")
    juego = juego_con(enemigo, (5, 5))
    juego.actualizar(INTERVALO_ENEMIGOS)
    assert (5, 5) not in juego.escenario.enemigos
    assert (6, 5) in juego.escenario.enemigos


def test_un_enemigo_que_te_alcanza_te_ataca():
    volador = Enemigo("v", vida=10, ataque=30, defensa=0, tipo="volador")
    juego = juego_con(volador, (1, 0))
    vida = juego.personaje.vida
    juego.actualizar(INTERVALO_ENEMIGOS)
    assert juego.personaje.vida < vida
    assert juego.escenario.enemigos[(1, 0)] is volador


def test_los_terrestres_no_pisan_objetos_pero_los_voladores_si():
    juego = juego_con(Enemigo("t", vida=1, ataque=1, defensa=0, tipo="terrestre"), (9, 9))
    from models.tesoro import Tesoro
    juego.escenario.colocar_objeto(Tesoro("x", 1), (4, 4))
    assert not juego.escenario.puede_ocupar((4, 4), vuela=False)
    assert juego.escenario.puede_ocupar((4, 4), vuela=True)


def test_nada_se_mueve_si_la_partida_termino():
    enemigo = Enemigo("t", vida=10, ataque=1, defensa=0, tipo="terrestre")
    juego = juego_con(enemigo, (5, 5))
    juego._resultado = "derrota"
    juego.actualizar(INTERVALO_ENEMIGOS * 3)
    assert (5, 5) in juego.escenario.enemigos
