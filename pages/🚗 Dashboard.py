import streamlit as st
import numpy as np
import joblib
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from database import create_tables, save_prediction

create_tables()

# load dataset
cars = pd.read_csv("data/processed_auto_mpg.csv")
# Create brand and model columns (since Auto MPG has 'car name')
cars["brand"] = cars["brand"].apply(lambda x: x.split()[0])
cars["model"] = cars["model"]

# load trained ML model
model = joblib.load("models/fuel_efficiency_model_final.pkl")

# load feature columns used in training
features = pickle.load(open("models/model_features.pkl","rb"))

rf = joblib.load("models/rf_model.pkl")
xgb = joblib.load("models/xgb_model.pkl")

# Initialize session state
if "username" not in st.session_state:
    st.session_state["username"] = "Guest"
    st.write("Welcome", st.session_state["username"])

if "prediction_saved" in st.session_state:
    del st.session_state["prediction_saved"]
    cyl = st.session_state.get("cyl")
    disp = st.session_state.get("disp")
    hp = st.session_state.get("hp")
    weight = st.session_state.get("weight")
    acc = st.session_state.get("acc")
    year = st.session_state.get("year")
    mpg = st.session_state.get("mpg")
    kmpl = st.session_state.get("kmpl")

st.title("Vehicle Configuration")

st.subheader("Choose how you want to predict fuel efficiency")

mode = st.radio(
    "Choose Prediction Mode",
    ["Select Car Model", "Enter Vehicle Configuration"]
)

# -----------------------------
# MODE 1: Select Car Model
# -----------------------------
if mode == "Select Car Model":

    brand = st.selectbox(
        "Select Car Brand",
        cars["brand"].unique()
    )

    models = cars[cars["brand"] == brand]["model"]

    model_name = st.selectbox(
        "Select Car Model",
        models
    )

    row = cars[cars["model"] == model_name].iloc[0]

    cyl = int(row["cylinders"])
    hp = float(row["horsepower"])
    weight = float(row["weight"])
    acc = float(row["acceleration"])
    year = int(row["model year"])
    disp = st.number_input("Engine Displacement (cc)",min_value=500.0,max_value=8000.0,step=50.0)

# -----------------------------
# MODE 2: Manual Input
# -----------------------------

if mode == "Enter Vehicle Configuration":

    cyl = st.number_input("Cylinders",3,12,4)
    disp = st.number_input("Engine Displacement (cc)",min_value=500.0,max_value=8000.0,step=50.0)
    hp = st.number_input("Horsepower",40.0,300.0,100.0)
    weight = st.number_input("Weight",1500.0,6000.0,3000.0)
    acc = st.number_input("Acceleration",5.0,30.0,15.0)
    year = st.number_input("Model Year",70,82,76)


# -----------------------------
# PREDICTION & SAVE
# -----------------------------
if st.button("Predict Fuel Efficiency",key="predict_btn"):
    # Feature Engineering (same as training)
    power_to_weight = hp / weight
    car_age = 82 - year
    horsepower_per_cylinder = hp / cyl

    data = pd.DataFrame([[
        cyl,
        disp,
        hp,
        weight,
        acc,
        year,
        power_to_weight,
        car_age,
        horsepower_per_cylinder
    ]], columns=features)
    

    # ✅ Make predictions
    rf_pred = rf.predict(data)
    xgb_pred = xgb.predict(data)

    mpg = (0.6 * rf_pred +0.4 * xgb_pred)[0]
    kmpl = mpg * 0.425

    # save prediction once
    save_prediction(
        st.session_state["username"],
        cyl, disp, hp, weight, acc, year,mpg, kmpl
    )
    st.session_state["mpg"] = mpg
    st.session_state["kmpl"] = kmpl
    st.session_state["cyl"] = cyl
    st.session_state["disp"] = disp
    st.session_state["hp"] = hp
    st.session_state["weight"] = weight
    st.session_state["acc"] = acc
    st.session_state["year"] = year
    st.session_state["power_to_weight"] = power_to_weight        # ✅ add this
    st.session_state["car_age"] = car_age                        # ✅ add this
    st.session_state["horsepower_per_cylinder"] = horsepower_per_cylinder  # ✅ add this


    st.switch_page("pages/📊Prediction.py")


st.markdown("""
<style>
.stApp{
    background: url("https://omdia.tech.informa.com/-/media/tech/omdia/omdia-website-enhancement-oct-2023/insights/abstract-shape-green-background.jpg");
    background-size: cover;
    background-attachment: fixed;
}
</style>""", unsafe_allow_html=True)


