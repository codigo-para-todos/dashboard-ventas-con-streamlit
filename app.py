import pandas as pd
import streamlit as st
import plotly.express as px

# ---- Configurar streamlit ----
st.set_page_config(page_title="Cuadro de mandos de ventas",
                   page_icon="📊",
                   layout="wide")


# ---- Leer archivo excel ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )

    # Añadir columna 'hour' al Dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour

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

st.markdown("""---""")

# ---- Mostrar Dataframe en streamlit ----
#st.dataframe(df_selection)

# ---- Mostrar ventas por línea de producto (gráfico de barras) en streamlit ----
ventas_por_linea_de_producto = (
    df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
)

grafico_ventas_por_linea_de_producto = px.bar(
    ventas_por_linea_de_producto,
    x="Total",
    y=ventas_por_linea_de_producto.index,
    orientation="h",
    title="<b>Ventas por línea de producto</b>",
    color_discrete_sequence=["#0083B8"] * len(ventas_por_linea_de_producto),
    template="plotly_white",
)

# ---- Fondo transparente en gráfico de barras ----
grafico_ventas_por_linea_de_producto.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(grafico_ventas_por_linea_de_producto)

# ---- Mostrar ventas por hora (gráfico de barras) en streamlit ----
ventas_por_hora = df_selection.groupby(by=["hour"])[["Total"]].sum()
grafico_ventas_por_horas = px.bar(
    ventas_por_hora,
    x=ventas_por_hora.index,
    y="Total",
    title="<b>Ventas por hora</b>",
    color_discrete_sequence=["#0083B8"] * len(ventas_por_hora),
    template="plotly_white",
)
grafico_ventas_por_horas.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# ---- Mostrar 2 gráficos de ventas en la misma línea
columna_izquierda, columna_derecha = st.columns(2)
columna_izquierda.plotly_chart(grafico_ventas_por_horas, use_container_width=True)
columna_derecha.plotly_chart(grafico_ventas_por_linea_de_producto, use_container_width=True)