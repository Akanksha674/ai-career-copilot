from pydantic import BaseModel


class ConversationCreateRequest(BaseModel):
    resume_id: int
    title: str = "New Conversation"