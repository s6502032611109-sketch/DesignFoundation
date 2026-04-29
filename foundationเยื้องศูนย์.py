"""
╔══════════════════════════════════════════════════════════════════╗
║     ECCENTRIC FOOTING DESIGN — TERZAGHI'S BEARING CAPACITY      ║
║     Geotechnical Engineering Tool                                ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import matplotlib.gridspec as gridspec
from io import BytesIO

# ─────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Eccentric Footing Design",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
  }

  /* ── App background ── */
  .stApp {
    background: linear-gradient(135deg, #0d1b2a 0%, #1b2838 60%, #0f2027 100%);
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #112240 0%, #0a1628 100%);
    border-right: 1px solid #1e3a5f;
  }
  [data-testid="stSidebar"] .stMarkdown h2,
  [data-testid="stSidebar"] .stMarkdown h3 {
    color: #64ffda !important;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
  }

  /* ── Sidebar inputs ── */
  [data-testid="stSidebar"] label {
    color: #a8b2d8 !important;
    font-size: 0.82rem;
    font-weight: 600;
  }
  [data-testid="stSidebar"] input {
    background: #0d1b2a !important;
    border: 1px solid #1e3a5f !important;
    color: #ccd6f6 !important;
    border-radius: 6px !important;
  }
  [data-testid="stSidebar"] input:focus {
    border-color: #64ffda !important;
    box-shadow: 0 0 0 2px rgba(100,255,218,0.15) !important;
  }

  /* ── Section divider in sidebar ── */
  .sidebar-divider {
    border: none;
    border-top: 1px solid #1e3a5f;
    margin: 12px 0;
  }

  /* ── Main title ── */
  .main-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    color: #ccd6f6;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 0;
  }
  .main-title span {
    color: #64ffda;
  }
  .subtitle {
    font-family: 'Space Mono', monospace;
    color: #8892b0;
    font-size: 0.78rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 6px;
    margin-bottom: 28px;
  }

  /* ── Metric cards ── */
  .metric-card {
    background: linear-gradient(135deg, #112240 0%, #0d1b2a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
    position: relative;
    overflow: hidden;
  }
  .metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: #64ffda;
    border-radius: 4px 0 0 4px;
  }
  .metric-card.warning::before { background: #ffd166; }
  .metric-card.danger::before  { background: #ef4444; }
  .metric-card.info::before    { background: #38bdf8; }

  .metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.70rem;
    color: #8892b0;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #64ffda;
    line-height: 1.0;
  }
  .metric-card.warning .metric-value { color: #ffd166; }
  .metric-card.danger  .metric-value { color: #ef4444; }
  .metric-card.info    .metric-value { color: #38bdf8; }
  .metric-unit {
    font-size: 0.9rem;
    color: #8892b0;
    font-weight: 400;
    margin-left: 4px;
  }

  /* ── Section headers ── */
  .section-header {
    font-family: 'Space Mono', monospace;
    color: #64ffda;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    border-bottom: 1px solid #1e3a5f;
    padding-bottom: 8px;
    margin-bottom: 16px;
    margin-top: 8px;
  }

  /* ── Status badge ── */
  .status-ok {
    background: rgba(100,255,218,0.12);
    color: #64ffda;
    border: 1px solid rgba(100,255,218,0.35);
    border-radius: 999px;
    padding: 6px 18px;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    display: inline-block;
    letter-spacing: 0.1em;
  }
  .status-fail {
    background: rgba(239,68,68,0.12);
    color: #ef4444;
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 999px;
    padding: 6px 18px;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    display: inline-block;
    letter-spacing: 0.1em;
  }
  .status-warn {
    background: rgba(255,209,102,0.12);
    color: #ffd166;
    border: 1px solid rgba(255,209,102,0.35);
    border-radius: 999px;
    padding: 6px 18px;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    display: inline-block;
    letter-spacing: 0.1em;
  }

  /* ── Formula box ── */
  .formula-box {
    background: #0a1628;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 16px 20px;
    font-family: 'Space Mono', monospace;
    color: #a8b2d8;
    font-size: 0.82rem;
    line-height: 1.8;
    margin-bottom: 12px;
  }
  .formula-box .highlight { color: #64ffda; font-weight: 700; }
  .formula-box .dim { color: #4a5568; }

  /* ── Stress distribution box ── */
  .stress-box {
    background: linear-gradient(135deg,#112240,#0d1b2a);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
  }

  /* ── Footer ── */
  .footer {
    font-family: 'Space Mono', monospace;
    color: #4a5568;
    font-size: 0.68rem;
    text-align: center;
    letter-spacing: 0.1em;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #1e3a5f;
  }

  /* ── Tab styling ── */
  .stTabs [data-baseweb="tab-list"] {
    background: transparent;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    background: #112240;
    color: #8892b0;
    border: 1px solid #1e3a5f;
    border-radius: 8px 8px 0 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    padding: 8px 18px;
  }
  .stTabs [aria-selected="true"] {
    background: #0d1b2a !important;
    color: #64ffda !important;
    border-bottom-color: #0d1b2a !important;
  }
  .stTabs [data-baseweb="tab-panel"] {
    background: #0d1b2a;
    border: 1px solid #1e3a5f;
    border-radius: 0 8px 8px 8px;
    padding: 20px;
  }

  /* ── Expander ── */
  .streamlit-expanderHeader {
    background: #112240 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    color: #ccd6f6 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
  }
  .streamlit-expanderContent {
    background: #0a1628 !important;
    border: 1px solid #1e3a5f !important;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# TERZAGHI BEARING CAPACITY FACTORS
# ─────────────────────────────────────────────────────────────────────
def terzaghi_factors(phi_deg: float) -> tuple[float, float, float]:
    """
    Compute Terzaghi's bearing capacity factors Nc, Nq, Nγ.
    Uses exact Terzaghi (1943) formulations.
    """
    phi = np.radians(phi_deg)

    if phi_deg == 0:
        Nc = 5.14
        Nq = 1.0
        Ngamma = 0.0
    else:
        # Nq — Terzaghi original
        Nq = (np.exp(2 * (0.75 * np.pi - phi / 2) * np.tan(phi))) / (
            2 * np.cos(np.radians(45 + phi_deg / 2)) ** 2
        )
        Nc = (Nq - 1) / np.tan(phi)
        # Nγ — Terzaghi (1943) approximation
        Ngamma = (Nq - 1) * np.tan(1.4 * phi)

    return round(Nc, 3), round(Nq, 3), round(Ngamma, 3)


# ─────────────────────────────────────────────────────────────────────
# EFFECTIVE DIMENSIONS  (Meyerhof's effective area for eccentricity)
# ─────────────────────────────────────────────────────────────────────
def effective_dimensions(B: float, L: float, eB: float, eL: float):
    B_eff = B - 2 * eB
    L_eff = L - 2 * eL
    return max(B_eff, 0.0), max(L_eff, 0.0)


# ─────────────────────────────────────────────────────────────────────
# ULTIMATE BEARING CAPACITY — TERZAGHI (General Shear, Rectangular)
# ─────────────────────────────────────────────────────────────────────
def ultimate_bearing_capacity(
    c: float, phi_deg: float, gamma: float, Df: float,
    B_eff: float, L_eff: float, shape: str = "rectangular"
) -> dict:

    Nc, Nq, Ngamma = terzaghi_factors(phi_deg)

    # Shape factors (Terzaghi)
    if shape == "square":
        sc, sq, sg = 1.3, 1.0, 0.8
    elif shape == "circular":
        sc, sq, sg = 1.3, 1.0, 0.6
    else:  # rectangular
        sc = 1.0 + 0.3 * (B_eff / L_eff) if L_eff > 0 else 1.0
        sq = 1.0
        sg = 1.0 - 0.2 * (B_eff / L_eff) if L_eff > 0 else 1.0

    qu = (c * Nc * sc) + (gamma * Df * Nq * sq) + (0.5 * gamma * B_eff * Ngamma * sg)

    return {
        "Nc": Nc, "Nq": Nq, "Ngamma": Ngamma,
        "sc": round(sc, 4), "sq": round(sq, 4), "sg": round(sg, 4),
        "qu": round(qu, 2),
        "term_cohesion":    round(c * Nc * sc, 2),
        "term_surcharge":   round(gamma * Df * Nq * sq, 2),
        "term_self_weight": round(0.5 * gamma * B_eff * Ngamma * sg, 2),
    }


# ─────────────────────────────────────────────────────────────────────
# CONTACT PRESSURE (Trapezoidal / one-side-zero kernel)
# ─────────────────────────────────────────────────────────────────────
def contact_pressure(P: float, B: float, L: float, eB: float, eL: float):
    A  = B * L
    IB = L * B**3 / 12
    IL = B * L**3 / 12
    MB = P * eB
    ML = P * eL

    q_max = P/A + MB*( B/2)/IB + ML*(L/2)/IL
    q_min = P/A - MB*( B/2)/IB - ML*(L/2)/IL

    return round(q_max, 2), round(q_min, 2)


# ─────────────────────────────────────────────────────────────────────
# STRESS DISTRIBUTION DIAGRAM
# ─────────────────────────────────────────────────────────────────────
def plot_stress_distribution(B, L, eB, q_max, q_min, q_allow):
    """Visualize the contact pressure distribution under the footing."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 5),
                             facecolor='#0d1b2a', gridspec_kw={'wspace': 0.38})

    DARK  = '#0d1b2a'
    PANEL = '#112240'
    TEAL  = '#64ffda'
    WARN  = '#ffd166'
    RED   = '#ef4444'
    GRAY  = '#8892b0'
    TEXT  = '#ccd6f6'
    BLUE  = '#38bdf8'

    for ax in axes:
        ax.set_facecolor(PANEL)
        for sp in ax.spines.values():
            sp.set_edgecolor('#1e3a5f')

    # ── Left: cross-section with trapezoidal stress ──────────────────
    ax = axes[0]
    ax.set_xlim(-0.1, B + 0.1)
    ax.set_ylim(-0.55, 1.15)
    ax.set_title("Contact Pressure Distribution", color=TEXT,
                 fontfamily='monospace', fontsize=9, pad=10, loc='left')

    # Footing rectangle
    footing = patches.Rectangle((0, 0.55), B, 0.3,
                                 linewidth=1.5, edgecolor=TEAL,
                                 facecolor='#1e3a5f', zorder=3)
    ax.add_patch(footing)
    ax.text(B/2, 0.70, f"B = {B:.2f} m", ha='center', va='center',
            color=TEAL, fontfamily='monospace', fontsize=8, fontweight='bold', zorder=4)

    # Eccentric load arrow
    xload = eB + B/2
    ax.annotate('', xy=(xload, 0.85), xytext=(xload, 1.10),
                arrowprops=dict(arrowstyle='->', color=WARN, lw=2.0))
    ax.text(xload + 0.03*B, 1.05, 'P', color=WARN,
            fontfamily='monospace', fontsize=9, fontweight='bold')

    # Neutral axis
    ax.axvline(x=B/2, ymin=0, ymax=0.5, color=GRAY,
               linestyle=':', lw=1.0, zorder=2)
    ax.annotate('', xy=(B/2, 0.30), xytext=(xload, 0.30),
                arrowprops=dict(arrowstyle='<->', color=WARN, lw=1.2))
    ax.text((B/2 + xload)/2, 0.22, f"e={eB:.3f}m",
            ha='center', color=WARN, fontfamily='monospace', fontsize=7.5)

    # Ground line
    ax.axhline(y=0.55, color=GRAY, lw=0.8, linestyle='--', zorder=1)

    # Trapezoid stress block  (below footing: y from 0.55 down to values)
    scale = 0.40 / max(abs(q_max), abs(q_min), 1)
    y_left  = 0.55 - q_max * scale   # q_max at left (x=0) if eB>0
    y_right = 0.55 - q_min * scale

    # Gradient fill
    n = 200
    xs = np.linspace(0, B, n)
    qs = np.linspace(q_max, q_min, n)
    for i in range(n-1):
        col_frac = (qs[i] - q_min) / max(q_max - q_min, 1)
        color = plt.cm.get_cmap('RdYlGn')(0.2 + col_frac * 0.6)
        ax.fill_between([xs[i], xs[i+1]],
                        [0.55, 0.55],
                        [0.55 - qs[i]*scale, 0.55 - qs[i+1]*scale],
                        color=color, alpha=0.75, zorder=2)

    ax.plot([0, B], [y_left, y_right], color=TEAL, lw=2.0, zorder=5)
    ax.plot([0, 0], [0.55, y_left],  color=TEAL, lw=1.5, linestyle='--', zorder=5)
    ax.plot([B, B], [0.55, y_right], color=TEAL, lw=1.5, linestyle='--', zorder=5)

    # Labels
    ax.text(-0.05, y_left, f"{q_max:.1f}", ha='right', va='center',
            color=RED if q_max > q_allow else TEAL,
            fontfamily='monospace', fontsize=7.5, fontweight='bold')
    ax.text(B+0.02, y_right, f"{q_min:.1f}", ha='left', va='center',
            color=BLUE, fontfamily='monospace', fontsize=7.5, fontweight='bold')
    ax.text(-0.05, y_left+0.05, "q_max", ha='right', color=GRAY,
            fontfamily='monospace', fontsize=6.5)
    ax.text(B+0.02, y_right+0.05, "q_min", ha='left', color=GRAY,
            fontfamily='monospace', fontsize=6.5)

    # Allowable line
    y_qa = 0.55 - q_allow * scale
    ax.axhline(y=y_qa, xmin=0.05, xmax=0.95, color=WARN,
               linestyle=(0, (5, 3)), lw=1.2, zorder=6)
    ax.text(B*0.55, y_qa - 0.025, f"q_allow={q_allow:.1f} kPa",
            color=WARN, fontfamily='monospace', fontsize=6.5, zorder=7)

    ax.set_xticks([]); ax.set_yticks([])
    ax.tick_params(colors=GRAY)

    # ── Right: bar chart ─────────────────────────────────────────────
    ax2 = axes[1]
    categories = ['q_max', 'q_allow', 'q_min']
    values     = [q_max, q_allow, q_min]
    colors_bar = [
        RED if q_max > q_allow else TEAL,
        WARN,
        BLUE
    ]
    bars = ax2.barh(categories, values, color=colors_bar,
                    height=0.45, edgecolor='#1e3a5f', linewidth=0.8)

    for bar, val in zip(bars, values):
        ax2.text(val + max(values)*0.02, bar.get_y() + bar.get_height()/2,
                 f"{val:.2f} kPa", va='center',
                 color=TEXT, fontfamily='monospace', fontsize=8.5, fontweight='bold')

    ax2.set_facecolor(PANEL)
    ax2.set_title("Pressure Comparison", color=TEXT,
                  fontfamily='monospace', fontsize=9, pad=10, loc='left')
    ax2.set_xlabel("kPa", color=GRAY, fontfamily='monospace', fontsize=8)
    ax2.tick_params(colors=GRAY, labelsize=8)
    for sp in ax2.spines.values():
        sp.set_edgecolor('#1e3a5f')
    ax2.xaxis.label.set_color(GRAY)
    ax2.yaxis.label.set_color(GRAY)
    ax2.set_xlim(0, max(values) * 1.3)

    # Gridlines
    ax2.xaxis.set_tick_params(labelcolor=GRAY)
    ax2.yaxis.set_tick_params(labelcolor=TEXT)
    ax2.grid(axis='x', color='#1e3a5f', linestyle='--', lw=0.6)
    ax2.set_axisbelow(True)

    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────
