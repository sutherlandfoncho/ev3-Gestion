from pathlib import Path
import json
from src.generar_datos import generar
from src.procesar_modelo import evaluar
from src.crear_dashboard import crear

root=Path(__file__).resolve().parent
print('1/3 Generando fuentes exclusivamente SIMULADAS...')
a,b=generar(root/'datos')
print('2/3 Preparando y entrenando modelo de DEMOSTRACIÓN...')
m=evaluar(a,b,root/'resultado')
print('3/3 Creando dashboard HTML que se abre sin servidor...')
p=crear(root/'resultado')
print(json.dumps(m,ensure_ascii=False,indent=2))
print('DASHBOARD:',p)
