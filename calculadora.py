import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import norm
import math

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
    ]
)

st.markdown("---")

# ============================================================
# 1. CONVERSIÓN DE TASAS (FÓRMULAS EXACTAS DEL EXCEL)
# ============================================================
if menu == "Conversión de tasas":
    st.header("Conversión de tasas de interés")
    st.markdown("### La triple igualdad de tasas de interés")
    
    # De tasas nominales i(m) a tasas efectivas i e instantáneas d
    st.subheader("📌 De tasas nominales i(m) a tasas efectivas i e instantáneas δ")
    col1, col2 = st.columns(2)
    
    with col1:
        i_nominal = st.number_input("i(m) =", value=0.20, step=0.01, format="%.4f")
        m = st.number_input("m =", value=2.0, step=0.5, format="%.4f")
    
    with col2:
        if m > 0:
            # Fórmula exacta del Excel: =((1+C9/C10)^C10)-1
            i_efectiva = ((1 + i_nominal/m) ** m) - 1
            # Fórmula exacta del Excel: =C10*LN(1+C9/C10)
            delta = m * np.log(1 + i_nominal/m)
            
            st.info(f"**i =** {i_efectiva:.6%}")
            st.info(f"**δ =** {delta:.6%}")
            st.caption(f"Fórmula i = ((1 + {i_nominal}/{m})^{m}) - 1")
            st.caption(f"Fórmula δ = {m} × LN(1 + {i_nominal}/{m})")
    
    st.markdown("---")
    
    # De tasas instantáneas d a tasa efectiva i
    st.subheader("📌 De tasas instantáneas δ a tasa efectiva i")
    col3, col4 = st.columns(2)
    
    with col3:
        delta2 = st.number_input("δ =", value=0.0975803283388641, step=0.01, format="%.6f")
    
    with col4:
        # Fórmula exacta del Excel: =EXP(C14)-1
        i_efectiva2 = np.exp(delta2) - 1
        st.info(f"**i =** {i_efectiva2:.6%}")
        st.caption(f"Fórmula i = EXP(δ) - 1")
    
    st.markdown("---")
    
    # De tasas instantáneas d a tasas nominales i(m)
    st.subheader("📌 De tasas instantáneas δ a tasas nominales i(m)")
    col5, col6 = st.columns(2)
    
    with col5:
        delta3 = st.number_input("δ =", value=0.025, step=0.001, format="%.6f", key="delta3")
        m2 = st.number_input("m =", value=2.0, step=1.0, format="%.4f", key="m2")
    
    with col6:
        if m2 > 0:
            # Fórmula exacta del Excel: =(EXP(C18/C19)-1)*C19
            i_nominal2 = (np.exp(delta3 / m2) - 1) * m2
            st.info(f"**i(m) =** {i_nominal2:.6%}")
            st.caption(f"Fórmula i(m) = (EXP(δ/{m2}) - 1) × {m2}")
    
    st.markdown("---")
    
    # De tasas nominales i(m) a tasas nominales i(p)
    st.subheader("📌 De tasas nominales i(m) a tasas nominales i(p)")
    col7, col8 = st.columns(2)
    
    with col7:
        m3 = st.number_input("m =", value=2.0, step=1.0, format="%.4f", key="m3")
        i_nominal3 = st.number_input("i(m) =", value=0.10, step=0.01, format="%.4f", key="im3")
        p = st.number_input("p =", value=3.0, step=1.0, format="%.4f")
    
    with col8:
        if m3 > 0 and p > 0:
            # Fórmula exacta del Excel: =((1+C24/C23)^(C23/C25))-1
            i_efectiva_periodo = ((1 + i_nominal3/m3) ** (m3/p)) - 1
            i_p = i_efectiva_periodo * p
            st.info(f"**i(p) =** {i_p:.6%}")
            st.caption(f"Fórmula i(p) = ((1 + {i_nominal3}/{m3})^({m3}/{p}) - 1) × {p}")
    
    st.markdown("---")
    
    # Ilustración de la reinversión
    st.subheader("📌 Ilustración de la reinversión de intereses")
    col9, col10 = st.columns(2)
    
    with col9:
        i_ejemplo = st.number_input("i =", value=0.10, step=0.01, format="%.4f", key="i_ej")
        C0_ej = st.number_input("C0 =", value=100000.0, key="c0_ej")
        n_ej = st.number_input("n =", value=10, key="n_ej")
    
    with col10:
        st.markdown("**Monto acumulado:**")
        
        # Fórmulas exactas del Excel
        # Cada 4 años: m = 1/4
        monto_cada4 = C0_ej * ((1 + i_ejemplo/(1/4)) ** (1/4))
        st.metric("Cada 4 años", f"${monto_cada4:,.2f}")
        
        # Cada 2 años: m = 1/2
        monto_cada2 = C0_ej * ((1 + i_ejemplo/(1/2)) ** (1/2))
        st.metric("Cada 2 años", f"${monto_cada2:,.2f}")
        
        # Anual: m = 1
        monto_anual = C0_ej * ((1 + i_ejemplo/1) ** 1)
        st.metric("Anual", f"${monto_anual:,.2f}")
        
        # Semestral: m = 2
        monto_semestral = C0_ej * ((1 + i_ejemplo/2) ** 2)
        st.metric("Semestral", f"${monto_semestral:,.2f}")
        
        # Trimestral: m = 4
        monto_trimestral = C0_ej * ((1 + i_ejemplo/4) ** 4)
        st.metric("Trimestral", f"${monto_trimestral:,.2f}")
        
        # Mensual: m = 12
        monto_mensual = C0_ej * ((1 + i_ejemplo/12) ** 12)
        st.metric("Mensual", f"${monto_mensual:,.2f}")
        
        # Instantánea: m = ∞
        monto_instantanea = C0_ej * np.exp(i_ejemplo)
        st.metric("Instantánea", f"${monto_instantanea:,.2f}")

