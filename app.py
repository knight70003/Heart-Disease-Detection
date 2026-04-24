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

# Page config
st.set_page_config(page_title="HeartGuard AI Pro", page_icon="🫀", layout="wide")

# === ULTIMATE CSS WITH PARTICLE SYSTEM & HEARTBEAT ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');

/* Animated Background with Heart Particles */
.canvas-bg {
    position: fixed; top: 0; left: 0; width: 100%; height: 100vh; 
    z-index: -1; opacity: 0.3;
}
.main { 
    position: relative; background: radial-gradient(ellipse at center, #0f2027 0%, #203a43 50%, #2c5364 100%);
    animation: pulseBg 8s ease-in-out infinite;
}
@keyframes pulseBg {
    0%, 100% { filter: hue-rotate(0deg) brightness(1); }
    50% { filter: hue-rotate(30deg) brightness(1.1); }
}

/* Heartbeat Pulse Animation */
.heartbeat {
    animation: heartbeat 1.5s ease-in-out infinite both;
}
@keyframes heartbeat {
    0% { transform: scale(1); }
    14% { transform: scale(1.1); }
    28% { transform: scale(1); }
    42% { transform: scale(1.1); }
    70% { transform: scale(1); }
}

/* Floating Cards */
.floating-card {
    animation: float 6s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Glow Effect */
.glow { 
    box-shadow: 0 0 20px rgba(255,107,107,0.5), 0 0 40px rgba(255,107,107,0.3);
    animation: glowPulse 2s ease-in-out infinite alternate;
}
@keyframes glowPulse {
    from { box-shadow: 0 0 20px rgba(255,107,107,0.5), 0 0 40px rgba(255,107,107,0.3); }
    to { box-shadow: 0 0 30px rgba(255,107,107,0.8), 0 0 60px rgba(255,107,107,0.5); }
}

/* Button Ripple Effect */
.ripple-btn {
    position: relative; overflow: hidden; border-radius: 50px;
}
.ripple-btn::before {
    content: ''; position: absolute; top: 50%; left: 50%; width: 0; height: 0;
    border-radius: 50%; background: rgba(255,255,255,0.6);
    transform: translate(-50%, -50%); transition: width 0.6s, height 0.6s;
}
.ripple-btn:active::before {
    width: 300px; height: 300px;
}

/* Glass Morphism */
.glass-card {
    background: rgba(255,255,255,0.1); backdrop-filter: blur(30px);
    border: 1px solid rgba(255,255,255,0.2); border-radius: 30px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.glass-card:hover {
    transform: translateY(-15px) scale(1.02); box-shadow: 0 40px 80px rgba(0,0,0,0.4);
}

/* Progress Ring */
.progress-ring { stroke-dasharray: 300; stroke-dashoffset: 300; transition: 1s; }

/* Typing Animation */
.typing { overflow: hidden; border-right: 3px solid #ff6b6b; 
          white-space: nowrap; animation: typing 3s steps(40) forwards, blink 0.75s infinite; }
@keyframes typing { from { width: 0; } to { width: 100%; } }
@keyframes blink { 50% { border-color: transparent; } }

/* Particle Burst */
@keyframes particleBurst {
    0% { opacity: 1; transform: scale(0) translate(0, 0); }
    50% { opacity: 0.8; transform: scale(1.2) translate(0, -10px); }
    100% { opacity: 0; transform: scale(1) translate(var(--dx), var(--dy)); }
}
.particle { position: absolute; width: 8px; height: 8px; 
            background: radial-gradient(circle, #ff6b6b, transparent);
            border-radius: 50%; animation: particleBurst 0.8s forwards; }
</style>
""", unsafe_allow_html=True)

# === PARTICLE SYSTEM HTML COMPONENT ===
particles_html = """
<div id="particles" style="position: fixed; top: 0; left: 0; width: 100%; height: 100vh; pointer-events: none; z-index: 1;">
    <canvas id="particleCanvas" class="canvas-bg"></canvas>
</div>
<script>
    const canvas = document.getElementById('particleCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const particles = [];
    for(let i = 0; i < 50; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            radius: Math.random() * 3 + 1,
            alpha: Math.random() * 0.5 + 0.2,
            hue: Math.random() * 60 + 200
        });
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            ctx.save();
            ctx.globalAlpha = p.alpha;
            ctx.translate(p.x, p.y);
            ctx.rotate(Date.now() * 0.001);
            ctx.fillStyle = `hsl(${p.hue}, 70%, 60%)`;
            ctx.beginPath();
            ctx.arc(0, 0, p.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
            
            p.x += p.vx; p.y += p.vy;
            if(p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if(p.y < 0 || p.y > canvas.height) p.vy *= -1;
        });
        requestAnimationFrame(animate);
    }
    animate();
</script>
"""
components.html(particles_html, height=0)

# === MODEL ===
@st.cache_resource
def load_model():
    model = joblib.load("knn_heart_model.pkl")
    scaler = joblib.load("heart_scaler.pkl")
    expected_columns = joblib.load("heart_columns.pkl")
    return model, scaler, expected_columns

model, scaler, expected_columns = load_model()

# === HERO WITH HEARTBEAT ===
st.markdown("""
<div style='text-align: center; padding: 4rem 2rem; position: relative; z-index: 2;'>
    <div class='glow heartbeat' style='font-size: 6rem; margin-bottom: 1rem;'>🫀</div>
    <h1 style='font-size: 4.5rem; background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #feca57);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                font-weight: 800; margin: 0; animation: rainbow 3s ease-in-out infinite;'>
        HeartGuard AI Pro
    </h1>
    <div style='font-size: 1.6rem; color: rgba(255,255,255,0.9); margin: 1rem 0;
                animation: typing 2.5s steps(40) forwards;'>
        Ultimate Cardiac Risk Intelligence
    </div>
</div>
<style>
@keyframes rainbow {
    0% { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# === ANIMATED INPUT SECTION ===
col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown("""
    <div class='glass-card floating-card animate__animated animate__fadeInLeft'>
        <h3 style='color: white; text-align: center; margin-bottom: 2rem;'>📊 Health Profile</h3>
    """, unsafe_allow_html=True)
    
    # Animated inputs
    age = st.slider("👴 Age", 18, 100, 45, help="Your chronological age")
    gender = st.selectbox("⚥ Gender", ['M', 'F'])
    chest_pain = st.selectbox("💔 Chest Pain", ['ATA','NAP','TA','ASY'])
    resting_bp = st.number_input("🩸 Blood Pressure", 80, 200, 130)
    cholesterol = st.number_input("🧪 Cholesterol", 100, 600, 240)
    fasting_bs = st.selectbox("🍬 Fasting Blood Sugar", [0, 1])
    resting_ecg = st.selectbox("📈 ECG Result", ['Normal','ST','LVH'])
    max_hr = st.slider("🏃 Max Heart Rate", 60, 220, 160)
    exercise_angina = st.selectbox("😰 Exercise Angina", ['Y','N'])
    st_slope = st.selectbox("📉 ST Slope", ['Up', 'Flat', 'Down'])
    oldpeak = st.slider("📊 ST Depression", 0.0, 6.0, 0.5, 0.1)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='glass-card floating-card animate__animated animate__fadeInRight glow'>
        <h3 style='color: white; text-align: center;'>🎯 Live AI Analysis</h3>
    """, unsafe_allow_html=True)
    
    # === ULTIMATE 3D HEARTBEAT GAUGE ===
    if 'age' in locals():
        try:
            # Live prediction
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
            risk_prob = model.predict_proba(scaled)[0][1]
            
            # 3D Animated Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=risk_prob,
                number={'font': {'size': 48, 'color': 'white', 'family': 'Inter'}},
                delta={'reference': 0.5, 'position': "top"},
                title={'text': "🫀 Cardiac Risk Score", 'font': {'size': 20, 'color': 'white'}},
                gauge={
                    'shape': "angular",
                    'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#ff4757", 'thickness': 0.25},
                    'steps': [
                        {'range': [0, 0.3], 'color': "#00d4aa"},
                        {'range': [0.3, 0.6], 'color': "#ffd23f"},
                        {'range': [0.6, 1], 'color': "#ff4757"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 6},
                        'thickness': 1,
                        'value': risk_prob
                    }
                }
            ))
            fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white'), margin=dict(l=20,r=20,t=60,b=20))
            st.plotly_chart(fig, use_container_width=True)
            
            # Animated metrics
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("🎯 AI Risk", f"{risk_prob:.1%}", delta=None)
            with col_m2:
                status = "🟢 LOW" if risk_prob < 0.3 else "🟡 MODERATE" if risk_prob < 0.6 else "🔴 HIGH"
                st.metric("🏥 Status", status)
            with col_m3:
                conf = max(model.predict_proba(scaled)[0]) * 100
                st.metric("⭐ Confidence", f"{conf:.0f}%")
                
        except:
            st.info("🎛️ Adjust sliders for live AI analysis")
    
    st.markdown("</div>", unsafe_allow_html=True)

# === EPIC PREDICTION BUTTON WITH RIPPLE & PARTICLES ===
st.markdown("""
<div style='text-align: center; padding: 3rem 0; position: relative; z-index: 10;'>
""", unsafe_allow_html=True)

if st.button("🚀 **GENERATE ULTIMATE CARDIAC REPORT**", 
             key="ultimate_predict", help="AI-Powered Medical Analysis"):
    
    # === PARTICLE EXPLOSION EFFECT ===
    st.markdown("""
    <div id="particle-container" style="position: relative; height: 100px;">
        <div class="particle" style="--dx: 100px; --dy: -50px;"></div>
        <div class="particle" style="--dx: -100px; --dy: -30px; animation-delay: 0.1s;"></div>
        <div class="particle" style="--dx: 50px; --dy: -80px; animation-delay: 0.2s;"></div>
        <div class="particle" style="--dx: -50px; --dy: 20px; animation-delay: 0.3s;"></div>
        <div class="particle" style="--dx: 80px; --dy: 40px; animation-delay: 0.4s;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress with heartbeat
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i in range(101):
        # Heartbeat progress
        pulse = 1 + 0.1 * math.sin(i * 0.3)
        progress_bar.progress(i / 100)
        status_text.markdown(f"""
        <div style='text-align: center; color: #ff6b6b; font-size: 1.2rem;'>
            🔬 AI Analysis {i}% <span style='animation: heartbeat 0.5s infinite;'>❤️</span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.03)
    
    # === SPECTACULAR RESULTS ===
    st.balloons()
    st.snow()
    
    st.markdown("""
    <div class='glass-card glow heartbeat animate__animated animate__zoomIn'>
        <div style='text-align: center; padding: 3rem;'>
    """, unsafe_allow_html=True)
    
    prediction = model.predict(scaled)[0]
    if prediction == 1:
        st.markdown("""
            <h2 style='color: #ff4757; font-size: 3rem; margin: 0;'>🚨 CRITICAL ALERT</h2>
            <p style='font-size: 1.5rem; color: rgba(255,255,255,0.9);'>
                High Risk of Cardiac Event Detected
            </p>
        """, unsafe_allow_html=True)
        st.error(f"🎯 **Risk Probability: {risk_prob:.1%}**")
    else:
        st.markdown("""
            <h2 style='color: #00d4aa; font-size: 3rem; margin: 0;'>✅ OPTIMAL HEALTH</h2>
            <p style='font-size: 1.5rem; color: rgba(255,255,255,0.9);'>
                Excellent Cardiovascular Profile
            </p>
        """, unsafe_allow_html=True)
        st.success(f"🎯 **Risk Probability: {risk_prob:.1%}**")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# === ANIMATED RECOMMENDATIONS ===
st.markdown("""
<div class='glass-card floating-card animate__animated animate__fadeInUp'>
    <h3 style='color: white; text-align: center;'>💡 AI-Powered Action Plan</h3>
""", unsafe_allow_html=True)

if 'risk_prob' in locals():
    recs = {
        'high': ['🏥 Emergency cardiologist consultation', '💊 Medication review required', 
                '🚫 Avoid physical exertion', '🍎 Strict cardiac diet'],
        'medium': ['📞 Schedule checkup', '🥗 Optimize nutrition', '🏃 Moderate exercise', 
                  '💤 Improve sleep quality'],
        'low': ['✅ Maintain current lifestyle', '🏆 Excellent health metrics', 
               '📈 Continue monitoring', '🥗 Balanced nutrition']
    }
    
    risk_level = 'high' if risk_prob > 0.6 else 'medium' if risk_prob > 0.3 else 'low'
    for i, rec in enumerate(recs[risk_level]):
        st.markdown(f"""
        <div style='animation-delay: {i * 0.5}s; animation: fadeInUp 0.5s ease forwards; opacity: 0;'>
            <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); margin: 0.5rem 0;'>{rec}</p>
        </div>
        """, unsafe_allow_html=True)
        