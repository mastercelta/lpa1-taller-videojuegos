from mundo.historia import FINAL_EXPLORACION, FINAL_JEFE, FINAL_PUNTAJE

UMBRAL_EXPLORACION = 0.6
UMBRAL_PUNTAJE = 100  # alcanzable con los bugs y tesoros, sin vencer al jefe


def verificar_victoria(personaje, escenario, jefe) -> str:
    if jefe is not None and not jefe.esta_vivo():
        return FINAL_JEFE  # R7.2

    if escenario.porcentaje_explorado() >= UMBRAL_EXPLORACION:
        return FINAL_EXPLORACION  # R7.1

    if personaje.puntos_commit_ganados >= UMBRAL_PUNTAJE:
        return FINAL_PUNTAJE.format(UMBRAL_PUNTAJE)  # R7.3

    return ""