# ============================================================
# 2. VALOR FUTURO (FÓRMULAS EXACTAS DEL EXCEL)
# ============================================================
elif menu == "Valor Futuro":
    st.header("Valor futuro de una inversión")
    
    tipo = st.radio("Selecciona el tipo de tasa:", 
                    ["Tasa efectiva anual i", "Tasa nominal i(m)", "Tasa instantánea δ"])
    
    if tipo == "Tasa efectiva anual i":
        C0 = st.number_input("C0 =", value=20000.0)
        i = st.number_input("i =", value=0.068)
        n = st.number_input("n =", value=6)
        
        # Fórmula exacta del Excel: =C7*((1+C8)^C9)
        Cn = C0 * ((1 + i) ** n)
        
        st.success(f"## Cn = ${Cn:,.2f}")
        st.caption(f"Fórmula: Cn = C0 × (1 + i)^{n}")
    
    elif tipo == "Tasa nominal i(m)":
        C0 = st.number_input("C0 =", value=54000.0)
        i_nom = st.number_input("i(m) =", value=0.1125)
        n = st.number_input("n = (años)", value=8)  # 1997-1989 = 8
        m = st.number_input("m = (frecuencia)", value=13)
        
        if m > 0:
            # Fórmula exacta del Excel: =C17*((1+C21)^(C19*C20))
            # donde C21 = i(m)/m
            i_efectiva_periodo = i_nom / m
            periodos_totales = n * m
            Cn = C0 * ((1 + i_efectiva_periodo) ** periodos_totales)
            
            st.success(f"## Cn = ${Cn:,.2f}")
            st.caption(f"Fórmula: Cn = C0 × (1 + i(m)/m)^(n×m)")
            st.caption(f"i(m)/m = {i_efectiva_periodo:.6%}")
            st.caption(f"n×m = {periodos_totales} periodos")
    
    else:  # Tasa instantánea
        C0 = st.number_input("C0 =", value=5000.0)
        d = st.number_input("δ =", value=0.10)
        n = st.number_input("n =", value=9)
        
        # Fórmula exacta del Excel: =C29*EXP(C30*C31)
        Cn = C0 * np.exp(d * n)
        
        st.success(f"## Cn = ${Cn:,.2f}")
        st.caption(f"Fórmula: Cn = C0 × e^(δ×n)")

