import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from api.backend_client import BackendClient
import pandas as pd

st.set_page_config(page_title="Admin - View All", layout="wide")

# Initialize cookies
cookies = EncryptedCookieManager(
    prefix="myapp_",
    password="987@%#@#958"
)

if not cookies.ready():
    st.stop()

# Restore session
if "token" not in st.session_state or st.session_state.token is None:
    if cookies.get("token"):
        st.session_state.token = cookies["token"]
        st.session_state.user = {"username": cookies.get("username", "User")}
    else:
        st.error("🔒 Please login first")
        st.markdown('<meta http-equiv="refresh" content="0; url=/" />', unsafe_allow_html=True)
        st.stop()

# Sidebar
with st.sidebar:
    st.write(f"**Logged in as:**")
    st.write(f"👤 {st.session_state.user['username']}")
    
    st.write("---")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.session_state.user = None
        cookies["token"] = ""
        cookies["username"] = ""
        cookies.save()
        st.success("Logged out!")
        st.markdown('<meta http-equiv="refresh" content="1; url=/" />', unsafe_allow_html=True)
        st.stop()

# Main content
st.subheader("Dashboard")
# st.caption("Read-only view of all columns. Go to Dashboard to edit.")

# Fetch data
with st.spinner("Loading all data..."):
    client = BackendClient()
    data, status = client.get_dashboard_data(st.session_state.token)

if status == 200 and data.get("data"):
    dashboard_items = data["data"]
    
    if len(dashboard_items) > 0:
        # Display ALL columns as read-only dataframe
        df = pd.DataFrame(dashboard_items)
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=600
        )
        
        st.write("---")
        
        # Download ALL columns
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download All Data (CSV)",
            data=csv,
            file_name="all_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No data available.")
        
elif status == 401:
    st.error("Session expired. Please login again.")
    st.session_state.token = None
    st.session_state.user = None
    cookies["token"] = ""
    cookies["username"] = ""
    cookies.save()
    st.markdown('<meta http-equiv="refresh" content="0; url=/" />', unsafe_allow_html=True)
else:
    st.error(f"❌ Failed to load data: {data.get('message', 'Error')}")
