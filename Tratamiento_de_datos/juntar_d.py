import json
import os

# Lista para almacenar los datos combinados
datos_combinados = []

# Lista de archivos JSON que deseas combinar
archivos_json = ['Spotify Extended Streaming History/Streaming_History_Audio_2014-2016_0.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2016-2017_1.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2017-2018_2.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2018-2019_3.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2019_4.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2019_5.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2019-2020_6.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2020_7.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2020-2021_8.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2021-2022_9.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2022-2023_10.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2023-2024_11.json',
                 'Spotify Extended Streaming History/Streaming_History_Audio_2024_12.json']

# Iterar sobre cada archivo JSON
for archivo in archivos_json:
    # Verificar si el archivo existe
    if os.path.exists(archivo):
        # Cargar los datos del archivo JSON
        with open(archivo, encoding='utf-8') as f:
            datos_archivo = json.load(f)
        # Agregar los datos del archivo al conjunto combinado
        datos_combinados.extend(datos_archivo)
    else:
        print(f"El archivo '{archivo}' no existe.")

# Escribir el resultado en un nuevo archivo JSON
with open('Datos/Streaming_History_Audio.json', 'w', encoding='utf-8') as f:
    json.dump(datos_combinados, f, indent=4)
