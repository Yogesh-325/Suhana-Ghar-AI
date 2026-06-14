# 🏠 SuhanaGhar AI
### Climate-Responsive Smart Housing Recommendation System for India

**Paper ID:** SG-AI-2026-001 | **Category:** Sustainable AI & Smart Construction

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![ML](https://img.shields.io/badge/Model-Random%20Forest-orange.svg)](https://scikit-learn.org/)

---

## 🌍 Overview
**SuhanaGhar AI** is an intelligent recommendation engine designed to optimize residential architecture for the Indian climate. In a country where cooling accounts for a massive portion of domestic energy consumption, this tool helps homeowners and architects design buildings that stay naturally cooler.

By analyzing building geometry, glazing distributions, and cardinal orientation, the system predicts energy loads and provides **Explainable AI (XAI)** suggestions to reduce reliance on mechanical cooling (HVAC) systems.

---

## 🚀 Key Features

### 1. ⚡ Dual-Mode Analysis
* **Simple Mode:** Quick estimation for homeowners based on house size, window count, and general sunlight exposure levels.
* **AI Energy Analysis:** Professional-grade prediction using 8+ architectural parameters to calculate exact thermal loads.

### 2. 🔥 Thermal Load Prediction
Predicts **Heating Load** and **Cooling Load** (kWh) using a trained **Random Forest Regressor**. This allows users to see the "hidden" energy cost of their design before construction begins.

### 3. 🧠 Smart Design Advisor
A logic-based recommendation engine that evaluates the "Energy Efficiency Score" of a plan. It provides specific passive-cooling strategies:
* Optimal window-to-wall ratios to prevent heat traps.
* Material suggestions for walls and roofs based on surface area.
* Shading device placements based on building orientation.

### 4. 📊 Interactive Visualizations
* **Load Distribution Charts:** Compare heating vs. cooling needs in real-time.
* **Feature Sensitivity:** Visual feedback on how changing one variable (like Glazing Area) affects the total efficiency score.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Interactive Web Dashboard)
* **Machine Learning:** Scikit-Learn (Random Forest & Decision Trees)
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly, Matplotlib

---

## 📖 Parameter Guide

| Parameter | Impact on Indian Context |
| :--- | :--- |
| **Relative Compactness** | Higher compactness reduces the surface area exposed to external heat. |
| **Surface/Wall Area** | Determines the total building "skin" exposed to solar radiation. |
| **Glazing Area** | Critical for tropical zones; high glazing often leads to a "Greenhouse Effect." |
| **Orientation** | Essential for managing the harsh South-West afternoon sun in India. |
| **Glazing Distribution** | Affects natural cross-ventilation and uniform internal daylighting. |

---

## 📦 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Yogesh-325/SuhanaGhar-AI.git](https://github.com/Yogesh-325/SuhanaGhar-AI.git)
   cd SuhanaGhar-AI

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Run the App:**
   ```bash
   streamlit run app.py  

## 📂 Project Structure

SuhanaGhar-AI/
├── app.py                # Main Streamlit UI application
├── train_model.py        # ML training and evaluation script
├── recommender.py        # Logic for the Smart Design Advisor
├── dataset.csv           # Building Energy Efficiency Dataset
├── model.pkl             # Serialized ML model
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation

## 👥 Authors
- Yogesh Pawar
- Vinay Patel
- Yash Kumar Patle

## 🎯 Future Roadmap

* 🌐 Live Weather API: Automatically fetch climate data based on the user's city.
* 🏗️ 3D Visualization: Integrate a 3D viewer to visualize building massing.
* 🏙️ City-Specific Datasets: Fine-tune models for diverse Indian climatic zones (Coastal, Arid, Hilly).

## ⭐ Final Note

**SuhanaGhar AI aims to democratize sustainable architecture. By putting AI in the hands of users, we can build a greener, cooler India, one home at a time.**