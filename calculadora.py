import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf
from scipy.stats import norm

st.set_page_config(page_title="Calculadora de Matemáticas Financieras", layout="wide")

st.title("📈 Calculadora de Matemáticas Financieras")
st.markdown("Aplicación basada en las fórmulas del archivo de Excel.")

menu = st.sidebar.selectbox(
    "Selecciona una sección",
    [
        "Conversión de tasas",
        "Valor Futuro",
        "Valor Presente",
        "Tasa de rendimiento anual",
        "Número de periodos",
        "VF Rentas Periódicas",
        "VP Rentas Periódicas",
        "Tablas de amortización",
        "Rentas crecientes",
        "Bonos",
        "Acciones",
        "Forward",
        "Opciones",
        "Opciones Black-Scholes",
        "Determinación Yield",
        "Acciones: rendimiento requerido"
    ]
)

# ==============================
# CONVERSIÓN DE TASAS
# ==============================
if menu == "Conversión de tasas":
    st.header("Conversión de tasas")

    tipo = st.selectbox(
        "Conversión",
        [
            "Nominal a efectiva e instantánea",
            "Instantánea a efectiva",
            "Instantánea a nominal",
            "Nominal a nominal"
        ]
    )

    if tipo == "Nominal a efectiva e instantánea":
        i_nom = st.number_input("Tasa nominal i(m)", value=0.40)
        m = st.number_input("m", value=2.0)

        i_ef = (1 + i_nom / m) ** m - 1
        d = m * np.log(1 + i_nom / m)

        st.success(f"Tasa efectiva: {i_ef:.6f}")
        st.success(f"Tasa instantánea: {d:.6f}")

    else:
        d = st.number_input("Tasa instantánea d", value=0.005)
        i = np.exp(d) - 1

        st.success(f"Tasa efectiva: {i:.6f}")

        st.latex(r"i = e^{\delta}-1")

    # ------------------------------
    # INSTANTÁNEA A NOMINAL
    # ------------------------------
    elif tipo == "Instantánea a nominal":
        d = st.number_input("Tasa instantánea δ", value=0.07)
        m = st.number_input("m", value=2.0)

        i_nom = m * (np.exp(d / m) - 1)

        st.success(f"Tasa nominal i(m): {i_nom:.6%}")

        st.latex(r"i^{(m)} = m\left(e^{\delta/m}-1\right)")

    # ------------------------------
    # NOMINAL A NOMINAL
    # ------------------------------
    else:
        m = st.number_input("Frecuencia m", value=2.0)
        i_m = st.number_input("Tasa nominal i(m)", value=0.10)
        p = st.number_input("Nueva frecuencia p", value=3.0)

        i_p = p * ((1 + i_m / m) ** (m / p) - 1)

        st.success(f"Tasa nominal equivalente i(p): {i_p:.6%}")

        st.latex(r"i^{(p)} = p\left[\left(1+\frac{i^{(m)}}{m}\right)^{m/p}-1\right]")

        frecuencias = np.array([0.25, 0.5, 1, 2, 4, 12, 52, 365])
        tasas = frecuencias * ((1 + i_m / m) ** (m / frecuencias) - 1)

        fig, ax = plt.subplots()
        ax.plot(frecuencias, tasas, marker='o')
        ax.set_title("Convergencia de tasas nominales")
        ax.set_xlabel("Frecuencia")
        ax.set_ylabel("Tasa equivalente")

        st.pyplot(fig)

# ==============================
# VALOR FUTURO
# ==============================
elif menu == "Valor Futuro":
    st.header("Valor Futuro")

    C0 = st.number_input("Capital inicial", value=20000.0)
    i = st.number_input("Tasa efectiva", value=0.068)
    n = st.number_input("Número de periodos", value=6)

    VF = C0 * (1 + i) ** n

    st.success(f"Valor Futuro = {VF:,.2f}")

    periodos = np.arange(0, n + 1)
    valores = C0 * (1 + i) ** periodos

    fig, ax = plt.subplots()
    ax.plot(periodos, valores)
    ax.set_xlabel("Periodo")
    ax.set_ylabel("Valor")
    ax.set_title("Crecimiento del capital")

    st.pyplot(fig)

# ==============================
# VALOR PRESENTE
# ==============================
elif menu == "Valor Presente":
    st.header("Valor Presente")

    VF = st.number_input("Valor futuro", value=245000.0)
    i = st.number_input("Tasa efectiva", value=0.112)
    n = st.number_input("Número de periodos", value=9)

    VP = VF / ((1 + i) ** n)

    st.success(f"Valor Presente = {VP:,.2f}")

    periodos = np.arange(0, n + 1)
    valores = VF / ((1 + i) ** periodos)

    fig, ax = plt.subplots()
    ax.plot(periodos, valores)
    ax.set_title("Descuento del valor")
    ax.set_xlabel("Periodo")
    ax.set_ylabel("Valor")

    st.pyplot(fig)

