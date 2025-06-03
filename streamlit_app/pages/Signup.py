import streamlit as st
import requests

from utils.us_states import US_STATES #us states

BACKEND_URL = "http://localhost:8000"

st.title("Signup - AdFusion")

# Form
with st.form("signup_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    age = st.number_input("Age", min_value=13, max_value=100)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    region = st.selectbox("Region (US)",US_STATES)
    interests = st.text_input("Your Interests (comma-separated)", help="e.g. gardening, fitness, cooking")
    search_history = st.text_input("Looking for discount products to buy (comma-separated)", help="e.g. mobile phones, perfumes")
    submit_btn = st.form_submit_button("Sign Up")

if submit_btn:
    # Validate inputs
    if not username or not password:
        st.error("Username and password are required.")
    elif "," not in interests or "," not in search_history:
        st.error("Please enter comma-separated values for interests and search history.")
    else:
        # Build request payload
        payload = {
            "username": username,
            "password": password,
            "age": age,
            "gender": gender,
            "region": region,
            "interests": interests,
            "search_history": search_history
        }

        try:
            # Call /auth/signup
            r = requests.post(f"{BACKEND_URL}/auth/signup", json=payload)
            if r.status_code == 200:
                st.success("Signup successful! Logging you in...")

                # Auto-login
                login_payload = {"username": username, "password": password}
                login_res = requests.post(f"{BACKEND_URL}/auth/login", data=login_payload)

                if login_res.status_code == 200:
                    token = login_res.json().get("access_token")
                    st.session_state["token"] = token
                    st.session_state["username"] = username
                    st.success("Taking to login page!")
                    st.switch_page("pages/Login.py")
                else:
                    st.error("Signup succeeded but login failed.")

            else:
                st.error(f"Signup failed: {r.json().get('detail')}")
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
