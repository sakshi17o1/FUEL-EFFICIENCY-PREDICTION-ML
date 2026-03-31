import streamlit as st
import pandas as pd

st.title("Fuel Analytics")

# Cost Section
st.subheader("💰 Fuel Cost Estimator")

fuel_price = st.number_input("Fuel Price (₹ per litre)", value=100.0, key="fuel_price")

unit = st.selectbox("Select Mileage Unit", ["MPG", "KM/L"])

if unit == "MPG":
    mpg = st.number_input("Enter MPG", value=25.0)
    kmpl = mpg * 0.425144
else:
    kmpl = st.number_input("Enter KM per Liter", value=10.0)
    mpg = kmpl / 0.425144


# ✅ Cost per 100 km
cost_per_100km = (100 / kmpl) * fuel_price
st.write(f"🚗 Cost per 100 km: ₹ {cost_per_100km:.2f}")


# ✅ Monthly cost
monthly_distance = st.number_input("Monthly Distance (km)", value=1000, key="monthly_distance")

monthly_cost = (monthly_distance / kmpl) * fuel_price

st.write(f"📅 Estimated Monthly Fuel Cost: ₹ {monthly_cost:.2f}")# ------------------------------
# Dashboard Enhancements
# ------------------------------

st.markdown("---")
st.header("📊 Fuel Cost Dashboard")

# Show metrics if mileage exists
try:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Mileage (MPG)", f"{mpg:.2f}")

    with col2:
        st.metric("Mileage (KM/L)", f"{kmpl:.2f}")

    with col3:
        cost_per_100km = (100 / kmpl) * fuel_price
        st.metric("Cost per 100 km", f"₹ {cost_per_100km:.2f}")

except:
    st.info("Enter mileage values to see dashboard metrics")


# ------------------------------
# Fuel Cost Graph
# ------------------------------

try:
    st.subheader("📈 Fuel Cost vs Distance")

    distances = [50, 100, 200, 300, 500, 800, 1000]
    costs = [(d / kmpl) * fuel_price for d in distances]

    chart_data = pd.DataFrame({
        "Distance (km)": distances,
        "Fuel Cost": costs
    })

    st.line_chart(chart_data.set_index("Distance (km)"))

except:
    st.info("Graph will appear after entering mileage values")


#  Vehicle Efficiency Rating

st.markdown("---")
st.header("🚗 Vehicle Efficiency Rating")

try:
    if kmpl < 8:
        st.error("Low Fuel Efficiency 🚨")
    elif kmpl < 15:
        st.warning("Moderate Fuel Efficiency ⚠️")
    else:
        st.success("High Fuel Efficiency ✅")

except:
    st.info("Enter mileage to see efficiency rating")


# 📊 Cost Comparison Chart

st.markdown("---")
st.header("📊 Cost Comparison")

try:
    distances = [100, 300, 500, 700, 1000]
    cost_values = [(d / kmpl) * fuel_price for d in distances]

    comparison_df = pd.DataFrame({
        "Distance (km)": distances,
        "Estimated Cost": cost_values
    })

    st.bar_chart(comparison_df.set_index("Distance (km)"))

except:
    st.info("Enter mileage values to view comparison chart")

st.markdown("""
            <style>
            .stApp{
        background: url("https://omdia.tech.informa.com/-/media/tech/omdia/omdia-website-enhancement-oct-2023/insights/abstract-shape-green-background.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    </style>""", unsafe_allow_html=True)



if st.button("Go to AI Simulation"):

    st.switch_page("E:\FEP\pages\⚡ What_If_AI_Simulation.py")


