from combate.combate import Combate
from models.armamento import Armamento
from models.personaje import Personaje
from models.tesoro import Tesoro
from mundo.contenido import crear_enemigos, crear_objetos, crear_jefe, crear_tienda
from mundo.escenario import Escenario
from mundo.victoria import verificar_victoria

MENSAJE_INICIAL = "Muévete con las flechas. Explora, combate y sube de nivel."
INTERVALO_ENEMIGOS = 0.6  # segundos entre cada paso de los enemigos
XP_POR_OBJETO = 10


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
        self._reloj_enemigos = 0.0

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
        self._personaje.mirar(dx, dy)
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

    def actualizar(self, dt: float) -> None:
        # R10.2: el mundo avanza con el tiempo aunque el jugador no se mueva
        if self.terminado:
            return
        self._reloj_enemigos += dt
        while self._reloj_enemigos >= INTERVALO_ENEMIGOS and not self.terminado:
            self._reloj_enemigos -= INTERVALO_ENEMIGOS
            self.mover_enemigos()

    def mover_enemigos(self) -> None:
        jugador = self._personaje.posicion
        for desde, enemigo in self._escenario.enemigos.items():
            if self.terminado:
                return
            if not enemigo.esta_vivo():
                continue
            puede_ir = lambda pos, vuela=enemigo.vuela: self._escenario.puede_ocupar(pos, vuela)
            dx, dy = enemigo.comportamiento.decidir(desde, jugador, puede_ir)  # polimorfismo
            if (dx, dy) == (0, 0):
                continue
            hasta = (desde[0] + dx, desde[1] + dy)
            if hasta == jugador:
                self._recibir_ataque(enemigo)
            elif self._escenario.puede_ocupar(hasta, enemigo.vuela):
                self._escenario.mover_enemigo(desde, hasta)

    def _recibir_ataque(self, enemigo) -> None:
        resultado = Combate.atacar(enemigo, self._personaje)  # R3.1: el enemigo también ataca
        self._mensaje = f"{enemigo.nombre} te embiste: -{resultado['daño']}"
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
        if self._personaje.ganar_experiencia(XP_POR_OBJETO):  # R6.1: también se gana XP al recolectar
            self._mensaje += f" ¡Nivel {self._personaje.nivel}!"

    @property
    def en_tienda(self) -> bool:
        return self._escenario.en_zona_venta(*self._personaje.posicion)

    def armas_en_inventario(self) -> list:
        return [o for o in self._personaje.inventario if isinstance(o, Armamento)]

    def comprar(self, armamento) -> str:
        # R3.3, R4.3: solo se compra parado en la zona de venta
        if not self.en_tienda:
            return "Debes estar en la zona de venta"
        self._mensaje = self._tienda.comprar(self._personaje, armamento)
        return self._mensaje

    def vender(self, armamento) -> str:
        if not self.en_tienda:
            return "Debes estar en la zona de venta"
        self._mensaje = self._tienda.vender(self._personaje, armamento)
        return self._mensaje

    def equipar(self, armamento) -> str:
        # R6.3: el equipamiento comprado mejora ataque y defensa
        if armamento not in self.armas_en_inventario():
            return f"No tienes {armamento.nombre} en tu inventario"
        self._personaje.equipar(armamento)
        self._mensaje = f"Equipaste {armamento.nombre} (+{armamento.aumento_ataque} ataque, +{armamento.aumento_defensa} defensa)"
        return self._mensaje

    def _revisar_tienda(self) -> None:
        if self.en_tienda:
            self._mensaje = "Zona de venta: presiona T para abrir la tienda"

    def _revisar_fin(self) -> None:
        if not self._personaje.esta_vivo():
            self._resultado = "derrota"
            self._texto_final = "Te quedaste sin vida. El sueño se volvió pesadilla."
            return
        texto = verificar_victoria(self._personaje, self._escenario, self._jefe)  # R7.1, R7.2, R7.3
        if texto:
            self._resultado = "victoria"
            self._texto_final = texto
