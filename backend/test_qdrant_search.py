
from app.services.rag_service import answer_resume_question

question = "What skills and technologies are mentioned in my resume?"

answer = answer_resume_question(
    question=question,
    user_id=7,
    resume_id=23
)

print("\nQuestion:", question)
print("\nAI Career Assistant Answer:\n")
print(answer)
