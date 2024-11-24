import pandas as pd
from scipy.stats import skew, kurtosis
from statistics import mode

data = pd.read_csv('Datos/Streaming_History_Audio.csv')

def estadisticas(duracion):
    estadisticas = {
        'Mínimo': duracion.min(),
        'Máximo': duracion.max(),
        'Moda': mode(duracion),
        'Conteo': duracion.count(),
        'Sumatoria': duracion.sum(),
        'Media': duracion.mean(),
        'Varianza': duracion.var(),
        'Desviación Estándar': duracion.std(),
        'Asimetría': skew(duracion, bias=False),
        'Curtosis': kurtosis(duracion, bias=False)
    }
    return pd.DataFrame([estadisticas], index=["min_played"])


def est_des_ms(data,columna):
    if columna == '':
        duracion_segundos = data['ms_played'] / 60000
        columna = 'Reproducciones'
    else:
        duracion_segundos = data.groupby(columna)['ms_played'].sum() / 60000
    print(f"\nEstadisticas descriptivas \n{columna}:")
    estadisticas_df = estadisticas(duracion_segundos)
    print(estadisticas_df.transpose())
         


def inicio():
    opcion = ''
    while opcion != '5':
        print("\nMenú Principal")
        print("1. Canciones")
        print("2. Álbumes")
        print("3. Artistas")
        print("4. Rreproducciones")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            est_des_ms(data,'master_metadata_track_name')
        elif opcion == '2':
            est_des_ms(data,'master_metadata_album_album_name')

        elif opcion == '3':
            est_des_ms(data,'master_metadata_album_artist_name')

        elif opcion == '4':
            est_des_ms(data,'')

        elif opcion == '5':
            return
        
        else:
            print("Opción no válida. Por favor, intenta nuevamente.")

inicio()