# ============================================================
# 3. VALOR PRESENTE (FÓRMULAS EXACTAS DEL EXCEL)
# ============================================================
elif menu == "Valor Presente":
    st.header("Valor presente de una cantidad futura")
    
    tipo = st.radio("Selecciona el tipo de tasa:", 
                    ["Tasa efectiva anual i", "Tasa nominal i(m)", "Tasa instantánea δ"])
    
    if tipo == "Tasa efectiva anual i":
        Cn = st.number_input("Cn =", value=245000.0)
        i = st.number_input("i =", value=0.112)
        n = st.number_input("n =", value=9)
        
        # Fórmula exacta del Excel: =C7*((1+C8)^(-C9))
        C0 = Cn * ((1 + i) ** (-n))
        
        st.success(f"## C0 = ${C0:,.2f}")
        st.caption(f"Fórmula: C0 = Cn × (1 + i)^(-n)")
    
    elif tipo == "Tasa nominal i(m)":
        Cn = st.number_input("Cn =", value=1000.0)
        i_nom = st.number_input("i(m) =", value=0.10)
        n = st.number_input("n = (años)", value=10)
        m = st.number_input("m = (frecuencia)", value=2)
        
        if m > 0:
            # Fórmula exacta del Excel: =C18*((1+C22)^(-C20*C21))
            i_efectiva_periodo = i_nom / m
            periodos_totales = n * m
            C0 = Cn * ((1 + i_efectiva_periodo) ** (-periodos_totales))
            
            st.success(f"## C0 = ${C0:,.2f}")
            st.caption(f"Fórmula: C0 = Cn × (1 + i(m)/m)^(-n×m)")
    
    else:  # Tasa instantánea
        Cn = st.number_input("Cn =", value=1000.0)
        d = st.number_input("δ =", value=0.10)
        n = st.number_input("n =", value=10)
        
        # Fórmula exacta del Excel: =C31*EXP(-C32*C33)
        C0 = Cn * np.exp(-d * n)
        
        st.success(f"## C0 = ${C0:,.2f}")
        st.caption(f"Fórmula: C0 = Cn × e^(-δ×n)")

# ============================================================
# 4. TASA DE RENDIMIENTO (FÓRMULA EXACTA DEL EXCEL)
# ============================================================
elif menu == "Tasa de rendimiento anual":
    st.header("Tasa de rendimiento efectivo anual o tasa de crecimiento geométrico")
    
    C0 = st.number_input("C0 = (Valor inicial)", value=4582500.0)
    Cn = st.number_input("Cn = (Valor final)", value=9360000.0)
    n = st.number_input("n = (Número de periodos)", value=10)
    
    if n > 0:
        # Fórmula exacta del Excel: =((C10/C9)^(1/C11))-1
        i = ((Cn / C0) ** (1 / n)) - 1
        
        st.success(f"## i = {i:.6%}")
        st.caption(f"Fórmula: i = (Cn/C0)^(1/n) - 1")

# ============================================================
# 5. NÚMERO DE PERIODOS (FÓRMULA EXACTA DEL EXCEL)
# ============================================================
elif menu == "Número de periodos":
    st.header("Determinación del número de periodos")
    
    C0 = st.number_input("C0 =", value=50000.0)
    Cn = st.number_input("Cn =", value=245000.0)
    i = st.number_input("i =", value=0.043)
    
    if Cn > C0 and i > 0:
        # Fórmula exacta del Excel: =LN(C9/C8)/LN(1+C10)
        n = np.log(Cn / C0) / np.log(1 + i)
        
        st.success(f"## n = {n:.6f} años")
        
        # Desglose como en el Excel
        años = int(n)
        meses = int((n - años) * 12)
        dias = int(((n - años) * 12 - meses) * 30.42)
        
        st.info(f"**Equivalente:** {años} años, {meses} meses, {dias} días")
        st.caption(f"Fórmula: n = LN(Cn/C0) / LN(1+i)")

