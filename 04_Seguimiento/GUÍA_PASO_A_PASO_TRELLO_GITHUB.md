# Publicación y seguimiento – pasos que requieren tu cuenta

## 1. Tablero real en Trello (prioridad máxima)

1. Abre Trello y crea el tablero privado `SCY1102 | Red Metropolitana | EP5-EP6`.
2. Crea las listas **Plan documentado**, **Demo parcial**, **Código preparado; prueba pendiente**, **Pendiente**, **Bloqueado sin cliente** y **Pendiente exposición**. No hay que fabricar cinco semanas de actividad.
3. Usa `WBS_17_Tareas_para_Trello_Jira.csv` como fuente. Trello no incluye una importación CSV universal igual para todas las cuentas; si tu espacio tiene importador o Power-Up, asigna los campos. Si no, crea las 17 tarjetas copiando el nombre y el comentario del CSV. La conexión de Trello en ChatGPT también permitiría crear tarjetas cuando la actives.
4. Mantén en cada tarjeta el **ID de WBS**, responsable **propuesto**, evidencia (ruta local o URL publicada) y un comentario breve que refleje lo realizado, sin retrofechar movimientos.
5. Sube una captura del tablero, copia su URL y reemplaza en el informe y diapositiva 7 el marcador **[PENDIENTE: URL TABLERO]**.
6. Cuando muevas una tarjeta, hazlo por trabajo comprobado, no por conveniencia de la presentación. Distingue el avance de la demo del plan operacional real.

## 2. Repositorio en GitHub

1. Crea un repositorio privado nuevo, por ejemplo `scy1102-red-metropolitana-demo`. No uses uno ajeno al curso.
2. Sube **solo** el contenido de `03_Prototipo_Datos_Simulados` y archivos útiles de `04_Seguimiento`, excluyendo `__pycache__`, `.venv`, credenciales y datos reales (este paquete no los contiene).
3. Sube `README.md`, `requirements.txt`, scripts Python, pruebas y el notebook. La salida HTML es opcional; los CSV son únicamente demostrativos.
4. Copia la URL y reemplaza en informe y diapositiva 7 **[PENDIENTE: URL REPOSITORIO]**.
5. Para reproducir: `pip install -r requirements.txt`, `python ejecutar_demo.py` y `python -m unittest discover -s tests -v`.

## 3. Verificar Streamlit en tu PC

1. Instala las dependencias `pip install -r requirements.txt` (requiere Internet).
2. Ejecuta `python ejecutar_demo.py` y luego `python -m streamlit run app_streamlit.py`.
3. Abre el navegador en la URL local que indique Streamlit y comprueba filtros, métricas y alertas.
4. Si funciona, agrega una captura a la carpeta `06_Evidencias` y cambia en informe el estado de **"código preparado"** a **"app comprobada localmente"**; solo después de esa comprobación.

## 4. Antes de entregar

- Confirma que cada afirmación del informe corresponde a una prueba o un archivo verificable.
- No atribuyas los resultados a Red Movilidad ni a un cliente que no participó.
- Vuelve a exportar informe y presentación cuando completes las URLs.
