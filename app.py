import pandas as pd
import streamlit as st

# ---- Configurar streamlit ----
st.set_page_config(page_title="Cuadro de mandos de ventas",
                   page_icon="📊",
                   layout="wide")


# ---- Leer archivo excel ----
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )

    return df


# ---- Obtener Dataframe ----
df = get_data_from_excel()

# ---- Mostrar Dataframe en streamlit ----
st.dataframe(df)
