
### Resultados específicos del ejemplo (i=10%, C0=100,000, n=10):
| Frecuencia | Fórmula | Resultado |
|-----------|---------|-----------|
| Cada 4 años (m=0.25) | 100,000 × (1 + 0.10×0.25)^(10/0.25) = 100,000 × (1.025)^40 | **$108,775.73** |
| Cada 2 años (m=0.5) | 100,000 × (1 + 0.10×0.5)^(10/0.5) = 100,000 × (1.05)^20 | **$109,544.51** |
| Anual (m=1) | 100,000 × (1.10)^10 | **$110,000.00** |
| Semestral (m=2) | 100,000 × (1.05)^20 | **$110,250.00** |
| Instantánea (m=∞) | 100,000 × e^(0.10×10) | **$110,517.09** |
""")

# ============================================================
# 1. CONVERSIÓN DE TASAS (FÓRMULAS EXACTAS DEL EXCEL)
# ============================================================
elif menu == "Conversión de tasas":
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
    i_efectiva = ((1 + i_nominal/m) ** m) - 1
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
    i_efectiva_periodo = ((1 + i_nominal3/m3) ** (m3/p)) - 1
    i_p = i_efectiva_periodo * p
    st.info(f"**i(p) =** {i_p:.6%}")
    st.caption(f"Fórmula i(p) = ((1 + {i_nominal3}/{m3})^({m3}/{p}) - 1) × {p}")

# ============================================================
# 2. VALOR FUTURO
# ============================================================
elif menu == "Valor Futuro":
st.header("Valor futuro de una inversión")

tipo = st.radio("Selecciona el tipo de tasa:", 
            ["Tasa efectiva anual i", "Tasa nominal i(m)", "Tasa instantánea δ"])

if tipo == "Tasa efectiva anual i":
C0 = st.number_input("C0 =", value=20000.0)
i = st.number_input("i =", value=0.068)
n = st.number_input("n =", value=6)

Cn = C0 * ((1 + i) ** n)

st.success(f"## Cn = ${Cn:,.2f}")
st.caption(f"Fórmula: Cn = C0 × (1 + i)^{n}")

elif tipo == "Tasa nominal i(m)":
C0 = st.number_input("C0 =", value=54000.0)
i_nom = st.number_input("i(m) =", value=0.1125)
n = st.number_input("n = (años)", value=8)
m = st.number_input("m = (frecuencia)", value=13)

if m > 0:
    i_efectiva_periodo = i_nom / m
    periodos_totales = n * m
    Cn = C0 * ((1 + i_efectiva_periodo) ** periodos_totales)
    
    st.success(f"## Cn = ${Cn:,.2f}")
    st.caption(f"Fórmula: Cn = C0 × (1 + i(m)/m)^(n×m)")

else:
C0 = st.number_input("C0 =", value=5000.0)
d = st.number_input("δ =", value=0.10)
n = st.number_input("n =", value=9)

Cn = C0 * np.exp(d * n)

st.success(f"## Cn = ${Cn:,.2f}")
st.caption(f"Fórmula: Cn = C0 × e^(δ×n)")

# ============================================================
# 3. VALOR PRESENTE
# ============================================================
elif menu == "Valor Presente":
st.header("Valor presente de una cantidad futura")

tipo = st.radio("Selecciona el tipo de tasa:", 
            ["Tasa efectiva anual i", "Tasa nominal i(m)", "Tasa instantánea δ"])

if tipo == "Tasa efectiva anual i":
Cn = st.number_input("Cn =", value=245000.0)
i = st.number_input("i =", value=0.112)
n = st.number_input("n =", value=9)

C0 = Cn * ((1 + i) ** (-n))

st.success(f"## C0 = ${C0:,.2f}")
st.caption(f"Fórmula: C0 = Cn × (1 + i)^(-n)")

elif tipo == "Tasa nominal i(m)":
Cn = st.number_input("Cn =", value=1000.0)
i_nom = st.number_input("i(m) =", value=0.10)
n = st.number_input("n = (años)", value=10)
m = st.number_input("m = (frecuencia)", value=2)

if m > 0:
    i_efectiva_periodo = i_nom / m
    periodos_totales = n * m
    C0 = Cn * ((1 + i_efectiva_periodo) ** (-periodos_totales))
    
    st.success(f"## C0 = ${C0:,.2f}")
    st.caption(f"Fórmula: C0 = Cn × (1 + i(m)/m)^(-n×m)")

else:
Cn = st.number_input("Cn =", value=1000.0)
d = st.number_input("δ =", value=0.10)
n = st.number_input("n =", value=10)

C0 = Cn * np.exp(-d * n)

st.success(f"## C0 = ${C0:,.2f}")
st.caption(f"Fórmula: C0 = Cn × e^(-δ×n)")

# ============================================================
# 4. TASA DE RENDIMIENTO ANUAL
# ============================================================
elif menu == "Tasa de rendimiento anual":
st.header("Tasa de rendimiento efectivo anual o tasa de crecimiento geométrico")

C0 = st.number_input("C0 = (Valor inicial)", value=4582500.0)
Cn = st.number_input("Cn = (Valor final)", value=9360000.0)
n = st.number_input("n = (Número de periodos)", value=10)

if n > 0:
i = ((Cn / C0) ** (1 / n)) - 1

st.success(f"## i = {i:.6%}")
st.caption(f"Fórmula: i = (Cn/C0)^(1/n) - 1")

# ============================================================
# 5. NÚMERO DE PERIODOS
# ============================================================
elif menu == "Número de periodos":
st.header("Determinación del número de periodos")

C0 = st.number_input("C0 =", value=50000.0)
Cn = st.number_input("Cn =", value=245000.0)
i = st.number_input("i =", value=0.043)

if Cn > C0 and i > 0:
n = np.log(Cn / C0) / np.log(1 + i)

st.success(f"## n = {n:.6f} años")

años = int(n)
meses = int((n - años) * 12)
dias = int(((n - años) * 12 - meses) * 30.42)

st.info(f"**Equivalente:** {años} años, {meses} meses, {dias} días")
st.caption(f"Fórmula: n = LN(Cn/C0) / LN(1+i)")

# ============================================================
# 6. VF RENTAS CONSTANTES
# ============================================================
elif menu == "VF Rentas periódicas constantes":
st.header("Valor futuro de rentas vencidas constantes")

renta = st.number_input("Renta =", value=1000.0)
i_nom = st.number_input("i(m) =", value=0.07)
n = st.number_input("n = (años)", value=1)
m = st.number_input("m = (frecuencia)", value=2)

if m > 0:
i_efectiva_periodo = i_nom / m
periodos_totales = n * m
factor_vf = (((1 + i_efectiva_periodo) ** periodos_totales) - 1) / i_efectiva_periodo
vf = renta * factor_vf

st.success(f"## Valor Futuro = ${vf:,.2f}")
st.caption(f"Fórmula: VF = R × [((1 + i(m)/m)^(n×m) - 1) / (i(m)/m)]")

# ============================================================
# 7. VP RENTAS CONSTANTES
# ============================================================
elif menu == "VP Rentas periódicas constantes":
st.header("Valor presente de rentas vencidas constantes")

renta = st.number_input("Renta =", value=6100.0)
i_nom = st.number_input("i(m) =", value=0.05)
n = st.number_input("n = (años)", value=5)
m = st.number_input("m = (frecuencia)", value=1)

if m > 0:
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
n = st.number_input("n = (años)", value=5)
m = st.number_input("m = (pagos por año)", value=12)

if m > 0:
financiamiento = VP * (1 - enganche_pct)
i_periodo = i_nom / m
periodos_totales = n * m

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
n = st.number_input("n = (años)", value=6.25)
m = st.number_input("m = (frecuencia)", value=4)
q = st.number_input("q = (tasa crecimiento)", value=0.02)

if m > 0:
i_periodo = i_nom / m
q_periodo = q / m
periodos_totales = n * m

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

def precio_bono(ytm_periodico):
    factor_vp_cupones = (1 - (1 + ytm_periodico) ** (-periodos_totales)) / ytm_periodico
    factor_vp_vn = (1 + ytm_periodico) ** (-periodos_totales)
    return cupon_periodico * factor_vp_cupones + VN * factor_vp_vn

ytm_periodico = tasa_cupon / periodicidad
for _ in range(100):
    precio_calc = precio_bono(ytm_periodico)
    if abs(precio_calc - precio_mercado) < 0.01:
        break
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

P0 = D0 / R

st.success(f"## P0 = ${P0:,.2f}")

elif modelo == "Crecimiento constante (Gordon)":
D0 = st.number_input("D0 = (Dividendo actual)", value=1.95)
R = st.number_input("R = (Rendimiento requerido)", value=0.105)
g = st.number_input("g = (Tasa de crecimiento)", value=0.04)

if R > g:
    P0 = (D0 * (1 + g)) / (R - g)
    st.success(f"## P0 = ${P0:,.2f}")
else:
    st.error("R debe ser mayor que g")

else:
st.info("Modelo de dividendos con crecimiento variable en los primeros años")
D0 = st.number_input("D0 = (Dividendo actual)", value=3.15)
R = st.number_input("R = (Rendimiento requerido)", value=0.1286)
g_largo = st.number_input("g (crecimiento a largo plazo) =", value=0.05)
t = st.number_input("t (años de crecimiento variable) =", value=4)

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

vp_dividendos = 0
for i in range(1, t + 1):
    vp_dividendos += dividendos[i] / ((1 + R) ** i)

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

P0 = pe_benchmark * eps

st.success(f"## P0 = ${P0:,.2f}")

else:
ps_benchmark = st.number_input("PS Benchmark =", value=4.3)
sales = st.number_input("Sales = (Ventas totales)", value=2700000.0)
shares = st.number_input("Number of shares =", value=130000.0)

if shares > 0:
    ps = sales / shares
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

F0_continuo = S0 * np.exp(r * T)

st.success(f"## Precio Forward = ${F0_continuo:,.2f}")

elif tipo == "Con ingresos conocidos":
S0 = st.number_input("S0 =", value=50.0)
r = st.number_input("r =", value=0.08)
T = st.number_input("T = (años)", value=1.0)

st.info("Ingresos esperados (ejemplo: dividendos):")
ingreso1 = st.number_input("Ingreso 1", value=2.0)
tiempo1 = st.number_input("Tiempo ingreso 1 (meses)", value=2.0) / 12
ingreso2 = st.number_input("Ingreso 2", value=2.0)
tiempo2 = st.number_input("Tiempo ingreso 2 (meses)", value=5.0) / 12

I = ingreso1 * np.exp(-r * tiempo1) + ingreso2 * np.exp(-r * tiempo2)
F0 = (S0 - I) * np.exp(r * T)

st.success(f"## Precio Forward = ${F0:,.2f}")

elif tipo == "Con yield conocido":
S0 = st.number_input("S0 =", value=100.0)
r = st.number_input("r = (Tasa libre de riesgo)", value=0.05)
q = st.number_input("q = (Yield o tasa de dividendo)", value=0.02)
T = st.number_input("T = (años)", value=1.0)

F0 = S0 * np.exp((r - q) * T)

st.success(f"## Precio Forward = ${F0:,.2f}")

else:
S0 = st.number_input("S0 = (Tipo de cambio spot)", value=19.58)
r = st.number_input("r = (Tasa doméstica)", value=0.0974)
rf = st.number_input("rf = (Tasa extranjera)", value=0.0403)
T = st.number_input("T = (años)", value=1.0)

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

else:
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
