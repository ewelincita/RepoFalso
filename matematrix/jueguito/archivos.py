import json
import csv

# Función que crea un diccionario basado en el CSV.
# Recibe como parámetro el nombre del archivo CSV.
def cargar_problemas(problemas_csv: str) -> dict:
    diccionario_problemas = {
        "Faciles": {"Problemas": [], "Puntaje": 5},
        "Medios": {"Problemas": [], "Puntaje": 10},
        "Dificiles": {"Problemas": [], "Puntaje": 15}
    }

    try:
        with open(problemas_csv, mode='r', encoding='utf-8') as archivo:
            lector_csv = csv.reader(archivo)
            next(lector_csv)  # Saltar la cabecera

            for fila in lector_csv:
                if len(fila) != 3:
                    print(f"Fila inválida en el archivo CSV: {fila}")
                    continue
                
                problema, solucion, dificultad = map(str.strip, fila[:3])
                
                if dificultad == '1':
                    diccionario_problemas['Faciles']['Problemas'].append({
                        "Problema": problema,
                        "Solucion": solucion
                    })
                elif dificultad == '2':
                    diccionario_problemas['Medios']['Problemas'].append({
                        "Problema": problema,
                        "Solucion": solucion
                    })
                elif dificultad == '3':
                    diccionario_problemas['Dificiles']['Problemas'].append({
                        "Problema": problema,
                        "Solucion": solucion
                    })

        # Depuración: mostrar cuántos problemas se cargaron en cada categoría
        for categoria, datos in diccionario_problemas.items():
            print(f"{categoria}: {len(datos['Problemas'])} problemas cargados.")

    except FileNotFoundError:
        print(f"Error: El archivo {problemas_csv} no se encontró.")
    except Exception as e:
        print(f"Error inesperado al leer el archivo CSV: {e}")

    return diccionario_problemas

# Función que crea un diccionario basado en el JSON.

# Función que guarda las estadísticas en un archivo JSON.
def guardar_puntaje_json(nombre: str, puntaje: int, tiempo: int, vidas: int):
    datos = {
        "Nombre": nombre,
        "Puntaje": puntaje,
        "Tiempo": tiempo, 
        "Vidas": vidas
    }

    try:
        with open("Archivo_Multimedia/Estadisticas.json", "r", encoding='utf-8') as archivo:
            estadisticas = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        estadisticas = []
        
    estadisticas.append(datos)

    try:
        with open("Archivo_Multimedia/Estadisticas.json", "w", encoding='utf-8') as puntaje_file:
            json.dump(estadisticas, puntaje_file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar las estadísticas: {e}")
