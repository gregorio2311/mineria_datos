import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Cargar los datos
file_path = 'Datos/Streaming_History_Audio.csv'  # Asegúrate de reemplazarlo con la ruta correcta
data = pd.read_csv(file_path)

# Preparar los datos (convertir tiempo y filtrar)
data['minutes_played'] = data['ms_played'] / 60000
data['ts'] = pd.to_datetime(data['ts'])

# Identificar el segundo artista más escuchado
artist_playtime = data.groupby('master_metadata_album_artist_name')['minutes_played'].sum().sort_values(ascending=False)
second_artist = artist_playtime.index[1]

# Filtrar datos del segundo artista más escuchado
second_artist_data = data[data['master_metadata_album_artist_name'] == second_artist]
second_artist_data = second_artist_data[second_artist_data['minutes_played'] > 0]
second_artist_data['ts_numeric'] = second_artist_data['ts'].map(pd.Timestamp.timestamp)

# Crear variables predictoras y objetivo
X = second_artist_data[['ts_numeric']]
y = second_artist_data['minutes_played']

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo KNN inicial
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

# Optimizar el modelo con GridSearchCV
param_grid = {'n_neighbors': range(1, 21)}
grid_search = GridSearchCV(KNeighborsRegressor(), param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Mejor número de vecinos y nuevo modelo
best_k = grid_search.best_params_['n_neighbors']
best_knn = KNeighborsRegressor(n_neighbors=best_k)
best_knn.fit(X_train, y_train)
optimized_y_pred = best_knn.predict(X_test)

# Crear gráficos
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))

# Scatter de datos reales
axes[0].scatter(second_artist_data['ts'], second_artist_data['minutes_played'], alpha=0.6, label="Datos Reales", marker='x')
axes[0].set_title(f"Datos Reales de Tiempo de Reproducción - {second_artist}")
axes[0].set_xlabel("Fecha")
axes[0].set_ylabel("Tiempo de Reproducción (min)")
axes[0].tick_params(axis='x', rotation=45)
axes[0].legend()
axes[0].grid(True, linestyle='--', alpha=0.5)

# Predicción del modelo optimizado
sorted_X_test = X_test.sort_values(by='ts_numeric')
sorted_optimized_y_pred = best_knn.predict(sorted_X_test)
axes[1].scatter(second_artist_data['ts'], second_artist_data['minutes_played'], alpha=0.6, label="Datos Reales", marker='x')
axes[1].plot(
    sorted_X_test['ts_numeric'].map(pd.Timestamp.fromtimestamp),
    sorted_optimized_y_pred,
    color='green',
    label=f"Predicción del Modelo Optimizado (KNN, k={best_k})",
    linewidth=2,
)
axes[1].set_title(f"Tiempo de Reproducción - {second_artist}")
axes[1].set_xlabel("Fecha")
axes[1].set_ylabel("Tiempo de Reproducción (min)")
axes[1].tick_params(axis='x', rotation=45)
axes[1].legend()
axes[1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
