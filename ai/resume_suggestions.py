def get_resume_suggestions(result):

    suggestions = []

    skills = [s.lower() for s in result["skills"]]

    if len(result["skills"]) < 5:
        suggestions.append("Add more technical skills.")

    if "python" not in skills:
        suggestions.append("Include Python if you have experience.")

    suggestions.append("Add your GitHub profile.")

    suggestions.append("Add your LinkedIn profile.")

    suggestions.append("Mention certifications.")

    suggestions.append("Use strong action verbs in project descriptions.")

    suggestions.append("Keep your resume to one page.")

    return suggestions