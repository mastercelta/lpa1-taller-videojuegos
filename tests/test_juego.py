from models.enemigo import Enemigo
from models.tesoro import Tesoro
from mundo.juego import Juego


def juego_limpio() -> Juego:
    juego = Juego()
    for pos, enemigo in list(juego.escenario.enemigos.items()):
        if enemigo is not juego.jefe:
            juego.escenario.quitar_enemigo(pos)
    for pos in list(juego.escenario.objetos):
        juego.escenario.quitar_objeto(pos)
    return juego


def enemigo_fijo(vida: int, ataque: int = 0) -> Enemigo:
    return Enemigo("Dummy", vida=vida, ataque=ataque, defensa=0, tipo="terrestre",
                   experiencia_otorgada=10, puntos_commit_otorgados=7)


def test_el_inicio_siempre_queda_libre():
    for _ in range(50):
        juego = Juego()
        assert (0, 0) not in juego.escenario.enemigos
        assert (0, 0) not in juego.escenario.objetos


def test_el_personaje_no_sale_del_mapa():
    juego = juego_limpio()
    juego.mover(-1, 0)
    juego.mover(0, -1)
    assert juego.personaje.posicion == (0, 0)


def test_mover_actualiza_posicion_y_exploracion():
    juego = juego_limpio()
    antes = juego.escenario.porcentaje_explorado()
    juego.mover(1, 0)
    assert juego.personaje.posicion == (1, 0)
    assert juego.escenario.porcentaje_explorado() > antes


def test_chocar_con_un_enemigo_ataca_y_no_avanza():
    juego = juego_limpio()
    enemigo = enemigo_fijo(vida=1000)
    juego.escenario.colocar_jefe(enemigo, (1, 0))
    juego.mover(1, 0)
    assert juego.personaje.posicion == (0, 0)
    assert enemigo.vida < 1000


def test_derrotar_al_enemigo_da_recompensas_y_avanza():
    juego = juego_limpio()
    juego.escenario.colocar_jefe(enemigo_fijo(vida=1), (1, 0))
    juego.mover(1, 0)
    assert juego.personaje.posicion == (1, 0)
    assert juego.personaje.puntos_commit == 7
    assert juego.personaje.experiencia == 10
    assert (1, 0) not in juego.escenario.enemigos


def test_recoger_un_tesoro_suma_puntos():
    juego = juego_limpio()
    juego.escenario.colocar_objeto(Tesoro("Café", valor_monetario=25), (1, 0))
    juego.mover(1, 0)
    assert juego.personaje.puntos_commit == 25
    assert (1, 0) not in juego.escenario.objetos


def test_en_la_zona_de_venta_se_muestra_el_catalogo():
    juego = juego_limpio()
    for _ in range(7):
        juego.mover(1, 0)
    for _ in range(5):
        juego.mover(0, 1)
    assert juego.escenario.en_zona_venta(*juego.personaje.posicion)
    assert juego.mensaje.startswith("Zona de venta")


def test_derrota_cuando_el_personaje_se_queda_sin_vida():
    juego = juego_limpio()
    juego.escenario.colocar_jefe(enemigo_fijo(vida=10_000, ataque=10_000), (1, 0))
    juego.mover(1, 0)
    assert juego.resultado == "derrota"
    posicion = juego.personaje.posicion
    juego.mover(0, 1)
    assert juego.personaje.posicion == posicion


def test_victoria_por_puntaje():
    juego = juego_limpio()
    juego.personaje.ganar_puntos_commit(150)
    juego.mover(1, 0)
    assert juego.resultado == "victoria"


def test_victoria_por_jefe_derrotado():
    juego = juego_limpio()
    juego.jefe.recibir_daño(10_000)
    juego.mover(1, 0)
    assert juego.resultado == "victoria"
    assert "Legacy Code" in juego.texto_final