# ============================================================
# 6. VF RENTAS CONSTANTES (FÓRMULA EXACTA DEL EXCEL)
# ============================================================
elif menu == "VF Rentas periódicas constantes":
    st.header("Valor futuro de rentas vencidas constantes")
    
    renta = st.number_input("Renta =", value=1000.0)
    i_nom = st.number_input("i(m) =", value=0.07)
    n = st.number_input("n = (años)", value=1)
    m = st.number_input("m = (frecuencia)", value=2)
    
    if m > 0:
        # Fórmula exacta del Excel: =C8*C14 donde C14 = (((1+C12)^(C10*C11))-1)/C12
        i_efectiva_periodo = i_nom / m
        periodos_totales = n * m
        factor_vf = (((1 + i_efectiva_periodo) ** periodos_totales) - 1) / i_efectiva_periodo
        vf = renta * factor_vf
        
        st.success(f"## Valor Futuro = ${vf:,.2f}")
        st.caption(f"Fórmula: VF = R × [((1 + i(m)/m)^(n×m) - 1) / (i(m)/m)]")

# ============================================================
# 7. VP RENTAS CONSTANTES (FÓRMULA EXACTA DEL EXCEL)
# ============================================================
elif menu == "VP Rentas periódicas constantes":
    st.header("Valor presente de rentas vencidas constantes")
    
    renta = st.number_input("Renta =", value=6100.0)
    i_nom = st.number_input("i(m) =", value=0.05)
    n = st.number_input("n = (años)", value=5)
    m = st.number_input("m = (frecuencia)", value=1)
    
    if m > 0:
        # Fórmula exacta del Excel: =C8*C14 donde C14 = (1-((1+C12)^(-C10*C11)))/C12
        i_efectiva_periodo = i_nom / m
        periodos_totales = n * m
        factor_vp = (1 - ((1 + i_efectiva_periodo) ** (-periodos_totales))) / i_efectiva_periodo
        vp = renta * factor_vp
        
        st.success(f"## Valor Presente = ${vp:,.2f}")
        st.caption(f"Fórmula: VP = R × [1 - (1 + i(m)/m)^(-n×m)] / (i(m)/m)")

# ============================================================
# 8. TABLA DE AMORTIZACIÓN
# ============================================================
elif menu == "Tabla de amortización":
    st.header("Amortización de una deuda")
    
    VP = st.number_input("VP (Valor presente de la deuda)", value=584990.0)
    enganche_pct = st.number_input("Enganche (%)", value=15.0) / 100
    i_nom = st.number_input("i(m) = (tasa nominal)", value=0.1789)
    n = st.number_input("n = (años)", value=5)  # 60/12 = 5
    m = st.number_input("m = (pagos por año)", value=12)
    
    if m > 0:
        financiamiento = VP * (1 - enganche_pct)
        i_periodo = i_nom / m
        periodos_totales = n * m
        
        # Fórmula exacta del Excel: =PMT(C12,C10*C11,-H10,,0)
        if i_periodo > 0:
            renta = financiamiento * (i_periodo * (1 + i_periodo) ** periodos_totales) / ((1 + i_periodo) ** periodos_totales - 1)
            
            st.success(f"## Renta mensual = ${renta:,.2f}")
            
            if st.button("Mostrar tabla de amortización"):
                saldo = financiamiento
                data = []
                for periodo in range(1, min(13, periodos_totales + 1)):
                    interes = saldo * i_periodo
                    capital = renta - interes
                    saldo -= capital
                    data.append([periodo, interes, capital, max(saldo, 0)])
                
                df = pd.DataFrame(data, columns=["Periodo", "Intereses", "Capital", "Saldo"])
                st.dataframe(df)

