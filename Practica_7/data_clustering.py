import pandas as pd
from sklearn.cluster import KMeans
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

# Plot the original scatter plot and the K-Means clustered plot side by side
fig, axs = plt.subplots(1, 2, figsize=(20, 6), sharey=True)

# Original scatter plot
axs[0].scatter(most_played_song_data['date'], most_played_song_data['hour'], alpha=0.6, edgecolors='w', linewidth=0.5)
axs[0].set_title(f'Original: Reproducción por Hora para "{most_played_song}"')
axs[0].set_xlabel('Fecha')
axs[0].set_ylabel('Hora del Día')
axs[0].tick_params(axis='x', rotation=45)
axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)  # Add finer grid lines
axs[0].set_ylim(0, 23)  # Set y-axis limits to show all hours
axs[0].xaxis.set_major_locator(plt.MaxNLocator(10))  # Set major ticks for x-axis
axs[0].xaxis.set_minor_locator(plt.MaxNLocator(50))  # Set minor ticks for x-axis
axs[0].yaxis.set_major_locator(plt.MaxNLocator(12))  # Set major ticks for y-axis
axs[0].yaxis.set_minor_locator(plt.MaxNLocator(24))  # Set minor ticks for y-axis

# Prepare data for KMeans clustering
clustering_data = most_played_song_data.copy()
clustering_data['date'] = clustering_data['date'].map(pd.Timestamp.toordinal)  # Convert date to ordinal for clustering

# Suponiendo que el número óptimo de clusters es 4
optimal_clusters = 5
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
clustering_data['cluster'] = kmeans.fit_predict(clustering_data[['date', 'hour']])

# Convert ordinal back to date for plotting
clustering_data['date'] = clustering_data['date'].map(pd.Timestamp.fromordinal)

# Plot the K-Means clustered scatter plot
for cluster in np.unique(clustering_data['cluster']):
    cluster_data = clustering_data[clustering_data['cluster'] == cluster]
    axs[1].scatter(cluster_data['date'], cluster_data['hour'], label=f'Cluster {cluster}', alpha=0.6)

axs[1].set_title(f'K-Means Clustering por Hora para "{most_played_song}"')
axs[1].set_xlabel('Fecha')
axs[1].tick_params(axis='x', rotation=45)
axs[1].legend()
axs[1].grid(True, which='both', linestyle='--', linewidth=0.5)  # Add finer grid lines
axs[1].set_ylim(0, 23)  # Set y-axis limits to show all hours
axs[1].xaxis.set_major_locator(plt.MaxNLocator(10))  # Set major ticks for x-axis
axs[1].xaxis.set_minor_locator(plt.MaxNLocator(50))  # Set minor ticks for x-axis
axs[1].yaxis.set_major_locator(plt.MaxNLocator(12))  # Set major ticks for y-axis
axs[1].yaxis.set_minor_locator(plt.MaxNLocator(24))  # Set minor ticks for y-axis

plt.tight_layout()
plt.show()
