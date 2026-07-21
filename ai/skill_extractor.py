SKILLS = [

    "Python",
    "Flask",
    "Django",
    "FastAPI",

    "MySQL",
    "SQL",
    "SQLite",

    "HTML",
    "CSS",
    "JavaScript",

    "Bootstrap",
    "React",

    "Git",
    "GitHub",

    "Pandas",
    "NumPy",

    "Machine Learning",
    "Deep Learning",

    "TensorFlow",
    "PyTorch"
]


def extract_skills(text):

    detected = []

    text = text.lower()

    for skill in SKILLS:

        if skill.lower() in text:
            detected.append(skill)

    return sorted(set(detected))