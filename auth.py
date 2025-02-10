import streamlit as st
from database import Database

class Authentication:
    def __init__(self):
        self.db = Database()

    def login_form(self):
        st.markdown("""
        <style>
        .auth-form {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=True):
            st.subheader("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                user = self.db.verify_user(email, password)
                if user:
                    st.session_state['user_id'] = user[0]
                    st.session_state['user_email'] = user[1]
                    st.session_state['authenticated'] = True
                    return True
                else:
                    st.error("Invalid credentials")
                    return False

    def register_form(self):
        with st.form("register_form", clear_on_submit=True):
            st.subheader("Register")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")

            if submit:
                if password != confirm_password:
                    st.error("Passwords do not match")
                    return False
                
                if self.db.add_user(email, password):
                    st.success("Registration successful! Please login.")
                    return True
                else:
                    st.error("Email already exists")
                    return False

    def logout(self):
        st.session_state['authenticated'] = False
        st.session_state['user_id'] = None
        st.session_state['user_email'] = None
