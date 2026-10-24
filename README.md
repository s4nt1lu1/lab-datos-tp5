# Laboratorio de Datos II - TP5

Proyecto de la materia "Laboratorio de datos II", perteneciente a la carrera de Ingenieria en Inteligencia Artificial de la Universidad Nacional del Litoral.

El objetivo de este trabajo es implementar un pipeline reproducible de análisis de datos para estimar la edad de moluscos (*Abalone*) a partir de medidas físicas.

## Requisitos y Entorno

- **Versión de Python:** 3.13.7

### Reproducción del Entorno Virtual

Se deben instalar las dependencias, para ello ejecutar:

#### Crear el entorno virtual
uv venv

#### Instalar dependencias
uv pip install -r requirements.txt

## Estructura del proyecto
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