from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import tempfile
import os

from app.database import get_db
from app.models.resume import Resume
from app.services.pdf_service import extract_text_from_pdf
from app.auth.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(contents)
        temp_file_path = temp_file.name

    try:
        extracted_text = extract_text_from_pdf(temp_file_path)

    finally:
        os.remove(temp_file_path)

    new_resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        extracted_text=extracted_text
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "id": new_resume.id,
        "filename": new_resume.filename,
        "text": new_resume.extracted_text
    }