import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Your Feed", layout="wide")
st.title("Your Personalized Feed")

# Check login
if "token" not in st.session_state:
    st.warning("You must be logged in to view your feed.")
    st.stop()

# Initialize page number
if "page" not in st.session_state:
    st.session_state["page"] = 1

# API headers
headers = {"Authorization": f"Bearer {st.session_state['token']}"}
params = {"page": st.session_state["page"]}

with st.spinner("Loading your feed..."):
    try:
        res = requests.get(f"{API_BASE}/recommend/stream", headers=headers, params=params)

        if res.status_code == 200:
            data = res.json()
            stream = data.get("stream", [])

            if not stream:
                st.info("Nothing to show right now.")
            else:
                for item in stream:
                    if item["type"] == "photo":
                        photo = item["data"]
                        st.image(photo["image_url"], caption=photo["alt"], use_container_width=True)
                        st.markdown(f"📸 *Photographer:* [{photo['photographer']}]({photo.get('pexels_url', '#')})")
                        st.markdown("---")

                    elif item["type"] == "product":
                        prod = item["data"]
                        st.markdown(f"### 🛍️ {prod['name']}")
                        st.image(prod["image_url"], width=300)
                        st.write(f"**Price:** {prod['price']}")
                        st.write(f"**Category:** {prod['category']}")
                        st.write(f"**Rating:** {prod['average_rating']}")
                        st.write(f"**Brand:** {prod['brand']}")
                        st.write(prod["description"])
                        st.markdown("----")

        else:
            try:
                st.error(res.json().get("detail", "Failed to load stream"))
            except Exception:
                st.error("Server returned an unexpected error.")

    except Exception as e:
        st.error(f"Error fetching feed: {e}")

# Load More
if st.button("🔄 Load More"):
    st.session_state["page"] += 1
    st.rerun()

# Logout
if st.button("🚪 Logout"):
    for key in ["token", "username", "page"]:
        st.session_state.pop(key, None)
    st.success("Logged out.")
    st.switch_page("pages/Login.py")
