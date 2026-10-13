from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.resume import Resume
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
