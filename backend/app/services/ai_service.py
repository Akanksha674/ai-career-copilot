import ollama


def analyze_job_description(job_description: str):
    prompt = f"""
Analyze the following job description.

Extract the following information:

1. Job title
2. Required technical skills
3. Responsibilities
4. Required experience
5. Education requirements
6. Important keywords

Job Description:
{job_description}

Return the result in a clear and structured format.
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

    return response["message"]["content"]