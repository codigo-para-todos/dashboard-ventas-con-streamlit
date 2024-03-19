from _ast import pattern

import pandas as pd

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

# Obtener Dataframe
df = get_data_from_excel()

# Imprimir Dataframe
print(df)
