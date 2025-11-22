import streamlit as st

st.set_page_config(page_title="Admin", layout="wide")

# Page gating via query param
params = st.query_params
if params.get("page", [""])[0] != "admin":
    st.stop()

# Check if user is logged in
if not st.session_state.get("token"):
    st.warning("⚠️ Please login first")
    page = st.query_params.get("page", "login")
    st.query_params["page"] = "login"
    st.rerun()

# Check if user is admin
user = st.session_state.get("user", {})
if user.get("role") != "admin":
    st.error("❌ You don't have access to this page. Admin role required.")
    st.stop()

st.header(f"Admin panel - {user.get('username')}")
st.subheader("Admin Controls")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Users", "0", help="Fetch from Supabase")
with col2:
    st.metric("Active Sessions", "0")
with col3:
    st.metric("System Health", "✅ Good")

st.divider()
st.subheader("📋 Admin Actions")
st.write("Add admin features here")