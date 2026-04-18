import streamlit as st
from database import save_prediction,create_tables
import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.ensemble import RandomForestRegressor

import plotly.graph_objects as go

create_tables()

# Load models
rf = joblib.load("models/rf_model.pkl")
xgb = joblib.load("models/xgb_model.pkl")

# Get session values
cyl = st.session_state.get("cyl")
disp = st.session_state.get("disp")
hp = st.session_state.get("hp")
weight = st.session_state.get("weight")
acc = st.session_state.get("acc")
year = st.session_state.get("year")
power_to_weight = st.session_state.get("power_to_weight")
car_age = st.session_state.get("car_age")
horsepower_per_cylinder = st.session_state.get("horsepower_per_cylinder")

# Run prediction only if inputs exist
prediction = None
confidence = None

if None not in (cyl, disp, hp, weight, acc, year, power_to_weight, car_age, horsepower_per_cylinder):
    input_data = np.array([[cyl, disp, hp, weight, acc, year, power_to_weight, car_age, horsepower_per_cylinder]])

    rf_pred = rf.predict(input_data)[0]
    xgb_pred = xgb.predict(input_data)[0]

    prediction = (rf_pred + xgb_pred) / 2
    difference = abs(rf_pred - xgb_pred)
    confidence = max(0.7, 1 - (difference / 10))

    # Store in session state
    st.session_state["mpg"] = prediction
    st.session_state["kmpl"] = prediction * 0.425144

st.markdown("""
<style>
.mpg-title{
    font-size:28px;
    font-weight:700;
    color:#00E5FF;
    margin-top:20px;
}
.mpg-box{
    font-size:20px;
    font-weight:500;
    color:#00a0b3;
    padding:12px;
    border-radius:10px;
    margin-bottom:8px;
    background:rgba(0,255,200,0.08);
    border-left:4px solid #00FFC6;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="rec-title">🚗 Prediction Result </div>', unsafe_allow_html=True)

mpg = st.session_state.get("mpg", None)
kmpl = st.session_state.get("kmpl", None)

if mpg:
    st.success(f"Predicted Fuel Efficiency: {mpg:.2f} MPG")
    st.info(f"Equivalent: {kmpl:.2f} KM/L")
else:
    st.warning("No prediction found. Go back and enter vehicle details.")

#-------------------------------------Fuel Efficiency Recommendations-------------------------------------------#

st.markdown("""
<style>
.rec-title{
    font-size:28px;
    font-weight:700;
    color:#00E5FF;
    margin-top:20px;
}
.rec-box{
    font-size:20px;
    font-weight:500;
    color:#00a0b3;
    padding:12px;
    border-radius:10px;
    margin-bottom:8px;
    background:rgba(0,255,200,0.08);
    border-left:4px solid #00FFC6;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="rec-title">⚡ Fuel Efficiency Recommendations</div>', unsafe_allow_html=True)

def fuel_efficiency_recommendation(cylinders, horsepower, weight, acceleration):
    recommendations = []

    if weight > 3500:
        recommendations.append("Reduce vehicle weight to improve fuel efficiency.")
    if cylinders > 6:
        recommendations.append("Use a lower cylinder engine configuration.")
    if horsepower > 150:
        recommendations.append("Optimize engine tuning to reduce fuel consumption.")
    if acceleration < 12:
        recommendations.append("Improve engine efficiency for better acceleration.")
    if len(recommendations) == 0:
        recommendations.append("Vehicle configuration is already optimized for good fuel efficiency.")

    return recommendations

if cyl is not None and hp is not None and weight is not None and acc is not None:
    recommendations = fuel_efficiency_recommendation(cyl, hp, weight, acc)
    for rec in recommendations:
        st.markdown(f'<div class="rec-box">✔ {rec}</div>', unsafe_allow_html=True)

#-------------------------Fuel Efficiency Meter-------------------------------------------------#

st.markdown("""
<style>
.pre-title{
    font-size:28px;
    font-weight:700;
    color:#00E5FF;
    margin-top:20px;
}
.pre-box{
    font-size:20px;
    font-weight:500;
    color:#00a0b3;
    padding:12px;
    border-radius:10px;
    margin-bottom:8px;
    backgroun  d:rgba(0,255,200,0.08);
    border-left:4px solid #00FFC6;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="rec-title">🚗 Fuel Efficiency Meter </div>', unsafe_allow_html=True)

if prediction is not None:

    # Toggle between MPG and KMPL
    unit = st.radio("Select Unit", ["MPG", "KM/L"], horizontal=True)

    if unit == "MPG":
        meter_value = prediction
        meter_max = 100
        meter_label = "Predicted MPG"
        meter_suffix = " MPG"
        steps = [
            {'range': [0, 33], 'color': "#ff6b6b"},
            {'range': [33, 66], 'color': "#ffd93d"},
            {'range': [66, 100], 'color': "#6bcB77"}
        ]
    else:
        meter_value = prediction * 0.425144
        meter_max = 50
        meter_label = "Predicted KM/L"
        meter_suffix = " KM/L"
        steps = [
            {'range': [0, 16], 'color': "#ff6b6b"},
            {'range': [16, 32], 'color': "#ffd93d"},
            {'range': [32, 50], 'color': "#6bcB77"}
        ]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=meter_value,
        title={'text': meter_label},
        number={'suffix': meter_suffix, 'valueformat': ".2f"},
        gauge={
            'axis': {'range': [0, meter_max]},
            'bar': {'color': "darkblue"},
            'steps': steps
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Prediction not available. Please enter vehicle details.")
if confidence is not None:
    st.subheader("🤖 AI Model Confidence")
    st.metric(
        label="Prediction Confidence",
        value=f"{confidence*100:.1f}%"
    )

#--------------------------------------------switch page --------------------------------------------------#

if st.button("Go to Explainable AI"):
    st.switch_page("pages/🧠 Explainable_AI.py")

st.markdown("""
<style>
.stApp{
    background: url("https://omdia.tech.informa.com/-/media/tech/omdia/omdia-website-enhancement-oct-2023/insights/abstract-shape-green-background.jpg");
    background-size: cover;
    background-attachment: fixed;
}
</style>""", unsafe_allow_html=True)