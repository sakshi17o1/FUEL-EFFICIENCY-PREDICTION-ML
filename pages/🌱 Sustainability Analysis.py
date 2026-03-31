import streamlit as st
import plotly.graph_objects as go

st.title("🌱 Sustainability Analysis")

mpg = st.session_state.get("mpg")

if mpg is None:
    st.warning("Please make a prediction first from Dashboard.")
    st.stop()

# -----------------------------
# Fuel Consumption Calculation
# -----------------------------

fuel_consumption = 235.215 / mpg   # L/100km

# -----------------------------
# CO2 Emission Estimation
# -----------------------------

co2 = fuel_consumption * 23.2   # Approx grams/km factor


st.subheader("Vehicle Environmental Metrics")

st.write("Predicted Fuel Efficiency (MPG):", round(mpg,2))
st.write("Fuel Consumption (L/100km):", round(fuel_consumption,2))
st.write("Estimated CO₂ Emission (g/km):", round(co2,2))


# -----------------------------
# Environmental Rating System
# -----------------------------

st.subheader("Environmental Impact Score")

if co2 < 150:

    st.success("🟢 Green Vehicle — Eco Friendly")

elif co2 >= 150 and co2 <= 250:

    st.warning("🟡 Moderate Emission Vehicle")

else:

    st.error("🔴 High Emission Vehicle")

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=co2,
    title={'text': "CO₂ Emission (g/km)"},
    gauge={
        'axis': {'range': [0, 400]},
        'steps': [
            {'range': [0, 150], 'color': "green"},
            {'range': [150, 250], 'color': "yellow"},
            {'range': [250, 400], 'color': "red"}
        ],
    }
))

st.plotly_chart(fig)

st.markdown("""
            <style>
            .stApp{
        background: url("https://omdia.tech.informa.com/-/media/tech/omdia/omdia-website-enhancement-oct-2023/insights/abstract-shape-green-background.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    </style>""", unsafe_allow_html=True)
