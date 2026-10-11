
from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import search_documents

query = "What skills and technologies are in my resume?"

embedding = generate_embedding(query)

results = search_documents(
    query_embedding=embedding,
    user_id=7,
    resume_id=23,
    limit=5
)

print("Query:", query)
print("Results found:", len(results))

for result in results:
    print(
        "Score:", round(result.score, 4),
        "| Chunk:", result.payload.get("chunk_index"),
        "| Resume ID:", result.payload.get("resume_id")
    )
