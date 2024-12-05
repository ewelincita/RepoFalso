import time
from archivos import cargar_problemas

# Ruta relativa al archivo CSV
palabras_csv = "matematrix/Archivo_Multimedia/problemas.csv"  

# Llamar a la función para obtener la lista de palabras
diccionario_problemas = cargar_problemas(palabras_csv)

# Esta función almacena un diccionario con variables estáticas y que se actualizan, retorna el diccionario
def inicializar_variables() -> dict:
    diccionario_juego = {
        "vidas": 3,
        "puntaje": 0,
        "tiempo": 10,
        "comodin_tiempo_disponible": True,
        "comodin_vida_disponible": True,
        "comodin_congelacion_disponible": True,
        "comodines_disponibles": 3,
        "tiempo_inicio": time.time(),
        "duracion_congelacion": 10,
        "tiempo_congelado": False,
        "tiempo_restante_congelacion": 0,
        "incremento_tiempo": 10
    }
    return diccionario_juego

estado_variables = inicializar_variables()

# Diccionario con los mensajes
diccionario_mensajes = {
    "mensaje_error": "Este comodín ya ha sido usado",
    "mensaje_error_general": "Ya no tenés más comodines :(",
}
