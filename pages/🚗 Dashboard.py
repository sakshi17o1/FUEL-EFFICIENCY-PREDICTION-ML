import streamlit as st
import numpy as np
import joblib
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from database import create_tables, save_prediction
import openrouteservice
import os
from dotenv import load_dotenv
load_dotenv()

create_tables()

ORS_API_KEY = os.getenv("ORS_API_KEY")

model_config  = joblib.load("models/model_config.pkl")
scaler_config = joblib.load("models/scaler_config.pkl")
model_brand   = joblib.load("models/model_brand.pkl")
scaler_brand  = joblib.load("models/scaler_brand.pkl")

car_specs = pd.read_csv("models/car_specs_final.csv")
car_specs.columns = car_specs.columns.str.strip()

config_features = ["cylinders", "displacement", "horsepower", "weight", "model-year", "power_to_weight", "car_age", "hp_per_cylinder"]
brand_features  = ["Engine HP", "Engine Cylinders", "weight_est", "displacement_est", "vehicle_age", "power_to_weight", "hp_per_cylinder"]

if "username" not in st.session_state:
    st.session_state["username"] = "Guest"
if "show_map" not in st.session_state:
    st.session_state["show_map"] = False

st.title("Vehicle Configuration")
st.subheader("Choose how you want to predict fuel efficiency")

mode = st.radio("Choose Prediction Mode", ["Select Car Model", "Enter Vehicle Configuration"])

# ─── MODE 1: Select Car Model ───
if mode == "Select Car Model":
    brands    = sorted(car_specs["Make"].dropna().unique())
    sel_brand = st.selectbox("Select Car Brand", ["-- Select --"] + list(brands))
    sel_model = None
    if sel_brand != "-- Select --":
        model_list = sorted(car_specs[car_specs["Make"] == sel_brand]["Model"].dropna().unique())
        sel_model  = st.selectbox("Select Car Model", ["-- Select --"] + list(model_list))
        if sel_model != "-- Select --":
            match = car_specs[(car_specs["Make"].str.lower() == sel_brand.lower()) & (car_specs["Model"].str.lower() == sel_model.lower())]
            if not match.empty:
                row = match.iloc[0]
                st.info(f"HP: {row['Engine HP']} | Cylinders: {row['Engine Cylinders']}")
            st.session_state["selected_brand"] = sel_brand
            st.session_state["selected_model"] = sel_model
            
    st.subheader("🗺️ Route Details (Optional)")
    origin      = st.text_input("Start Location", placeholder="e.g. Jalandhar, Punjab", key="origin_brand")
    destination = st.text_input("End Location",   placeholder="e.g. Delhi", key="dest_brand")
    fuel_price  = st.number_input("Fuel Price (₹ per litre)", min_value=50.0, max_value=200.0, value=96.0, step=0.5, key="fp_brand")

# ─── MODE 2: Enter Vehicle Configuration ───
if mode == "Enter Vehicle Configuration":
    st.subheader("🚗 Vehicle Configuration")
    cyl    = st.number_input("Cylinders",                3,     12,    4)
    disp   = st.number_input("Engine Displacement (cc)", 500.0, 8000.0, 1500.0, step=50.0)
    hp     = st.number_input("Horsepower",               40.0,  300.0,  100.0)
    weight = st.number_input("Weight (lbs)",             1500.0,6000.0, 3000.0)
    acc    = st.number_input("Acceleration",             5.0,   30.0,   15.0)
    year   = st.number_input("Model Year",               70,    82,     76)

    st.subheader("🗺️ Route Details (Optional)")
    origin      = st.text_input("Start Location", placeholder="e.g. Jalandhar, Punjab")
    destination = st.text_input("End Location",   placeholder="e.g. Delhi")
    fuel_price  = st.number_input("Fuel Price (₹ per litre)", min_value=50.0, max_value=200.0, value=96.0, step=0.5)

# ─── Route Helper Function ───
def get_route(kmpl, origin, destination, fuel_price):
    try:
        geolocator = Nominatim(user_agent="fep_app")
        with st.spinner("Fetching route..."):
            loc1 = geolocator.geocode(origin + ", India")
            loc2 = geolocator.geocode(destination + ", India")

        if loc1 and loc2:
            coords1 = (loc1.latitude, loc1.longitude)
            coords2 = (loc2.latitude, loc2.longitude)

            try:
                ors_client   = openrouteservice.Client(key=ORS_API_KEY)
                route        = ors_client.directions(
                    coordinates=[[coords1[1], coords1[0]], [coords2[1], coords2[0]]],
                    profile='driving-car',
                    format='json'
                )
                props        = route['routes'][0]['summary']
                distance_km  = round(props['distance'] / 1000, 2)
                duration_min = round(props['duration'] / 60, 2)
                geometry     = route['routes'][0]['geometry']
                decoded      = openrouteservice.convert.decode_polyline(geometry)
                route_coords = [(c[1], c[0]) for c in decoded['coordinates']]
            except Exception:
                distance_km  = round(geodesic(coords1, coords2).km, 2)
                duration_min = None
                route_coords = [coords1, coords2]

            fuel_required = round(distance_km / kmpl, 2)
            fuel_cost     = round(fuel_required * fuel_price, 2)

            st.session_state.update({
                "show_map": True,
                "map_coords1": coords1,
                "map_coords2": coords2,
                "map_origin": origin,
                "map_destination": destination,
                "map_origin_address": loc1.address,
                "map_dest_address": loc2.address,
                "route_distance": distance_km,
                "route_fuel": fuel_required,
                "route_cost": fuel_cost,
                "route_fuel_price": fuel_price,
                "route_coords": route_coords,
                "duration_min": duration_min
            })
        else:
            st.error("Location not found. Check spelling.")
    except Exception as e:
        st.error(f"Route Error: {str(e)}")

