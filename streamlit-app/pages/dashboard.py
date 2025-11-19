import streamlit as st
from api.backend_client import BackendClient

st.set_page_config(page_title="Dashboard", layout="wide")

# Check if user is logged in
if not st.session_state.get("token"):
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# User info
user = st.session_state.get("login", {})

col1, col2 = st.columns([3, 1])
with col1:
    st.title(f"👋 Welcome, {user.get('name', 'User')}!")

with col2:
    if st.button("🚪 Logout"):
        client = BackendClient()
        client.logout()
        st.session_state.token = None
        st.session_state.user = None
        st.success("✅ Logged out successfully!")
        st.switch_page("app.py")

st.divider()

# Dashboard content
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("User ID", user.get("id", "N/A"))

with col2:
    st.metric("Email", user.get("email", "N/A"))

with col3:
    st.metric("Role", user.get("role", "user").upper())

st.divider()

st.subheader("📊 Dashboard Content")
st.info("Add your dashboard content here - charts, tables, data visualization, etc.")

# Example: Display profile info
if st.button("Refresh Profile"):
    client = BackendClient()
    data, status = client.get_profile()
    if status == 200:
        st.json(data)
    else:
        st.error("Failed to fetch profile")
