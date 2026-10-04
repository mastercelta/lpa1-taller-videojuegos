from combate.combate import Combate
from models.personaje import Personaje
from models.tesoro import Tesoro
from mundo.contenido import crear_enemigos, crear_objetos, crear_jefe, crear_tienda
from mundo.escenario import Escenario
from mundo.victoria import verificar_victoria

MENSAJE_INICIAL = "Muévete con las flechas. Explora, combate y sube de nivel."


class Juego:

    def __init__(self, ancho: int = 14, alto: int = 10):
        self._ancho = ancho
        self._alto = alto
        inicio = (0, 0)
        posicion_jefe = (ancho - 1, alto - 1)

        self._escenario = Escenario(ancho, alto)
        self._escenario.generar(reservadas=[inicio, posicion_jefe])
        self._escenario.distribuir_enemigos(crear_enemigos())
        self._escenario.distribuir_objetos(crear_objetos())
        self._jefe = crear_jefe()
        self._escenario.colocar_jefe(self._jefe, posicion_jefe)

        self._personaje = Personaje("Estudiante", x=inicio[0], y=inicio[1])
        self._tienda = crear_tienda()
        self._escenario.visitar(*inicio)

        self._mensaje = MENSAJE_INICIAL
        self._resultado = ""
        self._texto_final = ""

    @property
    def ancho(self) -> int:
        return self._ancho

    @property
    def alto(self) -> int:
        return self._alto

    @property
    def escenario(self) -> Escenario:
        return self._escenario

    @property
    def personaje(self) -> Personaje:
        return self._personaje

    @property
    def tienda(self):
        return self._tienda

    @property
    def jefe(self):
        return self._jefe

    @property
    def mensaje(self) -> str:
        return self._mensaje

    @property
    def resultado(self) -> str:
        return self._resultado

    @property
    def texto_final(self) -> str:
        return self._texto_final

    @property
    def terminado(self) -> bool:
        return self._resultado != ""

    def mover(self, dx: int, dy: int) -> None:
        if self.terminado:
            return
        x, y = self._personaje.posicion
        nuevo_x = max(0, min(self._ancho - 1, x + dx))
        nuevo_y = max(0, min(self._alto - 1, y + dy))
        if (nuevo_x, nuevo_y) == (x, y):
            return

        enemigo = self._escenario.enemigos.get((nuevo_x, nuevo_y))
        if enemigo is not None:
            self._combatir(enemigo, (nuevo_x, nuevo_y))
            if enemigo.esta_vivo():
                self._revisar_fin()
                return

        self._personaje.mover(nuevo_x - x, nuevo_y - y)
        self._escenario.visitar(nuevo_x, nuevo_y)
        self._recoger((nuevo_x, nuevo_y))
        self._revisar_tienda()
        self._revisar_fin()

    def _combatir(self, enemigo, pos: tuple) -> None:
        resultados = Combate.resolver_combate_enemigo(self._personaje, enemigo)  # R3.1
        partes = []
        for r in resultados:
            if r["atacante"] == self._personaje.nombre:
                texto = f"Atacas a {r['defensor']}: -{r['daño']}"
            else:
                texto = f"{r['atacante']} te ataca: -{r['daño']}"
            if r["debilidad_explotada"]:
                texto += f" ¡débil a {r['debilidad_explotada']}!"
            partes.append(texto)
        self._mensaje = " | ".join(partes)

        if enemigo.esta_vivo():
            return
        self._escenario.quitar_enemigo(pos)
        self._personaje.ganar_puntos_commit(enemigo.puntos_commit_otorgados)
        subio = self._personaje.ganar_experiencia(enemigo.experiencia_otorgada)  # R6.1
        self._mensaje = f"Derrotaste a {enemigo.nombre} (+{enemigo.experiencia_otorgada} XP, +{enemigo.puntos_commit_otorgados} pts)"
        if subio:
            self._mensaje += f" ¡Nivel {self._personaje.nivel}!"

    def _recoger(self, pos: tuple) -> None:
        objeto = self._escenario.objetos.get(pos)
        if objeto is None:
            return
        if isinstance(objeto, Tesoro):
            self._personaje.ganar_puntos_commit(objeto.valor_monetario)  # R3.2
            self._mensaje = f"Recogiste {objeto.nombre}: +{objeto.valor_monetario} puntos de commit"
        else:
            self._personaje.recolectar(objeto)  # R3.2
            self._mensaje = f"Recogiste {objeto.nombre}"
        self._escenario.quitar_objeto(pos)

    def _revisar_tienda(self) -> None:
        if self._escenario.en_zona_venta(*self._personaje.posicion):
            nombres = ", ".join(a.nombre for a in self._tienda.catalogo_para_nivel(self._personaje.nivel))
            self._mensaje = f"Zona de venta: {nombres}"

    def _revisar_fin(self) -> None:
        if not self._personaje.esta_vivo():
            self._resultado = "derrota"
            self._texto_final = "Te quedaste sin vida. El sueño se volvió pesadilla."
            return
        texto = verificar_victoria(self._personaje, self._escenario, self._jefe)  # R7.1, R7.2, R7.3
        if texto:
            self._resultado = "victoria"
            self._texto_final = texto
