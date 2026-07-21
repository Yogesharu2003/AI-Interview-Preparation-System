from ai.resume_parser import extract_text
from ai.skill_extractor import extract_skills

pdf_path = "uploads/Yogesh-A_Python-Developer.pdf"

text = extract_text(pdf_path)

print("=" * 50)
print("RESUME TEXT")
print("=" * 50)

print(text)

print("\n")

skills = extract_skills(text)

print("=" * 50)
print("DETECTED SKILLS")
print("=" * 50)

for skill in skills:
    print("✔", skill)