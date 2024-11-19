import pandas as pd
import requests
from tabula import read_pdf
import matplotlib.pyplot as plt

# Opciones de visualización para pandas
pd.set_option('display.max_columns', None)

# Paso 1: Cargar Datos de México desde PDF
def cargar_datos_mexico():
    # Descarga manual del PDF si es necesario
    # Utiliza Tabula para extraer tablas del PDF
    try:
        tablas_mexico = read_pdf("ruta_al_pdf_mexico.pdf", pages="all", multiple_tables=True)
        df_mexico = tablas_mexico[0]  # Selecciona la tabla correcta
    except Exception as e:
        print("Error al cargar los datos de México:", e)
        df_mexico = pd.DataFrame()
    return df_mexico

# Paso 2: Cargar Datos de Argentina desde un archivo Excel
def cargar_datos_argentina():
    try:
        df_argentina = pd.read_excel("ruta_al_excel_argentina.xlsx")
    except Exception as e:
        print("Error al cargar los datos de Argentina:", e)
        df_argentina = pd.DataFrame()
    return df_argentina

# Paso 3: Cargar Datos de Suecia desde el Banco Mundial
def cargar_datos_suecia():
    try:
        url = "https://api.worldbank.org/v2/en/indicator/BN.KLT.DINV.CD?downloadformat=excel"
        response = requests.get(url)
        with open("suecia_ied.xlsx", "wb") as file:
            file.write(response.content)
        df_suecia = pd.read_excel("suecia_ied.xlsx", sheet_name="Data")
    except Exception as e:
        print("Error al cargar los datos de Suecia:", e)
        df_suecia = pd.DataFrame()
    return df_suecia

# Cargar todos los datos
df_mexico = cargar_datos_mexico()
df_argentina = cargar_datos_argentina()
df_suecia = cargar_datos_suecia()

# Paso 4: Limpiar y Estandarizar los Datos
def limpiar_datos(df, pais):
    # Renombrar columnas y estandarizar formatos según sea necesario
    df.columns = [col.strip() for col in df.columns]  # Limpia espacios en nombres de columnas
    df['País'] = pais
    # Realiza más limpieza según los datos específicos de cada tabla
    return df

df_mexico = limpiar_datos(df_mexico, "México")
df_argentina = limpiar_datos(df_argentina, "Argentina")
df_suecia = limpiar_datos(df_suecia, "Suecia")

# Paso 5: Concatenar los DataFrames
df_total = pd.concat([df_mexico, df_argentina, df_suecia], ignore_index=True)

# Paso 6: Visualizar los Datos
def visualizar_datos(df):
    plt.figure(figsize=(10, 6))
    for pais in df['País'].unique():
        df_pais = df[df['País'] == pais]
        plt.plot(df_pais['Año'], df_pais['IED'], label=pais)
    plt.xlabel('Año')
    plt.ylabel('Inversión Extranjera Directa (IED)')
    plt.title('Evolución de la IED en México, Argentina y Suecia')
    plt.legend()
    plt.show()

# Ejemplo de Visualización
visualizar_datos(df_total)
