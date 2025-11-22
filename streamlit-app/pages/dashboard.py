import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from api.backend_client import BackendClient
import pandas as pd

st.set_page_config(page_title="Dashboard", layout="wide")

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
        st.switch_page("app.py")
        st.stop()

# Sidebar logout
with st.sidebar:
    st.write(f"**Logged in as:**")
    st.write(f"👤 {st.session_state.user['username']}")
    st.write("---")
    
    if st.button("🚪 Logout", type="primary", use_container_width=True):
        st.session_state.token = None
        st.session_state.user = None
        cookies["token"] = ""
        cookies["username"] = ""
        cookies.save()
        st.success("Logged out!")
        st.rerun()

# Main content
st.subheader("Dashboard")

# Fetch dashboard data
with st.spinner("Loading dashboard data..."):
    client = BackendClient()
    data, status = client.get_dashboard_data(st.session_state.token)

if status == 200 and data.get("data"):
    dashboard_items = data["data"]
    
    if len(dashboard_items) > 0:
        # Display table only
        # st.write("### 📋 Data Table")
        df = pd.DataFrame(dashboard_items)
        st.dataframe(df, use_container_width=True, hide_index=True, height=497)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="dashboard_data.csv",
            mime="text/csv"
        )
    else:
        st.info("No data available. Add data to 'numbers' table in Supabase.")
        
elif status == 401:
    st.error("Session expired. Please login again.")
    st.session_state.token = None
    st.session_state.user = None
    cookies["token"] = ""
    cookies["username"] = ""
    cookies.save()
    st.switch_page("app.py")
else:
    st.error(f"❌ Failed to load dashboard data: {data.get('message', 'Unknown error')}")
    st.info("💡 Make sure your backend is running and Supabase table exists.")
