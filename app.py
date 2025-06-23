import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Monitor de Riesgo", layout="wide")
st.title("📉 Monitor de Riesgo de Inversiones Argentinas")

st.sidebar.header("📂 Carga de Cartera")
uploaded_file = st.sidebar.file_uploader("Subí tu CSV con los activos y pesos", type=["csv"])

@st.cache_data
def obtener_precios(activos, periodo="2y"):
    precios = {}
    for ticker in activos:
        try:
            data = yf.download(ticker, period=period)["Adj Close"]
            precios[ticker] = data
        except:
            st.warning(f"No se pudo descargar {ticker}")
    df_precios = pd.DataFrame(precios).dropna()
    return df_precios

def calcular_retorno_cartera(precios, pesos):
    retornos = precios.pct_change().dropna()
    retornos_cartera = (retornos * pesos).sum(axis=1)
    return retornos_cartera

def calcular_var_cvar(retornos, nivel_confianza=0.95):
    var = np.percentile(retornos, 100 * (1 - nivel_confianza))
    cvar = retornos[retornos <= var].mean()
    return var, cvar

if uploaded_file:
    cartera = pd.read_csv(uploaded_file)
    if "Activo" in cartera.columns and "Peso" in cartera.columns:
        st.subheader("📊 Tu Cartera")
        st.write(cartera)

        pesos = cartera.set_index("Activo")["Peso"]
        precios = obtener_precios(pesos.index.tolist())
        retornos = calcular_retorno_cartera(precios, pesos)

        var, cvar = calcular_var_cvar(retornos)

        st.subheader("📈 Resultados de Simulación")
        st.metric("VaR 95%", f"{var:.2%}")
        st.metric("CVaR 95%", f"{cvar:.2%}")

        st.line_chart((1 + retornos).cumprod())

    else:
        st.error("El archivo debe tener columnas llamadas 'Activo' y 'Peso'")
else:
    st.info("Subí un archivo .csv con columnas como: Activo, Peso")

st.markdown("---")
st.caption("Hecho por Mauro · Versión MVP")