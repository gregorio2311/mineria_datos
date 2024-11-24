import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

# Load data
file_path = 'Datos/Streaming_History_Audio.csv'
data = pd.read_csv(file_path)

# Parse datetime and extract date and hour
data['parsed_ts'] = pd.to_datetime(data['ts'])
data['date'] = data['parsed_ts'].dt.date
data['hour'] = data['parsed_ts'].dt.hour

# Identify the most played song
most_played_song = data['master_metadata_track_name'].value_counts().idxmax()

# Filter relevant data
most_played_song_data = data[data['master_metadata_track_name'] == most_played_song][['date', 'hour']]

# Ensure 'date' column is in datetime format
most_played_song_data['date'] = pd.to_datetime(most_played_song_data['date'])

# Convert date to ordinal for clustering
clustering_data = most_played_song_data.copy()
clustering_data['date'] = clustering_data['date'].map(pd.Timestamp.toordinal)

# Split data into training and testing sets
train_data, test_data = train_test_split(clustering_data, test_size=0.2, random_state=42)

# Train KMeans model on training data
optimal_clusters = 5
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
train_data['cluster'] = kmeans.fit_predict(train_data[['date', 'hour']])

# Evaluate the model on the test data
test_data['cluster'] = kmeans.predict(test_data[['date', 'hour']])
silhouette_avg = silhouette_score(test_data[['date', 'hour']], test_data['cluster'])
print(f'Coeficiente de Silueta para los datos de prueba: {silhouette_avg}')

# Convert ordinal back to date for plotting
train_data['date'] = train_data['date'].map(pd.Timestamp.fromordinal)
test_data['date'] = test_data['date'].map(pd.Timestamp.fromordinal)

# Plot the K-Means clustered scatter plot for training data
fig, axs = plt.subplots(1, 2, figsize=(20, 6), sharey=True)

for cluster in np.unique(train_data['cluster']):
    cluster_data = train_data[train_data['cluster'] == cluster]
    axs[0].scatter(cluster_data['date'], cluster_data['hour'], label=f'Cluster {cluster}', alpha=0.6)

axs[0].set_title(f'K-Means Clustering por Hora para "{most_played_song}" (Entrenamiento)')
axs[0].set_xlabel('Fecha')
axs[0].set_ylabel('Hora del Día')
axs[0].tick_params(axis='x', rotation=45)
axs[0].legend()
axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)
axs[0].set_ylim(0, 23)
axs[0].xaxis.set_major_locator(plt.MaxNLocator(10))
axs[0].xaxis.set_minor_locator(plt.MaxNLocator(50))
axs[0].yaxis.set_major_locator(plt.MaxNLocator(12))
axs[0].yaxis.set_minor_locator(plt.MaxNLocator(24))

# Plot the K-Means clustered scatter plot for test data
for cluster in np.unique(test_data['cluster']):
    cluster_data = test_data[test_data['cluster'] == cluster]
    axs[1].scatter(cluster_data['date'], cluster_data['hour'], label=f'Cluster {cluster}', alpha=0.6)

axs[1].set_title(f'K-Means Clustering por Hora para "{most_played_song}" (Prueba)')
axs[1].set_xlabel('Fecha')
axs[1].tick_params(axis='x', rotation=45)
axs[1].legend()
axs[1].grid(True, which='both', linestyle='--', linewidth=0.5)
axs[1].set_ylim(0, 23)
axs[1].xaxis.set_major_locator(plt.MaxNLocator(10))
axs[1].xaxis.set_minor_locator(plt.MaxNLocator(50))
axs[1].yaxis.set_major_locator(plt.MaxNLocator(12))
axs[1].yaxis.set_minor_locator(plt.MaxNLocator(24))

plt.tight_layout()
plt.show()