# ============================================================
# 9. VF RENTA CRECIENTE GEOMÉTRICA
# ============================================================
elif menu == "VF Renta creciente geométrica":
    st.header("Valor futuro de rentas crecientes geométricas")
    
    R1 = st.number_input("R1 = (Primera renta)", value=400.0)
    i_nom = st.number_input("i(m) =", value=0.0369)
    n = st.number_input("n = (años)", value=42)
    m = st.number_input("m = (frecuencia)", value=6)
    q = st.number_input("q = (tasa crecimiento)", value=0.005)
    
    if m > 0:
        i_periodo = i_nom / m
        q_periodo = q / m
        periodos_totales = n * m
        
        # Fórmula exacta del Excel: =(((1+C12)^(C10*C11))-((1+C14)^(C10*C11)))/(C12-C14)
        if i_periodo != q_periodo:
            factor_vf = (((1 + i_periodo) ** periodos_totales) - ((1 + q_periodo) ** periodos_totales)) / (i_periodo - q_periodo)
        else:
            factor_vf = periodos_totales * (1 + i_periodo) ** (periodos_totales - 1)
        
        vf = R1 * factor_vf
        
        st.success(f"## Valor Futuro = ${vf:,.2f}")

# ============================================================
# 10. VP RENTA CRECIENTE GEOMÉTRICA
# ============================================================
elif menu == "VP Renta creciente geométrica":
    st.header("Valor presente de rentas crecientes geométricas")
    
    R1 = st.number_input("R1 = (Primera renta)", value=150000.0)
    i_nom = st.number_input("i(m) =", value=0.11)
    n = st.number_input("n = (años)", value=6.25)  # 25/4 = 6.25
    m = st.number_input("m = (frecuencia)", value=4)
    q = st.number_input("q = (tasa crecimiento)", value=0.02)
    
    if m > 0:
        i_periodo = i_nom / m
        q_periodo = q / m
        periodos_totales = n * m
        
        # Fórmula exacta del Excel: =((1-((1+C15)/(1+C13))^(C11*C12))/(C13-C15))
        if i_periodo != q_periodo:
            factor_vp = (1 - ((1 + q_periodo) / (1 + i_periodo)) ** periodos_totales) / (i_periodo - q_periodo)
        else:
            factor_vp = periodos_totales / (1 + i_periodo)
        
        vp = R1 * factor_vp
        
        st.success(f"## Valor Presente = ${vp:,.2f}")

# ============================================================
# 11. VALUACIÓN DE BONOS
# ============================================================
elif menu == "Valuación de Bonos":
    st.header("Valuación de bonos")
    
    VN = st.number_input("VN = (Valor nominal)", value=1000.0)
    tasa_cupon = st.number_input("Tasa cupón anual =", value=0.08)
    ytm = st.number_input("Yield to maturity =", value=0.04)
    T = st.number_input("T = (años)", value=9)
    periodicidad = st.number_input("Periodicidad del cupón =", value=1)
    
    if periodicidad > 0:
        cupon_periodico = VN * tasa_cupon / periodicidad
        r_periodico = ytm / periodicidad
        periodos_totales = T * periodicidad
        
        # Fórmulas exactas del Excel
        factor_vp_cupones = (1 - (1 + r_periodico) ** (-periodos_totales)) / r_periodico
        factor_vp_vn = (1 + r_periodico) ** (-periodos_totales)
        
        precio = cupon_periodico * factor_vp_cupones + VN * factor_vp_vn
        
        st.success(f"## Precio del Bono = ${precio:,.2f}")
        
        if precio > VN:
            st.info("🔷 Bono cotiza con prima (precio > valor nominal)")
        elif precio < VN:
            st.info("🔶 Bono cotiza con descuento (precio < valor nominal)")
        else:
            st.info("⚪ Bono cotiza a la par")

