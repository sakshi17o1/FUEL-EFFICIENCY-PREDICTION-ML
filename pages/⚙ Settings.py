import streamlit as st
from style import load_css
from database import update_username, update_password, login_user

load_css()

st.title("⚙ Settings")

st.markdown('<div class="settings-card">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "Update Profile",
    "Change Password",
    "App Preferences"
])

# ---------------- PROFILE UPDATE ----------------
with tab1:

    st.subheader("👤 User Profile")

    st.write("**Current Username:**", st.session_state["username"])
    st.write("**Account Status:** Active")
    st.write("**Role:** User")

    st.write("")
    new_username = st.text_input("Enter New Username")

    if st.button("Save Profile", key="save_profile"):

        if new_username != "":

            update_username(st.session_state["username"], new_username)

            st.session_state["username"] = new_username

            st.success("Username Updated Successfully ✅")

        else:
            st.error("Please enter a new username")


# ---------------- PASSWORD CHANGE ----------------
with tab2:

    st.subheader("🔑 Change Password")

    old_pass = st.text_input("Old Password", type="password")
    new_pass = st.text_input("New Password", type="password")
    confirm_pass = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password", key="update_pass"):

        # verify old password
        if login_user(st.session_state["username"], old_pass):

            if new_pass == confirm_pass:

                update_password(st.session_state["username"], new_pass)

                st.success("Password Updated Successfully 🔐")

            else:
                st.error("New passwords do not match")

        else:
            st.error("Old password is incorrect")


# ---------------- APP PREFERENCES ----------------
with tab3:

    st.subheader("🎨 Application Preferences")

    theme = st.selectbox("Theme", ["Dark", "Light"])
    notifications = st.toggle("Enable Notifications")

    if st.button("💾 Save Preferences", key="save_pref"):

        st.success("Preferences Saved Successfully")

    st.write("")

    # -------- LOGOUT BUTTON --------
    if st.button("🚪 Logout", key="logout_btn"):

        st.session_state.clear()
        st.switch_page("app.py")

st.markdown('</div>', unsafe_allow_html=True)


# -------- BACKGROUND STYLE --------
st.markdown("""
<style>

.stApp{
background: url("https://earth.org/wp-content/uploads/2018/05/Kevin-Pereira-AI-consulting-Blu-Artificial-Intelligence-Hive-Life-1--1200x900.jpg");
background-size: cover;
background-attachment: fixed;
}

</style>
""", unsafe_allow_html=True)