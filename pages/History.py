import streamlit as st
import pandas as pd
from database import get_history

if "username" in st.session_state:
    st.write("Username:", st.session_state["username"])
else:
    st.warning("⚠ Please login first.")
    st.stop()

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

if not history:
    st.info("No prediction history found.")
else:
    df = pd.DataFrame(history, columns=[
        "Username", "Cylinders", "Displacement",
        "Horsepower", "Weight", "Acceleration",
        "Model Year", "MPG", "KMPL", "Time"
    ])

    # Fix bytes and encoding issues
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: x.decode('utf-8', errors='replace') if isinstance(x, bytes)
            else (x.encode('utf-8', errors='ignore').decode('utf-8') if isinstance(x, str) else x)
        )

    # Numeric fix
    df["MPG"]  = pd.to_numeric(df["MPG"],  errors='coerce').round(2)
    df["KMPL"] = pd.to_numeric(df["KMPL"], errors='coerce').round(2)

    st.dataframe(df)

    # Line chart
    if df["MPG"].notna().any():
        st.line_chart(df[["MPG", "KMPL"]])
    else:
        st.warning("No numeric data for chart.")
