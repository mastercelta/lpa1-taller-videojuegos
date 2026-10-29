# La historia vive aparte de la lógica: así se puede cambiar el guion sin tocar las reglas del juego

NARRADOR = "Narrador"
PATO = "Pato de Goma"
JEFE = "El Legacy Code"

INTRO = [
    (NARRADOR, "Son las 3:07 a. m. El parcial de programación es a las 7. Tus ojos se cierran sobre el teclado..."),
    (NARRADOR, "...y despiertas dentro de tu propio código: el Reino del Código, donde cada línea es tierra y cada función, un camino."),
    (PATO, "¡Por fin llegas! Soy el Pato de Goma. Los programadores me cuentan sus errores y yo los escucho. Tú eres el Depurador que esperábamos."),
    (PATO, "El reino se está rompiendo. Variables que apuntan a la nada, bucles sin salida, memoria que se escapa... Los bugs salieron de las sombras."),
    (PATO, "Todos obedecen a uno: El Legacy Code. Fue el primer programa del reino. Su autor se fue sin dejar un solo comentario."),
    (JEFE, "Nadie me entendió. Nadie me documentó. Y ahora quieren reemplazarme... Si nadie puede leerme, nadie podrá borrarme."),
    (JEFE, "Haré que todo el reino sea tan ilegible como yo."),
    (PATO, "Vence a los bugs, recoge commits y equípate en la tienda del Stack Overflow. Su guarida está en la esquina más oscura del mapa."),
    (PATO, "Y si te pierdes, explícame el problema en voz alta: así se depura. ¡Ve, antes de que suene el despertador!"),
]

AVISTAR_JEFE = f"{JEFE}: «Llegaste lejos, Depurador. Nadie ha leído mis diez mil líneas y salido cuerdo.»"

FINAL_JEFE = f"Refactorizaste a {JEFE}: por primera vez alguien lo entendió. Suena el despertador y estás listo para el parcial."
FINAL_EXPLORACION = "Mapeaste el Reino del Código: sin rincones oscuros, los bugs no tienen dónde esconderse. Despiertas con el mapa en la cabeza."
FINAL_PUNTAJE = "{} commits limpios: el reino vuelve a compilar. Despiertas y el código de anoche, por fin, funciona."
FINAL_DERROTA = f"{JEFE} se impone y el reino queda ilegible... Suena el despertador. Todo bug tiene solución: inténtalo de nuevo."
