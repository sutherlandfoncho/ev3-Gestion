"""Dashboard HTML autoconclusivo. 100 % datos de demostración SIMULADOS."""
from pathlib import Path
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

AZUL='#123b55'; TURQUESA='#008d94'; NARANJA='#d89d39'; GRIS='#607587'


def crear(resultado:Path):
    res=json.loads((resultado/'metricas_SIMULADAS.json').read_text(encoding='utf-8'))
    df=pd.read_csv(resultado/'predicciones_SIMULADAS.csv',dtype={'recorrido':str})
    zona=pd.read_csv(resultado/'mae_por_zona_SIMULADO.csv')
    top=(df.groupby(['recorrido','comuna'],as_index=False)['retraso_predicho_min']
           .mean().sort_values('retraso_predicho_min',ascending=False).head(8))
    fig=make_subplots(rows=1,cols=2,subplot_titles=('MAE: programado vs regresión vs Random Forest','Retraso promedio previsto por recorrido'),horizontal_spacing=0.17)
    fig.add_trace(go.Bar(x=['Programado','Regresión','Random Forest'],y=[res['mae_baseline_min'],res['mae_regresion_lineal_min'],res['mae_modelo_min']],marker_color=[GRIS,TURQUESA,AZUL],text=[f"{res['mae_baseline_min']:.2f}",f"{res['mae_regresion_lineal_min']:.2f}",f"{res['mae_modelo_min']:.2f}"],textposition='outside',showlegend=False),row=1,col=1)
    fig.add_trace(go.Bar(x=top['recorrido']+' · '+top['comuna'],y=top['retraso_predicho_min'],marker_color=NARANJA,showlegend=False),row=1,col=2)
    fig.update_layout(height=420,margin=dict(l=35,r=10,t=70,b=100),font=dict(family='Arial',size=11,color=AZUL),paper_bgcolor='white',plot_bgcolor='white')
    fig.update_xaxes(tickangle=-28,row=1,col=2)
    fig.update_yaxes(title='minutos',gridcolor='#edf0f3')
    grafico=plot(fig,include_plotlyjs=True,output_type='div',config={'displayModeBar':False,'responsive':True})
    rows=''.join(f"<tr><td>{r.zona}</td><td>{int(r.n):,}</td><td>{r.mae_min:.2f} min</td></tr>" for r in zona.itertuples())
    ult=df.sort_values('retraso_predicho_min',ascending=False).head(6)
    alerts=''.join(f'<tr><td>{r.fecha}</td><td>{r.recorrido}</td><td>{r.comuna}</td><td>{r.franja}</td><td><b>{r.retraso_predicho_min:.1f} min</b></td></tr>' for r in ult.itertuples())
    html=f'''<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Red Metropolitana · Prototipo</title><style>
    *{{box-sizing:border-box}}body{{margin:0;font-family:Arial,Helvetica,sans-serif;background:#f3f7f9;color:{AZUL}}}.wrap{{max-width:1260px;margin:auto;padding:35px}}.eyebrow{{font-weight:700;letter-spacing:2px;font-size:12px;color:{TURQUESA}}}h1{{margin:10px 0 5px;font-size:30px}}.sub{{color:#677d89}}.warning{{background:#fff2d7;border-left:5px solid #cc8525;padding:16px 20px;line-height:1.5;margin:24px 0;font-weight:600}}.stats{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}}.kpi{{background:white;border:1px solid #e0e7eb;border-radius:12px;padding:18px}}.val{{font-size:28px;font-weight:800;padding:8px 0}}.small{{font-size:12px;color:#657b87}}.panel{{background:white;border:1px solid #e0e7eb;border-radius:12px;padding:22px;margin-top:16px}}h2{{font-size:18px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:12px 10px;border-bottom:1px solid #e6edf1;text-align:left;font-size:14px}}th{{background:#eff5f7}}.columns{{display:grid;grid-template-columns:1fr 1.5fr;gap:18px}}@media(max-width:800px){{.stats,.columns{{grid-template-columns:1fr}}}}a{{color:{TURQUESA}}}</style></head><body><main class="wrap">
    <div class="eyebrow">GESTIÓN DE PROYECTOS DE DATOS · SCY1102</div><h1>Retrasos en la Red Metropolitana</h1><div class="sub">Dashboard de demostración | Prototipo técnico reproducible</div><div class="warning">DATOS 100 % SIMULADOS. No utiliza información GPS real, tarjetas bip! reales ni datos del cliente. Sus métricas NO demuestran eficacia operacional. Validación con la Red Metropolitana: pendiente.</div>
    <div class="stats"><div class="kpi"><div class="small">Viajes sintéticos analizados</div><div class="val">{res['registros_total']:,}</div></div><div class="kpi"><div class="small">MAE Regresión (demo)</div><div class="val">{res['mae_regresion_lineal_min']:.2f} min</div></div><div class="kpi"><div class="small">MAE Random Forest</div><div class="val">{res['mae_modelo_min']:.2f} min</div></div><div class="kpi"><div class="small">MAE programado</div><div class="val">{res['mae_baseline_min']:.2f} min</div></div><div class="kpi"><div class="small">Brecha territorial en demo</div><div class="val">{res['brecha_mae_centro_periferia_pct']:.1f}%</div></div></div>
    <section class="panel"><h2>Evaluación técnica sobre datos artificiales</h2><p class="small">La regresión obtiene menor MAE que Random Forest en estos datos fabricados. El generador contiene relaciones previsibles y ruido, por lo que NO demuestra desempeño operacional.</p>{grafico}</section><div class="columns"><section class="panel"><h2>Error por zona</h2><table><tr><th>Zona</th><th>Casos</th><th>MAE</th></tr>{rows}</table><p class="small">Comparación descriptiva en registros simulados, no auditoría de un sistema real.</p></section><section class="panel"><h2>Ejemplos de alertas generadas</h2><table><tr><th>Fecha</th><th>Rec.</th><th>Comuna</th><th>Franja</th><th>Retraso</th></tr>{alerts}</table></section></div><div class="panel"><b>Qué sí demuestra:</b> integración de fuentes simuladas, entrenamiento con división temporal, comparación de regresión lineal y Random Forest con el tiempo programado, cálculo de errores y generación de alertas visuales.<p><b>Qué falta:</b> acceso autorizado a datos reales, limpieza y anonimización verificadas con el cliente, definición formal de retraso y tiempos programados, pruebas operacionales, control de equidad con representatividad real y validación de los responsables de transporte.</p></div></main></body></html>'''
    path=resultado/'Dashboard_DEMO_Abrir.html'
    path.write_text(html,encoding='utf-8')
    return path

if __name__=='__main__':
    raiz=Path(__file__).resolve().parents[1]
    print(crear(raiz/'resultado'))
