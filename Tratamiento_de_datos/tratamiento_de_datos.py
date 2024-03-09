import json
import os
import csv
import pandas as pd

data = []
archivos_json = ['Spotify Extended Streaming History copy/Streaming_History_Audio_2014-2016_0.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2016-2017_1.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2017-2018_2.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2018-2019_3.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2019_4.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2019_5.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2019-2020_6.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2020_7.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2020-2021_8.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2021-2022_9.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2022-2023_10.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2023-2024_11.json',
                 'Spotify Extended Streaming History copy/Streaming_History_Audio_2024_12.json']

for archivo in archivos_json:
    if os.path.exists(archivo):
        with open(archivo, encoding='utf-8') as f:
            datos_archivo = json.load(f)
        data.extend(datos_archivo)
    else:
        print(f"El archivo '{archivo}' no existe.")

def print_n(data):
    
    number_of_objects = len(data)
    print(f"{number_of_objects} reproducciones en el documento")

print_n(data)

# Funcion para eliminar campos indeseados y entradas repetidas
campos_x = [
    'username', 'platform', 'conn_country', 'ip_addr_decrypted',
    'user_agent_decrypted', 'episode_name', 'episode_show_name',
    'spotify_episode_uri', 'reason_start', 'reason_end', 'shuffle',
    'offline', 'offline_timestamp', 'incognito_mode'
]

# Lista para almacenar los objetos únicos
json_limpio = []

# Variable para guardar el 'ts' del objeto anterior
previous_ts = None

for item in data:
    # Comprobar si el 'ts' actual es diferente al 'ts' del objeto anterior
    if item["ts"] != previous_ts and item["master_metadata_track_name"] != None:
        # Actualizar el 'ts' 
        previous_ts = item["ts"]
        
        # Remover los campos especificados
        for field in campos_x:
            item.pop(field, None)
        
        # Añadir el objeto a la lista de objetos únicos
        json_limpio.append(item)

data = json_limpio
print_n(data)

with open('Datos/Streaming_History_Audio.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# Guardamos la informacion del JSON como CSV
datos_json = pd.read_json('Datos/Streaming_History_Audio.json')

datos_json.to_csv('Datos/Streaming_History_Audio.csv', index=False)


