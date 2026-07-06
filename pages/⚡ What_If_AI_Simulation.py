import pandas as pd
import streamlit as st
import numpy as np
import joblib

model_config  = joblib.load("models/model_config.pkl")
scaler_config = joblib.load("models/scaler_config.pkl")

cyl = st.session_state.get("cyl")
disp = st.session_state.get("disp")
hp = st.session_state.get("hp")
weight = st.session_state.get("weight")
acc = st.session_state.get("acc")
year = st.session_state.get("year")
mpg = st.session_state.get("mpg")
kmpl = st.session_state.get("kmpl")

st.subheader("⚡What-If AI Analysis")

# Safety check
if weight is None:
    st.warning("Please make a prediction first from Dashboard.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/🚗 Dashboard.py")
    st.stop()

# Slider to adjust weight
new_weight = st.slider("Change Weight",1500.0,6000.0,float(weight),step=50.0)

if st.button("🔮Simulate Fuel Efficiency"):

    config_features = [
    "cylinders", "displacement", "horsepower",
    "weight", "model-year",
    "power_to_weight", "car_age", "hp_per_cylinder"
]

    input_df = pd.DataFrame([[
        cyl, disp, hp, new_weight,
        year,
        hp / new_weight,
        2026 - year,
        hp / cyl
    ]], columns=config_features)

    input_scaled = scaler_config.transform(input_df)
    new_mpg      = model_config.predict(input_scaled)[0]

    new_kmpl = new_mpg * 0.4251
    st.write("New Predicted MPG :", round(new_mpg, 2))
    st.write("New Predicted KMPL:", round(new_kmpl, 2))


st.markdown("""
            <style>
            .stApp{
        background: url("https://earth.org/wp-content/uploads/2018/05/Kevin-Pereira-AI-consulting-Blu-Artificial-Intelligence-Hive-Life-1--1200x720.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    </style>""", unsafe_allow_html=True)


