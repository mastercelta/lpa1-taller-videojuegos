class Combate:

    @staticmethod
    def atacar(atacante, defensor) -> dict:
        # R5.1, R5.2: mecánica de combate y cálculo de daño según ataque/defensa/vida
        daño_base = atacante.ataque
        debilidad_explotada = None

        # Polimorfismo: no importa si el enemigo es EnemigoNullPointer, EnemigoBucleInfinito
        # o EnemigoJefe — todos responden a es_debil_contra() a su manera, heredada o propia.
        if hasattr(defensor, "es_debil_contra") and hasattr(atacante, "nombres_armas_equipadas"):
            for nombre_arma in atacante.nombres_armas_equipadas():
                if defensor.es_debil_contra(nombre_arma):
                    daño_base = int(daño_base * 1.5)
                    debilidad_explotada = nombre_arma
                    break

        daño_real = defensor.recibir_daño(daño_base)
        return {
            "atacante": atacante.nombre,
            "defensor": defensor.nombre,
            "daño": daño_real,
            "defensor_derrotado": not defensor.esta_vivo(),
            "debilidad_explotada": debilidad_explotada,
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