# ============================================================
# 12. YIELD TO MATURITY
# ============================================================
elif menu == "Yield to Maturity (YTM)":
    st.header("Determinación del Yield to Maturity")
    
    VN = st.number_input("VN = (Valor nominal)", value=1000.0)
    precio_mercado = st.number_input("B Mercado = (Precio de mercado)", value=1110.0)
    tasa_cupon = st.number_input("Tasa cupón anual =", value=0.09)
    T = st.number_input("T = (años)", value=15)
    periodicidad = st.number_input("Periodicidad del cupón =", value=2)
    
    if periodicidad > 0:
        cupon_periodico = VN * tasa_cupon / periodicidad
        periodos_totales = T * periodicidad
        
        # Usamos el método de Newton-Raphson para encontrar YTM
        def precio_bono(ytm_periodico):
            factor_vp_cupones = (1 - (1 + ytm_periodico) ** (-periodos_totales)) / ytm_periodico
            factor_vp_vn = (1 + ytm_periodico) ** (-periodos_totales)
            return cupon_periodico * factor_vp_cupones + VN * factor_vp_vn
        
        # Búsqueda simple del YTM
        ytm_periodico = tasa_cupon / periodicidad  # valor inicial
        for _ in range(100):
            precio_calc = precio_bono(ytm_periodico)
            if abs(precio_calc - precio_mercado) < 0.01:
                break
            # Ajustar YTM
            if precio_calc > precio_mercado:
                ytm_periodico += 0.0001
            else:
                ytm_periodico -= 0.0001
        
        ytm_anual = ytm_periodico * periodicidad
        
        st.success(f"## Yield to Maturity = {ytm_anual:.6%}")

# ============================================================
# 13. VALUACIÓN DE ACCIONES (DIVIDENDOS)
# ============================================================
elif menu == "Valuación de acciones (Dividendos)":
    st.header("Valuación de acciones")
    
    modelo = st.radio("Selecciona el modelo:", 
                      ["Crecimiento cero", "Crecimiento constante (Gordon)", "Crecimiento no constante en etapas"])
    
    if modelo == "Crecimiento cero":
        D0 = st.number_input("D0 = (Dividendo actual)", value=5.0)
        R = st.number_input("R = (Rendimiento requerido)", value=0.18)
        
        # Fórmula exacta del Excel: =C8/C9
        P0 = D0 / R
        
        st.success(f"## P0 = ${P0:,.2f}")
    
    elif modelo == "Crecimiento constante (Gordon)":
        D0 = st.number_input("D0 = (Dividendo actual)", value=1.95)
        R = st.number_input("R = (Rendimiento requerido)", value=0.105)
        g = st.number_input("g = (Tasa de crecimiento)", value=0.04)
        
        if R > g:
            # Fórmula exacta del Excel: =(C21*(1+C23))/(C22-C23)
            P0 = (D0 * (1 + g)) / (R - g)
            st.success(f"## P0 = ${P0:,.2f}")
        else:
            st.error("R debe ser mayor que g")
    
    else:  # Crecimiento no constante
        st.info("Modelo de dividendos con crecimiento variable en los primeros años")
        D0 = st.number_input("D0 = (Dividendo actual)", value=3.15)
        R = st.number_input("R = (Rendimiento requerido)", value=0.1286)
        g_largo = st.number_input("g (crecimiento a largo plazo) =", value=0.05)
        t = st.number_input("t (años de crecimiento variable) =", value=4)
        
        # Crecimientos en cada año (puedes ajustarlos)
        col1, col2 = st.columns(2)
        with col1:
            g1 = st.number_input("Crecimiento año 1", value=1.20, format="%.2f")
            g3 = st.number_input("Crecimiento año 3", value=1.10, format="%.2f")
        with col2:
            g2 = st.number_input("Crecimiento año 2", value=1.15, format="%.2f")
            g4 = st.number_input("Crecimiento año 4", value=1.05, format="%.2f")
        
        dividendos = [D0]
        for i, g_anual in enumerate([g1, g2, g3, g4]):
            dividendos.append(dividendos[-1] * g_anual)
        
        # Calcular VP de dividendos
        vp_dividendos = 0
        for i in range(1, t + 1):
            vp_dividendos += dividendos[i] / ((1 + R) ** i)
        
        # Precio al final del periodo t
        Pt = (dividendos[t] * (1 + g_largo)) / (R - g_largo)
        vp_Pt = Pt / ((1 + R) ** t)
        
        P0 = vp_dividendos + vp_Pt
        
        st.success(f"## P0 = ${P0:,.2f}")

