import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración SEO y layout ancho
st.set_page_config(
    page_title="Calculadora de Cuentas Remuneradas y Neobrókers 2026",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": (
            "Herramienta cuantitativa para simular el interés compuesto en"
            " cuentas flexibles."
        ),
    },
)

# CSS con control absoluto de contraste (Compatible con Modo Oscuro y Claro)
st.markdown(
    """
    <style>
    /* Fondo global */
    .stApp {
        background-color: #f4f6f9 !important;
        background-image: radial-gradient(circle at top right, #e2e8f0, #f4f6f9) !important;
        color: #1e1e1e !important;
    }
    
    /* Cabecera transparente */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Panel lateral */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e9ecef !important;
    }
    [data-testid="stSidebar"] * {
        color: #1e1e1e !important;
    }

    /* Tarjeta principal flotante */
    .block-container {
        background-color: #ffffff !important;
        border-radius: 15px !important;
        padding: 3rem !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05) !important;
        max-width: 1100px !important;
        margin-top: 4rem !important;
        margin-bottom: 3rem !important;
    }

    /* Blindaje de texto dentro de la tarjeta */
    .block-container p, .block-container h1, .block-container h2, .block-container h3, 
    .block-container span, .block-container label, .block-container div {
        color: #1e1e1e !important;
    }

    /* Ajuste para métricas de Streamlit */
    [data-testid="stMetricValue"] {
        color: #111827 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #6c757d !important;
    }

    /* Ajuste para inputs, numéricos y selectbox */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #f8f9fa !important;
        color: #1e1e1e !important;
        border-color: #e5e7eb !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="input"] input {
        color: #1e1e1e !important;
    }
    
    /* Estilo para las pestañas */
    button[data-baseweb="tab"] {
        color: #4b5563 !important;
    }
    button[aria-selected="true"] {
        color: #10b981 !important;
    }

    hr { margin-top: 1.5rem; margin-bottom: 1.5rem; border: 0; border-top: 1px solid #eaeaea; }
    .disclaimer, .disclaimer * { font-size: 0.8rem !important; color: #6b7280 !important; text-align: justify; margin-top: 40px; }
    </style>
""",
    unsafe_allow_html=True,
)

# Cabecera
st.title("💸 Simulador de Rendimiento: Cuentas Flexibles")
st.markdown(
    "**Calcula el beneficio neto real** de tu liquidez. Compara el impacto del"
    " interés compuesto diario frente al mensual, con el 19% de IRPF ya"
    " descontado."
)
st.markdown("---")

# Base de datos de brókers con enlaces
brokers = {
    "Trading 212 🟢": {
        "nombre_corto": "Trading 212",
        "tae": 0.035,
        "pago": "Diario",
        "liquidez": "Inmediata",
        "link": "https://www.trading212.com",
    },
    "Trade Republic 🔵": {
        "nombre_corto": "Trade Republic",
        "tae": 0.030,
        "pago": "Mensual",
        "liquidez": "Inmediata",
        "link": "https://traderepublic.com",
    },
    "Revolut (Flex) 🟣": {
        "nombre_corto": "Revolut",
        "tae": 0.028,
        "pago": "Diario",
        "liquidez": "Inmediata",
        "link": "https://revolut.com",
    },
    "XTB 🟡": {
        "nombre_corto": "XTB",
        "tae": 0.025,
        "pago": "Mensual",
        "liquidez": "Inmediata",
        "link": "https://www.xtb.com",
    },
}

# Panel Lateral
with st.sidebar:
  st.header("⚙️ Configuración")
  capital_inicial = st.number_input(
      "Capital inicial (€)", min_value=0.0, value=10000.0, step=1000.0
  )
  aportacion_mensual = st.number_input(
      "Aportación mensual (€)", min_value=0.0, value=300.0, step=50.0
  )
  anos = st.slider("Horizonte temporal (años)", 1, 20, 5)

  st.markdown("---")
  st.markdown(
      "💡 *Los intereses se capitalizan automáticamente según la frecuencia de"
      " pago de cada entidad.*"
  )

irpf = 0.19

tab1, tab2 = st.tabs(["📈 Análisis Detallado", "⚖️ Comparador Global"])

