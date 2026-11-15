# Entrega EP5 y EP6 · Gestión de Proyectos de Datos

Proyecto: **Análisis y predicción de retrasos en la Red Metropolitana de Movilidad**.
Integrantes de la planificación original: **Diego Echeverria, Cristóbal Silva y Alfonso Sutherland**.

## Qué entregar
- `01_Informe_EP5/Informe_EP5_Red_Metropolitana.pdf` (informe 5–8 páginas; editable en DOCX).
- `02_Presentacion_EP6/Presentacion_EP6_Red_Metropolitana.pptx` (defensa de 10 min; también en PDF).
- Evidencias técnicas: carpeta `03_Prototipo_Datos_Simulados/`.
- Evidencias y registro de tareas: carpeta `04_Seguimiento/`.
- Ayuda para la exposición: carpeta `05_Guion_y_Defensa/`.

## Para probar el prototipo
1. Instalar Python 3.10 o posterior.
2. Abrir terminal en `03_Prototipo_Datos_Simulados`.
3. Ejecutar `pip install -r requirements.txt`, luego `python ejecutar_demo.py`.
4. Abrir `resultado/Dashboard_DEMO_Abrir.html`.
5. Ejecutar `python -m unittest discover -s tests -v` para revisar los siete controles.
6. Si deseas explorar el dataset, abrir `EDA_Datos_SIMULADOS.ipynb` con Jupyter o VS Code.

## Para mostrar la gestión
Abrir `04_Seguimiento/Tablero_Offline_Abrir.html`. Las tareas también están en `Tareas_para_copiar_en_Trello_o_Jira.csv` para migración. **No hay enlace de Trello/Jira registrado ni verificación de un tablero conectado.** Debe crearse en una cuenta real si el docente lo exige.

## Estado y límites que se deben defender
- El código y los tests se pueden ejecutar. Sus resultados provienen solo de **datos simulados**.
- No se utilizaron datos reales de GPS, tarjetas bip! ni usuarios, ni se obtuvo aceptación del Directorio de Transporte.
- No hay validación operacional del ETA ni evidencia de reducción de esperas reales.
- El dashboard HTML y el código Streamlit forman parte del prototipo. El equipo indicó que Streamlit abre localmente, pero todavía falta una captura autenticable de esa ejecución.
- Un resultado de laboratorio no equivale a cumplimiento total del plan original.

Recomendación: cada integrante debe ejecutar el programa, leer el código básico y revisar su sección antes de presentarlo.


## Revisión posterior – versión mejorada

- Nuevo baseline: regresión lineal regularizada, que en el dataset artificial presenta menor MAE que Random Forest.
- Nueva app `03_Prototipo_Datos_Simulados/app_streamlit.py` (se ejecuta con `python -m streamlit run app_streamlit.py`; falta adjuntar captura del PC).
- 8 tests automáticos, todos aprobados.
- `04_Seguimiento/WBS_17_Tareas_para_Trello_Jira.csv` corresponde 1:1 a la WBS de la evaluación anterior, pero **NO prueba cinco semanas de trabajo**.
- Pendiente de cuenta personal: crear tablero Trello/Jira, nuevo repositorio GitHub y reemplazar los marcadores de URL. Ver `04_Seguimiento/GUÍA_PASO_A_PASO_TRELLO_GITHUB.md`.

## Corrección de comparación de modelos (noviembre 2026)

Ridge tiene menor MAE global (1,615 min) pero mayor brecha relativa entre zonas (21,29 %); Random Forest tiene MAE 1,722 min y brecha 18,88 %. Las 426 alertas originales corresponden a Random Forest; aplicar el umbral a Ridge produce 457 en datos sintéticos. Nada de esto demuestra rendimiento con buses reales. La publicación de Trello/GitHub sigue pendiente hasta tener enlaces verificables.

### Evidencia pendiente fuera del ZIP

- URL real de Trello/Jira, actividad con fechas auténticas y captura del tablero.
- URL de GitHub si el equipo decide publicar un repositorio.
- Captura PNG auténtica de Streamlit abierto en el PC del equipo. Guardarla como `06_Evidencias/streamlit_dashboard_real.png`.

El archivo ZIP **no contiene** esas pruebas externas y no afirma tenerlas.