# BEARING CAPACITY TERMS PIE
# ─────────────────────────────────────────────────────────────────────
def plot_bc_breakdown(term_c, term_q, term_g, qu):
    fig, ax = plt.subplots(figsize=(5, 4.5), facecolor='#0d1b2a')
    ax.set_facecolor('#112240')

    sizes  = [term_c, term_q, term_g]
    labels = [f'Cohesion\n{term_c:.1f} kPa', f'Surcharge\n{term_q:.1f} kPa',
              f'Self-weight\n{term_g:.1f} kPa']
    colors = ['#64ffda', '#38bdf8', '#ffd166']
    explode = (0.04, 0.04, 0.04)

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, explode=explode,
        autopct='%1.1f%%', startangle=140,
        textprops={'fontfamily': 'monospace', 'color': '#ccd6f6', 'fontsize': 8.0},
        pctdistance=0.72,
        wedgeprops=dict(linewidth=1.5, edgecolor='#0d1b2a')
    )
    for at in autotexts:
        at.set_fontsize(8.0)
        at.set_fontfamily('monospace')
        at.set_color('#0d1b2a')
        at.set_fontweight('bold')

    ax.set_title(f"q_u = {qu:.1f} kPa  |  Bearing Capacity Breakdown",
                 color='#ccd6f6', fontfamily='monospace', fontsize=9, pad=14)
    for sp in ax.spines.values():
        sp.set_visible(False)

    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────
