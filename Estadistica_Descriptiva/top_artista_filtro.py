import pandas as pd
from datetime import datetime

# Cargar los datos de streaming
def load_streaming_data(file_path):
    return pd.read_csv(file_path)

# Función mejorada para análisis con parámetros específicos
def analyze_streaming_data_improved(df, group_by='track', skip_filter=None, start_date=None, end_date=None):
    """
    Realiza un análisis de estadística descriptiva de los datos de streaming con parámetros específicos.
    
    Parámetros:
    - df: DataFrame de Pandas con los datos de streaming.
    - group_by: Criterio de agrupación ('track', 'album', 'artist').
    - skip_filter: Filtrar por canciones saltadas ('skipped', 'not_skipped', None).
    - start_date: Fecha de inicio para filtrar los datos (YYYY-MM-DD).
    - end_date: Fecha de fin para filtrar los datos (YYYY-MM-DD).
    
    Retorna: DataFrame de Pandas con el análisis realizado.
    """
    # Conversión de fechas a formato adecuado si se proporcionan
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Aplicar filtros según los parámetros
    if start_date:
        df = df[df['ts'] >= start_date]
    if end_date:
        df = df[df['ts'] <= end_date]
    if skip_filter == 'skipped':
        df = df[df['skipped'] == 1.0]
    elif skip_filter == 'not_skipped':
        df = df[pd.isnull(df['skipped'])]
    
    # Convertir ms_played a minutos
    df['minutes_played'] = df['ms_played'] / 60000
    
    # Definir el campo por el cual agrupar
    if group_by == 'track':
        group_field = 'master_metadata_track_name'
    elif group_by == 'album':
        group_field = 'master_metadata_album_album_name'
    elif group_by == 'artist':
        group_field = 'master_metadata_album_artist_name'
    
    # Realizar el agrupamiento y calcular estadísticas
    grouped = df.groupby(group_field).agg(
        plays_count=('ts', 'count'),
        total_minutes_played=('minutes_played', 'sum'),
        avg_minutes_per_play=('minutes_played', 'mean')
    ).reset_index()
    
    return grouped.sort_values(by='plays_count', ascending=False)

# Ejemplo de cómo cargar los datos y realizar un análisis
file_path = 'Datos/Streaming_History_Audio.csv'  # Cambia esto por la ruta real a tu archivo CSV
data = load_streaming_data(file_path)

# Ejemplo de uso de la función con parámetros específicos
# Ajusta los parámetros según lo que quieras analizar
group_by = 'track'  # Opciones: 'track', 'album', 'artist'
skip_filter = 'None'  # Opciones: None, 'skipped', 'not_skipped'
start_date = '2023-01-01'  # Formato YYYY-MM-DD
end_date = '2024-01-01'  # Formato YYYY-MM-DD

analysis_result = analyze_streaming_data_improved(data, group_by=group_by, skip_filter=skip_filter, start_date=start_date, end_date=end_date)
print(analysis_result.head())  # Muestra las primeras filas del resultado
