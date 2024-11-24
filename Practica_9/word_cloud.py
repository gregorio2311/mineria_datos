import pandas as pd

# Cargar los datos
file_path = 'Datos/Streaming_History_Audio.csv'
data = pd.read_csv(file_path)

# Imprimir las columnas del DataFrame para verificar el nombre correcto

# Filtrar datos para incluir solo reproducciones después de 2020
data['ts'] = pd.to_datetime(data['ts'])
filtered_data = data[data['ts'].dt.year > 2022]

# Asumiendo que la columna correcta es 'master_metadata_album_album_name'
album_names = filtered_data['master_metadata_album_artist_name'].dropna()

# Crear una cadena de texto con todos los nombres de los álbumes
text = ' '.join(album_names)

# Crear el Word Cloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Mostrar el Word Cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud de Álbumes (Reproducciones después de 2021)')
plt.show()