# ============================================================
# 14. VALUACIÓN POR MÚLTIPLOS
# ============================================================
elif menu == "Valuación por múltiplos":
    st.header("Valuación de acciones usando múltiplos")
    
    tipo = st.radio("Selecciona el múltiplo:", ["P/E (Price-Earnings)", "P/S (Price-Sales)"])
    
    if tipo == "P/E (Price-Earnings)":
        pe_benchmark = st.number_input("PE Benchmark =", value=18.0)
        eps = st.number_input("EPS = (Ganancias por acción)", value=2.35)
        
        # Fórmula exacta del Excel: =C7*C8
        P0 = pe_benchmark * eps
        
        st.success(f"## P0 = ${P0:,.2f}")
    
    else:  # P/S
        ps_benchmark = st.number_input("PS Benchmark =", value=4.3)
        sales = st.number_input("Sales = (Ventas totales)", value=2700000.0)
        shares = st.number_input("Number of shares =", value=130000.0)
        
        if shares > 0:
            ps = sales / shares
            # Fórmula exacta del Excel: =C26*C27
            P0 = ps_benchmark * ps
            
            st.success(f"## P0 = ${P0:,.2f}")

# ============================================================
# 15. RENDIMIENTO REQUERIDO
# ============================================================
elif menu == "Rendimiento requerido":
    st.header("Rendimiento requerido (dividendos crecen a tasa constante)")
    
    D0 = st.number_input("D0 = (Dividendo actual)", value=2.1)
    g = st.number_input("g = (Tasa de crecimiento)", value=0.05)
    P0 = st.number_input("P0 = (Precio de la acción)", value=48.0)
    
    # Fórmula exacta del Excel: =((C8*(1+C9))/C10)+C9
    R = ((D0 * (1 + g)) / P0) + g
    
    st.success(f"## R = {R:.6%}")

# ============================================================
# 16. PRECIOS FORWARD
# ============================================================
elif menu == "Precios Forward":
    st.header("Precios Forward / Futuros")
    
    tipo = st.radio("Selecciona el tipo de activo:", 
                    ["Sin ingresos ni costos", "Con ingresos conocidos", "Con yield conocido", "Sobre monedas"])
    
    if tipo == "Sin ingresos ni costos":
        S0 = st.number_input("S0 = (Precio spot)", value=100.0)
        r = st.number_input("r = (Tasa libre de riesgo)", value=0.05)
        T = st.number_input("T = (Plazo en años)", value=1.0)
        
        # Fórmula exacta del Excel: =C8*(1+C9)^C10 (discreto) o =K8*EXP(K9*K10) (continuo)
        F0_discreto = S0 * (1 + r) ** T
        F0_continuo = S0 * np.exp(r * T)
        
        col1, col2 = st.columns(2)
        col1.metric("Forward (capitalización discreta)", f"${F0_discreto:,.2f}")
        col2.metric("Forward (capitalización continua)", f"${F0_continuo:,.2f}")
    
    elif tipo == "Con ingresos conocidos":
        S0 = st.number_input("S0 =", value=50.0)
        r = st.number_input("r =", value=0.08)
        T = st.number_input("T = (años)", value=1.0)
        
        st.info("Ingresos esperados (ejemplo: dividendos):")
        ingreso1 = st.number_input("Ingreso 1", value=2.0)
        tiempo1 = st.number_input("Tiempo ingreso 1 (meses)", value=2.0) / 12
        ingreso2 = st.number_input("Ingreso 2", value=2.0)
        tiempo2 = st.number_input("Tiempo ingreso 2 (meses)", value=5.0) / 12
        
        # Fórmula exacta del Excel: =2*EXP(-2/12*C23)+2*EXP(-5/12*C23)
        I = ingreso1 * np.exp(-r * tiempo1) + ingreso2 * np.exp(-r * tiempo2)
        F0 = (S0 - I) * np.exp(r * T)
        
        st.success(f"## Precio Forward = ${F0:,.2f}")
    
    elif tipo == "Con yield conocido":
        S0 = st.number_input("S0 =", value=100.0)
        r = st.number_input("r = (Tasa libre de riesgo)", value=0.05)
        q = st.number_input("q = (Yield o tasa de dividendo)", value=0.02)
        T = st.number_input("T = (años)", value=1.0)
        
        # Fórmula exacta del Excel: =K35*EXP((K36-K37)*K38)
        F0 = S0 * np.exp((r - q) * T)
        
        st.success(f"## Precio Forward = ${F0:,.2f}")
    
    else:  # Sobre monedas
        S0 = st.number_input("S0 = (Tipo de cambio spot)", value=19.58)
        r = st.number_input("r = (Tasa doméstica)", value=0.0974)
        rf = st.number_input("rf = (Tasa extranjera)", value=0.0403)
        T = st.number_input("T = (años)", value=1.0)
        
        # Fórmula exacta del Excel: =K49*EXP((K50-K51)*K52)
        F0 = S0 * np.exp((r - rf) * T)
        
        st.success(f"## Precio Forward = ${F0:,.4f}")

