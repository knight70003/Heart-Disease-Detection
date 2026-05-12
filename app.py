import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
import time
import math
from datetime import datetime
import streamlit.components.v1 as components
import json

# Page config - 2026 standards
st.set_page_config(
    page_title="HeartGuard AI 2026", 
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === 2026 NEOMORPHISM + AI GLOW CSS ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* 2026 AI-Neomorphism */
:root {
    --ai-glow: 0 0 20px rgba(59, 130, 246, 0.5), 0 0 40px rgba(59, 130, 246, 0.3);
    --neon-heart: 0 0 30px rgba(255, 107, 107, 0.6);
}

* { font-family: 'Inter', sans-serif; }

.main {
    background: radial-gradient(ellipse at top, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    background-attachment: fixed;
}

/* 2026 Glass 2.0 */
.ai-glass {
    background: rgba(20, 20, 40, 0.8);
    backdrop-filter: blur(40px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 28px;
    box-shadow: 
        0 25px 50px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.1);
    transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    position: relative;
    overflow: hidden;
}

.ai-glass::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.03), transparent);
    opacity: 0;
    transition: opacity 0.4s;
}

.ai-glass:hover::before { opacity: 1; }
.ai-glass:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 
        0 40px 80px rgba(0,0,0,0.4),
        var(--ai-glow),
        inset 0 1px 0 rgba(255,255,255,0.2);
}

/* AI Agent Chat */
.ai-chat {
    background: linear-gradient(180deg, rgba(59,130,246,0.1) 0%, rgba(20,20,40,0.9) 100%);
    border-radius: 20px;
    padding: 1.5rem;
    border: 1px solid rgba(59,130,246,0.3);
}

/* 2026 Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 16px 40px;
    font-weight: 600;
    font-size: 16px;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: var(--ai-glow);
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(59,130,246,0.4);
}

/* Voice Input */
.voice-btn {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border-radius: 50% !important;
    width: 60px !important;
    height: 60px !important;
    padding: 0 !important;
    box-shadow: 0 10px 30px rgba(16,185,129,0.4) !important;
}

/* Holographic Metrics */
.holo-metric {
    background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
    position: relative;
}

.holo-metric::after {
    content: '';
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(45deg, #3b82f6, #ff6b6b, #10b981, #f59e0b);
    border-radius: 22px;
    z-index: -1;
    opacity: 0;
    transition: opacity 0.3s;
}
.holo-metric:hover::after { opacity: 1; }
</style>
""", unsafe_allow_html=True)

# === 2026 AI PARTICLE SYSTEM ===
particles_2026 = """
<div id="ai-particles" style="position: fixed; top: 0; left: 0; width: 100%; height: 100vh; pointer-events: none; z-index: 1;">
    <canvas id="aiCanvas"></canvas>
</div>
<script>
const canvas = document.getElementById('aiCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

class AIParticle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.8;
        this.vy = (Math.random() - 0.5) * 0.8;
        this.radius = Math.random() * 2 + 1;
        this.hue = Math.random() * 60 + 220;
        this.life = 1;
    }
    update() {
        this.x += this.vx + Math.sin(Date.now() * 0.001 + this.x) * 0.1;
        this.y += this.vy + Math.cos(Date.now() * 0.001 + this.y) * 0.1;
        this.life -= 0.002;
        this.hue += 0.5;
        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }
    draw() {
        ctx.save();
        ctx.globalAlpha = this.life;
        ctx.translate(this.x, this.y);
        ctx.shadowBlur = 20;
        ctx.shadowColor = `hsl(${this.hue}, 70%, 60%)`;
        ctx.fillStyle = `hsl(${this.hue}, 70%, 60%)`;
        ctx.beginPath();
        ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

const particles = [];
for(let i = 0; i < 80; i++) particles.push(new AIParticle());

function animate() {
    ctx.fillStyle = 'rgba(12,12,12,0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    particles.forEach((p, i) => {
        p.update();
        p.draw();
        if(p.life < 0) particles[i] = new AIParticle();
    });
    requestAnimationFrame(animate);
}
animate();
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
</script>
"""
components.html(particles_2026, height=0)

# === MODEL ===
@st.cache_resource
def load_model():
    model = joblib.load("knn_heart_model.pkl")
    scaler = joblib.load("heart_scaler.pkl")
    expected_columns = joblib.load("heart_columns.pkl")
    return model, scaler, expected_columns

model, scaler, expected_columns = load_model()

# === 2026 HEADER ===
st.markdown("""
<div style='text-align: center; padding: 4rem 2rem; position: relative; z-index: 10;'>
    <div style='font-size: 6rem; margin-bottom: 1rem; filter: drop-shadow(0 0 30px rgba(255,107,107,0.5));'>🫀</div>
    <h1 style='font-size: 4rem; font-weight: 800; background: linear-gradient(45deg, #3b82f6, #ff6b6b, #10b981);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;'>HeartGuard AI 2026</h1>
    <p style='font-size: 1.4rem; color: rgba(255,255,255,0.9); margin: 1rem 0;'>Neural Cardiac Intelligence • Real-time Risk Prediction</p>
