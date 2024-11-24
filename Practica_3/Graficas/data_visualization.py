import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Cargar los datos
data = pd.read_csv('Datos/Streaming_History_Audio.csv')

# Convertir ts a datetime y extraer la hora
data['ts'] = pd.to_datetime(data['ts'])
data['hour'] = data['ts'].dt.hour
data['date'] = data['ts'].dt.date
data['month'] = data['ts'].dt.to_period('M')
data['year'] = data['ts'].dt.to_period('Y')
data['minutes_played'] = data['ms_played'] / 60000  # Convertir ms a minutos

# Excluir reproducciones de un artista específico, por ejemplo, "Artista X"
data = data[(data['skipped'] != False)]
data = data[(data['ms_played'] > 1000)]

# Funciones para graficar
def plot_top_songs():
    top_songs = data['master_metadata_track_name'].value_counts().head(50)
    plt.figure(figsize=(15, 9))
    sns.barplot(x=top_songs.values, y=top_songs.index, color='purple')
    plt.title('Top 50 Canciones Más Reproducidas')
    plt.xlabel('Número de Reproducciones')
    plt.ylabel('Canción')
    plt.show()

def plot_daily_plays():
    daily_plays = data.groupby('date').size()
    plt.figure(figsize=(15, 9))
    daily_plays.plot(title='Reproducciones Diarias', color='purple')
    plt.xlabel('Fecha')
    plt.ylabel('Reproducciones')
    plt.show()

# Removed plot_scatter_hour_vs_ms_played function

def plot_top_artists():
    top_artists = data['master_metadata_album_artist_name'].value_counts().head(25)
    plt.figure(figsize=(15, 9))
    sns.barplot(x=top_artists.values, y=top_artists.index, palette='coolwarm')
    plt.title('Top 25 Artistas Más Populares')
    plt.xlabel('Número de Reproducciones')
    plt.ylabel('Artista')
    plt.show()

def plot_reason_start():
    plt.figure(figsize=(15, 9))
    sns.countplot(y='reason_start', data=data, order=data['reason_start'].value_counts().index, palette='autumn')
    plt.title('Razones de Inicio de Reproducción')
    plt.xlabel('Cantidad')
    plt.ylabel('Razón')
    plt.show()

def plot_reason_end():
    plt.figure(figsize=(15, 9))
    sns.countplot(y='reason_end', data=data, order=data['reason_end'].value_counts().index, palette='spring')
    plt.title('Razones de Finalización de Reproducción')
    plt.xlabel('Cantidad')
    plt.ylabel('Razón')
    plt.show()

# Removed plot_skipped_vs_completed function

def plot_duration_histogram():
    duration_minutes = data['ms_played'] / 60000  # Convertir ms a minutos
    plt.figure(figsize=(15, 9))
    plt.hist(duration_minutes, bins=50, color='purple', alpha=0.7)
    plt.title('Histograma de Duración de Reproducciones en Minutos')
    plt.xlabel('Duración (minutos)')
    plt.ylabel('Frecuencia')
    plt.show()

def plot_avg_duration_vs_frequency():
    song_data = data.groupby('master_metadata_track_name').agg(
        frequency=('master_metadata_track_name', 'count'),
        total_ms_played=('ms_played', 'sum')
    ).reset_index()
    song_data['avg_duration_ms'] = song_data['total_ms_played'] / song_data['frequency']
    song_data = song_data[song_data['avg_duration_ms'] > 0]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(song_data['frequency'], song_data['avg_duration_ms'], alpha=0.6)
    plt.title('Duración promedio por canción vs Número de reproducciones')
    plt.xlabel('Número de reproducciones por canción')
    plt.ylabel('Duración promedio por canción (ms)')
    plt.grid(True)
    plt.show()

def plot_playback_distribution_by_hour():
    hourly_data = data.groupby('hour').agg(total_ms_played=('ms_played', 'sum')).reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.plot(hourly_data['hour'], hourly_data['total_ms_played'], marker='o')
    plt.title('Distribución de tiempo reproducido durante el día')
    plt.xlabel('Hora del día')
    plt.ylabel('Tiempo total reproducido (ms)')
    plt.grid(True)
    plt.xticks(range(0, 24))
    plt.show()

# Function to create the scatter plot
def scatter_plot_playtime_vs_timestamp(data_cleaned):
    sampled_data = data_cleaned.sample(5000, random_state=42)
    plt.figure(figsize=(12, 6))
    plt.scatter(sampled_data['ts'], sampled_data['ms_played'], alpha=0.5)
    plt.title('Scatter Plot of Playtime Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Milliseconds Played')
    plt.show()

# Crear el menú
def display_menu():
    opcion = ''
    while opcion != '10':  # Updated exit option number
        print("\nMenú de Gráficas")
        print("1. Top 25 Canciones Más Reproducidas")
        print("2. Reproducciones Diarias")
        # Removed option 3
        print("3. Top 10 Artistas Más Populares")
        print("4. Razones de Inicio de Reproducción")
        print("5. Razones de Finalización de Reproducción")
        # Removed option 7
        print("6. Histograma de Duración de Reproducciones en Minutos")
        print("7. Duración promedio por canción vs. Número de reproducciones")
        print("8. Distribución de tiempo reproducido durante el día")
        print("9. Scatter Plot of Playtime Over Time")
        print("10. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            plot_top_songs()
        elif opcion == '2':
            plot_daily_plays()
        elif opcion == '3':
            plot_top_artists()
        elif opcion == '4':
            plot_reason_start()
        elif opcion == '5':
            plot_reason_end()
        elif opcion == '6':
            plot_duration_histogram()
        elif opcion == '7':
            plot_avg_duration_vs_frequency()
        elif opcion == '8':
            plot_playback_distribution_by_hour()
        elif opcion == '9':
            scatter_plot_playtime_vs_timestamp(data)
        elif opcion == '10':
            return
        else:
            print("Opción no válida. Por favor, intenta nuevamente.")

if __name__ == "__main__":
    display_menu()