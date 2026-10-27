import numpy as np
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Cuentas Flexibles",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Estilos CSS personalizados para mejorar el diseño visual
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    .broker-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Título principal y subtítulo
st.title("💸 Simulador de Cuentas Flexibles y Neobrókers")
st.markdown(
    "Calcula el beneficio neto real (descontando el 19% de IRPF) y compara la rentabilidad diaria o mensual de tu capital."
)

# Diccionario de brókers actualizado
brokers = {
    "Trading 212 🟢": {
        "nombre_corto": "Trading 212",
        "tae": 0.035,
        "pago": "Diario",
        "liquidez": "Inmediata",
        "link": "https://www.trading212.com/invite/TU_CODIGO_DE_AFILIADO",  # <--- Pon aquí tu enlace real
    },
    "Trade Republic 🔵": {
        "nombre_corto": "Trade Republic",
        "tae": 0.030,
        "pago": "Mensual",
        "liquidez": "Inmediata",
        "link": "https://traderepublic.com/en-es?raf=TU_CODIGO_DE_AFILIADO",  # <--- Pon aquí tu enlace real
    },
    "XTB 🟡": {
        "nombre_corto": "XTB",
        "tae": 0.025,
        "pago": "Mensual",
        "liquidez": "Inmediata",
        "link": "https://www.xtb.com/es/alta?from=TU_CODIGO_DE_AFILIADO",  # <--- Pon aquí tu enlace real
    },
    "Revolut (Flex) 🟣": {
        "nombre_corto": "Revolut",
        "tae": 0.028,
        "pago": "Diario",
        "liquidez": "Inmediata",
        "link": "https://revolut.com/referral/?referral-code=TU_CODIGO",  # <--- Pon aquí tu enlace real
    },
}
# Panel lateral de entradas
st.sidebar.header("⚙️ Parámetros de Inversión")
capital_inicial = st.sidebar.number_input(
    "Capital inicial (€)", min_value=0.0, value=5000.0, step=500.0
)
aportacion_mensual = st.sidebar.number_input(
    "Aportación mensual (€)", min_value=0.0, value=200.0, step=50.0
)
anos = st.sidebar.slider("Horizonte temporal (años)", 1, 10, 3)

irpf = 0.19  # Retención IRPF

# Creación de Pestañas (Tabs) para separar vistas
tab1, tab2 = st.tabs(["📊 Simulador Detallado", "⚖️ Comparativa de Brókers"])

with tab1:
  selected_broker_key = st.selectbox(
      "Selecciona la plataforma a simular", list(brokers.keys())
  )
  broker_info = brokers[selected_broker_key]
  tae = broker_info["tae"]

  # Bloque de métricas de condiciones del bróker
  st.markdown("### Condiciones de la Plataforma")
  col_info1, col_info2, col_info3 = st.columns(3)
  col_info1.metric("Rentabilidad (TAE)", f"{tae*100:.2f}%")
  col_info2.metric("Frecuencia de Pago", broker_info["pago"])
  col_info3.metric("Disponibilidad", broker_info["liquidez"])

  # Cálculos iniciales
  interes_diario_inicial = (capital_inicial * tae) / 365 * (1 - irpf)
  interes_mensual_inicial = (capital_inicial * tae) / 12 * (1 - irpf)
  interes_anual_inicial = capital_inicial * tae * (1 - irpf)

  st.markdown(
      f"### 📈 Resultados Estimados para: {broker_info['nombre_corto']}"
  )

  col1, col2, col3 = st.columns(3)
  col1.metric("Beneficio Diario (Neto)", f"{interes_diario_inicial:.2f} €")
  col2.metric("Beneficio Mensual (Neto)", f"{interes_mensual_inicial:.2f} €")
  col3.metric("Beneficio Anual (Neto)", f"{interes_anual_inicial:.2f} €")

  # Simulación temporal
  meses = anos * 12
  saldo_actual = capital_inicial
  total_aportado = capital_inicial
  beneficio_total_neto = 0
  historial = []

  for m in range(1, meses + 1):
    if m > 1:
      saldo_actual += aportacion_mensual
      total_aportado += aportacion_mensual

    interes_mes = saldo_actual * (tae / 12) * (1 - irpf)
    beneficio_total_neto += interes_mes
    saldo_actual += interes_mes

    if m % 12 == 0 or m == meses:
      historial.append(
          {
              "Año": int(m / 12),
              "Capital Aportado (€)": round(total_aportado, 2),
              "Beneficio Neto Acumulado (€)": round(beneficio_total_neto, 2),
              "Saldo Total (€)": round(saldo_actual, 2),
          }
      )

  df_resumen = pd.DataFrame(historial)

  st.markdown("### Evolución del Capital")
  st.line_chart(
      df_resumen.set_index("Año")[["Saldo Total (€)", "Capital Aportado (€)"]]
  )

  st.markdown("### Desglose Anual")
  st.dataframe(df_resumen, use_container_width=True)

  # Bloque de Afiliación con diseño destacado
  st.markdown("---")
  st.success(
      f"🚀 **¿Listo para empezar en {broker_info['nombre_corto']}?**\n\n"
      f"Abre tu cuenta en pocos minutos de forma totalmente online y empieza a rentabilizar tu liquidez sin ataduras.\n\n"
      f"[👉 Abrir cuenta en {broker_info['nombre_corto']} (Enlace Oficial)]"
  )

with tab2:
  st.markdown("### Comparativa General de Cuentas Flexibles")
  st.markdown(
      "Visualiza de un vistazo la rentabilidad neta estimada al año para tu capital inicial con cada plataforma."
  )

  comparativa_data = []
  for b_key, b_val in brokers.items():
    beneficio_neto_anual = capital_inicial * b_val["tae"] * (1 - irpf)
    comparativa_data.append(
        {
            "Plataforma": b_key,
            "TAE": f"{b_val['tae']*100:.2f}%",
            "Pago de Intereses": b_val["pago"],
            "Beneficio Neto Anual (1er Año)": round(beneficio_neto_anual, 2),
        }
    )

  df_comparativa = pd.DataFrame(comparativa_data)
  st.dataframe(df_comparativa, use_container_width=True, hide_index=True)

  st.info(
      "💡 *Nota: Los cálculos del beneficio neto anual se realizan aplicando la retención fiscal estándar del 19% sobre los rendimientos del ahorro en España.*"
  )
