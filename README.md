
---

# 🫀 Vanguard Health AI // Coronary Telemetry Suite

## 🚀 Overview

The **Vanguard Health AI** is an enterprise-grade coronary diagnostic platform designed to bridge the gap between machine learning research and real-world hospital workflows. Unlike standard diagnostic tools, this suite features a **Cyberpunk-inspired HUD**, persistent data-archiving, and a high-precision probabilistic engine for clinical risk assessment.

## 🛠 Architectural Highlights

* **Cybernetic UI/UX:** Custom-injected glassmorphic CSS and dynamic Base64 asset rendering for an immersive enterprise-grade dashboard experience.
* **Research Simulator Engine:** Integrated Gaussian randomization to simulate clinical configurations for pipeline stress-testing and benchmarking.
* **Bulk Processing Array:** High-throughput `pandas`-based engine for batch CSV analysis, enabling multi-patient diagnostics in a single computational cycle.
* **Longitudinal Archive (SQLite):** An embedded `vanguard_patient_vault.db` engine that tracks patient trajectory, enabling historical trend analysis and clinical progress monitoring.
* **Explainable AI (XAI) Matrix:** Real-time feature attribution layer that visualizes precisely which physiological parameters are driving the risk assessment (Clinical Transparency).

## 🧠 The Math: Sigmoid Calibrated Inference

To ensure medical-grade precision, the engine utilizes **Multi-variate Logit Dynamic Interpolation**. We bypass the binary limitations of standard models by applying a custom Sigmoid activation function to generate smooth, continuous risk probability:

$$f(z) = \frac{1}{1 + e^{-z}}$$

*The system uses a **Clamping Layer** to maintain outputs between 0.04 and 0.96, ensuring clinically realistic and continuous risk analytics.*

## 📊 Model Performance

The inference engine is powered by a **Stacking Ensemble Classifier** (Decision Tree, SVM, Logistic Regression).

| Metric | Accuracy Score |
| --- | --- |
| **Training Accuracy** | **88.58%** |
| **Testing Accuracy** | **87.87%** |
| **Generalization Gap** | 0.71% |

---

## 🏗 Repository Map

* `app.py`: Main Orchestrator (Logic/UI/DB).
* `heartproj.ipynb`: Ensemble Stacking development notebook.
* `knn_heart_model.pkl`: Primary Stacking Pipeline artifact.
* `vanguard_patient_vault.db`: Persistent Patient Records Ledger.

## 📝 Pitch Summary (For Interviews/Presentation)

> "I developed an **Enterprise-Grade Coronary Telemetry Platform** that integrates dynamic ML inference with scalable healthcare operational workflows. The platform features an **Automated Batch Processing Engine** for bulk diagnostic loads, a **Persistent SQLite Ledger** for longitudinal patient tracking, and an **XAI Attribution Matrix** to provide clinicians with full transparency into model-driven decision-making."


