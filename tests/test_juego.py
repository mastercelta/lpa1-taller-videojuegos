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
    for pos in juego.escenario.obstaculos:
        juego.escenario.quitar_obstaculo(pos)
    juego.probabilidad_esquivar = 0
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


def ir_a_la_tienda(juego: Juego) -> None:
    juego.personaje.mover(*juego.escenario.zona_venta)


def test_solo_se_compra_en_la_zona_de_venta():
    juego = juego_limpio()
    juego.personaje.ganar_puntos_commit(100)
    debugger = juego.tienda.catalogo[0]
    assert juego.comprar(debugger) == "Debes estar en la zona de venta"
    ir_a_la_tienda(juego)
    assert juego.comprar(debugger) == "Compraste Debugger"
    assert juego.armas_en_inventario() == [debugger]
    assert juego.personaje.puntos_commit == 50


def test_equipar_mejora_ataque_y_defensa():
    juego = juego_limpio()
    juego.personaje.ganar_puntos_commit(100)
    ir_a_la_tienda(juego)
    debugger = juego.tienda.catalogo[0]
    juego.comprar(debugger)
    ataque, defensa = juego.personaje.ataque, juego.personaje.defensa
    juego.equipar(debugger)
    assert juego.personaje.ataque == ataque + debugger.aumento_ataque
    assert juego.personaje.defensa == defensa + debugger.aumento_defensa
    assert juego.armas_en_inventario() == []


def test_vender_devuelve_puntos():
    juego = juego_limpio()
    juego.personaje.ganar_puntos_commit(50)
    ir_a_la_tienda(juego)
    debugger = juego.tienda.catalogo[0]
    juego.comprar(debugger)
    juego.vender(debugger)
    assert juego.personaje.puntos_commit == debugger.precio_venta
    assert juego.armas_en_inventario() == []


def test_recolectar_un_objeto_da_experiencia():
    juego = juego_limpio()
    juego.escenario.colocar_objeto(Tesoro("Café", valor_monetario=15), (1, 0))
    juego.mover(1, 0)
    assert juego.personaje.experiencia == 10


def test_la_trampa_dania_solo_a_los_enemigos_en_su_alcance():
    from models.trampa_explosiva import TrampaExplosiva
    juego = juego_limpio()
    cerca, lejos = enemigo_fijo(vida=30), enemigo_fijo(vida=30)
    juego.escenario._enemigos[(1, 1)] = cerca
    juego.escenario._enemigos[(5, 5)] = lejos
    juego.personaje.recolectar(TrampaExplosiva("SyntaxError", alcance_explosion=1, daño_explosion=12))
    juego.activar_trampa()
    assert cerca.vida == 18
    assert lejos.vida == 30
    assert juego.trampas_en_inventario() == []


def test_la_trampa_puede_derrotar_y_dar_recompensa():
    from models.trampa_explosiva import TrampaExplosiva
    juego = juego_limpio()
    juego.escenario._enemigos[(1, 0)] = enemigo_fijo(vida=5)
    juego.personaje.recolectar(TrampaExplosiva("SyntaxError", alcance_explosion=1, daño_explosion=12))
    juego.activar_trampa()
    assert (1, 0) not in juego.escenario.enemigos
    assert juego.personaje.puntos_commit == 7


def test_sin_trampas_no_pasa_nada():
    juego = juego_limpio()
    assert juego.activar_trampa() == "No tienes trampas en el inventario"


def test_los_obstaculos_bloquean_el_paso_sin_aislar_celdas():
    juego = Juego()
    assert len(juego.escenario.obstaculos) == 10
    assert juego.escenario._todo_conectado()
    limpio = juego_limpio()
    limpio.escenario._obstaculos.add((1, 0))
    limpio.mover(1, 0)
    assert limpio.personaje.posicion == (0, 0)


def test_con_esquivar_seguro_el_enemigo_no_hace_daño():
    juego = juego_limpio()
    juego.probabilidad_esquivar = 1
    juego._recibir_ataque(enemigo_fijo(vida=10, ataque=50))
    assert juego.personaje.vida == juego.personaje.vida_maxima
    assert "Esquivaste" in juego.mensaje


def test_la_niebla_solo_revela_alrededor_de_lo_visitado():
    juego = juego_limpio()
    assert juego.escenario.revelada((2, 2))
    assert not juego.escenario.revelada((3, 0))
    juego.mover(1, 0)
    assert juego.escenario.revelada((3, 0))


def test_victoria_por_puntaje_aunque_se_gaste_en_la_tienda():
    from mundo.contenido import crear_enemigos, crear_objetos
    from mundo.victoria import UMBRAL_PUNTAJE
    from models.tesoro import Tesoro as T
    alcanzable = sum(e.puntos_commit_otorgados for e in crear_enemigos()) + sum(o.valor_monetario for o in crear_objetos() if isinstance(o, T))
    assert alcanzable >= UMBRAL_PUNTAJE
    juego = juego_limpio()
    juego.personaje.ganar_puntos_commit(UMBRAL_PUNTAJE - 1)
    juego.personaje.gastar_puntos_commit(50)
    juego.escenario.colocar_objeto(T("Café", valor_monetario=1), (1, 0))
    juego.mover(1, 0)
    assert juego.resultado == "victoria"
