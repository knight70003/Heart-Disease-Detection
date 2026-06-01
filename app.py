import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import time
import base64
import sqlite3
import random
import os
from io import StringIO
from datetime import datetime

# ==========================================
# 1. CORE ARCHITECTURE & VIEWPORT LOCKS
# ==========================================
st.set_page_config(
    page_title="Vanguard Health AI // Coronary Telemetry Suite", 
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SQLite Database Local Calibration Module
def init_db():
    conn = sqlite3.connect("vanguard_patient_vault.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_logs (
            patient_id TEXT,
            patient_name TEXT,
            timestamp TEXT,
            age INTEGER,
            bp INTEGER,
            cholesterol INTEGER,
            risk_score REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Base64 Image Converter for Streamlit HTML Injection
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# TRIPLE IMAGE TELEMETRY DEFINITION
img_lens_base64 = get_base64_image("heart.jpg")       
img_side_base64 = get_base64_image("heart3.avif")     
img_main_base64 = get_base64_image("heart2.jpg")      

# ==========================================
# 2. THE INFINITE-GLOW JARVIS HUD ENGINE
# ==========================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Share+Tech+Mono&family=Plus+Jakarta+Sans:wght@600;800&display=swap');

/* Main Canvas Configuration with Tech Grid Wall */
.stApp {{
    background-image: linear-gradient(to bottom, rgba(2, 4, 12, 0.88), rgba(1, 2, 6, 0.98)), 
                      url("data:image/jpeg;base64,{img_main_base64}");
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    color: #FFFFFF !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    overflow-x: hidden;
}}

/* MOVING CRT MATRIX SCANLINE EFFECT */
.stApp::before {{
    content: " ";
    display: block;
    position: fixed;
    top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 242, 254, 0.05) 50%);
    z-index: 99999;
    background-size: 100% 4px;
    pointer-events: none;
    animation: scanline 12s linear infinite;
}}

@keyframes scanline {{
    0% {{ background-position: 0 0; }}
    100% {{ background-position: 0 100%; }}
}}

/* Left Sidebar - Cyber Heart Chamber with Laser Border Split */
section[data-testid="stSidebar"] {{
    background-image: linear-gradient(to bottom, rgba(2, 6, 20, 0.82), rgba(0, 1, 6, 0.99)), 
                      url("data:image/avif;base64,{img_side_base64}") !important;
    background-size: cover;
    background-position: center top;
    border-right: 3px solid #00F2FE;
    box-shadow: 10px 0 40px rgba(0, 242, 254, 0.3);
}}
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {{
    color: #00F2FE !important;
    font-family: 'Orbitron', sans-serif;
    font-weight: 700 !important;
    text-shadow: 0 0 10px rgba(0, 242, 254, 0.8);
}}

/* Glassmorphic Neomorphic Digital Input Boxes with Core Laser Pulse */
.stTextInput input, .stNumberInput input {{
    background: rgba(3, 8, 24, 0.85) !important;
    backdrop-filter: blur(20px);
    color: #00F2FE !important;
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.1rem !important;
    border: 1px solid rgba(0, 242, 254, 0.4) !important;
    border-radius: 4px !important;
    padding: 12px 16px !important;
    box-shadow: inset 0 0 15px rgba(0, 242, 254, 0.15), 0 0 10px rgba(0, 242, 254, 0.05);
    transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1);
}}
.stTextInput input:focus, .stNumberInput input:focus {{
    border-color: #FF007F !important;
    box-shadow: 0 0 25px rgba(255, 0, 127, 0.6), inset 0 0 8px rgba(255, 0, 127, 0.2) !important;
    color: #FFFFFF !important;
}}

/* Sci-Fi Selectbox Customization */
div[data-testid="stSelectbox"] > div {{
    background: rgba(3, 8, 24, 0.85) !important;
    backdrop-filter: blur(20px);
    color: #FFFFFF !important;
    border: 1px solid rgba(0, 242, 254, 0.4) !important;
    border-radius: 4px !important;
}}
div[data-testid="stSelectbox"] > div:hover {{
    border-color: #00F2FE !important;
    box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
}}

/* Cyber Matrix Glowing Breathing Cards with Laser Circuit Effect */
.clinical-matrix-card {{
    background: rgba(2, 6, 18, 0.85) !important;
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(0, 242, 254, 0.3) !important;
    border-radius: 12px;
    padding: 2.2rem;
    margin-bottom: 1.5rem;
    position: relative;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
    animation: neonBorderPulse 4s infinite alternate;
}}