# ==============================
# TASA DE RENDIMIENTO
# ==============================
elif menu == "Tasa de rendimiento anual":
    st.header("Tasa de rendimiento anual")

    C0 = st.number_input("Valor inicial", value=4582500.0)
    Cn = st.number_input("Valor final", value=9360000.0)
    n = st.number_input("Número de periodos", value=10)

    i = (Cn / C0) ** (1 / n) - 1

    st.success(f"Tasa anual = {i:.6%}")

# ==============================
# NÚMERO DE PERIODOS
# ==============================
elif menu == "Número de periodos":
    st.header("Número de periodos")

    C0 = st.number_input("Valor inicial", value=50000.0)
    Cn = st.number_input("Valor final", value=245000.0)
    i = st.number_input("Tasa efectiva", value=0.043)

    n = np.log(Cn / C0) / np.log(1 + i)

    st.success(f"Número de periodos = {n:.2f}")

# ==============================
# VF RENTAS
# ==============================
elif menu == "VF Rentas Periódicas":
    st.header("Valor Futuro de Rentas")

    renta = st.number_input("Renta", value=1000.0)
    i = st.number_input("Tasa por periodo", value=0.05)
    n = st.number_input("Número de pagos", value=12)

    vf = renta * (((1 + i) ** n - 1) / i)

    st.success(f"Valor Futuro = {vf:,.2f}")

    periodos = np.arange(1, n + 1)
    acumulado = [renta * (((1 + i) ** t - 1) / i) for t in periodos]

    fig, ax = plt.subplots()
    ax.plot(periodos, acumulado)
    ax.set_title("Acumulación de rentas")
    ax.set_xlabel("Periodo")
    ax.set_ylabel("Valor Futuro")

    st.pyplot(fig)

# ==============================
# VP RENTAS
# ==============================
elif menu == "VP Rentas Periódicas":
    st.header("Valor Presente de Rentas")

    renta = st.number_input("Renta", value=6100.0)
    i = st.number_input("Tasa por periodo", value=0.05)
    n = st.number_input("Número de pagos", value=5)

    vp = renta * ((1 - (1 + i) ** (-n)) / i)

    st.success(f"Valor Presente = {vp:,.2f}")

# ==============================
# TABLAS DE AMORTIZACIÓN
# ==============================
elif menu == "Tablas de amortización":
    st.header("Tabla de amortización")

    prestamo = st.number_input("Monto del préstamo", value=500000.0)
    tasa = st.number_input("Tasa anual", value=0.12)
    años = st.number_input("Años", value=5)
    pagos_por_año = st.number_input("Pagos por año", value=12)

    n = int(años * pagos_por_año)
    i = tasa / pagos_por_año

    pago = npf.pmt(i, n, -prestamo)

    saldo = prestamo
    tabla = []

    for k in range(1, n + 1):
        interes = saldo * i
        amortizacion = pago - interes
        saldo -= amortizacion

        tabla.append([
            k,
            round(pago, 2),
            round(interes, 2),
            round(amortizacion, 2),
            round(max(saldo, 0), 2)
        ])

    df = pd.DataFrame(
        tabla,
        columns=["Periodo", "Pago", "Interés", "Amortización", "Saldo"]
    )

    st.success(f"Pago periódico = {pago:,.2f}")
    st.dataframe(df)

    fig, ax = plt.subplots()
    ax.plot(df["Periodo"], df["Saldo"])
    ax.set_title("Saldo insoluto")
    ax.set_xlabel("Periodo")
    ax.set_ylabel("Saldo")

    st.pyplot(fig)

# ==============================
# RENTAS CRECIENTES
# ==============================
elif menu == "Rentas crecientes":
    st.header("Rentas crecientes geométricas")

    tipo = st.selectbox(
        "Tipo",
        ["Valor Futuro", "Valor Presente"]
    )

    R1 = st.number_input("Primer pago", value=400.0)
    i = st.number_input("Tasa de interés", value=0.0369)
    q = st.number_input("Tasa de crecimiento", value=0.005)
    n = st.number_input("Número de periodos", value=10)

    if i != q:
        if tipo == "Valor Futuro":
            vf = R1 * (((1 + i) ** n - (1 + q) ** n) / (i - q))
            st.success(f"Valor Futuro = {vf:,.2f}")
        else:
            vp = (R1 / (i - q)) * (1 - ((1 + q) / (1 + i)) ** n)
            st.success(f"Valor Presente = {vp:,.2f}")
    else:
        st.error("La tasa i no puede ser igual a q")

# ==============================
# DETERMINACIÓN DE YIELD
# ==============================
elif menu == "Determinación Yield":
    st.header("Determinación de Yield")

    precio = st.number_input("Precio del bono", value=950.0)
    VN = st.number_input("Valor nominal", value=1000.0)
    cupon = st.number_input("Cupón anual", value=0.08)
    T = st.number_input("Años al vencimiento", value=5)
    m = st.number_input("Pagos por año", value=2)

    n = int(T * m)
    C = VN * cupon / m

    def precio_bono(y):
        r = y / m
        flujo = sum(C / ((1 + r) ** t) for t in range(1, n + 1))
        flujo += VN / ((1 + r) ** n)
        return flujo

    tasas = np.linspace(0.001, 0.30, 1000)
    precios = [precio_bono(y) for y in tasas]

    idx = np.argmin(np.abs(np.array(precios) - precio))
    ytm = tasas[idx]

    st.success(f"Yield aproximado = {ytm:.6%}")

    fig, ax = plt.subplots()
    ax.plot(tasas, precios)
    ax.axhline(precio)
    ax.set_title("Precio del bono vs Yield")
    ax.set_xlabel("Yield")
    ax.set_ylabel("Precio")

    st.pyplot(fig)

