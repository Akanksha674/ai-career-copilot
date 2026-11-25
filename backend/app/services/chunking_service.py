import re

def is_project_heading(line: str) -> bool:
    pattern = r"^.+\|.+$"
    return bool(re.match(pattern, line.strip()))

def extract_project_name(heading: str) -> str:
    return heading.split("|", 1)[0].strip()

def is_section_heading(line: str) -> bool:
    section_headings = {
        "PROFESSIONAL SUMMARY",
        "TECHNICAL SKILLS",
        "PROJECTS",
        "TECHNICAL EXPERIENCE",
        "EDUCATION",
        "CERTIFICATIONS & ACHIEVEMENTS"
    }

    return line.strip().upper() in section_headings

def get_resume_sections(text: str) -> dict[str, str]:
    sections = {}
    current_section = None
    current_lines = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if is_section_heading(line):
            if current_section:
                sections[current_section] = "\n".join(current_lines)

            current_section = line.upper()
            current_lines = []

        elif current_section:
            current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines)

    return sections

def split_text_into_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[str]:
    if not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

if __name__ == "__main__":
    print(is_project_heading(
        "RAG-Based AI Teaching Assistant | Python, BGE-M3"
    ))

    print(is_project_heading(
        "Built an end-to-end RAG application"
    ))

def split_into_projects(text: str) -> list[str]:
    projects = []
    current_project = []
    inside_projects_section = False

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        # Start collecting when PROJECTS section begins
        if line.upper() == "PROJECTS":
            inside_projects_section = True
            continue

        # Stop when another resume section begins
        if inside_projects_section and is_section_heading(line):
            if current_project:
                projects.append("\n".join(current_project))
                current_project = []
            break

        if not inside_projects_section:
            continue

        # Start a new project
        if is_project_heading(line):
            if current_project:
                projects.append("\n".join(current_project))

            current_project = [line]

        elif current_project:
            current_project.append(line)

    if current_project:
        projects.append("\n".join(current_project))

    return projects

if __name__ == "__main__":
    sample_text = """
PROJECTS

RAG-Based AI Teaching Assistant | Python, BGE-M3
Built a RAG application for video lectures.
Used Whisper for transcription.

Career Copilot | Python, FastAPI, Qdrant
Built an AI-powered career assistant.
"""

    projects = split_into_projects(sample_text)

    for index, project in enumerate(projects, start=1):
        print(f"\n--- Project {index} ---")
        print(project)

def create_metadata_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[dict]:

    metadata_chunks = []

    sections = get_resume_sections(text)

    for section_name, section_text in sections.items():

        # Handle individual projects separately
        if section_name == "PROJECTS":

            projects = split_into_projects("PROJECTS\n" + section_text)

            for project in projects:

                lines = project.splitlines()
                heading = lines[0]

                project_name = extract_project_name(heading)

                project_chunks = split_text_into_chunks(
                    project,
                    chunk_size,
                    overlap
                )

                for chunk in project_chunks:
                    metadata_chunks.append({
                        "text": chunk,
                        "section": section_name,
                        "project_name": project_name
                    })

        # Handle all other resume sections
        else:
            chunks = split_text_into_chunks(
                section_text,
                chunk_size,
                overlap
            )

            for chunk in chunks:
                metadata_chunks.append({
                    "text": chunk,
                    "section": section_name,
                    "project_name": None
                })

    return metadata_chunks