"""Dashboard complementario Streamlit, exclusivamente para el dataset SIMULADO.

Ejecutar desde la carpeta del prototipo:
    pip install -r requirements.txt
    python -m streamlit run app_streamlit.py

No está conectado a redes de buses, datos bip! reales ni sistemas de despacho.
"""
from pathlib import Path
import json
import pandas as pd

BASE = Path(__file__).resolve().parent
OUT = BASE / "resultado"


def cargar_resultados(base: Path = OUT):
    """Valida existencia y esquema mínimo, sin importar Streamlit."""
    required = {"predicciones_SIMULADAS.csv", "mae_por_zona_SIMULADO.csv", "metricas_SIMULADAS.json"}
    missing = [f for f in sorted(required) if not (base / f).is_file()]
    if missing:
        raise FileNotFoundError("Ejecuta primero python ejecutar_demo.py. Faltan: " + ", ".join(missing))
    df = pd.read_csv(base / "predicciones_SIMULADAS.csv", dtype={"recorrido": str})
    zonas = pd.read_csv(base / "mae_por_zona_SIMULADO.csv")
    metricas = json.loads((base / "metricas_SIMULADAS.json").read_text(encoding="utf-8"))
    if not metricas.get("es_prototipo_academico") or not df["zona"].isin(["Centro", "Periferia"]).all():
        raise ValueError("Origen/estructura de demostración no reconocidos.")
    expected = {"fecha", "zona", "comuna", "recorrido", "franja", "prediccion_min", "retraso_predicho_min", "alerta"}
    if not expected.issubset(df.columns):
        raise ValueError("Faltan columnas mínimas de la visualización.")
    return df, zonas, metricas


def main():
    try:
        import streamlit as st
    except ImportError as e:
        raise SystemExit("Streamlit no está instalado: pip install -r requirements.txt") from e
    st.set_page_config(page_title="Red Metropolitana | DEMO simulada", layout="wide", page_icon="🚌")
    st.title("Predicción de retrasos · Prototipo académico")
    st.warning("DEMO con datos 100 % SIMULADOS. Sin GPS real, validaciones bip! reales ni aprobación del cliente.")
    try:
        df, zonas, metricas = cargar_resultados()
    except (FileNotFoundError, ValueError) as error:
        st.error(str(error))
        st.stop()
    col1,col2,col3,col4=st.columns(4)
    col1.metric("MAE Random Forest",f"{metricas['mae_modelo_min']:.2f} min")
    col2.metric("MAE regresión lineal",f"{metricas['mae_regresion_lineal_min']:.2f} min")
    col3.metric("MAE programado",f"{metricas['mae_baseline_min']:.2f} min")
    col4.metric("Alertas RF (sintéticas)",str(metricas['registros_alerta_prioritario']))
    st.caption("Ridge logra menor MAE global, pero presenta mayor brecha relativa entre zonas; las alertas que se muestran corresponden a Random Forest. Resultados SOLO de simulación.")
    if 'brecha_mae_centro_periferia_ridge_pct' in metricas:
        st.info(f"Brecha territorial simulada: Ridge {metricas['brecha_mae_centro_periferia_ridge_pct']:.2f} % · Random Forest {metricas['brecha_mae_centro_periferia_random_forest_pct']:.2f} %. No indica equidad real.")
    st.subheader("Explorar predicciones")
    a,b,c=st.columns(3)
    zonas_sel=a.multiselect("Zona",sorted(df.zona.dropna().unique()),default=sorted(df.zona.dropna().unique()))
    rutas=b.multiselect("Recorrido",sorted(df.recorrido.dropna().unique()),default=sorted(df.recorrido.dropna().unique()))
    franjas=c.multiselect("Franja",sorted(df.franja.dropna().unique()),default=sorted(df.franja.dropna().unique()))
    muestra=df[df.zona.isin(zonas_sel)&df.recorrido.isin(rutas)&df.franja.isin(franjas)].copy()
    st.write(f"{len(muestra):,} filas de prueba filtradas (datos simulados)")
    st.dataframe(muestra[["fecha","recorrido","comuna","zona","franja","minutos_programados","prediccion_min","retraso_predicho_min","alerta"]],hide_index=True,use_container_width=True)
    u,v=st.columns(2)
    with u:
        st.subheader("MAE por zona · Random Forest (demo)")
        st.bar_chart(zonas.set_index("zona")[["mae_min"]])
    with v:
        st.subheader("Alertas por franja · demo")
        a=muestra.loc[muestra.alerta=="PRIORITARIO"].groupby("franja").size().rename("alertas")
        st.bar_chart(a)
    st.info("Pendiente: acceso autorizado a datos reales, validación temporal operacional, revisión de equidad, aceptación de cliente y despliegue.")

if __name__ == "__main__":
    main()
