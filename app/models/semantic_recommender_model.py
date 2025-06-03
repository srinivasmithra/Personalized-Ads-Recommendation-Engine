from sentence_transformers import SentenceTransformer, util

# Load SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """Returns a sentence embedding for a given input text."""
    return model.encode(text, convert_to_tensor=True)

def compute_similarity(embedding1, embedding2):
    """Computes cosine similarity between two tensors."""
    return float(util.cos_sim(embedding1, embedding2)[0][0])

def embed_user(user: dict) -> str:
    """Combine interests and search history into a single input string."""
    interests = user.get("interests", [])
    search_history = user.get("search_history", [])
    return " ".join(interests + search_history)

def embed_product(product: dict) -> str:
    """Extract relevant product text (name + cleaned tags + category)."""
    text_parts = []
    if "name" in product:
        text_parts.append(product["name"])
    if isinstance(product.get("tags"), str):
        cleaned_tags = product["tags"].replace("âº", ">").replace("›", ">")
        text_parts.extend([tag.strip().lower() for tag in cleaned_tags.split(">")])
    if len(text_parts) == 0:
        if "category" in product:
            text_parts.append(product["category"])
    return " ".join(text_parts)
