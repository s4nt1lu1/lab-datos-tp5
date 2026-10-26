# Laboratorio de Datos II - TP5

Proyecto de la materia "Laboratorio de datos II", perteneciente a la carrera de Ingenieria en Inteligencia Artificial de la Universidad Nacional del Litoral.

El objetivo de este trabajo es implementar un pipeline reproducible de análisis de datos para estimar la edad de moluscos (*Abalone*) a partir de medidas físicas.

## Requisitos y Entorno

- **Versión de Python:** 3.13.7

### Reproducción del Entorno Virtual

Se deben instalar las dependencias, para ello ejecutar:

#### Crear el entorno virtual
```bash
uv venv
```

#### Instalar dependencias
```bash
uv pip install -r requirements.txt
```

## Ejecución del Pipeline

### Preprocesamiento 
Para hacer las transforamciones de los datos y generar el dataset limpio:
```bash
python src/preprocess.py
```

### Entrenamiento y Evaluación

Para entrenar el modelo, evaluar sus métricas y guardar los resultados:

```bash
python src/train_model.py
```

## Estructura del proyecto

```text
abalone_project/
├── data/
│   ├── raw/                # Datos originales sin modificar
│   ├── processed/          # Datos transformados y limpios
│   └── data_log.json       # Registro de transformaciones realizadas
├── models/                 # Modelos serializados
├── results/
│   ├── metrics_v1.json     # Métricas y parámetros del modelo
│   └── experiments_log.csv # Registro histórico de experimentos
├── src/
│   ├── preprocess.py       # Limpieza y preprocesamiento de los datos
│   └── train_model.py      # Script de entrenamiento y evaluación
├── README.md               
└── requirements.txt
```

## Resultados

- **EXP-01 (`model_v1` - RandomForestRegressor `n_estimators=100, max_depth=15`):** MAE = 1.5589 | RMSE = 2.2467 | R² = 0.5787
- **EXP-02 (`model_v2` - RandomForestRegressor `n_estimators=200, max_depth=8`):** MAE = 1.5281 | RMSE = 2.2170 | R² = 0.5898
- **EXP-03 (`model_v3` - GradientBoostingRegressor `n_estimators=150, lr=0.05, max_depth=4`):** MAE = 1.5239 | RMSE = 2.2048 | R² = 0.5943
- **EXP-04 (`model_v4` - KNeighborsRegressor `n_neighbors=10, weights="distance"`):** MAE = 1.5742 | RMSE = 2.3323 | R² = 0.546
