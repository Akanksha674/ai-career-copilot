from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/job",
    tags=["Job Description"]
)


class JobDescriptionRequest(BaseModel):
    job_description: str


SKILLS = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "TypeScript",
    "React",
    "FastAPI",
    "Flask",
    "SQL",
    "PostgreSQL",
    "MongoDB",
    "REST APIs",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "GenAI",
    "LLM",
    "RAG",
    "LangChain",
    "Docker",
    "Git",
    "AWS",
    "Azure",
    ]


def extract_skills(job_description: str):
    description_lower = job_description.lower()

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in description_lower:
            found_skills.append(skill)

    return found_skills

def extract_responsibilities(job_description: str):
    sentences = job_description.replace("\n", " ").split(".")

    responsibility_keywords = [
        "develop ",
        "design ",
        "build ",
        "create ",
        "implement ",
        "maintain ",
        "test ",
        "deploy ",
        "analyze ",
        "manage ",
        "collaborate ",
        "developing ",
        "building ",
        "implementing ",
    ]

    responsibilities = []

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_lower = sentence.lower()

        # Ignore common job-description introduction sentences
        if (
            sentence_lower.startswith("we are looking for")
            or sentence_lower.startswith("we're looking for")
            or sentence_lower.startswith("we seek")
            or sentence_lower.startswith("the ideal candidate")
        ):
            continue

        if any(
            keyword in sentence_lower
            for keyword in responsibility_keywords
        ):
            responsibilities.append(sentence + ".")

    return responsibilities

def extract_experience(job_description: str):
    import re

    patterns = [
        r"\b\d+\s*[-–]\s*\d+\s*(?:years?|yrs?)\s*(?:of\s+experience)?\b",
        r"\b\d+\+?\s*(?:years?|yrs?)\s*(?:of\s+experience)?\b",
        r"\b(?:freshers?|fresh graduate|entry[- ]level)\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, job_description, re.IGNORECASE)

        if match:
            return match.group(0)

    return ""

@router.post("/analyze")
def analyze_job_description(request: JobDescriptionRequest):

    if not request.job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty"
        )

    job_description = request.job_description

    skills = extract_skills(job_description)
    responsibilities = extract_responsibilities(job_description)
    experience = extract_experience(job_description)

    return {
        "message": "Job description analyzed successfully",
        "analysis": {
            "job_description": job_description,
            "skills": skills,
            "responsibilities": responsibilities,
            "experience": experience,
            "keywords": skills
        }
    }