# SIDEBAR  — Input Parameters
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Input Parameters")
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    st.markdown("### 📐 Footing Geometry")
    B = st.number_input("Width  B  (m)", min_value=0.5, max_value=20.0, value=2.0, step=0.1, format="%.2f")
    L = st.number_input("Length  L  (m)", min_value=0.5, max_value=30.0, value=3.0, step=0.1, format="%.2f")
    Df = st.number_input("Depth of Footing  Df  (m)", min_value=0.3, max_value=10.0, value=1.5, step=0.1, format="%.2f")
    shape = st.selectbox("Footing Shape", ["rectangular", "square", "circular"])

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown("### ⚖️ Loading")
    P = st.number_input("Axial Load  P  (kN)", min_value=10.0, max_value=50000.0, value=1200.0, step=10.0)
    eB = st.number_input("Eccentricity  eB  (m)  [along B]", min_value=0.0, max_value=B/2*0.99, value=0.20, step=0.01, format="%.3f")
    eL = st.number_input("Eccentricity  eL  (m)  [along L]", min_value=0.0, max_value=L/2*0.99, value=0.10, step=0.01, format="%.3f")

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown("### 🪨 Soil Properties")
    c    = st.number_input("Cohesion  c  (kPa)", min_value=0.0, max_value=500.0, value=25.0, step=1.0, format="%.1f")
    phi  = st.number_input("Friction Angle  φ  (°)", min_value=0.0, max_value=45.0, value=30.0, step=0.5, format="%.1f")
    gamma = st.number_input("Unit Weight  γ  (kN/m³)", min_value=10.0, max_value=25.0, value=18.0, step=0.5, format="%.1f")

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown("### 🛡️ Safety")
    FS  = st.number_input("Factor of Safety  FS", min_value=1.5, max_value=5.0, value=3.0, step=0.5, format="%.1f")

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    calc_btn = st.button("🔍  CALCULATE", use_container_width=True)


