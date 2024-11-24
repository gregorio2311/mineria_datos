import pandas as pd
from scipy.stats import skew, kurtosis
from statistics import mode

data = pd.read_csv('Datos/Streaming_History_Audio.csv')

def estadistica(reproducciones):
    estadisticas = {
        'Mínimo': reproducciones.min(),
        'Máximo': reproducciones.max(),
        'Moda': mode(reproducciones),
        'Conteo': reproducciones.count(),
        'Sumatoria': reproducciones.sum(),
        'Media': reproducciones.mean(),
        'Varianza': reproducciones.var(),
        'Desviación Estándar': reproducciones.std(),
        'Asimetría': skew(reproducciones, bias=False),
        'Curtosis': kurtosis(reproducciones, bias=False)
    }
    return pd.DataFrame([estadisticas], index=["n_reproducciones"])

def est_des_rep(data, columna):
    reproducciones = data.groupby(columna).size()
    print(f"\nEstadísticas descriptivas \n{columna}:")
    estadisticas_df = estadistica(reproducciones)
    print(estadisticas_df.transpose())
    top_cinco = reproducciones.sort_values(ascending=False).head(5)
    print("\nTop 5 más reproducidos:")
    for nombre, conteo in top_cinco.items():
        print(f"{conteo} {nombre}")


def inicio():
    opcion = ''
    while opcion != '4':
        print("\nMenú Principal")
        print("1. Canciones")
        print("2. Álbumes")
        print("3. Artistas")
        print("4. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            est_des_rep(data, 'master_metadata_track_name')
        elif opcion == '2':
            est_des_rep(data, 'master_metadata_album_album_name')
        elif opcion == '3':
            est_des_rep(data, 'master_metadata_album_artist_name')
        elif opcion == '4':
            return
        else:
            print("Opción no válida. Por favor, intenta nuevamente.")

inicio()