with tab1:
  selected_broker_key = st.selectbox(
      "Selecciona la plataforma a analizar", list(brokers.keys())
  )
  b_info = brokers[selected_broker_key]
  tae = b_info["tae"]

  col_info1, col_info2, col_info3 = st.columns(3)
  col_info1.metric("Rentabilidad (TAE)", f"{tae*100:.2f}%")
  col_info2.metric("Frecuencia", b_info["pago"])
  col_info3.metric("Liquidez", b_info["liquidez"])

  meses = anos * 12
  saldo_actual = capital_inicial
  total_aportado = capital_inicial
  beneficio_neto = 0
  historial = [{
      "Mes": 0,
      "Año": 0,
      "Capital Aportado": total_aportado,
      "Saldo Total": saldo_actual,
      "Beneficio Neto": 0,
  }]

  for m in range(1, meses + 1):
    saldo_actual += aportacion_mensual
    total_aportado += aportacion_mensual

    interes_mes = saldo_actual * (tae / 12) * (1 - irpf)
    beneficio_neto += interes_mes
    saldo_actual += interes_mes

    if m % 12 == 0 or m == meses:
      historial.append({
          "Mes": m,
          "Año": round(m / 12, 1),
          "Capital Aportado": round(total_aportado, 2),
          "Saldo Total": round(saldo_actual, 2),
          "Beneficio Neto": round(beneficio_neto, 2),
      })

  df = pd.DataFrame(historial)

  st.markdown("---")
  st.subheader("Proyección del Patrimonio")

  fig = px.area(
      df,
      x="Año",
      y=["Capital Aportado", "Beneficio Neto"],
      color_discrete_sequence=["#d1d5db", "#10b981"],
      labels={"value": "Euros (€)", "variable": "Desglose"},
  )
  fig.update_layout(
      legend=dict(
          orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
      ),
      margin=dict(l=0, r=0, t=30, b=0),
      plot_bgcolor="rgba(0,0,0,0)",
      paper_bgcolor="rgba(0,0,0,0)",
      hovermode="x unified",
  )
  fig.update_yaxes(showgrid=True, gridcolor="#f0f0f0")
  fig.update_xaxes(showgrid=False)
  st.plotly_chart(fig, use_container_width=True)

  st.info(
      f"⚡ **¿Todo listo para empezar?**\n\nAbre tu cuenta en"
      f" {b_info['nombre_corto']} en 5 minutos y empieza a generar intereses"
      " diarios/mensuales por tu liquidez."
  )
  st.link_button(
      f"👉 Abrir cuenta oficial en {b_info['nombre_corto']}",
      url=b_info["link"],
  )

with tab2:
  st.markdown("### Ranking y Comparativa Directa")
  st.markdown(
      f"Estimación para **{capital_inicial:,.2f} €** iniciales y"
      f" **{aportacion_mensual:,.2f} €/mes** durante **{anos} años**:"
  )
  st.markdown("---")

  # Muestra cada bróker ordenado con su botón de enlace directo
  for k, v in sorted(
      brokers.items(), key=lambda x: x[1]["tae"], reverse=True
  ):
    s_act = capital_inicial
    for m in range(1, meses + 1):
      s_act += aportacion_mensual
      int_m = s_act * (v["tae"] / 12) * (1 - irpf)
      s_act += int_m

    total_depositado = capital_inicial + (aportacion_mensual * meses)
    beneficio_neto_total = s_act - total_depositado

    c1, c2, c3, c4 = st.columns([2, 1.5, 2, 2])
    c1.markdown(f"**{k}**\n\nTAE: `{v['tae']*100:.2f}%` | Pago: {v['pago']}")
    c2.metric("Beneficio Neto", f"{beneficio_neto_total:,.2f} €")
    c3.metric("Saldo Final", f"{s_act:,.2f} €")
    with c4:
      st.write("")
      st.link_button(f"Abrir en {v['nombre_corto']}", url=v["link"])
    st.markdown("---")

# Sección FAQ y Disclaimer
st.markdown("### Preguntas Frecuentes")
with st.expander("¿Cómo se calcula el beneficio neto?"):
  st.write(
      "El simulador aplica la fórmula del interés compuesto sobre tu capital"
      " inicial y aportaciones. Al beneficio bruto generado se le aplica"
      " automáticamente la retención fiscal estándar del 19% correspondiente a"
      " las rentas del capital mobiliario en España."
  )
with st.expander("¿Cuál es la diferencia entre pago diario y mensual?"):
  st.write(
      "Plataformas como Trading 212 o Revolut abonan los intereses cada día,"
      " maximizando el interés compuesto acumulado. Otras como Trade Republic"
      " lo abonado el primer día laborable del mes siguiente."
  )

st.markdown(
    '<div class="disclaimer"><strong>Aviso legal:</strong> Esta herramienta es'
    " un simulador matemático basado en las TAEs públicas ofertadas por las"
    " entidades en el momento actual. No constituye asesoramiento financiero."
    " Las rentabilidades pasadas o promocionales no garantizan rendimientos"
    " futuros. La fiscalidad puede variar según la situación personal del"
    " usuario y su residencia fiscal (cálculos basados en la tributación"
    " estándar española del 19%).</div>",
    unsafe_allow_html=True,
)
