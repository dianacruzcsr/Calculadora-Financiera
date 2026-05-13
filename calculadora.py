import { useState, useEffect, useRef } from "react";

// ─── colour tokens ──────────────────────────────────────────────────────────
const C = {
  bg: "#0d1117",
  panel: "#161b22",
  card: "#1c2230",
  border: "#2a3444",
  accent: "#22d3ee",
  accentDim: "#0e7490",
  green: "#10b981",
  greenDim: "#065f46",
  text: "#e2e8f0",
  muted: "#64748b",
  label: "#94a3b8",
};

// ─── tiny helpers ────────────────────────────────────────────────────────────
const fmt = (v, d = 6) =>
  (v * 100).toLocaleString("es-CO", {
    minimumFractionDigits: d,
    maximumFractionDigits: d,
  }) + "%";

const fmtN = (v, d = 2) =>
  v.toLocaleString("es-CO", {
    minimumFractionDigits: d,
    maximumFractionDigits: d,
  });

// ─── Sparkline canvas ────────────────────────────────────────────────────────
function LineChart({ data, xLabel, yLabel, color = C.accent, width = 520, height = 260, dots = [] }) {
  const ref = useRef();
  useEffect(() => {
    const canvas = ref.current;
    if (!canvas || data.length < 2) return;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
    const ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);

    const pad = { top: 24, right: 24, bottom: 48, left: 72 };
    const W = width - pad.left - pad.right;
    const H = height - pad.top - pad.bottom;

    const xs = data.map((d) => d[0]);
    const ys = data.map((d) => d[1]);
    const xMin = Math.min(...xs), xMax = Math.max(...xs);
    const yMin = Math.min(...ys) * 0.998, yMax = Math.max(...ys) * 1.002;

    const px = (x) => pad.left + ((x - xMin) / (xMax - xMin || 1)) * W;
    const py = (y) => pad.top + H - ((y - yMin) / (yMax - yMin || 1)) * H;

    // grid
    ctx.strokeStyle = C.border;
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= 4; i++) {
      const y = pad.top + (H / 4) * i;
      ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(pad.left + W, y); ctx.stroke();
      const val = yMax - ((yMax - yMin) / 4) * i;
      ctx.fillStyle = C.muted; ctx.font = "10px monospace"; ctx.textAlign = "right";
      ctx.fillText(fmtN(val, 0), pad.left - 6, y + 4);
    }

    // x ticks
    const xTicks = 5;
    for (let i = 0; i <= xTicks; i++) {
      const x = xMin + ((xMax - xMin) / xTicks) * i;
      ctx.fillStyle = C.muted; ctx.font = "10px monospace"; ctx.textAlign = "center";
      ctx.fillText(fmtN(x, 2), px(x), height - pad.bottom + 18);
    }

    // axis labels
    ctx.fillStyle = C.label; ctx.font = "11px sans-serif"; ctx.textAlign = "center";
    ctx.fillText(xLabel, pad.left + W / 2, height - 4);
    ctx.save(); ctx.translate(14, pad.top + H / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText(yLabel, 0, 0); ctx.restore();

    // line with gradient fill
    const grad = ctx.createLinearGradient(0, pad.top, 0, pad.top + H);
    grad.addColorStop(0, color + "55");
    grad.addColorStop(1, color + "00");
    ctx.beginPath();
    data.forEach(([x, y], i) => { if (i === 0) ctx.moveTo(px(x), py(y)); else ctx.lineTo(px(x), py(y)); });
    ctx.lineTo(px(xs[xs.length - 1]), pad.top + H);
    ctx.lineTo(px(xs[0]), pad.top + H);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();

    ctx.beginPath();
    data.forEach(([x, y], i) => { if (i === 0) ctx.moveTo(px(x), py(y)); else ctx.lineTo(px(x), py(y)); });
    ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.stroke();

    // labelled dots
    dots.forEach(([x, y, label]) => {
      ctx.beginPath(); ctx.arc(px(x), py(y), 4, 0, Math.PI * 2);
      ctx.fillStyle = color; ctx.fill();
      ctx.strokeStyle = C.bg; ctx.lineWidth = 1.5; ctx.stroke();
      ctx.fillStyle = C.text; ctx.font = "bold 9px monospace"; ctx.textAlign = "left";
      ctx.fillText(`${label}, ${fmtN(y, 0)}`, px(x) + 6, py(y) - 4);
    });
  }, [data, xLabel, yLabel, color, width, height, dots]);

  return <canvas ref={ref} style={{ borderRadius: 8, background: C.panel, display: "block" }} />;
}

