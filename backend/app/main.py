from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.routes.auth import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Career Copilot API",
    description="Backend API for the AI Career Copilot",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "AI Career Copilot API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }