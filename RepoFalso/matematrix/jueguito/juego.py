# juego.py
import time
import os  # Para limpiar la pantalla
from archivos import *
from datos import *
from comodines import *
from funciones import *

def crear_juego():
    # Inicializamos las variables del estado del juego
    estado_variables = inicializar_variables()
    estado_variables["tiempo_inicio"] = time.time()

    # Bucle principal del juego
    while estado_variables["vidas"] > 0:
        # Limpia la pantalla (compatible con Windows y Unix)
        os.system('cls' if os.name == 'nt' else 'clear')

        # Calculamos el tiempo usado
        tiempo_usado = int(time.time() - estado_variables["tiempo_inicio"])

        # Gestionamos congelación del tiempo si está activa
        gestionar_tiempo_congelado(estado_variables)

        if not estado_variables["tiempo_congelado"]:
            tiempo_restante = estado_variables["tiempo"] - tiempo_usado
            estado_variables["tiempo"] = max(0, tiempo_restante)

        # Actualizamos la hora de inicio para el siguiente ciclo
        estado_variables["tiempo_inicio"] = time.time()

        # Mostramos el estado actual del juego
        print(f"Vidas: {estado_variables['vidas']} | Puntaje: {estado_variables['puntaje']} | Tiempo restante: {estado_variables['tiempo']} segundos")
        print(f"Comodines disponibles: {estado_variables['comodines_disponibles']}")

        try:
            # Obtenemos el problema actual según el tiempo restante
            problema_actual = obtener_problema(estado_variables["tiempo"], diccionario_problemas)
            print(f"Resuelve el problema: {problema_actual['Problema']}")
        except ValueError as e:
            print(e)
            break  # Salimos del bucle si no hay problemas disponibles

        # Entrada del usuario
        entrada_usuario = input("""Tu respuesta: 
        (Escribe "T" para obtener Tiempo extra, "V" para Vida extra, "C" para Congelar el tiempo): """).strip().lower()

        # Manejo de comodines
        if entrada_usuario in ["t", "v", "c"]:
            if entrada_usuario == "t":
                mensaje_tiempo = generar_mensaje_comodin("tiempo", estado_variables["tiempo"], estado_variables["incremento_tiempo"])
                mensaje_resultado = crear_comodin_tiempo(
                    estado_variables,
                    estado_variables["tiempo_inicio"],
                    estado_variables["incremento_tiempo"],
                    diccionario_mensajes,
                    mensaje_tiempo
                )
                print(mensaje_resultado)

            elif entrada_usuario == "v":
                mensaje_vidas = generar_mensaje_comodin("vida", estado_variables["vidas"] + 1)
                mensaje_comodin_vidas = crear_comodin_vida(estado_variables, diccionario_mensajes, mensaje_vidas)
                print(mensaje_comodin_vidas)

            elif entrada_usuario == "c":
                mensaje_congelacion = generar_mensaje_comodin("congelacion", estado_variables["duracion_congelacion"])
                mensaje_comodin_congelacion = activar_comodin_congelacion(estado_variables, diccionario_mensajes, mensaje_congelacion)
                print(mensaje_comodin_congelacion)

            time.sleep(1)
            continue

        # Validar si la respuesta es correcta
        es_correcta = ingresar_y_validar_problema(diccionario_problemas, entrada_usuario)
        if es_correcta:
            estado_variables["puntaje"] = calcular_puntaje(diccionario_problemas, estado_variables["puntaje"], entrada_usuario)
            print("¡Respuesta correcta!")
        else:
            mensaje, estado_variables["vidas"] = restar_vidas(estado_variables["vidas"])
            print(mensaje)

        time.sleep(1)

        # Verificar fin del juego por falta de comodines, vidas o tiempo
        if estado_variables['comodines_disponibles'] == 0:
            print(diccionario_mensajes['mensaje_error_general'])
        if estado_variables['vidas'] == 0 or estado_variables['tiempo'] == 0:
            break

    # Guardamos el puntaje al finalizar el juego
    nombre = input("Ingresa tu nombre para guardar el puntaje: ").strip()
    guardar_puntaje_json(nombre, estado_variables["puntaje"], estado_variables["tiempo"], estado_variables["vidas"])

    # Mostrar estadísticas finales
    print(f"\nEstadísticas finales:")
    print(f"Nombre: {nombre}")
    print(f"Puntaje: {estado_variables['puntaje']}")
    print(f"Tiempo restante: {estado_variables['tiempo']} segundos")
    print(f"Vidas restantes: {estado_variables['vidas']}")

    # Opción para reiniciar el juego
    seguir = input("¿Quieres jugar de nuevo? (si/no): ").strip().lower()
    if seguir == "si":
        return crear_juego()  # Reiniciar el juego
    print("Gracias por jugar. ¡Hasta pronto!")

