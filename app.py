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

# ---- Configurar SideBar
st.sidebar.header("Introduzca los filtros aquí:")
ciudad = st.sidebar.multiselect(
    "Seleccione la ciudad:",
    options = df["City"].unique(),
    default = df["City"].unique()
)

tipo_cliente = st.sidebar.multiselect(
    "Seleccione el tipo de cliente:",
    options = df["Customer_type"].unique(),
    default = df["Customer_type"].unique()
)

genero = st.sidebar.multiselect(
    "Seleccione el género:",
    options = df["Gender"].unique(),
    default = df["Gender"].unique()
)

# ---- Aplicar filtros seleccionados al Dataframe
df_selection = df.query("City == @ciudad & Customer_type == @tipo_cliente & Gender == @genero")

# ---- Mostrar Dataframe en streamlit ----
st.dataframe(df_selection)