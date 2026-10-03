class Tienda:

    def __init__(self, catalogo: list):
        self._catalogo = catalogo  # lista de Armamento disponibles

    @property
    def catalogo(self) -> list:
        return self._catalogo.copy()

    def catalogo_para_nivel(self, nivel: int) -> list:
        return [a for a in self._catalogo if a.nivel_requerido <= nivel]  # R6.3

    def comprar(self, personaje, armamento) -> str:
        # R3.3: el personaje puede comprar objetos de armamento/defensa
        if armamento not in self._catalogo:
            return f"{armamento.nombre} no está disponible en esta tienda"
        if personaje.nivel < armamento.nivel_requerido:
            return f"Necesitas nivel {armamento.nivel_requerido} para comprar {armamento.nombre}"
        if not personaje.gastar_puntos_commit(armamento.precio_compra):
            return "No tienes suficientes puntos de commit"
        personaje.recolectar(armamento)
        return f"Compraste {armamento.nombre}"

    def vender(self, personaje, armamento) -> str:
        # R3.3: el personaje puede vender objetos de armamento/defensa
        if not personaje.quitar_del_inventario(armamento):
            return f"No tienes {armamento.nombre} en tu inventario"
        personaje.ganar_puntos_commit(armamento.precio_venta)
        return f"Vendiste {armamento.nombre} por {armamento.precio_venta} puntos de commit"
