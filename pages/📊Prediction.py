import streamlit as st
from database import save_prediction,create_tables
import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.ensemble import RandomForestRegressor

create_tables()

rf = joblib.load("models/rf_model.pkl")
xgb = joblib.load("models/xgb_model.pkl")

cyl = st.session_state.get("cyl")
disp = st.session_state.get("disp")
hp = st.session_state.get("hp")
weight = st.session_state.get("weight")
acc = st.session_state.get("acc")
year = st.session_state.get("year")
mpg = st.session_state.get("mpg")
kmpl = st.session_state.get("kmpl")


st.title("🚗 Prediction Result")

mpg = st.session_state.get("mpg", None)
kmpl = st.session_state.get("kmpl", None)

if mpg:
    st.success(f"Predicted Fuel Efficiency: {mpg:.2f} MPG")
    st.info(f"Equivalent: {kmpl:.2f} KM/L")
else:
    st.warning("No prediction found. Go back and enter vehicle details.")



if st.button("Go to Explainable AI"):

    st.switch_page("pages/🧠 Explainable_AI.py")



st.markdown("""
            <style>
            .stApp{
        background: url("https://web-assets.bcg.com/db/3a/3e3c640f44ee9f8f657bd20b10e6/capturing-real-world-value-in-automotive-with-ai-rectangle.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    </style>""", unsafe_allow_html=True)