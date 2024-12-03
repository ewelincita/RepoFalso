import csv
import json
import random
import time
from datetime import datetime

# Variables globales
vidas: int = 3
puntaje: int = 0
dificultad: int = 1
comodines_disponibles: int = 2

def cargar_problemas(nombre_archivo: str) -> list[dict]:
    """ Lee problemas desde un archivo CSV y devuelve una lista de diccionarios. """
    with open(nombre_archivo, mode="r") as archivo:
        return [
            {"problema": fila["problema"], "solucion": float(fila["solucion"]), "dificultad": int(fila["dificultad"])}
            for fila in csv.DictReader(archivo)
        ]

def guardar_puntaje(nombre: str, puntaje: int, archivo: str = "Archivo_Multimedia/scores.json") -> None:
    """ Registra los puntajes de los jugadores en un archivo JSON. """
    try:
        with open(archivo, "r") as archivo_json:
            datos = json.load(archivo_json)
    except FileNotFoundError:
        datos = []
    datos.append({"nombre": nombre, "puntaje": puntaje, "fecha": str(datetime.now())})
    with open(archivo, "w") as archivo_json:
        json.dump(datos, archivo_json, indent=4)
    print("Puntaje guardado correctamente.")

def obtener_problema(lista_problemas: list[dict], dificultad: int) -> dict | None:
    """ Obtiene un problema según la dificultad. """
    problemas_filtrados = [p for p in lista_problemas if p["dificultad"] == dificultad]
    return random.choice(problemas_filtrados) if problemas_filtrados else None

def crear_comodin_tiempo(diccionario_juego, tiempo_inicio, incremento_tiempo, diccionario_mensajes):
    """ Comodín para agregar tiempo extra al juego. """
    tiempo_transcurrido = int(time.time() - tiempo_inicio)
    tiempo_restante = diccionario_juego["tiempo"] - tiempo_transcurrido
    if diccionario_juego["comodines_disponibles"] > 0 and diccionario_juego["comodin_tiempo_disponible"]:
        diccionario_juego["tiempo"] += incremento_tiempo
        diccionario_juego["comodines_disponibles"] -= 1
        mensaje = f"[Comodín usado] Tiempo extra: {incremento_tiempo} segundos | restante: {tiempo_restante}."
    else:
        mensaje = diccionario_mensajes['mensaje_error'] if not diccionario_juego["comodin_tiempo_disponible"] else diccionario_mensajes['mensaje_general']
    diccionario_juego["tiempo"] = tiempo_restante
    return mensaje

def jugar() -> None:
    """ Lógica principal del juego """
    global vidas, puntaje, dificultad, comodines_disponibles
    lista_problemas = cargar_problemas("Archivo_Multimedia/problemas.csv")
    if not lista_problemas:
        print("No se pudo cargar los problemas. Verifica el archivo CSV.")
        return

    print("\nMatematrix")
    nombre_jugador: str = input("Por favor, ingresa tu nombre: ").strip()
    while vidas > 0:
        problema = obtener_problema(lista_problemas, dificultad)
        if not problema:
            print(f"No hay problemas para la dificultad {dificultad}.")
            break
        
        print(f"\nProblema: {problema['problema']}")
        print("Tienes 10 segundos para responder.")
        
        # Comodín: ofrecer al jugador la opción de usarlo
        if comodines_disponibles > 0:
            usar_comodin = input(f"Tienes {comodines_disponibles} comodín(es). ¿Quieres usar uno para ganar 10 segundos (s/n): ").strip().lower()
            if usar_comodin == "s":
                tiempo_extra = 10  # Tiempo adicional
                mensaje_comodin = crear_comodin_tiempo(
                    {"comodines_disponibles": comodines_disponibles, "tiempo": 10, "comodin_tiempo_disponible": True},
                    time.time(),
                    tiempo_extra,
                    {"mensaje_error": "No puedes usar más comodines.", "mensaje_general": "El comodín no está disponible."}
                )
                print(mensaje_comodin)

        start_time = time.time()
        respuesta = input("Tu respuesta: ").strip()
        elapsed_time = time.time() - start_time
        
        if elapsed_time > 10:
            print("\u2718 Tiempo agotado. La respuesta era :", problema["solucion"])
            vidas -= 1
        elif respuesta and respuesta.isdigit() and float(respuesta) == problema["solucion"]:
            print("\u2714 Correcto!")
            puntaje += 1
            if puntaje % 5 == 0:
                dificultad += 1
                print("\nHas subido de nivel! Dificultad aumentada.")
        else:
            print(f"\u2718 Incorrecto. La respuesta era: {problema['solucion']}")
            vidas -= 1
        
        print(f"Vidas restantes: {vidas} | Puntaje: {puntaje} | Comodines restantes: {comodines_disponibles}")

    print(f"\nJuego terminado. Puntaje final: {puntaje}")
    guardar_puntaje(nombre_jugador, puntaje, "Archivo_Multimedia/scores.json")

if __name__ == "__main__":
    jugar()
