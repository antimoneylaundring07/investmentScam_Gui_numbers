import streamlit as st

st.set_page_config(page_title="Admin", layout="wide")

# Check if user is logged in
if not st.session_state.get("token"):
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Check if user is admin
user = st.session_state.get("user", {})
if user.get("role") != "admin":
    st.error("❌ You don't have access to this page. Admin role required.")
    st.stop()

st.title("⚙️ Admin Panel")

st.subheader("Admin Controls")
st.info("Add admin-specific features here - user management, reports, system settings, etc.")

# Example admin features
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Users", "0", help="Fetch from Supabase")

with col2:
    st.metric("Active Sessions", "0")

with col3:
    st.metric("System Health", "✅ Good")

st.divider()

st.subheader("📋 User Management")
st.write("Add user management features here")
