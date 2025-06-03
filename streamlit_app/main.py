import streamlit as st

st.set_page_config(page_title="AdFusion")

st.title("AdFusion: Personalized Recommendations in Entertainment Content")

st.markdown("""
**AdFusion** is a proof-of-concept system that integrates personalized product recommendations into a dynamic visual feed.

### Key Features:
- Presents a stream combining curated photos and recommended products.
- Learns from user interests and search history to personalize content.
- Stores session data to support ongoing, user-specific recommendations.

### Technology Overview:
- Uses the `all-MiniLM-L6-v2` model from Sentence-Transformers for semantic similarity.
- Computes recommendations based on embedding similarity between user intent and product metadata.
- Employs FAISS for efficient Approximate Nearest Neighbors (ANN) search over product embeddings.
- Caches personalized recommendations to improve performance and scalability.
- Exploratory (non-personalized) products are also included to encourage discovery.

Use the sidebar to log in or sign up and begin exploring the personalized feed.
""")