# ─────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-title">Eccentric <span>Footing</span> Design</div>
<div class="subtitle">Terzaghi's General Bearing Capacity Theory · 1943</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# CALCULATE
# ─────────────────────────────────────────────────────────────────────
if calc_btn or True:   # auto-calculate on load
    # Kernel check
    kern_B = B / 6
    kern_L = L / 6
    in_kernel = (eB <= kern_B) and (eL <= kern_L)

    # Effective dimensions
    B_eff, L_eff = effective_dimensions(B, L, eB, eL)

    # Bearing capacity
    result = ultimate_bearing_capacity(c, phi, gamma, Df, B_eff, L_eff, shape)
    qu     = result["qu"]
    q_all  = round(qu / FS, 2)

    # Contact pressure (gross)
    q_max, q_min = contact_pressure(P, B, L, eB, eL)

    # Net allowable
    q_net_all = round((qu - gamma * Df) / FS, 2)

    # Factor of safety check
    actual_FS = round(qu / q_max, 2) if q_max > 0 else float('inf')

    # ── TABS ──────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📊  RESULTS", "📐  DIAGRAMS", "📖  THEORY"])

    # ──────────────────────────────────────────────────────────────────
    # TAB 1 — Results
    # ──────────────────────────────────────────────────────────────────
    with tab1:
        # Status row
        st.markdown("")
        col_s1, col_s2, col_s3 = st.columns([1, 1, 2])
        with col_s1:
            if q_max <= q_all:
                st.markdown('<span class="status-ok">✅  SAFE — q_max ≤ q_allow</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-fail">❌  UNSAFE — q_max > q_allow</span>', unsafe_allow_html=True)
        with col_s2:
            if in_kernel:
                st.markdown('<span class="status-ok">✅  Within Kern</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-warn">⚠️  Outside Kern</span>', unsafe_allow_html=True)
        with col_s3:
            fs_color = "status-ok" if actual_FS >= FS else "status-fail"
            st.markdown(f'<span class="{fs_color}">🔒  Actual FS = {actual_FS:.2f}  (required ≥ {FS:.1f})</span>', unsafe_allow_html=True)

        st.markdown("")

        # Metric cards row 1
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Ultimate Bearing Capacity</div>
              <div class="metric-value">{qu:,.1f}<span class="metric-unit">kPa</span></div>
            </div>""", unsafe_allow_html=True)
        with c2:
            card_cls = "metric-card"
            st.markdown(f"""
            <div class="{card_cls} info">
              <div class="metric-label">Allowable (Gross)</div>
              <div class="metric-value">{q_all:,.1f}<span class="metric-unit">kPa</span></div>
            </div>""", unsafe_allow_html=True)
        with c3:
            cls2 = "danger" if q_max > q_all else ""
            st.markdown(f"""
            <div class="metric-card {cls2}">
              <div class="metric-label">Max Contact Pressure</div>
              <div class="metric-value">{q_max:,.1f}<span class="metric-unit">kPa</span></div>
            </div>""", unsafe_allow_html=True)
        with c4:
            cls3 = "warning" if q_min < 0 else ""
            st.markdown(f"""
            <div class="metric-card {cls3}">
              <div class="metric-label">Min Contact Pressure</div>
              <div class="metric-value">{q_min:,.1f}<span class="metric-unit">kPa</span></div>
            </div>""", unsafe_allow_html=True)

        # Metric cards row 2
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Effective Width B'</div>
              <div class="metric-value">{B_eff:.3f}<span class="metric-unit">m</span></div>
            </div>""", unsafe_allow_html=True)
        with c6:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">Effective Length L'</div>
              <div class="metric-value">{L_eff:.3f}<span class="metric-unit">m</span></div>
            </div>""", unsafe_allow_html=True)
        with c7:
            ek_cls = "" if in_kernel else "warning"
            st.markdown(f"""
            <div class="metric-card {ek_cls}">
              <div class="metric-label">Kern Limit (B/6)</div>
              <div class="metric-value">{kern_B:.3f}<span class="metric-unit">m</span></div>
            </div>""", unsafe_allow_html=True)
        with c8:
            st.markdown(f"""
            <div class="metric-card info">
              <div class="metric-label">Allowable (Net)</div>
              <div class="metric-value">{q_net_all:,.1f}<span class="metric-unit">kPa</span></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("")

        # Bearing capacity factors & shape factors
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown('<div class="section-header">Bearing Capacity Factors (Terzaghi 1943)</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="formula-box">
              <span class="highlight">Nc</span> = {result['Nc']:.3f} &nbsp;&nbsp;
              <span class="highlight">Nq</span> = {result['Nq']:.3f} &nbsp;&nbsp;
              <span class="highlight">Nγ</span> = {result['Ngamma']:.3f}
            </div>
            <div class="formula-box">
              Shape Factors &nbsp;—&nbsp; φ = {phi:.1f}°<br>
              <span class="highlight">sc</span> = {result['sc']:.4f} &nbsp;&nbsp;
              <span class="highlight">sq</span> = {result['sq']:.4f} &nbsp;&nbsp;
              <span class="highlight">sγ</span> = {result['sg']:.4f}
            </div>
            """, unsafe_allow_html=True)

        with col_f2:
            st.markdown('<div class="section-header">Bearing Capacity Term Breakdown</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="formula-box">
              Cohesion Term &nbsp;&nbsp;&nbsp;&nbsp;: <span class="highlight">{result['term_cohesion']:,.2f} kPa</span>
              &nbsp;<span class="dim">({result['term_cohesion']/qu*100:.1f}%)</span><br>
              Surcharge Term &nbsp;&nbsp;&nbsp;: <span class="highlight">{result['term_surcharge']:,.2f} kPa</span>
              &nbsp;<span class="dim">({result['term_surcharge']/qu*100:.1f}%)</span><br>
              Self-weight Term : <span class="highlight">{result['term_self_weight']:,.2f} kPa</span>
              &nbsp;<span class="dim">({result['term_self_weight']/qu*100:.1f}%)</span><br>
              <hr style="border-color:#1e3a5f;margin:8px 0">
              <b>q_u (ultimate)</b> &nbsp;: <span class="highlight">{qu:,.2f} kPa</span>
            </div>
            """, unsafe_allow_html=True)

        # Eccentricity summary
        st.markdown('<div class="section-header">Eccentricity & Kern Check</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="formula-box">
          eB = {eB:.3f} m &nbsp;|&nbsp; Kern limit B/6 = {kern_B:.3f} m
          &nbsp;&nbsp; {'<span class="highlight">✓ OK</span>' if eB <= kern_B else '<span style="color:#ef4444">✗ Exceeds kern — tension may occur</span>'}<br>
          eL = {eL:.3f} m &nbsp;|&nbsp; Kern limit L/6 = {kern_L:.3f} m
          &nbsp;&nbsp; {'<span class="highlight">✓ OK</span>' if eL <= kern_L else '<span style="color:#ef4444">✗ Exceeds kern — tension may occur</span>'}
        </div>
        """, unsafe_allow_html=True)

    # ──────────────────────────────────────────────────────────────────
    # TAB 2 — Diagrams
    # ──────────────────────────────────────────────────────────────────
    with tab2:
        d1, d2 = st.columns([3, 2])
        with d1:
            st.markdown('<div class="section-header">Contact Pressure Distribution</div>', unsafe_allow_html=True)
            fig_stress = plot_stress_distribution(B, L, eB, q_max, q_min, q_all)
            st.pyplot(fig_stress, use_container_width=True)
            plt.close(fig_stress)

        with d2:
            st.markdown('<div class="section-header">Bearing Capacity Composition</div>', unsafe_allow_html=True)
            fig_pie = plot_bc_breakdown(
                result['term_cohesion'],
                result['term_surcharge'],
                result['term_self_weight'],
                qu
            )
            st.pyplot(fig_pie, use_container_width=True)
            plt.close(fig_pie)

        # Eccentricity range chart
        st.markdown('<div class="section-header">q_u vs Eccentricity (eB Sensitivity)</div>', unsafe_allow_html=True)
        eB_range = np.linspace(0, B/2 * 0.98, 60)
        qu_range = []
        for e in eB_range:
            B_e, L_e = effective_dimensions(B, L, e, eL)
            r = ultimate_bearing_capacity(c, phi, gamma, Df, B_e, L_e, shape)
            qu_range.append(r["qu"])

        fig_sens, ax_s = plt.subplots(figsize=(10, 3.5), facecolor='#0d1b2a')
        ax_s.set_facecolor('#112240')
        ax_s.plot(eB_range, qu_range, color='#64ffda', lw=2.5, zorder=3)
        ax_s.fill_between(eB_range, qu_range, alpha=0.12, color='#64ffda', zorder=2)
        ax_s.axvline(x=eB, color='#ffd166', lw=1.8, linestyle='--', zorder=4,
                     label=f'Current eB={eB:.3f}m → qu={qu:.1f} kPa')
        ax_s.axvline(x=kern_B, color='#ef4444', lw=1.4, linestyle=':', zorder=4,
                     label=f'Kern B/6={kern_B:.3f}m')
        ax_s.set_xlabel("Eccentricity eB (m)", color='#8892b0', fontfamily='monospace', fontsize=9)
        ax_s.set_ylabel("q_u  (kPa)", color='#8892b0', fontfamily='monospace', fontsize=9)
        ax_s.tick_params(colors='#8892b0', labelsize=8)
        ax_s.legend(fontsize=8, facecolor='#0d1b2a', edgecolor='#1e3a5f',
                    labelcolor='#ccd6f6', prop={'family': 'monospace'})
        for sp in ax_s.spines.values():
            sp.set_edgecolor('#1e3a5f')
        ax_s.grid(color='#1e3a5f', linestyle='--', lw=0.6)
        plt.tight_layout()
        st.pyplot(fig_sens, use_container_width=True)
        plt.close(fig_sens)

    # ──────────────────────────────────────────────────────────────────
    # TAB 3 — Theory
    # ──────────────────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">Terzaghi\'s General Bearing Capacity Equation</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="formula-box" style="font-size:0.9rem;line-height:2.2">
          <span class="highlight">q_u = c · Nc · sc  +  γ · Df · Nq · sq  +  ½ · γ · B' · Nγ · sγ</span>
          <br>
          <span class="dim">─────────────────────────────────────────────────────</span><br>
          c  &nbsp;= cohesion (kPa) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          γ  = unit weight of soil (kN/m³)<br>
          Df = depth of footing (m) &nbsp;&nbsp;&nbsp;
          B' = effective width = B − 2eB (m)<br>
          L' = effective length = L − 2eL (m)
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Bearing Capacity Factors — Terzaghi (1943)</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="formula-box" style="line-height:2.1">
          <span class="highlight">Nq</span> = exp(2π(0.75 − φ/2)·tanφ) / [2·cos²(45+φ/2)]<br>
          <span class="highlight">Nc</span> = (Nq − 1) / tanφ &nbsp;&nbsp;&nbsp; (5.14 when φ=0)<br>
          <span class="highlight">Nγ</span> = (Nq − 1)·tan(1.4φ)
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Shape Factors (Rectangular Footing)</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="formula-box" style="line-height:2.1">
          <span class="highlight">sc</span> = 1 + 0.3(B'/L') &nbsp;&nbsp;
          <span class="highlight">sq</span> = 1.0 &nbsp;&nbsp;
          <span class="highlight">sγ</span> = 1 − 0.2(B'/L')
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Eccentric Loading — Meyerhof\'s Effective Area</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="formula-box" style="line-height:2.1">
          <span class="highlight">B' = B − 2eB</span> &nbsp;&nbsp;&nbsp; <span class="highlight">L' = L − 2eL</span><br>
          Kern condition (no tension): &nbsp;
          <span class="highlight">eB ≤ B/6 &nbsp;&amp;&amp;&nbsp; eL ≤ L/6</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Contact Pressure Distribution</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="formula-box" style="line-height:2.1">
          q = P/A ± M·y/I<br>
          <span class="highlight">q_max</span> = P/(BL) + P·eB·(B/2)/(LB³/12) + P·eL·(L/2)/(BL³/12)<br>
          <span class="highlight">q_min</span> = P/(BL) − P·eB·(B/2)/(LB³/12) − P·eL·(L/2)/(BL³/12)
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Allowable Bearing Capacity</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="formula-box" style="line-height:2.1">
          <span class="highlight">q_allow (gross)</span> = q_u / FS = {qu:.2f} / {FS:.1f} = {q_all:.2f} kPa<br>
          <span class="highlight">q_allow (net)</span> &nbsp; = (q_u − γ·Df) / FS = {q_net_all:.2f} kPa<br>
          <span class="dim">Reference: Terzaghi, K. (1943). Theoretical Soil Mechanics. Wiley.</span>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Eccentric Footing Design · Terzaghi (1943) · Geotechnical Engineering Tool<br>
  For educational and preliminary design purposes only — verify with site-specific investigations
</div>
""", unsafe_allow_html=True)
