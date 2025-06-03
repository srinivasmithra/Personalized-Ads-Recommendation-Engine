import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.title("Login")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Log In")

if submit:
    if not username or not password:
        st.warning("Please enter both username and password.")
    else:
        try:
            payload = {"username": username, "password": password}
            res = requests.post(f"{API_BASE}/auth/login", json=payload)

            if res.status_code == 200:
                token = res.json().get("access_token")
                st.session_state["token"] = token
                st.session_state["username"] = username
                st.success("Login successful. Go to Logi Page...")
                st.switch_page("pages/Feed.py")
            else:
                st.error(res.json().get("detail", "Invalid credentials"))
        except Exception as e:
            st.error(f"Error: {e}")
