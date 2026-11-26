from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import Filter, FieldCondition, MatchValue

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

def search_documents(
    query_embedding: list[float],
    user_id: int,
    resume_id: int | None = None,
    project_name: str | None = None,
    section: str | None = None,
    limit: int = 5
):
    conditions = [
        FieldCondition(
            key="user_id",
            match=MatchValue(value=user_id)
        )
    ]

    if resume_id is not None:
        conditions.append(
            FieldCondition(
                key="resume_id",
                match=MatchValue(value=resume_id)
            )
        )

    if project_name is not None:
        conditions.append(
            FieldCondition(
                key="project_name",
                match=MatchValue(value=project_name)
            )
        )

    if section is not None:
        conditions.append(
            FieldCondition(
                key="section",
                match=MatchValue(value=section)
            )
        )

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=Filter(must=conditions),
        limit=limit,
        with_payload=True
    ).points

    return results


def get_resume_projects(
    user_id: int,
    resume_id: int
) -> list[str]:

    conditions = [
        FieldCondition(
            key="user_id",
            match=MatchValue(value=user_id)
        ),
        FieldCondition(
            key="resume_id",
            match=MatchValue(value=resume_id)
        ),
        FieldCondition(
            key="section",
            match=MatchValue(value="PROJECTS")
        )
    ]

    records, _ = qdrant_client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(must=conditions),
        with_payload=True,
        limit=100
    )

    project_names = {
        record.payload["project_name"]
        for record in records
        if record.payload
        and record.payload.get("project_name")
    }

    return list(project_names)