# ============================================================
# 17. OPCIONES BLACK-SCHOLES
# ============================================================
elif menu == "Opciones (Black-Scholes)":
    st.header("Precios de opciones (Black-Scholes-Merton)")
    
    tipo = st.radio("Selecciona el tipo de activo:", 
                    ["Activos sin ingresos", "Activos con dividendos", "Sobre divisas"])
    
    if tipo == "Activos sin ingresos":
        S = st.number_input("S = (Precio spot)", value=34.97)
        K = st.number_input("K = (Strike price)", value=34.97)
        T = st.number_input("T = (Tiempo en años)", value=1.0)
        r = st.number_input("r = (Tasa libre de riesgo)", value=0.0681)
        sigma = st.number_input("σ = (Volatilidad)", value=0.048)
        
        if sigma > 0 and T > 0:
            d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            
            call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
            put = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
            
            col1, col2 = st.columns(2)
            col1.metric("Call", f"${call:,.4f}")
            col2.metric("Put", f"${put:,.4f}")
            
            st.caption(f"d1 = {d1:.4f}, d2 = {d2:.4f}")
    
    elif tipo == "Activos con dividendos":
        S = st.number_input("S = (Precio spot)", value=20.0)
        K = st.number_input("K = (Strike price)", value=20.0)
        T = st.number_input("T = (tiempo en años)", value=0.25)
        r = st.number_input("r = (Tasa libre de riesgo)", value=0.1133)
        q = st.number_input("q = (Tasa de dividendo)", value=0.05)
        sigma = st.number_input("σ = (Volatilidad)", value=0.30)
        
        if sigma > 0 and T > 0:
            d1 = (np.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            
            call = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
            put = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
            
            col1, col2 = st.columns(2)
            col1.metric("Call", f"${call:,.4f}")
            col2.metric("Put", f"${put:,.4f}")
    
    else:  # Divisas
        S = st.number_input("S0 = (Tipo de cambio spot)", value=19.58)
        K = st.number_input("K = (Strike)", value=22.0)
        T = st.number_input("T = (años)", value=1.0)
        r = st.number_input("r = (Tasa doméstica)", value=0.0974)
        rf = st.number_input("rf = (Tasa extranjera)", value=0.0403)
        sigma = st.number_input("σ = (Volatilidad)", value=0.10155)
        
        if sigma > 0 and T > 0:
            d1 = (np.log(S / K) + (r - rf + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            
            call = S * np.exp(-rf * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
            put = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-rf * T) * norm.cdf(-d1)
            
            col1, col2 = st.columns(2)
            col1.metric("Call", f"${call:,.4f}")
            col2.metric("Put", f"${put:,.4f}")