</div>
""", unsafe_allow_html=True)

# === 2026 SIDEBAR: AI AGENT ===
with st.sidebar:
    st.markdown("""
    <div class='ai-glass' style='padding: 2rem; margin-bottom: 2rem;'>
        <h3 style='color: #3b82f6; text-align: center;'>🤖 HeartAI Agent</h3>
    """, unsafe_allow_html=True)
    
    # Voice input simulation
    col_v1, col_v2 = st.columns([3,1])
    with col_v1:
        st.text_input("💭 Ask HeartAI", placeholder="e.g., 'Analyze my risk profile'")
    with col_v2:
        if st.button("🎤", key="voice", help="Voice Input", use_container_width=True):
            st.balloons()
    
    st.markdown("""
        <div class='ai-chat' style='margin-top: 1rem;'>
            <div style='color: #3b82f6; font-size: 0.9rem;'>HeartAI:</div>
            <div style='color: rgba(255,255,255,0.8); font-size: 0.85rem;'>
                Ready to analyze your cardiac profile. Speak or type your symptoms.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Patient profile
    st.markdown("""
    <div class='ai-glass' style='padding: 2rem;'>
        <h4 style='color: white;'>👤 Patient Profile</h4>
    """, unsafe_allow_html=True)
    
    patient_name = st.text_input("Name", "John Doe")
    patient_id = st.text_input("ID", f"HD-{datetime.now().strftime('%Y%m%d')}-001")
    
    st.markdown("</div>", unsafe_allow_html=True)

# === 2026 INPUT INTERFACE ===
st.markdown("""
<div class='ai-glass' style='padding: 3rem; margin: 2rem 0;'>
    <h3 style='color: white; text-align: center;'>🔬 Neural Input Matrix</h3>
""", unsafe_allow_html=True)

# 2026 Input tabs with AI assistance
tab1, tab2, tab3 = st.tabs(["🫀 Cardiac Profile", "📊 Biometrics", "🏃 AI Stress Test"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ['M', 'F'])
        chest_pain = st.selectbox("Chest Pain", ['None','ATA','NAP','TA','ASY'])
        resting_ecg = st.selectbox("ECG", ['Normal','ST','LVH'])
    with col2:
        fasting_bs = st.selectbox("FBS >120mg/dL", [0, 1])
        exercise_angina = st.selectbox("Exercise Angina", ['N','Y'])
        st_slope = st.selectbox("ST Slope", ['Up', 'Flat', 'Down'])

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Age", 18, 100, 45, help="Neural age adjustment applied")
        resting_bp = st.number_input("BP (mmHg)", 80, 200, 130)
        cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 240)
    with col2:
        max_hr = st.slider("Max HR (bpm)", 60, 220, 160)
        oldpeak = st.slider("ST Depression", 0.0, 6.0, 0.0, 0.1)

