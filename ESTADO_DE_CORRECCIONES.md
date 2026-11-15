# Control de cambios – EP5 y EP6

Fecha de revisión del material: 9 de noviembre de 2026 (no se presenta como cinco semanas históricas de ejecución).

## Correcciones realizadas y comprobadas

| Observación de auditoría | Cambio que se hizo | Evidencia |
|---|---|---|
| Faltaba regresión de referencia | Se agregó regresión lineal regularizada Ridge en las mismas fechas y variables. | `src/procesar_modelo.py`, JSON y predicciones CSV |
| RF parecía siempre mejor | Se informó el resultado real de laboratorio: programado 4,490; Ridge 1,615; Random Forest 1,722 min. La regresión es mejor en esta muestra. | `resultado/metricas_SIMULADAS.json`, informe y lámina 4 |
| Métricas sintéticas poco interpretadas | Se documentaron las reglas del generador y el MAE esperado del ruido gaussiano (1,52–1,80 minutos por zona); no representa un piso universal ni prueba operación real. | Informe, README, JSON y lámina 4 |
| Eran solo 7 pruebas | Se añadió control de regresión. **8/8 pruebas** aprobadas, ejecutadas en este entorno. | `tests/test_demo.py`, `06_Evidencias/pruebas_8_aprobadas.txt` |
| Dashboard comprometido en Streamlit | Se escribió `app_streamlit.py` para cargar los resultados, filtrar recorridos y mostrar gráficos. Se verificó sintaxis y carga de datos. | `app_streamlit.py` y `requirements.txt` |
| Dashboard HTML solo comparaba 2 modelos | HTML recreado con tres alternativas; captura nueva auténtica. | `resultado/Dashboard_DEMO_Abrir.html`, capturas nuevas |
| 12 tarjetas ≠ 17 tareas | CSV WBS 17/17 con IDs, responsables propuestos, estados y evidencia. El tablero de 12 sigue siendo resumen separado. | `04_Seguimiento/WBS_17_Tareas_para_Trello_Jira.csv` |
| Diapositiva 8 sin encabezados arriba | Encabezados corregidos y mejor legibilidad. | PowerPoint y PDF de presentación |
| Imágenes poco legibles y arco de portada | Captura ampliada, slide 7 reemplazada por lectura clara, arco eliminado. | Presentación PDF |
| Falta explicación oral de nueva versión | Se actualizó guion con Ridge, 8 pruebas, Streamlit y publicación pendiente. | DOCX y PDF de guion |

## Pendiente y por qué

1. **Trello/Jira real**: requiere que el equipo cree o conecte un tablero en su cuenta. No hay URL real ni registro remoto. No simular movimientos anteriores.
2. **GitHub**: el repositorio debe crearse nuevo en la cuenta del usuario. No se utilizaron repositorios personales no relacionados. Sustituir marcadores `[PENDIENTE: URL ...]` en informe y diapositiva 7.
3. **Verificación visual de Streamlit**: la dependencia no pudo instalarse en este entorno porque no hay acceso al índice de paquetes. El código compiló y su función de lectura de datos fue comprobada. En el equipo del estudiante, instalar dependencias, ejecutar `streamlit run app_streamlit.py`, revisar interfaz y capturar evidencia.
4. **Datos reales / aceptación**: no existen en el paquete. No se finge una validación con Red Movilidad.

## Límites al defender

Las observaciones 5.792 registros, 1.184 de prueba y 426 alertas son **completamente simuladas**. Los modelos recuperan relaciones establecidas en el propio generador. La demostración sí respalda la reproducibilidad del software, pero no su precisión sobre buses reales, ni la reducción de tiempos de espera.

Ver `04_Seguimiento/GUÍA_PASO_A_PASO_TRELLO_GITHUB.md` para la parte que debe completar el equipo.

## Integración de las correcciones finales

- Se reemplazó el PowerPoint antiguo por la versión corregida de 11 diapositivas y su PDF.
- Se corrigió el README del prototipo y la atribución de las métricas de Ridge y Random Forest en el informe y guion.
- El módulo de modelado registra ambas brechas territoriales y las alertas de cada modelo por separado.
- Streamlit fue abierto localmente según el equipo; se requiere una captura de pantalla para evidenciarlo y no hay despliegue institucional.
- Se incluyeron instrucciones de Trello y títulos de las 17 actividades WBS para gestionar sus fechas reales. No se ha conectado ninguna cuenta.
