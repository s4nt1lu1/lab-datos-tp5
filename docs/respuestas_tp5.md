#  RESPUESTAS CONCEPTUALES
## EJERCICIO 2
### 1. ¿Qué información de `data_log.json` es imprescindible para reconstruir el dataset y alcanza con el registro actual?
Para reconstruir el dataset procesado a partir del original de forma exacta se necesita conocer:
- El archivo de entrada (`source`) y su integridad (idealmente un hash/checksum SHA-256).
- El orden exacto de las operaciones y sus parámetros numéricos precisos: fórmula de la variable derivada (`age = rings + 1.5`), umbral exacto de filtrado de atípicos (`0 < height <= 0.4`) y esquema del One-Hot Encoding de `sex` (`sex_F`, `sex_I`, `sex_M`).

**¿Alcanza con el registro actual?** Sí alcanza en conjunto con `src/preprocess.py` porque los criterios están explícitos. Si solo se tuviera el JSON de forma aislada, faltaría el checksum del archivo original para asegurar que no fue alterado y detalles técnicos menores como el tipo de dato o orden de las columnas generadas.

### 2. ¿Qué pasaría si el dataset pesara varios GB o cambiara todas las semanas al versionarlo en Git?
Git almacena instantáneas (snapshots) completas de cada versión de un archivo y, al ser distribuido (DVCS), cada `git clone` descarga todo el historial. Si un dataset de varios GB cambiara todas las semanas, el repositorio `.git` crecería exponencialmente (decenas de GB), volviendo las operaciones de `clone`, `pull` y `push` extremadamente lentas e incompatibles con los límites de plataformas como GitHub. En ese caso debe separarse el código de los datos usando **DVC** y almacenamiento en la nube (como S3), guardando en Git únicamente archivos puntero livianos (.dvc). (no entendi mucho esto lo extraje tal cual de la teoria)


## Ejercicio 4: Cambios realizados en `src/train_model.py` (Rama `exp/hiperparametros`)
En la rama `exp/hiperparametros` se entrenó una nueva versión del modelo (`v2` / `EXP-02`) realizando las siguientes modificaciones sobre `src/train_model.py`:
1. **Ajuste de hiperparámetros del `RandomForestRegressor`:**
   - Se incrementó `N_ESTIMATORS` de `100` a `200` (mayor estabilidad del ensamble).
   - Se redujo `MAX_DEPTH` de `15` a `8` (regularización de la profundidad de los árboles para reducir el sobreajuste que presentaba la versión `v1`).
   - Se mantuvo `RANDOM_STATE = 42` y `TEST_SIZE = 0.2` para que la partición de evaluación sea exactamente comparable con `v1`.
2. **Versionado de artefactos y métricas:**
   - El pipeline entrenado se serializó con compresión en `models/model_v2.pkl` (`compress=3`).
   - Las métricas y configuración se exportaron a `results/metrics_v2.json`.
   - Se añadió el registro `EXP-02` en `results/experiments_log.csv`.
3. **Comparación de desempeño obtenida:**
   - **Modelo `v1` (`n_estimators=100, max_depth=15`):** `MAE = 1.5589` | `RMSE = 2.2467` | `R2 = 0.5787`
   - **Modelo `v2` (`n_estimators=200, max_depth=8`):** `MAE = 1.5281` | `RMSE = 2.2170` | `R2 = 0.5898` *(mejora en las tres métricas).*


## Ejercicio 4 (Parte 2): Rama `exp/otro-algoritmo` y Resolución Manual de Conflictos
### 1. Cambios realizados en la rama `exp/otro-algoritmo` (`model_v3`)
Partiendo del `main` original, se modificó `src/train_model.py` reemplazando `RandomForestRegressor` por **`GradientBoostingRegressor`** (`n_estimators=150`, `learning_rate=0.05`, `max_depth=4`, `random_state=42`), guardando `models/model_v3.pkl`, `results/metrics_v3.json` y la fila `EXP-03` en `results/experiments_log.csv`:
- **Resultado obtenido (`v3`):** `MAE = 1.5239` | `RMSE = 2.2048` | `R2 = 0.5943` (mejor modelo de los tres experimentos).

### 2. Qué mostraban los archivos en conflicto al integrar la segunda rama a `main`
Al integrar primero `exp/hiperparametros` a `main` y luego ejecutar `git merge exp/otro-algoritmo`, Git detuvo la fusión automática de tres vías (*three-way merge*) e insertó los marcadores de conflicto porque ambas ramas habían modificado las mismas líneas a partir del mismo ancestro común.

```text
<<<<<<< HEAD
EXP-02,2026-10-25 04:18:19,v2,"{""n_estimators"": 200, ""max_depth"": 8, ""random_state"": 42}",1.5281,2.217,0.5898
=======
EXP-01,2026-10-25 04:35:31,v1,"{""n_estimators"": 100, ""max_depth"": 15, ""random_state"": 42}",1.5589,2.2467,0.5787
EXP-03,2026-10-25 04:37:48,v3,"{""n_estimators"": 150, ""learning_rate"": 0.05, ""max_depth"": 4, ""random_state"": 42}",1.5239,2.2048,0.5943
>>>>>>> exp/otro-algoritmo
```

### ¿Como resolvimos el conflicto?
En results/experiments_log.csv y README.md: Se conservaron los registros de ambos experimentos nuevos (EXP-02 y EXP-03) en orden secuencial, se eliminó la fila duplicada accidental de EXP-01 (04:35:31) y se borraron las líneas de los marcadores (<<<<<<<, =======, >>>>>>>), ya que la tabla debe preservar todas las pruebas válidas para compararlas

En src/train_model.py: Se conservó la versión de exp/otro-algoritmo (v3 con GradientBoostingRegressor) usando git checkout --theirs src/train_model.py, dado que fue el modelo con mejor desempeño en test (R^2=0.5943)

