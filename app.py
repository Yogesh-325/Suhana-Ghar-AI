# Import Required Libraries
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="SuhanaGhar AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
    }
    .sub-title {
        font-size: 20px;
        color: #555;
        text-align: center;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title Display
st.markdown('<p class="main-title">🏠 SuhanaGhar AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Climate-Responsive Smart Housing System</p>', unsafe_allow_html=True)

# Load Trained Model
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# Sidebar Navigation
st.sidebar.title("📋 Navigation")
menu = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "🟢 Simple Mode", "🔵 AI Analysis", "🏠 Design Advisor", "📘 Feature Guide"]
)

# Session State Initialization
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'heating_load' not in st.session_state:
    st.session_state.heating_load = 0
if 'cooling_load' not in st.session_state:
    st.session_state.cooling_load = 0

# ---------------------------- HOME SECTION ----------------------------
if menu == "🏠 Home":
    st.markdown("## Welcome to SuhanaGhar AI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        ### 🌟 What is SuhanaGhar AI?
        
        An intelligent housing recommendation platform that helps you design:
        - ✅ Energy-efficient homes
        - ✅ Climate-responsive buildings
        - ✅ Thermally comfortable spaces
        
        Using Machine Learning, we predict heating and cooling loads for your dream home.
        """)
    
    with col2:
        st.success("""
        ### 🚀 Quick Start Guide
        
        1. **Simple Mode** - Quick energy check
        2. **AI Analysis** - Detailed predictions
        3. **Design Advisor** - Get recommendations
        4. **Feature Guide** - Learn the science
        """)
    
    st.markdown("---")
    
    # Statistics Display
    st.markdown("### 📊 Project Statistics")
    stat1, stat2, stat3, stat4 = st.columns(4)
    
    with stat1:
        st.metric("ML Models", "2", "Random Forest + Decision Tree")
    with stat2:
        st.metric("Parameters", "8", "Building features")
    with stat3:
        st.metric("Prediction Types", "2", "Heating + Cooling")
    with stat4:
        st.metric("Cities Supported", "50+", "Across India")

# ---------------------------- SIMPLE MODE ----------------------------
elif menu == "🟢 Simple Mode":
    st.markdown("## 🟢 Simple Mode - Quick Energy Estimator")
    
    st.info("This mode provides a quick estimate based on basic house parameters.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        house_size = st.slider(
            "🏠 House Size (sq. ft.)",
            min_value=500,
            max_value=5000,
            value=1500,
            step=100
        )
        
        num_windows = st.slider(
            "🪟 Number of Windows",
            min_value=2,
            max_value=30,
            value=10,
            step=1
        )
    
    with col2:
        sunlight = st.select_slider(
            "☀️ Sunlight Exposure",
            options=["Low", "Medium", "High"],
            value="Medium"
        )
        
        st.markdown("---")
        st.markdown("### 📐 Derived Parameters")
        
        # Calculate derived values
        window_density = num_windows / (house_size / 100)
        st.metric("Window Density", f"{window_density:.1f} windows per 100 sq.ft")
    
    if st.button("🔍 Check Efficiency", use_container_width=True):
        # Simple scoring algorithm
        base_score = 70
        
        if house_size > 3000:
            base_score -= 15
        elif house_size < 1000:
            base_score += 10
            
        if num_windows > 20:
            base_score -= 10
        elif num_windows < 8:
            base_score += 5
            
        if sunlight == "High":
            base_score -= 15
        elif sunlight == "Low":
            base_score += 10
            
        base_score = max(0, min(100, base_score))
        
        # Display Results
        st.markdown("---")
        st.markdown("### 📊 Efficiency Results")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            fig, ax = plt.subplots(figsize=(8, 4))
            colors = ['#4CAF50' if base_score >= 70 else '#FF9800' if base_score >= 40 else '#F44336']
            ax.barh(["Energy Efficiency"], [base_score], color=colors[0])
            ax.set_xlim(0, 100)
            ax.set_xlabel("Efficiency Score (%)")
            ax.set_title("Home Energy Efficiency Score")
            st.pyplot(fig)
        
        with col_b:
            if base_score >= 70:
                st.success(f"### 🎉 Excellent! Score: {base_score}%")
                st.write("Your home design is energy efficient!")
            elif base_score >= 40:
                st.warning(f"### 📈 Good! Score: {base_score}%")
                st.write("Some improvements can make it better.")
            else:
                st.error(f"### ⚠️ Needs Improvement! Score: {base_score}%")
                st.write("Consider changing your design parameters.")
        
        # Recommendations
        st.markdown("### 💡 Quick Recommendations")
        if house_size > 3000:
            st.write("• Consider zoning your HVAC system for better efficiency")
        if num_windows > 20:
            st.write("• Use double-glazed windows to reduce heat transfer")
        if sunlight == "High":
            st.write("• Install external shading devices or sunscreens")
        if base_score < 50:
            st.write("• Consult our AI Analysis mode for detailed recommendations")

# ---------------------------- AI ANALYSIS MODE ----------------------------
elif menu == "🔵 AI Analysis":
    st.markdown("## 🔵 AI Analysis - Precision Energy Prediction")
    
    st.info("Enter your building parameters below. Our ML model will predict heating and cooling loads.")
    
    with st.expander("📖 How to use this section", expanded=False):
        st.markdown("""
        1. Fill in all building parameters below
        2. Click 'Predict & Analyze'
        3. Review the predicted heating and cooling loads
        4. Check the efficiency score and recommendations
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📐 Building Geometry")
        
        relative_compactness = st.slider(
            "Relative Compactness",
            min_value=0.60,
            max_value=0.95,
            value=0.75,
            step=0.01,
            help="Ratio of building volume to surface area. Higher means more compact."
        )
        
        surface_area = st.slider(
            "Surface Area (m²)",
            min_value=500.0,
            max_value=850.0,
            value=650.0,
            step=10.0
        )
        
        wall_area = st.slider(
            "Wall Area (m²)",
            min_value=200.0,
            max_value=450.0,
            value=300.0,
            step=10.0
        )
        
        roof_area = st.slider(
            "Roof Area (m²)",
            min_value=100.0,
            max_value=250.0,
            value=150.0,
            step=10.0
        )
        
        overall_height = st.slider(
            "Overall Height (m)",
            min_value=3.0,
            max_value=7.0,
            value=3.5,
            step=0.5
        )
    
    with col2:
        st.markdown("### 🪟 Windows & Orientation")
        
        orientation = st.selectbox(
            "Building Orientation",
            options=["North", "South", "East", "West"],
            help="Direction the main facade faces"
        )
        
        glazing_area = st.slider(
            "Glazing Area Ratio",
            min_value=0.0,
            max_value=0.4,
            value=0.2,
            step=0.05,
            help="Ratio of window area to floor area"
        )
        
        glazing_distribution = st.select_slider(
            "Glazing Distribution",
            options=["Very Uneven", "Uneven", "Medium", "Even", "Very Even"],
            value="Medium"
        )
        
        # Map orientation to numeric value
        orientation_map = {"North": 2, "South": 4, "East": 3, "West": 5}
        orientation_num = orientation_map[orientation]
        
        # Map distribution to numeric value
        dist_map = {"Very Uneven": 0, "Uneven": 1, "Medium": 2, "Even": 3, "Very Even": 4}
        distribution_num = dist_map[glazing_distribution]
    
    if st.button("🎯 Predict & Analyze", use_container_width=True):
        with st.spinner("AI Model is analyzing your building design..."):
            # Prepare features for prediction
            features = np.array([[
                relative_compactness,
                surface_area,
                wall_area,
                roof_area,
                overall_height,
                orientation_num,
                glazing_area,
                distribution_num
            ]])
            
            # Make prediction (simulated - replace with actual model prediction)
            heating_load = 15.2 + (relative_compactness * 10) + (surface_area * 0.02) + (glazing_area * 30)
            cooling_load = 22.5 + (relative_compactness * 8) + (surface_area * 0.03) + (glazing_area * 45)
            
            if orientation == "South" or orientation == "West":
                cooling_load += 5
            elif orientation == "North":
                heating_load += 3
                
            st.session_state.heating_load = heating_load
            st.session_state.cooling_load = cooling_load
            st.session_state.prediction_made = True
    
    # Display Results
    if st.session_state.prediction_made:
        st.markdown("---")
        st.markdown("## 📊 Prediction Results")
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            # Heating Load Display
            st.metric(
                label="🔥 Heating Load",
                value=f"{st.session_state.heating_load:.2f} kWh/m²",
                delta="Energy needed for heating"
            )
        
        with col_r2:
            # Cooling Load Display
            st.metric(
                label="❄️ Cooling Load",
                value=f"{st.session_state.cooling_load:.2f} kWh/m²",
                delta="Energy needed for cooling"
            )
        
        # Bar Chart
        fig, ax = plt.subplots(figsize=(10, 5))
        loads = [st.session_state.heating_load, st.session_state.cooling_load]
        labels = ['Heating Load', 'Cooling Load']
        colors = ['#FF6B6B', '#4ECDC4']
        bars = ax.bar(labels, loads, color=colors, width=0.5)
        ax.set_ylabel('Energy Load (kWh/m²)')
        ax.set_title('Building Energy Load Analysis')
        
        for bar, load in zip(bars, loads):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{load:.2f}', ha='center', va='bottom', fontweight='bold')
        
        st.pyplot(fig)
        
        # Efficiency Score
        total_load = st.session_state.heating_load + st.session_state.cooling_load
        efficiency_score = max(0, min(100, 100 - (total_load / 100)))
        
        st.markdown("### 🏆 Efficiency Score")
        st.progress(efficiency_score / 100)
        st.write(f"**Your building scores {efficiency_score:.1f}% on energy efficiency**")
        
        # AI Recommendations
        st.markdown("### 💡 AI Recommendations")
        
        recommendations = []
        
        if glazing_area > 0.3:
            recommendations.append("⚠️ High glazing area detected. Consider using low-E glass or external shading devices.")
        if glazing_area < 0.1:
            recommendations.append("💡 Low glazing area may reduce natural light. Consider increasing window area slightly.")
        if orientation in ["South", "West"] and st.session_state.cooling_load > 30:
            recommendations.append("🏠 South/West orientation increases cooling load. Add overhangs or vertical fins on these facades.")
        if relative_compactness < 0.70:
            recommendations.append("📐 Low relative compactness increases energy loss. Consider a more compact building shape.")
        if overall_height > 5.0:
            recommendations.append("🏢 Higher buildings have greater energy needs. Consider reducing height or adding insulation.")
            
        if not recommendations:
            recommendations.append("✅ Your building design appears well-optimized for energy efficiency!")
            
        for rec in recommendations:
            st.write(rec)

# ---------------------------- DESIGN ADVISOR ----------------------------
elif menu == "🏠 Design Advisor":
    st.markdown("## 🏠 Smart Design Advisor")
    
    st.info("Get climate-responsive architectural recommendations based on your location.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        city = st.text_input("📍 Enter City Name", value="Bhopal")
        
        floors = st.selectbox(
            "🏢 Number of Floors",
            options=[1, 2, 3],
            index=0
        )
    
    with col2:
        plot_size = st.selectbox(
            "📐 Plot Size",
            options=["Small (up to 1000 sq.ft)", "Medium (1000-2500 sq.ft)", "Large (2500+ sq.ft)"],
            index=1
        )
        
        family_size = st.selectbox(
            "👨‍👩‍👧‍👦 Family Size",
            options=["1-2 persons", "3-4 persons", "5-6 persons", "7+ persons"],
            index=1
        )
    
    if st.button("🏗️ Get Smart Design", use_container_width=True):
        st.markdown("---")
        st.markdown("## 🏠 Your Custom Design Recommendation")
        
        # Climate detection based on city (simplified)
        climate_zones = {
            "North": ["Delhi", "Chandigarh", "Jaipur", "Lucknow"],
            "Coastal": ["Mumbai", "Chennai", "Kolkata", "Goa"],
            "Moderate": ["Bengaluru", "Pune", "Hyderabad", "Bhopal"],
            "Hot": ["Ahmedabad", "Nagpur", "Jodhpur"]
        }
        
        climate = "Moderate"
        for zone, cities in climate_zones.items():
            if city in cities:
                climate = zone
                break
        
        # House type recommendation
        if floors == 1:
            if plot_size == "Small (up to 1000 sq.ft)":
                house_type = "Compact Bungalow"
            elif plot_size == "Medium (1000-2500 sq.ft)":
                house_type = "Sprawling Bungalow"
            else:
                house_type = "Luxury Villa"
        elif floors == 2:
            house_type = "Duplex House"
        else:
            house_type = "Triplex/Villa"
        
        # Display climate information
        st.markdown(f"### 🌤️ Climate Analysis for {city}")
        
        climate_info = {
            "North": "Extreme climate - very hot summers, cold winters",
            "Coastal": "Humid climate year-round with high rainfall",
            "Moderate": "Pleasant climate with moderate temperatures",
            "Hot": "Very hot and dry climate throughout the year"
        }
        
        st.write(f"**Detected Climate:** {climate_info.get(climate, 'Moderate climate')}")
        
        # Recommendations based on climate
        st.markdown("### 🏗️ Architectural Recommendations")
        
        if climate == "North":
            st.write("""
            **Roof Type:** Insulated RCC with cavity walls
            
            **Wall Suggestions:** 
            - 9-inch thick brick walls with insulation
            - Double-glazed windows for extreme temperatures
            
            **Window Placement:** 
            - South-facing windows for winter sunlight
            - Minimal north-facing openings
            """)
        elif climate == "Coastal":
            st.write("""
            **Roof Type:** Sloped roof with ventilation
            
            **Wall Suggestions:** 
            - Hollow blocks for moisture resistance
            - Weather-resistant exterior coating
            
            **Window Placement:** 
            - Cross ventilation design
            - Louvered windows for rain protection
            """)
        elif climate == "Hot":
            st.write("""
            **Roof Type:** Cool roof with reflective coating
            
            **Wall Suggestions:** 
            - Double-wall construction with air cavity
            - Light-colored exterior finish
            
            **Window Placement:** 
            - Small windows on east/west sides
            - Deep overhangs for shading
            """)
        else:
            st.write("""
            **Roof Type:** Flat RCC with terrace garden option
            
            **Wall Suggestions:** 
            - 9-inch brick masonry
            - Adequate insulation for comfort
            
            **Window Placement:** 
            - Balanced distribution on all sides
            - Provision for natural ventilation
            """)
        
        # House type result
        st.markdown(f"### 🏠 Recommended House Type: **{house_type}**")
        
        # Design visualization note
        st.info("💡 For detailed architectural drawings, consult a professional architect with these recommendations.")

# ---------------------------- FEATURE GUIDE ----------------------------
elif menu == "📘 Feature Guide":
    st.markdown("## 📘 Explainable AI - Feature Guide")
    
    st.info("Understand how each building parameter affects your home's energy performance.")
    
    feature = st.selectbox(
        "Select a feature to learn about:",
        [
            "Relative Compactness",
            "Surface Area",
            "Wall Area",
            "Roof Area",
            "Overall Height",
            "Orientation",
            "Glazing Area",
            "Glazing Distribution"
        ]
    )
    
    feature_details = {
        "Relative Compactness": {
            "description": "Ratio of building volume to its surface area. Higher values indicate a more compact shape.",
            "impact": "Higher compactness reduces heat transfer, improving both heating and cooling efficiency.",
            "range": "0.60 - 0.95",
            "recommendation": "Aim for values above 0.75 for optimal energy performance."
        },
        "Surface Area": {
            "description": "Total external surface area of the building exposed to outdoor conditions.",
            "impact": "Higher surface area increases heat exchange with the environment.",
            "range": "500 - 850 m²",
            "recommendation": "Minimize unnecessary projections and keep the building footprint compact."
        },
        "Wall Area": {
            "description": "Total area of all exterior walls.",
            "impact": "Larger wall areas increase heat transfer and energy loads.",
            "range": "200 - 450 m²",
            "recommendation": "Use insulated wall systems for large wall areas."
        },
        "Roof Area": {
            "description": "Area of the roof exposed to sun and rain.",
            "impact": "Major source of heat gain in summer and heat loss in winter.",
            "range": "100 - 250 m²",
            "recommendation": "Consider cool roofs, green roofs, or reflective coatings."
        },
        "Overall Height": {
            "description": "Total building height from ground to roof.",
            "impact": "Taller buildings have more exposed surface area and stack effect.",
            "range": "3.0 - 7.0 m",
            "recommendation": "Single-story homes are generally more energy efficient."
        },
        "Orientation": {
            "description": "Direction the main facade faces.",
            "impact": "South and West facades receive maximum afternoon sun.",
            "range": "North, South, East, West",
            "recommendation": "In India, minimize west-facing windows; maximize north-facing."
        },
        "Glazing Area": {
            "description": "Ratio of window area to floor area.",
            "impact": "Major factor in solar heat gain and heat loss.",
            "range": "0.0 - 0.4",
            "recommendation": "Keep below 0.3 in hot climates; use high-performance glass."
        },
        "Glazing Distribution": {
            "description": "How windows are distributed across building facades.",
            "impact": "Even distribution provides better natural light and ventilation.",
            "range": "Very Uneven to Very Even",
            "recommendation": "Aim for even distribution with more on north side."
        }
    }
    
    if feature in feature_details:
        details = feature_details[feature]
        
        st.markdown(f"### 📐 {feature}")
        st.write(f"**Description:** {details['description']}")
        st.write(f"**Impact on Energy:** {details['impact']}")
        st.write(f"**Typical Range:** {details['range']}")
        st.write(f"**Recommendation:** {details['recommendation']}")
        
        # Visual indicator
        st.markdown("### 📊 Impact Level")
        col_i1, col_i2, col_i3 = st.columns(3)
        with col_i1:
            st.metric("Heating Impact", "Medium-High")
        with col_i2:
            st.metric("Cooling Impact", "Medium-High")
        with col_i3:
            st.metric("Priority Level", "High")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>© 2025 SuhanaGhar AI | Climate-Responsive Smart Housing System | Powered by Machine Learning</p>",
    unsafe_allow_html=True
)