# ==============================
# BONOS
# ==============================
elif menu == "Bonos":
    st.header("Valuación de Bonos")

    VN = st.number_input("Valor nominal", value=1000.0)
    cupon = st.number_input("Tasa cupón", value=0.08)
    ytm = st.number_input("Yield to maturity", value=0.04)
    T = st.number_input("Años al vencimiento", value=10)
    m = st.number_input("Pagos por año", value=1)

    C = VN * cupon / m
    n = int(T * m)
    r = ytm / m

    precio = sum(C / ((1 + r) ** t) for t in range(1, n + 1))
    precio += VN / ((1 + r) ** n)

    st.success(f"Precio del bono = {precio:,.2f}")

# ==============================
# RENDIMIENTO REQUERIDO DE ACCIONES
# ==============================
elif menu == "Acciones: rendimiento requerido":
    st.header("Rendimiento requerido")

    D1 = st.number_input("Dividendo esperado D1", value=5.0)
    P0 = st.number_input("Precio actual", value=45.0)
    g = st.number_input("Crecimiento g", value=0.04)

    R = (D1 / P0) + g

    st.success(f"Rendimiento requerido = {R:.6%}")

    st.latex(r"R = rac{D_1}{P_0} + g")

# ==============================
# ACCIONES
# ==============================
elif menu == "Acciones":
    st.header("Valuación de Acciones")

    metodo = st.selectbox(
        "Método",
        [
            "Modelo Gordon",
            "Múltiplo PE"
        ]
    )

    if metodo == "Modelo Gordon":
        D0 = st.number_input("Dividendo actual", value=5.0)
        R = st.number_input("Rendimiento requerido", value=0.18)
        g = st.number_input("Crecimiento", value=0.05)

        P0 = (D0 * (1 + g)) / (R - g)

        st.success(f"Precio de la acción = {P0:,.2f}")

    else:
        PE = st.number_input("PE Benchmark", value=18.0)
        EPS = st.number_input("EPS", value=2.35)

        precio = PE * EPS

        st.success(f"Precio estimado = {precio:,.2f}")

# ==============================
# OPCIONES
# ==============================
elif menu == "Opciones":
    st.header("Payoff de Opciones")

    tipo = st.selectbox("Tipo", ["Call", "Put"])

    K = st.number_input("Strike", value=100.0)
    prima = st.number_input("Prima", value=10.0)

    ST = np.linspace(0, 2 * K, 200)

    if tipo == "Call":
        payoff = np.maximum(ST - K, 0) - prima
    else:
        payoff = np.maximum(K - ST, 0) - prima

    fig, ax = plt.subplots()
    ax.plot(ST, payoff)
    ax.axhline(0)
    ax.set_title(f"Payoff {tipo}")
    ax.set_xlabel("Precio al vencimiento")
    ax.set_ylabel("Ganancia")

    st.pyplot(fig)

# ==============================
# FORWARD
# ==============================
elif menu == "Forward":
    st.header("Precio Forward")

    S0 = st.number_input("Precio spot", value=100.0)
    r = st.number_input("Tasa libre de riesgo", value=0.08)
    T = st.number_input("Tiempo", value=1.0)

    F0 = S0 * (1 + r) ** T

    st.success(f"Precio forward = {F0:,.2f}")

# ==============================
# OPCIONES BLACK-SCHOLES
# ==============================
elif menu == "Opciones Black-Scholes":
    st.header("Opciones Black-Scholes")

    S = st.number_input("Precio del activo", value=34.97)
    K = st.number_input("Strike", value=34.97)
    r = st.number_input("Tasa libre de riesgo", value=0.0681)
    sigma = st.number_input("Volatilidad", value=0.20)
    T = st.number_input("Tiempo a vencimiento", value=1.0)

    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    st.success(f"Precio Call = {call:.4f}")
    st.success(f"Precio Put = {put:.4f}")

    precios = np.linspace(0.5 * K, 1.5 * K, 100)
    calls = []

    for s in precios:
        d1_tmp = (np.log(s / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
        d2_tmp = d1_tmp - sigma * np.sqrt(T)
        c_tmp = s * norm.cdf(d1_tmp) - K * np.exp(-r * T) * norm.cdf(d2_tmp)
        calls.append(c_tmp)

    fig, ax = plt.subplots()
    ax.plot(precios, calls)
    ax.set_title("Precio Call vs Precio Spot")
    ax.set_xlabel("Precio Spot")
    ax.set_ylabel("Precio Call")

    st.pyplot(fig)
