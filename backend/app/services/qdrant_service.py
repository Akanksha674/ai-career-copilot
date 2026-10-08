from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

COLLECTION_NAME = "career_copilot_documents"

qdrant_client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT
)


def create_collection():
    existing_collections = qdrant_client.get_collections().collections

    collection_names = [
        collection.name for collection in existing_collections
    ]

    if COLLECTION_NAME not in collection_names:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1024,
                distance=Distance.COSINE
            )
        )

        print(f"Collection '{COLLECTION_NAME}' created.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")