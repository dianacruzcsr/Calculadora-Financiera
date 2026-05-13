import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy_financial as npf
from scipy.stats import norm

st.set_page_config(page_title="Calculadora de Matemáticas Financieras", layout="wide")

plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor": "#161b22",
    "axes.edgecolor": "#2a3444",
    "axes.labelcolor": "#94a3b8",
    "xtick.color": "#64748b",
    "ytick.color": "#64748b",
    "text.color": "#e2e8f0",
    "grid.color": "#2a3444",
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
    "lines.linewidth": 2,
})

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
        "Acciones: rendimiento requerido",
    ],
)

# ══════════════════════════════════════════════════════════════════════════════
# CONVERSIÓN DE TASAS
# ══════════════════════════════════════════════════════════════════════════════
if menu == "Conversión de tasas":
    st.header("Conversión de tasas")

    tipo = st.selectbox(
        "Conversión",
        [
            "Nominal a efectiva e instantánea",
            "Instantánea a efectiva",
            "Instantánea a nominal",
            "Nominal a nominal",
            "Reinversión de intereses",
        ],
    )

    # ── Nominal → Efectiva e instantánea ─────────────────────────────────────
    if tipo == "Nominal a efectiva e instantánea":
        col1, col2 = st.columns(2)
        with col1:
            i_nom = st.number_input("Tasa nominal i(m)", value=0.40, step=0.01, format="%.4f")
            m = st.number_input("m (frecuencia de capitalización)", value=2.0, min_value=0.01, step=0.25, format="%.2f")

        i_ef = (1 + i_nom / m) ** m - 1
        delta = m * np.log(1 + i_nom / m)

        st.success(f"Tasa efectiva: {i_ef:.6%}")
        st.success(f"Tasa instantánea δ: {delta:.6%}")

        st.latex(r"i = \left(1+\frac{i^{(m)}}{m}\right)^m -1")
        st.latex(r"\delta = m\ln\left(1+\frac{i^{(m)}}{m}\right)")

    # ── Instantánea → Efectiva ────────────────────────────────────────────────
    elif tipo == "Instantánea a efectiva":
        delta = st.number_input("Tasa instantánea δ", value=0.005, step=0.001, format="%.4f")

        i = np.exp(delta) - 1

        st.success(f"Tasa efectiva: {i:.6%}")
        st.latex(r"i = e^{\delta}-1")

    # ── Instantánea → Nominal ─────────────────────────────────────────────────
    elif tipo == "Instantánea a nominal":
        col1, col2 = st.columns(2)
        with col1:
            delta = st.number_input("Tasa instantánea δ", value=0.07, step=0.001, format="%.4f")
            m = st.number_input("m (frecuencia)", value=2.0, min_value=0.01, step=0.25, format="%.2f")

        i_nom = m * (np.exp(delta / m) - 1)

        st.success(f"Tasa nominal i(m): {i_nom:.6%}")
        st.latex(r"i^{(m)} = m\left(e^{\delta/m}-1\right)")

    # ── Nominal → Nominal ─────────────────────────────────────────────────────
    elif tipo == "Nominal a nominal":
        col1, col2 = st.columns(2)
        with col1:
            m = st.number_input(
                "Frecuencia m (capitalización original)",
                value=2.0, min_value=0.01, step=0.25, format="%.2f",
                help="Número de veces que se capitaliza al año con i(m)",
            )
            i_m = st.number_input(
                "Tasa nominal i(m)",
                value=0.10, step=0.01, format="%.4f",
                help="Tasa nominal anual capitalizable m veces por año",
            )
            p = st.number_input(
                "Nueva frecuencia p (capitalización deseada)",
                value=3.0, min_value=0.01, step=0.25, format="%.2f",
                help="Número de veces que se quiere capitalizar al año",
            )

        # Tasa periódica (lo que muestra el Excel en la celda amarilla)
        tasa_periodica = (1 + i_m / m) ** (m / p) - 1
        # Tasa nominal anual equivalente (tasa periódica × p)
        i_p = p * tasa_periodica

        st.success(f"Tasa periódica por subperíodo: {tasa_periodica:.6%}  ← valor que muestra el Excel")
        st.success(f"Tasa nominal anual equivalente i(p): {i_p:.6%}")
        st.latex(r"\text{Tasa periódica} = \left(1+\frac{i^{(m)}}{m}\right)^{m/p}-1")
        st.latex(r"i^{(p)} = p\left[\left(1+\frac{i^{(m)}}{m}\right)^{m/p}-1\right]")

        # Tabla de equivalencias para frecuencias estándar
        st.subheader("Tabla de tasas nominales equivalentes")
        freq_labels = ["Cada 4 años", "Cada 2 años", "Anual", "Semestral",
                       "Trimestral", "Mensual", "Semanal", "Diaria"]
        freq_m = [0.25, 0.5, 1, 2, 4, 12, 52, 365]
        tasas_equiv = [f * ((1 + i_m / m) ** (m / f) - 1) for f in freq_m]

        df_equiv = pd.DataFrame({
            "Período": freq_labels,
            "p (veces/año)": freq_m,
            "i(p) equivalente": [f"{t:.6%}" for t in tasas_equiv],
        })
        st.dataframe(df_equiv, use_container_width=True, hide_index=True)

        # Gráfica de convergencia
        st.subheader("Convergencia de tasas nominales equivalentes")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(freq_m, [t * 100 for t in tasas_equiv], marker="o", color="#22d3ee")
        for xv, yv, lbl in zip(freq_m, [t * 100 for t in tasas_equiv], freq_m):
            ax.annotate(f"{xv}", (xv, yv), textcoords="offset points",
                        xytext=(4, 6), fontsize=8, color="#94a3b8")
        ax.set_xlabel("Frecuencia p (veces al año)")
        ax.set_ylabel("i(p) (%)")
        ax.set_title("Tasas nominales equivalentes para distintas frecuencias")
        ax.grid(True)
        st.pyplot(fig)
        plt.close(fig)

    # ── Reinversión de intereses ───────────────────────────────────────────────
    elif tipo == "Reinversión de intereses":
        st.subheader("Ilustración de la reinversión de los intereses")
        st.markdown(
            "Muestra cómo aumenta el saldo acumulado al reinvertir los intereses "
            "con mayor frecuencia, llegando al límite de la capitalización continua."
        )

        col1, col2 = st.columns(2)
        with col1:
            i_nom = st.number_input(
                "Tasa nominal anual i", value=0.10, step=0.01, format="%.4f",
                help="Tasa nominal anual que se capitaliza m veces al año.",
            )
            C0 = st.number_input(
                "Capital inicial C₀", value=100_000.0, step=1_000.0, format="%.2f",
            )
            n = st.number_input(
                "Años n", value=1, min_value=1, step=1,
                help="Horizonte de capitalización. El Excel ilustra n=1 (al cabo de 1 año).",
            )

        st.info(
            "La tabla muestra cómo crece C₀ al cabo de **n años** "
            "capitalizando m veces por año con la misma tasa nominal i. "
            "El Excel usa n=1 para comparar frecuencias en igualdad de condiciones."
        )

        # Períodos estándar (igual que el Excel)
        periodos = [
            ("Cada 4 años",   0.25),
            ("Cada 2 años",   0.50),
            ("Anual",          1),
            ("Semestral",      2),
            ("Trimestral",     4),
            ("Mensual",       12),
            ("Semanal",       52),
            ("Diaria",       365),
            ("Cada hora",   8_760),
            ("Cada minuto", 525_600),
            ("Cada segundo", 31_536_000),
        ]

        def saldo(m_val):
            return C0 * (1 + i_nom / m_val) ** (m_val * n)

        filas = [(lbl, m_val, saldo(m_val)) for lbl, m_val in periodos]
        saldo_inst = C0 * np.exp(i_nom * n)
        filas.append(("Instantánea", np.inf, saldo_inst))

        df = pd.DataFrame(filas, columns=["Período de reinversión", "m = Veces al año", "Monto acumulado"])
        df["m = Veces al año"] = df["m = Veces al año"].apply(
            lambda x: "∞" if np.isinf(x) else f"{x:,.2f}"
        )
        df["Monto acumulado"] = df["Monto acumulado"].apply(lambda x: f"{x:,.0f}")

        st.dataframe(df, use_container_width=True, hide_index=True)

        # Gráfica — igual estructura que el Excel
        m_vals = np.array([0.25, 0.5, 1, 2, 4, 12, 52, 365, 8_760, 525_600])
        saldos = C0 * (1 + i_nom / m_vals) ** (m_vals * n)

        puntos_etiqueta = [(0.25, C0*(1+i_nom/0.25)**(0.25*n)),
                           (0.5,  C0*(1+i_nom/0.5)**(0.5*n)),
                           (1,    C0*(1+i_nom)**n),
                           (2,    C0*(1+i_nom/2)**(2*n)),
                           (12,   C0*(1+i_nom/12)**(12*n))]

        fig2, ax2 = plt.subplots(figsize=(9, 4.5))
        ax2.plot(m_vals, saldos, color="#10b981", marker="o", markersize=5)

        for xv, yv in puntos_etiqueta:
            ax2.annotate(
                f"{xv:g}, {yv:,.0f}",
                (xv, yv), textcoords="offset points",
                xytext=(6, 6), fontsize=8, color="#94a3b8",
            )

        # Línea punteada del límite continuo
        ax2.axhline(saldo_inst, linestyle="--", color="#f59e0b", linewidth=1.2,
                    label=f"Instantánea = {saldo_inst:,.0f}")
        ax2.legend(fontsize=9)

        ax2.set_xlabel("Reinversión de los intereses (m — veces al año)")
        ax2.set_ylabel("Saldo acumulado")
        ax2.set_title("Convergencia del Saldo Acumulado")
        ax2.grid(True)
        st.pyplot(fig2)
        plt.close(fig2)

        st.latex(r"C_n = C_0\left(1+\frac{i}{m}\right)^{mn}")
        st.latex(r"C_\infty = C_0\,e^{i\,n} \quad \text{(capitalización continua)}")

