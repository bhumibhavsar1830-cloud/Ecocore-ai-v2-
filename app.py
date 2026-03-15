import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
import io

st.set_page_config(page_title="EcoCore AI v2", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

* { font-family: 'Outfit', sans-serif !important; }

.stApp {
    background: linear-gradient(135deg, #0a0015 0%, #0d0020 40%, #050a05 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0020 0%, #0a0015 100%) !important;
    border-right: 1px solid #7C3AED33 !important;
}

/* Header gradient text */
.gradient-text {
    background: linear-gradient(135deg, #7C3AED, #00E87A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1px;
}

.subtitle-text {
    color: #a0a0c0;
    font-size: 1rem;
    margin-top: -8px;
    margin-bottom: 24px;
}

/* Metric cards */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 20px 0;
}
.metric-card {
    background: linear-gradient(135deg, #1a0035, #0d1a0d);
    border: 1px solid #7C3AED44;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #7C3AED, #00E87A);
}
.metric-icon { font-size: 1.8rem; margin-bottom: 8px; }
.metric-value { font-size: 1.6rem; font-weight: 800; color: #00E87A; }
.metric-label { font-size: 0.75rem; color: #7a7a9a; margin-top: 4px; letter-spacing: 1px; text-transform: uppercase; }
.metric-change { font-size: 0.8rem; color: #7C3AED; margin-top: 4px; }

/* Section headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 32px 0 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #7C3AED22;
}
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #7C3AED, #00E87A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Recommendation cards */
.rec-card {
    background: linear-gradient(135deg, #1a0035, #0d1a0d);
    border: 1px solid #7C3AED33;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 10px 0;
    position: relative;
    overflow: hidden;
}
.rec-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #7C3AED, #00E87A);
}
.rec-title { font-weight: 700; color: #e8e8ff; font-size: 0.95rem; }
.rec-desc { color: #8888aa; font-size: 0.85rem; margin-top: 4px; line-height: 1.5; }
.rec-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 700;
    margin-left: 8px;
}
.badge-high { background: #FF6B6B22; color: #FF6B6B; border: 1px solid #FF6B6B44; }
.badge-medium { background: #FFD93D22; color: #FFD93D; border: 1px solid #FFD93D44; }
.badge-low { background: #00E87A22; color: #00E87A; border: 1px solid #00E87A44; }
.badge-opp { background: #7C3AED22; color: #a78bfa; border: 1px solid #7C3AED44; }

/* Credit cards */
.credit-card {
    background: linear-gradient(135deg, #1a0035, #0d1a0d);
    border: 1px solid #7C3AED44;
    border-radius: 20px;
    padding: 28px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.credit-card::after {
    content: '';
    position: absolute;
    width: 100px; height: 100px;
    background: radial-gradient(circle, #7C3AED11, transparent);
    top: -20px; right: -20px;
    border-radius: 50%;
}
.credit-icon { font-size: 2.5rem; margin-bottom: 12px; }
.credit-value { font-size: 2.2rem; font-weight: 800; color: #00E87A; }
.credit-label { font-size: 0.8rem; color: #7a7a9a; margin-top: 4px; letter-spacing: 1px; }

/* Landing cards */
.feature-card {
    background: linear-gradient(135deg, #1a0035, #0d1a0d);
    border: 1px solid #7C3AED33;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s;
}
.feature-icon { font-size: 2.5rem; margin-bottom: 12px; }
.feature-title { font-weight: 700; color: #e8e8ff; font-size: 1rem; margin-bottom: 8px; }
.feature-desc { color: #7a7a9a; font-size: 0.85rem; line-height: 1.5; }

/* Streamlit overrides */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1a0035, #0d1a0d) !important;
    border: 1px solid #7C3AED44 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #00E87A) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #7C3AED, #00E87A) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load/Train Model ──────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_model():
    model_path = os.path.join(BASE_DIR, "carbon_model.pkl")
    if os.path.exists(model_path):
        return pickle.load(open(model_path, "rb"))
    from sklearn.ensemble import RandomForestRegressor
    np.random.seed(42)
    n = 1000
    units   = np.random.randint(100, 1000, n)
    energy  = np.random.uniform(500, 5000, n)
    renew   = np.random.uniform(0, 100, n)
    down    = np.random.uniform(0, 24, n)
    eff     = np.random.uniform(50, 100, n)
    carbon  = np.clip(energy*0.85 - renew*2.5 + units*0.05 + down*1.2 - eff*0.3 + np.random.normal(0,1.5,n), 5, 200)
    X = np.column_stack([units, energy, renew, down, eff])
    mdl = RandomForestRegressor(n_estimators=100, random_state=42)
    mdl.fit(X, carbon)
    return mdl

model = load_model()

# ── Sidebar ───────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding: 16px 0;'>
    <div style='font-size:2rem'>🌿</div>
    <div style='font-size:1.2rem; font-weight:800; background: linear-gradient(135deg, #7C3AED, #00E87A); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>EcoCore AI</div>
    <div style='font-size:0.7rem; color:#7a7a9a; letter-spacing:2px;'>INDUSTRIAL OPTIMIZER</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("#### ⚙️ Factory Parameters")

factory_name = st.sidebar.text_input("🏭 Factory Name", "My Factory")
units        = st.sidebar.number_input("🏭 Units Produced", 100, 10000, 500, 50)
energy       = st.sidebar.number_input("⚡ Energy (kWh)", 100.0, 10000.0, 1000.0, 50.0)
renewable    = st.sidebar.slider("☀️ Renewable Energy %", 0, 100, 20)
downtime     = st.sidebar.number_input("🔧 Machine Downtime (hrs)", 0.0, 24.0, 5.0, 0.5)
efficiency   = st.sidebar.number_input("📊 Efficiency Index", 50.0, 100.0, 75.0, 1.0)
energy_cost  = st.sidebar.number_input("💰 Energy Cost (₹/kWh)", 5.0, 15.0, 8.0, 0.5)

st.sidebar.markdown("---")
predict_btn = st.sidebar.button("🚀 Predict & Analyze", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align:center; color:#7a7a9a; font-size:0.75rem; line-height:1.8;'>
    Built with ❤️ by<br/>
    <span style='color:#7C3AED; font-weight:700;'>Team EcoOptimizer</span><br/>
    MMIT Pune
</div>
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
import io

st.set_page_config(page_title="EcoCore AI v2", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

* { font-family: 'Outfit', sans-serif !important; }

.stApp {
    background: linear-gradient(135deg, #0a0015 0%, #0d0020 40%, #050a05 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0020 0%, #0a0015 100%) !important;
    border-right: 1px solid #7C3AED33 !important;
}

/* Header gradient text */
.gradient-text {
    background: linear-gradient(135deg, #7C3AED, #00E87A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1px;
}

.subtitle-text {
    color: #a0a0c0;
    font-size: 1rem;
    margin-top: -8px;
    margin-bottom: 24px;
}

/* Metric cards */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 20px 0;
}
.metric-card {
    background: linear-gradient(135deg, #1a0035, #0d1a0d);
    border: 1px solid #7C3AED44;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #7C3AED, #00E87A);
}
.metric-icon { font-size: 1.8rem; margin-bottom: 8px; }
.metric-value { font-size: 1.6rem; font-weight: 800; color: #00E87A; }
.metric-label { font-size: 0.75rem; color: #7a7a9a; margin-top: 4px; letter-spacing: 1px; text-transform: uppercase; }
.metric-change { font-size: 0.8rem; color: #7C3AED; margin-top: 4px; }

/* Section headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 32px 0 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #7C3AED22;
}
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #7C3AED, #00E87A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Recommendation cards */
.rec-card {
    background: linear-gradient(135deg, #1a0035, #0d1a0d);
    border: 1px solid #7C3AED33;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 10px 0;
    position: relative;
    overflow: hidden;
}
.rec-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #7C3AED, #00E87A);
}
.rec-title { font-weight: 700; color: #e8e8ff; font-size: 0.95rem; }
.rec-desc { color: #8888aa; font-size: 0.85rem; margin-top: 4px; line-height: 1.5; }
.rec-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 700;
    margin-left: 8px;
}
.badge-high { background: #FF6B6B22; color: #FF6B6B; border: 1px solid #FF6B6B44; }
.badge-medium { background: #FFD93D22; color: #FFD93D; border: 1px solid #FFD93D44; }
.badge-low { background: #00E87A22; color: #00E87A; border: 1px solid #00E87A44; }
.badge-opp { background: #7C3AED22; color: #a78bfa; border: 1px solid #7C3AED44; }

/* Credit cards */
.credit-card {
    background: linear-gradient(135deg, #1a0035, #0d1a0d);
    border: 1px solid #7C3AED44;
    border-radius: 20px;
    padding: 28px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.credit-card::after {
    content: '';
    position: absolute;
    width: 100px; height: 100px;
    background: radial-gradient(circle, #7C3AED11, transparent);
    top: -20px; right: -20px;
    border-radius: 50%;
}
.credit-icon { font-size: 2.5rem; margin-bottom: 12px; }
.credit-value { font-size: 2.2rem; font-weight: 800; color: #00E87A; }
.credit-label { font-size: 0.8rem; color: #7a7a9a; margin-top: 4px; letter-spacing: 1px; }

/* Landing cards */
.feature-card {
    background: linear-gradient(135deg, #1a0035, #0d1a0d);
    border: 1px solid #7C3AED33;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s;
}
.feature-icon { font-size: 2.5rem; margin-bottom: 12px; }
.feature-title { font-weight: 700; color: #e8e8ff; font-size: 1rem; margin-bottom: 8px; }
.feature-desc { color: #7a7a9a; font-size: 0.85rem; line-height: 1.5; }

/* Streamlit overrides */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1a0035, #0d1a0d) !important;
    border: 1px solid #7C3AED44 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #00E87A) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #7C3AED, #00E87A) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load/Train Model ──────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_model():
    model_path = os.path.join(BASE_DIR, "carbon_model.pkl")
    if os.path.exists(model_path):
        return pickle.load(open(model_path, "rb"))
    from sklearn.ensemble import RandomForestRegressor
    np.random.seed(42)
    n = 1000
    units   = np.random.randint(100, 1000, n)
    energy  = np.random.uniform(500, 5000, n)
    renew   = np.random.uniform(0, 100, n)
    down    = np.random.uniform(0, 24, n)
    eff     = np.random.uniform(50, 100, n)
    carbon  = np.clip(energy*0.85 - renew*2.5 + units*0.05 + down*1.2 - eff*0.3 + np.random.normal(0,1.5,n), 5, 200)
    X = np.column_stack([units, energy, renew, down, eff])
    mdl = RandomForestRegressor(n_estimators=100, random_state=42)
    mdl.fit(X, carbon)
    return mdl

model = load_model()

# ── Sidebar ───────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding: 16px 0;'>
    <div style='font-size:2rem'>🌿</div>
    <div style='font-size:1.2rem; font-weight:800; background: linear-gradient(135deg, #7C3AED, #00E87A); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>EcoCore AI</div>
    <div style='font-size:0.7rem; color:#7a7a9a; letter-spacing:2px;'>INDUSTRIAL OPTIMIZER</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("#### ⚙️ Factory Parameters")

factory_name = st.sidebar.text_input("🏭 Factory Name", "My Factory")
units        = st.sidebar.number_input("🏭 Units Produced", 100, 10000, 500, 50)
energy       = st.sidebar.number_input("⚡ Energy (kWh)", 100.0, 10000.0, 1000.0, 50.0)
renewable    = st.sidebar.slider("☀️ Renewable Energy %", 0, 100, 20)
downtime     = st.sidebar.number_input("🔧 Machine Downtime (hrs)", 0.0, 24.0, 5.0, 0.5)
efficiency   = st.sidebar.number_input("📊 Efficiency Index", 50.0, 100.0, 75.0, 1.0)
energy_cost  = st.sidebar.number_input("💰 Energy Cost (₹/kWh)", 5.0, 15.0, 8.0, 0.5)

st.sidebar.markdown("---")
predict_btn = st.sidebar.button("🚀 Predict & Analyze", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align:center; color:#7a7a9a; font-size:0.75rem; line-height:1.8;'>
    Built with ❤️ by<br/>
    <span style='color:#7C3AED; font-weight:700;'>Team EcoOptimizer</span><br/>
    MMIT Pune
</div>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown("""
<div style='padding: 8px 0 0;'>
    <div class='gradient-text'>🌍 EcoCore AI</div>
    <div class='subtitle-text'>AI-powered Industrial Carbon & Energy Optimization Platform for Indian Manufacturing</div>
</div>
""", unsafe_allow_html=True)

col_h1, col_h2, col_h3 = st.columns(3)
col_h1.markdown("""<div style='background:linear-gradient(135deg,#1a0035,#0d1a0d);border:1px solid #7C3AED33;border-radius:12px;padding:14px;text-align:center;'>
<div style='font-size:1.5rem;font-weight:800;color:#00E87A;'>6 Cr+</div>
<div style='font-size:0.75rem;color:#7a7a9a;letter-spacing:1px;'>INDIAN FACTORIES</div></div>""", unsafe_allow_html=True)
col_h2.markdown("""<div style='background:linear-gradient(135deg,#1a0035,#0d1a0d);border:1px solid #7C3AED33;border-radius:12px;padding:14px;text-align:center;'>
<div style='font-size:1.5rem;font-weight:800;color:#7C3AED;'>30-40%</div>
<div style='font-size:0.75rem;color:#7a7a9a;letter-spacing:1px;'>ENERGY WASTED</div></div>""", unsafe_allow_html=True)
col_h3.markdown("""<div style='background:linear-gradient(135deg,#1a0035,#0d1a0d);border:1px solid #7C3AED33;border-radius:12px;padding:14px;text-align:center;'>
<div style='font-size:1.5rem;font-weight:800;color:#00E87A;'>$2.8B</div>
<div style='font-size:0.75rem;color:#7a7a9a;letter-spacing:1px;'>CO₂ MARKET BY 2027</div></div>""", unsafe_allow_html=True)

st.markdown("<div style='margin:20px 0;border-top:1px solid #7C3AED22;'></div>", unsafe_allow_html=True)

if predict_btn:
    X_in         = np.array([[units, energy, renewable, downtime, efficiency]])
    carbon       = model.predict(X_in)[0]
    optimal      = carbon * 0.70
    saved        = carbon - optimal
    kwh_saved    = energy * 0.25
    money_saved  = kwh_saved * energy_cost * 30
    credit_val   = saved * 750
    annual       = credit_val * 12 + money_saved * 12

    # ── KPI Cards ─────────────────────────────────────────
    st.markdown("<div class='section-header'><span class='section-title'>📊 Live Analysis Dashboard</span></div>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-icon'>🌿</div>
            <div class='metric-value'>{carbon:.1f}</div>
            <div class='metric-label'>Tons CO₂</div>
            <div class='metric-change'>Carbon Emissions</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-icon'>⚡</div>
            <div class='metric-value'>{kwh_saved:.0f}</div>
            <div class='metric-label'>kWh Saveable</div>
            <div class='metric-change'>↓ 25% Reduction</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-icon'>💰</div>
            <div class='metric-value'>₹{money_saved/1000:.0f}K</div>
            <div class='metric-label'>Monthly Savings</div>
            <div class='metric-change'>Potential Benefit</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-icon'>🌱</div>
            <div class='metric-value'>₹{credit_val/1000:.0f}K</div>
            <div class='metric-label'>Carbon Credits</div>
            <div class='metric-change'>{saved:.1f} Tons Saved</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────
    plt.rcParams.update({'font.family': 'DejaVu Sans'})
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'><span class='section-title'>📊 Emissions Analysis</span></div>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 3.5))
        fig.patch.set_facecolor('#0a0015')
        ax.set_facecolor('#0a0015')
        bars = ax.bar(['Current\nEmissions', 'Optimal\nTarget', 'CO₂\nSaved'],
                      [carbon, optimal, saved],
                      color=['#FF6B6B', '#00E87A', '#7C3AED'],
                      width=0.5, edgecolor='#0a0015', linewidth=2,
                      zorder=3)
        for bar, val in zip(bars, [carbon, optimal, saved]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val:.1f}t', ha='center', color='white', fontweight='bold', fontsize=10)
        ax.set_ylabel('Tons CO₂', color='#7a7a9a', fontsize=10)
        ax.set_title('Carbon Emissions Breakdown', color='white', fontweight='bold', fontsize=12, pad=12)
        ax.tick_params(colors='#7a7a9a')
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color='#1a0035', linestyle='--', alpha=0.5, zorder=0)
        for spine in ax.spines.values(): spine.set_color('#1a0035')
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("<div class='section-header'><span class='section-title'>🔋 Energy Breakdown</span></div>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(6, 3.5))
        fig2.patch.set_facecolor('#0a0015')
        sizes = [renewable, max(0, 75 - renewable), 25]
        pie_colors = ['#00E87A', '#FF6B6B', '#7C3AED']
        labels = ['Renewable', 'Non-Renewable', 'Saveable']
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=pie_colors,
                                            autopct='%1.0f%%', startangle=90,
                                            textprops={'color': 'white', 'fontsize': 10},
                                            wedgeprops={'edgecolor': '#0a0015', 'linewidth': 2},
                                            pctdistance=0.75)
        for at in autotexts: at.set_fontweight('bold')
        ax2.set_title('Energy Source Distribution', color='white', fontweight='bold', fontsize=12, pad=12)
        fig2.patch.set_facecolor('#0a0015')
        st.pyplot(fig2)
        plt.close()

    # ── Historical Trends ─────────────────────────────────
    st.markdown("<div class='section-header'><span class='section-title'>📈 30-Day Historical Trends</span></div>", unsafe_allow_html=True)

    dates = pd.date_range(end=datetime.today(), periods=30, freq='D')
    np.random.seed(42)
    hist_c = np.clip(carbon + np.random.normal(0,3,30) + np.linspace(0,-carbon*0.1,30), 0, None)
    hist_e = energy + np.random.normal(0, 50, 30)

    fig3, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 3.5))
    fig3.patch.set_facecolor('#0a0015')

    for ax in [ax3, ax4]:
        ax.set_facecolor('#0a0015')
        ax.tick_params(colors='#7a7a9a', labelsize=8)
        for spine in ax.spines.values(): spine.set_color('#1a0035')
        ax.yaxis.grid(True, color='#1a0035', linestyle='--', alpha=0.5)

    # Carbon trend
    ax3.plot(dates, hist_c, color='#00E87A', linewidth=2.5, zorder=3)
    ax3.fill_between(dates, hist_c, alpha=0.15, color='#00E87A')
    ax3.fill_between(dates, hist_c, alpha=0.05, color='#7C3AED')
    ax3.axhline(y=carbon, color='#7C3AED', linestyle='--', alpha=0.8, linewidth=1.5, label=f'Today: {carbon:.1f}t')
    ax3.set_title('Carbon Emissions Trend', color='white', fontweight='bold', fontsize=11)
    ax3.set_ylabel('Tons CO₂', color='#7a7a9a', fontsize=9)
    ax3.legend(facecolor='#1a0035', edgecolor='#7C3AED44', labelcolor='white', fontsize=8)
    ax3.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d %b'))
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Energy bars
    bar_colors = ['#7C3AED' if e > energy else '#00E87A' for e in hist_e]
    ax4.bar(dates, hist_e, color=bar_colors, alpha=0.8, width=0.7, zorder=3)
    ax4.axhline(y=energy, color='#FFD93D', linestyle='--', alpha=0.8, linewidth=1.5, label=f'Today: {energy:.0f}kWh')
    ax4.set_title('Energy Consumption Trend', color='white', fontweight='bold', fontsize=11)
    ax4.set_ylabel('kWh', color='#7a7a9a', fontsize=9)
    ax4.legend(facecolor='#1a0035', edgecolor='#7C3AED44', labelcolor='white', fontsize=8)
    ax4.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d %b'))
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout(pad=2)
    st.pyplot(fig3)
    plt.close()

    # ── Recommendations ───────────────────────────────────
    st.markdown("<div class='section-header'><span class='section-title'>💡 AI-Powered Recommendations</span></div>", unsafe_allow_html=True)

    recs = []
    if renewable < 30:
        recs.append(("🌞 Increase Renewable Energy",
                      f"Boost renewable from {renewable}% → 40%. Save ~{(40-renewable)*2.5:.1f} tons CO₂/month and reduce grid dependency.", "HIGH"))
    if efficiency < 80:
        recs.append(("⚙️ Predictive Maintenance",
                      f"Efficiency at {efficiency}% is below optimal. Implement IoT-based predictive maintenance to reach 85% → 15% energy reduction.", "HIGH"))
    if downtime > 4:
        recs.append(("🔧 Reduce Machine Downtime",
                      f"Downtime of {downtime}hrs/day is high. Optimize schedules to <2hrs → Save ₹{downtime*500*30:,.0f}/month.", "MEDIUM"))
    if energy > 2000:
        recs.append(("💡 Energy Peak Shifting",
                      "Shift heavy operations to off-peak hours (10PM–6AM). Electricity costs drop 20-30% during off-peak periods.", "MEDIUM"))
    recs.append(("🌱 Carbon Credit Market",
                  f"Register on BEE/UNFCCC carbon market. Earn ₹{credit_val:,.0f}/month by reducing {saved:.1f} tons CO₂.", "OPPORTUNITY"))
    recs.append(("📡 IoT Real-Time Monitoring",
                  "Install smart meters & IoT sensors for granular energy monitoring → Identify waste patterns in real-time.", "LOW"))

    badge_map = {"HIGH": "badge-high", "MEDIUM": "badge-medium", "LOW": "badge-low", "OPPORTUNITY": "badge-opp"}
    for title, desc, priority in recs:
        st.markdown(f"""
        <div class='rec-card'>
            <div class='rec-title'>{title} <span class='rec-badge {badge_map[priority]}'>{priority}</span></div>
            <div class='rec-desc'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    # ── Carbon Credit Calculator ───────────────────────────
    st.markdown("<div class='section-header'><span class='section-title'>🌱 Carbon Credit Calculator</span></div>", unsafe_allow_html=True)

    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        st.markdown(f"""<div class='credit-card'>
            <div class='credit-icon'>🌿</div>
            <div class='credit-value'>{saved:.1f} tons</div>
            <div class='credit-label'>CO₂ SAVED / MONTH</div></div>""", unsafe_allow_html=True)
    with cc2:
        st.markdown(f"""<div class='credit-card'>
            <div class='credit-icon'>💰</div>
            <div class='credit-value'>₹{credit_val:,.0f}</div>
            <div class='credit-label'>CARBON CREDIT VALUE</div></div>""", unsafe_allow_html=True)
    with cc3:
        st.markdown(f"""<div class='credit-card'>
            <div class='credit-icon'>📈</div>
            <div class='credit-value'>₹{annual/100000:.1f}L</div>
            <div class='credit-label'>ANNUAL TOTAL BENEFIT</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Savings Breakdown Chart ────────────────────────────
    st.markdown("<div class='section-header'><span class='section-title'>💸 Annual Savings Breakdown</span></div>", unsafe_allow_html=True)

    fig4, ax5 = plt.subplots(figsize=(10, 3))
    fig4.patch.set_facecolor('#0a0015')
    ax5.set_facecolor('#0a0015')

    categories = ['Energy\nSavings', 'Carbon\nCredits', 'Total\nAnnual']
    values = [money_saved * 12, credit_val * 12, annual]
    bar_c = ['#00E87A', '#7C3AED', '#FFD93D']

    bars2 = ax5.barh(categories, values, color=bar_c, height=0.4, edgecolor='#0a0015', linewid""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown("""
<div style='padding: 8px 0 0;'>
    <div class='gradient-text'>🌍 EcoCore AI</div>
    <div class='subtitle-text'>AI-powered Industrial Carbon & Energy Optimization Platform for Indian Manufacturing</div>
</div>
""", unsafe_allow_html=True)

col_h1, col_h2, col_h3 = st.columns(3)
col_h1.markdown("""<div style='background:linear-gradient(135deg,#1a0035,#0d1a0d);border:1px solid #7C3AED33;border-radius:12px;padding:14px;text-align:center;'>
<div style='font-size:1.5rem;font-weight:800;color:#00E87A;'>6 Cr+</div>
<div style='font-size:0.75rem;color:#7a7a9a;letter-spacing:1px;'>INDIAN FACTORIES</div></div>""", unsafe_allow_html=True)
col_h2.markdown("""<div style='background:linear-gradient(135deg,#1a0035,#0d1a0d);border:1px solid #7C3AED33;border-radius:12px;padding:14px;text-align:center;'>
<div style='font-size:1.5rem;font-weight:800;color:#7C3AED;'>30-40%</div>
<div style='font-size:0.75rem;color:#7a7a9a;letter-spacing:1px;'>ENERGY WASTED</div></div>""", unsafe_allow_html=True)
col_h3.markdown("""<div style='background:linear-gradient(135deg,#1a0035,#0d1a0d);border:1px solid #7C3AED33;border-radius:12px;padding:14px;text-align:center;'>
<div style='font-size:1.5rem;font-weight:800;color:#00E87A;'>$2.8B</div>
<div style='font-size:0.75rem;color:#7a7a9a;letter-spacing:1px;'>CO₂ MARKET BY 2027</div></div>""", unsafe_allow_html=True)

st.markdown("<div style='margin:20px 0;border-top:1px solid #7C3AED22;'></div>", unsafe_allow_html=True)

if predict_btn:
    X_in         = np.array([[units, energy, renewable, downtime, efficiency]])
    carbon       = model.predict(X_in)[0]
    optimal      = carbon * 0.70
    saved        = carbon - optimal
    kwh_saved    = energy * 0.25
    money_saved  = kwh_saved * energy_cost * 30
    credit_val   = saved * 750
    annual       = credit_val * 12 + money_saved * 12

    # ── KPI Cards ─────────────────────────────────────────
    st.markdown("<div class='section-header'><span class='section-title'>📊 Live Analysis Dashboard</span></div>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-icon'>🌿</div>
            <div class='metric-value'>{carbon:.1f}</div>
            <div class='metric-label'>Tons CO₂</div>
            <div class='metric-change'>Carbon Emissions</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-icon'>⚡</div>
            <div class='metric-value'>{kwh_saved:.0f}</div>
            <div class='metric-label'>kWh Saveable</div>
            <div class='metric-change'>↓ 25% Reduction</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-icon'>💰</div>
            <div class='metric-value'>₹{money_saved/1000:.0f}K</div>
            <div class='metric-label'>Monthly Savings</div>
            <div class='metric-change'>Potential Benefit</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-icon'>🌱</div>
            <div class='metric-value'>₹{credit_val/1000:.0f}K</div>
            <div class='metric-label'>Carbon Credits</div>
            <div class='metric-change'>{saved:.1f} Tons Saved</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────
    plt.rcParams.update({'font.family': 'DejaVu Sans'})
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'><span class='section-title'>📊 Emissions Analysis</span></div>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 3.5))
        fig.patch.set_facecolor('#0a0015')
        ax.set_facecolor('#0a0015')
        bars = ax.bar(['Current\nEmissions', 'Optimal\nTarget', 'CO₂\nSaved'],
                      [carbon, optimal, saved],
                      color=['#FF6B6B', '#00E87A', '#7C3AED'],
                      width=0.5, edgecolor='#0a0015', linewidth=2,
                      zorder=3)
        for bar, val in zip(bars, [carbon, optimal, saved]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val:.1f}t', ha='center', color='white', fontweight='bold', fontsize=10)
        ax.set_ylabel('Tons CO₂', color='#7a7a9a', fontsize=10)
        ax.set_title('Carbon Emissions Breakdown', color='white', fontweight='bold', fontsize=12, pad=12)
        ax.tick_params(colors='#7a7a9a')
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color='#1a0035', linestyle='--', alpha=0.5, zorder=0)
        for spine in ax.spines.values(): spine.set_color('#1a0035')
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("<div class='section-header'><span class='section-title'>🔋 Energy Breakdown</span></div>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(6, 3.5))
        fig2.patch.set_facecolor('#0a0015')
        sizes = [renewable, max(0, 75 - renewable), 25]
        pie_colors = ['#00E87A', '#FF6B6B', '#7C3AED']
        labels = ['Renewable', 'Non-Renewable', 'Saveable']
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=pie_colors,
                                            autopct='%1.0f%%', startangle=90,
                                            textprops={'color': 'white', 'fontsize': 10},
                                            wedgeprops={'edgecolor': '#0a0015', 'linewidth': 2},
                                            pctdistance=0.75)
        for at in autotexts: at.set_fontweight('bold')
        ax2.set_title('Energy Source Distribution', color='white', fontweight='bold', fontsize=12, pad=12)
        fig2.patch.set_facecolor('#0a0015')
        st.pyplot(fig2)

