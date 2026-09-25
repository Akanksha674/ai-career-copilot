import json
import ollama


def analyze_job_description(job_description: str):
    prompt = f"""
Analyze the following job description.

Return ONLY valid JSON.
Do not include markdown.
Do not include ```json.
Do not include any explanation outside the JSON.

Use exactly this structure:

{{
    "job_title": "",
    "technical_skills": [],
    "responsibilities": [],
    "experience": "",
    "education": "",
    "keywords": []
}}

Rules:
- Extract only information present in the job description.
- If experience is not mentioned, use "None specified".
- If education is not mentioned, use "None specified".
- technical_skills must be an array of strings.
- responsibilities must be an array of strings.
- keywords must be an array of important job-related terms.
- Do not invent information.

Job Description:
{job_description}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "raw_analysis": content
        }

def match_resume_with_job(resume_text: str, job_description: str):
    prompt = f"""
Compare the candidate's resume with the job description.

Return ONLY valid JSON.
Do not include markdown.
Do not include ```json.
Do not include any explanation outside the JSON.

Use exactly this structure:

{{
    "match_percentage": 0,
    "matching_skills": [],
    "missing_skills": [],
    "strengths": [],
    "skill_gaps": [],
    "suggestions": []
}}

Rules:
- match_percentage must be a number between 0 and 100.
- matching_skills must contain skills present in both the resume and job description.
- missing_skills must contain important job-related skills present in the job description but missing from the resume.
- strengths must describe relevant experience, projects, education, or skills found in the resume.
- skill_gaps must describe important areas the candidate should improve.
- suggestions must provide practical recommendations for improving the candidate's fit for this job.
- Do not invent information that is not present in the resume or job description.

CANDIDATE RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        cleaned_content = content.strip()

        if cleaned_content.startswith("```json"):
            cleaned_content = cleaned_content[7:]

        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3]

        cleaned_content = cleaned_content.strip()

        try:
            return json.loads(cleaned_content)
        except json.JSONDecodeError:
            return {
                "raw_analysis": content
            }