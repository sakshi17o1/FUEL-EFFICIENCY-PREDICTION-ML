import streamlit as st
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt

st.title("🧠 Explainable AI")

model_config  = joblib.load("models/model_config.pkl")
scaler_config = joblib.load("models/scaler_config.pkl")

# Get prediction inputs from session
cyl = st.session_state.get("cyl")
disp = st.session_state.get("disp")
hp = st.session_state.get("hp")
weight = st.session_state.get("weight")
acc = st.session_state.get("acc")
year = st.session_state.get("year")

if cyl is None:
    st.warning("Please make a prediction first from Dashboard.")
    st.stop()

# Create feature vector
# st.subheader("Feature Contribution")

importance = model_config.feature_importances_

features = [
    "cylinders",
    "displacement",
    "horsepower",
    "weight",
    "model-year",      # ✅ correct name
    "power_to_weight",
    "car_age",
    "hp_per_cylinder"
]

df_imp = pd.DataFrame({
    "Feature": features,
    "Importance": importance
})

df_imp = df_imp.sort_values(by="Importance", ascending=False)

# st.bar_chart(df_imp.set_index("Feature"))
fig, ax = plt.subplots(figsize=(6,3))

ax.bar(df_imp["Feature"], df_imp["Importance"])

ax.set_xlabel("Vehicle Configurations", fontsize=6)
ax.set_ylabel("Importance Value", fontsize=6)
ax.set_title("Feature Contribution Analysis", fontsize=8)

plt.xticks(rotation=45, fontsize=5)
plt.yticks(fontsize=5)

ax.grid(axis='y', linestyle='--', alpha=0.7)
# plt.tight_layout()

st.pyplot(fig)


if st.button("Go to Analytics"):

    st.switch_page("pages/📈 Analytics.py")

st.markdown("""
            <style>
            .stApp{
        background: url("https://omdia.tech.informa.com/-/media/tech/omdia/omdia-website-enhancement-oct-2023/insights/abstract-shape-green-background.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    </style>""", unsafe_allow_html=True)

