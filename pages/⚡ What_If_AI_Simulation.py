import streamlit as st
import numpy as np
import joblib

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

st.subheader("⚡What-If AI Analysis")

# Safety check
if weight is None:
    st.warning("Please make a prediction first from Dashboard.")
    st.stop()

# Slider to adjust weight
new_weight = st.slider("Change Weight",1500.0,6000.0,float(weight),step=50.0)

if st.button("🔮Simulate Fuel Efficiency"):

    data = np.array([[cyl, disp, hp, new_weight, acc, year,
                    hp/new_weight,
                    82-year,
                    hp/cyl]])

    rf_pred = rf.predict(data)
    xgb_pred = xgb.predict(data)

    new_mpg = (0.6*rf_pred + 0.4*xgb_pred)[0]

    st.write("New Predicted MPG:", round(new_mpg,2))
    
    # Convert MPG to KM/L
    new_kmpl = new_mpg * 0.425144

    st.write("New Predicted KM/L:", round(new_kmpl,2))


st.markdown("""
            <style>
            .stApp{
        background: url("https://earth.org/wp-content/uploads/2018/05/Kevin-Pereira-AI-consulting-Blu-Artificial-Intelligence-Hive-Life-1--1200x720.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    </style>""", unsafe_allow_html=True)


