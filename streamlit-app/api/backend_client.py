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

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
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
            return {"error": str(e)}, 500

    def login(self, email, password):
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"email": email, "password": password},
                headers=self._get_headers()
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500

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
