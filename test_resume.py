from ai.resume_analyzer import analyze_resume
from ai.ats_score import calculate_ats

pdf = "uploads/Yogesh-A_Python-Developer.pdf"

result = analyze_resume(pdf)

score = calculate_ats(result)

print("=" * 50)
print("EMAIL")
print(result["email"])

print("=" * 50)
print("PHONE")
print(result["phone"])

print("=" * 50)
print("SKILLS")

for skill in result["skills"]:
    print("✔", skill)

print("=" * 50)
print("ATS SCORE")

print(score, "/100")