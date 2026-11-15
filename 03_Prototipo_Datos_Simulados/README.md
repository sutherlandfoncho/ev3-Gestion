# Red Metropolitana — Prototipo de laboratorio (EP5–EP6)

> **Origen de datos:** 100 % sintéticos. Ningún archivo contiene datos GPS o validaciones bip! reales de Red Movilidad. Las métricas sirven para comprobar el funcionamiento del software y no para acreditar predicciones operacionales reales.

## Inicio rápido en Windows

1. Instalar **Python 3.10 o superior** y abrir PowerShell dentro de esta carpeta.
2. Instalar dependencias: `python -m pip install -r requirements.txt`.
3. Generar datos, entrenar modelos y reconstruir resultados: `python ejecutar_demo.py`.
4. Abrir el HTML de demostración: `resultado/Dashboard_DEMO_Abrir.html`.
5. Abrir la aplicación interactiva: `python -m streamlit run app_streamlit.py`.
6. Entrar a `http://localhost:8501` si no se abre automáticamente.
7. Ejecutar las pruebas: `python -m unittest discover -s tests -v` (**8 pruebas** en la última ejecución verificada del paquete).

> Nota: en Windows, si el comando `streamlit run ...` no se reconoce, usar **`python -m streamlit run app_streamlit.py`**. Esta opción utiliza el paquete instalado en el mismo intérprete de Python.

## Qué implementa el prototipo

- Genera seis meses de viajes agregados y validaciones bip! **ficticios**; el generador usa una semilla fija (`1102`) para facilitar la reproducibilidad.
- Prepara y cruza registros por fecha, recorrido y franja. Utiliza una variable histórica de demanda y controla que no se incorporen identificadores de usuarios.
- Divide cronológicamente datos de entrenamiento y prueba (4.608 / 1.184 observaciones).
- Compara tres referencias: **tiempo programado**, **regresión lineal regularizada (Ridge)** y **Random Forest**.
- Calcula errores MAE/RMSE y diferencia relativa de MAE entre Centro y Periferia.
- Genera CSV, JSON, notebook exploratorio, pruebas y dos opciones de tablero: HTML local y app Streamlit.

## Resultados reproducibles (solo simulación)

| Indicador | Referencia programada | Ridge | Random Forest |
|---|---:|---:|---:|
| MAE (min) | 4,490 | **1,615** | 1,722 |
| MAE Centro (min) | — | 1,459 | 1,573 |
| MAE Periferia (min) | — | 1,770 | 1,870 |
| Brecha relativa Centro–Periferia | — | **21,29 %** | **18,88 %** |
| Alertas de retraso previsto ≥ 5 min | — | **457** (recalculadas para comparación) | **426** (archivo oficial `alertas_SIMULADAS.csv`) |

**Cómo interpretar:** Ridge tiene el MAE global más bajo, pero supera el umbral *propuesto* de brecha relativa ≤20 % dentro de la simulación. Random Forest cumple ese umbral simulado, aunque su MAE es mayor. No se debe afirmar que uno cumple estos objetivos en la operación real: ambos necesitan validación externa.

**De dónde vienen las alertas:** las columnas `prediccion_min`, `retraso_predicho_min` y `alerta` del archivo de predicciones corresponden a **Random Forest**. La columna `prediccion_lineal_min` es Ridge. Las 457 alertas Ridge se obtienen aplicando el mismo umbral de 5 minutos a `prediccion_lineal_min - minutos_programados`; no son el archivo de alertas que genera actualmente la aplicación.

**Piso de ruido del simulador:** el objetivo se construye combinando duración programada, congestión, lluvia, demanda, efectos por recorrido y ruido gaussiano (σ = 1,9 min Centro / 2,25 min Periferia). El MAE esperado solo del componente de ruido es aproximadamente 1,52/1,80 minutos. Esto ayuda a explicar por qué los resultados aparentan ser tan buenos: no demuestra precisión real.

## Qué falta y qué no debe afirmarse

- No se entrenó con datos de buses de Santiago ni se comprobó reducción de tiempos de espera.
- No se validó el ETA operacional, el desempeño por comuna real ni el cumplimiento regulatorio sobre datos personales reales.
- No existe autorización o acta de aceptación del Directorio Operacional de Red Movilidad.
- El tablero local no equivale a una historia de cambios autenticada en Trello/Jira.
- La aplicación Streamlit **ha sido ejecutada en un PC del equipo según confirmación del usuario**. Su captura de pantalla aún debe adjuntarse y revisarse; no se debe afirmar que está desplegada institucionalmente.

## Evidencias y capturas

- Ejecutable: `ejecutar_demo.py`.
- Datos generados: `datos/`.
- Resultados: `resultado/metricas_SIMULADAS.json`, `resultado/predicciones_SIMULADAS.csv`, `resultado/alertas_SIMULADAS.csv` y archivos `mae_por_*`.
- Código: `src/generar_datos.py`, `src/procesar_modelo.py`, `src/crear_dashboard.py`, `app_streamlit.py`.
- Notebook: `EDA_Datos_SIMULADOS.ipynb`.
- Pruebas: `tests/test_demo.py`.
- Captura de la app Streamlit al ejecutarse localmente: guardar en `../06_Evidencias/streamlit_dashboard_real.png`.
- Captura general del Trello auténtico: `../06_Evidencias/trello_tablero_real.png`.
- Captura del historial/comentarios de una tarjeta: `../06_Evidencias/trello_historial_tarjeta.png`.

## Próxima etapa para usar datos reales

Pedir autorización y esquema de datos, definir con el cliente retraso/ETA operacional, garantizar la privacidad, verificar la calidad por zonas, reentrenar modelos y comparar MAE y brecha con muestras temporales independientes. La elección entre Ridge y Random Forest se deberá hacer considerando **precisión y equidad simultáneamente**.

## Evidencias remotas (agregar cuando existan)

- **Repositorio GitHub:** pendiente de URL verificable.
- **Tablero Trello/Jira:** pendiente de URL verificable.
- **Notebook publicado:** pendiente; actualmente está dentro del proyecto local.
