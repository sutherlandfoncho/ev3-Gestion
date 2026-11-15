# Guion de exposición — EP6 (máximo 5 minutos)

**Presentar diapositivas 1 a 7. Las diapositivas 8 y 9 son de respaldo y NO se exponen.**

**Duración total planificada: 4 min 40 s (más transiciones).**

## Diapositiva 1 — 0:10 · PORTADA

Presentamos el paso de nuestro plan a un prototipo académico de predicción de retrasos en la Red Metropolitana. Todo lo que veremos utiliza datos simulados.

## Diapositiva 2 — 0:35 · PLANIFICACIÓN VS. EJECUCIÓN

En la evaluación anterior planificamos cinco entregables y diecisiete actividades, pensando en datos GPS y bip! reales. Hoy mostramos un prototipo reproducible en Python, un dashboard funcional en HTML y Streamlit, ocho pruebas aprobadas y un tablero Trello con las diecisiete tareas. Todavía no tenemos datos autorizados del cliente, por eso no hablamos de precisión operacional.

## Diapositiva 3 — 1:00 · EVIDENCIA TÉCNICA

Esta captura es de la aplicación Streamlit funcionando en nuestro computador. El proyecto genera datos sintéticos, los prepara, entrena una regresión Ridge y Random Forest y evalúa sus predicciones con fechas posteriores al entrenamiento. Ridge obtiene un MAE de 1,615 minutos y Random Forest 1,722; la referencia programada marca 4,49. Las 426 alertas que muestra el prototipo provienen de Random Forest. Los ocho tests pasan. Por zona, la brecha simulada es de 21,29 por ciento con Ridge y de 18,88 por ciento con Random Forest. Esto demuestra ejecución de código, no comportamiento real del transporte.

## Diapositiva 4 — 0:35 · INTERPRETACIÓN

Es importante explicar qué significan estos números. Los datos se fabricaron con reglas conocidas y con distinto nivel de ruido entre zonas; por eso los modelos pueden recuperar esos patrones. La semilla fija permite repetir el experimento. No estamos demostrando que ya cumplimos la precisión ni la equidad con buses reales de Santiago.

## Diapositiva 5 — 0:55 · SEGUIMIENTO REAL

Aquí está nuestro tablero real de Trello. Incluye las diecisiete actividades de la WBS, distribuidas en cuatro listas: dos de planificación documentada, diez de demostración parcial, tres pendientes y dos bloqueadas por datos reales. No significa que diez entregables estén aprobados: son tareas trabajadas en el demo. Con este tablero podemos asignar responsables, adjuntar evidencias y registrar comentarios y cambios de estado. Tenemos los estados actuales; el historial de seguimiento se construirá con los próximos avances auténticos.

## Diapositiva 6 — 0:55 · DESVIACIONES Y CORRECCIONES

Respecto del plan inicial, no tuvimos acceso a GPS ni bip! reales: usamos datos simulados. El dashboard ya se ejecuta también en Streamlit, no solamente en HTML. Agregamos la regresión Ridge para comparar modelos y corregimos nuestra interpretación cuando vimos que tenía menor error global, pero una mayor brecha territorial relativa. También migramos las diecisiete tareas a Trello. Quedan como acciones validar con usuarios, documentar el seguimiento y solicitar datos autorizados.

## Diapositiva 7 — 0:30 · CIERRE

Los riesgos que siguen abiertos son el acceso a datos reales, su calidad, la equidad territorial y la precisión fuera del laboratorio. Lo entregado es un prototipo reproducible con evidencia técnica y seguimiento inicial, pero no un sistema aprobado por Red Movilidad. El próximo paso es validar con datos autorizados. Muchas gracias.

## Qué mostrar durante la defensa

- Diapositiva 3: captura REAL de Streamlit del equipo, no un mockup. Los datos son sintéticos.
- Diapositiva 5: captura REAL de Trello con 17 tarjetas (2 Plan documentado / 10 Demo parcial / 3 Pendiente / 2 Bloqueado). No presentar estados como actas de aceptación.
- Ridge: MAE 1,615 min; brecha 21,29 %. Random Forest: MAE 1,722 min; brecha 18,88 %; 426 alertas. Todo simulado.
- El historial de seguimiento periódico y la validación con datos reales siguen pendientes de documentarse.
