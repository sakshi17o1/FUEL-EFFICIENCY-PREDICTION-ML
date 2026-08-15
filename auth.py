import streamlit as st
import streamlit.components.v1 as components

from database import login_user, add_user


# ============================================================
# LOGIN
# ============================================================

def login():

    st.markdown(
        '<div class="glass">',
        unsafe_allow_html=True
    )

    # ========================================================
    # LOGIN FORM
    # ========================================================

    with st.form(
        "login_form",
        clear_on_submit=False
    ):

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        login_pressed = st.form_submit_button(
            "Login"
        )


    # ========================================================
    # USERNAME -> ENTER -> PASSWORD
    #
    # Password -> ENTER -> FORM SUBMISSION
    #
    # The second part is handled naturally by st.form().
    # ========================================================

    components.html(
        """
        <script>

        function setupLoginKeyboard() {

            try {

                const doc = window.parent.document;

                const usernameInput =
                    doc.querySelector(
                        'input[aria-label="Username"]'
                    );

                const passwordInput =
                    doc.querySelector(
                        'input[aria-label="Password"]'
                    );


                /* ============================================
                   USERNAME -> ENTER -> PASSWORD
                   ============================================ */

                if (
                    usernameInput &&
                    passwordInput &&
                    !usernameInput.dataset.enterToPassword
                ) {

                    usernameInput.addEventListener(
                        "keydown",
                        function(event) {

                            if (event.key === "Enter") {

                                event.preventDefault();
                                event.stopPropagation();

                                passwordInput.focus();

                            }

                        }
                    );

                    usernameInput.dataset.enterToPassword =
                        "true";
                }

            }

            catch(error) {

                console.log(
                    "Login keyboard setup:",
                    error
                );

            }

        }


        setTimeout(setupLoginKeyboard, 300);
        setTimeout(setupLoginKeyboard, 800);
        setTimeout(setupLoginKeyboard, 1500);
        setTimeout(setupLoginKeyboard, 2500);

        </script>
        """,
        height=0
    )


    # ========================================================
    # LOGIN ACTION
    # ========================================================

    if login_pressed:

        result = login_user(
            username,
            password
        )

        if result:

            st.session_state["logged_in"] = True
            st.session_state["username"] = username

            st.success(
                "Login successful"
            )

            st.switch_page(
                "pages/🚗 Dashboard.py"
            )

        else:

            st.error(
                "Invalid Login"
            )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# REGISTER
# ============================================================

def register():

    st.markdown(
        '<div class="glass">',
        unsafe_allow_html=True
    )

    st.title(
        "Create Account"
    )


    # ========================================================
    # REGISTER FORM
    # ========================================================

    with st.form(
        "register_form",
        clear_on_submit=False
    ):

        user = st.text_input(
            "Username",
            key="register_username"
        )

        pwd = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        register_pressed = st.form_submit_button(
            "Register"
        )


    # ========================================================
    # USERNAME -> ENTER -> PASSWORD
    #
    # Password -> ENTER -> FORM SUBMISSION
    # ========================================================

    components.html(
        """
        <script>

        function setupRegisterKeyboard() {

            try {

                const doc = window.parent.document;

                const usernameInput =
                    doc.querySelector(
                        'input[aria-label="Username"]'
                    );

                const passwordInput =
                    doc.querySelector(
                        'input[aria-label="Password"]'
                    );


                /* ============================================
                   USERNAME -> ENTER -> PASSWORD
                   ============================================ */

                if (
                    usernameInput &&
                    passwordInput &&
                    !usernameInput.dataset.registerEnter
                ) {

                    usernameInput.addEventListener(
                        "keydown",
                        function(event) {

                            if (event.key === "Enter") {

                                event.preventDefault();
                                event.stopPropagation();

                                passwordInput.focus();

                            }

                        }
                    );

                    usernameInput.dataset.registerEnter =
                        "true";
                }

            }

            catch(error) {

                console.log(
                    "Register keyboard setup:",
                    error
                );

            }

        }


        setTimeout(setupRegisterKeyboard, 300);
        setTimeout(setupRegisterKeyboard, 800);
        setTimeout(setupRegisterKeyboard, 1500);
        setTimeout(setupRegisterKeyboard, 2500);

        </script>
        """,
        height=0
    )


    # ========================================================
    # REGISTER ACTION
    # ========================================================

    if register_pressed:

        add_user(
            user,
            pwd
        )

        st.success(
            "Account created"
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )