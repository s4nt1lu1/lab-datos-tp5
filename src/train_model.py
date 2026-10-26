import csv
from datetime import datetime
import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Rutas para la versión v4 (KNN)
DATA_PATH = "data/processed/abalone_clean.csv"
MODEL_PATH = "models/model_v4.pkl"
METRICS_PATH = "results/metrics_v4.json"
LOG_PATH = "results/experiments_log.csv"

# Parámetros reproducibles (Experimento 4: KNeighborsRegressor)
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_NEIGHBORS = 10
WEIGHTS = "distance"

def train():
  df = pd.read_csv(DATA_PATH)

  X = df.drop(columns=["age", "rings"])
  y = df["age"]

  # divido train y test
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
  )
  # Pipeline con KNN (el escalado SÍ importa: KNN usa distancias)
  hyperparams = {
      "n_neighbors": N_NEIGHBORS,
      "weights": WEIGHTS,
  }

  pipeline = Pipeline([
      ("scaler", StandardScaler()),
      ("regressor", KNeighborsRegressor(**hyperparams)),
  ])

  pipeline.fit(X_train, y_train)

  y_pred = pipeline.predict(X_test)
  mae = float(mean_absolute_error(y_test, y_pred))
  rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
  r2 = float(r2_score(y_test, y_pred))

  # guardo el modelo comprimido
  os.makedirs("models", exist_ok=True)
  joblib.dump(pipeline, MODEL_PATH, compress=3)

  # guardo métricas
  os.makedirs("results", exist_ok=True)
  metrics_data = {
      "model_version": "v4",
      "algorithm": "KNeighborsRegressor",
      "random_state": RANDOM_STATE,
      "hyperparameters": hyperparams,
      "metrics": {
          "MAE": round(mae, 4),
          "RMSE": round(rmse, 4),
          "R2": round(r2, 4),
      },
  }
  with open(METRICS_PATH, "w", encoding="utf-8") as f:
    json.dump(metrics_data, f, indent=4)

  # guardo historial de exp
  fieldnames = [
      "experiment_id",
      "timestamp",
      "model_version",
      "hyperparameters",
      "mae",
      "rmse",
      "r2",
  ]
  file_exists = os.path.exists(LOG_PATH)

  with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not file_exists:
      writer.writeheader()
    writer.writerow({
        "experiment_id": "EXP-04",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_version": "v4",
        "hyperparameters": json.dumps(hyperparams),
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4),
    })


if __name__ == "__main__":
  train()