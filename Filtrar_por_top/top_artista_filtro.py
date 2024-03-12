import pandas as pd
from datetime import datetime

def load_streaming_data(file_path):
    return pd.read_csv(file_path)

def analyze_streaming_data_improved(df, group_by='track', skip_filter=None, start_date=None, end_date=None):

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
    
    if start_date:
        df = df[df['ts'] >= start_date]
    if end_date:
        df = df[df['ts'] <= end_date]
    if skip_filter == 'skipped':
        df = df[df['skipped'] == 1.0]
    elif skip_filter == 'not_skipped':
        df = df[pd.isnull(df['skipped'])]
    
    df['minutes_played'] = df['ms_played'] / 60000
    
    if group_by == 'track':
        group_field = 'master_metadata_track_name'
    elif group_by == 'album':
        group_field = 'master_metadata_album_album_name'
    elif group_by == 'artist':
        group_field = 'master_metadata_album_artist_name'
    
    grouped = df.groupby(group_field).agg(
        plays_count=('ts', 'count'),
        total_minutes_played=('minutes_played', 'sum'),
        avg_minutes_per_play=('minutes_played', 'mean')
    ).reset_index()
    
    return grouped.sort_values(by='plays_count', ascending=False)


file_path = 'Datos/Streaming_History_Audio.csv'  
data = load_streaming_data(file_path)

group_by = 'track'  
skip_filter = 'None'  
start_date = '2023-01-01'  
end_date = '2024-01-01'  

analysis_result = analyze_streaming_data_improved(data, group_by=group_by, skip_filter=skip_filter, start_date=start_date, end_date=end_date)
print(analysis_result.head())  
