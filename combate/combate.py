class Combate:

    @staticmethod
    def atacar(atacante, defensor) -> dict:
        # R5.1, R5.2: mecánica de combate y cálculo de daño según ataque/defensa/vida
        daño_real = defensor.recibir_daño(atacante.ataque)
        return {
            "atacante": atacante.nombre,
            "defensor": defensor.nombre,
            "daño": daño_real,
            "defensor_derrotado": not defensor.esta_vivo(),
        }

    @staticmethod
    def usar_trampa(trampa, objetivos: list) -> dict:
        resultados = trampa.explotar(objetivos)  # R5.3: efecto especial (explosión en área)
        derrotados = [nombre for nombre, _ in resultados.items() if not any(o.nombre == nombre and o.esta_vivo() for o in objetivos)]
        return {"trampa": trampa.nombre, "daños": resultados, "derrotados": derrotados}

    @staticmethod
    def resolver_combate_enemigo(personaje, enemigo) -> list:
        # R3.1: el personaje ataca y se defiende de los enemigos
        resultados = [Combate.atacar(personaje, enemigo)]
        if enemigo.esta_vivo():
            resultados.append(Combate.atacar(enemigo, personaje))
        return resultados