# ─── Predict Button ───
if st.button("Predict Fuel Efficiency", key="predict_btn"):
    mpg  = None
    kmpl = None
    st.session_state["show_map"] = False

    if mode == "Select Car Model":
        sb = st.session_state.get("selected_brand")
        sm = st.session_state.get("selected_model")
        if sb and sm and sb != "-- Select --" and sm != "-- Select --":
            match = car_specs[(car_specs["Make"].str.lower() == sb.lower()) & (car_specs["Model"].str.lower() == sm.lower())]
            if not match.empty:
                row      = match.iloc[0]
                input_df = pd.DataFrame([[row["Engine HP"], row["Engine Cylinders"], row["weight_est"], row["displacement_est"], row["vehicle_age"], row["power_to_weight"], row["hp_per_cylinder"]]], columns=brand_features)
                input_scaled = scaler_brand.transform(input_df)
                model_xgb_b = joblib.load("models/model_xgb_brand.pkl")
                model_rf_b  = joblib.load("models/model_rf_brand.pkl")
                scaler_b    = joblib.load("models/scaler_brand_final.pkl")

                input_scaled  = scaler_b.transform(input_df)
                xgb_pred_b   = model_xgb_b.predict(input_scaled)[0]
                rf_pred_b    = model_rf_b.predict(input_scaled)[0]
                mpg          = (0.60 * xgb_pred_b) + (0.40 * rf_pred_b)
                kmpl         = mpg * 0.4251

                st.session_state["prediction_mode"] = "brand"
                st.session_state["brand_input_sc"]  = scaler_b.transform(input_df)[0].tolist()
                st.session_state["hp"]     = row["Engine HP"]
                st.session_state["cyl"]    = row["Engine Cylinders"]
                st.session_state["weight"] = row["weight_est"]
                st.session_state["disp"]   = row["displacement_est"]
                st.session_state["year"]   = 2026 - row["vehicle_age"]
                st.session_state["acc"]    = 15.0  # default
                st.session_state["power_to_weight"]         = row["power_to_weight"]
                st.session_state["car_age"]                 = row["vehicle_age"]
                st.session_state["horsepower_per_cylinder"] = row["hp_per_cylinder"]
                
                origin      = st.session_state.get("origin_brand", "")
                destination = st.session_state.get("dest_brand", "")
                fuel_price  = st.session_state.get("fp_brand", 96.0)
                if origin and destination:
                    get_route(kmpl, origin, destination, fuel_price)
            else:
                st.error("Car not found in database.")
        else:
            st.warning("Please select Brand and Model first.")

    elif mode == "Enter Vehicle Configuration":
        power_to_weight    = hp / weight
        car_age            = 2026 - year
        horsepower_per_cyl = hp / cyl

        input_df = pd.DataFrame([[cyl, disp, hp, weight, year, power_to_weight, car_age, horsepower_per_cyl]], columns=config_features)
        model_xgb_c = joblib.load("models/model_xgb_final.pkl")
        model_rf_c  = joblib.load("models/model_rf_final.pkl")
        scaler_c    = joblib.load("models/scaler_final.pkl")

        input_scaled = scaler_c.transform(input_df)
        xgb_pred_c  = model_xgb_c.predict(input_scaled)[0]
        rf_pred_c   = model_rf_c.predict(input_scaled)[0]
        mpg         = (0.60 * xgb_pred_c) + (0.40 * rf_pred_c)
        kmpl        = mpg * 0.4251

        st.session_state.update({
            "cyl": cyl, "disp": disp, "hp": hp,
            "weight": weight, "acc": acc, "year": year,
            "power_to_weight": power_to_weight,
            "car_age": car_age, "horsepower_per_cylinder": horsepower_per_cyl
        })

        if origin and destination:
            get_route(kmpl, origin, destination, fuel_price)

    if mpg is not None:
        save_prediction(
            st.session_state["username"],
            st.session_state.get("cyl", 0), st.session_state.get("disp", 0),
            st.session_state.get("hp", 0),  st.session_state.get("weight", 0),
            st.session_state.get("acc", 0), st.session_state.get("year", 0),
            mpg, kmpl
        )
        st.session_state["mpg"]  = mpg
        st.session_state["kmpl"] = kmpl
        st.session_state["route_mpg"]  = mpg
        st.session_state["route_kmpl"] = kmpl
        st.session_state["prediction_mode"] = "config"
        st.switch_page("pages/📊Prediction.py")

st.markdown("""
<style>
.stApp{
    background: url("https://omdia.tech.informa.com/-/media/tech/omdia/omdia-website-enhancement-oct-2023/insights/abstract-shape-green-background.jpg");
    background-size: cover;
    background-attachment: fixed;
}
</style>""", unsafe_allow_html=True)