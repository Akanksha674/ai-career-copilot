[1mdiff --git a/backend/app/main.py b/backend/app/main.py[m
[1mindex 94305e2..68709e4 100644[m
[1m--- a/backend/app/main.py[m
[1m+++ b/backend/app/main.py[m
[36m@@ -8,6 +8,7 @@[m [mfrom app.models.resume import Resume[m
 from app.routes.auth import router as auth_router[m
 from app.routes.resume import router as resume_router[m
 from app.routes.job import router as job_router[m
[32m+[m[32mfrom app.routes.career_assistant import router as career_assistant_router[m
 [m
 [m
 Base.metadata.create_all(bind=engine)[m
[36m@@ -30,6 +31,7 @@[m [mapp.add_middleware([m
 app.include_router(auth_router)[m
 app.include_router(resume_router)[m
 app.include_router(job_router)[m
[32m+[m[32mapp.include_router(career_assistant_router)[m
 [m
 @app.get("/")[m
 def root():[m
[1mdiff --git a/backend/app/routes/career_assistant.py b/backend/app/routes/career_assistant.py[m
[1mnew file mode 100644[m
[1mindex 0000000..f92ce15[m
[1m--- /dev/null[m
[1m+++ b/backend/app/routes/career_assistant.py[m
[36m@@ -0,0 +1,48 @@[m
[32m+[m[32mfrom fastapi import APIRouter, Depends, HTTPException[m
[32m+[m[32mfrom sqlalchemy.orm import Session[m
[32m+[m
[32m+[m[32mfrom app.database import get_db[m
[32m+[m[32mfrom app.auth.dependencies import get_current_user[m
[32m+[m[32mfrom app.models.user import User[m
[32m+[m[32mfrom app.models.resume import Resume[m
[32m+[m[32mfrom app.schemas.career_assistant import ([m
[32m+[m[32m    CareerQuestionRequest,[m
[32m+[m[32m    CareerAnswerResponse[m
[32m+[m[32m)[m
[32m+[m[32mfrom app.services.rag_service import answer_resume_question[m
[32m+[m
[32m+[m[32mrouter = APIRouter([m
[32m+[m[32m    prefix="/career-assistant",[m
[32m+[m[32m    tags=["Career Assistant"][m
[32m+[m[32m)[m
[32m+[m
[32m+[m[32m@router.post([m
[32m+[m[32m    "/ask",[m
[32m+[m[32m    response_model=CareerAnswerResponse[m
[32m+[m[32m)[m
[32m+[m[32mdef ask_career_assistant([m
[32m+[m[32m    request: CareerQuestionRequest,[m
[32m+[m[32m    db: Session = Depends(get_db),[m
[32m+[m[32m    current_user: User = Depends(get_current_user)[m
[32m+[m[32m):[m
[32m+[m[32m    resume = ([m
[32m+[m[32m    db.query(Resume)[m
[32m+[m[32m    .filter([m
[32m+[m[32m        Resume.id == request.resume_id,[m
[32m+[m[32m        Resume.user_id == current_user.id[m
[32m+[m[32m    )[m
[32m+[m[32m    .first()[m
[32m+[m[32m)[m
[32m+[m[32m    if resume is None:[m
[32m+[m[32m        raise HTTPException([m
[32m+[m[32m            status_code=404,[m
[32m+[m[32m            detail="Resume not found"[m
[32m+[m[32m        )[m
[32m+[m[41m    [m
[32m+[m[32m    answer = answer_resume_question([m
[32m+[m[32m        question=request.question,[m
[32m+[m[32m        user_id=current_user.id,[m
[32m+[m[32m        resume_id=resume.id[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    return CareerAnswerResponse(answer=answer)[m
\ No newline at end of file[m
[1mdiff --git a/backend/app/schemas/career_assistant.py b/backend/app/schemas/career_assistant.py[m
[1mnew file mode 100644[m
[1mindex 0000000..43cd86f[m
[1m--- /dev/null[m
[1m+++ b/backend/app/schemas/career_assistant.py[m
[36m@@ -0,0 +1,8 @@[m
[32m+[m[32mfrom pydantic import BaseModel[m
[32m+[m
[32m+[m[32mclass CareerQuestionRequest(BaseModel):[m
[32m+[m[32m    question: str[m
[32m+[m[32m    resume_id: int[m
[32m+[m
[32m+[m[32mclass CareerAnswerResponse(BaseModel):[m
[32m+[m[32m    answer: str[m
\ No newline at end of file[m
