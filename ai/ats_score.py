def calculate_ats(result):

    score = 0

    # Email
    if result["email"]:
        score += 10

    # Phone
    if result["phone"]:
        score += 10

    # Skills
    score += min(len(result["skills"]) * 5, 40)

    # Education
    education_keywords = [
        "B.Tech",
        "B.E",
        "M.Tech",
        "MCA",
        "B.Sc",
        "M.Sc",
        "MBA"
    ]

    if any(word.lower() in result["text"].lower() for word in education_keywords):
        score += 20

    # Projects
    project_keywords = [
        "project",
        "projects",
        "developed",
        "application"
    ]

    if any(word.lower() in result["text"].lower() for word in project_keywords):
        score += 20

    return min(score, 100)