// ─── Slider input ────────────────────────────────────────────────────────────
function Field({ label, value, onChange, min, max, step, format }) {
  return (
    <div style={{ marginBottom: 20 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
        <span style={{ color: C.label, fontSize: 13, fontFamily: "sans-serif" }}>{label}</span>
        <span style={{ color: C.accent, fontSize: 14, fontFamily: "monospace", fontWeight: 700 }}>
          {format ? format(value) : value}
        </span>
      </div>
      <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
        <button onClick={() => onChange(Math.max(min, parseFloat((value - step).toFixed(10))))}
          style={btnSm}>−</button>
        <input type="range" min={min} max={max} step={step} value={value}
          onChange={(e) => onChange(parseFloat(e.target.value))}
          style={{ flex: 1, accentColor: C.accent, height: 4 }} />
        <button onClick={() => onChange(Math.min(max, parseFloat((value + step).toFixed(10))))}
          style={btnSm}>+</button>
      </div>
    </div>
  );
}

const btnSm = {
  background: C.card, border: `1px solid ${C.border}`, color: C.text,
  borderRadius: 6, width: 28, height: 28, cursor: "pointer", fontSize: 16,
  display: "flex", alignItems: "center", justifyContent: "center",
};

// ─── Result box ──────────────────────────────────────────────────────────────
function Result({ label, value }) {
  return (
    <div style={{
      background: C.greenDim, border: `1px solid ${C.green}`, borderRadius: 10,
      padding: "14px 20px", marginBottom: 16,
    }}>
      <span style={{ color: C.green, fontSize: 15, fontFamily: "monospace" }}>{label}: {value}</span>
    </div>
  );
}

// ─── LaTeX-ish formula renderer (SVG text) ───────────────────────────────────
function Formula({ children }) {
  return (
    <div style={{
      background: C.card, border: `1px solid ${C.border}`, borderRadius: 10,
      padding: "14px 20px", marginTop: 12, textAlign: "center",
      color: C.label, fontSize: 14, fontFamily: "Georgia, serif", letterSpacing: "0.02em",
    }}>
      {children}
    </div>
  );
}

// ─── SECTION: Nominal → Nominal ──────────────────────────────────────────────
function NominalNominal() {
  const [m, setM] = useState(2);
  const [iM, setIM] = useState(0.10);
  const [p, setP] = useState(3);

  const iP = p * ((1 + iM / m) ** (m / p) - 1);

  // convergence curve: vary p from 0.1 to 365
  const pVals = [0.25, 0.5, 1, 2, 4, 12, 52, 365];
  const chartData = pVals.map((pv) => [pv, pv * ((1 + iM / m) ** (m / pv) - 1) * 100]);
  const labeledDots = [
    [0.25, pVals[0] * ((1 + iM / m) ** (m / pVals[0]) - 1) * 100, "0.25"],
    [0.5,  pVals[1] * ((1 + iM / m) ** (m / pVals[1]) - 1) * 100, "0.5"],
    [2,    pVals[3] * ((1 + iM / m) ** (m / pVals[3]) - 1) * 100, "2"],
    [12,   pVals[5] * ((1 + iM / m) ** (m / pVals[5]) - 1) * 100, "12"],
  ];

  return (
    <div>
      <Field label="Frecuencia m" value={m} onChange={setM} min={1} max={52} step={1}
        format={(v) => v.toFixed(2)} />
      <Field label="Tasa nominal i(m)" value={iM} onChange={setIM} min={0.01} max={1} step={0.01}
        format={(v) => (v * 100).toFixed(2) + "%"} />
      <Field label="Nueva frecuencia p" value={p} onChange={setP} min={1} max={52} step={1}
        format={(v) => v.toFixed(2)} />

      <Result label="Tasa nominal equivalente i(p)" value={fmt(iP)} />

      <Formula>
        i<sup>(p)</sup> = p · [(1 + i<sup>(m)</sup>/m)<sup>m/p</sup> − 1]
      </Formula>

      <div style={{ marginTop: 20 }}>
        <p style={{ color: C.label, fontSize: 12, marginBottom: 8 }}>
          Convergencia de tasas nominales equivalentes
        </p>
        <LineChart
          data={chartData}
          xLabel="Frecuencia p (reinversiones/año)"
          yLabel="Tasa nominal (%)"
          color={C.accent}
          dots={labeledDots}
        />
      </div>
    </div>
  );
}

// ─── SECTION: Reinversión de intereses ───────────────────────────────────────
function Reinversion() {
  const [C0, setC0] = useState(100000);
  const [i, setI] = useState(0.10);
  const [n, setN] = useState(10);

  const periodos = [
    { label: "Cada 4 años", m: 0.25 },
    { label: "Cada 2 años", m: 0.50 },
    { label: "Anual", m: 1 },
    { label: "Semestral", m: 2 },
    { label: "Trimestral", m: 4 },
    { label: "Mensual", m: 12 },
    { label: "Semanal", m: 52 },
    { label: "Diaria", m: 365 },
    { label: "Cada hora", m: 8760 },
    { label: "Cada minuto", m: 525600 },
    { label: "Cada segundo", m: 31536000 },
    { label: "Instantánea", m: Infinity },
  ];

  const calcSaldo = (m) =>
    m === Infinity ? C0 * Math.exp(i * n) : C0 * (1 + i / m) ** (m * n);

  const rows = periodos.map((p) => ({ ...p, saldo: calcSaldo(p.m) }));

  // chart: m vs saldo acumulado
  const mVals = [0.25, 0.5, 1, 2, 4, 12, 52, 365, 8760, 525600];
  const chartData = mVals.map((m) => [m, C0 * (1 + i / m) ** (m * n)]);
  const labeledDots = [[0.25, C0*(1+i/0.25)**(0.25*n), "0.25"],
                        [0.5,  C0*(1+i/0.5)**(0.5*n),  "0.50"],
                        [1,    C0*(1+i)**n,              "1"],
                        [2,    C0*(1+i/2)**(2*n),        "2"],
                        [12,   C0*(1+i/12)**(12*n),      "12"]];

  return (
    <div>
      <Field label="Capital inicial C₀" value={C0} onChange={setC0} min={1000} max={1000000} step={1000}
        format={(v) => "$" + fmtN(v, 0)} />
      <Field label="Tasa efectiva anual i" value={i} onChange={setI} min={0.01} max={0.5} step={0.01}
        format={(v) => (v * 100).toFixed(0) + "%"} />
      <Field label="Años n" value={n} onChange={setN} min={1} max={30} step={1}
        format={(v) => v + " años"} />

      <p style={{ color: C.label, fontSize: 12, marginBottom: 10 }}>
        Saldo acumulado según frecuencia de reinversión
      </p>

      <div style={{ overflowX: "auto", marginBottom: 20 }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13, fontFamily: "monospace" }}>
          <thead>
            <tr style={{ background: C.card }}>
              {["Período de reinversión", "m (veces/año)", "Monto acumulado"].map((h) => (
                <th key={h} style={{ padding: "8px 12px", textAlign: "right", color: C.label,
                  borderBottom: `1px solid ${C.border}`, whiteSpace: "nowrap" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.label} style={{ borderBottom: `1px solid ${C.border}20` }}>
                <td style={{ padding: "7px 12px", color: C.text, textAlign: "right" }}>{r.label}</td>
                <td style={{ padding: "7px 12px", color: C.muted, textAlign: "right" }}>
                  {r.m === Infinity ? "∞" : fmtN(r.m, 2)}
                </td>
                <td style={{ padding: "7px 12px", color: C.green, textAlign: "right", fontWeight: 700 }}>
                  {fmtN(r.saldo, 0)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <LineChart
        data={chartData}
        xLabel="m — Reinversión de los intereses (veces/año)"
        yLabel="Saldo acumulado"
        color={C.green}
        dots={labeledDots}
        width={520}
        height={260}
      />

      <Formula>
        C<sub>n</sub> = C<sub>0</sub>(1 + i/m)<sup>m·n</sup> &nbsp;|&nbsp;
        C<sub>∞</sub> = C<sub>0</sub>·e<sup>i·n</sup>
      </Formula>
    </div>
  );
}

// ─── SECTION: Nominal → Efectiva e instantánea ───────────────────────────────
function NominalEfectiva() {
  const [iNom, setINom] = useState(0.40);
  const [m, setM] = useState(2);

  const iEf = (1 + iNom / m) ** m - 1;
  const delta = m * Math.log(1 + iNom / m);

  return (
    <div>
      <Field label="Tasa nominal i(m)" value={iNom} onChange={setINom} min={0.01} max={2} step={0.01}
        format={(v) => (v * 100).toFixed(2) + "%"} />
      <Field label="m (frecuencia)" value={m} onChange={setM} min={1} max={52} step={1}
        format={(v) => v.toFixed(0)} />
      <Result label="Tasa efectiva i" value={fmt(iEf)} />
      <Result label="Tasa instantánea δ" value={fmt(delta)} />
      <Formula>
        i = (1 + i<sup>(m)</sup>/m)<sup>m</sup> − 1 &nbsp;&nbsp;|&nbsp;&nbsp;
        δ = m·ln(1 + i<sup>(m)</sup>/m)
      </Formula>
    </div>
  );
}

// ─── SECTION: Instantánea → Efectiva ─────────────────────────────────────────
function InstEfectiva() {
  const [delta, setDelta] = useState(0.005);
  const iEf = Math.exp(delta) - 1;
  return (
    <div>
      <Field label="Tasa instantánea δ" value={delta} onChange={setDelta} min={0.001} max={0.5} step={0.001}
        format={(v) => (v * 100).toFixed(3) + "%"} />
      <Result label="Tasa efectiva i" value={fmt(iEf)} />
      <Formula>i = e<sup>δ</sup> − 1</Formula>
    </div>
  );
}

// ─── SECTION: Instantánea → Nominal ──────────────────────────────────────────
function InstNominal() {
  const [delta, setDelta] = useState(0.07);
  const [m, setM] = useState(2);
  const iNom = m * (Math.exp(delta / m) - 1);
  return (
    <div>
      <Field label="Tasa instantánea δ" value={delta} onChange={setDelta} min={0.001} max={0.5} step={0.001}
        format={(v) => (v * 100).toFixed(3) + "%"} />
      <Field label="m (frecuencia)" value={m} onChange={setM} min={1} max={52} step={1}
        format={(v) => v.toFixed(0)} />
      <Result label="Tasa nominal i(m)" value={fmt(iNom)} />
      <Formula>i<sup>(m)</sup> = m·(e<sup>δ/m</sup> − 1)</Formula>
    </div>
  );
}

// ─── MENU ────────────────────────────────────────────────────────────────────
const SECTIONS = [
  { id: "nom-ef",   label: "Nominal → Efectiva",   component: NominalEfectiva },
  { id: "inst-ef",  label: "Instantánea → Efectiva", component: InstEfectiva },
  { id: "inst-nom", label: "Instantánea → Nominal", component: InstNominal },
  { id: "nom-nom",  label: "Nominal → Nominal",     component: NominalNominal },
  { id: "reinv",    label: "Reinversión intereses",  component: Reinversion },
];

// ─── ROOT ────────────────────────────────────────────────────────────────────
export default function App() {
  const [active, setActive] = useState("nom-nom");

  const Section = SECTIONS.find((s) => s.id === active)?.component ?? (() => null);

  return (
    <div style={{
      minHeight: "100vh", background: C.bg, color: C.text,
      fontFamily: "'Segoe UI', sans-serif", padding: "0 0 40px",
    }}>
      {/* header */}
      <div style={{
        background: C.panel, borderBottom: `1px solid ${C.border}`,
        padding: "18px 28px", display: "flex", alignItems: "center", gap: 14,
      }}>
        <span style={{ fontSize: 22, color: C.accent }}>📈</span>
        <div>
          <h1 style={{ margin: 0, fontSize: 18, fontWeight: 700, color: C.text }}>
            Calculadora de Matemáticas Financieras
          </h1>
          <p style={{ margin: 0, fontSize: 12, color: C.muted }}>Conversión de Tasas de Interés</p>
        </div>
      </div>

      <div style={{ display: "flex", gap: 0 }}>
        {/* sidebar */}
        <nav style={{
          width: 220, background: C.panel, borderRight: `1px solid ${C.border}`,
          minHeight: "calc(100vh - 65px)", padding: "20px 0",
          flexShrink: 0,
        }}>
          {SECTIONS.map((s) => (
            <button key={s.id} onClick={() => setActive(s.id)}
              style={{
                display: "block", width: "100%", textAlign: "left",
                padding: "11px 22px", border: "none", cursor: "pointer",
                fontSize: 13, fontFamily: "sans-serif",
                background: active === s.id ? C.card : "transparent",
                color: active === s.id ? C.accent : C.label,
                borderLeft: active === s.id ? `3px solid ${C.accent}` : "3px solid transparent",
                transition: "all 0.15s",
              }}>
              {s.label}
            </button>
          ))}
        </nav>

        {/* main */}
        <main style={{ flex: 1, padding: "28px 32px", maxWidth: 640 }}>
          <h2 style={{
            margin: "0 0 22px", fontSize: 20, fontWeight: 700, color: C.text,
            borderBottom: `1px solid ${C.border}`, paddingBottom: 14,
          }}>
            {SECTIONS.find((s) => s.id === active)?.label}
          </h2>
          <Section />
        </main>
      </div>
    </div>
  );
}