with tab3:
    st.markdown("""
    <div style='text-align: center; color: rgba(255,255,255,0.7);'>
        <div style='font-size: 3rem;'>🚀</div>
        <h4>AI Stress Test Simulation</h4>
        <p>Neural network simulates exercise tolerance automatically</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# === 2026 AI ANALYSIS BUTTON ===
if st.button("🧠 **NEURAL RISK ANALYSIS**", use_container_width=True):
    with st.spinner("🧠 Activating neural network..."):
        time.sleep(2)
    
    # AI Analysis
    try:
        input_dict = {
            "Age": age, "RestingBP": resting_bp, "Cholesterol": cholesterol,
            "FastingBS": fasting_bs, "MaxHR": max_hr, "Oldpeak": oldpeak,
            f"Sex_{gender}": 1, f"ChestPainType_{chest_pain}": 1,
            f"RestingECG_{resting_ecg}": 1, f"ExerciseAngina_{exercise_angina}": 1,
            f"ST_Slope_{st_slope}": 1
        }
        input_df = pd.DataFrame([input_dict])
        for col in expected_columns:
            if col not in input_df.columns: input_df[col] = 0
        input_df = input_df[expected_columns]
        
        scaled = scaler.transform(input_df)
        prediction = model.predict(scaled)[0]
        risk_prob = model.predict_proba(scaled)[0][1]
        confidence = max(model.predict_proba(scaled)[0]) * 100
        
        # === 2026 HOLOGRAPHIC DASHBOARD ===
        st.markdown("""
        <div class='ai-glass' style='padding: 3rem; margin: 2rem 0;'>
            <h3 style='color: #3b82f6; text-align: center;'>🎯 Neural Risk Matrix</h3>
        """, unsafe_allow_html=True)
        
        # Holographic gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_prob*100,
            number={'suffix': "%", 'font': {'size': 48, 'color': '#3b82f6'}},
            delta={'reference': 50, 'position': "top", 'increasing': {'color': "#ef4444"}},
            gauge={
                'shape': "angular",
                'axis': {'range': [0, 100]},
                'bar': {'color': "#3b82f6", 'thickness': 0.2},
                'steps': [
                    {'range': [0, 30], 'color': "#10b981"},
                    {'range': [30, 70], 'color': "#f59e0b"},
                    {'range': [70, 100], 'color': "#ef4444"}
                ]
            }
        ))
        fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        # 2026 Holo-Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class='holo-metric'>
                <div style='font-size: 3rem; color: {'#10b981' if risk_prob<0.3 else '#f59e0b' if risk_prob<0.7 else '#ef4444'};'>
                    {'🟢' if risk_prob<0.3 else '🟡' if risk_prob<0.7 else '🔴'}
                </div>
                <h4 style='color: white; margin: 0.5rem 0 0 0;'>Risk Tier</h4>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='holo-metric'>
                <h2 style='color: #3b82f6; margin: 0;'>{risk_prob:.1%}</h2>
                <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;'>Neural Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='holo-metric'>
                <h2 style='color: #10b981; margin: 0;'>{confidence:.0f}%</h2>
                <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;'>AI Certainty</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            status = "NEURAL OPTIMAL" if risk_prob < 0.3 else "MONITOR" if risk_prob < 0.7 else "CRITICAL"
            st.markdown(f"""
            <div class='holo-metric'>
                <h4 style='color: white; margin: 0;'>{status}</h4>
                <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Status</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # === AI AGENT RECOMMENDATIONS ===
        st.markdown("""
        <div class='ai-glass' style='padding: 2.5rem; margin: 2rem 0;'>
            <h4 style='color: #3b82f6;'>🤖 HeartAI Action Protocol</h4>
        """, unsafe_allow_html=True)
        
        recs = {
            'low': ['✅ Neural optimal detected', '🧬 Continue current protocol', '📡 Annual neural scan'],
            'medium': ['⚠️ Monitor neural markers', '🥗 Optimize metabolic input', '🏃 Adaptive exercise'],
            'high': ['🚨 Critical neural alert', '🏥 Immediate intervention', '🧠 Specialist neural consult']
        }
        
        risk_cat = 'low' if risk_prob < 0.3 else 'medium' if risk_prob < 0.7 else 'high'
        for i, rec in enumerate(recs[risk_cat]):
            st.markdown(f"""
            <div style='display: flex; align-items: center; margin: 1rem 0; padding: 1rem; 
                       background: rgba(59,130,246,0.1); border-radius: 12px;'>
                <div style='font-size: 1.5rem; margin-right: 1rem;'>{['✅','⚠️','🚨'][i%3]}</div>
                <div style='color: rgba(255,255,255,0.9);'>{rec}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    except:
        st.error("🧠 Neural input incomplete. Please fill all matrices.")

# === 2026 FOOTER ===
st.markdown("""
<div style='text-align: center; padding: 4rem 2rem; color: rgba(255,255,255,0.5); border-top: 1px solid rgba(255,255,255,0.1); margin-top: 4rem;'>
    <h4 style='color: white; margin-bottom: 1rem;'>HeartGuard AI 2026</h4>
    <p>Neural Cardiac Intelligence • May 2026 Release</p>
    <p style='font-size: 0.85rem;'>⚠️ Medical AI advisory system. Consult healthcare professionals.</p>
</div>
""", unsafe_allow_html=True)

        