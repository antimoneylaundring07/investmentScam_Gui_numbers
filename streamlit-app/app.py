import streamlit as st
from api.backend_client import BackendClient

st.set_page_config(page_title="Login", layout="centered")

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

# If already logged in, redirect to dashboard
if st.session_state.token:
    st.switch_page("pages/dashboard.py")

st.title("🔐 Login")

# Tabs for login/register
tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.subheader("Login to your account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", type="primary"):
        if email and password:
            client = BackendClient()
            data, status = client.login(email, password)

            if status == 200:
                st.session_state.token = data.get("token")
                st.session_state.user = data.get("user")
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error(f"❌ Login failed: {data.get('message', 'Unknown error')}")
        else:
            st.warning("⚠️ Please enter email and password")

with tab2:
    st.subheader("Create a new account")
    name = st.text_input("Full Name")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register", type="primary"):
        if not all([name, email, password, confirm_password]):
            st.warning("⚠️ Please fill all fields")
        elif password != confirm_password:
            st.error("❌ Passwords do not match")
        else:
            client = BackendClient()
            data, status = client.register(email, password, name)

            if status == 201:
                st.session_state.token = data.get("token")
                st.session_state.user = data.get("user")
                st.success("✅ Registration successful!")
                st.rerun()
            else:
                st.error(f"❌ Registration failed: {data.get('message', 'Unknown error')}")
