import time
import random
from comodines import *
from archivos import *

#Esta función resta las vidas.
#Recibe las vidas
#Retorna una tupla de mensaje y vidas.
def restar_vidas(vidas: int)-> str|int:
    vidas -= 1
    if vidas > 0:
        mensaje = f"¡Vida perdida! Te quedan: {vidas} vidas."
    else:
        mensaje = f"Te quedaste sin vidas, termina el juego."

    return mensaje, vidas

#Esta funcion ingresa y valida la polabra puesta por el usuario.
#Recibe como parámetro el diccionario y el mensaje
#Retorna un booleano, "False" si la palabra es incorrecta, "True" si no.
def ingresar_y_validar_problema(diccionario: dict, mensaje: str) -> bool:
    problema = mensaje.lower()  # Usamos el mensaje que es la palabra ingresada por el usuario
    es_problema = False
    for clave in diccionario:
        for item in diccionario[clave]["Problemas"]:
            # Comparamos la palabra con cada elemento en la lista de problemas
            if problema == item:
                es_problema = True
                break  # Salimos del ciclo ya que no hace falta seguir buscando
        if es_problema:
            break  # Salimos del ciclo externo si encontramos el problema
    return es_problema


#Esta función calcula el porcentaje.
#Recibe el diccionario, el puntaje inicial (0) y la palabra
#Retorna el puntaje
def calcular_puntaje(diccionario: dict, puntaje: int, palabra: str)-> int:
    # Recorre cada categoría en el diccionario
    for clave in diccionario:
        lista_problemas = diccionario[clave]["Problemas"]
        # Recorre la lista de palabras de la categoría
        for problema_en_lista in lista_problemas:
            if palabra == problema_en_lista:
                puntaje += diccionario[clave]["Puntaje"]  # Sumar el puntaje de la palabra
                return puntaje  # Sale de la función una vez que encuentra la palabra
    return puntaje

#Esta función obtiene la palabra del diccionario.
#Recibe el diccionario y el tiempo restante
#Retorna un diccionario con la palabra, categoria y puntaje
def obtener_problema(tiempo_restante: int, diccionario_problemas: dict)-> dict:
    if tiempo_restante > 10: 
        categoria = "Faciles"
    elif tiempo_restante > 5:  
        categoria = "Medios"
    else:
        categoria = "Dificiles" 

# Selecciona un problema aleatorio de la categoría seleccionada
    problema_seleccionado = random.choice(diccionario_problemas[categoria]["Problemas"])
    return {
        "Categoria": categoria,
        "Problema": problema_seleccionado["Problema"],
        "Puntaje": diccionario_problemas[categoria]["Puntaje"]
    }