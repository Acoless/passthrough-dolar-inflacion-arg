# %% [markdown]
# Paso 1: Importacion de librerias y extraccion de datos del Dolar
# 

# %%
import requests
import pandas as pd

url_dolar = "https://api.argentinadatos.com/v1/cotizaciones/dolares"

print("Datos Dolar")
respuesta = requests.get(url_dolar)
datos_json = respuesta.json()

df_dolares_raw = pd.DataFrame(datos_json)

print("Filas y columnas descargadas:", df_dolares_raw.shape)
df_dolares_raw.head()

# %%
df_blue = df_dolares_raw[df_dolares_raw['casa'] == 'blue'].copy()

df_blue = df_blue.drop(columns=['casa'])

df_blue['fecha'] = pd.to_datetime(df_blue['fecha'])

df_blue = df_blue.sort_values(by='fecha').reset_index(drop=True)

print('Tabla limpia')
print(df_blue.info())

df_blue.head()

# %% [markdown]
# Traigo la informacion de la inflacion mensual (IPC) de ArgentinaDatos

# %%
url_inflacion = 'https://api.argentinadatos.com/v1/finanzas/indices/inflacion'

print('Trayendo datos IPC')
resp_inflacion = requests.get(url_inflacion)
df_inflacion_raw = pd.DataFrame(resp_inflacion.json())

print('Filas y columnas:', df_inflacion_raw.shape)
df_inflacion_raw.tail()

# %%
df_inflacion = df_inflacion_raw.copy()
df_inflacion['fecha'] = pd.to_datetime(df_inflacion['fecha'])
df_inflacion = df_inflacion.rename(columns={'valor': 'inflacion_mensual'})

df_blue['anio_mes'] = df_blue['fecha'].dt.to_period('M')

df_dolar_mensual = df_blue.groupby('anio_mes')['venta'].mean().reset_index()
df_dolar_mensual = df_dolar_mensual.rename(columns={'venta': 'dolar_promedio'})

df_dolar_mensual['dolar_variacion_pct'] = df_dolar_mensual['dolar_promedio'].pct_change() * 100

df_dolar_mensual.tail()


# %% [markdown]
# MERGE. union de tablas 
# 

# %%
df_inflacion['anio_mes'] = df_inflacion['fecha'].dt.to_period('M')

df_final = pd.merge(
    df_dolar_mensual,
    df_inflacion[['anio_mes', 'inflacion_mensual']],
    on='anio_mes',
    how='inner'
)

df_final = df_final.dropna().reset_index(drop=True)

df_final.tail(10)

# %% [markdown]
# Graficar con matplotlib y seaborn 

# %%
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')
plt.figure(figsize=(12, 6))

fechas_str = df_final['anio_mes'].astype(str)

plt.plot(fechas_str, df_final['dolar_variacion_pct'], label='Variacion Dolar Blue (%)', color='#1f77b4', linewidth=2)
plt.plot(fechas_str, df_final['inflacion_mensual'], label='Inflacion IPC (%)', color='#d62728', linewidth=2.5, linestyle='--')

plt.title('Comparativa Mensual: Variacion del Dolar Blue vs. Inflacion (IPC)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Periodo (Año-Mes)', fontsize=11)
plt.ylabel('Porcentaje (%)', fontsize=11)

plt.xticks(fechas_str[::6], rotation=45)

plt.legend(fontsize=11)
plt.tight_layout()
plt.show()

correlacion = df_final['dolar_variacion_pct'].corr(df_final['inflacion_mensual'])
print(f"📊 Coeficiente de correlación de Pearson entre Dólar e Inflación: {correlacion:.2f}")


# %% [markdown]
# Medir la correlacion con rezagos (Pass-Trhough)

# %%
corr_mismo_mes = df_final['dolar_variacion_pct'].corr(df_final['inflacion_mensual'])
corr_lag_1 = df_final['dolar_variacion_pct'].shift(1).corr(df_final['inflacion_mensual'])
corr_lag_2 = df_final['dolar_variacion_pct'].shift(2).corr(df_final['inflacion_mensual'])
corr_lag_3 = df_final['dolar_variacion_pct'].shift(3).corr(df_final['inflacion_mensual'])

print('ANALISIS DE PASS-TRHOUGH (REDUCCION DE REZAGOS)')
print(f'Impacto en el mismo mes (t): {corr_mismo_mes:.2f}')
print(f'Impacto a 1 mes (dolar t-1 -> Inflacion t): {corr_lag_1:.2f}')
print(f'Impacto a 2 meses (dolar t-2 -> Inflacion t): {corr_lag_2:.2f}')
print(f'Impacto a 3 meses (dolar t-3 -> Inflacion t): {corr_lag_3:.2f}')

# %% [markdown]
# ## 📝 Conclusiones del Análisis de Pass-Through
# * **Inercia Cambiaria:** La cotización del Dólar Blue presenta picos de volatilidad mucho más agresivos en comparación con la inflación del IPC.
# * **Desfasaje Temporal:** El análisis de rezagos (*lags*) confirma que el impacto del dólar sobre los precios al consumidor alcanza su mayor correlación a los **3 meses de ocurrido el movimiento cambiario** (pasando de 0.19 a 0.31).

# %% [markdown]
# ## Creacion de SQLlite 
# * **Base de datos** Creamos una base de datos para poder almacernar nuestra informacion y completar nuestro proyecto end-to-end
# 

# %%
import sqlite3  

df_sql = df_final.copy()
df_sql['anio_mes'] = df_sql['anio_mes'].astype(str)

conexion = sqlite3.connect('macroeconomia.db')

df_sql.to_sql('passthrough_dolar_ipc', conexion, if_exists='replace', index=False)

print('Base de datos creada')

conexion.close()


# %%
conexion = sqlite3.connect('macroeconomia.db')

query_sql = """
    SELECT anio_mes, dolar_promedio, dolar_variacion_pct, inflacion_mensual
    FROM passthrough_dolar_ipc
    WHERE dolar_variacion_pct > 10
    ORDER BY dolar_variacion_pct DESC;
"""

df_top_saltos = pd.read_sql_query(query_sql, conexion)
conexion.close()

print("Meses con saltos del Dólar mayores al 10% (Consulta SQL):")
df_top_saltos.head(10)

# %%
df_final.to_csv('passthrough_dolar_ipc.csv', index=False)

# %%



