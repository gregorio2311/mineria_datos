import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import skew, kurtosis

data = pd.read_csv('Datos/Streaming_History_Audio.csv')

data['ts'] = pd.to_datetime(data['ts'])  # Convertir la columna 'ts' a formato datetime
data['minutes_played'] = data['ms_played'] / 60000  # Convertir 'ms_played' a minutos

def visualizar_reproducciones_por_fecha(data):
    fig, ax = plt.subplots(figsize=(15, 8))
    data.groupby(data['ts'].dt.date)['minutes_played'].sum().plot(kind='line', ax=ax)
    ax.set(title='Reproducciones Diarias', xlabel='Fecha', ylabel='Minutos Reproducidos')
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


    fig, ax = plt.subplots(figsize=(15, 8))
    data_grouped = data.groupby(data['ts'].dt.date)['minutes_played'].sum().reset_index()
    data_grouped['ts'] = pd.to_datetime(data_grouped['ts'])
    ax.scatter(data_grouped['ts'], data_grouped['minutes_played'], alpha=0.5, edgecolors='none')
    plt.gcf().autofmt_xdate()
    ax.set_title('Tiempo de reproducción por fecha')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Minutos reproducidos')

    plt.show()


def calcular_estadisticas_descriptivas(duracion):
    estadisticas = {
        'Mínimo': duracion.min(),
        'Máximo': duracion.max(),
        'Moda': calcular_moda(duracion),
        'Conteo': duracion.count(),
        'Sumatoria': duracion.sum(),
        'Media': duracion.mean(),
        'Varianza': duracion.var(),
        'Desviación Estándar': duracion.std(),
        'Asimetría': skew(duracion, bias=False),
        'Curtosis': kurtosis(duracion, bias=False)
    }
    return pd.DataFrame([estadisticas], index=["Estadísticas"])

def calcular_moda(serie):
    moda = serie.mode()
    if len(moda) > 1:
        moda = ", ".join(moda)
    else:
        moda = moda[0]
    return moda

def menu_principal():
    opcion = ''
    while opcion != '5':
        print("\nMenú Principal")
        print("1. Canciones")
        print("2. Álbumes")
        print("3. Artistas")
        print("4. Filtro")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            menu_generico('Canciones', 'master_metadata_track_name')
        elif opcion == '2':
            menu_generico('Álbumes', 'master_metadata_album_album_name')
        elif opcion == '3':
            menu_generico('Artistas', 'master_metadata_album_artist_name')
        elif opcion == '4':
            visualizar_reproducciones_por_fecha(data)
        elif opcion == '5':
            return
        else:
            print("Opción no válida. Por favor, intenta nuevamente.")

def menu_generico(tipo, columna):

    opcion = ''

    while opcion != '3':
        print(f"\nMenú {tipo}")
        print("1. Ver estadísticas generales")
        print("2. Buscar específico")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            estadisticas_generales(data, columna, tipo)
        elif opcion == '2':
            buscar_especifico(data, columna, tipo)
        else:
            print("Opción no válida. Por favor, intenta nuevamente.")

def estadisticas_generales(data, columna, tipo):
    print(f"\nEstadísticas Descriptivas por {columna}:")
    duracion_segundos = data.groupby(columna)['ms_played'].sum() / 60000
    estadisticas_df = calcular_estadisticas_descriptivas(duracion_segundos)
    print(estadisticas_df.transpose())

    visualizar_reproducciones_por_fecha(data)

def calcular_moda_canciones(data):
    moda = data.value_counts().idxmax()  
    return moda

def buscar_especifico(data, columna, tipo):
    nombre = input(f"Ingresa el nombre de {columna} que deseas buscar: ")
    filtrados = data[data[columna].str.contains(nombre, case=False)]
    
    if filtrados.empty:
        print("No se encontraron coincidencias.")
        return

    if tipo == 'Canciones':
        minimo = filtrados['ms_played'].min()
        maximo = filtrados['ms_played'].max()
        moda = calcular_moda_canciones(filtrados['ms_played'])

        print(f"\nEstadísticas para '{nombre}':")
        print(f"Mínimo (ms_played): {minimo}")
        print(f"Máximo (ms_played): {maximo}")
        print(f"Moda (ms_played): {moda}")

    elif tipo == 'Álbumes' or tipo == 'Artistas':
        cancion_minimo = filtrados.loc[filtrados['ms_played'].idxmin(), 'master_metadata_track_name']
        cancion_maximo = filtrados.loc[filtrados['ms_played'].idxmax(), 'master_metadata_track_name']
        cancion_moda = calcular_moda_canciones(filtrados['master_metadata_track_name'])

        print(f"\nEstadísticas para '{nombre}':")
        print(f"Mínimo (Canción): {cancion_minimo}")
        print(f"Máximo (Canción): {cancion_maximo}")
        print(f"Moda (Canción): {cancion_moda}")

menu_principal()
