from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-m3"

embedding_model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str):
    embedding = embedding_model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()
