"""Genera exclusivamente DATOS SIMULADOS para el piloto didáctico.
NO son datos del Directorio de Transporte Público, GPS real ni tarjetas bip! reales.
"""
from pathlib import Path
import numpy as np
import pandas as pd

RUTAS = [
    ('101','Santiago','Centro',23,105),
    ('102','Providencia','Centro',26,125),
    ('103','Ñuñoa','Centro',29,95),
    ('104','Estación Central','Centro',32,130),
    ('201','Puente Alto','Periferia',42,115),
    ('202','La Pintana','Periferia',39,105),
    ('203','Quilicura','Periferia',37,85),
    ('204','Maipú','Periferia',44,115),
]
FRANJAS = [('AM','07:00',1.00,1.5),('Valle','12:00',0.48,0.5),('PM','18:00',0.95,1.4),('Noche','22:00',0.25,0.15)]


def generar(destino: Path, semilla: int = 1102) -> tuple[Path, Path]:
    destino.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(semilla)
    filas_gps, filas_bip = [], []
    for fecha in pd.date_range('2026-01-01','2026-06-30'):
        fin_semana = fecha.weekday() >= 5
        for codigo, comuna, zona, programado, demanda_base in RUTAS:
            sesgo_ruta = {'101':0.5,'102':1.5,'103':0.3,'104':1.0,'201':1.2,'202':1.8,'203':1.4,'204':2.1}[codigo]
            for nombre, hora, nivel_demanda, nivel_congestion in FRANJAS:
                lluvia_pronosticada = int(rng.random() < (0.28 if fecha.month in (5,6) else 0.09))
                congestion_pronosticada = max(0.05, rng.normal(nivel_congestion*(0.55 if fin_semana else 1),0.19))
                demanda = max(10,int(rng.normal(demanda_base*(0.65 if fin_semana else 1)*(0.45+0.65*nivel_demanda),12)))
                calidad = float(np.clip(rng.normal(0.963 if zona=='Centro' else 0.935,0.045),0.55,1))
                minutos = max(9,programado + 3.15*congestion_pronosticada + 1.65*lluvia_pronosticada + 0.025*(demanda-90) + sesgo_ruta + rng.normal(0,1.9 if zona=='Centro' else 2.25))
                filas_gps.append({
                    'fecha':fecha.date().isoformat(), 'recorrido':codigo, 'comuna':comuna,
                    'zona':zona,'franja':nombre,'hora_inicio':hora,
                    'minutos_programados':programado,'minutos_observados_gps':round(minutos,2),
                    'congestion_pronosticada':round(congestion_pronosticada,3),
                    'lluvia_pronosticada':lluvia_pronosticada,
                    'cobertura_gps':round(calidad,3),
                    'tipo_dato':'SIMULADO_NO_REAL'
                })
                filas_bip.append({
                    'fecha':fecha.date().isoformat(),'recorrido':codigo,'franja':nombre,
                    'validaciones_agregadas':demanda,'tipo_dato':'SIMULADO_NO_REAL'
                })
    gps = pd.DataFrame(filas_gps)
    bip = pd.DataFrame(filas_bip)
    gps_csv=destino/'gps_viajes_SIMULADOS.csv'
    bip_csv=destino/'bip_aggregado_SIMULADO.csv'
    gps.to_csv(gps_csv,index=False,encoding='utf-8-sig')
    bip.to_csv(bip_csv,index=False,encoding='utf-8-sig')
    return gps_csv,bip_csv

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    a,b=generar(root/'datos')
    print(f'Datos SIMULADOS generados: {a.name} / {b.name}')
