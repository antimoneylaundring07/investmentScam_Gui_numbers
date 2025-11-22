import streamlit as st
from api.backend_client import BackendClient

st.set_page_config(page_title="Login", layout="centered")

# Hide sidebar on login screen
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
        div[data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Session keys setup
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

# Check query params for existing session
try:
    params = st.query_params.to_dict()
    if params.get("token") and params.get("username"):
        st.session_state.token = params["token"]
        st.session_state.user = {"username": params["username"]}
except:
    pass

# If already logged in, redirect to dashboard
if st.session_state.token:
    st.switch_page("pages/dashboard.py")
    st.stop()

st.title("🔐 Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

client = BackendClient()

if st.button("Login"):
    data, status = client.login(username, password)
    if status == 200 and data.get("token"):
        st.session_state.token = data["token"]
        st.session_state.user = data["user"]
        
        # Set query params
        st.query_params.update({
            "token": data["token"],
            "username": data["user"]["username"]
        })
        
        st.success("Login successful!")
        st.rerun()
    else:
        st.error(data.get("message", "Login failed"))
