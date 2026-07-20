from sentence_transformers import SentenceTransformer

print("Loading SentenceTransformer model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model Loaded Successfully")

def get_embedding(text):
    print("Encoding:", text[:40])
    return model.encode(text, convert_to_tensor=True)