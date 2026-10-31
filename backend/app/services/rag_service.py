
import ollama
from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import search_documents


def generate_rag_answer(
    question: str,
    context_chunks: list[str]
) -> str:

    if not context_chunks:
        return (
            "I couldn't find relevant information in your resume "
            "to answer this question."
        )

    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI Career Assistant that answers questions
based on a user's resume.

STRICT GROUNDING RULES:

1. Use only the information provided in the retrieved
   resume context.

2. Do not use external knowledge, assumptions, or
   information from other projects.

3. Keep each project's technologies, responsibilities,
   achievements, and descriptions separate.

4. Mention a technology as part of a specific project
   only when the retrieved context explicitly connects
   that technology to that project.

5. Never invent skills, qualifications, experience,
   project details, metrics, or achievements.

6. If the retrieved context does not contain enough
   information, clearly state that the information
   is not available in the provided resume context.

7. If information is available, provide a clear,
   relevant, and professional answer.

Retrieved resume context:
{context}

User question:
{question}

Answer:
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()



def answer_resume_question(
    question: str,
    user_id: int,
    resume_id: int
) -> str:
    # Step 1: Convert the question into an embedding
    query_embedding = generate_embedding(question)

    # Step 2: Retrieve relevant chunks from this user's resume
    results = search_documents(
        query_embedding=query_embedding,
        user_id=user_id,
        resume_id=resume_id,
        limit=5
    )

    # Step 3: Extract the retrieved text
    context_chunks = [
        result.payload["text"]
        for result in results
        if result.payload and result.payload.get("text")
    ]

    # Step 4: Generate an answer using the retrieved context
    return generate_rag_answer(
        question=question,
        context_chunks=context_chunks
    )
