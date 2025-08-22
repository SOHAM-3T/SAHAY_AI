# local_test.py (at project root)

from pdf_parser import extract_text_from_pdf

# from text_preprocessing import clean_text  # optional
from resume_parser import parse_resume

raw = extract_text_from_pdf("Resume.pdf")
parsed = parse_resume(raw)

print("EDUCATION:", parsed["education"])
print("EXPERIENCE:", parsed["experience"])
print("PROJECTS:", parsed["projects"])
print("SKILLS:", parsed["skills"])
