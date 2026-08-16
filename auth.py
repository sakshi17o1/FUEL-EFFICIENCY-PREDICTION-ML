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

    # --------------------------------------------------------
    # LOGIN FORM
    # --------------------------------------------------------

    with st.form(
        "login_form",
        clear_on_submit=False,
        enter_to_submit=True
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
            "Login",
            key="auth_login_btn"
        )


    # ========================================================
    # ENTER KEY HANDLING
    # ========================================================

    components.html(
        """
        <script>

        (function() {

            function setupLoginKeyboard() {

                try {

                    const doc = window.parent.document;


                    // EXACT USERNAME INPUT
                    const usernameInput =
                        doc.querySelector(
                            '.st-key-login_username input'
                        );


                    // EXACT PASSWORD INPUT
                    const passwordInput =
                        doc.querySelector(
                            '.st-key-login_password input'
                        );


                    // EXACT LOGIN SUBMIT BUTTON
                    const loginButton =
                        doc.querySelector(
                            '.st-key-auth_login_btn button'
                        );


                    // ==========================================
                    // USERNAME -> ENTER -> PASSWORD
                    // ==========================================

                    if (
                        usernameInput &&
                        passwordInput &&
                        !usernameInput.dataset.enterNavigation
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

                        usernameInput.dataset.enterNavigation =
                            "true";
                    }


                    // ==========================================
                    // PASSWORD -> ENTER -> LOGIN
                    // ==========================================

                    if (
                        passwordInput &&
                        loginButton &&
                        !passwordInput.dataset.enterNavigation
                    ) {

                        passwordInput.addEventListener(
                            "keydown",
                            function(event) {

                                if (event.key === "Enter") {

                                    event.preventDefault();
                                    event.stopPropagation();

                                    loginButton.click();

                                }

                            }
                        );

                        passwordInput.dataset.enterNavigation =
                            "true";
                    }

                }

                catch(error) {

                    console.log(
                        "Login keyboard error:",
                        error
                    );

                }

            }


            // Streamlit renders widgets asynchronously
            setTimeout(setupLoginKeyboard, 200);
            setTimeout(setupLoginKeyboard, 500);
            setTimeout(setupLoginKeyboard, 1000);
            setTimeout(setupLoginKeyboard, 2000);
            setTimeout(setupLoginKeyboard, 3000);

        })();

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


    # --------------------------------------------------------
    # REGISTER FORM
    # --------------------------------------------------------

    with st.form(
        "register_form",
        clear_on_submit=False,
        enter_to_submit=True
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
            "Register",
            key="auth_register_btn"
        )


    # ========================================================
    # ENTER KEY HANDLING
    # ========================================================

    components.html(
        """
        <script>

        (function() {

            function setupRegisterKeyboard() {

                try {

                    const doc = window.parent.document;


                    // EXACT REGISTER USERNAME INPUT
                    const usernameInput =
                        doc.querySelector(
                            '.st-key-register_username input'
                        );


                    // EXACT REGISTER PASSWORD INPUT
                    const passwordInput =
                        doc.querySelector(
                            '.st-key-register_password input'
                        );


                    // EXACT REGISTER SUBMIT BUTTON
                    const registerButton =
                        doc.querySelector(
                            '.st-key-auth_register_btn button'
                        );


                    // ==========================================
                    // USERNAME -> ENTER -> PASSWORD
                    // ==========================================

                    if (
                        usernameInput &&
                        passwordInput &&
                        !usernameInput.dataset.enterNavigation
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

                        usernameInput.dataset.enterNavigation =
                            "true";
                    }


                    // ==========================================
                    // PASSWORD -> ENTER -> REGISTER
                    // ==========================================

                    if (
                        passwordInput &&
                        registerButton &&
                        !passwordInput.dataset.enterNavigation
                    ) {

                        passwordInput.addEventListener(
                            "keydown",
                            function(event) {

                                if (event.key === "Enter") {

                                    event.preventDefault();
                                    event.stopPropagation();

                                    registerButton.click();

                                }

                            }
                        );

                        passwordInput.dataset.enterNavigation =
                            "true";
                    }

                }

                catch(error) {

                    console.log(
                        "Register keyboard error:",
                        error
                    );

                }

            }


            // Streamlit renders widgets asynchronously
            setTimeout(setupRegisterKeyboard, 200);
            setTimeout(setupRegisterKeyboard, 500);
            setTimeout(setupRegisterKeyboard, 1000);
            setTimeout(setupRegisterKeyboard, 2000);
            setTimeout(setupRegisterKeyboard, 3000);

        })();

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