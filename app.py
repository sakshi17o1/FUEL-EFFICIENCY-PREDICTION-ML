import streamlit as st
from auth import login, register

# from database import create_user_table
# create_user_table()

from database import create_tables
create_tables()


# SESSION STATE INITIALIZATION

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = None


#-----------------------#

from database import create_tables
from style import load_css

create_tables()
load_css()


st.set_page_config(
    page_title="Fuel Efficiency Predictor",
    page_icon="🚗",
    layout="wide"
)


# ---- Custom CSS for Login Page ----

st.markdown("""
<style>

.stApp{
background:url("https://image.slidesdocs.com/responsive-images/background/high-tech-electronic-data-flow-wave-line-advertising-powerpoint-background_1d5bc8f2b5__960_540.jpg");
color:white;
}


/* Login Card */

.login-card{
background: rgba(255,255,255,0.08);
padding:35px;
border-radius:20px;
backdrop-filter: blur(12px);
box-shadow:0px 0px 20px rgba(0,0,0,0.6);
}


/* Title */

.title{
font-size:45px;
font-weight:bold;
text-align:center;
}


/* Buttons */

.stButton>button{
background:#0099ff;
color:white;
border-radius:10px;
padding:10px 15px;
border:none;
width:100%;
}

</style>
""", unsafe_allow_html=True)


# Hide Streamlit default pages navigation

hide_streamlit_style = """
<style>

[data-testid="stSidebarNav"] {
    display: none;
}

</style>
"""

st.markdown(
    hide_streamlit_style,
    unsafe_allow_html=True
)


# SESSION STATES

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "menu" not in st.session_state:
    st.session_state["menu"] = "login"


# ============================================================
# LOGIN SCREEN
# ============================================================

if not st.session_state["logged_in"]:


    # ========================================================
    # NAVBAR
    # ========================================================

    col0, col2, col3 = st.columns(
        [6, 1, 1]
    )


    with col0:

        st.markdown(
            "### 🚗 Fuel efficiency prediction"
        )


    # ========================================================
    # HERO SECTION
    # ========================================================

    left, right = st.columns(
        [2, 1]
    )


    with left:

        st.markdown("""
        <div class="hero-title">
        Welcome to Fuel efficiency predictor
        </div>
        """, unsafe_allow_html=True)


        st.markdown("""
        <div class="hero-sub">
        AI-Powered Fuel Efficiency Prediction System
        Predict vehicle mileage using machine learning and estimate fuel costs instantly.
        </div>
        """, unsafe_allow_html=True)


        st.markdown("""
        <div class="hero-desc">
        About project:<br>
        This web application predicts the fuel efficiency of vehicles based on user input.
        The application features a user-friendly interface for entering vehicle specifications
        and displays the predicted miles per gallon (MPG) along with the equivalent
        kilometers per liter (KM/L). Additionally, it includes user authentication and a
        dashboard for tracking predictions and analytics.
        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # LOGIN / REGISTER CARD
    # ========================================================

    with right:

        st.markdown(
            '<div class="login-card">',
            unsafe_allow_html=True
        )


        st.subheader(
            "Login to Continue"
        )


        b1, b2 = st.columns(2)


        with b1:

            if st.button(
                "Login",
                key="login_menu_btn"
            ):

                st.session_state["menu"] = "login"


        with b2:

            if st.button(
                "Register",
                key="register_menu_btn"
            ):

                st.session_state["menu"] = "register"


        # ====================================================
        # LOGIN
        # ====================================================

        if st.session_state["menu"] == "login":

            login()


        # ====================================================
        # REGISTER
        # ====================================================

        if st.session_state["menu"] == "register":

            register()


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )