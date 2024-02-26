import json

document = 'Datos/Streaming_History_Audio.json'

with open(document, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Contamos el numero de objetos en nuestro archivo Json
if isinstance(data, list):
    number_of_objects = len(data)
else:
    number_of_objects = 1

print(f"There are {number_of_objects} objects in the JSON file.")

# Funcion para eliminar campos indeseados y entradas repetidas
def remove_field(json_list):
    campos_x = [
        'username', 'platform', 'conn_country', 'ip_addr_decrypted',
        'user_agent_decrypted', 'episode_name', 'episode_show_name',
        'spotify_episode_uri', 'reason_start', 'reason_end', 'shuffle',
        'offline', 'offline_timestamp', 'incognito_mode'
    ]
    
    # Lista para almacenar los objetos únicos
    unique_json_list = []
    
    # Variable para guardar el 'ts' del objeto anterior
    previous_ts = None
    
    for item in json_list:
        # Comprobar si el 'ts' actual es diferente al 'ts' del objeto anterior
        if item["ts"] != previous_ts:
            # Actualizar el 'ts' 
            previous_ts = item["ts"]
            
            # Remover los campos especificados
            for field in campos_x:
                item.pop(field, None)
            
            # Añadir el objeto a la lista de objetos únicos
            unique_json_list.append(item)
    
    return unique_json_list


data = remove_field(data)

with open('Datos/Streaming_History_Audio.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
