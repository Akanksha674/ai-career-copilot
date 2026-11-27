from pydantic import BaseModel


class CareerQuestionRequest(BaseModel):
    question: str
    conversation_id: int


class CareerAnswerResponse(BaseModel):
    answer: str