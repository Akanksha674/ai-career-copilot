from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreateRequest
from app.schemas.career_assistant import (
    CareerQuestionRequest,
    CareerAnswerResponse
    )
from app.services.rag_service import answer_resume_question

router = APIRouter(
    prefix="/career-assistant",
    tags=["Career Assistant"]
    )

@router.post(
    "/ask",
    response_model=CareerAnswerResponse
    )
def ask_career_assistant(
    request: CareerQuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = (
        db.query(Resume)
            .filter(
                Resume.id == request.resume_id,
                Resume.user_id == current_user.id
            )
            .first()
    )
    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )
    answer = answer_resume_question(
        question=request.question,
        user_id=current_user.id,
        resume_id=resume.id
    )

    return CareerAnswerResponse(answer=answer)

@router.post("/conversations")
def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    conversation = Conversation(
        user_id=current_user.id,
        resume_id=resume.id,
        title=request.title
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "id": conversation.id,
        "title": conversation.title,
        "resume_id": conversation.resume_id
    }

@router.get("/conversations")
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == current_user.id
        )
        .order_by(Conversation.created_at.desc())
        .all()
    )

    return conversations
