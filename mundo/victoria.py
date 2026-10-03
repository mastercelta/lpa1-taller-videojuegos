UMBRAL_EXPLORACION = 0.6
UMBRAL_PUNTAJE = 150


def verificar_victoria(personaje, escenario, jefe) -> str:
    if jefe is not None and not jefe.esta_vivo():
        return f"¡Venciste a {jefe.nombre}! Depuraste el sueño por completo."  # R7.2

    if escenario.porcentaje_explorado() >= UMBRAL_EXPLORACION:
        return "¡Exploraste todo el escritorio! El sueño termina en paz."  # R7.1

    if personaje.puntos_commit >= UMBRAL_PUNTAJE:
        return f"¡Alcanzaste {UMBRAL_PUNTAJE} puntos de commit! Despiertas satisfecho."  # R7.3

    return ""
