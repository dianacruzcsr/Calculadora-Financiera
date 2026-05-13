import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="Calculadora Financiera", layout="wide")
st.title("📊 Calculadora de Matemáticas Financieras")
st.markdown("Basada en el modelo de Excel proporcionado")

menu = st.sidebar.selectbox(
    "Selecciona una sección",
    [
        "Conversión de tasas",
        "Valor Futuro",
        "Valor Presente",
        "Tasa de rendimiento anual",
        "Número de periodos",
        "VF Rentas periódicas constantes",
        "VP Rentas periódicas constantes",
        "Tabla de amortización",
        "VF Renta creciente geométrica",
        "VP Renta creciente geométrica",
        "Valuación de Bonos",
        "Yield to Maturity (YTM)",
        "Valuación de acciones (Dividendos)",
        "Valuación por múltiplos",
        "Rendimiento requerido",
        "Precios Forward",
        "Opciones (Black-Scholes)",
        "Reinversión de intereses (Gráfica)",
    ]
)

st.markdown("---")

# ============================================================
# REINVERSIÓN DE INTERESES CON GRÁFICA
# ============================================================
if menu == "Reinversión de intereses (Gráfica)":
    st.header("Ilustración de la reinversión de los intereses")
    st.markdown("Comparación de montos acumulados según frecuencia de capitalización")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        i = st.number_input("i (tasa efectiva anual)", value=0.10, step=0.01, format="%.4f")
    with col2:
        C0 = st.number_input("C0 (capital inicial)", value=100000.0, step=10000.0)
    with col3:
        n = st.number_input("n (años)", value=10, step=1)
    
    st.markdown("---")
    
    # Definir frecuencias según el Excel
    frecuencias = [
        ("Cada 4 años", 1/4),
        ("Cada 2 años", 1/2),
        ("Anual", 1),
        ("Semestral", 2),
        ("Trimestral", 4),
        ("Mensual", 12),
        ("Semanal", 52),
        ("Diaria", 365),
        ("Cada hora", 8760),
        ("Cada minuto", 525600),
        ("Cada segundo", 31536000),
        ("Instantánea", float('inf'))
    ]
    
    resultados = []
    
    st.subheader("📈 Monto acumulado según frecuencia")
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        for nombre, m in frecuencias:
            if m == float('inf'):
                # Fórmula para capitalización continua
                monto = C0 * np.exp(i * n)
            else:
                # Fórmula correcta según Excel
                if m < 1:
                    # Para periodos mayores a 1 año (cada 4 años, cada 2 años)
                    monto = C0 * (1 + i * m) ** (n / m)
                else:
                    # Para periodos menores o iguales a 1 año
                    monto = C0 * (1 + i / m) ** (m * n)
            
            resultados.append({
                "Frecuencia": nombre,
                "m (veces al año)": m if m != float('inf') else "∞",
                "Monto acumulado": monto
            })
            
            # Mostrar en formato de métrica
            st.metric(nombre, f"${monto:,.2f}")
    
    with col_right:
        # Crear DataFrame para la gráfica
        df = pd.DataFrame(resultados)
        
        # Gráfica de barras
        fig = go.Figure()
        
        # Solo mostrar las primeras 8 frecuencias para mejor visualización
        df_plot = df.head(8).copy()
        
        fig.add_trace(go.Bar(
            x=df_plot["Frecuencia"],
            y=df_plot["Monto acumulado"],
            text=df_plot["Monto acumulado"].apply(lambda x: f"${x:,.0f}"),
            textposition='outside',
            marker_color='lightblue',
            name='Monto'
        ))
        
        # Línea horizontal del valor teórico (capitalización continua)
        monto_continuo = resultados[-1]["Monto acumulado"]
        fig.add_hline(y=monto_continuo, line_dash="dash", line_color="red",
                      annotation_text=f"Límite continuo: ${monto_continuo:,.0f}")
        
        fig.update_layout(
            title="Monto acumulado por frecuencia de capitalización",
            xaxis_title="Frecuencia de reinversión",
            yaxis_title="Monto acumulado ($)",
            yaxis_tickformat="$,.0f",
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfica de convergencia
        st.subheader("📉 Convergencia hacia la capitalización continua")
        
        # Crear datos para gráfica de líneas
        frecuencias_num = []
        montos = []
        
        for r in resultados:
            if r["m (veces al año)"] != "∞":
                m_val = r["m (veces al año)"]
                frecuencias_num.append(m_val)
                montos.append(r["Monto acumulado"])
        
        # Ordenar por frecuencia
        orden = np.argsort(frecuencias_num)
        frecuencias_ordenadas = np.array(frecuencias_num)[orden]
        montos_ordenados = np.array(montos)[orden]
        
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=frecuencias_ordenadas,
            y=montos_ordenados,
            mode='lines+markers',
            name='Monto acumulado',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        # Línea asintótica
        fig2.add_hline(y=monto_continuo, line_dash="dash", line_color="red",
                       annotation_text=f"Asíntota: ${monto_continuo:,.0f}")
        
        fig2.update_layout(
            title="Convergencia del monto hacia la capitalización continua",
            xaxis_title="Frecuencia de capitalización (veces por año)",
            yaxis_title="Monto acumulado ($)",
            xaxis_type="log",
            yaxis_tickformat="$,.0f",
            height=450,
            showlegend=True
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Tabla completa
    st.subheader("📋 Tabla completa de resultados")
    st.dataframe(
        df.style.format({
            "Monto acumulado": "${:,.2f}"
        }),
        use_container_width=True
    )
    
    # Explicación de fórmulas
    with st.expander("📖 Ver fórmulas utilizadas"):
        st.markdown("""
        ### Fórmulas según el Excel:
        
        **Para frecuencias m ≥ 1 (anual, semestral, etc.):**
