import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures

# Load the dataset
FILE_PATH = 'Datos/Streaming_History_Audio.csv'
data = pd.read_csv(FILE_PATH)

# Calculate the average duration of each song and its total play count
song_stats = data.groupby('master_metadata_track_name').agg(
    avg_duration=('ms_played', 'mean'),
    total_plays=('ms_played', 'count')  # Use count instead of sum
).reset_index()

# Filter for songs with an average duration of less than 10 minutes (600,000 ms)
filtered_song_stats = song_stats[song_stats['avg_duration'] < 600000]

# Extract variables for modeling
avg_durations = filtered_song_stats['avg_duration']
total_plays = filtered_song_stats['total_plays']

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(filtered_song_stats[['avg_duration', 'total_plays']])
scaled_avg_duration = scaled_data[:, 0]
scaled_total_plays = scaled_data[:, 1]

# Fit Normal distribution to average durations
mu_duration, std_duration = norm.fit(avg_durations)
x_duration = np.linspace(avg_durations.min(), avg_durations.max(), 1000)
normal_pdf_duration = norm.pdf(x_duration, mu_duration, std_duration) * max(total_plays) / max(norm.pdf(x_duration, mu_duration, std_duration))

# Fit Quadratic Models
X_scaled = scaled_avg_duration.reshape(-1, 1)
y_scaled = scaled_total_plays
poly = PolynomialFeatures(degree=2)
X_scaled_poly = poly.fit_transform(X_scaled)

# Quadratic Model: Normal assumption
normal_quad_model = LinearRegression()
normal_quad_model.fit(X_scaled_poly, y_scaled)
y_pred_normal_quad = normal_quad_model.predict(X_scaled_poly)

# Evaluate Model
r2_normal_quad = r2_score(y_scaled, y_pred_normal_quad)
mse_normal_quad = mean_squared_error(y_scaled, y_pred_normal_quad)

# Plot: Original scatter plot and Normal distribution
fig, axs = plt.subplots(1, 2, figsize=(12, 6), tight_layout=True)

# Original scatter plot
axs[0].scatter(avg_durations, total_plays, alpha=0.7, label='Original Data', color='blue')
axs[0].set_title('Original Scatter Plot')
axs[0].set_xlabel('Average Song Duration (ms)')
axs[0].set_ylabel('Total Plays')
axs[0].grid(True)

# Normal distribution fit
axs[1].hist(avg_durations, bins=30, density=True, alpha=0.6, color='blue', label='Duration Data')
axs[1].plot(x_duration, normal_pdf_duration, label='Normal Fit', color='red', linewidth=2)
axs[1].set_title('Normal Distribution Fit')
axs[1].set_xlabel('Average Song Duration (ms)')
axs[1].set_ylabel('Density')
axs[1].legend()
axs[1].grid(True)

plt.show()

# Overlay Normal distribution on the original scatter plot
plt.figure(figsize=(10, 6))

# Original scatter plot
plt.scatter(avg_durations, total_plays, alpha=0.7, label='Original Data', color='blue')

# Overlay Normal distribution fit
plt.plot(x_duration, normal_pdf_duration, label='Normal Fit', color='red', linewidth=2)

plt.title('Original Data with Overlaid Normal Distribution')
plt.xlabel('Average Song Duration (ms)')
plt.ylabel('Total Plays')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
