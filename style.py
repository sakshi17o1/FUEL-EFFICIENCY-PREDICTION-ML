import streamlit as st

def load_css():
    st.markdown("""
    <style>

    .hero-title{
        font-size:55px;
        font-weight:800;
        letter-spacing:1px;
        color:white;
    }

    .hero-sub{
        font-size:25px;
        font-weight:400;
        letter-spacing:1px;
        color:white;
    }

    .hero-desc{
        font-size:25px;
        font-weight:400;
        letter-spacing:1px;
        color:white;
    }

    .stApp{
        background: url("https://thumbs.dreamstime.com/b/ai-assisted-ev-charging-clean-energy-monitoring-vouch-manages-dashboards-tracking-battery-status-optimizing-renewable-power-421865356.jpg?w=992");
        background-size: cover;
        background-attachment: fixed;
    }

    .glass {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding:30px;
        border-radius:15px;
    }

    h1,h2,h3{
        color:white;
        text-align:center;
    }

    .stButton>button{
        background:#ff4b4b;
        color:white;
        border-radius:10px;
        width:200px;
        height:40px;
    }

    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>

.stTextInput input {
    border-radius:10px;
}

.stButton>button{
    width:100%;
    border-radius:8px;
    height:40px;
}

            
.stApp{
        background: url("https://thumbs.dreamstime.com/b/ai-assisted-ev-charging-clean-energy-monitoring-vouch-manages-dashboards-tracking-battery-status-optimizing-renewable-power-421865356.jpg?w=992");
        background-size: cover;
        background-attachment: fixed;
        color:white;
    }

    /* NAVBAR */
    .navbar{
        align-items:center;
        padding:15px 40px;
        border-bottom:1px solid rgba(255,255,255,0.2);
    }

    .nav-left{
        font-size:22px;
        font-weight:bold;
    }

    .nav-links{
        display:flex;
        gap:25px;
        font-size:16px;
    }

    .login-btn{
        border:1px solid #00c3ff;
        padding:6px 20px;
        border-radius:8px;
        color:white;
    }

    /* HERO SECTION */

    .hero{
        padding:80px 60px;
    }

    .hero-title{
        font-size:55px;
        font-weight:bold;
    }

    .hero-sub{
        font-size:22px;
        margin-top:10px;
        color:#dcdcdc;
    }

    .start-btn{
        margin-top:25px;
        padding:12px 30px;
        border-radius:10px;
        background:#00bfff;
        color:white;
        font-size:18px;
    }

    /* LOGIN CARD */

    .login-card{
        background: rgba(255,255,255,0.08);
        padding:35px;
        border-radius:20px;
        backdrop-filter: blur(12px);
        box-shadow:0px 0px 20px rgba(0,0,0,0.6);
    }

</style>
""", unsafe_allow_html=True)




st.markdown("""
    <style>

    /* GLOBAL BACKGROUND */

    .stApp{
        background: url("https://s40145.pcdn.co/wp-content/uploads/2025/02/iStock-1397077161-scaled.jpg");
        background-size: cover;
        background-attachment: fixed;
    }

    /* SETTINGS PAGE TITLE */

    h1{
        color:white;
        font-weight:700;
    }

    /* PROFILE CARD */

    .profile-card{
        background: rgba(255,255,255,0.08);
        padding:25px;
        border-radius:15px;
        backdrop-filter: blur(10px);
        box-shadow:0px 5px 20px rgba(0,0,0,0.4);
        color:white;
    }

    /* SETTINGS PANEL */

    .settings-card{
        background: rgba(255,255,255,0.08);
        padding:30px;
        border-radius:15px;
        backdrop-filter: blur(10px);
        box-shadow:0px 5px 20px rgba(0,0,0,0.4);
        color:white;
    }

    /* INPUT BOX */

    .stTextInput>div>div>input{
        background: rgba(255,255,255,0.15);
        color:white;
        border-radius:8px;
    }

    /* SELECT BOX */

    .stSelectbox>div>div{
        background: rgba(255,255,255,0.15);
        border-radius:8px;
    }

    /* BUTTON STYLE */

    .stButton>button{
        background: linear-gradient(90deg,#00c6ff,#0072ff);
        color:white;
        border:none;
        border-radius:8px;
        padding:10px 25px;
        font-weight:600;
        transition:0.3s;
    }

    .stButton>button:hover{
        transform:scale(1.05);
        background: linear-gradient(90deg,#0072ff,#00c6ff);
    }

    /* LOGOUT BUTTON */

    .logout-btn button{
        background:#ff4b4b !important;
        color:white;
        border-radius:10px;
        font-weight:bold;
    }

    /* TABS */

    .stTabs [data-baseweb="tab"]{
        font-size:16px;
        font-weight:600;
    }

    </style>
    """, unsafe_allow_html=True)