# ══════════════════════════════════════════════════════════════════════════════
# VALOR FUTURO
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Valor Futuro":
    st.header("Valor Futuro")

    tipo_vf = st.selectbox(
        "Tipo de capitalización",
        [
            "Tasa efectiva anual  —  Cₙ = C₀(1+i)ⁿ",
            "Tasa efectiva por subperíodo  —  Cₙ = C₀(1+iₘ)ⁿᵐ",
            "Tasa instantánea  —  Cₙ = C₀·eᵟⁿ",
        ],
    )

    # ── 1. Tasa efectiva anual ────────────────────────────────────────────────
    if tipo_vf.startswith("Tasa efectiva anual"):
        col1, _ = st.columns(2)
        with col1:
            C0 = st.number_input("Capital inicial C₀", value=20_000.0, format="%.2f")
            i  = st.number_input("Tasa efectiva anual i", value=0.068, step=0.001, format="%.4f")
            n  = st.number_input("Número de períodos n", value=6, min_value=1, step=1)

        VF = C0 * (1 + i) ** n
        st.success(f"Cₙ = {VF:,.2f}")
        st.latex(r"C_n = C_0 \times (1+i)^n")

        periodos = np.arange(0, n + 1)
        valores  = C0 * (1 + i) ** periodos
        fig, ax  = plt.subplots()
        ax.plot(periodos, valores, color="#22d3ee")
        ax.set_xlabel("Período"); ax.set_ylabel("Valor"); ax.set_title("Crecimiento del capital")
        ax.grid(True)
        st.pyplot(fig); plt.close(fig)

    # ── 2. Tasa efectiva por subperíodo (iₘ) ─────────────────────────────────
    elif tipo_vf.startswith("Tasa efectiva por subperíodo"):
        col1, _ = st.columns(2)
        with col1:
            C0  = st.number_input("Capital inicial C₀", value=54_000.0, format="%.2f")
            i_m = st.number_input("Tasa nominal i(m)", value=0.1125, step=0.001, format="%.4f",
                                  help="Tasa nominal anual capitalizable m veces")
            n   = st.number_input("Número de años n", value=8, min_value=1, step=1)
            m   = st.number_input("Frecuencia m (subperíodos/año)", value=13.0, min_value=0.01,
                                  step=0.25, format="%.2f")

        im   = i_m / m          # tasa efectiva por subperíodo
        nm   = n * m             # total de subperíodos
        VF   = C0 * (1 + im) ** nm

        st.success(f"Tasa efectiva por subperíodo iₘ = {im:.6%}")
        st.success(f"Total subperíodos nm = {nm:,.2f}")
        st.success(f"Cₙₘ = {VF:,.2f}")
        st.latex(r"i_m = \frac{i^{(m)}}{m}")
        st.latex(r"C_{nm} = C_0 \times (1+i_m)^{nm}")

        pasos  = np.linspace(0, nm, 300)
        valores = C0 * (1 + im) ** pasos
        fig, ax = plt.subplots()
        ax.plot(pasos, valores, color="#22d3ee")
        ax.set_xlabel("Subperíodos"); ax.set_ylabel("Valor")
        ax.set_title("Crecimiento del capital (subperíodos)")
        ax.grid(True)
        st.pyplot(fig); plt.close(fig)

    # ── 3. Tasa instantánea ───────────────────────────────────────────────────
    elif tipo_vf.startswith("Tasa instantánea"):
        col1, _ = st.columns(2)
        with col1:
            C0    = st.number_input("Capital inicial C₀", value=5_000.0, format="%.2f")
            delta = st.number_input("Tasa instantánea δ", value=0.10, step=0.001, format="%.4f")
            n     = st.number_input("Número de períodos n", value=9, min_value=1, step=1)

        VF = C0 * np.exp(delta * n)
        st.success(f"Cₙ = {VF:,.2f}")
        st.latex(r"C_n = C_0 \times e^{\delta n}")

        periodos = np.linspace(0, n, 300)
        valores  = C0 * np.exp(delta * periodos)
        fig, ax  = plt.subplots()
        ax.plot(periodos, valores, color="#10b981")
        ax.set_xlabel("Período"); ax.set_ylabel("Valor")
        ax.set_title("Crecimiento con capitalización continua")
        ax.grid(True)
        st.pyplot(fig); plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# VALOR PRESENTE
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Valor Presente":
    st.header("Valor Presente")

    VF = st.number_input("Valor futuro", value=245000.0)
    i = st.number_input("Tasa efectiva", value=0.112, format="%.4f")
    n = st.number_input("Número de periodos", value=9, min_value=1)

    VP = VF / ((1 + i) ** n)
    st.success(f"Valor Presente = {VP:,.2f}")

    periodos = np.arange(0, n + 1)
    valores = VF / ((1 + i) ** periodos)

    fig, ax = plt.subplots()
    ax.plot(periodos, valores, color="#22d3ee")
    ax.set_title("Descuento del valor"); ax.set_xlabel("Periodo"); ax.set_ylabel("Valor")
    ax.grid(True)
    st.pyplot(fig); plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# TASA DE RENDIMIENTO
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Tasa de rendimiento anual":
    st.header("Tasa de rendimiento anual")

    C0 = st.number_input("Valor inicial", value=4582500.0)
    Cn = st.number_input("Valor final", value=9360000.0)
    n = st.number_input("Número de periodos", value=10, min_value=1)

    i = (Cn / C0) ** (1 / n) - 1
    st.success(f"Tasa anual = {i:.6%}")

# ══════════════════════════════════════════════════════════════════════════════
# NÚMERO DE PERIODOS
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Número de periodos":
    st.header("Número de periodos")

    C0 = st.number_input("Valor inicial", value=50000.0)
    Cn = st.number_input("Valor final", value=245000.0)
    i = st.number_input("Tasa efectiva", value=0.043, format="%.4f")

    n = np.log(Cn / C0) / np.log(1 + i)
    st.success(f"Número de periodos = {n:.2f}")

# ══════════════════════════════════════════════════════════════════════════════
# VF RENTAS
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "VF Rentas Periódicas":
    st.header("Valor Futuro de Rentas")

    renta = st.number_input("Renta", value=1000.0)
    i = st.number_input("Tasa por periodo", value=0.05, format="%.4f")
    n = st.number_input("Número de pagos", value=12, min_value=1)

    vf = renta * (((1 + i) ** n - 1) / i)
    st.success(f"Valor Futuro = {vf:,.2f}")

    periodos = np.arange(1, n + 1)
    acumulado = [renta * (((1 + i) ** t - 1) / i) for t in periodos]

    fig, ax = plt.subplots()
    ax.plot(periodos, acumulado, color="#22d3ee")
    ax.set_title("Acumulación de rentas"); ax.set_xlabel("Periodo"); ax.set_ylabel("Valor Futuro")
    ax.grid(True)
    st.pyplot(fig); plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# VP RENTAS
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "VP Rentas Periódicas":
    st.header("Valor Presente de Rentas")

    renta = st.number_input("Renta", value=6100.0)
    i = st.number_input("Tasa por periodo", value=0.05, format="%.4f")
    n = st.number_input("Número de pagos", value=5, min_value=1)

    vp = renta * ((1 - (1 + i) ** (-n)) / i)
    st.success(f"Valor Presente = {vp:,.2f}")

