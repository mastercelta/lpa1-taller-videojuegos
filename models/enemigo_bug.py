from .enemigo import Enemigo


class EnemigoBug(Enemigo):
    # Todos los "bugs" del sueño heredan esta debilidad por defecto.
    # Una subclase que NO defina su propio DEBILIDAD queda con esta misma,
    # simplemente porque la heredó de aquí (no es que la repita a mano).
    DEBILIDAD = "Debugger"

    def es_debil_contra(self, nombre_arma: str) -> bool:
        return nombre_arma == self.DEBILIDAD


class EnemigoNullPointer(EnemigoBug):
    pass  # no sobreescribe DEBILIDAD: hereda "Debugger" tal cual de EnemigoBug


class EnemigoBucleInfinito(EnemigoBug):
    pass  # igual que arriba: misma debilidad heredada, sin redefinirla


class EnemigoVariableGlobal(EnemigoBug):
    pass  # igual que arriba


class EnemigoMemoryLeak(EnemigoBug):
    DEBILIDAD = "Stack Trace"  # este SÍ sobreescribe: polimorfismo, debilidad distinta


class EnemigoJefe(EnemigoBug):
    DEBILIDAD = "Refactorizador"  # el jefe también sobreescribe, solo vulnerable al arma final
