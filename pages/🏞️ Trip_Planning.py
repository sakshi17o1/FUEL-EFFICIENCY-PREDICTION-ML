import streamlit as st
import pandas as pd

# Trip Cost Calculator

st.markdown("---")
st.header("🧾 Trip Fuel Cost Calculator")

fuel_price = st.number_input("Fuel Price (₹ per litre)", value=100.0, key="fuel_price")
unit = st.selectbox("Select Mileage Unit", ["MPG", "KM/L"])

if unit == "MPG":
    mpg = st.number_input("Enter MPG", value=25.0)
    kmpl = mpg * 0.425144
else:
    kmpl = st.number_input("Enter KM per Liter", value=10.0)
    mpg = kmpl / 0.425144

    # Cost per 100 km
    cost_per_100km = (100 / kmpl) * fuel_price

    st.write(f"🚗 Cost per 100 km: ₹ {cost_per_100km:.2f}")

    monthly_distance = st.number_input("Monthly Distance (km)", value=1000, key="monthly_distance")
    monthly_cost = (monthly_distance / kmpl) * fuel_price

    st.write(f"📅 Estimated Monthly Fuel Cost: ₹ {monthly_cost:.2f}")
    
try:
    trip_distance = st.number_input("Enter Trip Distance (km)", value=200)

    trip_fuel = trip_distance / kmpl
    trip_cost = trip_fuel * fuel_price

    st.write(f"Fuel needed for trip: {trip_fuel:.2f} liters")
    st.write(f"Estimated Trip Cost: ₹ {trip_cost:.2f}")

except:
    st.info("Enter mileage values to calculate trip cost")


st.markdown("""
            <style>
            .stApp{
        background: url("https://publiclawproject.org.uk/content/uploads/2024/08/shutterstock_2360611911-scaled.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    </style>""", unsafe_allow_html=True)