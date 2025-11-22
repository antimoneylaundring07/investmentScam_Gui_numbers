import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from api.backend_client import BackendClient

st.set_page_config(page_title="Login", layout="centered")

# Hide sidebar
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
        div[data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Initialize cookies
cookies = EncryptedCookieManager(
    prefix="myapp_",
    password="987@%#@#958"  # Change this
)

if not cookies.ready():
    st.stop()

# Session keys
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

# Restore from cookies
if cookies.get("token"):
    st.session_state.token = cookies["token"]
    st.session_state.user = {"username": cookies.get("username", "User")}

# Redirect if logged in
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
        # Save to session
        st.session_state.token = data["token"]
        st.session_state.user = data["user"]
        
        # Save to cookies
        cookies["token"] = data["token"]
        cookies["username"] = data["user"]["username"]
        cookies.save()
        
        st.success("Login successful!")
        st.rerun()
    else:
        st.error(data.get("message", "Login failed"))
