"""Piloto de predicción de tiempos de viaje con datos expresamente SIMULADOS.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

SENSIBLES = {'rut','nro_tarjeta','numero_tarjeta','card_id','card_number','user_id','id_usuario','id_pasajero','pasajero_id','nombre','email'}
FEATURES_CAT=['recorrido','comuna','zona','franja']
FEATURES_NUM=['dia_semana','minutos_programados','congestion_pronosticada','lluvia_pronosticada','demanda_rezago_7d']
FEATURES=FEATURES_CAT+FEATURES_NUM


def verificar_estructura(gps:pd.DataFrame,bip:pd.DataFrame)->None:
    expected_gps={'fecha','recorrido','comuna','zona','franja','minutos_programados','minutos_observados_gps','congestion_pronosticada','lluvia_pronosticada','tipo_dato'}
    expected_bip={'fecha','recorrido','franja','validaciones_agregadas','tipo_dato'}
    if not expected_gps.issubset(gps.columns) or not expected_bip.issubset(bip.columns):
        raise ValueError('El esquema de datos no cumple los campos requeridos.')
    names={str(c).lower() for c in list(gps.columns)+list(bip.columns)}
    if any(t in names for t in SENSIBLES):
        raise ValueError('Detectados campos personales: no procesar sin revisión y anonimización.')
    if not gps['tipo_dato'].eq('SIMULADO_NO_REAL').all() or not bip['tipo_dato'].eq('SIMULADO_NO_REAL').all():
        raise ValueError('Este ejemplo sólo permite datos de laboratorio expresamente SIMULADOS.')


def preparar(gps:pd.DataFrame,bip:pd.DataFrame)->pd.DataFrame:
    verificar_estructura(gps,bip)
    out=gps.merge(bip[['fecha','recorrido','franja','validaciones_agregadas']],on=['fecha','recorrido','franja'],how='inner',validate='one_to_one')
    out['fecha']=pd.to_datetime(out['fecha'])
    out['dia_semana']=out['fecha'].dt.dayofweek
    out=out.sort_values(['recorrido','franja','fecha']).reset_index(drop=True)
    # El rezago excluye expresamente las validaciones del mismo día: evita filtración temporal.
    out['demanda_rezago_7d']=out.groupby(['recorrido','franja'])['validaciones_agregadas'].transform(lambda s:s.shift(1).rolling(7,min_periods=1).mean())
    out['demanda_rezago_7d']=out['demanda_rezago_7d'].fillna(0)  # Sin historia previa disponible: valor neutro, nunca dato futuro
    out=out.sort_values(['fecha','recorrido','franja']).reset_index(drop=True)
    # La duración observada GPS sólo es objetivo, nunca variable de entrada.
    return out


def evaluar(gps_file:Path,bip_file:Path,salida:Path)->dict:
    salida.mkdir(exist_ok=True,parents=True)
    gps=pd.read_csv(gps_file,dtype={'recorrido':str})
    bip=pd.read_csv(bip_file,dtype={'recorrido':str})
    df=preparar(gps,bip)
    fechas=sorted(df['fecha'].unique())
    corte=fechas[int(len(fechas)*0.80)]
    train=df.loc[df.fecha<corte].copy()
    test=df.loc[df.fecha>=corte].copy()
    assert train.fecha.max()<test.fecha.min(),'Corte temporal incorrecto.'
    pre=ColumnTransformer([
        ('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),FEATURES_CAT),
        ('num',SimpleImputer(strategy='median'),FEATURES_NUM),
    ])
    modelo=Pipeline([('prep',pre),('rf',RandomForestRegressor(n_estimators=90,max_depth=11,min_samples_leaf=4,random_state=1102,n_jobs=-1))])
    modelo.fit(train[FEATURES],train['minutos_observados_gps'])
    predicted=modelo.predict(test[FEATURES])
    # Segunda referencia comprometida en EP3: regresión lineal regularizada con las mismas variables.
    # Se usa el mismo corte temporal que Random Forest, sin mirar las fechas de prueba.
    lineal=Pipeline([('prep',ColumnTransformer([
        ('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),FEATURES_CAT),
        ('num',SimpleImputer(strategy='median'),FEATURES_NUM),
    ])),('ridge',Ridge(alpha=10.0))])
    lineal.fit(train[FEATURES],train['minutos_observados_gps'])
    pred_lineal=lineal.predict(test[FEATURES])
    baseline=test['minutos_programados'].to_numpy()
    y=test['minutos_observados_gps'].to_numpy()
    test['prediccion_min']=np.round(predicted,2)
    test['prediccion_lineal_min']=np.round(pred_lineal,2)
    test['retraso_predicho_min']=(test['prediccion_min']-test['minutos_programados']).round(2)
    test['alerta']=np.where(test['retraso_predicho_min']>=5,'PRIORITARIO','Monitorear')
    test['error_abs_min']=np.abs(y-predicted).round(2)
    por_zona=test.groupby('zona',sort=True).agg(n=('error_abs_min','size'),mae_min=('error_abs_min','mean')).round(3)
    por_comuna=test.groupby(['zona','comuna'],sort=True).agg(n=('error_abs_min','size'),mae_min=('error_abs_min','mean')).round(3)
    # Métricas de equidad para Ridge, sobre el mismo conjunto de prueba.
    # No mezclar la brecha de Random Forest con el modelo Ridge de menor MAE.
    test['error_abs_lineal_min']=np.abs(y-test['prediccion_lineal_min'])  # exactamente la columna exportada
    errores_ridge=test.groupby('zona')['error_abs_lineal_min'].agg(['size','mean'])
    if {'Centro','Periferia'}.issubset(errores_ridge.index):
        c_ridge=float(errores_ridge.loc['Centro','mean'])
        p_ridge=float(errores_ridge.loc['Periferia','mean'])
        brecha_ridge=round(abs(p_ridge-c_ridge)/c_ridge*100,2) if c_ridge else None
    else: brecha_ridge=None
    comparacion_zonas=pd.DataFrame({
        'zona':sorted(test.zona.unique()),
    })
    comparacion_zonas['n']=[int((test.zona==z).sum()) for z in comparacion_zonas.zona]
    comparacion_zonas['mae_random_forest_min']=[round(float(test.loc[test.zona==z,'error_abs_min'].mean()),3) for z in comparacion_zonas.zona]
    comparacion_zonas['mae_ridge_min']=[round(float(test.loc[test.zona==z,'error_abs_lineal_min'].mean()),3) for z in comparacion_zonas.zona]
    alertas_ridge=int(((test['prediccion_lineal_min']-test['minutos_programados'])>=5).sum())
    if {'Centro','Periferia'}.issubset(por_zona.index):
        centro=float(por_zona.loc['Centro','mae_min']); periferia=float(por_zona.loc['Periferia','mae_min'])
        brecha=round(abs(periferia-centro)/centro*100,2) if centro else None
    else: brecha=None
    resumen={
        'fuente':'SIMULADA (NO corresponde a Red Movilidad ni a datos bip! reales)',
        'es_prototipo_academico':True,
        'periodo_simulado_inicio':str(df.fecha.min().date()),
        'periodo_simulado_fin':str(df.fecha.max().date()),
        'corte_prueba':str(pd.Timestamp(corte).date()),
        'registros_total':len(df),'registros_entrenamiento':len(train),'registros_prueba':len(test),
        'mae_baseline_min':round(float(mean_absolute_error(y,baseline)),3),
        'mae_regresion_lineal_min':round(float(mean_absolute_error(y,pred_lineal)),3),
        'rmse_regresion_lineal_min':round(float(root_mean_squared_error(y,pred_lineal)),3),
        'mae_modelo_min':round(float(mean_absolute_error(y,predicted)),3),
        'rmse_modelo_min':round(float(root_mean_squared_error(y,predicted)),3),
        'mejora_mae_pct':round(float((1-mean_absolute_error(y,predicted)/mean_absolute_error(y,baseline))*100),2),
        'brecha_mae_centro_periferia_pct':brecha,  # histórica: Random Forest
        'brecha_mae_centro_periferia_random_forest_pct':brecha,
        'brecha_mae_centro_periferia_ridge_pct':brecha_ridge,
        'registros_alerta_prioritario':int((test['alerta']=='PRIORITARIO').sum()), # Random Forest
        'registros_alerta_prioritario_random_forest':int((test['alerta']=='PRIORITARIO').sum()),
        'registros_alerta_prioritario_ridge':alertas_ridge,
        'evaluacion_datos_reales':'NO REALIZADA',
        'validacion_cliente':'PENDIENTE',
        'nota':'Estas métricas solo comprueban la ejecución del código sobre datos artificiales; no evidencian desempeño operativo.',
        'explicacion_generador':'La variable objetivo se fabrica con duración programada, congestión, lluvia, demanda, efecto por recorrido y ruido gaussiano con sigma 1.9 min (Centro) y 2.25 min (Periferia). El aprendizaje recupera parte de esa función artificial.',
        'piso_ruido_teorico_mae_centro_min':round(float(1.9*np.sqrt(2/np.pi)),3),
        'piso_ruido_teorico_mae_periferia_min':round(float(2.25*np.sqrt(2/np.pi)),3),
        'aclaracion_piso_ruido':'Son referencias teóricas para el componente gaussiano artificial; no son cotas exactas del error observado ni equivalen a un test externo.',
    }
    test[['fecha','recorrido','comuna','zona','franja','minutos_programados','minutos_observados_gps','prediccion_min','prediccion_lineal_min','retraso_predicho_min','alerta','error_abs_min']].to_csv(salida/'predicciones_SIMULADAS.csv',index=False,encoding='utf-8-sig')
    test.loc[test.alerta=='PRIORITARIO',['fecha','recorrido','comuna','franja','retraso_predicho_min']].to_csv(salida/'alertas_SIMULADAS.csv',index=False,encoding='utf-8-sig')
    por_zona.to_csv(salida/'mae_por_zona_SIMULADO.csv',encoding='utf-8-sig')
    comparacion_zonas.to_csv(salida/'mae_por_zona_ambos_modelos_SIMULADO.csv',index=False,encoding='utf-8-sig')
    por_comuna.to_csv(salida/'mae_por_comuna_SIMULADO.csv',encoding='utf-8-sig')
    (salida/'metricas_SIMULADAS.json').write_text(json.dumps(resumen,ensure_ascii=False,indent=2),encoding='utf-8')
    return resumen

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    r=evaluar(root/'datos/gps_viajes_SIMULADOS.csv',root/'datos/bip_aggregado_SIMULADO.csv',root/'resultado')
    print(json.dumps(r,indent=2,ensure_ascii=False))
