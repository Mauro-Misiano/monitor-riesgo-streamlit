import streamlit as st
import pandas as pd

st.set_page_config(page_title="Monitor de Riesgo", layout="wide")
st.title("📉 Monitor de Riesgo de Inversiones Argentinas")

st.sidebar.header("📂 Carga de Cartera")
uploaded_file = st.sidebar.file_uploader("Subí tu CSV con los activos y pesos", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Tu Cartera")
    st.write(df)
    
    # Placeholder de simulación
    st.subheader("⚙️ Resultados de Simulación")
    st.write("Simulación de riesgo pendiente de implementación.")
else:
    st.info("Subí un archivo .csv con columnas como: Activo, Peso")

st.markdown("---")
st.caption("Hecho por Mauro · Versión MVP")