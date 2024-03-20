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

# ---- Página principal
st.title("📊")
st.markdown("##")

# ---- Establecer KPIs
total_ventas = int(df_selection["Total"].sum())
rating_medio = round(df_selection["Rating"].mean(), 1)
rating_estrellas = "🌟" * int(round(rating_medio, 0))
venta_media_por_transaccion = round(df_selection["Total"].mean(), 2)

# ---- Establecer 3 columnas
columna_izquierda, columna_central, columna_derecha = st.columns(3)

# ---- Mostrar total ventas en la columna izquierda
with columna_izquierda:
    st.subheader("Total ventas:")
    st.subheader(f"US $ {total_ventas:,}")

# ---- Mostrar Rating medio (con estrellas) en la columna central
with columna_central:
    st.subheader("Rating medio:")
    st.subheader(f"{rating_medio} {rating_estrellas}")

# ---- Mostrar Media de ventas por transacción en la columna derecha
with columna_derecha:
    st.subheader("Venta media por transacción:")
    st.subheader(f"US $ {venta_media_por_transaccion}")

# ---- Mostrar Dataframe en streamlit ----
st.dataframe(df_selection)