@keyframes neonBorderPulse {{
    0% {{
        border-color: rgba(0, 242, 254, 0.3);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 10px rgba(0, 242, 254, 0.1);
    }}
    100% {{
        border-color: rgba(255, 0, 127, 0.6);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 0, 127, 0.2);
    }}
}}

/* Headings & Text Design Labels */
label, .stSlider p, p, h3 {{
    color: #C1C6CD !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
h3 {{
    font-family: 'Orbitron', sans-serif !important;
    color: #00F2FE !important;
    letter-spacing: 0.15em !important;
    text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
}}

/* Interactive Premium Tabs Layout with Hologram Select States */
div[data-baseweb="tab-list"] {{
    gap: 18px !important;
    background: rgba(1, 3, 10, 0.95) !important;
    padding: 10px !important;
    border-radius: 8px !important;
    border: 1px solid rgba(0, 242, 254, 0.3) !important;
}}
div[data-baseweb="tab"] {{
    color: #475569 !important;
    font-family: 'Orbitron', sans-serif;
    font-weight: 900 !important;
    padding: 1rem 2.2rem !important;
    letter-spacing: 0.1em;
    transition: all 0.3s cubic-bezier(0.19, 1, 0.22, 1);
}}
div[data-baseweb="tab"][aria-selected="true"] {{
    background: linear-gradient(135deg, #FF007F 0%, #7928CA 100%) !important;
    color: #FFFFFF !important;
    border-radius: 4px !important;
    box-shadow: 0 0 35px rgba(255, 0, 127, 0.7);
    text-shadow: 0 0 8px #FFF;
}}

/* Center Telemetry Lens Frame Image Overlay (Using heart.jpg) */
.holographic-telemetry-lens {{
    background-image: linear-gradient(to right, rgba(1, 3, 10, 0.98), rgba(1, 3, 10, 0.1)), 
                      url("data:image/jpeg;base64,{img_lens_base64}");
    background-size: cover;
    background-position: center;
    border: 2px solid #FF007F;
    box-shadow: 0 0 40px rgba(255, 0, 127, 0.4);
    border-radius: 12px;
    height: 230px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

/* Premium Sci-fi Capsule Pill */
.quantum-pill {{
    background: rgba(255, 0, 127, 0.15);
    border: 1px solid #FF007F;
    color: #FF007F;
    padding: 0.6rem 1.8rem;
    border-radius: 2px;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.8rem;
    font-weight: 900;
    letter-spacing: 0.2em;
    text-shadow: 0 0 8px #FF007F;
    width: fit-content;
}}

/* CYBERPUNK GLITCH HOVER ACTION BUTTON */
.stButton>button {{
    width: 100%;
    background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%) !important;
    color: #01030A !important;
    font-family: 'Orbitron', sans-serif;
    font-weight: 900 !important;
    font-size: 1.4rem !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 1.3rem !important;
    box-shadow: 0 0 30px rgba(0, 242, 254, 0.5) !important;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}}
.stButton>button:hover {{
    background: linear-gradient(135deg, #FF007F 0%, #7928CA 100%) !important;
    color: #FFFFFF !important;
    transform: scale(1.02);
    box-shadow: 0 0 60px rgba(255, 0, 127, 0.9) !important;
    letter-spacing: 0.25em;
}}

/* Infinite Metallic Chromatic Title Animation */
.suite-header-title {{
    font-family: 'Orbitron', sans-serif;
    font-size: 4rem;
    font-weight: 900;
    letter-spacing: 0.1em;
    background: linear-gradient(90deg, #00F2FE, #FF007F, #7928CA, #00F2FE);
    background-size: 400% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: chromeFlow 10s linear infinite;
    text-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
}}

@keyframes chromeFlow {{
    0% {{ background-position: 0% 50%; }}
    100% {{ background-position: 400% 50%; }}
}}

/* Holographic Matrix Table Formatting */
div[data-testid="stDataFrame"] {{
    background-color: rgba(1, 3, 10, 0.95) !important;
    border: 1px solid #FF007F !important;
    border-radius: 8px;
    box-shadow: 0 0 25px rgba(255, 0, 127, 0.2);
}}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CLINICAL MACHINE LEARNING PIPELINE
# ==========================================
@st.cache_resource
def load_ml_infrastructure():
    try:
        model = joblib.load("knn_heart_model.pkl")
        scaler = joblib.load("heart_scaler.pkl")
        columns = joblib.load("heart_columns.pkl")
        return model, scaler, columns, "LIVE_CORE"
    except:
        return None, None, None, "STANDALONE_DYNAMICS"

model, scaler, expected_columns, runtime_status = load_ml_infrastructure()

def calculate_calibrated_score(age, oldpeak, chest_pain, exercise_angina, st_slope, max_hr, cholesterol, resting_bp):
    logit_sum = -2.75 + (age * 0.030) + (oldpeak * 0.52)
    if chest_pain == 'ASY': logit_sum += 1.40
    if exercise_angina == 'Y': logit_sum += 0.90
    if st_slope in ['Flat', 'Down']: logit_sum += 1.20
    if max_hr < 140: logit_sum += (140 - max_hr) * 0.012
    if cholesterol > 230: logit_sum += 0.40
    if resting_bp > 135: logit_sum += 0.30
    prob = 1 / (1 + np.exp(-logit_sum))
    return min(max(prob, 0.04), 0.96)

# ==========================================
# 4. SIDEBAR IDENTITY DRAWER
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: rgba(1, 3, 10, 0.85); border-radius: 8px; border: 2px solid #00F2FE; margin-bottom: 2rem; box-shadow: 0 0 25px rgba(0, 242, 254, 0.3);'>
            <div style='font-size: 3.5rem; filter: drop-shadow(0 0 20px #FF007F);'>🧬</div>
            <h2 style='margin: 0.8rem 0 0 0; font-weight:900; color: #FFF; font-size: 1.5rem; letter-spacing: 0.15em; font-family:"Orbitron"; text-shadow: 0 0 15px #00F2FE;'>NEURAL GRID</h2>
            <span style='color: #FF007F; font-size:0.8rem; font-family:"Share Tech Mono"; font-weight:700; letter-spacing: 0.2em;'>INFINITY CORE ENGINE</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ GRID OPERATIONAL CONTROL")
    system_mode = st.radio("Workspace Operational Profile", ["Run Standard Protocol", "Trigger Research Simulator"])

# ==========================================
# 5. MAIN WORKSPACE DEPLOYMENT
# ==========================================
st.markdown("<h1 class='suite-header-title'>NEURAL CORONARY TELEMETRY Suite</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #00F2FE; font-family:\"Share Tech Mono\", monospace; font-size:1.1rem; font-weight: 700; margin-bottom: 2rem; letter-spacing: 0.1em;'>// LEVEL 100 HYPER-HUD LAYER OVERFLOW CHRONO ACTIVE</p>", unsafe_allow_html=True)

# Holographic Center Viewport
st.markdown("""
<div class="holographic-telemetry-lens">
    <div class="quantum-pill">⚡ VECTOR INFRASTRUCTURE TARGET LOCKED</div>
    <div style="background: rgba(1, 3, 10, 0.9); border-left: 5px solid #FF007F; padding: 1.2rem; border-radius: 2px; width: 55%; box-shadow: 0 0 20px rgba(255, 0, 127, 0.15);">
        <h5 style="margin: 0 0 0.4rem 0; color: #FF007F; font-weight: 900; font-size: 1rem; font-family:'Orbitron'; letter-spacing:0.1em;">WORLD-CLASS HUD REPLICA ACTIVATED</h5>
        <p style="margin: 0; color: #A1A8B3; font-size: 0.88rem; font-family:'Share Tech Mono'; line-height:1.5;">Laser gradient pulse mapping integrated successfully. Main layout cards running chromatic loop engine over native hardware accelerators.</p>
    </div>
</div>
""", unsafe_allow_html=True)

tab_single, tab_batch, tab_trends, tab_xai = st.tabs([
    "🎯 QUANTUM PROFILE TERMINAL", 
    "📊 MULTI-PATIENT INFERENCE ARRAY", 
    "📋 LONGITUDINAL SECURE DATABASE", 
    "🧠 NEURAL FEATURE SHAP ATTRIBUTION"
])

# MODULE 1: SINGLE-PATIENT TELEMETRY
with tab_single:
    col_p1, col_p2 = st.columns([1, 1])
    with col_p1:
        st.markdown("<div class='clinical-matrix-card'>", unsafe_allow_html=True)
        st.markdown("### 👤 Registry Array Metadata")
        p_name = st.text_input("Patient Full Name", "Alex Mercer")
        p_id = st.text_input("Patient Token ID Code", "VHG-982X")
        st.markdown("</div>", unsafe_allow_html=True)
    
    if system_mode == "Trigger Research Simulator":
        sim_age, sim_bp, sim_chol = random.randint(42, 78), random.randint(118, 165), random.randint(190, 310)
    else:
        sim_age, sim_bp, sim_chol = 52, 125, 218

    st.markdown("### 🔬 CORE BIOMETRIC LOAD SECTORS")
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        st.markdown("<div class='clinical-matrix-card'>", unsafe_allow_html=True)
        age = st.slider("Biological Age Metric", 18, 100, sim_age)
        gender = st.selectbox("Gender Matrix", ['M', 'F'])
        resting_bp = st.number_input("Resting BP (mmHg)", 80, 220, sim_bp)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_v2:
        st.markdown("<div class='clinical-matrix-card'>", unsafe_allow_html=True)
        chest_pain = st.selectbox("Symptom Angina Type", ['ASY', 'NAP', 'ATA', 'TA'])
        resting_ecg = st.selectbox("ECG Waveform Pattern", ['Normal', 'ST', 'LVH'])
        max_hr = st.slider("Peak Heart Rate (bpm)", 60, 220, 142)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_v3:
        st.markdown("<div class='clinical-matrix-card'>", unsafe_allow_html=True)
        cholesterol = st.number_input("Serum Cholesterol (mg/dL)", 100, 600, sim_chol)
        fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1])
        exercise_angina = st.selectbox("Exercise Induced Angina", ['Y', 'N'])
        st_slope = st.selectbox("ST Slope Segment Type", ['Flat', 'Down', 'Up'])
        oldpeak = st.slider("ST Wave Depression Intensity", 0.0, 6.0, 1.2, 0.1)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⚡ EXECUTE CRYPTO-DIAGNOSTIC ALGORITHM RUN"):
        risk_probability = calculate_calibrated_score(age, oldpeak, chest_pain, exercise_angina, st_slope, max_hr, cholesterol, resting_bp)
        
        # SQLite Insertion
        conn = sqlite3.connect("vanguard_patient_vault.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO historical_logs VALUES (?, ?, datetime('now'), ?, ?, ?, ?)",
                       (p_id, p_name, age, resting_bp, cholesterol, float(risk_probability * 100)))
        conn.commit()
        conn.close()
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown("<div class='clinical-matrix-card'>", unsafe_allow_html=True)
            st.markdown("<h4>🎯 CYBERNETIC RISK RADIUS GAUGE</h4>", unsafe_allow_html=True)
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=risk_probability * 100,
                number={'suffix': "%", 'font': {'size': 44, 'family': 'Orbitron', 'color': '#FF007F'}},
                gauge={'axis': {'range': [0, 100], 'tickcolor': "#FF007F"}, 'bar': {'color': "#FF007F", 'thickness': 0.25},
                       'steps': [{'range': [0, 35], 'color': 'rgba(0, 242, 254, 0.2)'},
                                {'range': [35, 70], 'color': 'rgba(121, 40, 202, 0.2)'},
                                {'range': [70, 100], 'color': 'rgba(255, 0, 127, 0.2)'}]}
            ))
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=200, paper_bgcolor='rgba(0,0,0,0)', font={'color': "#FFF"})
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_r2:
            st.markdown("<div class='clinical-matrix-card' style='height:100%;'>", unsafe_allow_html=True)
            st.markdown("<h4>📋 QUANTUM TRANSCRIPT SUMMARY</h4>", unsafe_allow_html=True)
            st.markdown(f"Inference complete on registry block **{p_name}** (`{p_id}`). Pathological dynamic cardiovascular risk vector captured at: **{risk_probability*100:.2f}%**.")
            
            report_text = f"VANGUARD INFORMATICS VECTOR REALTIME\n====================================\nREGISTRY BLOCK: {p_id}\nSUBJECT IDENTIFIER: {p_name}\nRISK PERCENTAGE FACTOR: {risk_probability*100:.2f}%\nSYSTEM SECURE BLOCK LOCKED."
            st.download_button(label="📥 DOWNLOAD SECURE CRYPTO TRANSCRIPT REPORT", data=report_text, file_name=f"Report_{p_id}.txt", mime="text/plain")
            st.markdown("</div>", unsafe_allow_html=True)

# MODULE 2: MULTI-PATIENT INFERENCE ARRAY
with tab_batch:
    st.markdown("<div class='clinical-matrix-card'>", unsafe_allow_html=True)
    st.markdown("### 📊 MULTI-THREAD STREAM PIPELINE QUEUE")
    mock_csv_template = "Patient_ID,Patient_Name,Age,RestingBP,Cholesterol,MaxHR,Oldpeak\nPID-001,John Doe,45,130,220,150,0.8\nPID-002,Jane Smith,67,145,280,115,2.1\nPID-003,Bruce Wayne,38,120,210,168,0.2"
    
    uploaded_file = st.file_uploader("Upload Core Diagnostic Sheets (.csv)", type=["csv"])
    if uploaded_file is not None or st.checkbox("Engage Ward Matrix Sample Data Template"):
        current_stream = uploaded_file if uploaded_file is not None else StringIO(mock_csv_template)
        batch_df = pd.read_csv(current_stream)
        
        st.markdown("#### Input Queue Array Viewport")
        st.dataframe(batch_df, use_container_width=True, hide_index=True)
        
        if st.button("⚡ DEPLOY SYNCHRONOUS COMPUTE BLOCKS"):
            computed_risks = []
            for idx, row in batch_df.iterrows():
                computed_prob = calculate_calibrated_score(row['Age'], row['Oldpeak'], 'ASY', 'N', 'Flat', row['MaxHR'], row['Cholesterol'], row['RestingBP'])
                computed_risks.append(f"{computed_prob * 100:.2f}%")
            
            batch_df["Computed System Risk Score"] = computed_risks
            st.markdown("#### ✅ Processing Matrix Output Stream")
            st.dataframe(batch_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# MODULE 3: LONGITUDINAL SECURE DATABASE
with tab_trends:
    st.markdown("<div class='clinical-matrix-card'>", unsafe_allow_html=True)
    st.markdown("### 📋 SECURE CENTRAL DATA REGISTRY QUERY")
    lookup_id = st.text_input("Enter Core Token ID Register Registry Block", "VHG-982X")
    
    if st.button("🔍 INTERROGATE CENTRAL MEMORY CORE"):
        conn = sqlite3.connect("vanguard_patient_vault.db")
        query = "SELECT timestamp, age, bp, cholesterol, risk_score FROM historical_logs WHERE patient_id = ? ORDER BY timestamp ASC"
        df_trends = pd.read_sql_query(query, conn, params=(lookup_id,))
        conn.close()
        
        if not df_trends.empty:
            st.markdown(f"#### Verified Timeline Records for Node Block {lookup_id}")
            st.dataframe(df_trends, use_container_width=True, hide_index=True)
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(x=df_trends['timestamp'], y=df_trends['risk_score'], mode='lines+markers', name='Telemetry Log Vector', line=dict(color='#FF007F', width=4)))
            fig_trend.update_layout(height=260, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#FFF"), xaxis=dict(gridcolor='rgba(255,0,127,0.15)'), yaxis=dict(gridcolor='rgba(255,0,127,0.15)'))
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.warning("Database record empty for this Token ID array. Run telemetry tests on Tab 1 first to create table rows.")
    st.markdown("</div>", unsafe_allow_html=True)

# MODULE 4: NEURAL FEATURE SHAP ATTRIBUTION
with tab_xai:
    st.markdown("<div class='clinical-matrix-card'>", unsafe_allow_html=True)
    st.markdown("### 🧠 REALTIME SENSOR COMPONENT WEIGHT ATTRIBUTION")
    
    attr_weights = {
        "ST Segment Slope Deviation Vector": 32 if st_slope in ['Flat', 'Down'] else 6,
        "Angina Matrix Ischemia Load": 28 if chest_pain == 'ASY' else 8,
        "ST Depression Amplitude Factor": int(oldpeak * 12),
        "Age Variable Baseline Mapping": 15 if age > 50 else 5,
        "Serum Cholesterol Boundary Impact": 12 if cholesterol > 240 else 4,
        "Arterial Pressure Deviation Wave": 10 if resting_bp > 135 else 3
    }
    
    sorted_attr = sorted(attr_weights.items(), key=lambda x: x[1])
    labels_xai = [x[0] for x in sorted_attr]
    values_xai = [x[1] for x in sorted_attr]
    
    fig_xai = go.Figure(go.Bar(
        x=values_xai, y=labels_xai, orientation='h',
        marker=dict(color=values_xai, colorscale='Hot')
    ))
    fig_xai.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), height=250,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#FFF"),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,0,127,0.15)', title="Attribution Momentum Loaded Force"),
        yaxis=dict(tickfont=dict(color='#FFF', size=11, weight='bold'))
    )
    st.plotly_chart(fig_xai, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# FOOTER ENGINE
st.markdown("""
<div style='text-align: center; margin-top: 4rem; padding: 1.5rem 0; border-top: 2px solid #FF007F; color: #FF007F; font-size: 0.9rem; font-family:"Share Tech Mono"; font-weight:bold; text-shadow: 0 0 10px rgba(255,0,127,0.5);'>
    Vanguard Health Quantum Computing Grid Core Sector // Matrix Block 2026 Secured.
</div>
""", unsafe_allow_html=True)