# ══════════════════════════════════════════════════════════════════════════════
# TABLAS DE AMORTIZACIÓN
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Tablas de amortización":
    st.header("Tabla de amortización")

    prestamo = st.number_input("Monto del préstamo", value=500000.0)
    tasa = st.number_input("Tasa anual", value=0.12, format="%.4f")
    años = st.number_input("Años", value=5, min_value=1)
    pagos_por_año = st.number_input("Pagos por año", value=12, min_value=1)

    n = int(años * pagos_por_año)
    i = tasa / pagos_por_año
    pago = npf.pmt(i, n, -prestamo)

    saldo = prestamo
    tabla = []
    for k in range(1, n + 1):
        interes = saldo * i
        amortizacion = pago - interes
        saldo -= amortizacion
        tabla.append([k, round(pago, 2), round(interes, 2),
                      round(amortizacion, 2), round(max(saldo, 0), 2)])

    df = pd.DataFrame(tabla, columns=["Periodo", "Pago", "Interés", "Amortización", "Saldo"])
    st.success(f"Pago periódico = {pago:,.2f}")
    st.dataframe(df, use_container_width=True, hide_index=True)

    fig, ax = plt.subplots()
    ax.plot(df["Periodo"], df["Saldo"], color="#22d3ee")
    ax.set_title("Saldo insoluto"); ax.set_xlabel("Periodo"); ax.set_ylabel("Saldo")
    ax.grid(True)
    st.pyplot(fig); plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# RENTAS CRECIENTES
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Rentas crecientes":
    st.header("Rentas crecientes geométricas")

    tipo = st.selectbox("Tipo", ["Valor Futuro", "Valor Presente"])
    R1 = st.number_input("Primer pago", value=400.0)
    i = st.number_input("Tasa de interés", value=0.0369, format="%.4f")
    q = st.number_input("Tasa de crecimiento", value=0.005, format="%.4f")
    n = st.number_input("Número de periodos", value=10, min_value=1)

    if i != q:
        if tipo == "Valor Futuro":
            vf = R1 * (((1 + i) ** n - (1 + q) ** n) / (i - q))
            st.success(f"Valor Futuro = {vf:,.2f}")
        else:
            vp = (R1 / (i - q)) * (1 - ((1 + q) / (1 + i)) ** n)
            st.success(f"Valor Presente = {vp:,.2f}")
    else:
        st.error("La tasa i no puede ser igual a q")

