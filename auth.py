import streamlit as st
from database import login_user, add_user

def login():

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", key="auth_login_btn"):

        result = login_user(username,password)

        if login_user(username,password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful")

            st.switch_page("pages/🚗 Dashboard.py")

        else:
            st.error("Invalid Login")

    st.markdown('</div>', unsafe_allow_html=True)


def register():

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.title("Create Account")

    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pass")

    if st.button("Register", key="auth_register_btn"):
        add_user(user,pwd)
        st.success("Account created")

    st.markdown('</div>', unsafe_allow_html=True)