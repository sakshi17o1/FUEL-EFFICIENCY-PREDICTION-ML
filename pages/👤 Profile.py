import streamlit as st
import pandas as pd
from database import get_history

if "username" in st.session_state:
    st.write("Username:", st.session_state["username"])
else:
    st.warning("⚠ Please login first.")


st.title("User Profile")

st.write("Username:",st.session_state["username"])

st.markdown("""
            <style>
            .stApp{
        background: url("https://publiclawproject.org.uk/content/uploads/2024/08/shutterstock_2360611911-scaled.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    </style>""", unsafe_allow_html=True)


history = get_history(st.session_state["username"])
st.subheader("Your Prediction History")

df = pd.DataFrame(history, columns=[
    "Username",
    "Cylinders",
    "Displacement",
    "Horsepower",
    "Weight",
    "Acceleration",
    "Model Year",
    "MPG",
    "KMPL",
    "Time"
])
# save_prediction(st.session_state["username"], mpg, kmpl)
st.dataframe(df)
st.line_chart(df[["MPG","KMPL"]])
