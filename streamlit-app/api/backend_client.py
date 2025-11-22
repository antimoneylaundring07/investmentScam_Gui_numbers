import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Backend API configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

class BackendClient:
    def __init__(self, base_url=BACKEND_URL):
        self.base_url = base_url
        self.token = st.session_state.get("token", None)
    
    def _get_headers(self, token=None):  # ✅ Add token parameter
        headers = {"Content-Type": "application/json"}
        # Use provided token OR self.token
        auth_token = token if token else self.token
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        return headers
    
    def register(self, email, password, name):
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json={"email": email, "password": password, "name": name},
                headers=self._get_headers()
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"message": str(e)}, 500
    
    def login(self, username, password):
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"username": username, "password": password},
                headers=self._get_headers(),
                timeout=10
            )
            try:
                data = response.json()
            except ValueError:
                raw = response.text.strip()
                msg = raw or f"Empty response (status {response.status_code})"
                return {"message": msg, "raw": raw}, response.status_code
            
            return data, response.status_code
        except requests.exceptions.RequestException as e:
            return {"message": str(e)}, 500
    
    def logout(self):
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/logout",
                headers=self._get_headers()
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_profile(self):
        try:
            response = requests.get(
                f"{self.base_url}/api/profile",
                headers=self._get_headers()
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def get_dashboard_data(self, token):
        """Fetch dashboard data"""
        try:
            response = requests.get(
                f"{self.base_url}/api/dashboard",
                headers=self._get_headers(token),  # ✅ Now this will work
                timeout=10
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
