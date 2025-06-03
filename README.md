
# AdFusion: Personalized Product Recommendations Inside Entertainment Content

AdFusion is a scalable system that integrates AI-driven product recommendations into visual entertainment streams (like photo feeds). It uses semantic similarity via transformer embeddings and FAISS-based approximate nearest neighbor (ANN) search to recommend highly relevant products to each user.

---

## 🗂 Project Structure

```

AdFusion/
├── app/
│   ├── api/                  # FastAPI routes
│   ├── db/                   # MongoDB methods & config
│   ├── models/               # Recommendation logic (semantic, FAISS, etc.)
│   ├── main.py               # FastAPI entrypoint
│
├── streamlit\_app/
│   ├── pages/
│   │   ├── Feed.py           # User interface for feed
│   ├── main.py               # Streamlit launcher
│
├── sample\_data/
│   ├── products.json         # Sample products (30)
│   ├── photos.json           # Sample photos (40)
│
├── faiss\_index/
│   ├── product\_index.faiss   # FAISS index file (generated)
│   ├── product\_id\_map.pkl    # Mapping for ANN search
│
├── requirements.txt
├── README.md

````

---

## ⚙️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: MongoDB
- **ML/NLP**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **ANN Search**: FAISS
- **Authentication**: JWT
- **Data Sources**: Curated product + photo dataset

---

## 💡 Features

- Personalized product recommendations for every user
- FAISS-powered semantic search for fast and accurate results
- Lazy personalization using background tasks
- Session-based photo-product interleaving in user feed
- JWT-secured login and signup system

---

## 🚀 Getting Started (Run Locally)

1. **Clone This Repository**
   ```bash
   git clone https://github.com/your-username/adfusion.git
   cd adfusion
````

2. **Install Dependencies**
   *(Recommended: create a virtual environment)*

   ```bash
   pip install -r requirements.txt
   ```

3. **MongoDB Setup**

   * Ensure MongoDB is running locally.
   * Import sample data into your local DB:

     ```bash
     mongoimport --db adfusion --collection products --file sample_data/products.json --jsonArray
     mongoimport --db adfusion --collection photos --file sample_data/photos.json --jsonArray
     ```

4. **Build FAISS Index (Run Once)**

   ```bash
   python app/models/helper/build_faiss_index.py
   ```

5. **Run FastAPI Backend**
   From the project root:

   ```bash
   uvicorn app.main:app --reload
   ```

6. **Run Streamlit Frontend**
   From the `streamlit_app/` folder:

   ```bash
   streamlit run main.py
   ```

7. **Visit in Browser**
   Open [http://localhost:8501](http://localhost:8501)

---

## 📦 Sample Data

You can find demo-ready data under:

* `sample_data/products.json` – 30 sample products
* `sample_data/photos.json` – 40 sample photos

Users can be created through the web UI (signup page). Products are embedded and indexed once via FAISS.
