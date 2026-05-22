import streamlit as st
import numpy as np
import joblib
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from database import create_tables, save_prediction

create_tables()

# Load both models + scalers
model_config  = joblib.load("models/model_config.pkl")
scaler_config = joblib.load("models/scaler_config.pkl")
model_brand   = joblib.load("models/model_brand.pkl")
scaler_brand  = joblib.load("models/scaler_brand.pkl")

# Load car specs for brand+model dropdown
car_specs = pd.read_csv("models/car_specs_final.csv")
car_specs.columns = car_specs.columns.str.strip()

config_features = [
    "cylinders", "displacement", "horsepower",
    "weight", "model-year", "origin",
    "power_to_weight", "car_age", "hp_per_cylinder"
]

brand_features = [
    "Engine HP", "Engine Cylinders", "weight_est",
    "displacement_est", "vehicle_age",
    "power_to_weight", "hp_per_cylinder"
]

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
    brands     = sorted(car_specs["Make"].dropna().unique())
    sel_brand  = st.selectbox("Select Car Brand", ["-- Select --"] + list(brands))

    sel_model = None
    if sel_brand != "-- Select --":
        model_list = sorted(
            car_specs[car_specs["Make"] == sel_brand]["Model"]
            .dropna().unique()
        )
        sel_model = st.selectbox("Select Car Model", ["-- Select --"] + list(model_list))

        if sel_model != "-- Select --":
            # Show specs of selected car
            match = car_specs[
                (car_specs["Make"].str.lower() == sel_brand.lower()) &
                (car_specs["Model"].str.lower() == sel_model.lower())
            ]
            if not match.empty:
                row = match.iloc[0]
                st.info(f"HP: {row['Engine HP']} | Cylinders: {row['Engine Cylinders']}")

            # Save to session
            st.session_state["selected_brand"] = sel_brand
            st.session_state["selected_model"] = sel_model

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
if st.button("Predict Fuel Efficiency", key="predict_btn"):

    mpg  = None
    kmpl = None

    # ── WAY 1: Brand + Model ─────────────────────────
    if mode == "Select Car Model":
        sb = st.session_state.get("selected_brand")
        sm = st.session_state.get("selected_model")

        if sb and sm and sb != "-- Select --" and sm != "-- Select --":
            match = car_specs[
                (car_specs["Make"].str.lower() == sb.lower()) &
                (car_specs["Model"].str.lower() == sm.lower())
            ]
            if not match.empty:
                row = match.iloc[0]
                input_df = pd.DataFrame([[
                    row["Engine HP"],
                    row["Engine Cylinders"],
                    row["weight_est"],
                    row["displacement_est"],
                    row["vehicle_age"],
                    row["power_to_weight"],
                    row["hp_per_cylinder"]
                ]], columns=brand_features)
            
                # Scaler ke expected columns check karo
                expected_cols = scaler_brand.feature_names_in_
    
                # Missing columns ko 0 se fill karo
                for col in expected_cols:
                    if col not in input_df.columns:
                        input_df[col] = 0
    
                # Correct order mein arrange karo
                input_df = input_df[expected_cols]
    
                input_scaled = scaler_brand.transform(input_df)
                mpg = model_brand.predict(input_scaled)[0]

                input_scaled = scaler_brand.transform(input_df)
                mpg  = model_brand.predict(input_scaled)[0]
                kmpl = mpg * 0.4251

                # Session save
                st.session_state["selected_brand"] = sb
                st.session_state["selected_model"]  = sm
                st.session_state["hp"]     = row["Engine HP"]
                st.session_state["cyl"]    = row["Engine Cylinders"]
            else:
                st.error("Car not found in database.")

        else:
            st.warning("Please select Brand and Model first.")

    # ── WAY 2: Manual Config ──────────────────────────
    elif mode == "Enter Vehicle Configuration":
        power_to_weight      = hp / weight
        car_age              = 2026 - year
        horsepower_per_cyl   = hp / cyl

        config_features = [
                "cylinders", "displacement", "horsepower",
                "weight", "model-year",
                "power_to_weight", "car_age", "hp_per_cylinder"
            ]

        input_df = pd.DataFrame([[
            cyl, disp, hp, weight,
            year,
            power_to_weight, car_age, horsepower_per_cyl
        ]], columns=config_features)

        input_scaled = scaler_config.transform(input_df)
        mpg  = model_config.predict(input_scaled)[0]
        kmpl = mpg * 0.4251

        # Session save
        st.session_state["cyl"]                    = cyl
        st.session_state["disp"]                   = disp
        st.session_state["hp"]                     = hp
        st.session_state["weight"]                 = weight
        st.session_state["acc"]                    = acc
        st.session_state["year"]                   = year
        st.session_state["power_to_weight"]        = power_to_weight
        st.session_state["car_age"]                = car_age
        st.session_state["horsepower_per_cylinder"]= horsepower_per_cyl

    # ── Common: Save + Switch ─────────────────────────
    if mpg is not None:
        save_prediction(
            st.session_state["username"],
            st.session_state.get("cyl", 0),
            st.session_state.get("disp", 0),
            st.session_state.get("hp", 0),
            st.session_state.get("weight", 0),
            st.session_state.get("acc", 0),
            st.session_state.get("year", 0),
            mpg, kmpl
        )
        st.session_state["mpg"]  = mpg
        st.session_state["kmpl"] = kmpl
        st.switch_page("pages/📊Prediction.py")

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
    st.session_state["horsepower_per_cylinder"] = horsepower_per_cyl  # ✅ add this


    st.switch_page("pages/📊Prediction.py")


st.markdown("""
<style>
.stApp{
    background: url("https://omdia.tech.informa.com/-/media/tech/omdia/omdia-website-enhancement-oct-2023/insights/abstract-shape-green-background.jpg");
    background-size: cover;
    background-attachment: fixed;
}
</style>""", unsafe_allow_html=True)


