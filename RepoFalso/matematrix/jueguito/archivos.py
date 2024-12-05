
# Función que crea un diccionario basado en el CSV.
# Recibe como parámetro el nombre del archivo CSV.
# archivos.py
# archivos.py
import csv

def cargar_problemas(problemas_csv: str) -> dict:
    diccionario_problemas = {
        "Faciles": {"Problemas": [], "Puntaje": 5},
        "Medios": {"Problemas": [], "Puntaje": 10},
        "Dificiles": {"Problemas": [], "Puntaje": 15},
    }

    filas_invalidas = []  # Almacena las filas que no son válidas

    try:
        with open(problemas_csv, mode='r', encoding='utf-8') as archivo:
            lector_csv = csv.reader(archivo)
            next(lector_csv)  # Saltar la cabecera

            for numero_linea, fila in enumerate(lector_csv, start=2):  # Empezamos en la línea 2 (después de la cabecera)
                if len(fila) != 3 or not all(fila):  # Verificar longitud y que no haya valores vacíos
                    filas_invalidas.append((numero_linea, fila))
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

        # Depuración: Mostrar cuántos problemas se cargaron
        for categoria, datos in diccionario_problemas.items():
            print(f"{categoria}: {len(datos['Problemas'])} problemas cargados.")

        # Mostrar advertencia sobre filas inválidas
        if filas_invalidas:
            print("\nAdvertencia: Se encontraron filas inválidas en el archivo CSV:")
            for numero_linea, fila in filas_invalidas:
                print(f" - Línea {numero_linea}: {fila}")

    except FileNotFoundError:
        print(f"Error: El archivo {problemas_csv} no se encontró.")
    except Exception as e:
        print(f"Error inesperado al leer el archivo CSV: {e}")

    return diccionario_problemas


# Función que guarda las estadísticas en un archivo JSON.
def guardar_puntaje_json(nombre: str, puntaje: int, tiempo: int, vidas: int):
    datos = {
        "Nombre": nombre,
        "Puntaje": puntaje,
        "Tiempo": tiempo, 
        "Vidas": vidas
    }

    try:
        with open("matematrix/Archivo_Multimedia/Estadisticas.json", "r", encoding='utf-8') as archivo:
            estadisticas = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        estadisticas = []
        
    estadisticas.append(datos)

    try:
        with open("matematrix/Archivo_Multimedia/Estadisticas.json", "w", encoding='utf-8') as puntaje_file:
            json.dump(estadisticas, puntaje_file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar las estadísticas: {e}")
