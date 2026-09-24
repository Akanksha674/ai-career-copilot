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