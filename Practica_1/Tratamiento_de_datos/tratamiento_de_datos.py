import pandas as pd
import json
import os


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

# Campos a eliminar
campos_x = [
    'username', 'platform', 'conn_country', 'ip_addr_decrypted',
    'user_agent_decrypted', 'episode_name', 'episode_show_name',
    'spotify_episode_uri', 'shuffle','offline', 'offline_timestamp', 
    'incognito_mode', 'spotify_track_uri'
]

# DataFrame para almacenar todos los datos limpios
df_limpio = pd.DataFrame()
previous_ts = None

for archivo in archivos_json:
    if os.path.exists(archivo):
        with open(archivo, encoding='utf-8') as f:
            datos_archivo = json.load(f)
            
        # Limpieza de datos dentro del mismo bucle
        datos_limpio = []
        for item in datos_archivo:
            # Comprobar si el 'ts' actual es diferente al 'ts' del objeto anterior
            if item["ts"] != previous_ts and item.get("master_metadata_track_name") is not None:
                # Actualizar el 'ts' 
                previous_ts = item["ts"]

                if item["ms_played"] == 0 and item["skipped"] == 0:
                    continue

                # Remover los campos especificados
                item_limpio = {k: v for k, v in item.items() if k not in campos_x}
                datos_limpio.append(item_limpio)
        
        # Convertir a DataFrame y agregarlo al DataFrame global
        df_temp = pd.DataFrame(datos_limpio)
        df_limpio = pd.concat([df_limpio, df_temp], ignore_index=True)
    else:
        print(f"El archivo '{archivo}' no existe.")

# Guardar el DataFrame final en un archivo CSV
ruta_csv = 'Datos/Streaming_History_Audio.csv'
df_limpio.to_csv(ruta_csv, index=False)

print(f"Datos guardados en {ruta_csv}")
