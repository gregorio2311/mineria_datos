import json
import csv
import pandas as pd

# Guardamos la informacion del JSON como CSV
datos_json = pd.read_json('Datos/Streaming_History_Audio.json')
datos_json.to_csv('Datos/Streaming_History_Audio.csv', index=False)


# Organizamos la informacion del JSON en otro archivo
# Leer el archivo JSON
with open('Datos/Streaming_History_Audio.json','r',encoding='utf-8') as f:
    data = json.load(f)

# Diccionario para almacenar los datos organizados
organizado = {}

# Procesar cada entrada del archivo JSON
for entry in data:
    artist_name = entry['master_metadata_album_artist_name']
    album_name = entry['master_metadata_album_album_name']
    track_name = entry['master_metadata_track_name']
    track_uri = entry['spotify_track_uri']
    ts = entry['ts']
    ms_played = entry['ms_played']
    skipped = entry['skipped']

    # Verificar si el artista ya está en el diccionario
    if artist_name not in organizado:
        organizado[artist_name] = {
            'myl_album': {}
        }

    # Verificar si el album ya está en el diccionario
    if album_name not in organizado[artist_name]['myl_album']:
        organizado[artist_name]['myl_album'][album_name] = {
            'myl_songs': {}
        }

    # Verificar si la canción ya está en el diccionario
    if track_name not in organizado[artist_name]['myl_album'][album_name]['myl_songs']:
        organizado[artist_name]['myl_album'][album_name]['myl_songs'][track_name] = {
            'spotify_track_uri': track_uri,
            'myl_reproductions': []
        }

    # Registrar la reproducción de la canción
    organizado[artist_name]['myl_album'][album_name]['myl_songs'][track_name]['myl_reproductions'].append({
        'ts': ts,
        'ms_played': ms_played,
        'skipped': skipped
    })


# Convertir el diccionario organizado a una lista
organizado_list = [{'master_metadata_album_artist_name': artist_name,
                    'myl_album': [{'master_metadata_album_album_name': album_name,
                                   'myl_songs': [{'master_metadata_track_name': track_name,
                                                  'spotify_track_uri': track_uri,
                                                  'myl_reproductions': song_details['myl_reproductions']} 
                                                 for track_name, song_details in album_details['myl_songs'].items()]}
                                  for album_name, album_details in details['myl_album'].items()]}
                   for artist_name, details in organizado.items()]

with open('Datos/Streaming_History_Audio_Org.json', 'w',encoding='utf-8') as f:
    json.dump(organizado_list, f,ensure_ascii=False, indent=4)
