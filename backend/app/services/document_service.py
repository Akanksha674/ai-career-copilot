
from uuid import uuid4

from qdrant_client.models import PointStruct
from app.services.chunking_service import split_text_into_chunks
from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import (
    qdrant_client,
    COLLECTION_NAME
)


def store_document(
    text: str,
    user_id: int,
    resume_id: int,
    filename: str
) -> int:
    chunks = split_text_into_chunks(text)

    if not chunks:
        return 0

    points = []

    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "user_id": user_id,
                    "resume_id": resume_id,
                    "filename": filename,
                    "chunk_index": index,
                    "text": chunk
                }
            )
        )

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return len(points)