# ══════════════════════════════════════════════════════════════════════════════
# DETERMINACIÓN DE YIELD
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Determinación Yield":
    st.header("Determinación de Yield")

    precio = st.number_input("Precio del bono", value=950.0)
    VN = st.number_input("Valor nominal", value=1000.0)
    cupon = st.number_input("Cupón anual", value=0.08, format="%.4f")
    T = st.number_input("Años al vencimiento", value=5, min_value=1)
    m = st.number_input("Pagos por año", value=2, min_value=1)

    n = int(T * m)
    C = VN * cupon / m

    def precio_bono(y):
        r = y / m
        return sum(C / (1 + r) ** t for t in range(1, n + 1)) + VN / (1 + r) ** n

    tasas = np.linspace(0.001, 0.30, 1000)
    precios = [precio_bono(y) for y in tasas]
    ytm = tasas[np.argmin(np.abs(np.array(precios) - precio))]

    st.success(f"Yield aproximado = {ytm:.6%}")

    fig, ax = plt.subplots()
    ax.plot(tasas, precios, color="#22d3ee")
    ax.axhline(precio, color="#f59e0b", linestyle="--", label=f"Precio = {precio}")
    ax.legend(); ax.set_title("Precio del bono vs Yield")
    ax.set_xlabel("Yield"); ax.set_ylabel("Precio"); ax.grid(True)
    st.pyplot(fig); plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# BONOS
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Bonos":
    st.header("Valuación de Bonos")

    VN = st.number_input("Valor nominal", value=1000.0)
    cupon = st.number_input("Tasa cupón", value=0.08, format="%.4f")
    ytm = st.number_input("Yield to maturity", value=0.04, format="%.4f")
    T = st.number_input("Años al vencimiento", value=10, min_value=1)
    m = st.number_input("Pagos por año", value=1, min_value=1)

    C = VN * cupon / m
    n = int(T * m)
    r = ytm / m
    precio = sum(C / (1 + r) ** t for t in range(1, n + 1)) + VN / (1 + r) ** n

    st.success(f"Precio del bono = {precio:,.2f}")

