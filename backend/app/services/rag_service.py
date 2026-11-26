
import ollama
from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import search_documents
from app.services.qdrant_service import (
    search_documents,
    get_resume_projects
)

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


def detect_resume_section(question: str) -> str | None:
    question = question.lower()

    if "technical skills" in question or "skills" in question:
        return "TECHNICAL SKILLS"

    if "education" in question or "degree" in question:
        return "EDUCATION"

    if "certification" in question or "achievement" in question:
        return "CERTIFICATIONS & ACHIEVEMENTS"

    if "experience" in question:
        return "TECHNICAL EXPERIENCE"

    if "project" in question:
        return "PROJECTS"

    if "summary" in question:
        return "PROFESSIONAL SUMMARY"

    return None


def detect_resume_project(
    question: str,
    user_id: int,
    resume_id: int
) -> str | None:

    projects = get_resume_projects(
        user_id=user_id,
        resume_id=resume_id
    )

    question_lower = question.lower()

    for project in projects:
        project_lower = project.lower()

        project_core_name = project_lower.split("—")[0].strip()
        project_core_name = project_core_name.split("-")[0].strip()

        if project_core_name in question_lower:
            return project

    return None


def answer_resume_question(
    question: str,
    user_id: int,
    resume_id: int,
    project_name: str | None = None,
    section: str | None = None
) -> str:
    if section is None:
        section = detect_resume_section(question)
    if project_name is None:
        project_name = detect_resume_project(
            question=question,
            user_id=user_id,
            resume_id=resume_id
        )
    # Step 1: Convert the question into an embedding
    query_embedding = generate_embedding(question)

    # Step 2: Retrieve relevant chunks from this user's resume
    results = search_documents(
        query_embedding=query_embedding,
        user_id=user_id,
        resume_id=resume_id,
        project_name=project_name,
        section=section,
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
