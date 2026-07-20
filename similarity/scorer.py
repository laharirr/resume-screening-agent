from sentence_transformers.util import cos_sim
from similarity.embeddings import get_embedding


def semantic_similarity(text1, text2):
    print("Generating embedding 1...")
    emb1 = get_embedding(text1)

    print("Generating embedding 2...")
    emb2 = get_embedding(text2)

    print("Calculating cosine similarity...")
    score = cos_sim(emb1, emb2)

    print("Similarity Done")

    return float(score.item()) * 100
