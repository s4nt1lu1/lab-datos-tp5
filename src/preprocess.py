import pandas as pd

RAW_DATA_PATH = "data/raw/abalone_raw.csv"
PROCESSED_DATA_PATH = "data/processed/abalone_clean.csv"

COLUMNS = [
    "sex",
    "length",
    "diameter",
    "height",
    "whole_weight",
    "shucked_weight",
    "viscera_weight",
    "shell_weight",
    "rings",
]


def clean_abalone_data(ruta_entrada, ruta_salida) -> None:
  df = pd.read_csv(ruta_entrada, header=None, names=COLUMNS)

  # creo age
  df["age"] = df["rings"] + 1.5

  # borro el outlier de height
  mask_valid = (df["height"] > 0) & (df["height"] <= 0.4)
  df_clean = df[mask_valid].copy()

  # one-hot de 'sex'
  df_clean = pd.get_dummies(
      df_clean, columns=["sex"], prefix="sex", dtype=int
  )

  df_clean.to_csv(ruta_salida, index=False)


if __name__ == "__main__":
  clean_abalone_data(RAW_DATA_PATH, PROCESSED_DATA_PATH)