# ══════════════════════════════════════════════════════════════════════════════
# RENDIMIENTO REQUERIDO DE ACCIONES
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Acciones: rendimiento requerido":
    st.header("Rendimiento requerido")

    D1 = st.number_input("Dividendo esperado D1", value=5.0)
    P0 = st.number_input("Precio actual", value=45.0)
    g = st.number_input("Crecimiento g", value=0.04, format="%.4f")

    R = (D1 / P0) + g
    st.success(f"Rendimiento requerido = {R:.6%}")
    st.latex(r"R = \frac{D_1}{P_0} + g")

# ══════════════════════════════════════════════════════════════════════════════
# ACCIONES
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Acciones":
    st.header("Valuación de Acciones")

    metodo = st.selectbox("Método", ["Modelo Gordon", "Múltiplo PE"])

    if metodo == "Modelo Gordon":
        D0 = st.number_input("Dividendo actual", value=5.0)
        R = st.number_input("Rendimiento requerido", value=0.18, format="%.4f")
        g = st.number_input("Crecimiento", value=0.05, format="%.4f")
        P0 = (D0 * (1 + g)) / (R - g)
        st.success(f"Precio de la acción = {P0:,.2f}")
    else:
        PE = st.number_input("PE Benchmark", value=18.0)
        EPS = st.number_input("EPS", value=2.35)
        st.success(f"Precio estimado = {PE * EPS:,.2f}")

# ══════════════════════════════════════════════════════════════════════════════
# OPCIONES
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Opciones":
    st.header("Payoff de Opciones")

    tipo = st.selectbox("Tipo", ["Call", "Put"])
    K = st.number_input("Strike", value=100.0)
    prima = st.number_input("Prima", value=10.0)

    ST = np.linspace(0, 2 * K, 200)
    payoff = np.maximum(ST - K, 0) - prima if tipo == "Call" else np.maximum(K - ST, 0) - prima

    fig, ax = plt.subplots()
    ax.plot(ST, payoff, color="#22d3ee")
    ax.axhline(0, color="#64748b", linewidth=0.8)
    ax.set_title(f"Payoff {tipo}"); ax.set_xlabel("Precio al vencimiento")
    ax.set_ylabel("Ganancia"); ax.grid(True)
    st.pyplot(fig); plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# FORWARD
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Forward":
    st.header("Precio Forward")

    S0 = st.number_input("Precio spot", value=100.0)
    r = st.number_input("Tasa libre de riesgo", value=0.08, format="%.4f")
    T = st.number_input("Tiempo", value=1.0, format="%.2f")

    F0 = S0 * (1 + r) ** T
    st.success(f"Precio forward = {F0:,.2f}")

# ══════════════════════════════════════════════════════════════════════════════
# OPCIONES BLACK-SCHOLES
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "Opciones Black-Scholes":
    st.header("Opciones Black-Scholes")

    S = st.number_input("Precio del activo", value=34.97)
    K = st.number_input("Strike", value=34.97)
    r = st.number_input("Tasa libre de riesgo", value=0.0681, format="%.4f")
    sigma = st.number_input("Volatilidad", value=0.20, format="%.4f")
    T = st.number_input("Tiempo a vencimiento", value=1.0, format="%.2f")

    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    st.success(f"Precio Call = {call:.4f}")
    st.success(f"Precio Put = {put:.4f}")

    precios = np.linspace(0.5 * K, 1.5 * K, 100)
    calls = []
    for s in precios:
        d1t = (np.log(s / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
        d2t = d1t - sigma * np.sqrt(T)
        calls.append(s * norm.cdf(d1t) - K * np.exp(-r * T) * norm.cdf(d2t))

    fig, ax = plt.subplots()
    ax.plot(precios, calls, color="#22d3ee")
    ax.set_title("Precio Call vs Precio Spot")
    ax.set_xlabel("Precio Spot"); ax.set_ylabel("Precio Call"); ax.grid(True)
    st.pyplot(fig); plt.close(fig)
