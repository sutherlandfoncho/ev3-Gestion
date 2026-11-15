# Guía de actualización final — Trello, evidencias y enlaces

**Estado de esta entrega:** PowerPoint corregido respecto de métricas Ridge/Random Forest; README actualizado. Las capturas reales y enlaces aún faltan, porque solo tú puedes producirlos al abrir Streamlit y tu tablero.

## Trello: procedimiento para crear un historial real

1. Entrar a https://trello.com/, iniciar sesión y elegir **Crear → Crear tablero**. Nombrarlo `SCY1102 | Red Metropolitana | EP5-EP6`. Seleccionar visibilidad **Privado**.
2. Crear cuatro listas: `01 · Plan documentado`, `02 · Demo parcial`, `03 · Pendiente / validación`, `04 · Bloqueado: datos reales`.
3. Abrir `TRELLO_17_TARJETAS_PARA_COPIAR.md`, copiar los nombres de cada grupo y pegarlos en el cuadro **Añadir una tarjeta** de la lista correspondiente; Trello permite convertir líneas pegadas en tarjetas. El CSV es una **fuente**, no un importador automático nativo.
4. Abrir cada tarjeta y pegar: descripción/objetivo, responsable real, estado actual, evidencia concreta (ruta local o enlace GitHub cuando exista) y próxima acción. Usar los datos de `WBS_17_Tareas_para_Trello_Jira.csv` como propuesta que debe contrastarse antes de darla por ejecutada.
5. Invitar a los compañeros y asignar los miembros a sus tarjetas (Diego: negocio/modelos; Cristóbal: limpieza/datos; Alfonso: dashboard/ETL), si están de acuerdo con ese reparto real.
6. Crear tres etiquetas: `Demo sintética`, `Validación pendiente`, `Dependencia externa`. Añadir fechas **reales** de vencimiento, no fechas retroactivas inventadas.
7. En las tarjetas efectivamente trabajadas, adjuntar evidencia (captura, script, archivo, URL GitHub) y escribir un comentario hoy, por ejemplo: «13/11/2026. Migramos el registro local al tablero Trello. Evidencia disponible: [ruta]. Lo pendiente: validar con datos reales».
8. Mover tarjetas solo cuando su **estado actual real** lo justifique. Cada movimiento queda registrado en la actividad de la tarjeta. No se deben simular movimientos históricos.
9. Si después de revisar Streamlit ya se ha usado correctamente: abrir `4.1 · Desarrollo dashboard Streamlit`, adjuntar `streamlit_dashboard_real.png`, comentar «La app abrió en localhost y se comprobaron [los filtros que efectivamente revisamos]. Queda pendiente despliegue institucional». Pasar a `02 · Demo parcial` si procede.
10. Realizar una revisión al final de cada jornada de trabajo: revisar pendientes/bloqueos, escribir comentarios con avances y decisión correctiva, mover tarjetas cuya evidencia cambió y anotar un resumen de control. En tres días de trabajo reales, tres cortes de seguimiento; no es necesario esperar semanas.
11. Guardar URL del tablero desde la barra del navegador. Para revisión académica, dar acceso por invitación al profesor o compartir un enlace que pueda abrir sin exponer información personal.
12. Exportar una evidencia adicional si hace falta: menú del tablero → **Imprimir, exportar y compartir → JSON** (según permisos de cuenta). Los comentarios y movimientos recientes pueden quedar en el JSON; no es lo mismo que una captura.

**Capturas Trello:** abrir el tablero con listas y títulos legibles, usar `Win + Shift + S` y guardar `EP5_EP6_MEJORADO/06_Evidencias/trello_tablero_real.png`. Abrir tarjeta `4.1` o `3.3`, pulsar **Comentarios y actividad**, mostrar movimientos/comentarios con fechas y guardar `.../trello_historial_tarjeta.png`. No usar la imagen antigua del tablero local como prueba de Trello.

## Streamlit: dos pantallazos

1. PowerShell en `EP5_EP6_MEJORADO/03_Prototipo_Datos_Simulados/`:

   ```powershell
   python ejecutar_demo.py
   python -m streamlit run app_streamlit.py
   ```

2. Abrir `http://localhost:8501`. Verificar título, etiquetas que adviertan «datos simulados», indicadores y gráficos; cambiar **un filtro real** y comprobar que cambia la vista.
3. Usar `Win + Shift + S` para capturar un rectángulo amplio que muestre **cabecera + métricas + gráfico principal + filtros**. Guardar como `EP5_EP6_MEJORADO/06_Evidencias/streamlit_dashboard_real.png`.
4. Si los gráficos importantes están más abajo, hacer otra captura `EP5_EP6_MEJORADO/06_Evidencias/streamlit_detalle_filtros.png` donde se vea la selección y la gráfica correspondiente.
5. Evitar capturar nombres de usuarios, correos y archivos personales. La URL `localhost:8501` no se podrá abrir desde el computador del profesor, por eso la captura es importante; la aplicación se puede ejecutar con las instrucciones de README.

## Para corregir posteriormente las diapositivas 6 y 7

Envíame exactamente:
- `streamlit_dashboard_real.png` (y, si cabe, `streamlit_detalle_filtros.png`): sustituiré los gráficos HTML antiguos de la diapositiva 6 por evidencia de Streamlit y retiraré «captura pendiente».
- `trello_tablero_real.png`: sustituiré la imagen del tablero local en la diapositiva 7.
- `trello_historial_tarjeta.png`: permite demostrar seguimiento real, no solo una lista estática.
- URL del tablero Trello y URL del repositorio GitHub cuando existan: las añadiré en la diapositiva 7 y en el informe EP5.

## Límites a recordar

- Los resultados Ridge y Random Forest provienen de datos simulados, no de Red Movilidad real.
- Ridge: MAE 1,615 min; brecha Centro–Periferia 21,29 %.
- Random Forest: MAE 1,722 min; brecha 18,88 % y 426 alertas del archivo oficial.
- El panel Streamlit en un equipo local no equivale a un servicio desplegado para el cliente.
