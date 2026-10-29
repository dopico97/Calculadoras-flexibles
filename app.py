import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# Configuración SEO y layout
st.set_page_config(
    page_title="Simulador Interés Compuesto 2026 | Trade Republic vs Trading 212 | Cálculo Neto IRPF",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "Simulador para calcular el beneficio neto real en cuentas remuneradas en España con IRPF descontado.",
    },
)

# CSS Limpio para aspecto SaaS (Modo Claro Forzado)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f6f9;
        background-image: radial-gradient(circle at top right, #e2e8f0, #f4f6f9);
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e9ecef;
    }
    .block-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 3rem !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        max-width: 1100px;
        margin-top: 4rem;
        margin-bottom: 3rem;
    }
    h1, h2, h3 { font-family: 'Inter', sans-serif; }
    hr { margin-top: 1.5rem; margin-bottom: 1.5rem; border: 0; border-top: 1px solid #eaeaea; }
    .disclaimer { font-size: 0.8rem; color: #6b7280; text-align: justify; margin-top: 40px; }
    </style>
""",
    unsafe_allow_html=True,
)

# Cabecera
st.title("💸 Simulador de Rendimiento: Cuentas Flexibles")
st.markdown(
    "**Calcula el beneficio neto real** de tu liquidez. Compara el impacto del"
    " interés compuesto diario frente al mensual, con el 19% de IRPF ya descontado."
)
st.markdown("---")

# Base de datos de brókers
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
      f" {b_info['nombre_corto']} en 5 minutos y empieza a generar intereses."
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

st.markdown("### Preguntas Frecuentes sobre Rentabilidad y Fiscalidad")

with st.expander("¿Cuánto paga Trade Republic o Trading 212 descontando impuestos en España?"):
  st.write(
      "Al utilizar este simulador de beneficio neto para cuentas remuneradas, la herramienta descuenta automáticamente "
      "la retención estándar del 19% de IRPF aplicada en España sobre los rendimientos del capital mobiliario. "
      "Esto te permite visualizar tu ganancia real neta sin sorpresas frente a Hacienda, comparando directamente "
      "las opciones de Trade Republic vs Trading 212."
  )

with st.expander("Calculadora de interés compuesto: ¿Mejor pago diario (Revolut Flex) o mensual?"):
  st.write(
      "La principal diferencia matemática radica en la frecuencia de capitalización. Plataformas como Revolut (Cuentas Flexibles) "
      "y Trading 212 ofrecen abono diario de intereses, lo que acelera el efecto del interés compuesto a largo plazo "
      "frente al pago mensual tradicional. Esta calculadora te permite proyectar visualmente esa diferencia de rentabilidad "
      "sobre tu patrimonio a lo largo de los años."
  )

with st.expander("¿Cómo calcular el beneficio neto real de mis ahorros frente a la inflación?"):
  st.write(
      "El cálculo exacto depende de tu capital inicial, aportaciones periódicas y el horizonte temporal. Seleccionando "
      "el neobróker en nuestro comparador global, obtendrás el desglose financiero preciso entre el capital que has depositado "
      "y los intereses netos generados, creando una proyección patrimonial a medida para proteger tu liquidez."
  )

st.markdown(
    '<div class="disclaimer"><strong>Aviso legal:</strong> Simulador matemático '
    "sin validez como asesoramiento financiero ni tributario. Cálculos basados en retención IRPF España (19%).</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <head>
        <meta name="google-site-verification" content=<meta name="google-site-verification" content="xg0jtIBmBD7L_TlG_jc4jGWCUpwSKM5v-rYpw6L45tc" />">
        <meta name="description" content="Simulador online gratuito para calcular el beneficio neto real en cuentas remuneradas y neobrókers en España aplicando el 19% de retención de IRPF.">
    </head>
    """,
    unsafe_allow_html=True,
)

import streamlit.components.v1 as components


# ==========================================
# SEGUIMIENTO GOOGLE ANALYTICS (Modo Debug)
# ==========================================
ga_snippet = """
<script async src="https://www.googletagmanager.com/gtag/js?id=G-40QXT5RVGK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-40QXT5RVGK', {
      'debug_mode': true
  });
</script>
"""

components.html(ga_snippet, height=0, width=0)
import uuid
import requests
import streamlit as st

# ==========================================
# RASTREO SERVER-SIDE GA4 (A prueba de móviles)
# ==========================================
GA_MEASUREMENT_ID = "G-40QXT5RVGK"
GA_API_SECRET = "jQsXK2F2RSuzrToEay-sxQ"  # <--- Sustituye por el secreto de API generado


def registrar_visita_servidor():
  if "user_client_id" not in st.session_state:
    st.session_state["user_client_id"] = str(uuid.uuid4())

    url = (
        "https://www.google-analytics.com/mp/collect"
        f"?measurement_id={GA_MEASUREMENT_ID}&api_secret={GA_API_SECRET}"
    )
    payload = {
        "client_id": st.session_state["user_client_id"],
        "events": [{
            "name": "page_view",
            "params": {
                "page_title": "Calculadora Cuentas Flexibles",
                "engagement_time_msec": "100",
            },
        }],
    }
    try:
      requests.post(url, json=payload, timeout=2)
    except Exception:
      pass


# Llama a la función al inicio de app.py
registrar_visita_servidor()
