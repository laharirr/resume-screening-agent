from sentence_transformers.util import cos_sim
from similarity.embeddings import get_embedding


def semantic_similarity(text1, text2):
    """
    Calculate semantic similarity between two texts.
    """
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)

    score = cos_sim(emb1, emb2)

    return float(score.item()) * 100