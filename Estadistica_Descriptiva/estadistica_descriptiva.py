import pandas as pd
from scipy.stats import skew, kurtosis

data = pd.read_csv('Datos/Streaming_History_Audio.csv')

def calcular_estadisticas_descriptivas(duracion):
    estadisticas = {
        'Minimo': duracion.min(),
        'Maximo': duracion.max(),
        'Moda': duracion.mode()[0],
        'Conteo': duracion.count(),
        'Sumatoria': duracion.sum(),
        'Media': duracion.mean(),
        'Varianza': duracion.var(),
        'Desviacion Estandar': duracion.std(),
        'Asimetria': skew(duracion, bias=False),
        'Curtosis': kurtosis(duracion, bias=False)
    }
    return pd.DataFrame([estadisticas], index=["Estadísticas"])

# Menú Principal
def menu_principal():
    opcion = ''
    while opcion != '5':
        print("\nMenú Principal")
        print("1. Canciones")
        print("2. Álbumes")
        print("3. Artistas")
        print("4. Filtros")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            menu_canciones()
        elif opcion == '2':
            menu_albumes()
        elif opcion == '3':
            menu_artistas()
        elif opcion == '4':
            menu_filtros()
        elif opcion == '5':
            print("Saliendo del programa...")
        else:
            print("Opción no válida. Por favor, intenta nuevamente.")

# Menú y funciones para Canciones
def menu_canciones():
    opcion = ''
    while opcion != '3':
        print("\nMenú Canciones")
        print("1. Ver estadísticas generales")
        print("2. Buscar canción específica")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            estadisticas_canciones(data)
        elif opcion == '2':
            buscar_cancion(data)
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, intenta nuevamente.")

def estadisticas_canciones(data):
    print("\nEstadísticas Descriptivas de Canciones:")
    duracion_segundos = data['ms_played'] / 1000
    estadisticas_df = calcular_estadisticas_descriptivas(duracion_segundos)
    print(estadisticas_df)

def buscar_cancion(data):
    nombre_cancion = input("Ingresa el nombre de la canción que deseas buscar: ")
    canciones_filtradas = data[data['master_metadata_track_name'].str.contains(nombre_cancion, case=False)]
    if canciones_filtradas.empty:
        print("No se encontraron coincidencias.")
    else:
        print(f"\nEstadísticas para '{nombre_cancion}':")
        duracion_segundos = canciones_filtradas['ms_played'] / 1000
        estadisticas_df = calcular_estadisticas_descriptivas(duracion_segundos)
        print(estadisticas_df)

# Implementaciones para menú de álbumes y artistas serían similares a las de canciones

# Menú y funciones para Álbumes
def menu_albumes():
    # Esta función seguiría un patrón similar al menu_canciones, adaptado para álbumes
    pass

# Menú y funciones para Artistas
def menu_artistas():
    # Esta función seguiría un patrón similar al menu_canciones, adaptado para artistas
    pass

# Menú y funciones para Filtros
def menu_filtros():
    # Implementación del menú de filtros y aplicación
    pass

# Iniciar el programa
if __name__ == "__main__":
    menu_principal()
