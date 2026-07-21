import re

from ai.resume_parser import extract_text
from ai.skill_extractor import extract_skills


def analyze_resume(pdf_path):

    text = extract_text(pdf_path)

    skills = extract_skills(text)

    email = ""

    phone = ""

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email_match:
        email = email_match.group()

    phone_match = re.search(
        r"\d{10}",
        text
    )

    if phone_match:
        phone = phone_match.group()

    return {

        "email": email,

        "phone": phone,

        "skills": skills,

        "text": text

    }