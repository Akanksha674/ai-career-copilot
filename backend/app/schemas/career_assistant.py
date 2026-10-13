from pydantic import BaseModel

class CareerQuestionRequest(BaseModel):
    question: str
    resume_id: int

class CareerAnswerResponse(BaseModel):
    answer: str