# 📈 Pass-Through Analysis: Dólar Blue vs. Inflación (IPC) en Argentina

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow?logo=powerbi&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

Proyecto **End-to-End** de Análisis de Datos e Ingeniería de Pipelines para evaluar el fenómeno de **Pass-Through** (transmisión de shocks del tipo de cambio informal a la estructura general de precios minoristas) en Argentina para el período **2011 – Presente**.

---

## 📌 Resumen Ejecutivo & Key Findings

El análisis econométrico mediante **correlaciones cruzadas y estructura de rezagos (*lags*)** demuestra que el traspaso de una variación del Dólar Blue sobre el IPC no ocurre de manera instantánea en su totalidad, sino que presenta una inercia de absorción con su pico máximo a los 3 meses:

* **Efecto Inmediato ($t$):** `0.19` — Repaso directo inicial en productos dolarizados.
* **Efecto a 1 mes ($t-1 \rightarrow t$):** `0.19` — Persistencia inercial de precios.
* **Efecto a 2 meses ($t-2 \rightarrow t$):** `0.26` — Aceleración por reposición de stock.
* **Pico de Impacto a 3 meses ($t-3 \rightarrow t$):** `0.31` — Absorción máxima del shock cambiario.

---

## 🛠️ Arquitectura Técnica y Tubería ETL
1. **Extracción (Extract):** Scripts automatizados en Python consumiendo las APIs oficiales de indicadores macroeconómicos.
2. **Transformación (Transform):** Limpieza, cálculo de variaciones porcentuales simples y compuestas, generación de variables rezagadas ($t-1, t-2, t-3$) e imputación de series temporales.
3. **Almacenamiento (Load):** Modelado relacional y almacenamiento persistente en **SQLite** (`macroeconomia.db`).
4. **Visualización (BI):** Tablero ejecutivo interactivo en **Power BI** con métricas clave (KPIs), serie histórica combinada y acumulados anuales.

---

## 📂 Estructura del Repositorio

```text
├── data/
│   ├── macroeconomia.db          # Base de datos relacional SQLite
│   └── passthrough_dolar_ipc.csv # Dataset procesado listo para análisis
├── scripts/
│   └── etl_passthrough.py        # Pipeline de extracción, limpieza y cálculo de rezagos
├── dashboard/
│   ├── dashboard_passthrough.pbix # Archivo interactivo de Power BI
│   └── dashboard_preview.png     # Captura de pantalla del dashboard
├── docs/
│   └── Reporte_Ejecutivo.pdf     # Documento de resumen técnico
├── README.md
└── LICENSE
