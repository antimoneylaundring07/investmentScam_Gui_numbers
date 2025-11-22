import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

# Restore session from query params if needed
try:
    params = st.query_params.to_dict()
    if "token" not in st.session_state or st.session_state.token is None:
        if params.get("token") and params.get("username"):
            st.session_state.token = params["token"]
            st.session_state.user = {"username": params["username"]}
except:
    pass

# Check if logged in
if "token" not in st.session_state or st.session_state.token is None:
    st.switch_page("app.py")
    st.stop()

# Sidebar with logout
with st.sidebar:
    st.write(f"**Logged in as:**")
    st.write(f"👤 {st.session_state.user['username']}")
    st.write("---")
    
    if st.button("🚪 Logout", type="primary", use_container_width=True):
        st.session_state.token = None
        st.session_state.user = None
        st.query_params.clear()
        st.success("Logged out!")
        st.rerun()

# Main content
st.header(f"Welcome, {st.session_state.user['username']}")
st.subheader("Dashboard Page Loaded Successfully!")

st.write("")
st.write("Dashboard content goes here...")
