import re
from typing import List

def clean_line(line: str) -> str:
    # collapse whitespace, strip non-word (but keep dots & hyphens), lowercase
    line = re.sub(r'\s+', ' ', line)
    line = re.sub(r'[^\w\s\.\-]', '', line)
    return line.strip().lower()

def extract_section(lines: List[str], header: str) -> List[str]:
    """
    Grabs lines after a header (singular or plural) until the next ALL-CAPS header.
    """
    # match "header" or "headers"
    pattern = re.compile(rf'^{header}s?\b', re.IGNORECASE)
    start = None
    section = []

    # find header line
    for i, raw in enumerate(lines):
        if pattern.search(raw):
            start = i + 1
            break

    # collect until the next uppercase header (or end)
    if start is not None:
        for raw in lines[start:]:
            if raw.isupper() and len(raw.split()) <= 4:
                break
            if raw.strip():
                section.append(raw)
    return [clean_line(r) for r in section]

def split_skills(skill_lines: List[str]) -> List[str]:
    """
    Splits each skill line into individual skills using colon and commas.
    Handles both comma-separated and space-separated formats.
    """
    skills = []
    for line in skill_lines:
        # Remove category label (e.g., "Languages:")
        if ':' in line:
            _, rest = line.split(':', 1)
        else:
            rest = line

        # Split on commas first
        parts = [p.strip() for p in rest.split(',') if p.strip()]
        # If no commas, fall back to space split
        if len(parts) <= 1:
            parts = [p.strip() for p in rest.split() if p.strip()]

        skills.extend(parts)

    return list(dict.fromkeys(skills))  # dedupe while preserving order

def parse_resume(raw_text: str) -> dict:
    """
    raw_text: full PDF text (with newlines)
    returns dict with lists for each section
    """
    # keep the original casing/lines so headers stay intact
    raw_lines = [ln for ln in raw_text.split('\n') if ln.strip()]

    education = extract_section(raw_lines, "education")
    experience = extract_section(raw_lines, "experience")
    projects = (
        extract_section(raw_lines, "project")
        or extract_section(raw_lines, "projects")
    )
    skill_lines = (
        extract_section(raw_lines, "skills")
        or extract_section(raw_lines, "technical skills")
    )
    skills = split_skills(skill_lines)

    return {
        "education": education,
        "experience": experience,
        "projects": projects,
        "skills": skills,
    }
