import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# Configuración SEO y cambio a layout="wide" para aprovechar la pantalla
st.set_page_config(
    page_title="Calculadora de Cuentas Remuneradas y Neobrókers 2026",
    page_icon="💸",
    layout="wide",  # <--- Cambiado de "centered" a "wide"
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Herramienta cuantitativa para simular el interés compuesto en cuentas flexibles."
    }
)

# CSS Avanzado para aspecto de Tarjeta Flotante (SaaS)
st.markdown("""
    <style>
    /* Fondo general de la aplicación con un gradiente muy sutil */
    .stApp {
        background-color: #f4f6f9;
        background-image: radial-gradient(circle at top right, #e2e8f0, #f4f6f9);
    }
    
    /* Darle fondo blanco al panel lateral para que se integre mejor */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e9ecef;
    }

    /* Contenedor principal estilo "tarjeta" blanca flotante */
    .block-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 3rem !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        max-width: 1100px; /* Ancho máximo para que no sea infinito en monitores grandes */
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    /* Estilos de tipografía y métricas */
    h1, h2, h3 { color: #1e1e1e; font-family: 'Inter', sans-serif; }
    .stMetric label { color: #6c757d !important; font-weight: 600; font-size: 0.9rem; }
    .stMetric value { color: #111827 !important; font-weight: 800; }
    hr { margin-top: 1.5rem; margin-bottom: 1.5rem; border: 0; border-top: 1px solid #eaeaea; }
    .disclaimer { font-size: 0.8rem; color: #888; text-align: justify; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# Cabecera (Hero Section)
st.title("💸 Simulador de Rendimiento: Cuentas Flexibles")
st.markdown("**Calcula el beneficio neto real** de tu liquidez. Compara el impacto del interés compuesto diario frente al mensual, con el 19% de IRPF ya descontado.")
st.markdown("---")

# (A partir de aquí, deja tu código tal cual, empezando por el diccionario de brokers)

# Base de datos de brókers
brokers = {
    "Trading 212 🟢": {"nombre_corto": "Trading 212", "tae": 0.035, "pago": "Diario", "liquidez": "Inmediata", "link": "TU_ENLACE"},
    "Trade Republic 🔵": {"nombre_corto": "Trade Republic", "tae": 0.030, "pago": "Mensual", "liquidez": "Inmediata", "link": "TU_ENLACE"},
    "XTB 🟡": {"nombre_corto": "XTB", "tae": 0.025, "pago": "Mensual", "liquidez": "Inmediata", "link": "TU_ENLACE"},
    "Revolut (Flex) 🟣": {"nombre_corto": "Revolut", "tae": 0.028, "pago": "Diario", "liquidez": "Inmediata", "link": "TU_ENLACE"},
}

# Sidebar - Panel de control
with st.sidebar:
    st.header("⚙️ Configuración")
    capital_inicial = st.number_input("Capital inicial (€)", min_value=0.0, value=10000.0, step=1000.0)
    aportacion_mensual = st.number_input("Aportación mensual (€)", min_value=0.0, value=300.0, step=50.0)
    anos = st.slider("Horizonte temporal (años)", 1, 20, 5)
    
    st.markdown("---")
    st.markdown("💡 *Los intereses se capitalizan automáticamente según la frecuencia de pago de cada entidad.*")

irpf = 0.19

tab1, tab2 = st.tabs(["📈 Análisis Detallado", "⚖️ Comparador Global"])

with tab1:
    selected_broker_key = st.selectbox("Selecciona la plataforma a analizar", list(brokers.keys()))
    b_info = brokers[selected_broker_key]
    tae = b_info["tae"]

    # Dashboard de métricas principales
    col_info1, col_info2, col_info3 = st.columns(3)
    col_info1.metric("Rentabilidad (TAE)", f"{tae*100:.2f}%")
    col_info2.metric("Frecuencia", b_info["pago"])
    col_info3.metric("Liquidez", b_info["liquidez"])

    # Simulación Matemática
    meses = anos * 12
    saldo_actual = capital_inicial
    total_aportado = capital_inicial
    beneficio_neto = 0
    historial = [{"Mes": 0, "Año": 0, "Capital Aportado": total_aportado, "Saldo Total": saldo_actual, "Beneficio Neto": 0}]

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
                "Beneficio Neto": round(beneficio_neto, 2)
            })

    df = pd.DataFrame(historial)

    st.markdown("---")
    st.subheader("Proyección del Patrimonio")
    
    # Gráfico interactivo profesional con Plotly
    fig = px.area(
        df, 
        x="Año", 
        y=["Capital Aportado", "Saldo Total"],
        color_discrete_sequence=["#9ca3af", "#10b981"],
        labels={"value": "Euros (€)", "variable": "Métrica"}
    )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified"
    )
    fig.update_yaxes(showgrid=True, gridcolor="#f0f0f0")
    fig.update_xaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True)

    # CTA de Afiliación (Call To Action)
    st.info(f"⚡ **¿Todo listo para empezar?**\n\nAbre tu cuenta en {b_info['nombre_corto']} en 5 minutos y empieza a generar intereses diarios/mensuales por tu liquidez.")
    st.link_button(f"👉 Abrir cuenta oficial en {b_info['nombre_corto']}", url=b_info["link"])

with tab2:
    st.markdown("### Ranking de Rentabilidad Estimada")
    st.markdown(f"Basado en un capital de **{capital_inicial:,.2f} €** y aportaciones de **{aportacion_mensual:,.2f} €/mes** durante **{anos} años**.")
    
    comp_data = []
    for k, v in brokers.items():
        s_act = capital_inicial
        for m in range(1, meses + 1):
            s_act += aportacion_mensual
            int_m = s_act * (v["tae"] / 12) * (1 - irpf)
            s_act += int_m
        
        comp_data.append({
            "Plataforma": v["nombre_corto"],
            "TAE": f"{v['tae']*100:.2f}%",
            "Pago": v["pago"],
            "Capital Final (€)": round(s_act, 2),
            "Beneficio Neto Total (€)": round(s_act - (capital_inicial + aportacion_mensual*meses), 2)
        })
    
    df_comp = pd.DataFrame(comp_data).sort_values(by="Beneficio Neto Total (€)", ascending=False)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

# Sección SEO y Confianza (Expanders)
st.markdown("---")
st.subheader("Preguntas Frecuentes")
with st.expander("¿Cómo se calcula el beneficio neto?"):
    st.write("El simulador aplica la fórmula del interés compuesto sobre tu capital inicial y aportaciones mensuales. Al beneficio bruto generado se le aplica automáticamente la retención fiscal estándar del 19% correspondiente a las rentas del capital mobiliario en España.")
with st.expander("¿Cuál es la diferencia entre pago diario y mensual?"):
    st.write("Plataformas como Trading 212 o Revolut abonan los intereses cada día, lo que significa que al día siguiente generas intereses sobre los intereses del día anterior (mayor efecto bola de nieve). Otras como Trade Republic lo hacen el día 1 de cada mes.")

# Disclaimer Legal
st.markdown('<div class="disclaimer"><strong>Aviso legal:</strong> Esta herramienta es un simulador matemático basado en las TAEs públicas ofertadas por las entidades en el momento actual. No constituye asesoramiento financiero. Las rentabilidades pasadas o promocionales no garantizan rendimientos futuros. La fiscalidad puede variar según la situación personal del usuario y su residencia fiscal (cálculos basados en la tributación estándar española del 19%).</div>', unsafe_allow_html=True)
