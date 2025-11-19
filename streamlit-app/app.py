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

# Only Login (no tabs, register removed)
st.subheader("Login to your account")
username = st.text_input("username", key="login_username")
password = st.text_input("password", type="password", key="login_password")

if st.button("Login", type="primary"):
    if username and password:
        client = BackendClient()
        data, status = client.login(username, password)
        
        if status == 200:
            st.session_state.token = data.get("token")
            st.session_state.user = data.get("user")
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error(f"❌ Login failed: {data.get('message', 'Unknown error')}")
    else:
        st.warning("⚠️ Please enter username and password")
